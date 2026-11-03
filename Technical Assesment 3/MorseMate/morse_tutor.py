"""MorseMate: a small case-based Intelligent Tutoring System.

Run: python morse_tutor.py
Demo: python morse_tutor.py --demo
Only Python's standard library is needed.
"""

import argparse
import json
from pathlib import Path


MORSE = {
    "E": ".", "T": "-", "I": "..", "M": "--",
    "A": ".-", "N": "-.", "S": "...", "O": "---",
}
WEIGHTS = {"error_type": 60, "letter": 25, "confidence": 15}
STRATEGIES = {
    "reversed": "read_order",
    "missing_symbol": "count_symbols",
    "extra_symbol": "count_symbols",
    "wrong_symbols": "compare_symbols",
    "correct": "reinforce",
}
CASE_FILE = Path(__file__).with_name("case_base.json")


def diagnose(letter, answer):
    """Identify the student's mistake using the known correct pattern."""
    correct = MORSE[letter]
    if answer == correct:
        return "correct"
    if answer == correct[::-1]:
        return "reversed"
    if len(answer) < len(correct):
        return "missing_symbol"
    if len(answer) > len(correct):
        return "extra_symbol"
    return "wrong_symbols"


def similarity(new_problem, past_problem):
    """Matching attributes earn points; the maximum score is 100."""
    return sum(
        weight for feature, weight in WEIGHTS.items()
        if new_problem[feature] == past_problem[feature]
    )


def adapt_solution(problem, retrieved):
    """Reuse a teaching strategy, then tailor it to this student's answer."""
    letter = problem["letter"]
    answer = problem["answer"]
    correct = MORSE[letter]
    error = problem["error_type"]
    strategy = retrieved["solution"]["strategy"]

    # A weak match must not cause the tutor to teach the wrong kind of fix.
    if error != retrieved["problem"]["error_type"]:
        strategy = STRATEGIES[error]

    feedback = [f"Your answer: '{answer}'. Correct Morse code for {letter}: '{correct}'."]
    if strategy == "read_order":
        sounds = " then ".join("dot" if mark == "." else "dash" for mark in correct)
        feedback.append(f"You reversed the order. Read left to right: {sounds}.")
        practice = f"Write {letter} ({correct}) three times, keeping the same order."
    elif strategy == "count_symbols":
        difference = abs(len(correct) - len(answer))
        description = "missing" if error == "missing_symbol" else "extra"
        feedback.append(
            f"Your answer has {difference} {description} symbol(s). "
            f"{letter} needs {len(correct)} symbol(s); compare the dots and dashes too."
        )
        practice = f"Count each mark in {correct}, then write {letter} again."
    elif strategy == "compare_symbols":
        feedback.append("The number of symbols is right, but a dot or dash is incorrect.")
        practice = f"Compare {answer} with {correct} one position at a time, then retry."
    else:
        feedback.append("Correct! You recognized both the symbols and their order.")
        practice = f"Cover the answer and write {letter} ({correct}) again from memory."

    if problem["confidence"] == "low":
        feedback.append("A dot (.) is short; a dash (-) is long. Say each mark slowly.")
    elif problem["confidence"] == "medium":
        feedback.append("Say the pattern aloud, then try once without looking.")
    else:
        feedback.append("Challenge yourself to repeat the pattern without a reference.")

    return {"strategy": strategy, "feedback": " ".join(feedback), "practice": practice}


def tutor(letter, answer, confidence, case_file=CASE_FILE):
    """Retrieve, adapt and retain one attempt, printing the required evidence."""
    with case_file.open(encoding="utf-8") as source:
        cases = json.load(source)
    if not isinstance(cases, list) or not cases:
        raise ValueError("The case base must contain at least one past case.")

    problem = {
        "letter": letter, "answer": answer,
        "error_type": diagnose(letter, answer), "confidence": confidence,
    }
    print(f"\nStored cases before this attempt: {len(cases)}")
    print(f"New problem: letter={letter}, answer={answer}, confidence={confidence}")
    print(f"Diagnosis: {problem['error_type']}")

    # RETRIEVE: highest score first. Stable sorting keeps the earlier case on ties.
    ranked = sorted(cases, key=lambda case: similarity(problem, case["problem"]), reverse=True)
    print("\nSimilarity ranking (error 60 + letter 25 + confidence 15):")
    for rank, case in enumerate(ranked, start=1):
        past = case["problem"]
        score = similarity(problem, past)
        print(
            f"{rank}. C{case['id']:03d}: {score:3d}% | letter={past['letter']} "
            f"| error={past['error_type']} | confidence={past['confidence']}"
        )
    retrieved = ranked[0]
    print(f"\nMost relevant past case: C{retrieved['id']:03d}")
    print(f"Retrieved strategy: {retrieved['solution']['strategy']}")

    # ADAPT: use the retrieved teaching method with the new letter and confidence.
    solution = adapt_solution(problem, retrieved)
    print(f"\nPersonalized feedback:\n{solution['feedback']}")
    print(f"Practice: {solution['practice']}")

    # RETAIN: persist both the new problem and the adapted solution in JSON.
    new_case = {"id": max(case["id"] for case in cases) + 1,
                "problem": problem, "solution": solution}
    cases.append(new_case)
    temporary = case_file.with_suffix(".tmp")
    temporary.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")
    temporary.replace(case_file)
    print(f"\nNew case saved: C{new_case['id']:03d}")
    print(f"Updated case list ({len(cases)} cases):")
    for case in cases:
        past = case["problem"]
        print(
            f"C{case['id']:03d}: letter={past['letter']}, answer={past['answer']}, "
            f"error={past['error_type']}, confidence={past['confidence']}"
        )
    return new_case


def ask_problem():
    print("Practice letters: " + ", ".join(MORSE))
    while True:
        letter = input("Which letter would you like to practice? ").strip().upper()
        if letter in MORSE:
            break
        print("Please choose one of the listed letters.")
    while True:
        answer = "".join(input(f"Write the Morse code for {letter} (. and -): ").split())
        if answer and set(answer) <= {".", "-"}:
            break
        print("Use only dots (.) and dashes (-). The answer cannot be empty.")
    while True:
        confidence = input("Your confidence (low / medium / high): ").strip().lower()
        if confidence in {"low", "medium", "high"}:
            return letter, answer, confidence
        print("Please enter low, medium, or high.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Run a sample mistake and save it.")
    args = parser.parse_args()
    print("MORSEMATE - A Case-Based Morse Code Tutor")
    problem = ("N", ".-", "medium") if args.demo else ask_problem()
    try:
        tutor(*problem)
    except (OSError, ValueError) as error:
        raise SystemExit(f"Could not complete this attempt: {error}") from error


if __name__ == "__main__":
    main()
