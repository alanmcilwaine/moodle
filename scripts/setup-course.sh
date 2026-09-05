#!/usr/bin/env bash
# One-time setup: prepare local configuration, start the stack, and build the
# course packages under courses/. Safe to re-run.
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v python3 >/dev/null; then
    echo "python3 is required to validate course packages." >&2
    exit 1
fi
python3 tools/validate-course-packages.py courses

if ! command -v docker >/dev/null; then
    echo "docker is required. See README.md for VM setup." >&2
    exit 1
fi
if ! docker compose version >/dev/null; then
    echo "the docker compose plugin is required." >&2
    exit 1
fi
if ! docker info >/dev/null 2>&1; then
    echo "Cannot reach the docker daemon as $(whoami)." >&2
    echo "Add yourself to the docker group, then log out and back in:" >&2
    echo "  sudo usermod -aG docker $(whoami)" >&2
    exit 1
fi

if [[ ! -f .env ]]; then
    cp .env.example .env
    echo "Created .env from .env.example. Fill it in, then run just setup again." >&2
    exit 1
fi

if ! ip link show wg0 >/dev/null 2>&1; then
    echo "WireGuard is not configured." >&2
    echo "Run: sudo ./scripts/setup-wireguard.sh <VPS public IP>" >&2
    exit 1
fi

git submodule update --init

docker compose up -d

container_id="$(docker compose ps -q moodle)"

echo "Waiting for Moodle to finish installing. The first run takes a few minutes."
deadline=$((SECONDS + 900))
until [[ "$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}starting{{end}}' "$container_id")" == "healthy" ]]; do
    if (( SECONDS > deadline )); then
        echo "Moodle did not become healthy within 15 minutes. Check docker compose logs moodle." >&2
        exit 1
    fi
    sleep 5
done

# Point CodeRunner at the local Jobe container. Without this it silently
# grades through the plugin's default public Jobe server.
docker compose exec -T moodle php /var/www/html/admin/cli/cfg.php \
    --component=qtype_coderunner --name=jobe_host --set=jobe

# Fail fast if the jobe service name does not resolve from the moodle
# container. A stale network attachment otherwise surfaces as "sandbox down"
# at submission time.
if ! docker compose exec -T moodle curl -sf -m 10 http://jobe/jobe/index.php/restapi/languages >/dev/null; then
    echo "Moodle cannot reach the jobe service." >&2
    echo "Try: docker compose up -d --force-recreate jobe" >&2
    exit 1
fi

shopt -s nullglob
course_manifests=(courses/*/manifest.json)
if (( ${#course_manifests[@]} == 0 )); then
    echo "No course packages found under courses/." >&2
    exit 1
fi

docker cp scripts/moodle/bootstrap-course.php "$container_id":/tmp/bootstrap-course.php
docker cp scripts/moodle/sync-prototypes.php "$container_id":/tmp/sync-prototypes.php

for manifest in "${course_manifests[@]}"; do
    course_dir="${manifest%/manifest.json}"
    course_name="${course_dir##*/}"
    container_course_dir="/tmp/course/$course_name"

    echo "Building the course package from $manifest..."
    # Restage from scratch so deleted source files do not linger in the container.
    # docker cp creates subdirectories as root, so the cleanup must run as root.
    docker compose exec -u root -T moodle rm -rf "$container_course_dir"
    docker compose exec -T moodle mkdir -p "$container_course_dir"
    docker cp "$course_dir/." "$container_id:$container_course_dir/"
    docker compose exec -T moodle php /tmp/bootstrap-course.php "$container_course_dir/manifest.json" "$container_course_dir"
    docker compose exec -T moodle php /tmp/sync-prototypes.php "$container_course_dir/manifest.json" "$container_course_dir"
done

echo "Done. Open https://moodle.alanjam.com once the VPS is proxying. Log in with the admin credentials from .env"
