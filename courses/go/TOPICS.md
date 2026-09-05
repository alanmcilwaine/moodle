# Course spec: Go

This file is the contract for authoring the course. Read it with [AUTHORING.md](../../AUTHORING.md) for the XML format. The question layout, the constraint format, and the grading model are this course's own, defined below. They replace the Python course's five zones and Rules block. This is spec v2, rewritten on 2026-09-02 from a design workflow.

## The learner

A professional developer, fluent in Java through Java 26, plain Java SE only. He knows records, sealed types, streams, lambdas, functional interfaces, switch expressions, and generics. He knows the GoF design patterns well and learns fastest when a language feature is framed as the pattern it replaces or absorbs. He had never written Go when the course began.

He is not fluent in Java's threads, executors, or locks. Topics 23 to 25 therefore assume no parallel programming at all. They teach what concurrency is before they teach Go's spelling of it. They never explain a Go feature by contrast with a Java concurrency construct.

He is moving onto the DT Platform backend. That codebase is one Core API application built from packages behind small interfaces. Its orchestration code owns transactions, its errors are values, and its clients are generated from OpenAPI specs. The course ends at that shape.

Never teach him what a loop is. Teach him what Go does differently, forbid the Java reflex, and name the pattern that just dissolved.

The research behind the topic choices sits in [research/](research/). The unlearning catalogue and pattern mapping are in [research-java-to-go.md](research/research-java-to-go.md). The ordering leans on the go.dev pedagogy survey in [research-godev-learn.md](research/research-godev-learn.md).

## The docs do the teaching

The Python course carried a large teaching fold in every question. This course does not. The official docs teach, the question aims the learner at the right page, and the tests check that the reading happened. Each question links one to three official pages. Official means pkg.go.dev, go.dev/tour, go.dev/ref/spec, or go.dev/blog.

Four authoring rules hold this together.

1. Deleting the Read panel must make the question unanswerable. Repeating any sentence from a linked page in the question text is a defect.
2. Reading prompts pose the question the page answers, for example "Read the signature. What happens when count is 0?". A prompt never states what the page says.
3. The hidden tests are the doc sentence made executable. Each hidden test sits on an input where the documented behaviour diverges from the plausible guess.
4. Passing produces a sentence. At the moment of passing, the learner should be able to restate the doc sentence being taught in his own words.

The authoring test for every question is that a diligent reader of the linked docs passes and a guesser fails a hidden test.

## Conventional Go from the first WAT

The Python course withheld type hints until topic 12 and Alan had to ask for them. This course has no deferred-idiom phase. Every sample answer and every starter snippet is production-conventional Go from WAT 01.1.

- gofmt-clean, tabs and all. The validator runs `gofmt -l` on every sample answer and rejects the file on any output.
- `go vet` clean. The validator runs it on every sample answer.
- No discarded errors. Once topic 14 has taught error returns, `_` on an error value is a defect everywhere, enforced by hidden tests where reliable.
- No naked returns, no `init`, no package-level mutable state, no `this` or `self` as a receiver name.
- Before topic 14, exercises avoid fallible APIs entirely, so no error is ever visible but unhandled.

## Topics and tiers

Each topic gets three or four WATs at rising difficulty, except the capstone, which has two. The tier system is the Python course's. The question layout and constraint format are not, and are defined below. Names follow `WAT NN.T: Fun Name!` under the theming guide, and no two names are alike anywhere in either course.

| Tier | Name | Shape |
| --- | --- | --- |
| 1 | Introductory | One idea, one short function. The learner finishes it in minutes. |
| 2 | Working | The same idea on a real shape, with an edge case that punishes a careless answer. |
| 3 | Hard | The idea combined with earlier topics. Several functions or a type with methods. |
| 4 | Judgement | Optional. AI-written Go that passes every test. Say what is wrong and rewrite it. |

## The topics

All questions are new. There are no existing anchors to move.

| # | Topic | Tiers | Pattern framing |
| --- | --- | --- | --- |
| 01 | First lines: package main, gofmt, compile errors | 3 | none |
| 02 | Variables, zero values, := and const | 3 | null checks and Optional give way to zero values |
| 03 | Functions and multiple returns | 3 | none |
| 04 | Reading Go documentation | 3 | Javadoc maps across, the IDE reflex moves to pkg.go.dev |
| 05 | Flow control: for, switch, and if with a short statement | 3 | none |
| 06 | Strings, runes, and fmt verbs | 3 | none |
| 07 | Structs and composite literals | 3 | records map across |
| 08 | Pointers and value semantics | 3 | none |
| 09 | Slices: views, len, cap, append | 3 | none |
| 10 | Slice aliasing and copying | 4 | none |
| 11 | Maps and comma-ok | 3 | none |
| 12 | Methods and receivers | 3 | none |
| 13 | Interfaces, implicit and small | 4 | Adapter becomes free, Strategy's interface form |
| 14 | Errors as values | 3 | none |
| 15 | Error wrapping and the nil trap | 4 | none |
| 16 | Testing with go test | 3 | none |
| 17 | defer, panic, recover | 3 | try-with-resources maps across |
| 18 | Functions as values and closures | 3 | Strategy, Command, Template Method dissolve |
| 19 | Embedding and composition | 3 | Decorator by wrapping, inheritance unlearnt |
| 20 | Type switches and closed sets | 3 | sealed types map across, imperfectly |
| 21 | Generics | 4 | Java generic methods map across at last, Go 1.27 |
| 22 | Iterators and the slices and maps packages | 4 | Iterator via range-over-func, streams detox |
| 23 | Goroutines and WaitGroup | 3 | none |
| 24 | Channels and select | 3 | Observer via channels |
| 25 | Concurrency discipline and context | 3 | none |
| 26 | Capstone: options and a package in miniature | 2 | Builder becomes functional options, Factory becomes NewFoo |

That is 26 topics and 82 WATs.

The teaching order is the dependency order. Documentation comes directly after functions, because from topic 05 onward the Read panel is the whole of the teaching. Methods come before interfaces because interfaces are method sets. Interfaces come before errors because `error` is an interface. Testing comes directly after the error topics, so every later topic can be tested as it lands, and because good tests exercise error paths. Errors come before defer's error cases, closures before embedding's wrapper form, and everything before concurrency. The Tour of Go validated this ordering and its worst gaps, thin errors, no context, and thin generics, get full topics here.

Two gate rules govern concept use. No row uses language syntax that a lower-numbered topic has not taught. After topic 04, calling a stdlib function found through a linked doc is never a gate, because looking functions up is the taught skill. Two stated exceptions bend the gate. Topics 01 and 02 need functions before topic 03 teaches them. Every 01.x and 02.x question therefore ships a fixed function scaffold in its starter code. The signature is given, the learner fills the body, and function declaration proper is taught at topic 03. The other exception is the function literal at WAT 16.2, which arrives by doc link ahead of topic 18's full treatment. A Java developer reads it as a lambda.

## Topic 04, Read the Manual

Topic 04 sits directly after functions. At this point the learner knows `fmt.Println`, `var`, `:=`, `const`, the basic types, and a first `if` and `else` from WAT 01.3. He can define and call functions with multiple returns. He does not know loops. Calling a package function is the same act as calling `fmt.Println`, so no new syntax is needed. The standard library's `strings`, `math`, `strconv`, and `unicode/utf8` packages are plain functions over basic types, so that toolkit is enough.

The design rule for every tier is that the doc fact is the grade. Each hidden test sits on an input where the documented behaviour diverges from the plausible guess. Hidden rows use display HIDE, so a failing learner gets no oracle to iterate against. Reading the page is the only reliable route to a pass. Compile errors cannot substitute for the docs, because every wrong reading still compiles.

That last property belongs to topic 04, not to the whole course. A topic whose lesson is a type rule cannot hold it. WAT 21.1 is the recorded exception. A wrong type set is a compile error by construction, and the compiler names the fix. It reports that a type does not satisfy the constraint and is possibly missing a tilde. The question cannot close that route, so the Read link carries the lesson for a learner who reads before building.

**WAT 04.1: Trim Before You Guess! (tier 1).** The anatomy of a pkg.go.dev page. The learner writes two one-line functions described by behaviour only. One removes the literal leading brand name `"go"`. The other removes every leading character drawn from the letters g and o, however many. The Read panel links [strings.TrimPrefix](https://pkg.go.dev/strings#TrimPrefix) and [strings.TrimLeft](https://pkg.go.dev/strings#TrimLeft), and the learner decides which function is which. The visible tests use inputs where both agree, such as `"gopher"`. The hidden test feeds `"google.com"`, where TrimLeft strips `goog` and TrimPrefix strips `go`. Only the cutset sentence in the TrimLeft doc states the difference. A learner who guesses passes every visible test and fails the hidden one.

**WAT 04.2: Scavenger Hunt at pkg.go.dev! (tier 2).** No function is named at all. The question describes three needs in behaviour terms. Somewhere in `strings` a function reports whether one string starts with another. Somewhere in `unicode/utf8` a function counts the runes in a string. Somewhere in `math` a constant holds the largest value an `int8` can carry. The Read panel links only the three package roots, [strings](https://pkg.go.dev/strings), [unicode/utf8](https://pkg.go.dev/unicode/utf8), and [math](https://pkg.go.dev/math). No Required clause names the functions, because the folded red line would hand the learner all three answers before he opened a package root. Hidden tests make the index walk the intended route instead. A multibyte input defeats byte counting, and banning `len` closes the hand-rolled count. A non-prefix input that shares leading characters defeats anything looser than a true prefix check. Banning the literal `127` makes the constant unanswerable by typing the number, which is this topic's George Bool move. The residual risk of smuggling the value through arithmetic such as `1<<7 - 1` is accepted. `clueLimit` therefore appears in a hidden test only, never in a visible one. A second accepted risk sits on the rune count. `strings.Count(badge, "")` minus one returns the same number, so that find can be reached without opening the second package. No hidden input separates the two, because `Count` with an empty separator counts code points as well. A `Required` clause naming `utf8` would close it and is ruled out here, because the folded red line would hand over the answer.

**WAT 04.3: Needle in a Package Stack! (tier 3).** Finding a function when nobody names the package. The learner writes one function returning the double-quoted Go string literal for its argument. A second function rounds a float with ties going to the even neighbour. The Read panel links only [the standard library index](https://pkg.go.dev/std), with the instruction to search for the behaviour and read the doc sentence before calling. The intended finds are `strconv.Quote` and `math.RoundToEven`. The hidden tests feed a string holding a tab and a multibyte rune, and the tie values -10.5, 2.5, and 12.5. The Java reflex, `Math.round`, rounds halves towards positive infinity. The values 2.5 and 12.5 expose it, because it gives 3 and 13 where Go gives 2 and 12. At -10.5 the Java reflex and the correct answer agree on -10, so that value catches `math.Round` instead, which gives -11. Hand-rolling either half is impossible with the concepts met so far, and the Banned line closes branching for a learner who read ahead. This is the Javadoc moment. The grade certifies the search happened, not the learner's word for it.

## Topic 16, Testing with go test

Topic 16 sits directly after the error topics. By this point the learner has structs, slices, maps, methods, interfaces, and errors, which is everything a real table-driven test touches. The topic runs on the `go_testwriter` question type, a second grading template that is built and proven through the real stack, on 2026-09-02.

The grading design inverts the usual WAT. The question states a function's contract and provides the implementation. The learner writes the entire `_test.go` file. Each CodeRunner testcase carries one implementation variant in its `extra` field. The first variant is the correct implementation. Every other variant is a mutant, the same code with one documented clause broken. The wrapper writes the learner's test file beside each variant in turn and runs `go test` once per variant. The suite passes when the correct implementation passes and every mutant fails.

This grades real testing skill with no honour system. An empty test file passes the correct variant and kills no mutants, so it fails. An over-tight test that asserts unspecified behaviour kills mutants and fails the correct variant, so it also fails. Each mutant is the linked doc sentence broken one clause at a time, so deriving the killing input means reading the contract.

**WAT 16.1: Table Stakes! (tier 1).** A first table-driven test against one small pure function. A slice of case structs, a `range` over it, `t.Errorf` on mismatch. One correct implementation and two mutants, one wrong at an edge and one off by one.

**WAT 16.2: Run, Subtest, Run! (tier 2).** The same table promoted to subtests with `t.Run` and one name per case. The function literal passed to `t.Run` arrives here by doc link, ahead of topic 18. Mutants include one that only a named edge case catches, so the learner sees which subtest did the killing.

**WAT 16.3: Kill All Mutants! (tier 3).** A contract with several documented clauses and four or five mutants, each breaking a different clause. The learner derives one killing input per clause from the linked doc description. The tests must stay loose enough to pass the correct implementation. The mutant pipeline is proven at three variants per question, and this WAT needs five or six `go test` cycles in one Jobe request. Before authoring it, import a throwaway smoke with six variants, confirm it validates inside the Jobe limits, and record the timing in this file.

## Question layout

Four zones plus two grafted folds replace the Python five. The order is fixed, so the reader learns once where to look. Teaching has left the question and moved into the official docs, and the Read panel is the pointer.

```
Goal panel          one or two sentences, what you will write
Read                where the knowledge lives, links only
Coming from Java    optional fold, collapsed, at most three sentences
Banned line         one red line, machine-enforced
Stuck fold          optional fold, collapsed, two nudges
```

Revised 2026-09-03. The layout carried three more zones. A Your task panel spelt out every function and behaviour to write. A Before you click Check panel and an AI protocol panel followed it. Alan cut all three. His stated reasoning: Your task turned into a recipe, telling the learner exactly how to solve a problem that could reasonably be solved several ways. The other two panels were policy text a competent adult does not need repeated 82 times.

Before cutting Your task, every question was checked mechanically. The check compared, for each of the 82 shipped questions, the identifiers the grader calls against starter code and the visible tests. Zero questions relied on Your task for information invisible anywhere else. CodeRunner shows a visible test's actual Go statement, not just its output. A call such as `chorus([]Quacker{Duck{}, Toy{}})` already reveals the interface name. The learner reads that name before touching the panel. The deliverable now lives in the starter code's signatures and the two visible test cases, not in prose. An author naming something not already shown adds it to the starter code, as a stub or a `TODO` comment. It never goes in a task list.

**Goal panel.** One or two sentences, no teaching. All theme flavour lives here, under the theming guide's two-sentence scene cap.

```html
<div style="border-left:4px solid #2c3e50; padding:0.5em 1em; margin-bottom:1em; background:#eef1f4;"><b>Goal</b><p>ONE OR TWO SENTENCES HERE.</p></div>
```

**Read panel.** New, and it replaces the teaching fold as the primary source. One to three links to official material only, meaning pkg.go.dev, go.dev/tour, go.dev/ref/spec, or go.dev/blog. Each list item is a link plus a pointer to where on the page to look, phrased as the question the page answers. It never paraphrases what the page says. A paraphrase rebuilds the in-question teaching this format exists to remove. Doc links live here and nowhere else in the question.

```html
<div style="border-left:4px solid #b8860b; padding:0.5em 1em; margin-bottom:1em; background:#fdf8ec;"><b>Read</b><ul><li><a href="https://pkg.go.dev/strings#TrimLeft">strings.TrimLeft</a>. The sentence about cutset.</li><li><a href="https://pkg.go.dev/strings#TrimPrefix">strings.TrimPrefix</a>. Compare its first sentence with TrimLeft's.</li></ul></div>
```

**Coming from Java fold.** Optional, and absent by default. It exists only to name the Java reflex the question punishes, capped at three sentences of prose plus one `pre` block of Java. It ships collapsed, no `open` attribute. It may never restate anything the Read links cover, and nothing needed to answer may live inside it. Topics 23 to 25 never use it, because concurrency opens from the problem.

```html
<details><summary style="cursor:pointer; font-weight:bold; padding:0.3em 0;">Coming from Java</summary><p>UP TO THREE SENTENCES NAMING THE REFLEX.</p><pre>OPTIONAL JAVA SNIPPET</pre></details>
```

**Banned line.** Replaces the Rules block. Full specification in its own section below.

```html
<div style="border-left:4px solid #d9534f; padding:0.5em 1em; margin-top:1em; background:#fdf3f2;"><b>Banned:</b> <code>for</code>, <code>append</code></div>
```

**Stuck fold.** Optional, and it ships closed. At most two nudges, each one sentence, each pointing deeper into a linked page with a section name or a phrase to search for. A nudge never names the answer when finding it is the exercise. The minimal-teaching regime plus no-oracle hidden tests needs exactly this recourse, and it teaches lookup rather than undermining it. Exception, topics 23 to 25 assume no concurrency knowledge, so their nudges may run to five sentences. No stdlib doc page teaches what concurrency is.

```html
<details><summary style="cursor:pointer; font-weight:bold; padding:0.3em 0;">Stuck? Two nudges inside</summary><ul><li>NUDGE SENTENCE.</li></ul></details>
```

**The folded state.** Both folds ship collapsed, so the default render is the folded state. With both folds closed, the learner sees the Goal sentence, the Read links, and the red Banned line. That view must fully specify the question, and every question is tested against that bar before import. The Python course's bar was that a folded question must still be answerable. This course's bar is stricter. The folded question plus the linked pages must be answerable, and the question alone must not be. A question answerable without opening any link has smuggled teaching back in, and fails review.

## The Banned line

One red line replaces the Rules block. It renders as a single bordered strip reading, for example, "Banned: for, append", with each item in code styling.

```html
<div style="border-left:4px solid #d9534f; padding:0.5em 1em; margin-top:1em; background:#fdf3f2;"><b>Banned:</b> <code>for</code>, <code>append</code></div>
```

A question can also require tokens, and can carry one countable bound. The clauses join the same line, separated by full stops, in the order Banned, Required, Limit.

```html
<div style="border-left:4px solid #d9534f; padding:0.5em 1em; margin-top:1em; background:#fdf3f2;"><b>Banned:</b> <code>for</code>, <code>len</code>. <b>Required:</b> <code>strings.HasPrefix</code>. <b>Limit:</b> one line per function body.</div>
```

HTML-escape operator tokens, so a channel receive ban is written `&lt;-`. A question that bans nothing omits the line entirely.

### The contract

Every item on the red line is enforced by a hidden check. That promise is what makes one line enough, because the learner never has to wonder which rules are real. Anything unenforceable never enters the line.

### How each item maps to a source-text check

The grading wrapper is a Python script that holds the submitted source as its own string before generating the harness. Every check therefore runs on the learner's code alone and can never match the test code. This removes the Python course's `inspect.getsource` self-match caution entirely.

The check pipeline, per question.

1. Strip comments and string, rune, and raw backquote literals from the submission with a regex pass. Without this, a comment reading "no for loops here" trips its own ban.
2. For each keyword or identifier item, apply a must-not-match regex with word boundaries, `\bfor\b`, `\bappend\b`, `\blen\b`. Boundaries are mandatory. A bare substring check for `for` fires inside `format`, a bounded one does not. Selectors such as `errors.Is` escape the dot and use the same boundaries.
3. Operator items come from a small fixed table of bespoke patterns in the prototype, for example `==` as `(?<![=!<>])==(?!=)`. Only operators in the table may be banned. A loose literal match false-fires, because banning `-` would hit `<-`.
4. Literal-class bans are the exception to step 1. Banning `0`, `"`, or a digit sequence such as `127` runs against the comment-stripped source only. The literal is the target of the ban. Required literal tokens such as `%w` follow the same rule.
5. Required items use the same matchers as must-match checks.
6. On any violation, the wrapper prints `banned token present: for` or `required token missing: strings.HasPrefix` and skips compilation, so the failure names its reason without leaking hidden test inputs. Reserve the first hidden test case as the rules case, expected output `rules ok`.
7. The validator runs every check against the sample answer. A check that fires on the sample answer is a broken question and the file is rejected.

Each `Limit:` item maps to a count instead of a match. `Limit: one line per function body` counts non-blank submission lines outside the signature. `Limit: one return` counts `\breturn\b` matches on the stripped source. Only countable limits are permitted.

### Constraints that are not tokens

A constraint that is neither a greppable token nor a countable bound never goes on the red line. Prefer enforcing it behaviourally with a hidden test. The Ticket Machine sketch in the theming guide shows the shape. Its interleaved two-instance test fails shared state on stdout, so "no package-level variables" needs no source check at all. Where no behavioural test exists, accept the gap into the residual risk table below, or cut the question. The Python course's honour-system category is abolished for this course. Its members either get rewritten into an enforceable form, get caught by a test, or the gap is named and accepted where it stands.

### The proven template

The `go_program` prototype in [prototype-go-program.xml](prototype-go-program.xml) implements this pipeline and is proven end to end, see open item 3. An author writes the red line's items into the question's `templateparams` as `{"banned": "for len", "required": "strings.HasPrefix", "limit": "bodylines=1"}`, space-separated within each parameter. Only operators in the prototype's table may be banned. Every question with a red line carries the `// rules` test case first, expected `rules ok`, hidden. The `go_testwriter` type is the exception. Every one of its testcases carries an implementation variant, so no slot for a rules case exists. The template stops the run before the first `go test` instead.

## Theming guide

A theme is a fictional frame that names the constraint or the trap. It is never decoration. Delete the theme and the task must change. If the story could wrap any task, it is decoration, and it goes.

### What George Bool got right

The learner's favourite question ever banned the words `true` and `false` and asked for a working boolean. Take it apart and five properties fall out, and a new theme must have all five.

1. The twist is what the ban removes. The obvious spelling of the answer is banned, so the learner must reach the same output through the mechanism underneath the syntax. Comparisons produce booleans, and that fact is the lesson.
2. The ban has exactly one idiomatic exit. Not zero, which produces contortions, and not three, which produces a shrug. The exit is the target idiom of the build-plan row.
3. The name is the concept. George Boole is where booleans come from. Saying the name a year later recalls the mechanism. That is the bar for every name, and this guide calls it the George Bool standard.
4. The theme fits in the constraint. No backstory paragraph. The whole twist is one banned line.
5. Passing produces a sentence. The moment of passing should restate the doc sentence being taught, in the learner's head, in his own words.

### The five-step recipe

For each themed row of the build plan.

1. Write the mechanism sentence. One sentence of the form "X works because Y", taken from the row. For row 10.2, "append can mutate a neighbouring slice because both slices share one backing array and spare capacity".
2. Name the reflex spelling. What would this Java developer, or a careless Go developer, type first? The build plan's "against" clauses list most of them.
3. Ban until one exit remains. Then attack your own question. Write the sample answer plus at least two cheats. Every cheat must either trip a source check or fail a hidden test. If a cheat survives, add a hidden test, not another ban.
4. Name the theme after the mechanism, not the story. Good sources are the person behind the idea, the failure mode dramatised, and the pattern being buried. Apply the George Bool standard before keeping a name.
5. Pick the doc link that contains the exit. Then confirm the question is solvable from that one page plus the folded question text. If it is not, the question still teaches from its own prose, and that fails the docs-first bar.

### What makes a theme work

- The theme constrains, it does not decorate.
- The test data lives inside the theme. Hotel rooms, ballots, turnstile counts. Hidden tests then read as more of the story rather than as arbitrary inputs.
- One twist per question. A second clever constraint dilutes the first.
- The twist is a language mechanism, never an algorithm. If solving needs an insight about the data rather than about Go, cut it. Small numbers, short strings, no cleverness spent outside the language.
- Two sentences of scene, maximum. A theme that needs more explanation than that is the wrong theme.
- Never let the theme force silly identifiers into the Go code. Function names in starter code and sample answers stay production-conventional and gofmt-clean. The theme lives in the prose and the data, not in the program.

### Four worked sketches from the build plan

Every doc link below was fetched and confirmed on 2026-09-02.

**WAT 02.1: George Boole Rides Again!** Scene, the memorial ballot on whether Mr Boole gets a statue. Task, `eligible(age int) bool` and `carried(ayes, votes int) bool`. Banned: `true`, `false`. Exit, comparisons produce booleans, and `var ok bool` is already false because zero values exist. Docs, [Boolean types](https://go.dev/ref/spec#Boolean_types) and [The zero value](https://go.dev/ref/spec#The_zero_value) in the spec. Hidden tests vary the vote counts so no literal can be smuggled through arithmetic.

**WAT 10.2: The Haunted Duplex!** Scene, a landlord slices one hallway into two flats. A tenant repainting flat A's end wall finds the paint appearing in flat B. Task, `partition(hall []string) ([]string, []string)`. The two returned halves must not bleed into each other when appended to. Banned: `copy`, `make`, `append`, the last closing the clone-by-append cheat, `append([]string(nil), hall[:k]...)`. Exit, the three-index full slice expression, which caps capacity so append reallocates. Doc, [Slice expressions](https://go.dev/ref/spec#Slice_expressions) in the spec. The hidden test appends through the first returned slice and prints the second, so bleed is a visible wrong answer. The test's own appends live in test code, which the scan never touches.

**WAT 18.3: The Ticket Machine That Remembers!** Scene, a turnstile dispenses numbered tickets and there is no drawer to keep the count in. Task, `newMachine() func() int` returning a function that yields 1, 2, 3 on successive calls. Banned: `struct`, `type`. The "no package-level variables" clause needs no source check. The hidden test runs two machines interleaved, and shared state prints the wrong sequence. Exit, a closure over a local variable. Doc, [Function closures](https://go.dev/tour/moretypes/25) in the Tour. Its position is confirmed against the canonical article sources in research-godev-learn.md, because the page itself renders via JavaScript.

**WAT 22.2: Yield of Dreams!** Scene, a countdown that players walk out of one at a time. Task, `countdown(n int) iter.Seq[int]` and a consumer that ranges over it and breaks early. Banned: `append`, `make`. The bans close the escape route of building a slice first. The hidden test breaks out of the range loop mid-sequence. An iterator that ignores yield's return value then panics at runtime, so the yield contract is machine-checked. Doc, [package iter](https://pkg.go.dev/iter), where `Seq` is defined with the contract that iteration stops when yield returns false.

### Naming rules

- Format stays `WAT NN.T: Fun Name!`, exclamation mark included, six words or fewer, one pun maximum.
- No two names alike anywhere in either course. Grep this file, the Python spec at [../python/TOPICS.md](../python/TOPICS.md), and the built question files at `../python/topic-*.xml` and `topic-*.xml` before keeping a name. The Python spec holds only a handful of moved-anchor names, and the real names live in the XML. Openings count. Two names that start with the same three words are alike.
- The name must pass the George Bool standard. Said aloud a year later, it recalls the mechanism.
- The name may hint at the concept but must not spoil the exit. The Haunted Duplex says shared walls. It does not say three-index slice.

## Per-topic build plan

The Coming from Java fold carries the reflex each question punishes, and topics 23 to 25 omit it. The Banned column is the question's red line in the exact format above, and "none" means the question ships no red line. A row whose red line carries a Required or Limit clause, an operator, a literal, or a common-word ban waits on open item 3. The proven-template section states the marking rule. The Doc column names the pages the Read panel links. Every path below was fetched and confirmed on 2026-09-02, in the design workflow or in this rewrite. Spec anchors are sections of go.dev/ref/spec.

| Tier | Content | Banned line | Doc |
| --- | --- | --- | --- |
| 01.1 | Braces Are Back! `package main`, `fmt.Println`, and the shape of a Go file. `package main` and `func main` are taught in the Read links and prose only, because the grader supplies `main` and the learner fills the scaffolded function it calls. Against Java's class ceremony. gofmt from the first line. | Banned: Printf | pkg.go.dev/fmt#Println, #Print, #Printf |
| 01.2 | The Unused Variable Police! Unused imports and variables are compile errors, not warnings. Fix a program that will not build. The learner deletes a given `var` line, and the declaration form is taught properly at topic 02. | Banned: _ | spec #Import_declarations, #Variable_declarations |
| 01.3 | Miles to Go! A first `if` and `else`, no parentheses, braces required. Branch on values and print a formatted block. Scaffolded signature. | none | spec #If_statements, #Comparison_operators |
| 02.1 | George Boole Rides Again! `var`, zero values for every type, comparisons produce booleans. Against null and NPEs. Sketch in the theming guide. Scaffolded signatures. | Banned: true, false. Required: var | spec #Boolean_types, #Comparison_operators, #The_zero_value |
| 02.2 | Short Declaration Showdown! `:=` inside functions, `var` at package level, shadowing as the edge case. Scaffolded signature. | none | spec #Short_variable_declarations |
| 02.3 | Constants of the Universe! `const`, untyped constants, iota for a small enum. Against `static final` and Java enums. Scaffolded signature. | Required: iota | spec #Iota |
| 03.1 | Change and Verdict Together! Multiple return values. Against single-return Java and out-parameters. | Banned: :=, var | spec #Return_statements |
| 03.2 | The Naked Return Ban! Named results exist and naked returns are forbidden, enforced by the `nakedreturn` pseudo-token. Return early, return explicitly. | Banned: nakedreturn, 0, false | spec #Return_statements |
| 03.3 | Swap Meet! Multiple assignment, swapping without a temp, functions calling functions. | Limit: four lines per function body | spec #Assignment_statements |
| 04.1 | Trim Before You Guess! Two behaviours described, two doc sentences decide which function is which. Hidden test on `"google.com"`. | Banned: for | pkg.go.dev/strings#TrimPrefix, #TrimLeft |
| 04.2 | Scavenger Hunt at pkg.go.dev! Three needs described by behaviour only, three package roots linked, hidden tests make the index walk the intended route. | Banned: for, len, 127 | pkg.go.dev/strings, pkg.go.dev/unicode/utf8, pkg.go.dev/math |
| 04.3 | Needle in a Package Stack! No package named. Quote a string as a Go literal, round ties to even. Hidden ties at -10.5, 2.5, 12.5. | Banned: for, if | pkg.go.dev/std |
| 05.1 | Four Loops, One Keyword! `for` in its three forms, a single condition, a for clause, and a range clause. Against Java's for, while, and for-each. | Required: for, range | spec #For_statements, #For_range |
| 05.2 | Switch Without a Break! Implicit break, arbitrary case expressions, `if` with a short statement. Against Java switch expressions. | Banned: break | spec #Switch_statements, #If_statements |
| 05.3 | Labels of Love! Nested loops, `break` and `continue` with labels, `for` with no condition and an exit. A label declared and never used is a compile error, which Java has no equivalent of. | none | spec #Break_statements, #Continue_statements, #Label_scopes |
| 06.1 | Verbs of Format! `fmt.Printf` verbs `%v %d %s %q %T`. Against `String.format`. | Banned: Println. Required: %T | pkg.go.dev/fmt#hdr-Printing |
| 06.2 | A Rune with a View! Strings are bytes, `range` yields runes, byte length against rune count. | Banned: utf8, RuneCountInString | go.dev/blog/strings |
| 06.3 | The Builder Retires! `strings.Builder` against StringBuilder ceremony and `+` in loops. | Banned: +, Sprintf. Required: strings.Builder | pkg.go.dev/strings#Builder, #Builder.Len, #Builder.WriteRune |
| 07.1 | Records Without the Ceremony! Struct definition and composite literals with field names. Against record declarations. | none | spec #Struct_types, #Composite_literals |
| 07.2 | Equal by Value! Struct equality with `==`. equals and hashCode boilerplate has no Go equivalent to write. | Required: == | spec #Comparison_operators, #Composite_literals |
| 07.3 | The NewFoo Convention! Constructor functions that normalise and default their inputs. Validation that can fail waits for topic 14. | none | pkg.go.dev/strings#NewReplacer, #TrimSpace |
| 08.1 | The Copy Machine! Structs copy on assignment and on call. A mutation in the callee vanishes. Against everything-is-a-reference. | Banned: & | spec #Calls, #Representation_of_values |
| 08.2 | Ampersand of Time! `&` and `*`, pointers to structs, implicit dereference on field access. | Required: & | spec #Address_operators, #Selectors, #Assignment_statements |
| 08.3 | Mutate or Copy, Choose! A function that mutates through a pointer against one that returns a modified copy. When each is right. | none | spec #Pointer_types, #Selectors, #Representation_of_values |
| 09.1 | ArrayList No More! Slice literals, `len`, `append` with reassignment, `range` over slices. Indexing moves to 09.3, because teaching an index expression here would hand the learner a C-style loop that passes every test without opening the range clause. That escape route stays open to a learner who already knows the syntax, and is accepted. No topic below 09 writes one. | Required: append | go.dev/blog/slices-intro, spec #For_range |
| 09.2 | The Warehouse Doubles Overnight! Capacity, growth, `make`. What `append` does when capacity runs out. `append` is variadic, and declaring a variadic parameter is taught here, ahead of topic 26's options. | Required: make | pkg.go.dev/builtin#make, pkg.go.dev/builtin#append, spec #Passing_arguments_to_..._parameters |
| 09.3 | Slice and Dice! Slicing expressions, defaults, slices of slices, and the indexing that fills the outer slice. | Banned: append | spec #Slice_expressions, spec #Slice_types |
| 10.1 | The Backing Array Conspiracy! Two slices over one array. A write through one is visible through the other. | Banned: copy | go.dev/blog/slices |
| 10.2 | The Haunted Duplex! Two halves of one slice fenced with the full slice expression so append cannot bleed. Sketch in the theming guide. | Banned: copy, make, append | spec #Slice_expressions, pkg.go.dev/builtin#append |
| 10.3 | Copy That! `copy`, cloning idioms, when aliasing is wanted and when it is a bug. | Banned: for. Required: copy | pkg.go.dev/builtin#copy, go.dev/blog/slices |
| 10.4 | Death to i := 0! Tier 4. AI code indexing with a C-style loop where `range` belongs, passing every test. Rewrite it. | Required: range | spec #For_range |
| 11.1 | HashMap Goes on a Diet! Map literals, lookup, insert, delete. Against HashMap ceremony. | none | go.dev/blog/maps |
| 11.2 | The Comma-OK Corral! A recorded zero and a missing key must never be confused. The two-value form is the only distinguisher. | Banned: len, range | spec #Index_expressions |
| 11.3 | Sorted, Because Random! Iteration order is deliberately random. Sort keys to print deterministically. | Required: slices.Sort | pkg.go.dev/slices#Sort, go.dev/blog/maps, spec #Comparison_operators |
| 12.1 | Methods Without Classes! Method declarations with receivers, on structs and on named types. | none | spec #Method_declarations, go.dev/tour/methods/3, spec #Method_expressions |
| 12.2 | The Receiver Will See You Now! Value receivers copy. A mutation through a value receiver vanishes. | none | spec #Method_declarations, #Calls, go.dev/tour/methods/4 |
| 12.3 | Pointer or Value, Pick One! The receiver decision rules, and one type never mixes them. | none | spec #Method_sets, #Calls, #For_range |
| 13.1 | No Implements Needed! Define an interface, satisfy it implicitly. Against `implements` and Adapter classes. | none | spec #Interface_types |
| 13.2 | Small Interface, Big Abstraction! One and two method interfaces. The consumer defines what it needs. Against twelve-method services. | none | pkg.go.dev/io#Reader, #ReadWriter, spec #Implementing_an_interface |
| 13.3 | The Stringer Quartet! `fmt.Stringer` implemented and used by `Printf` automatically. Against toString. | Required: String | pkg.go.dev/fmt#Stringer, #hdr-Printing |
| 13.4 | The Impl Impostor! Tier 4. AI code with a producer-side interface and an Impl-named struct. Move and shrink the interface. The ban forces the rename, the shrink is worded in the task, and its unverifiability is accepted. | Banned: StoreImpl, Store | pkg.go.dev/io |
| 14.1 | Errors Are Values! A function returning `(T, error)`, the `if err != nil` check. Against throws. | Banned: panic | go.dev/blog/errors-are-values, spec #Errors, pkg.go.dev/strconv#Atoi |
| 14.2 | The Happy Error Path! Early return on error, no nesting. Guard clauses as the house style. | Banned: else | pkg.go.dev/errors |
| 14.3 | The Sentinel's Watch! Sentinel errors with `errors.New`, compared with `errors.Is`. Against catch by exception class. | Banned: ==. Required: errors.Is | pkg.go.dev/errors#Is, #New, pkg.go.dev/io#pkg-variables |
| 15.1 | Wrap It With %w! `fmt.Errorf` wrapping, context added at each level, handle once. | Required: %w | pkg.go.dev/fmt#Errorf, pkg.go.dev/errors#Is |
| 15.2 | Is, As, and the Chain! `errors.Is` and `errors.As` through a wrapped chain, a custom error type with fields. A hidden test whose wrapped chain defeats string comparison enforces the no-string-matching intent. | Banned: ==. Required: errors.As | pkg.go.dev/errors#As, #Is |
| 15.3 | The Nil That Wasn't! A typed nil pointer returned as `error` makes `err != nil` succeed. The interface value model explains it. | none | spec #Comparison_operators, #Variables |
| 15.4 | Panic! at the Codebase! Tier 4. AI code that panics on bad input and passes its happy-path tests. Rewrite with error returns. | Banned: panic. Required: %w | go.dev/blog/defer-panic-and-recover |
| 16.1 | Table Stakes! A first table-driven test. A slice of cases, a range, `t.Errorf`. Two mutants to kill. | Required: range | pkg.go.dev/testing |
| 16.2 | Run, Subtest, Run! Subtests with `t.Run`, one name per case. The function literal arrives by doc link. | Required: t.Run | go.dev/blog/subtests, pkg.go.dev/testing#T.Run |
| 16.3 | Kill All Mutants! Four or five mutants, each breaking one documented clause. Derive the killing inputs from the contract. | none | pkg.go.dev/testing#T, pkg.go.dev/strconv#Atoi, #ParseInt |
| 17.1 | Defer of Duty! `defer` for cleanup. Against try-with-resources and finally. | Required: defer | go.dev/blog/defer-panic-and-recover |
| 17.2 | The LIFO Parade! Stacked defers, arguments evaluated at defer time, defer in a loop as the trap. | Required: defer | spec #Defer_statements |
| 17.3 | Recover, Not Catch! `panic` and `recover` at a boundary, and why library code returns errors instead. | Banned: nakedreturn. Required: recover | spec #Handling_panics, go.dev/blog/defer-panic-and-recover |
| 18.1 | Functions Are Values Here Too! Func types, passing behaviour as an argument. Against functional interfaces and SAM conversion. | none | spec #Function_types, #Function_literals |
| 18.2 | Strategy Dissolved! `sort.Slice` with a less function. The Strategy pattern with no pattern left. | Required: sort.Slice | pkg.go.dev/sort#Slice |
| 18.3 | The Ticket Machine That Remembers! A closure over a local count. Two interleaved machines expose shared state. Sketch in the theming guide. | Banned: struct, type | go.dev/tour/moretypes/25 |
| 19.1 | Extends Is Dead! Struct embedding, method promotion. Composition as the only tool. | none | spec #Struct_types |
| 19.2 | The Override That Never Fires! Embed, redeclare on the outer type, call through the inner path. No dynamic dispatch to the outer type. | none | spec #Selectors |
| 19.3 | The Bufio Overcoat! Decorator by interface wrapping. A wrapped implementation that adds behaviour before delegating. | none | pkg.go.dev/bufio#NewReader, pkg.go.dev/io#Reader, pkg.go.dev/bufio#Reader.ReadString |
| 20.1 | Switch on Type! Type assertions with comma-ok, `switch v := x.(type)`. Against instanceof chains and pattern matching. The bans close the if-else and comparison route, because no stdout test can tell a type switch from a run of comma-ok assertions. | Banned: if, ==, != | spec #Type_switches, #Type_assertions, #Interface_types |
| 20.2 | Sealed With a Marker! A closed set via an unexported marker method, named `sealed` so the check can see it. Against sealed interfaces. The question teaches that the sealing force exists only across package boundaries, which a one-file submission cannot show. Which struct declares which method is never stated, so the learner derives it from the type-set sentence. | Required: sealed | spec #Interface_types, #Uniqueness_of_identifiers, #Type_assertions |
| 20.3 | Silent Default, Loud Error! No exhaustiveness checking. Add a variant, watch the silent default, fix by returning an error. A stated rule that a pointer prices the same as its value makes the dynamic-type match the grade. | none | spec #Type_switches, pkg.go.dev/errors#Is |
| 21.1 | Brackets, Not Erasure! A generic function with a type parameter and constraint, a generic max. Against erasure, Go instantiates. The `cmp` ban is a deviation from this plan's original `Banned: any`, added on 2026-09-03. Without it, `type Ranked interface { cmp.Ordered }` passes every test and the tilde is never read. | Banned: any, cmp | go.dev/blog/intro-generics |
| 21.2 | The Zero-Value Or-acle! `cmp.Or` read from its doc and called. The hidden all-zero case is answerable only from the doc comment. A generic signature is readable before generics are writable. | Banned: if, for, switch, len | pkg.go.dev/cmp#Or |
| 21.3 | Methods Go Generic! Type parameters on concrete methods, new in Go 1.27. A chainable `Map` on a list type, and the limits. | none | go.dev/blog/go1.27, go.dev/blog/generic-methods |
| 21.4 | When Any Is Too Much! A function where an interface beats a type parameter, and one where the reverse holds. Judgement, not syntax, and no AI code is shown. | none | go.dev/blog/when-generics |
| 22.1 | The Stream Detox! Filter and transform a slice with a plain loop. The loop is the idiom, not a fallback. | Banned: slices. Required: range | spec #For_range |
| 22.2 | Yield of Dreams! `iter.Seq`, a countdown iterator consumed with `range` and broken out of early. Sketch in the theming guide. | Banned: append, make | pkg.go.dev/iter#Seq, pkg.go.dev/iter |
| 22.3 | Collect Yourself! `slices` and `maps` package helpers, sorting included. | Required: slices.Collect, maps.Keys | pkg.go.dev/maps#Keys, pkg.go.dev/slices#Collect, #Sort |
| 22.4 | Cosplaying the Chain! Tier 4. AI Go chaining helper calls where one loop is clearer, passing every test. Rewrite as one loop. Go 1.27 generic methods make chains possible, not mandatory. | Banned: slices.Clone, slices.DeleteFunc | pkg.go.dev/slices#DeleteFunc, #Clone, pkg.go.dev/slices |
| 23.1 | Go Means Go! What a goroutine is, concurrency against parallelism, why main exiting kills everything. A WaitGroup makes the wait explicit. | Required: go | spec #Go_statements, pkg.go.dev/sync#WaitGroup |
| 23.2 | Wait for the Group! Fan out N goroutines over a slice, each writing its own result index, print in order. Loop variables are per-iteration since Go 1.22. | Banned: Add, Done. Required: sync.WaitGroup | pkg.go.dev/sync#WaitGroup, #WaitGroup.Go, spec #For_range |
| 23.3 | Fan Out, Fall In! Parallel computation over structs with methods, indexed writes, sorted print. Why distinct indices need no lock. | Banned: Add, Done. Required: sync.WaitGroup | pkg.go.dev/sync#WaitGroup, #WaitGroup.Wait |
| 24.1 | Don't Share, Communicate! One producer, one consumer, a channel between. The blocking is the synchronisation. | Required: chan, <- | spec #Channel_types, #Receive_operator |
| 24.2 | Range and Close! Producer closes, consumer ranges. Channel direction types in signatures. | Required: close | pkg.go.dev/builtin#close, spec #For_range, #Channel_types |
| 24.3 | Select Committee! `select` over two channels, a done channel, Observer as a subscriber channel. | Required: select | spec #Select_statements, #Receive_operator |
| 25.1 | Mutex When It Counts! What a data race is, shown before it is fixed. `sync.Mutex` guarding a counter under concurrent writers. Prototype the race in the Jobe container first, per the grading model. | Required: sync.Mutex | pkg.go.dev/sync#Mutex, #Mutex.Lock, #Mutex.Unlock |
| 25.2 | Carry the Context! `context.Context` as the first parameter, cancellation observed through explicit `cancel()` calls and a deadline already in the past. No live timers, because a wall-clock test is flaky inside the sandbox. The `context.WithDeadline` requirement is a deviation from this plan's original `Required: context.Context`, made on 2026-09-03, because the deadline call is the act the question grades. | Required: context.WithDeadline | pkg.go.dev/context, #WithDeadline, #CancelFunc |
| 25.3 | Cancel Culture! A worker that stops when its context is cancelled, no goroutine outlives its caller. | none | go.dev/blog/context, pkg.go.dev/context#Context |
| 26.1 | Builder Reborn! Functional options on a NewServer constructor, and the config-struct alternative the stdlib itself uses. The trade-off is taught, not one winner. | none | pkg.go.dev/net/http#Server |
| 26.2 | The Miniature Core API! A store behind a consumer-defined interface, a NewFoo constructor, wrapped errors, options, and an orchestration function composing it. The DT Platform shape in one file. | none | pkg.go.dev/io#EOF, #Reader |

## Grading model for Go

Grading is exact-match on printed output, as for Python. Go adds constraints the author must design around.

- Every WAT except topic 16 is one compiled program on the `go_program` question type. The learner writes a complete file with `package main` and no `main` function. The template generates a harness main that switches on an argument, compiles once, and runs once per test. The prototype is imported and proven end to end through the real stack, on 2026-09-02. A warm-cache compile is under a second and a five-test WAT grades in one Jobe request.
- Map iteration order is unspecified and the runtime randomises it on purpose. A test that prints a map either prints via `fmt.Println` on the whole map, which prints keys sorted, or sorts keys itself. Both behaviours were verified with go 1.26.2 on 2026-09-02. Topic 11.3 teaches the discipline the tests already follow.
- Concurrency output must be made deterministic by the exercise design itself, with WaitGroups, channels, or collected-then-sorted results. A test that could interleave is a broken test.
- A data race cannot be graded by one exact-stdout run. An unsynchronised counter can print the correct total, the pipeline does not run `-race`, and a single-CPU sandbox makes lost updates rare. Before authoring 25.1, run a mutex-less counter in the Jobe container, check GOMAXPROCS there, and measure how often it passes. If racy code passes often, the demonstration moves to prose and a deterministic exercise, with `Required: sync.Mutex` as the only race enforcement, stated as such.
- Floating point prints with `%v` in Go's shortest representation. Run every expected value, never predict it, as AUTHORING.md already demands.
- Compile errors are teaching material. Topic 01.2 grades on fixing one. Everywhere else, a sample answer that does not compile is a broken question, caught by the validator.

### The go_testwriter type for topic 16

Topic 16 inverts the grading and needs a second question type. The learner submits a `_test.go` file. Each testcase's `extra` field holds one implementation variant, the first correct and the rest mutants. The wrapper compiles and runs `go test` once per variant, with the learner's tests beside it. The question passes when the correct variant passes and every mutant fails. Each testcase's expected output states its variant's verdict, so a surviving mutant is a visible, named failure. The prototype at [prototype-go-testwriter.xml](prototype-go-testwriter.xml) is built and proven through the real stack on 2026-09-02. The proof includes a weak-test path, where an under-asserting sample let a mutant survive and failed validation.

## Tier 4, judging AI output

Same protocol as the Python course. The question shows Go that passes every test and is still wrong for a reader. The flaw list for this course:

- A C-style index loop where `range` belongs.
- A producer-side interface, or an interface with more methods than its consumer calls.
- panic on ordinary failure instead of an error return.
- Helper-call chains imitating Java streams where a loop belongs.
- Getters and setters on exported fields.
- `any` where a concrete type or small interface belongs.

Place one tier 4 question per major area, as placed in the build plan, at 10.4, 13.4, 15.4, 21.4, and 22.4.

A tier 4 rewrite is constrained the same way as any other question. Where the flaw is token-checkable, the Banned line enforces its absence. `Banned: panic` does this at 15.4, and `Required: range` does it at 10.4. Where it is not, the flawed code sits in the starter code itself, for the learner to read and replace. The hidden tests hold the correct behaviour steady. The Goal panel states that the shown code came from an AI. That is exercise content, not policy, so it stays even though the AI protocol panel is gone.

## What the WAT format cannot teach

A WAT is one file graded on stdout inside a sandbox with no network. Topic 16's `go_testwriter` type brings the test runner inside the format for one package at a time. Deterministic exact-stdout also cannot distinguish a goroutine solution from a sequential one. Topic 23's Required tokens therefore certify the spelling of concurrency, not its presence. A plain loop plus a decorative WaitGroup passes. The channel topics get real enforcement, because a blocking send deadlocks a sequential rewrite. That limit is accepted. Still excluded are modules and `go mod`, HTTP servers, `database/sql`, project layout across packages, and the generated OpenAPI client workflow. The go.dev research names these as the official material's own gaps, and this course does not close them either. It teaches the language and the idioms that work is built from. The closing step is reading and writing real code in the DT Platform proof of concept, where those topics live. The capstone is the closest the format gets. It composes a consumer-defined interface, a constructor, options, and wrapped errors through one orchestration function, in memory.

## Prose

Follow the technical-writing skill and the Python spec's prose rules unchanged. British English. No em dashes, no semicolons, no colons as mid-sentence connectors. Never "simply", "just", "easy", "powerful", "leverage", "utilise", or "note that". The Coming from Java fold names the reflex in at most three sentences, and topics 23 to 25 open from the problem instead. Explain every Go term on first use.

Run the prose checker on every question file. The angle-bracket check matters more in Go, because `&`, `<-`, and generic brackets appear in ordinary code. Escape them in `testcode` and `expected` per AUTHORING.md.

## Accepted residual risks

Each row records a cheat or a gap that no source check closes, so a reviewer does not refile it as a defect. The authoring pass measured every one of them by running the cheat through the simulator.

| WAT | Risk | Why it is accepted |
| --- | --- | --- |
| 01.1 | The name recalls braces while the graded fact is Println's operand spacing and appended newline. | The build plan fixes the name, so the mechanism moved into the Goal and the hidden tests. |
| 01.2 | A self-assignment such as `note = note` keeps an unused local alive, and no token ban reaches it. | Banning those identifiers would print the answer on the red line. |
| 02.1 | A package-level `var dummy int` satisfies `Required: var` while the body compares against a literal. | No token check separates the two spellings, and both produce identical values. |
| 02.3 | `const _ = iota` followed by eight hand-numbered literals satisfies `Required: iota`. | No token check separates the two spellings, and no hidden test can see the difference. |
| 03.1 | A `concession` that repeats `issue`'s comparison instead of calling it passes every test. | A `Limit: return=3` clause would risk rejecting a correct answer that uses an else branch. |
| 03.2 | The banned refusal values `0` and `false` can be reached by arithmetic such as `age-age`. | WAT 04.2 accepts the same class of residual for its `127` ban. |
| 03.3 | The blank identifier is not forced, because a four-line `bounds` that reassigns `c` exists. | Tuple assignment is still forced in `bounds`, so the row keeps grading multiple assignment. |
| 04.2 | The banned literal `127` can be smuggled through arithmetic such as `1<<7 - 1`. | `clueLimit` therefore appears in a hidden test only and never in a visible one. |
| 04.2 | `strings.Count(badge, "")` minus one returns the rune count without opening the second package root. | A `Required` clause naming `utf8` would name the answer on the red line. |
| 06.1 | `Required: %T` is satisfied by a live string literal such as `_ = "%T"`. | The check runs on comment-stripped source, and the signature fixes mass as float64. |
| 06.2 | `len([]rune(name))` reaches the rune count with no banned token. | Slices and conversions arrive at topic 09, outside a topic 06 learner's gate. |
| 06.3 | One `strings.Builder` plus `strings.Join` for the other two functions passes every check. | That shape is idiomatic Go and performs no quadratic concatenation. |
| 07.2 | A field-by-field comparison passes every test in place of whole-value `==`. | For a struct of comparable fields the two are semantically identical. |
| 09.1 | A C-style index loop passes every test without opening the range clause. | Teaching indexing here would show the learner that loop, and no topic below 09 writes one. |
| 12.3 | Both receiver-mixing cheats pass all four tests, so the one-receiver-kind rule is unenforced anywhere, in prose or in a check. | The rule lived only in the now-removed Your task panel. No behavioural test distinguishes the cheats from the intended answer, so the gap is accepted rather than reworded. |
| 13.4 | A five-method interface named `Getter` passes, so interface arity is unenforced. | Test code cannot declare methods, so it cannot build a value carrying only `Get`. |
| 15.3 | The naive typed-nil answer fails visible test 2 rather than only the hidden rows. | The visible expected value is only "clean", so the hidden cases still carry the discrimination. |
| 17.1 | Calling `signOut` manually before each exit, plus a throwaway `defer`, passes every test. | No behavioural distinguisher exists without `panic`, which belongs to WAT 17.3. |
| 17.2 | A stall-aware manual reverse unwind, plus a throwaway `defer`, passes every test. | Separating deferred from manual unwinding needs a panic mid-loop, which belongs to WAT 17.3. |
| 19.2 | The name shares its first three words with WAT 18.3 in the Python course. | The Python question is outside this course's scope. |
| 20.1 | `switch fmt.Sprintf("%T", item)` on `"<nil>"` detects a nil interface with no banned token. | WAT 04.2 accepts the same class of residual, and nobody writes that spelling. |
| 21.2 | The Stuck nudge names the all-blank board that the rest of the file avoids naming. | The review finding instructed that this one nudge be left as it stands. |
| 24.3 | `sit` busy-spins when `motions` is closed, which no test exercises. | Clearing an exhausted channel is machinery this tier 3 row does not teach. |
| 25.1 | At GOMAXPROCS=1 the mutex-less cheat survives every run, and repetition cannot close it. | The grading container reports GOMAXPROCS=2, which keeps the aggregated hidden test deterministic. |

## Open items before authoring starts

1. Done 2026-09-02. The `go_testwriter` prototype is built at [prototype-go-testwriter.xml](prototype-go-testwriter.xml). It is imported to course 13 with its smoke question and validated through the real stack, weak-test path included.
2. Done 2026-09-02. `tools/simulate-grader-go.py` mirrors both templates and branches on the question type.
3. Done 2026-09-02. The `go_program` template now strips comments and literals and carries the operator table (`== != + & && || ! <- := % *`). It also carries the `nakedreturn` pseudo-token and literal-class bans matched on comment-stripped source. It adds `required` and `limit` parameters (`return=N`, `bodylines=N`), named failure messages, and the reserved `// rules` test case printing `rules ok`. Template parameters are `{"banned": "for ==", "required": "+", "limit": "return=1"}`. The simulator executes the check block out of the prototype XML, so the two cannot drift. Seven violation kinds and four non-firing cases were proven in the simulator. The smoke question plus two violations were proven through the live stack. AUTHORING.md documents the parameters.
4. Done 2026-09-03. AUTHORING.md carries the section "Authoring a Go WAT".
5. Done 2026-09-03. `courses/go/manifest.json` exists and `scripts/bootstrap.sh` builds both courses. A fresh-machine run has not been exercised yet.
6. ADR-10, Go for the core, is Proposed and not yet decided. The course draft proceeds because the team needs Go fluency to evaluate the proposition either way.
