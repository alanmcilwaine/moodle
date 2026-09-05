# Java developer learning Go, research findings

Evidence for a course aimed at one learner. A professional Java developer, fluent through Java 26 (records, sealed types, streams, lambdas, switch expressions, generics), no Spring, strong on GoF patterns. He learns best when a Go feature is explained via the pattern it replaces or absorbs.

Effective Go states the framing plainly. "A straightforward translation of a C++ or Java program into Go is unlikely to produce a satisfactory result. Java programs are written in Java, not Go."

## 1. Unlearning catalogue

| Java habit | Go replacement | Why it matters | Severity |
|---|---|---|---|
| Inheritance hierarchies, `extends`, abstract base classes | Struct and interface embedding plus composition. Embedding promotes methods, but "the receiver of the method is the inner type, not the outer one". There is no dynamic dispatch back to the outer type | The single biggest source of unidiomatic Go. Learners build pseudo-hierarchies and are then surprised the "override" is never called. The FAQ's stated reason for omitting inheritance is that type relationships "often could be derived automatically" | High |
| Exceptions, try-catch-finally, checked exceptions | Errors as ordinary values via multi-value returns. `if err != nil` checks. `errors.Is`/`errors.As` for matching. Panic is reserved for the unrecoverable; "real library functions should avoid panic" | The FAQ says try-catch "results in convoluted code" and encourages labelling ordinary errors as exceptional. Java developers either panic everywhere or ignore returned errors. 100 Go Mistakes devotes a chapter to this (#48 to #54) | High |
| Interface-first design, `FooService` plus `FooServiceImpl`, interfaces defined next to implementations | Consumer-defined small interfaces, discovered late. "Interfaces generally belong in the package that uses values of the interface type, not the package that implements those values." Return concrete types, accept interfaces | 100 Go Mistakes #5 to #7 (interface pollution, producer-side interfaces, returning interfaces). Harsanyi's rule is "abstractions should be discovered, not created". The proverb is "the bigger the interface, the weaker the abstraction" | High |
| Null checks and `Optional` reflexes | Zero values that are useful by design. `bytes.Buffer` and `sync.Mutex` work uninitialised. The separate trap is the nil interface gotcha. An interface holding a typed nil pointer is not `nil` | The FAQ documents the gotcha directly ("Why is my nil error value not equal to nil?"). Returning `*MyError` instead of `error` produces an error that is never nil. 100 Go Mistakes #45 covers the same failure | High |
| `ArrayList` mental model for slices | Slices are views over a shared backing array. Assignment aliases. `append` may or may not reallocate, so mutations leak between slices with shared capacity. Growth must be captured with `x = append(x, ...)` | 100 Go Mistakes #20 to #26 (length vs capacity, nil vs empty, copy, append side effects, capacity leaks). Effective Go confirms the aliasing semantics. Java has no equivalent trap because `List` never aliases silently | High |
| Getters and setters on every field | Export the field, or name the getter `Owner()` without the `Get` prefix. "It's neither idiomatic nor necessary to put Get into the getter's name" (Effective Go) | 100 Go Mistakes #4 calls blanket accessors overuse. Low mechanical cost but a high visibility marker of Java-flavoured Go | Medium |
| Constructor overloading and telescoping constructors | Plain `NewFoo` functions, composite literals, and the functional options pattern for optional configuration | Go has no overloading at all ("names in a scope must be unique"). Cheney's dotGo talk shows overloading and config structs both failing, and 100 Go Mistakes #11 lists not using functional options as a mistake | Medium |
| Streams chains for every collection operation | Plain `for` loops, plus Go 1.23 `iter.Seq` iterators and the `slices`/`maps` helpers where composition genuinely earns its place | "Clear is better than clever." The stdlib still has no `Filter`. A learner who reaches for a streams equivalent first writes convoluted Go. Loops are the default idiom | Medium |
| One public class per file, deep package trees, `com.company.project.module` | Packages as directories of related files. Multiple types per file is normal. Short lower-case package names. Visibility by capitalisation, two levels only (exported and package-private) | 100 Go Mistakes #12 to #14 (misorganisation, utility packages, name collisions). CodeReviewComments bans `util`, `common`, `misc` names. Identifiers should not repeat the package name (`bufio.Reader`, not `bufio.BufReader`) | Medium |
| Everything is a reference; `this` semantics | Value semantics by default. Arrays copy. Structs copy on assignment and in `range` loops (#30). Choose pointer vs value receivers deliberately and never mix them on one type | CodeReviewComments gives the rules of thumb. Mutation, `sync.Mutex` fields, and large structs need pointers. "When in doubt, use a pointer receiver." Receiver names avoid `this` and `self` | High |
| ORM and annotation reflexes, DI containers | `database/sql` directly, struct tags for serialisation, explicit wiring in `main` | "Reflection is never clear." No Spring background helps this learner, but the reflex to want a framework layer remains. 100 Go Mistakes #78 covers SQL usage errors | Low |
| Static initialisers and eager global setup | Avoid `init()`. Prefer explicit initialisation from `main`. Uber's guide requires `init()` to be deterministic and free of I/O | 100 Go Mistakes #3. Ordering-dependent init is a real production trap | Low |
| Assertion-style defensive code | Handle and report errors properly instead. The FAQ removed assertions deliberately, calling them "a crutch to avoid thinking about proper error handling" | Shapes test style too. Go tests favour table-driven tests and plain comparisons over assertion frameworks | Low |
| Threads, executors, `synchronized` | Goroutines and channels. "Don't communicate by sharing memory, share memory by communicating." Mutexes still exist ("channels orchestrate; mutexes serialize") | 100 Go Mistakes gives concurrency two chapters (#55 to #74). The largest trap is #62, starting a goroutine without knowing when it stops | High |

## 2. GoF pattern mapping

Verdicts cross-checked against Linhares (2022), Effective Go, the Go blog, and the 100 Go Mistakes catalogue. "Dissolves" means the language feature does the job with no pattern structure left. "Reshapes" means the intent survives in a different form.

| GoF pattern | Go outcome | Idiom evidence | Disputes and caveats |
|---|---|---|---|
| Strategy | Dissolves into function values, or a one-method interface when state is needed | Linhares says single-method interfaces are possible but "not very idiomatic"; define a func signature per algorithm. `sort.Slice(s, less)` is the canonical example | Interface form returns when the strategy carries configuration or several related methods. Both are accepted; funcs are the default |
| Decorator | Reshapes into interface wrapping and function wrapping | `http.Handler` middleware, `func(http.Handler) http.Handler`. Effective Go's `http.HandlerFunc` shows a func type carrying a method. Struct embedding also delegates | Linhares' caveat is real. It only works over interfaces or func types. You cannot wrap a concrete struct such as `net.Resolver`. Uber additionally warns against embedding in public structs, which cuts against the embedding-based form |
| Observer | Dissolves into channels for single consumer; reshapes for fan-out | Linhares calls the pattern "almost first-class citizens in go" via channels. Producer goroutine, consumer ranges over the channel | Multi-subscriber fan-out is not free. It needs one channel per subscriber or a broker. Callback-slice observers still appear in real code. Teach both |
| Iterator | Was diminished, now first-class via range-over-func (Go 1.23) | `iter.Seq[V]` is `func(yield func(V) bool)`. `for v := range s.All()` compiles the loop body into the yield func. `slices.Collect`, `maps.Keys`, `iter.Pull` in the stdlib (Taylor, Go blog, Aug 2024) | Push iterators only for `range`; pull iterators need `iter.Pull` and a mandatory `stop` call. Pre-1.23 material calls the pattern rare, so date-check any source |
| Template Method | Dissolves into function parameters ("template function") | Linhares' example is `sort.SliceStable` taking a comparison closure. The hook method becomes an argument | No dispute found. Inheritance-based template method is simply unwritable in Go |
| Singleton | Reshapes into package-level state plus `sync.Once` for lazy init | Package variables are singletons by construction. `sync.OnceValue` (Go 1.21) is the modern lazy form | Community pushback targets the pattern itself. Package-level mutable state harms testability, so the idiom is often "pass the dependency instead". Linhares does not cover it |
| Factory Method / Abstract Factory | Dissolves into plain `NewFoo` constructor functions and factory func parameters | Effective Go's `NewFile`. Linhares reduces abstract factories to "just a function signature", motivated mainly by testability (swap a `net.Dialer` for a mock) | Returning interfaces from constructors is discouraged (100 Go Mistakes #7) except when hiding an unexported type, as `crc32.NewIEEE` does. That nuance is worth a lesson |
| Adapter | Survives, made cheap by implicit interface satisfaction | Linhares says "widely used all over", citing `database/sql` drivers and go-cloud. Any type with the right method set already satisfies the interface, so many adapters are zero code | The FAQ's structural typing is the mechanism. Compile-time checks use `var _ I = (*T)(nil)` |
| Command | Dissolves into func values; survives as `http.Handler` when named | Linhares treats Command jointly with Chain of Responsibility. `http.HandlerFunc` adapts a bare func into the Command interface. Middleware stacks are the chain | None found |
| Builder | Reshapes into functional options; fluent builders exist but are secondary | Cheney's `func(*Server)` variadic options. "We, as Go programmers, should work hard to ensure that nil is never a parameter that needs to be passed to any public function." 100 Go Mistakes #11 | Genuine dispute. Config structs remain common (e.g. `http.Server`) and some argue options are overkill for internal code. Uber's guide endorses options for exported APIs. Teach the trade-off, not one winner |
| Facade | Survives unchanged | Linhares, "still here!", go-cloud as the example | None |
| Proxy | Survives with the Decorator caveat | Interface and func types only. No dynamic proxies, no `method_missing`; runtime proxying needs code generation | Reflection-based proxying is anti-idiomatic ("reflection is never clear") |

## 3. Direct transfers from Java 26

These map cleanly and should open the course, since they let the learner reuse fluency instead of unlearning.

| Java 26 feature | Go equivalent | Friction to flag |
|---|---|---|
| Records | Structs with composite literals. Struct equality is built in for comparable fields, so `equals`/`hashCode` boilerplate vanishes (yourbasic Go vs Java) | Structs are mutable and copied by value. No compact constructor validation; use a `NewFoo` func |
| Sealed interfaces plus pattern-matching switch | Type switch on an interface, `switch v := x.(type)` (Effective Go) | No exhaustiveness checking and no sealing. Adding a type silently falls to `default`. Closed sets are simulated with unexported marker methods |
| Functional interfaces and lambdas | First-class func types and closures. No SAM conversion needed; a func is already a value | Named func types can carry methods (`http.HandlerFunc`), which Java cannot express |
| Switch expressions | Go switch. No fallthrough by default, arbitrary boolean cases, comma-separated case lists | Go's switch is a statement, not an expression. No arrow-yield form |
| try-with-resources | `defer f.Close()` | Function-scoped, not block-scoped. Arguments evaluate at defer time. LIFO order. In a loop, defers pile up until the function returns (100 Go Mistakes #35) |
| Generics with bounded type parameters | Type parameters with constraints (Go 1.18) | No generic methods (FAQ explains why). Square brackets. Inference is deliberately limited. #9 warns against pre-emptive use |
| Streams | Go 1.23 iterators plus `slices`/`maps` helpers, partially | The default idiom is still the loop. No stdlib `Filter` yet |
| `var` local inference | `:=` | Shadowing bites (#1) |

## 4. Ten mistakes worth building exercises around

Chosen for frequency in the sources, direct collision with this learner's Java instincts, and testability as an exercise.

1. The nil interface error. Return `*MyError` from a func typed `error` and watch `err != nil` succeed with a nil pointer inside. FAQ plus 100 Go Mistakes #45. The single best "Go is not Java" demonstration.
2. Slice aliasing through `append`. Two slices share a backing array, an append mutates the neighbour, a full slice expression `s[low:high:max]` or `copy` fixes it. #20, #24, #25.
3. Consumer-side interfaces. Refactor a Java-style `Store` interface out of the producer package, shrink it to the two methods the consumer uses, mock it in the consumer's test. #5 to #7 plus CodeReviewComments.
4. Embedding is not inheritance. Embed a type, "override" a method on the outer type, call it through the inner method, observe the override never fires. Effective Go's promotion rules.
5. Error wrapping and handling once. Build a call chain using `%w`, match with `errors.Is`/`errors.As`, then find and fix a log-and-return duplicate. #49 to #52 plus Uber's decision table.
6. Functional options. Convert a telescoping constructor (Java Builder instinct) into `NewServer(addr string, opts ...Option)`. Cheney's pattern, #11.
7. Pointer vs value receivers. A value receiver silently mutates a copy; a struct with a `sync.Mutex` gets copied. Apply the CodeReviewComments rules and `go vet`. #42, #74.
8. Goroutine lifetime as Observer. Build a channel-based notifier, then extend to two subscribers and discover fan-out. Then kill the leak from an unstoppable goroutine. #62, #65.
9. Zero values and nil vs empty. Design a type whose zero value works (`bytes.Buffer` style), and fix an API that distinguishes nil from empty slices. Proverb "make the zero value useful", #22, #23.
10. Defer semantics. Arguments evaluated at defer time (#47), LIFO order, defer in a loop (#35), and the deferred `Close` error nobody checks (#54). Contrast directly with try-with-resources scoping.

Package organisation (#12 to #14) narrowly missed the list. It suits a project-layout walkthrough better than a discrete exercise.

## Sources fetched

- https://go.dev/doc/effective_go
- https://go.dev/doc/faq
- https://go-proverbs.github.io/
- https://100go.co/ (100 Go Mistakes, Teiva Harsanyi, full catalogue)
- https://yourbasic.org/golang/go-vs-java/
- https://go.dev/blog/range-functions (Ian Lance Taylor, Aug 2024)
- https://go.dev/wiki/CodeReviewComments
- https://dave.cheney.net/2014/10/17/functional-options-for-friendly-apis
- https://mauricio.github.io/2022/02/07/gof-patterns-in-golang.html
- https://github.com/uber-go/guide/blob/master/style.md

## Postscript, 2026-09-02

The direct-transfer table above says Go has no generic methods and cites the FAQ. That was true when the sources were fetched and is now stale. Go 1.27, released August 2026, added type parameters on concrete methods (https://go.dev/blog/generic-methods, Mark Freeman, 26 August 2026). Interface methods still cannot take type parameters, and a generic method cannot help satisfy an interface. The course teaches the feature in WAT 19.3.
