#!/usr/bin/env python3
"""
Code P - University-level practical exercises
Run from trainer option 9, or: python3 exercises.py
"""

import os


def clear():
    os.system("clear" if os.name != "nt" else "cls")


EXERCISES = [
    {
        "id": "EX1",
        "title": "Early return in nested loop",
        "level": "Beginner",
        "broken": '''
def flatten(bags):
    flat = []
    for bag in bags:
        for x in bag:
            flat.append(x)
        return flat

print(flatten([[1, 2], [3]]))
''',
        "symptom": "Output is [1, 2] instead of [1, 2, 3]",
        "tasks": [
            "Find the bug",
            "Explain why only the first bag is processed",
            "Write the minimal fix",
        ],
        "answer": "return is inside the outer loop, so function exits after first bag. Dedent return to function level.",
    },
    {
        "id": "EX2",
        "title": "append vs extend on strings/flags",
        "level": "Intermediate",
        "broken": '''
def flatten_pool(items):
    out = []
    for x in items:
        out.extend(list(x))
    return out

print(flatten_pool(["AB", "CD"]))
''',
        "symptom": "Gets ['A','B','C','D'] instead of whole tokens",
        "tasks": [
            "Why does list(x) split tokens?",
            "When is extend correct?",
            "Write a safe flatten that keeps whole strings",
        ],
        "answer": "list(string) yields characters. extend expands iterables. Use append for strings and extend only for lists.",
    },
    {
        "id": "EX3",
        "title": "Hardcoded salt + debug leak",
        "level": "Intermediate-Advanced",
        "broken": '''
import hashlib

def make_system_salt(material: bytes) -> str:
    salt = b"advanced_path_generator_v200"
    out = hashlib.pbkdf2_hmac("sha3_512", material, salt, 600000)
    print("salt=", salt)
    return out.hex()
''',
        "symptom": "Same salt pattern every time; secret may leak in logs",
        "tasks": [
            "Name two security problems",
            "Patch with minimal changes",
            "State what must never be shown",
        ],
        "answer": "Hardcoded salt and printed secret. Use secrets.token_bytes(32), remove print. Never show internal salt/intermediates.",
    },
    {
        "id": "EX4",
        "title": "DictReader without header",
        "level": "Beginner",
        "broken": '''
# knowledge.csv content (no header):
# decision,Why use functions?,To organize code,Code Decision

import csv
with open("knowledge.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(rows[0])
''',
        "symptom": "Keys become first-row values; meaning becomes wrong",
        "tasks": [
            "What does DictReader expect on line 1?",
            "What breaks without header?",
            "Write the correct header line",
        ],
        "answer": "DictReader expects header names. Without them first data row becomes keys. Header must be type,term,meaning,category.",
    },
    {
        "id": "EX5",
        "title": "JSON progress KeyError",
        "level": "Beginner-Intermediate",
        "broken": '''
import json, os

def load_progress():
    if os.path.exists("progress.json"):
        with open("progress.json") as f:
            return json.load(f)
    return {}

progress = load_progress()
progress["wrong"].append({"term": "x"})
''',
        "symptom": "KeyError: 'wrong' on first run",
        "tasks": [
            "Why KeyError happens",
            "Provide a safe default structure",
            "Rewrite load_progress safely",
        ],
        "answer": "Empty default {} has no 'wrong'. Default should be {'wrong': [], 'next_review': {}}.",
    },
    {
        "id": "EX6",
        "title": "Off-by-one hardened levels",
        "level": "Intermediate",
        "broken": '''
switch_point = 5
parts = []
for i in range(8):
    if i <= switch_point:
        parts.append(f"{i}'")
    else:
        parts.append(str(i))
print(parts)
''',
        "symptom": "One extra hardened index compared to intended i < switch_point policy",
        "tasks": [
            "What is the boundary bug?",
            "Which indexes are hardened now?",
            "Fix the comparison",
        ],
        "answer": "i <= switch_point hardens indexes 0..5. Use i < switch_point to harden 0..4.",
    },
    {
        "id": "EX7",
        "title": "Noise before digits",
        "level": "Intermediate",
        "broken": '''
number = "42"
noise = "🔥"
piece = noise + number + "'"
print(piece)
''',
        "symptom": "Path segment may be rejected or misparsed by wallets",
        "tasks": [
            "Why is noise-before-digits dangerous?",
            "Rewrite segment order correctly",
            "State the placement rule",
        ],
        "answer": "Wallets expect index digits first. Correct order: number, optional ', then noise.",
    },
    {
        "id": "EX8",
        "title": "Shadowed loop variable",
        "level": "Intermediate",
        "broken": '''
pools = [["a", "b"], ["c"]]
flat = []
for emoji in pools:
    for emoji in emoji:
        flat.append(emoji)
print(flat)
''',
        "symptom": "Code may work here but is fragile and hard to reason about",
        "tasks": [
            "What is variable shadowing here?",
            "Rename variables cleanly",
            "Explain maintainability risk",
        ],
        "answer": "Inner emoji overwrites outer emoji name. Use group/item names to avoid confusion and future bugs.",
    },
    {
        "id": "EX9",
        "title": "Missing try-except on int(input)",
        "level": "Beginner",
        "broken": '''
num = int(input("How many questions? "))
print("Got", num)
''',
        "symptom": "Typing 'ten' crashes with ValueError",
        "tasks": [
            "What exception occurs?",
            "Wrap with try-except",
            "Choose a safe default",
        ],
        "answer": "ValueError. Catch Exception/ValueError and fallback to a default like 10.",
    },
    {
        "id": "EX10",
        "title": "Risky direct commits on main",
        "level": "Process",
        "broken": '''
# Process anti-pattern
# 1. edit production code on main
# 2. commit experimental break
# 3. push immediately
''',
        "symptom": "Stable branch becomes unusable for everyone",
        "tasks": [
            "Why is this dangerous?",
            "Describe safer branch workflow",
            "When should main be updated?",
        ],
        "answer": "Main should stay stable. Use feature branch, test, then merge. Main updates only after verified work.",
    },
    {
        "id": "EX11",
        "title": "Secret committed then deleted",
        "level": "Security",
        "broken": '''
# Day 1: commit .env with real API key
# Day 2: delete .env and commit deletion
# Assume secret is gone forever
''',
        "symptom": "Key can still be recovered from git history",
        "tasks": [
            "Why deletion is not enough",
            "What must you do to the secret itself?",
            "What preventive control stops reoccurrence?",
        ],
        "answer": "History still contains the blob. Rotate/revoke secret. Add .env to .gitignore and use env vars.",
    },
    {
        "id": "EX12",
        "title": "Create .gitignore with cat heredoc",
        "level": "Linux",
        "broken": '''
# Incomplete attempt
echo .env > .gitignore
# missing other important entries and not using heredoc multi-line creation
''',
        "symptom": "Only one ignore rule; weak protection",
        "tasks": [
            "Write a cat << EOF command that creates .gitignore",
            "Include .env __pycache__/ and venv/",
            "Explain why heredoc helps",
        ],
        "answer": "cat > .gitignore << 'EOF' then lines then EOF. Heredoc writes multi-line files cleanly.",
    },
    {
        "id": "EX13",
        "title": "diff then patch workflow",
        "level": "Linux",
        "broken": '''
# Student edited file in place with no patch trail
# No diff was saved, so change cannot be reviewed/reapplied
''',
        "symptom": "No auditable repair history",
        "tasks": [
            "Write command to create unified patch",
            "Write command to inspect patch",
            "Write command to apply patch",
        ],
        "answer": "diff -u old.py new.py > fix.patch; cat fix.patch; patch < fix.patch",
    },
    {
        "id": "EX14",
        "title": "Heredoc piped directly to patch",
        "level": "Linux-Intermediate",
        "broken": '''
# Need emergency one-line fix but no patch file on disk
''',
        "symptom": "Student does not know inline patch pattern",
        "tasks": [
            "Write cat << 'PATCH' | patch pattern",
            "State one risk of blind applying",
            "State one benefit",
        ],
        "answer": "cat << 'PATCH' | patch ... PATCH. Benefit: fast. Risk: applying without review can damage files.",
    },
    {
        "id": "EX15",
        "title": "Combined recovery with cat/diff/patch",
        "level": "Linux-Advanced",
        "broken": '''
# config.py is broken
# backup exists as config.py.bak
# need reproducible repair trail
''',
        "symptom": "Ad-hoc edits with no recoverable trail",
        "tasks": [
            "List ordered steps using cp, edit, diff, cat, patch",
            "Explain why order matters",
        ],
        "answer": "Keep backup, edit copy, diff -u backup edited > fix.patch, cat fix.patch, patch < fix.patch. Order preserves rollback and audit.",
    },
    {
        "id": "EX16",
        "title": "Deep nested counting with early return",
        "level": "Intermediate",
        "broken": '''
def count_people(country):
    total = 0
    for state in country:
        for lga in state:
            for person in lga:
                total += 1
            return total
''',
        "symptom": "Counts only first LGA group",
        "tasks": [
            "Identify wrong indentation level of return",
            "Fix function",
            "Relate to flatten lessons",
        ],
        "answer": "return is too deep. Accumulate fully, return once. Same discipline as nested flatten loops.",
    },
    {
        "id": "EX17",
        "title": "Nested stall random choice",
        "level": "Intermediate",
        "broken": '''
import random
emoji_stall = [["🔥", "🚀"], ["🐍"]]
print(random.choice(emoji_stall))
''',
        "symptom": "Sometimes returns a whole group list not one emoji",
        "tasks": [
            "Why does this happen?",
            "Flatten correctly then choose",
            "Connect to generator noise pools",
        ],
        "answer": "choice selects one top-level element (a list). Flatten first, then choice on flat list.",
    },
    {
        "id": "EX18",
        "title": "Thin UI violated",
        "level": "Design",
        "broken": '''
# main.py
import hashlib, secrets

def main():
    salt = secrets.token_bytes(32)
    material = hashlib.pbkdf2_hmac("sha3_512", b"x", salt, 600000)
    path = "m/" + material.hex()
    print(path)
''',
        "symptom": "UI layer owns crypto; hard to test/reuse/audit",
        "tasks": [
            "Name the design principle violated",
            "Propose file split",
            "Say what main should do",
        ],
        "answer": "Separation of Concerns / thin UI. Move crypto to crypto.py and path build to generator.py. main should only coordinate I/O.",
    },
    {
        "id": "EX19",
        "title": "Predictable switch point fingerprint",
        "level": "Security",
        "broken": '''
for i in range(levels):
    if i < 200:
        piece = f"{idx}'"
    else:
        piece = idx
''',
        "symptom": "Every output shares same structural hardening pattern",
        "tasks": [
            "Why is this a fingerprint?",
            "Replace with random switch_point approach",
            "State attacker advantage against fixed structure",
        ],
        "answer": "Fixed rule is detectable. Use random switch_point in a range. Attackers can model structure more easily when fixed.",
    },
    {
        "id": "EX20",
        "title": "Overly loose answer checker",
        "level": "Logic",
        "broken": '''
def is_correct(user_answer, correct):
    user = user_answer.lower().strip()
    correct = correct.lower()
    return user in correct or correct in user
''',
        "symptom": "Very short or weak answers can pass",
        "tasks": [
            "Give one false-positive example",
            "Add a minimum-length guard",
            "Suggest one extra tightening rule",
        ],
        "answer": "Answer 'a' may pass inside many texts. Require len(user) >= 3 and stronger token overlap checks.",
    },
]


def run_exercises():
    while True:
        clear()
        print("=== Exercises-only mode ===")
        print("1. List all exercises")
        print("2. Practice one by ID (EX1..EX20)")
        print("3. Random exercise")
        print("0. Back")
        choice = input("\nChoose: ").strip()

        if choice == "0":
            return
        if choice == "1":
            clear()
            for ex in EXERCISES:
                print(f"{ex['id']} [{ex['level']}] {ex['title']}")
            input("\nPress Enter...")
            continue
        if choice == "2":
            ex_id = input("Enter ID (e.g. EX7): ").strip().upper()
            ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
            if not ex:
                print("Not found")
                input("Press Enter...")
                continue
            practice_one(ex)
            continue
        if choice == "3":
            import random
            practice_one(random.choice(EXERCISES))
            continue
        print("Invalid choice")
        input("Press Enter...")


def practice_one(ex):
    clear()
    print(f"{ex['id']} - {ex['title']} ({ex['level']})")
    print("\nBROKEN CODE:")
    print(ex["broken"])
    print("SYMPTOM:")
    print(ex["symptom"])
    print("\nTASKS:")
    for i, t in enumerate(ex["tasks"], 1):
        print(f"{i}. {t}")
    input("\nSolve first, then Press Enter to view model answer...")
    print("\nMODEL ANSWER:")
    print(ex["answer"])
    input("\nPress Enter...")


if __name__ == "__main__":
    run_exercises()