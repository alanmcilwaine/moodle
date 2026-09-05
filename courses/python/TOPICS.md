# Course spec: Python

This file is the contract for authoring the course. Read it with [AUTHORING.md](../../AUTHORING.md), which covers the XML format and the grading model.

## The learner

A professional developer, fluent in Java through Java 24, plain Java SE only. He knows OOP, generics, collections, streams, lambdas, exceptions, records, sealed types, and switch expressions. He had never written Python when the course began. He is moving onto a large safety-critical Python codebase.

Never teach him what a loop is. Teach him what Python does differently, and forbid the Java reflex.

## Topics and tiers

The course is a list of topics. Each topic gets three or four WATs at rising difficulty, because one exposure to a concept builds recognition and only repetition builds fluency.

| Tier | Name | Shape |
| --- | --- | --- |
| 1 | Introductory | One idea, one short function. Three to six lines. The learner should finish it in a few minutes. |
| 2 | Working | The same idea applied to a real shape, with an edge case that punishes a careless answer. |
| 3 | Hard | The idea combined with earlier topics. Multiple functions or a class. |
| 4 | Judgement | Optional fourth tier. Given AI-written Python that passes every test, say what is wrong with it and rewrite it. |

Name questions `WAT 07.2: Fun Name!` where 07 is the zero-padded topic number and 2 is the tier. Names sort into teaching order, and a new tier never renumbers anything else.

Fun, memorable names in the spirit of "Death to range(len)!" and "Boilerplate Bonfire!". No two names alike anywhere in the course.

## The topics

Existing questions move into a topic as its harder tiers. The file column says where the existing question lives today, before the restructure.

| # | Topic | Tiers | Existing anchors (old name, old file) |
| --- | --- | --- | --- |
| 01 | First lines: print, names, indentation | 3 | WAT 01, WAT 02 (module-01) |
| 02 | Loops: for, range, while | 3 | WAT 03 (module-01) |
| 03 | Functions: def, return, scope | 3 | WAT 04 (module-01) |
| 04 | Strings and f-strings | 3 | WAT 05 (module-02) |
| 05 | Numbers and arithmetic | 3 | WAT 06 (module-02) |
| 06 | Truth, None, and identity | 3 | WAT 07, WAT 08 (module-02) |
| 07 | Lists, indexing, slicing | 4 | WAT 09 (module-03) |
| 08 | Mutation, aliasing, copying | 3 | WAT 10, WAT 12 (module-03) |
| 09 | Tuples and unpacking | 3 | WAT 11 (module-03) |
| 10 | Dictionaries and sets | 4 | WAT 13, WAT 14, WAT 15, WAT 16 (module-04) |
| 11 | Exceptions and EAFP | 3 | none, all new |
| 12 | Type hints and validation | 3 | WAT 17, WAT 18 (module-05) |
| 13 | Comprehensions and iteration | 4 | WAT 19, WAT 20, WAT 21 (module-06) |
| 14 | Generators and laziness | 3 | WAT 22 (module-06) |
| 15 | Signatures and defaults | 3 | WAT 23, WAT 24 (module-07) |
| 16 | Closures and dispatch | 3 | WAT 25, WAT 26 (module-07) |
| 17 | Classes and instances | 3 | WAT 27, WAT 28 (module-08) |
| 18 | Inheritance and protocols | 3 | WAT 30 (module-08), WAT 36 (module-10) |
| 19 | Dunders, dataclasses, enums | 4 | WAT 29 (module-08) |
| 20 | Decorators | 3 | WAT 31, WAT 32 (module-09) |
| 21 | Context managers | 3 | WAT 33 (module-09) |
| 22 | Pattern matching | 3 | WAT 35 (module-10) |
| 23 | Modern generics and stdlib | 3 | WAT 37, WAT 38 (module-10) |
| 24 | Capstone | 1 | WAT 34 (module-09) |

Each topic becomes one file, `topic-NN.xml`, holding every tier for that topic. The old `module-NN.xml` files are deleted once every topic file exists.

## Per-topic build plan

"Move" means take the existing question whole. Keep its prose, code, tests and rules, and rename it to the new tier name. Then add the Predict block and the AI protocol block. "New" means author it.

Never use a concept the learner has not met. The topic order above is the teaching order.

| Tier | Action |
| --- | --- |
| 01.1 | Move WAT 01 Print or Perish! |
| 01.2 | Move WAT 02 The Curly Brace Famine! |
| 01.3 | New. Branch on several values and print a formatted block. No loops, no functions. |
| 02.1 | New. `for` over `range(n)` and over a list, against Java's two for loops. |
| 02.2 | Move WAT 03 Sheep, Ranged and Listed! |
| 02.3 | New. `while` with a sentinel, `break` against `continue`, and `for ... else`. |
| 03.1 | New. `def`, parameters, `return`, and calling. Against a Java method. |
| 03.2 | New. Returning several values, the implicit `None` return, and local scope. |
| 03.3 | Move WAT 04 Return of the Def! |
| 04.1 | New. String methods, indexing, and immutability. |
| 04.2 | New. f-strings against Java concatenation and `String.format`. |
| 04.3 | Move WAT 05 F-String Theory! |
| 05.1 | New. `int`, `float`, arithmetic, `//` and `%` against Java's `/`. |
| 05.2 | New. Rounding, `round` half to even, and the `math` module. |
| 05.3 | Move WAT 06 Division Is a Lie! |
| 06.1 | New. `bool`, `None`, and what counts as false. |
| 06.2 | Move WAT 07 Empty Is Not Nothing! |
| 06.3 | Move WAT 08 The Impostor Test! |
| 07.1 | New. List basics, indexing, and negative indexing against Java arrays. |
| 07.2 | New. Slicing with start, stop, and step. |
| 07.3 | Move WAT 09 Slice Twice, Cut Once! |
| 07.4 | New, tier 4. AI code that indexes with `range(len(...))`. Replace it. |
| 08.1 | New. Mutating methods, and `sort` against `sorted`. |
| 08.2 | Move WAT 10 Mutants Assemble! |
| 08.3 | Move WAT 12 Attack of the Clones! |
| 09.1 | New. Tuples, immutability, and tuples against a Java array. |
| 09.2 | New. Unpacking, swapping, and returning several values. |
| 09.3 | Move WAT 11 Unpack Your Bags! |
| 10.1 | New. Dict literals, lookup, and iteration against `HashMap`. |
| 10.2 | Move WAT 13 KeyError Is Not Null! |
| 10.3 | Move WAT 14 Group Therapy! |
| 10.4 | Move WAT 15 The True 1.0 Impostor! |
| 10.5 | Move WAT 16 Set Phasers to Unique! Five tiers here, because dictionaries carry the most unlearning. |
| 11.1 | New. `try`, `except`, `else`, `finally`, and no checked exceptions. |
| 11.2 | New. EAFP against Java's look-before-you-leap, and catching narrowly. |
| 11.3 | New. Custom exception classes, `raise from`, and why a bare `except` is a defect. |
| 12.1 | Move WAT 17 Types Are Back! |
| 12.2 | New. Annotating collections, `str \| None`, and reading a checker's complaint. |
| 12.3 | Move WAT 18 The Lie Detector! |
| 13.1 | New. A first list comprehension against a Java stream. |
| 13.2 | Move WAT 19 One Line to Rule Them All! |
| 13.3 | Move WAT 20 Invert the Universe! |
| 13.4 | Move WAT 21 Death to range(len)! |
| 14.1 | New. `yield`, and a generator against a Java `Iterator`. |
| 14.2 | New. Laziness, generator expressions, and one-shot exhaustion. |
| 14.3 | Move WAT 22 The Stream That Ran Dry! |
| 15.1 | New. Default arguments and keyword arguments, which Java has not got. |
| 15.2 | Move WAT 23 The Default That Remembers! |
| 15.3 | Move WAT 24 No Positional Smuggling! |
| 16.1 | New. Functions as values, and passing one as an argument. |
| 16.2 | Move WAT 25 The Switchless Switchboard! |
| 16.3 | Move WAT 26 Closure Encounters! |
| 17.1 | New. `class`, `__init__`, `self`, and instances against a Java class. |
| 17.2 | Move WAT 27 Self Service! |
| 17.3 | Move WAT 28 Getters Get Gone! |
| 18.1 | New. Subclassing, `super`, and method resolution. |
| 18.2 | Move WAT 30 Fill in the Abstract! |
| 18.3 | Move WAT 36 The Override That Wasn't! |
| 19.1 | New. `__str__` and `__repr__` against `toString`. |
| 19.2 | New. `__eq__`, `__hash__`, and `NotImplemented`. |
| 19.3 | Move WAT 29 Boilerplate Bonfire! |
| 19.4 | New, tier 4. AI code with a getter and setter pair and a hand-written `equals`. Replace it. |
| 20.1 | New. A first decorator, and `@` as shorthand for reassignment. |
| 20.2 | Move WAT 31 At Sign Alchemy! |
| 20.3 | Move WAT 32 Matryoshka! |
| 21.1 | New. `with`, against try-with-resources. |
| 21.2 | New. Writing `__enter__` and `__exit__`. |
| 21.3 | Move WAT 33 With Great Power! |
| 22.1 | New. `match` on literals and the wildcard, against a Java switch expression. |
| 22.2 | New. Class patterns that destructure, against Java record deconstruction. |
| 22.3 | Move WAT 35 Death to isinstance! |
| 23.1 | New. The walrus operator and `pathlib` pure paths. |
| 23.2 | Move WAT 37 TypeVar Is Dead! |
| 23.3 | Move WAT 38 The Walrus and the Path! |
| 24.1 | Move WAT 34 Fail Safe or Fail Loud! |

## Question layout

Every question uses the same five zones in the same order, so the reader learns once where to look. Teaching and task are never interleaved.

```
Goal panel          one sentence, what you will write
How this works      the teaching, in a fold the reader can collapse
Your task           the exact deliverable, in a green panel
Rules               red panel
Before you click    grey panel
AI protocol         blue panel
```

Collapse the teaching and five things remain: the goal, the task, the rules, the predict prompt, and the AI protocol. That is the test. A reader who has folded the teaching must still be able to answer the question.

The teaching folds away. Moodle renders question text without running the HTML purifier over it, so `details` and `summary` reach the browser intact. The reader can collapse the teaching once the concept has landed. This was confirmed by rendering a live question, not assumed.

**Goal panel.** The first thing in the question text. One sentence naming what the learner writes, with no teaching in it.

```html
<div style="border-left:4px solid #2c3e50; padding:0.5em 1em; margin-bottom:1em; background:#eef1f4;"><b>Goal</b><p>ONE SENTENCE HERE.</p></div>
```

**Teaching.** Everything that explains the concept goes inside one fold, and nothing else does. It opens by default and the reader collapses it once the concept has landed.

```html
<details open><summary style="cursor:pointer; font-weight:bold; font-size:1.1em; padding:0.3em 0;">How this works in Python</summary>
TEACHING GOES HERE.
</details>
```

Use `h4` for sections inside the fold. Keep the Java contrast, the worked examples, and the diagrams here. Nothing the learner needs while writing the answer may live inside the fold, because a folded question must still be answerable.

**Your task.** The complete deliverable, and nothing else. No teaching, no background, no worked examples. One list item per function or class the learner writes. Close it with the pass condition.

```html
<div style="border-left:4px solid #5cb85c; padding:0.5em 1em; margin-top:1em; background:#f2f9f2;"><b>Your task</b><ul><li>ONE ITEM PER THING TO WRITE.</li></ul><p>You pass when the printed output matches the expected text exactly.</p></div>
```

A reader who folds away everything except the Goal panel and the Your task panel must still know exactly what to write. Test each question against that bar.

## Every question carries three blocks

Put all three at the end of the question text, in this order.

**Rules.** One to four playful constraints that forbid the Java habit and force the Python idiom. Write them as short commands. Enforce a rule with a hidden test where the check is reliable, and never write a check that fires on the correct answer.

```html
<div style="border-left:4px solid #d9534f; padding:0.5em 1em; margin-top:1em; background:#fdf3f2;"><b>Rules</b><ul><li>One rule per list item.</li></ul></div>
```

**Predict, then run.** One line, identical everywhere. It exists because the study behind this course found that moving too fast through a problem produces a false sense of progress.

```html
<div style="border-left:4px solid #6c757d; padding:0.5em 1em; margin-top:1em; background:#f6f6f6;"><b>Before you click Check</b><p>Write down what you expect each test to print. Then run it. A surprise means your model of Python is wrong, and that is the part worth learning.</p></div>
```

**AI protocol.** The kind of question decides the text, not the tier number. A hard question takes the tier 3 text whether it sits at tier 3, 4, or 5. Use the tier 4 text only on a question that shows AI-written code for the learner to judge. Copy the matching text exactly.

```html
<div style="border-left:4px solid #0275d8; padding:0.5em 1em; margin-top:1em; background:#f0f7fd;"><b>AI protocol</b><p>TIER TEXT HERE</p></div>
```

- Tier 1: `No AI. Type every character yourself. This tier builds the muscle, and a tool that types it for you skips the exercise.`
- Tier 2: `AI for explanation only. Ask it what an error means or why one form is more idiomatic. Do not let it write your answer.`
- Tier 3: `AI allowed, on three conditions. Write your plan before you open it. Read every suggestion and reject the ones you did not plan. Type accepted code out yourself rather than pressing Tab.`
- Tier 4: `AI allowed for discussion. The code below came from an AI and it passes every test. Your job is to judge it, so do not ask an AI whether it is good.`

## Tier 4, judging AI output

A tier 4 question shows Python that passes its tests and is still wrong for a reader. Pick the flaw from this list.

- A `for` loop with `append` where a comprehension belongs.
- `range(len(...))` indexing instead of `enumerate`.
- A getter and setter pair instead of a property.
- An `isinstance` chain instead of `match`.
- A mutable default argument.
- String concatenation instead of an f-string.

The learner writes the idiomatic replacement. The tests check that the behaviour still holds and that the Java shape is gone. Say plainly in the prose that passing tests is not the same as correct code. Add that he will be reviewing AI-written Python at work.

Place one tier 4 question in each major topic area rather than in every topic.

## Annotations

Topics 1 to 12 stay unannotated. Their job is to break the habit of declaring a type before every name.

Topic 13 teaches type hints. From topic 14 onward every signature the learner writes carries annotations, because that is what production Python looks like.

Modern syntax only. Write `list[int]`, never `typing.List[int]`. Write `str | None`, never `Optional[str]`. Import `Iterator`, `Iterable`, and `Callable` from `collections.abc`. Give `-> None` to anything that returns nothing, including `__init__`.

## Prose

Follow the technical-writing skill. Open every question from the Java side, name the Java construct first, and show it in a `pre` block when that helps. Explain every Python term on first use.

British English. No em dashes, no semicolons, no colons used as mid-sentence connectors. Never "simply", "just", "easy", "powerful", "leverage", "utilise", or "note that".

Reading the standard is not enough. Every question you write or move goes through the checker:

```
python3 tools/check-prose.py courses/python/topic-NN.xml
```

The checker is not yet portable: `tools/check-prose.py` hardcodes a path to a personal skill installation and does not run as shipped, and the decision on restoring it is pending. Until it runs, apply the rules above by hand. When it runs, it must report every question clean. The checker strips the code samples and the three standard blocks, so it reads only the teaching prose. It also misreports line numbers, so locate each finding yourself.

Fix a finding by rewriting the sentence, not by trimming words until the count passes. A 26-word sentence usually carries two thoughts, so the fix is a full stop in the middle.
