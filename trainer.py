#!/usr/bin/env python3
"""
Chat Knowledge Trainer
Active recall tool covering the entire conversation + code logic
"""

import csv
import random
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

DATA_FILE = "progress.json"
RECENT_FILE = "recent.json"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def load_knowledge():
    knowledge = []
    try:
        with open("knowledge.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                knowledge.append(row)
    except FileNotFoundError:
        print("ERROR: knowledge.csv not found!")
        exit()
    return knowledge

def load_json(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename) as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def is_correct(user_answer, correct):
    user = user_answer.strip().lower()
    correct = correct.lower()
    if len(user) < 3:
        return False
    return user in correct or correct in user or any(word in user for word in correct.split() if len(word) > 4)

def get_questions(knowledge, num):
    recent = load_json(RECENT_FILE, [])
    available = [k for k in knowledge if k["term"] not in recent]
    if len(available) < num:
        available = knowledge[:]
    questions = random.sample(available, min(num, len(available)))
    new_recent = [q["term"] for q in questions] + recent
    save_json(RECENT_FILE, new_recent[:60])
    return questions

def show_menu():
    print("\n=== Chat Knowledge Trainer ===")
    print("1. Mixed Quiz (term → meaning)")
    print("2. Reverse Practice (meaning → term)")
    print("3. Review all concepts")
    print("4. Review wrong answers")
    print("5. Spaced Repetition")
    print("6. Browse by Category")
    print("7. Code Logic Deep Dive")
    print("8. Strict Top-to-Bottom Code Walkthrough")   # ← New option
    print("0. Exit")
    return input("\nChoose: ").strip()

def mixed_quiz(knowledge):
    clear()
    try:
        num = int(input("How many questions? (8-20): ") or "10")
        num = max(5, min(num, 25))
    except:
        num = 10

    questions = get_questions(knowledge, num)
    progress = load_json(DATA_FILE, {"wrong": [], "next_review": {}})
    score = 0
    wrongs = []

    for i, q in enumerate(questions, 1):
        print(f"\n{i}. [{q['category']}] What is: {q['term']}?")
        ans = input("Your answer: ").strip()
        if is_correct(ans, q["meaning"]):
            print("✓ Correct")
            score += 1
        else:
            print(f"✗ {q['meaning']}")
            wrongs.append(q)

    for item in wrongs:
        if not any(w["term"] == item["term"] for w in progress["wrong"]):
            progress["wrong"].append(item)
            progress["next_review"][item["term"]] = (datetime.now() + timedelta(hours=6)).isoformat()

    save_json(DATA_FILE, progress)
    print(f"\nScore: {score}/{len(questions)}")
    input("Press Enter...")

def reverse_practice(knowledge):
    clear()
    questions = random.sample(knowledge, min(8, len(knowledge)))
    score = 0
    for q in questions:
        print(f"\nMeaning: {q['meaning']}")
        ans = input("What concept is this? ").strip()
        if is_correct(ans, q["term"]):
            print("✓ Correct")
            score += 1
        else:
            print(f"✗ {q['term']}")
    print(f"\nScore: {score}/{len(questions)}")
    input("Press Enter...")

def review_all(knowledge):
    clear()
    print("--- All Concepts ---")
    for k in knowledge:
        print(f"{k['term']:40} → {k['meaning']}")
    input("\nPress Enter...")

def review_wrong():
    clear()
    progress = load_json(DATA_FILE, {"wrong": [], "next_review": {}})
    wrongs = progress.get("wrong", [])
    if not wrongs:
        print("No wrong answers yet.")
        input("Press Enter...")
        return
    print(f"--- Wrong Answers ({len(wrongs)}) ---")
    for i, item in enumerate(wrongs, 1):
        print(f"{i}. {item['term']} → {item['meaning']}")
    print("\na = Clear all | Enter = Back")
    if input("Choice: ").strip().lower() == "a":
        progress["wrong"] = []
        progress["next_review"] = {}
        save_json(DATA_FILE, progress)
        print("Cleared.")
    input("Press Enter...")

def spaced_repetition():
    clear()
    progress = load_json(DATA_FILE, {"wrong": [], "next_review": {}})
    now = datetime.now()
    due = []
    for w in progress["wrong"]:
        next_time = progress["next_review"].get(w["term"])
        if next_time:
            try:
                if datetime.fromisoformat(next_time) <= now:
                    due.append(w)
            except:
                due.append(w)

    if not due:
        print("Nothing due right now.")
        input("Press Enter...")
        return

    print(f"{len(due)} items due\n")
    random.shuffle(due)
    for item in due:
        print(f"What is: {item['term']}?")
        ans = input("Answer: ").strip()
        if is_correct(ans, item["meaning"]):
            print("✓ Remembered")
            progress["wrong"] = [w for w in progress["wrong"] if w["term"] != item["term"]]
            progress["next_review"][item["term"]] = (now + timedelta(hours=12)).isoformat()
        else:
            print(f"✗ {item['meaning']}")
            progress["next_review"][item["term"]] = (now + timedelta(hours=6)).isoformat()
    save_json(DATA_FILE, progress)
    input("\nFinished. Press Enter...")

def browse_by_category(knowledge):
    clear()
    categories = defaultdict(list)
    for item in knowledge:
        categories[item["category"]].append(item)

    print("--- Available Categories ---")
    cat_list = sorted(categories.keys())
    for i, cat in enumerate(cat_list, 1):
        print(f"{i}. {cat} ({len(categories[cat])} items)")

    try:
        choice = int(input("\nChoose category number: "))
        selected = cat_list[choice - 1]
    except:
        print("Invalid choice")
        input("Press Enter...")
        return

    clear()
    print(f"--- {selected} ---")
    for item in categories[selected]:
        print(f"\n• {item['term']}")
        print(f"  {item['meaning']}")
    input("\nPress Enter to return...")

def code_deep_dive():
    clear()
    print("=== Code Logic Deep Dive (Option 7) ===")
    print("This section tests understanding of key lines and decisions.\n")

    questions = [
        {
            "q": "What does this line do?\nwith open('terms.csv', newline='', encoding='utf-8') as f:",
            "a": "It opens the CSV file safely so it can be read, and closes it automatically afterwards."
        },
        {
            "q": "Why do we use csv.DictReader instead of normal csv.reader?",
            "a": "DictReader turns each row into a dictionary using the header names as keys."
        },
        {
            "q": "What is the purpose of the load_knowledge() / load_terms() function?",
            "a": "It reads the CSV file once and converts all rows into a list of dictionaries."
        },
        {
            "q": "Why is the main program wrapped in while True?",
            "a": "So the menu keeps running until the user chooses to exit."
        },
        {
            "q": "What does the is_correct() function do?",
            "a": "It checks if the user's answer is reasonably close to the correct meaning."
        },
        {
            "q": "Why do we save wrong answers with a future timestamp?",
            "a": "To support spaced repetition."
        },
        {
            "q": "Why use random.sample()?",
            "a": "To get unique random questions without repetition in one round."
        },
        {
            "q": "What happens if the CSV file is missing?",
            "a": "The program shows an error message and exits cleanly."
        }
    ]

    random.shuffle(questions)
    for i, item in enumerate(questions, 1):
        print(f"\n{i}. {item['q']}")
        input("\nYour explanation: ")
        print(f"\nModel answer: {item['a']}")
        input("\nPress Enter for next...")

    input("\nDeep dive finished. Press Enter...")

def strict_walkthrough():
    clear()
    print("=== Option 8: Strict Top-to-Bottom Code Walkthrough ===")
    print("We will go through the important parts of the code in order.\n")
    input("Press Enter to start...")

    steps = [
        ("1. Shebang & Docstring", 
         "The first lines tell the system to run the file with Python and describe what the program does."),

        ("2. Imports", 
         "We import csv, random, os, json, datetime and defaultdict because we need them for reading files, randomness, clearing screen, saving progress and grouping data."),

        ("3. Global constants", 
         "DATA_FILE and RECENT_FILE are defined at the top so the whole program knows the names of the progress files."),

        ("4. clear() function", 
         "This function clears the terminal screen so the interface looks cleaner between sections."),

        ("5. load_knowledge() function", 
         "This is one of the most important functions. It opens knowledge.csv, reads every row with DictReader, and builds a list of dictionaries."),

        ("6. load_json() and save_json()", 
         "These two helper functions safely read and write the progress and recent files."),

        ("7. is_correct() function", 
         "This function decides whether the user's answer is good enough. It uses flexible matching instead of exact match."),

        ("8. get_questions() function", 
         "This function selects random questions while trying to avoid recently asked ones."),

        ("9. show_menu() function", 
         "This function only displays the menu and returns the user's choice. It keeps the main loop clean."),

        ("10. Individual feature functions", 
         "mixed_quiz, reverse_practice, review_all, review_wrong, spaced_repetition, browse_by_category, etc. Each one handles one specific feature."),

        ("11. main() function", 
         "This is the controller. It loads the data once, then uses a while True loop to keep showing the menu and calling the correct function."),

        ("12. if __name__ == '__main__':", 
         "This line makes sure the main() function runs only when the file is executed directly, not when it is imported.")
    ]

    for title, explanation in steps:
        clear()
        print(f"=== {title} ===\n")
        print(explanation)
        input("\nPress Enter to go to the next part...")

    clear()
    print("Strict top-to-bottom walkthrough completed.")
    print("You have now gone through the major structure of the program in order.")
    input("\nPress Enter to return to the menu...")

def main():
    knowledge = load_knowledge()
    print(f"Loaded {len(knowledge)} concepts")
    while True:
        choice = show_menu()
        if choice == "1":
            mixed_quiz(knowledge)
        elif choice == "2":
            reverse_practice(knowledge)
        elif choice == "3":
            review_all(knowledge)
        elif choice == "4":
            review_wrong()
        elif choice == "5":
            spaced_repetition()
        elif choice == "6":
            browse_by_category(knowledge)
        elif choice == "7":
            code_deep_dive()
        elif choice == "8":
            strict_walkthrough()
        elif choice == "0":
            print("Keep practising!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

