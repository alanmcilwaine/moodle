# Go question solvability audit

Audited against `a1c3c46` on 2026-09-04. This review considered every Goal,
starter, linked reading, visible example, hidden case, and reference answer. A
hidden case may vary the input, but it may not invent the rule.

The verdicts mean:

- **Contract** means the prompt states behaviour that cannot be inferred safely.
- **Generalisation** means visible cases establish the rule and hidden cases vary it.
- **Discovery** means finding the relevant Go rule or API is the intended puzzle.
- **Review** means fixed starter code states the behaviour while the learner rewrites it.

`Repaired` marks questions whose missing contract was restored by `a1c3c46`.
`Sound` marks questions that were already answerable without exposing their hidden
inputs.

| Question | Result | Verdict | Reason |
|---|---|---|---|
| 01.1 | Sound | Generalisation | Visible tickets establish exact spacing and newlines; hidden tickets only change visitor data. |
| 01.2 | Sound | Discovery | The fixed print line and compiler identify the unused-name problem; hidden zero stock changes no rule. |
| 01.3 | Repaired earlier | Contract | The three distance messages and the 10-mile boundary are now stated explicitly. |
| 02.1 | Sound | Generalisation | Visible boundary cases establish adult eligibility and strict majority; the zero-value reading explains blank registration. |
| 02.2 | Repaired | Contract | Crate size, tasting removal, delivery doubling, order, and scope were arbitrary business rules. |
| 02.3 | Repaired | Contract | Planet numbering, valid range, inner range, and between semantics needed an explicit contract. |
| 03.1 | Repaired | Contract | Refusal results and concession rounding were ticket-office policy, not Go semantics. |
| 03.2 | Repaired | Contract | Age and pace thresholds were arbitrary and the old swimwear story contradicted the answer. |
| 03.3 | Repaired | Contract | Ordering, bounds, and span operations could not be recovered from the function names alone. |
| 04.1 | Sound | Discovery | The Goal distinguishes a prefix from a cutset; hidden strings expose the documented difference. |
| 04.2 | Sound | Discovery | Three behavioural clues and three package indexes deliberately make API discovery the exercise. |
| 04.3 | Sound | Discovery | The Goal specifies quoting and ties-to-even; linked package search is the intended puzzle. |
| 05.1 | Repaired | Contract | Trip rounding, inclusive departures, and port-side numbering needed to be stated. |
| 05.2 | Repaired | Contract | Force thresholds, descriptions, and exact advice are local harbour rules. |
| 05.3 | Repaired | Contract | Search order, stopping rule, consolation count, and doubling limit were arbitrary. |
| 06.1 | Sound | Discovery | Visible cards establish the layout while fmt documentation determines quoting, type, and numeric formatting. |
| 06.2 | Sound | Discovery | The engraving story asks for letters; visible Unicode names and linked rune material define the unit. |
| 06.3 | Repaired | Contract | Separator placement and the deliberate rune-versus-byte distinction needed to be explicit. |
| 07.1 | Sound | Generalisation | The visible booking establishes fields and the zero room; hidden data only generalises it. |
| 07.2 | Sound | Discovery | Visible structurally similar tickets establish whole-struct equality; zero-value comparison follows the linked Go rule. |
| 07.3 | Repaired | Contract | Constructor validation and normalisation rules are application policy. |
| 08.1 | Repaired | Contract | Which value is copied, stamped, and returned was essential to the pointer lesson. |
| 08.2 | Repaired | Contract | Minute carry, day wrap, and swapping clock values rather than pointers needed to be stated. |
| 08.3 | Sound | Generalisation | Visible moves, trips, home swaps, and shared docks establish the operations; hidden cases recombine them. |
| 09.1 | Sound | Generalisation | Visible logging establishes append and total semantics; nil and zero scores are ordinary generalisation. |
| 09.2 | Sound | Discovery | The task promises enough capacity without prescribing a growth factor; hidden checks do not require doubling. |
| 09.3 | Repaired | Contract | Reveal deliberately extends beyond length into capacity, which is not implied by dealing cards. |
| 10.1 | Sound | Discovery | Page views, redaction, and trim are demonstrated visibly; hidden cases test the same backing-array rule. |
| 10.2 | Sound | Discovery | Preventing append bleed is the stated outcome; full-slice capacity is the linked mechanism to discover. |
| 10.3 | Sound | Generalisation | Fixed-pad writes, newest-first pinning, and independent snapshots are visible before hidden combinations. |
| 10.4 | Sound | Review | Fixed starter comments fully specify behaviour; the learner judges and replaces loop form. |
| 11.1 | Sound | Generalisation | The Goal and visible board establish water at zero plus normal map operations; hidden deletion adds no rule. |
| 11.2 | Repaired | Contract | Missing versus registered-at-zero and non-destructive registration are application rules. |
| 11.3 | Sound | Discovery | Visible output establishes ascending order and line format; hidden maps test determinism and nil input. |
| 12.1 | Sound | Generalisation | Four-digit clock output and visible examples establish conversion; hidden receiver forms change no behaviour. |
| 12.2 | Repaired | Contract | Copy-return stamping and the three-visit threshold were clinic policy. |
| 12.3 | Repaired | Contract | Mutation, total, reading format, and missing-meter nil behaviour needed to be explicit. |
| 13.1 | Repaired | Contract | Nil entries, list order, and the two sounds were not implied by the interface lesson. |
| 13.2 | Repaired | Contract | Empty mean and `%v` log formatting were arbitrary presentation choices. |
| 13.3 | Sound | Generalisation | Visible seats establish names and Player layout; hidden seats test fmt verb behaviour and the documented fallback. |
| 13.4 | Repaired | Review | The required one-method consumer interface and preserved concrete API now define the refactor. |
| 14.1 | Repaired | Contract | First-error stopping, zero total, unchanged error, and empty-week behaviour needed stating. |
| 14.2 | Repaired | Contract | Validation order, thresholds, messages, and label format are parcel-counter policy. |
| 14.3 | Repaired | Contract | Gate check order, capacity mutation, wrapped matching, and fallback verdict needed stating. |
| 15.1 | Sound | Discovery | Visible wrapping establishes message shape; hidden depth and false text matches test errors.Is semantics. |
| 15.2 | Sound | Discovery | Visible chains establish relay order and formatting; misleading station names intentionally test identity rather than text. |
| 15.3 | Sound | Discovery | The empty-envelope metaphor and visible typed-nil case provide the intended interface puzzle. |
| 15.4 | Repaired | Review | Each new error result and exact wrapping layer now has a visible contract. |
| 16.1 | Repaired | Contract | Table capacity and minimum players were missing, and the former story contradicted the implementation. |
| 16.2 | Repaired | Contract | Pen boundaries and the absent-prediction case were arbitrary race policy. |
| 16.3 | Sound | Discovery | The linked strconv.Atoi contract is deliberately the specification; mutants test whether the learner read it. |
| 17.1 | Repaired | Contract | Entry, exit, breach order, indexing, and error text were sentry policy. |
| 17.2 | Repaired | Contract | Parade return timing, pre-existing floats, stall handling, and dispatch order needed stating. |
| 17.3 | Repaired | Contract | Session failure text and quote behaviour were application rules outside panic and recover semantics. |
| 18.1 | Sound | Generalisation | Visible station sequences establish nil steps as switched off; hidden sequences only vary placement. |
| 18.2 | Sound | Generalisation | Score-descending and name-ascending order is explicit; hidden larger boards test comparator consistency. |
| 18.3 | Sound | Generalisation | Visible interleaving establishes independent counters, starting value, and gate capacity. |
| 19.1 | Sound | Discovery | Embedded engine promotion and load are specified; hidden interface assignments test the linked composition rule. |
| 19.2 | Sound | Discovery | The locked receiver explains why embedding cannot override its internal call; visible night output defines the replacement. |
| 19.3 | Sound | Discovery | Exact byte counting is stated and visible; hidden Unicode and EOF reads test io.Reader semantics. |
| 20.1 | Repaired | Contract | Nil, unknown, decimal, and failed coin-conversion results needed explicit values. |
| 20.2 | Repaired | Contract | The copied marker is intentionally accepted and the unmarked sack rejected; the old story contradicted this. |
| 20.3 | Repaired | Contract | Pointer/value parity and wrapped sentinel reachability were required beyond visible fare values. |
| 21.1 | Sound | Discovery | Visible types and generic constraints define supported marks; negatives and empty slices test zero-value correctness. |
| 21.2 | Sound | Discovery | Source priority and empty zero values are explicit; whitespace and negatives test cmp.Or semantics without inventing policy. |
| 21.3 | Sound | Generalisation | Visible mapping and labels establish behaviour; hidden element types and Unicode lengths generalise it. |
| 21.4 | Repaired | Contract | The permitted load types had to be named before a learner could write the type set. |
| 22.1 | Sound | Generalisation | Visible cases establish strict sugar limits and slug formatting; hidden cases test mutation and nil range behaviour. |
| 22.2 | Repaired | Contract | Countdown direction, endpoint, floor result, empty result, and early stop needed stating. |
| 22.3 | Repaired | Contract | Sort order, duplicate totals, threshold meaning, iterator order, and early stop needed stating. |
| 22.4 | Sound | Review | Fixed comments specify both functions; tests preserve behaviour while the learner removes needless copies. |
| 23.1 | Sound | Generalisation | The race rate and duration naturally define distance; visible and hidden cases vary crews and zero rates. |
| 23.2 | Sound | Generalisation | Visible entries establish exact line format and retained input order; hidden duplicates test index capture. |
| 23.3 | Sound | Generalisation | Visible sectors establish minutes and sorted report format; hidden empty and larger sets vary workload. |
| 24.1 | Sound | Discovery | One-at-a-time unbuffered transfer is explicit; hidden zero consumption tests channel blocking without a new result rule. |
| 24.2 | Sound | Discovery | Closing after the final loaf is explicit; hidden direct receives test the documented closed-channel values. |
| 24.3 | Sound | Discovery | Non-blocking poll and done-driven sitting are stated; hidden closed and pre-cancelled channels test select semantics. |
| 25.1 | Sound | Discovery | Concurrent addition and no lost bins define the invariant; hidden repetition tests the mutex rather than a new total rule. |
| 25.2 | Sound | Discovery | Recall and expiry are explicit; visible states and Context documentation define the three words. |
| 25.3 | Repaired | Contract | Closed-radio success, cancellation error identity, partial results, forwarding, and pre-cancel behaviour needed stating. |
| 26.1 | Repaired | Contract | Display-time defaults, exact layout, empty address, and non-positive timeout output were application policy. |
| 26.2 | Repaired | Contract | Minimum seats, validation order, contextual messages, and Manifest wrapping were application policy. |

## Conclusion

All 82 questions are answerable at this revision. The 37 questions changed in
`a1c3c46`, plus the earlier 01.3 repair, needed explicit contracts. The other 44
retain intentional discovery or generalisation. Their hidden inputs do not add
new application rules.

The audit does not require hidden inputs to be disclosed. It requires the rule
that determines their result to be available. That keeps the useful puzzle while
removing guesswork.
