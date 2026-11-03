# MorseMate: A Case-Based Morse Code Tutor

A simple Intelligent Tutoring System (ITS) for learning eight basic Morse-code
letters. Instead of a usual math or spelling tutor, this project helps a student
fix dot-and-dash mistakes. It uses case-based reasoning and only Python's standard
library. No installation of extra packages, API key, internet or database is needed.

## Run

1. Extract the ZIP, if using the packaged version.
2. Install Python 3 if it is not already available.
3. Open a terminal in this folder.
4. Run `python morse_tutor.py` (or `py morse_tutor.py` on Windows).
5. Choose a letter, enter your Morse-code answer, and choose your confidence.

To show the activity immediately, run:

```text
python morse_tutor.py --demo
```

The demo supplies `N`, `.-`, and `medium`. The correct code for N is `-.`,
so the tutor diagnoses a reversed order. Both the demo and interactive mode save
the attempt into `case_base.json`. Start with the supplied five-case JSON file to
reproduce `sample_output.txt` exactly; later runs include previously saved cases.
Repeated attempts are intentionally retained as separate cases.

## How the activity is completed

### 3. Define the case base

`case_base.json` begins with five fictional teaching cases. Each has an ID, a
`problem` dictionary (letter, answer, error type, confidence) and a `solution`
dictionary (teaching strategy, feedback, practice). These are illustrative cases,
not collected student records.

| Case | Letter | Student answer | Error | Confidence | Strategy |
| --- | --- | --- | --- | --- | --- |
| C001 | A | `-.` | Reversed order | Low | Read left to right |
| C002 | S | `..` | Missing symbol | Low | Count symbols |
| C003 | E | `-` | Wrong symbols | Medium | Compare symbols |
| C004 | N | `-..` | Extra symbol | Medium | Count symbols |
| C005 | O | `---` | Correct answer | High | Reinforce recall |

### 4. Assess similarity and retrieve

The program compares the new problem with every stored case:

```text
Similarity = 60 x same_error + 25 x same_letter + 15 x same_confidence
```

Each match is 1 if true and 0 otherwise, so scores range from 0% to 100%.
These are similarity points, not probabilities. Error type receives the largest
weight because a teaching method for the same mistake can transfer to a new
letter. The program prints the full ranking and retrieves the highest-scoring
case. Ties use the case that appears earlier in the JSON list.

For the supplied demo, C001 scores 60%, C004 scores 40%, C003 scores 15%,
and C002 and C005 score 0%. C001 is retrieved even though its letter is A:
both students reversed a pattern.

### 5. Adapt the solution

The tutor reuses C001's `read_order` strategy. It changes the example from
A (`.-`, dot then dash) to N (`-.`, dash then dot), provides a practice task for
N, and adjusts the advice to medium confidence. If a retrieved case has a different
error type, the tutor selects the teaching strategy appropriate to the new error.
It builds new feedback rather than copying an unrelated past answer.

Error diagnosis checks in this order: correct answer, reversed order, too few
symbols, too many symbols, and wrong symbols with the right length. An answer
with several mistakes is assigned one main category to keep the project simple.

### 6. Retain the new case

After feedback is generated, the program saves the new problem and adapted
solution to the JSON file, prints **New case saved**, and displays the updated
case list. The first demo grows the case base from five to six cases. On the next
run, that saved attempt is eligible for retrieval. This is learning through case
retention; the program does not train a machine-learning model or claim that the
student has mastered the letter.

## Files

- `morse_tutor.py`: readable Python implementation.
- `case_base.json`: five starting cases; updated when the program runs.
- `sample_output.txt`: actual output from a fresh five-case demonstration.
- `MorseMate_Activity_Report.pdf`: short explanation and demonstration results.
- `README.md`: run instructions and explanation in editable text.

## Reference chart

| Letter | E | T | I | M | A | N | S | O |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Morse code | `.` | `-` | `..` | `--` | `.-` | `-.` | `...` | `---` |

This deliberately small prototype supports only these eight letters. It uses
simple rules and self-reported confidence, and does not test timing, audio
recognition, or whether the recommended practice improved the learner's skill.
