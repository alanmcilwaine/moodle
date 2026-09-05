#!/usr/bin/env bash
# Build both courses from scratch in an isolated local Moodle project.
set -euo pipefail

cd "$(dirname "$0")/.."

readonly PROJECT="moodle-go-test"
readonly WAIT_SECONDS="${MOODLE_REHEARSAL_WAIT_SECONDS:-900}"
compose=(docker compose -p "$PROJECT" -f compose.yaml -f compose.test.yaml)

die() {
    printf 'error: %s\n' "$*" >&2
    exit 1
}

stable_course_state() {
    "${compose[@]}" exec -T moodle php /tmp/course-state.php "$1" |
        python3 -c 'import json, sys; state = json.load(sys.stdin); state["question_count"] = len(state.pop("questions")); print(json.dumps(state, sort_keys=True))'
}

test_topic_import() {
    local container_id="$1"
    local topic="courses/go/topic-05.xml"
    local quiz="Topic 5: Flow control: for, switch, and if with a short statement"
    local before
    local after
    local stable_before
    local stable_after

    "${compose[@]}" exec -u root -T moodle rm -rf /tmp/sync
    "${compose[@]}" exec -T moodle mkdir -p /tmp/sync
    docker cp "$topic" "$container_id:/tmp/sync/topic-05.xml" >/dev/null
    docker cp courses/go/manifest.json "$container_id:/tmp/sync/manifest.json" >/dev/null

    before="$("${compose[@]}" exec -T moodle php /tmp/course-state.php go)"
    if "${compose[@]}" exec -T -e MOODLE_SYNC_TEST_FAIL_AFTER_DELETE=1 moodle \
        php /tmp/sync-topic.php /tmp/sync/topic-05.xml /tmp/sync/manifest.json; then
        die "the injected topic-sync failure unexpectedly succeeded"
    fi
    after="$("${compose[@]}" exec -T moodle php /tmp/course-state.php go)"
    [[ "$before" == "$after" ]] || die "the topic-sync rollback changed course state"

    "${compose[@]}" exec -T moodle php /tmp/rehearsal-attempt.php create go "$quiz"
    before="$("${compose[@]}" exec -T moodle php /tmp/course-state.php go)"
    if "${compose[@]}" exec -T moodle \
        php /tmp/sync-topic.php /tmp/sync/topic-05.xml /tmp/sync/manifest.json; then
        "${compose[@]}" exec -T moodle php /tmp/rehearsal-attempt.php remove go "$quiz"
        die "topic sync ignored an existing quiz attempt"
    fi
    after="$("${compose[@]}" exec -T moodle php /tmp/course-state.php go)"
    "${compose[@]}" exec -T moodle php /tmp/rehearsal-attempt.php remove go "$quiz"
    [[ "$before" == "$after" ]] || die "the refused topic sync changed course state"

    "${compose[@]}" exec -T moodle php /tmp/sync-topic.php /tmp/sync/topic-05.xml /tmp/sync/manifest.json
    stable_before="$(stable_course_state go)"
    "${compose[@]}" exec -T moodle php /tmp/sync-topic.php /tmp/sync/topic-05.xml /tmp/sync/manifest.json
    stable_after="$(stable_course_state go)"
    [[ "$stable_before" == "$stable_after" ]] || die "repeated topic sync did not converge"
}

for command in docker python3; do
    command -v "$command" >/dev/null || die "$command is required"
done
docker compose version >/dev/null || die "the Docker Compose plugin is required"
docker info >/dev/null 2>&1 || die "the Docker daemon is unavailable"
[[ -r .env ]] || die "create .env from .env.example before running the rehearsal"
[[ -r compose.test.yaml ]] || die "compose.test.yaml is missing"

python3 tools/validate-course-packages.py courses
git submodule update --init
"${compose[@]}" config >/dev/null

printf 'Removing only Docker resources labelled for %s.\n' "$PROJECT"
docker ps -a --filter "label=com.docker.compose.project=$PROJECT" --format '  {{.Names}} {{.Status}}'
docker volume ls --filter "label=com.docker.compose.project=$PROJECT" --format '  {{.Name}}'
"${compose[@]}" down -v

"${compose[@]}" build jobe
"${compose[@]}" up -d

container_id="$("${compose[@]}" ps -q moodle)"
[[ -n "$container_id" ]] || die "the Moodle container did not start"

printf 'Waiting for Moodle to become healthy.\n'
deadline=$((SECONDS + WAIT_SECONDS))
until [[ "$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}starting{{end}}' "$container_id")" == "healthy" ]]; do
    if ((SECONDS > deadline)); then
        die "Moodle did not become healthy within ${WAIT_SECONDS}s"
    fi
    sleep 5
done

curl --silent --show-error --fail --max-redirs 0 --output /dev/null \
    http://127.0.0.1:8081/login/index.php
"${compose[@]}" exec -T moodle php /var/www/html/admin/cli/upgrade.php --non-interactive --allow-unstable
"${compose[@]}" exec -T moodle php /var/www/html/admin/cli/cfg.php \
    --component=qtype_coderunner --name=jobe_host --set=jobe
"${compose[@]}" exec -T moodle curl -sf -m 10 http://jobe/jobe/index.php/restapi/languages >/dev/null
"${compose[@]}" exec -T jobe /usr/bin/go version

for script in scripts/moodle/*.php; do
    docker cp "$script" "$container_id:/tmp/$(basename "$script")" >/dev/null
    "${compose[@]}" exec -T moodle php -l "/tmp/$(basename "$script")"
done

docker run --rm --entrypoint /bin/bash \
    -v "$(pwd):/work" -w /work jobe-go:1.27.1 \
    -lc 'python3 tools/simulate-grader-go.py --go /usr/bin/go courses/go/topic-*.xml'
python3 tools/simulate-grader.py courses/python/topic-*.xml

for manifest in courses/*/manifest.json; do
    course_dir="${manifest%/manifest.json}"
    course_name="${course_dir##*/}"
    container_course_dir="/tmp/course/$course_name"

    "${compose[@]}" exec -u root -T moodle rm -rf "$container_course_dir"
    "${compose[@]}" exec -T moodle mkdir -p "$container_course_dir"
    docker cp "$course_dir/." "$container_id:$container_course_dir/" >/dev/null
    if [[ "$course_name" == "go" ]]; then
        if "${compose[@]}" exec -T -e MOODLE_BOOTSTRAP_TEST_FAIL_AFTER_IMPORTS=1 moodle \
            php /tmp/bootstrap-course.php "$container_course_dir/manifest.json" "$container_course_dir"; then
            die "the injected bootstrap failure unexpectedly succeeded"
        fi
        printf 'The partial Go course was removed after the injected bootstrap failure.\n'
    fi
    "${compose[@]}" exec -T moodle php /tmp/bootstrap-course.php \
        "$container_course_dir/manifest.json" "$container_course_dir"
    if [[ "$course_name" == "go" ]]; then
        "${compose[@]}" exec -T -e MOODLE_SYNC_PROTOTYPE_TEST_FORCE_UPDATE=1 moodle \
            php /tmp/sync-prototypes.php "$container_course_dir/manifest.json" "$container_course_dir"
    fi
    "${compose[@]}" exec -T moodle php /tmp/sync-prototypes.php \
        "$container_course_dir/manifest.json" "$container_course_dir"
    "${compose[@]}" exec -T moodle php /tmp/validate-questions.php "$course_name"
    before="$("${compose[@]}" exec -T moodle php /tmp/course-state.php "$course_name")"
    "${compose[@]}" exec -T moodle php /tmp/bootstrap-course.php \
        "$container_course_dir/manifest.json" "$container_course_dir"
    after="$("${compose[@]}" exec -T moodle php /tmp/course-state.php "$course_name")"
    [[ "$before" == "$after" ]] || die "repeated bootstrap changed the $course_name course"
    if [[ "$course_name" == "go" ]]; then
        test_topic_import "$container_id"
        "${compose[@]}" exec -T moodle php /tmp/validate-questions.php go
    fi
done

printf 'Rehearsal passed. Moodle remains available at http://127.0.0.1:8081 for inspection.\n'
