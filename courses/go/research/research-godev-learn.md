# go.dev learning paths: survey and pedagogy evaluation

Research date 2026-09-02. Purpose is evidence for designing a Go course aimed at professional Java developers. Sources fetched this session are listed inline. The Tour lesson ordering comes from the canonical `.article` source files in the `golang/website` repository on go.googlesource.com, because https://go.dev/tour/list renders its contents with JavaScript and returns no table of contents to a plain fetch.

## 1. Inventory of official learning paths

### Primary paths on https://go.dev/learn/ (fetched)

| Path | URL | Form |
|---|---|---|
| A Tour of Go | https://go.dev/tour/ | Interactive browser slides with an embedded playground. Four advertised sections plus generics and a welcome module. Exercises close each module. |
| Documentation hub | https://go.dev/doc/ | Index of all tutorials and references. |
| Go by Example (linked, third party) | https://gobyexample.com/ | Annotated runnable programs. The official site leans on it for coverage the Tour lacks. |
| Guided learning journey, Web Dev | https://gowebexamples.com | Third-party snippet collection. |
| Guided learning journey, CLIs | spf13 OSCON workshop link | Third-party workshop material. |
| Guided learning journey, new coders | YouTube intro course | Video for programming beginners. |
| Qwiklabs | Google Cloud labs (three listed) | Paid cloud-platform labs, not language teaching. |
| Training and books sections | Ardan Labs, Gopher Guides, GOPL, and others | Commercial and print, outside go.dev. |

The "guided learning journeys" are thin. Three of the four cards point off-site to third-party material. Official first-party teaching lives in the Tour and the tutorial series under /doc/.

### Tutorials under https://go.dev/doc/ (fetched)

| Tutorial | URL | Scope |
|---|---|---|
| Getting started | https://go.dev/doc/tutorial/getting-started | Install, `go mod init`, Hello World, import `rsc.io/quote`, `go mod tidy`, pkg.go.dev discovery. |
| Create a module (seven parts) | https://go.dev/doc/tutorial/create-module | Library module plus caller app. Part 3 handles errors, part 6 adds a test, part 7 compiles and installs. |
| Multi-module workspaces | https://go.dev/doc/tutorial/workspaces | `go work`, editing across modules. |
| Accessing a relational database | https://go.dev/doc/tutorial/database-access | `database/sql` with MySQL. Backed by a ten-page database guide under /doc/database/. |
| Developing a RESTful API with Go and Gin | https://go.dev/doc/tutorial/web-service-gin | Third-party framework, two endpoints, in-memory data. |
| Getting started with generics | https://go.dev/doc/tutorial/generics | Duplication first, then type parameters, inference, named constraints. (Fetched.) |
| Getting started with fuzzing | https://go.dev/doc/tutorial/fuzz | Unit test first, then fuzz test, two planted bugs fixed. (Fetched.) |
| Writing Web Applications | https://go.dev/doc/articles/wiki/ | Older stdlib-only wiki app article. |
| How to write Go code | https://go.dev/doc/code.html | Workspace conventions, `go install`, basic testing. |
| Effective Go | https://go.dev/doc/effective_go | Idiom reference, frozen at 2009. See section 3. |
| Codewalks | https://go.dev/doc/codewalk/functions and siblings | Guided reading of complete programs, including Share Memory by Communicating. |

The /doc/ page fetch also surfaced Managing dependencies, the module publishing guides, and Organizing a Go module (https://go.dev/doc/modules/layout). A govulncheck tutorial exists at go.dev/doc/tutorial/govulncheck but is not linked from the /doc/ index, per that fetch.

## 2. Tour of Go concept order

Source is the `.article` files fetched from https://go.googlesource.com/website/+/refs/heads/master/_content/tour/ (basics, flowcontrol, moretypes, methods, generics, concurrency, welcome). Lesson titles are verbatim and in file order. Congratulations slides are omitted.

### Welcome

| # | Lesson | Concept |
|---|---|---|
| 1 | Hello, 世界 | The playground itself, UTF-8 source as a first impression. |
| 2 | Go local | Translated tours. |

### Basics: packages, variables, and functions

| # | Lesson | Concept |
|---|---|---|
| 1 | Packages | Every program starts in `package main`. |
| 2 | Imports | Factored import statements. |
| 3 | Exported names | Capitalisation is visibility. |
| 4 | Functions | Type after the name. |
| 5 | Functions continued | Shared type across parameters. |
| 6 | Multiple results | Functions return tuples. |
| 7 | Named return values | Naked returns, with a warning. |
| 8 | Variables | `var` declarations. |
| 9 | Variables with initializers | Initialisers drop the type. |
| 10 | Short variable declarations | `:=` inside functions only. |
| 11 | Basic types | bool, string, int family, byte, rune, float, complex. |
| 12 | Zero values | No uninitialised variables. |
| 13 | Type conversions | Conversions are always explicit. |
| 14 | Type inference | Untyped constants pick a default. |
| 15 | Constants | `const`, no `:=`. |
| 16 | Numeric Constants | Arbitrary-precision untyped constants. |

### Flow control statements: for, if, else, switch and defer

| # | Lesson | Concept |
|---|---|---|
| 1 | For | The only loop keyword. No parentheses, braces required. |
| 2 | For continued | Init and post are optional. |
| 3 | For is Go's "while" | Drop the semicolons. |
| 4 | Forever | Infinite loop. |
| 5 | If | Same brace rules as for. |
| 6 | If with a short statement | Scoped pre-statement. |
| 7 | If and else | Scope of the short statement extends to else. |
| 8 | Exercise: Loops and Functions | Newton's method square root. |
| 9 | Switch | Implicit break, arbitrary case values. |
| 10 | Switch evaluation order | Top to bottom, stops on match. |
| 11 | Switch with no condition | Clean long if-else chains. |
| 12 | Defer | Deferred execution, arguments evaluated now. |
| 13 | Stacking defers | LIFO defer stack. |

### More types: structs, slices, and maps

| # | Lesson | Concept |
|---|---|---|
| 1 | Pointers | `*T`, `&`, no pointer arithmetic. |
| 2 | Structs | Typed field collections. |
| 3 | Struct Fields | Dot access. |
| 4 | Pointers to structs | Implicit dereference on field access. |
| 5 | Struct Literals | Positional and named literals. |
| 6 | Arrays | Fixed length is part of the type. |
| 7 | Slices | Views onto arrays. |
| 8 | Slices are like references to arrays | Shared backing storage. |
| 9 | Slice literals | Array literal without the length. |
| 10 | Slice defaults | Omitting bounds. |
| 11 | Slice length and capacity | `len` and `cap`, re-slicing. |
| 12 | Nil slices | nil has len 0 and cap 0. |
| 13 | Creating a slice with make | Dynamically sized allocation. |
| 14 | Slices of slices | Nested slices. |
| 15 | Appending to a slice | `append` and growth. |
| 16 | Range | Index and copy per iteration. |
| 17 | Range continued | Skipping with `_`. |
| 18 | Exercise: Slices | Build a picture as `[][]uint8`. |
| 19 | Maps | make, nil maps. |
| 20 | Map literals | Literal syntax. |
| 21 | Map literals continued | Eliding the element type name. |
| 22 | Mutating Maps | Insert, delete, comma-ok test. |
| 23 | Exercise: Maps | Word count. |
| 24 | Function values | Functions as arguments and returns. |
| 25 | Function closures | Captured variables. |
| 26 | Exercise: Fibonacci closure | Stateful closure. |

### Methods and interfaces

| # | Lesson | Concept |
|---|---|---|
| 1 | Methods | Receiver argument, no classes. |
| 2 | Methods are functions | Receiver is just a parameter. |
| 3 | Methods continued | Methods on non-struct named types, same-package rule. |
| 4 | Pointer receivers | Mutating the receiver. |
| 5 | Pointers and functions | Contrast with plain pointer parameters. |
| 6 | Methods and pointer indirection | Value calls pointer methods automatically. |
| 7 | Methods and pointer indirection (2) | The reverse direction. |
| 8 | Choosing a value or pointer receiver | Mutation and copy-cost rationale, consistency rule. |
| 9 | Interfaces | Method sets as types. |
| 10 | Interfaces are implemented implicitly | No `implements` keyword. |
| 11 | Interface values | (value, type) pair model. |
| 12 | Interface values with nil underlying values | Methods on nil receivers. |
| 13 | Nil interface values | Nil interface versus nil inside an interface. |
| 14 | The empty interface | `interface{}` holds anything. |
| 15 | Type assertions | Comma-ok assertion. |
| 16 | Type switches | Switch on dynamic type. |
| 17 | Stringers | `fmt.Stringer`, first stdlib interface. |
| 18 | Exercise: Stringers | Implement String on an IP type. |
| 19 | Errors | `error` is an interface, comma-error idiom. |
| 20 | Exercise: Errors | Custom error type for negative sqrt. |
| 21 | Readers | `io.Reader` stream contract. |
| 22 | Exercise: Readers | Infinite 'A' reader. |
| 23 | Exercise: rot13Reader | Reader wrapping a reader. |
| 24 | Images | `image.Image` interface. |
| 25 | Exercise: Images | Generate an image. |

### Generics

| # | Lesson | Concept |
|---|---|---|
| 1 | Type parameters | Square-bracket type parameters, `comparable`. |
| 2 | Generic types | A generic linked list. |

### Concurrency

| # | Lesson | Concept |
|---|---|---|
| 1 | Goroutines | `go` statement, shared address space. |
| 2 | Channels | Typed, blocking send and receive. |
| 3 | Buffered Channels | Capacity and blocking rules. |
| 4 | Range and Close | Producer closes, receiver ranges. |
| 5 | Select | Multiplexing channel operations. |
| 6 | Default Selection | Non-blocking attempts. |
| 7 | Exercise: Equivalent Binary Trees | Channels as tree iterators. |
| 8 | sync.Mutex | Mutual exclusion when channels do not fit. |
| 9 | Exercise: Web Crawler | Parallel fetch with dedupe, the capstone. |
| 10 | Where to Go from here... | Pointers onward to docs and codewalks. |

## 3. Pedagogy evaluation

### The ordering, and why it mostly works

The Tour runs syntax, then data, then abstraction, then concurrency. Each module depends only on earlier ones. Methods precede interfaces because interfaces are method sets. Interfaces precede errors, Stringers, and Readers because all three are taught as instances of one idea, small stdlib interfaces satisfied implicitly. That sequencing is the Tour's best design decision. A learner meets `error` as an ordinary interface on slide 19 of the methods module, not as special machinery.

Concurrency comes last and gets a full module with the strongest exercises (binary tree equivalence, a parallel web crawler). Placing the language's marquee feature at the end rewards completion but also means many learners never reach it.

The ordering fails in two places. Generics sit between interfaces and concurrency but get only two slides, so parametric polymorphism arrives with no exercises and no constraint design guidance. And within modules the Tour is a feature catalogue, not a skill ladder. Go trainer Cory LaNou's assessment, quoted in a learning round-up (https://medium.com/@IndianGuru/how-do-i-go-about-learning-go-3a58a3a29a0b, surfaced via web search), is that the Tour "does a great job of showing off a lot of language features" but not of "building up your skills in a manner that is conducive to actually learning the language".

### Assumed prior knowledge

The Tour is written for working programmers and says so through contrast. The flow-control module opens by comparing `for` with "other languages like C, Java, or JavaScript". It assumes the reader already knows what pointers, static types, while loops, and closures are, and only explains Go's variations. Exercises assume algorithmic maturity (Newton's method, Fibonacci, binary trees, a concurrent crawler). Jon Calhoun's guide (https://www.calhoun.io/guide-to-go/, via search) makes the same point from the other side. The Tour suits experienced developers and confuses beginners. For a Java-developer course this assumption is a feature, not a bug.

### Use of runnable examples

Every Tour slide is a complete, editable program in an embedded playground. Nothing is pseudocode. The tutorials use a different but equally disciplined loop. Each step gives exact shell commands and the exact expected output, so the learner verifies every stage (observed in the getting-started, generics, and fuzzing tutorials fetched above). The generics tutorial is the strongest pedagogical specimen. It starts from duplicated `SumInts` and `SumFloats` functions, so the motivation exists before the syntax, then keeps all variants in one file and shows identical output for each. The fuzzing tutorial plants two real bugs (byte-wise reversal of multi-byte UTF-8, then invalid input) and walks the learner through discovering and fixing both, changing the function signature to return an error along the way.

The playground also constrains the Tour. A sandboxed single-file environment cannot demonstrate modules, multi-file packages, the test runner, or real IO. Several of the Tour's omissions trace directly to that constraint.

### What officialdom leaves out that a professional needs

- **Error wrapping.** The Tour gives errors one slide and one exercise, all pre-2019 style. No `fmt.Errorf` with `%w`, no `errors.Is`, `errors.As`, no sentinel-versus-typed guidance. Effective Go carries its own warning, quoted from the fetched page, that it "was written for Go's release in 2009 and is not actively updated" and does not cover generics, modules, or newer libraries. So neither of the two flagship documents teaches modern error handling. Zed Shaw's study guide (https://learncodethehardway.com/blog/36-an-efficient-go-study-guide/, via search) notes the imbalance directly. Modules get hundreds of pages while error handling gets almost none. Robin Moffatt's learning notes (https://rmoff.net/2020/07/01/learning-golang-some-rough-notes-s01e06-errors/, via search) call the Tour's errors treatment "too abstract" and report falling back to Go by Example.
- **context.Context.** Absent from the Tour, the tutorial series, and Effective Go. The only official appearances found are in the database guide's cancellation page. For server-side Go this is the single largest gap.
- **Testing.** The Tour contains zero testing. `go test` first appears in part 6 of the create-module series, and table-driven tests only in the fuzzing tutorial. Nothing official teaches test structure, subtests, coverage habits, or the race detector as a workflow.
- **Modules and tooling.** The Tour never runs the `go` command. Tooling lives in the tutorials and the modules reference, so a Tour-only learner ships nothing. gofmt, go vet, and staticcheck-style linting are not taught anywhere in the beginner paths.
- **Project structure.** Organizing a Go module (https://go.dev/doc/modules/layout) exists but sits deep in the modules section, unlinked from any beginner path.
- **Concurrency discipline.** The Tour teaches goroutines, channels, select, and Mutex, but not sync.WaitGroup, errgroup, channel ownership conventions, goroutine leak avoidance, or cancellation. The crawler exercise expects learners to invent coordination themselves.
- **Everyday production topics.** Struct embedding, panic and recover, JSON, HTTP servers, and logging are all outside the Tour. Embedding and panic sit only in the frozen Effective Go.

### Other criticised weaknesses

Exercise density is low, roughly nine exercises across some ninety substantive slides. An Earthly review (https://earthly.dev/blog/top-3-resources-to-learn-golang-in-2021/, via search) praises the low barrier to entry but wants more exercises. The interfaces sequence explains the (value, type) model well but, per Moffatt, under-explains its own code examples. The guided journeys page outsources three of four journeys to third parties, so there is no official end-to-end path from Hello World to a deployed, tested service.

## 4. What a Java-developer course should copy, and what it must add

### Copy

- **Runnable-first, every step verified.** Every concept lands as a complete program with expected output. The tutorials' command-plus-expected-output rhythm doubles as self-assessment.
- **Motivation before syntax.** The generics tutorial's duplication-then-generalise arc is the model. Show the pain, then the feature.
- **Interfaces as one repeated idea.** Teach interface, then immediately instantiate it three times (Stringer, error, Reader) exactly as the Tour does. For Java developers, lead with the contrast that satisfaction is implicit and interfaces are defined by consumers.
- **Methods before interfaces, interfaces before errors.** The dependency ordering is sound. Keep it.
- **Planted-bug exercises.** The fuzzing tutorial's discover-and-fix cycle teaches debugging and testing together. Reuse the pattern.
- **The library-plus-caller module shape.** The create-module series builds a two-module system, adds errors, adds a test, then installs a binary. That is a miniature of real work and a better spine than slides.
- **Contrast teaching.** The Tour's brief "unlike C, Java, or JavaScript" asides work. A Java-specific course can go much further with a systematic mapping (exceptions to error values, inheritance to composition and embedding, packages and visibility, null to nil and zero values, Java generics erasure to Go instantiation, threads and executors to goroutines).

### Add (the gaps the official material leaves open)

1. **Modern error handling as a first-class unit.** Wrapping with `%w`, `errors.Is` and `errors.As`, sentinel versus typed errors, error strategy at API boundaries. Teach it right after the error interface, not as an appendix.
2. **context.Context early and everywhere.** Introduce alongside goroutines, then thread it through HTTP and database units.
3. **Testing from the first module.** Table-driven tests, subtests, `go test` flags, coverage, the race detector, then fuzzing. Java developers expect JUnit-level rigour on day one, so meet it.
4. **Tooling as curriculum.** `go mod`, `go work`, gofmt, `go vet`, staticcheck, govulncheck, pkg.go.dev literacy. The Tour's playground hides all of this.
5. **Project layout and package design.** Package naming, internal packages, the module layout guidance, avoiding Java-style deep hierarchies and util packages.
6. **Concurrency discipline beyond primitives.** WaitGroup and errgroup, worker pools, channel ownership, leak detection, cancellation via context. Rework the Tour's crawler exercise with these tools.
7. **A single continuous project.** The official material has no end-to-end path. A course should carry one service from module init through tests, database, HTTP, and deployment, using the database and Gin tutorials as reference points but preferring `net/http` first.
8. **Generics with judgement.** More depth than the Tour's two slides, plus explicit guidance on when interfaces beat type parameters, which Java developers will over-apply.

## Sources fetched this session

- https://go.dev/learn/
- https://go.dev/doc/
- https://go.dev/doc/effective_go
- https://go.dev/doc/tutorial/getting-started
- https://go.dev/doc/tutorial/create-module
- https://go.dev/doc/tutorial/generics
- https://go.dev/doc/tutorial/fuzz
- Tour article sources from https://go.googlesource.com/website/+/refs/heads/master/_content/tour/ (welcome, basics, flowcontrol, moretypes, methods, generics, concurrency), saved locally as `tour-*.article` in this scratchpad.
- Critique sources surfaced by web search and quoted from search results, not fetched in full: learncodethehardway.com study guide, rmoff.net errors notes, calhoun.io guide, the Medium round-up quoting Cory LaNou, and the Earthly review.
