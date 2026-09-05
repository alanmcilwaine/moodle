set shell := ["bash", "-euo", "pipefail", "-c"]

# List available recipes
default:
    @just --list

# Set up the VM and build the course; safe to re-run
setup:
    ./scripts/setup-course.sh

# Rebuild and validate both courses in an isolated local Moodle project
rehearse:
    ./scripts/rehearse.sh

# Remove only the isolated local rehearsal project and its volumes
rehearse-down:
    docker compose -p moodle-go-test -f compose.yaml -f compose.test.yaml down -v

# Pull the latest code, rebuild the Jobe image, then restart the stack
deploy:
    git pull --ff-only
    git submodule update --init
    docker compose pull postgres moodle
    docker compose build jobe
    docker compose up -d --force-recreate jobe
    docker compose up -d

# Replace one module's questions in the course question bank and rebuild its quiz
import xml:
    ./scripts/import-questions.sh "{{xml}}"

# Stop the stack; data volumes are kept
down:
    docker compose down
