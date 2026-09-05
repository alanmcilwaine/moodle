# How to author a WAT

Read this before writing questions. It is the contract an agent follows to produce a course that imports and grades correctly.

A WAT is one CodeRunner question. The learner sees a description, the example tests, and an editor box holding starter code. The learner writes a function, clicks Check, and passes when the printed output matches the expected output exactly.

## Grading compares printed output

CodeRunner runs the test code and compares stdout against `expected` as an exact string. There are no assertions in the grading itself.

Every test case must print. Match Python's own formatting when you write the expected value:

- A dict prints as `{'a': 1}` with single quotes.
- A string inside a list keeps its quotes. `['a']`, not `[a]`.
- Booleans print as `True` and `False`.
- A float that is a whole number prints as `5.0`, not `5`.
- A function that returns nothing prints as `None`.

Run the code before you write the expected value. Never predict output.

## All test cases share one process

This trips up every new author. The built-in `python3` question type is a **combinator template**. CodeRunner builds one program from the sample answer followed by every test case, runs it once, and splits the output back into per-test results.

Code at module level therefore runs **once for the whole question**, not once per test case.

If your answer prints at module level, that output belongs to the first test case only. Do not repeat it in the expected value of the later test cases.

Questions that define a function and print nothing at import time avoid the problem entirely. Prefer that shape unless the lesson is about top-level code.

State also persists across test cases. A list that test 1 mutates arrives mutated at test 2.

Run the simulator before you import:

```
python3 tools/simulate-grader.py courses/python/topic-01.xml
```

The simulator reproduces the combinator exactly and prints a diff for any mismatch.

## Annotate from topic 13 onward

The Python course teaches type hints in topic 12. Topics 1 to 11 stay unannotated on purpose, because their job is to break the reader's habit of declaring a type before every name. From topic 13 every signature carries annotations, because that is what production Python looks like.

Write modern syntax. Use `list[int]` and `dict[str, float]`, never `typing.List`. Use `str | None`, never `Optional[str]`. Import `Iterator`, `Iterable`, and `Callable` from `collections.abc`. Give a function that returns nothing `-> None`, including `__init__`.

Annotate signatures, not obvious locals. A loop variable needs no annotation, and over-annotating is its own kind of noise.

## Every question needs a sample answer

Put a working solution in `answer`. The validator runs every sample answer against its own tests, and a question whose sample answer fails is rejected. A question without one cannot ship.

## Write the Rules block

Rules are the point of this course. Each rule forbids a habit from the learner's previous language and forces the idiom you are teaching. Write them as short commands, for example "Do not write the word `for`" or "Solve this in one line".

Put the block at the end of the question text in this shape:

```html
<div style="border-left:4px solid #d9534f; padding:0.5em 1em; margin-top:1em; background:#fdf3f2;"><b>Rules</b><ul><li>One rule per list item.</li></ul></div>
```

Enforce a rule with a hidden test case when the check is reliable:

```python
import inspect
src = inspect.getsource(tally)
assert "append(" not in src, "rule broken: build the list with a comprehension"
print(tally([1, 2, 3]))
```

`inspect.getsource` works because the program is a real file. Two cautions. The source contains every test case as well as the answer, so a check can match its own text. A comprehension contains the word `for`, so never test for the bare word on a comprehension exercise.

Run every check against your own sample answer. A check that fails the sample answer is a broken question. Where a rule cannot be checked reliably, display it and leave it to the honour system.

## Structure of the file

Copy the element order from any finished file, such as `courses/python/topic-13.xml`. Per question:

| Element | Holds |
| --- | --- |
| `name` | `WAT NN.T: Fun Name!` where NN is the zero-padded topic and T is the tier, because names sort into teaching order |
| `questiontext` | The five zones from the course spec, wrapped in CDATA |
| `answerpreload` | Starter code for the editor box, usually a signature and a TODO |
| `answer` | The sample solution, wrapped in CDATA |
| `testcases` | Three or four cases |

Mark the first two test cases `useasexample="1"` with display `SHOW`, so the learner sees them. Hide the last one.

Fixed values for every question: `coderunnertype` `python3`, `prototypetype` 0, `allornothing` 1, `penaltyregime` 0, `precheck` 0, `defaultgrade` 1.0000000, `penalty` 0.0000000, `validateonsave` 1, `useace` 1.

Start the file with the XML declaration and a `quiz` root element. Do not include a `question type="category"` element, because the import script chooses the category.

Escape `<`, `>`, and `&` inside `testcode` and `expected`.

## Check your work

Run these three before you hand the file over:

```
python3 -c "import xml.etree.ElementTree as ET; ET.parse('courses/python/topic-01.xml')"
python3 tools/simulate-grader.py courses/python/topic-01.xml
python3 tools/check-angle-brackets.py courses/python/topic-01.xml
```

The prose checker, `tools/check-prose.py`, belongs to this gate but is not yet portable: it hardcodes a path to a personal skill installation and does not run as shipped. Whether to make it portable is a pending decision. Until then, apply the prose rules in `courses/python/TOPICS.md` by hand.

## Keep angle brackets out of expected output

Moodle treats angle brackets in an expected value as HTML. When two such sequences sit on adjacent lines, the newline between them is collapsed during import. The question then rejects output that is actually correct. The XML on disk still looks right, so the fault stays invisible until a learner meets it.

This was found by comparing the stored expected values against the source files after an import. One test case in 255 was affected.

Print `type(value).__name__` rather than `type(value)`. The output reads `tuple` instead of `<class 'tuple'>`, which is clearer teaching as well as safe.

Run the check before you import:

```
python3 tools/check-angle-brackets.py courses/python/topic-NN.xml
```

It fails on the broken pattern and warns on any other angle brackets in expected output.

## Authoring a Go WAT

The Go course keeps exact-match grading on printed output. The layout, the constraint format, and the question types all differ. This section is complete on its own. Do not apply the Python sections above to a Go question.

### The two question types

Choose the type by what the learner writes.

`go_program` covers every topic except 16. The learner writes the implementation, and the grade is the printed output of the grader's calls into it. Use it unless the topic is about writing tests.

`go_testwriter` covers topic 16. The learner writes the test file, and the question carries the implementations. The grade measures whether the suite passes one correct implementation and fails every mutant.

Import the matching prototype into the course before any question of its type. `courses/go/prototype-go-program.xml` and `courses/go/prototype-go-testwriter.xml` hold the two.

### XML differences from Python

Copy the element order from `courses/go/topic-04.xml` for a `go_program` question, or from `courses/go/topic-16.xml` for a `go_testwriter` question. These are the differences from a Python question file.

- `coderunnertype` is `go_program` or `go_testwriter`. `validateonsave` is 0. Every other fixed value matches the Python course.
- `answerpreload` and `answer` both start with `package main`. The learner submits a complete file holding the package clause, the imports, and the named functions. The learner writes no `main`, because the template generates one.
- `templateparams` carries the Banned line as one JSON object. An example is `{"banned": "for len", "required": "strings.HasPrefix", "limit": "return=1"}`. Each value is a space-separated list, all three keys are optional, and a question with no Banned line leaves the element empty.
- `limit` accepts `return=N` and `bodylines=N` and nothing else. Only the operators in the prototype's own table may be banned.
- A `go_program` question with a Banned line puts the rules case first. Its `testcode` is exactly `// rules`, its `expected` is `rules ok`, and its display is `HIDE`. A `go_testwriter` question has no rules case, because a violation stops the run before the first variant.
- `testcode` in a `go_program` question is one or more Go statements, such as `fmt.Println(dropBrand("gopher"), dropLetters("gopher"))`. Those statements may use `fmt` and the learner's identifiers, and nothing else.
- `testcode` in a `go_testwriter` question is a one-word label such as `correct` or `mutant2`. The `extra` field of that case holds one implementation variant, a whole `package main` file carrying the function under test. The first case is the correct implementation, expected `PASS`. Every later case is a mutant with one clause of the contract broken, expected `FAIL`.
- Mark the first two graded cases `useasexample="1"` with display `SHOW`, and hide the rest.

Escape `<`, `>`, and `&` inside `testcode` and `expected`. Ordinary Go uses all three.

### How expected values are produced

Run the code and paste what it printed. Never predict a value. Go's own `fmt` formatting decides every character.

- `fmt.Println` puts one space between operands and appends a newline.
- A struct prints as `{Grace Hopper 4}` with no field names.
- A slice of strings prints as `[bolts nuts]` with no quotes.
- A float prints in Go's shortest representation, so `8.166666666666666` rather than a rounded form.
- An error prints as the text of its `Error` method.

`fmt` prints a whole map with the keys sorted, so `map[bar-x:0]` is stable across runs. Map iteration order is unspecified and the runtime randomises it. A test that ranges a map and prints as it goes is a broken test. A test that builds map output by hand must sort the keys first.

Concurrency output has to be deterministic by design. Use a WaitGroup, a channel, or results collected and sorted before printing.

Keep angle brackets out of `expected`. Moodle reads them as HTML, and on import it collapses the newline between two such sequences on adjacent lines. The question then rejects output that is correct.

### The checks before import

Run these from the repository root before you hand the file over.

```
python3 tools/simulate-grader-go.py courses/go/topic-NN.xml
python3 tools/check-angle-brackets.py courses/go/topic-NN.xml
python3 -c "import xml.etree.ElementTree as ET; ET.parse('courses/go/topic-NN.xml')"
```

`simulate-grader-go.py` runs every test case against the sample answer and applies the rule checks. It reads those checks out of the prototype XML, and it also enforces the production idiom. Every sample answer must be gofmt-clean and pass `go vet`. A sample answer that breaks its own Banned line fails with `sample answer fails its own rules`. The simulator usage is `python3 tools/simulate-grader-go.py [--go /path/to/go] courses/go/topic-NN.xml`, and it runs the `go` found on PATH unless `--go` points elsewhere. Grading in the deployed course runs Go inside the Jobe container only; the course requires no Go install on the host.

`check-prose.py` enforces the course's sentence caps, but it is not yet portable: it hardcodes a path to a personal skill installation and does not run as shipped, and the decision on restoring the prose gate is pending. Until then, apply the sentence caps by hand on every edit to the question text.

### Layout

The seven zones and the two folds are fixed, and the block HTML for each one sits in the "Question layout" section of `courses/go/TOPICS.md`. Copy the markup from there.

### Pitfalls found while authoring

Four problems recurred across the 26 topic files.

**A visible test can act as an oracle.** A learner reads the expected value of a `SHOW` case and works backwards to the answer. Every visible case must print the same text under the careless implementation and under the correct one. The discriminating inputs belong in hidden cases. Run both implementations side by side and compare, rather than reasoning about which cases diverge. At WAT 09.2 that comparison found a second visible case the review had missed, and both cases moved to `newWarehouse(0)`. WAT 05.1 and WAT 22.1 moved their discriminating inputs the same way. A visible case must also avoid calling a banned token. WAT 11.2 rewrote its second example for that reason.

**A clean simulator run does not prove a rule is enforced.** Swap each cheat into `answer` and run the simulator against the real test cases. A live ban reports `banned token present: for`, and a live requirement reports `required token missing: range`. At WAT 06.3 the `Required: strings.Builder` clause alone let a mixed answer through. Running that answer added `Sprintf` to the ban. At WAT 17.3 the filed fix did not close its own cheat, because an empty `settle` still simulated clean. WAT 20.1 ran seven wrong solutions and recorded what the simulator printed.

**A ban matches on word boundaries over stripped source.** Identifier and keyword bans run after comments and string literals are removed. A comment therefore cannot match a banned token, and it cannot satisfy a required one. A ban on part of a longer identifier never matches. `Banned: Impl` was inert against `StoreImpl` at WAT 13.4, so that question bans both names. A ban also reaches every use in the file rather than the one you meant. `Banned: +` at WAT 06.3 forbids `++` as well, and `Banned: ==` at WAT 15.2 forbids the length guard. The simulator catches this against your own sample answer. It does not catch a correct learner answer written a different way. Check by hand that an idiomatic solution still exists once the wider ban is in force. Digits, quote characters, and `%` verbs match on a view that keeps string literals. A string literal can therefore satisfy the `Required: %T` at WAT 06.1. A required token the starter code already carries enforces nothing, as `Required: chan` did at WAT 24.1.

**Test code cannot import a package.** The generated harness imports `fmt` and `os`, so a test case reaches the learner's identifiers and `fmt` and nothing more. At WAT 14.3 the sentinel-identity check could not call `errors.Is`, so it runs through a `verdict` function the learner writes. At WAT 15.4 no behavioural test for wrapping was possible, and the Banned line carries `Required: %w` instead. At WAT 22.2 the case passes a bare function literal assignable to `iter.Seq[int]`, so the harness needs no `iter` import. Design each deliverable so the learner's own identifiers can express the check.
