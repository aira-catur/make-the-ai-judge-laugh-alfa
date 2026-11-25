#!/usr/bin/env python3
"""Make the AI Judge Laugh - one line about office life.

Strategy: draft many candidates across distinct comedic angles
(meta-AI, absurd, wordplay, observational), score them with a
deterministic heuristic that mimics the judge brief (truth to
office life, surprising turn, tightness, freshness), then write
the winner to /output/entry.txt with no trailing newline.
"""

import os

# --- Angle 1: meta-AI (the judge is a model; so is the threat) ---
META_AI = [
    "HR replaced me with an AI. It now attends my meetings, nods at "
    "my slides, and has also requested a transfer.",
    "My job was automated by an AI that now spends its days in "
    "meetings asking humans to circle back offline.",
    "The AI took my job, then immediately started updating its "
    "resume and complaining about the coffee machine.",
]

# --- Angle 2: absurd / surreal office truths ---
ABSURD = [
    "Our office printer has been 'low on toner' for three years. "
    "It is not broken; it is the only employee here who learned "
    "how to say no.",
    "The office fridge is where leftovers go to earn the seniority "
    "I will never get.",
    "Our fire drill took eleven minutes because everyone treated "
    "the alarm as a calendar invite they could decline.",
]

# --- Angle 3: wordplay ---
WORDPLAY = [
    "I put 'proficient in Excel' on my resume, which is Latin for "
    "'I cry inside a spreadsheet professionally.'",
    "My boss calls us a family, so I asked for an allowance and "
    "stopped coming to Sunday dinners. And Mondays.",
    "A 'quick sync' at our office is neither: it is a 47-minute "
    "ceremony where calendars mate and produce more meetings.",
]

# --- Angle 4: pure observational, tight and true ---
OBSERVATIONAL = [
    "My manager scheduled a meeting to discuss our meeting problem. "
    "It ran long, so we booked a follow-up.",
    "My out-of-office reply promises a response on my return. Bold "
    "of it to assume either of us is coming back.",
    "I asked for a raise; my boss gave me more responsibility, "
    "which is office for 'here is a heavier backpack, champ.'",
    "Every status update I write says 'almost done', a phrase that "
    "in office means 'I have not started, but with confidence.'",
]

ALL_CANDIDATES = META_AI + ABSURD + WORDPLAY + OBSERVATIONAL


# Concrete office props signal a true observation to the judge.
PROPS = ["printer", "fridge", "meeting", "calendar", "boss", "hr",
         "resume", "spreadsheet", "coffee", "toner", "alarm"]
# A second clause after one of these usually carries the twist.
TWIST_MARKERS = [";", ". ", ", which", ", so ", " because "]


def score(line: str) -> float:
    """Heuristic echo of the brief: truth + surprise + tight + fresh."""
    low = line.lower()
    s = 0.0
    s += 2.0 * sum(1 for p in PROPS if p in low)          # office truth
    s += 3.0 * sum(1 for m in TWIST_MARKERS if m in line)  # visible turn
    s += 4.0 if "ai" in low.split() or "an ai" in low else 0.0  # fresh angle
    s -= max(0, len(line) - 130) / 25.0                   # tightness tax
    s -= 1.5 * low.count("very")                          # filler tax
    return s


def pick_winner() -> str:
    ranked = sorted(ALL_CANDIDATES, key=lambda c: (-score(c), c))
    for c in ranked:
        print(f"{score(c):5.2f}  {c}")
    return ranked[0]


def main() -> None:
    winner = pick_winner()
    assert 1 <= len(winner) <= 200, len(winner)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(winner)  # no trailing newline, deterministic
    print("WROTE", path, len(winner), "chars")


if __name__ == "__main__":
    main()
