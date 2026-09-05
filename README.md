# Moodle

Personal Moodle environment for programming courses and question banks, using the CodeRunner question type and a Jobe sandbox to run submitted code.

## What you need

- Docker with the Compose plugin
- [just](https://just.systems)
- Python 3, for the course package checks
- A VPS with a public IPv4 address

## Setup

On the VPS, follow [vps/README.md](vps/README.md) to configure WireGuard and Caddy. Add a DNS A record for `moodle.alanjam.com` pointing at the VPS. On the VM, clone this repository and run:

```
sudo ./scripts/setup-wireguard.sh <VPS public IP>
just setup
```

The setup script tells you if it needs anything else.

## Commands

- `just setup` validates every course package, starts the stack, and creates any missing course. Run it again any time; complete courses are left unchanged.
- `just deploy` fast-forwards the checkout, syncs the pinned plugin submodules, pulls the registry images, rebuilds the Jobe image, and restarts the stack. It never touches course content.
- `just import courses/go/topic-14.xml` replaces one topic's questions in its course and rebuilds that topic's quiz. If the quiz has attempts, the import refuses and changes nothing.
- `just down` stops the stack and keeps the data volumes.

## Course packages

Each directory under `courses/` that holds a `manifest.json` is one course. The manifest names the course, lists any CodeRunner prototype files, and declares each topic file with its WAT range and question count. `tools/validate-course-packages.py` checks every package before setup or import touches Moodle. A directory without a manifest is ignored, which keeps test fixtures such as `tests/smoke-go/` off the live site.

## Go grading

The Go course grades inside the Jobe sandbox. The `jobe` service builds a local image from the pinned Jobe digest plus the Go 1.27.1 toolchain; see `jobe/Dockerfile`. Neither the VM nor a workstation needs Go installed.

## Invite someone

Public registration is off. Add accounts through the Moodle admin interface, as described in [Create a user](https://docs.moodle.org/502/en/Create_a_user).
