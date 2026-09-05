# Adding Go to the Moodle + CodeRunner + Jobe stack

Research findings, 2026-09-02. Read-only investigation. Local sources are the reference clones at `~/wats/reference/jobe` and `~/wats/reference/moodle-qtype_coderunner` (the latter is the copy mounted into the running Moodle container per `~/wats/moodle/docker-compose.yml`).

## 1. How Jobe language tasks work, and what GoTask.php needs

Files read. `~/wats/reference/jobe/app/Libraries/LanguageTask.php`, `CTask.php`, `JavaTask.php`, `~/wats/reference/jobe/app/Controllers/Runs.php`, `~/wats/reference/jobe/app/Controllers/Languages.php`, `~/wats/reference/jobe/app/Models/LanguagesModel.php`, `~/wats/reference/jobe/app/Config/Jobe.php`, `~/wats/reference/jobe/runguard/runguard.c`.

Dispatch. `Runs.php` line 43 builds the class name from the request. `"\\Jobe\\" . ucwords($run->language_id) . 'Task'`. A run with `language_id: "go"` instantiates `\Jobe\GoTask`. The flow per job is `prepareExecutionEnvironment` (temp dir under `/home/jobe/runs`, source file written, a `jobeNN` user allocated), then `compile()`, then `execute()` if `cmpinfo` is empty, then `close()`.

Discovery. `LanguagesModel::supportedLanguages()` scans `app/Libraries/` for files ending `Task.php`, calls each class's static `getVersion()`, and lists the language only when the version command succeeds. The result is cached in `/tmp/jobe_language_cache_file`. Adding a language means dropping `GoTask.php` into `app/Libraries/`, having the toolchain on the PATH of the web server user, and deleting the cache file (or restarting the container). The version probe runs as `www-data` outside the sandbox via PHP `exec`, so `go` must resolve there. `setPath()` falls back to `/sbin:/bin:/usr/sbin:/usr/bin`, which finds an apt-installed `/usr/bin/go` but not a tarball install at `/usr/local/go/bin`.

What GoTask.php must define, modelled on CTask.php.

- `getVersionCommand()`. Return `array('go version', '/go version go([0-9.]+)/')`.
- `defaultFileName($sourcecode)`. Return `'prog.go'`.
- `compile()`. Run `go build -o prog.exe prog.go` through `runInSandbox($cmd)` with environment prepended, for example `GOCACHE=/tmp/.go-cache GOPATH=/tmp/.go-path go build -o prog.exe prog.go`. Stderr lands in `cmpinfo`, which flags a compilation error result.
- `getExecutablePath()`. Return `"./" . $this->executableFileName`. `getTargetFile()` returns `''` (compiled language convention, per the comment block at LanguageTask.php lines 413 to 426).
- Constructor overrides, the JavaTask precedent (see section 3). Set `$params['memorylimit'] = 0`, raise `numprocs`, and raise `min_params_compile['cputime']` above the 2 second global minimum (LanguageTask.php line 52) because a cold-cache build exceeds it.

The sandbox. `runInSandbox()` wraps every compile and run in `runguard` with `--cputime`, `--time` (wall kill at 2x cputime), `--nproc`, `--streamsize`, `--memsize`, and `--filesize`. Defaults are 400 MB memory and 5 s CPU for runs, with compile minima of 500 MB and 2 s (LanguageTask.php lines 35 to 57).

## 2. Prior art

The decisive find. CodeRunner itself already supports Go through its built-in multilanguage question type. PR [trampgeek/moodle-qtype_coderunner#179](https://github.com/trampgeek/moodle-qtype_coderunner/pull/179) ("extension of multilanguage for Perl, PHP, Ruby, JavaScript, C#, Golang", author rmallah of redgrape-tech) was merged by Richard Lobb on 26 October 2023. It edits `db/builtin_PROTOTYPES.xml`. The golang branch of the template writes the answer to `tester.go`, runs `subprocess.run(["go", "build", "-o", "tester.exe", filename], env={"GOCACHE": "/tmp/.go-cache"})`, then executes `./tester.exe`. This code is present in the mounted clone at `~/wats/reference/moodle-qtype_coderunner/db/builtin_PROTOTYPES.xml` lines 673 to 731, so the running Moodle already ships it. The Jobe server only needs the `go` binary installed. No GoTask.php is required because the sandbox language stays `python3`.

Upstream Jobe. No GoTask exists in [trampgeek/jobe](https://github.com/trampgeek/jobe), matching the running server's language list. A GitHub issues and PR search over the repo (`api.github.com/search/issues`, queries for "golang" and "go language") found no Go PR. The only language-addition PRs are [Pascal #5](https://github.com/trampgeek/jobe/pull/5) and [VHDL #37](https://github.com/trampgeek/jobe/pull/37), which confirm that new languages land as single `*Task.php` files. A scan of the 82 forks (`api.github.com/repos/trampgeek/jobe/forks`) surfaced none advertising Go.

Forum threads. A Moodle.org thread asks exactly this question, [How to Add Go Lang Support for CodeRunner](https://moodle.org/mod/forum/discuss.php?d=449685) (direct fetch returned HTTP 403, content taken from search snippets). It predates PR 179 and redirects to the [CodeRunner Question Authors' Forum](https://coderunner.org.nz/mod/forum/view.php?id=51). Site-restricted searches of coderunner.org.nz found no dedicated Go thread. The [CodeRunner docs](https://trampgeek.github.io/moodle-qtype_coderunner/) state that languages beyond the built-ins are supported via custom question types without source changes.

## 3. Pitfalls of `go build` under runguard

GOCACHE. Since Go 1.12 the build cache is mandatory. With GOCACHE, XDG_CACHE_HOME, and HOME all unset, `go build` fails with "build cache is required, but could not be located", and an unwritable cache dir fails with "failed to initialize build cache" (Go's own test [build_nocache.txt](https://go.dev/src/cmd/go/testdata/script/build_nocache.txt) and [cache/default.go](https://go.dev/src/cmd/go/internal/cache/default.go)). The sandbox user has no HOME, so GOCACHE must be set to an absolute writable path. PR 179 uses `/tmp/.go-cache`.

Cache survival. Jobe wipes per-user files after every run. `LanguageTask::removeTemporaryFiles()` runs `find $dir -user $user -delete` over `clean_up_path`, which defaults to `/tmp;/var/tmp;/var/crash;/run/lock;/var/lock` (Jobe.php line 42). Cache entries a `jobeNN` user writes to `/tmp/.go-cache` are deleted when its run closes. Every submission therefore compiles cold unless the cache is pre-warmed by root at image build time (`go build std`, then `chmod -R a+rwX`), because root-owned files survive the per-user find.

Memory. Runguard's `--memsize` sets rlimits ("all (total, stack, etc) memory limits", runguard.c lines 261 and 573 to 575), so RLIMIT_AS applies. The Go runtime reserves large virtual address regions at startup, and Linux counts even PROT_NONE reservations against RLIMIT_AS, so Go binaries can die immediately under a modest `ulimit -v` (LKML thread [mmap, the language go, problems with the linux kernel](https://lkml.iu.edu/hypermail/linux/kernel/1102.1/00738.html), plus golang/go issues [#22871](https://github.com/golang/go/issues/22871) and [#52576](https://github.com/golang/go/issues/52576)). The precedent is JavaTask.php lines 22 to 39. It sets `$params['memorylimit'] = 0` to disable the rlimit entirely, lets the JVM flags (`-Xss8m -Xmx200m`) bound real usage, and forces `numprocs` to at least 256. The multilanguage prototype instead sets `memlimitmb` to 16000 and `numprocs` to 50 in its sandbox params (builtin_PROTOTYPES.xml lines 772 to 774), which is high enough in practice.

Modules and network. No pitfall for single-file stdlib-only programs. `go build prog.go` outside any module builds as the command-line-arguments package with no network access needed. Verified locally with go 1.26.2 in an environment containing only PATH and GOCACHE (no HOME, no GOPATH, no go.mod). `GOFLAGS=-mod=mod` or vendoring only matters once third-party imports appear, which exact-match stdout WATs do not need.

PATH under the wrapper. PR 179 calls `subprocess.run(..., env={"GOCACHE": ...})`, which drops PATH. Python then resolves the executable via `os.defpath` (`/bin:/usr/bin`). An apt install (`golang-go` puts `/usr/bin/go`) works. A tarball install under `/usr/local/go` silently fails unless symlinked into `/usr/bin`.

Compile latency, measured on this host (the machine class running the stack). Cold cache build of a two-line fmt program took 4.9 s wall and 9.5 s user CPU. Warm cache took 0.14 s. A cold build also risks the runguard wall-clock kill at 2x cputime and the 2 s compile CPU minimum if run through a native GoTask, and risks the question's CPU limit under the python wrapper. Pre-warming the cache in the image removes the problem.

## 4. The CodeRunner side

Question types are prototype questions. A prototype is a CodeRunner question with `prototypetype` set, whose `coderunnertype` name becomes selectable in child questions. The prototype carries the Twig template CodeRunner expands and posts to Jobe, plus the `language` field, which is the Jobe `language_id` the run is submitted under. Built-ins live in `db/builtin_PROTOTYPES.xml`. There is no `go_program` built-in. Go arrives only through `BUILT_IN_PROTOTYPE_multilanguage` (lines 629 onward of the local clone), whose sandbox language is `python3` and whose Ace language list is `c,cpp,java,python3,perl,php,ruby,javascript,c#,golang`.

Templates run per test or combined. The multilanguage template is per-test (`iscombinatortemplate` 0), so every test case is a separate Jobe POST that recompiles the program. `classes/jobrunner.php` lines 133 to 138 show the combinator path runs only when the template is a combinator and either no test has stdin, `allowmultiplestdins` is set, or the grader is a template grader. Grading here is exact-match stdout, which is CodeRunner's default `EqualityGrader`, already the multilanguage prototype's grader.

A combinator-style Go template would be a python3 script that compiles once and loops the tests, with `allowmultiplestdins` enabled so stdin-bearing tests still combine. Sketch.

```
import subprocess, os
open('prog.go', 'w').write("""{{ STUDENT_ANSWER | e('py') }}""")
env = {'GOCACHE': '/tmp/.go-cache', 'PATH': '/usr/bin:/bin'}
cp = subprocess.run(['go', 'build', '-o', 'prog.exe', 'prog.go'],
                    env=env, capture_output=True, text=True)
if cp.returncode != 0:
    raise Exception('** Compilation failed **\n' + cp.stderr)
{% for TEST in TESTCASES %}
r = subprocess.run(['./prog.exe'], input="""{{ TEST.stdin | e('py') }}""",
                   capture_output=True, text=True)
print(r.stdout)
print('#<ab@17943918#@>#')
{% endfor %}
```

The separator line must match the prototype's test splitter. One Jobe POST grades the whole submission, and ANSWER_LANGUAGE is not needed because the type is Go-only. Note the multilanguage type's language dropdown only appears when `acelang` contains a comma (renderer.php lines 636 to 642), and `question.php` lines 746 to 752 only default the sample-answer language from a comma-separated list, so a dedicated Go prototype is cleaner than a single-language multilanguage question.

## 5. Smallest viable path, end to end

Written during the investigation. The deployed variant is this repository's jobe/Dockerfile, which adds the Go 1.27.1 tarball to the pinned Jobe digest instead of the apt route below.

The multilanguage route needs no Jobe code change at all, and the CodeRunner side is already deployed. That makes it the smallest path. A native GoTask.php is a later optimisation, not a prerequisite.

1. Write `~/wats/moodle/jobe/Dockerfile`. `FROM trampgeek/jobeinabox:latest`, then `RUN apt-get update && apt-get install -y --no-install-recommends golang-go && rm -rf /var/lib/apt/lists/*`, then pre-warm with `RUN GOCACHE=/tmp/.go-cache go build std && chmod -R a+rwX /tmp/.go-cache`. Base image is Ubuntu 24.04 (jobeinabox Dockerfile, fetched from raw.githubusercontent.com), so apt gives Go 1.22, ample for WATs.
2. Point the compose `jobe` service at the Dockerfile (`build: ./jobe` replacing `image:`) and rebuild that one service. No Moodle change.
3. Smoke-test Jobe directly. POST a run with `language_id: python3` whose script performs the golang branch of the multilanguage template (write tester.go, `go build` with `GOCACHE=/tmp/.go-cache`, run it). This proves the toolchain, cache permissions, and PATH resolution inside the sandbox before Moodle is involved.
4. In the Moodle question bank, create a question of type `multilanguage`, or better a local prototype `go_program`. For the prototype, duplicate the multilanguage question, keep `language` as python3, set the template to the Go-only combinator above, set `iscombinatortemplate` 1 and `allowmultiplestdins` 1, keep `EqualityGrader`, set `memlimitmb` 16000 (or 0), `cputimelimitsecs` 10, and mark it Is prototype with type name `go_program`.
5. Author one WAT question from the prototype. Test cases carry stdin and expected stdout, exact match. Validate with a sample answer on save.
6. Add the question to the quiz through the existing pipeline scripts in `~/wats/moodle` (`import-questions.php`, `add-questions-to-quiz.php`, `validate-questions.php`).
7. Optional later step for native support. Bake `GoTask.php` into the image (`COPY GoTask.php /var/www/html/jobe/app/Libraries/` plus `rm -f /tmp/jobe_language_cache_file`), following section 1 and the JavaTask memory precedent, and switch the prototype's `language` to `go` to drop the python wrapper.

Latency estimate per submission. With the pre-warmed cache, compile is about 0.15 to 0.5 s and each test run is tens of milliseconds. The combinator template gives one Jobe POST, so a 5-test WAT grades in roughly 1 to 3 s including Moodle and Jobe overhead, comparable to the current Python questions. The stock per-test multilanguage template would instead pay one compile per test, roughly 3 to 8 s for 5 tests warm. Without pre-warming, the first submission per container pays a 5 to 10 s stdlib compile inside the CPU limit and can time out, so the pre-warm step is mandatory rather than an optimisation.
