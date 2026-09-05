#!/usr/bin/env bash
# Replace one module's questions in the Moodle question bank and rebuild its
# quiz in a single transaction, then re-validate the whole bank through Jobe.
# The XML file must live directly in a course package: a directory under
# courses/ holding a manifest.json that declares the module.
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ $# -ne 1 ]]; then
    echo "Usage: just import <file.xml>" >&2
    exit 1
fi

xml_file="$1"
if [[ "$xml_file" != *.xml || ! -r "$xml_file" ]]; then
    echo "Cannot read XML file $xml_file" >&2
    exit 1
fi

package_dir="$(dirname "$xml_file")"
manifest="$package_dir/manifest.json"
if [[ ! -r "$manifest" ]]; then
    echo "Cannot read $manifest: $xml_file must live directly in a course package (a directory under courses/ holding manifest.json)" >&2
    exit 1
fi

# Fail fast on package inconsistency before touching the container.
python3 tools/validate-course-packages.py courses

container_id="$(docker compose ps -q moodle)"
# Stage under the original file name; sync-topic.php matches the basename
# against the manifest's module list. Clear the staging directory as root
# because docker cp creates files owned by root.
docker compose exec -u root -T moodle rm -rf /tmp/sync
docker compose exec -T moodle mkdir -p /tmp/sync
docker cp "$xml_file" "$container_id":/tmp/sync/
docker cp "$manifest" "$container_id":/tmp/sync/manifest.json
docker cp scripts/moodle/sync-topic.php "$container_id":/tmp/sync-topic.php
docker compose exec -T moodle php /tmp/sync-topic.php "/tmp/sync/$(basename "$xml_file")" /tmp/sync/manifest.json
