#!/usr/bin/env python3
"""
Code P - Knowledge Trainer
Option 9 opens Exercises mode
"""

import csv
import random
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

PROGRESS_FILE = "progress.json"
RECENT_FILE = "recent.json"
KNOWLEDGE_FILE = "knowledge.csv"


def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def load_knowledge_rows():
    knowledge_rows = []
    try:
        with open(KNOWLEDGE_FILE, newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for one_row in csv_reader:
                term_text = (one_row.get("term") or "").strip()
                if not term_text:
                    continue
                knowledge_rows.append({
                    "type": (one_row.get("type") or "").strip(),
                    "term": term_text,
                    "meaning": (one_row.get("meaning") or "").strip(),
                    "category": (one_row.get("category") or "").strip(),
                })
    except FileNotFoundError:
        print(f"ERROR: {KNOWLEDGE_FILE} not found!")
        raise SystemExit(1)
    return knowledge_rows


def load_json_file(file_name, default_value):
    if os.path.exists(file_name):
        try:
            with open(file_name, encoding="utf-8") as json_file:
                return json.load(json_file)
        except Exception:
            return default_value
    return default_value


def save_json_file(file_name, data_value):
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(data_value, json_file, indent=2)


def answer_looks_correct(student_answer, expected_answer):
    student_text = student_answer.strip().lower()
    expected_text = expected_answer.lower()
    if len(student_text) < 3:
        return False
    return (
        student_text in expected_text
        or expected_text in student_text
        or any(word in student_text for word in expected_text.split() if len(word) > 4)
    )


def pick_quiz_questions(knowledge_rows, how_many):
    recent_terms = load_json_file(RECENT_FILE, [])
    available_rows = [row for row in knowledge_rows if row["term"] not in recent_terms]
    if len(available_rows) < how_many:
        available_rows = knowledge_rows[:]
    selected_rows = random.sample(available_rows, min(how_many, len(available_rows)))
    updated_recent = [row["term"] for row in selected_rows] + recent_terms
    save_json_file(RECENT_FILE, updated_recent[:60])
    return selected_rows


def show_main_menu():
    print("\n=== Code P - Knowledge Trainer ===")
    print("1. Mixed Quiz (term -> meaning)")
    print("2. Reverse Practice (meaning -> term)")
    print("3. Review all concepts")
    print("4. Review wrong answers")
    print("5. Spaced Repetition")
    print("6. Browse by Category")
    print("7. Code Logic Deep Dive")
    print("8. Strict Top-to-Bottom Walkthrough")
    print("9. Exercises-only mode")
    print("0. Exit")
    return input("\nChoose: ").strip()


def run_mixed_quiz(knowledge_rows):
    clear_screen()
    try:
        how_many = int(input("How many questions? (8-20): ") or "10")
        how_many = max(5, min(how_many, 25))
    except Exception:
        how_many = 10

    selected_rows = pick_quiz_questions(knowledge_rows, how_many)
    progress_data = load_json_file(PROGRESS_FILE, {"wrong": [], "next_review": {}})
    correct_count = 0
    wrong_rows = []

    for question_number, one_row in enumerate(selected_rows, 1):
        print(f"\n{question_number}. [{one_row['category']}] What is: {one_row['term']}?")
        student_answer = input("Your answer: ").strip()
        if answer_looks_correct(student_answer, one_row["meaning"]):
            print("Correct")
            correct_count += 1
        else:
            print(f"Answer: {one_row['meaning']}")
            wrong_rows.append(one_row)

    for wrong_row in wrong_rows:
        already_saved = any(saved["term"] == wrong_row["term"] for saved in progress_data["wrong"])
        if not already_saved:
            progress_data["wrong"].append(wrong_row)
            progress_data["next_review"][wrong_row["term"]] = (
                datetime.now() + timedelta(hours=6)
            ).isoformat()

    save_json_file(PROGRESS_FILE, progress_data)
    print(f"\nScore: {correct_count}/{len(selected_rows)}")
    input("Press Enter...")


def run_reverse_practice(knowledge_rows):
    clear_screen()
    selected_rows = random.sample(knowledge_rows, min(8, len(knowledge_rows)))
    correct_count = 0
    for one_row in selected_rows:
        print(f"\nMeaning: {one_row['meaning']}")
        student_answer = input("What term/concept is this? ").strip()
        if answer_looks_correct(student_answer, one_row["term"]):
            print("Correct")
            correct_count += 1
        else:
            print(f"Answer: {one_row['term']}")
    print(f"\nScore: {correct_count}/{len(selected_rows)}")
    input("Press Enter...")


def review_all_concepts(knowledge_rows):
    clear_screen()
    for one_row in knowledge_rows:
        print(f"{one_row['term'][:42]:42} -> {one_row['meaning']}")
    input("\nPress Enter...")


def review_wrong_answers():
    clear_screen()
    progress_data = load_json_file(PROGRESS_FILE, {"wrong": [], "next_review": {}})
    wrong_rows = progress_data.get("wrong", [])
    if not wrong_rows:
        print("No wrong answers yet.")
        input("Press Enter...")
        return
    for index_number, wrong_row in enumerate(wrong_rows, 1):
        print(f"{index_number}. {wrong_row['term']} -> {wrong_row['meaning']}")
    if input("\na = Clear all | Enter = Back: ").strip().lower() == "a":
        progress_data["wrong"] = []
        progress_data["next_review"] = {}
        save_json_file(PROGRESS_FILE, progress_data)
        print("Cleared.")
    input("Press Enter...")


def run_spaced_repetition():
    clear_screen()
    progress_data = load_json_file(PROGRESS_FILE, {"wrong": [], "next_review": {}})
    now_time = datetime.now()
    due_rows = []
    for wrong_row in progress_data["wrong"]:
        next_time_text = progress_data["next_review"].get(wrong_row["term"])
        if next_time_text:
            try:
                if datetime.fromisoformat(next_time_text) <= now_time:
                    due_rows.append(wrong_row)
            except Exception:
                due_rows.append(wrong_row)
    if not due_rows:
        print("Nothing due right now.")
        input("Press Enter...")
        return
    random.shuffle(due_rows)
    for due_row in due_rows:
        print(f"What is: {due_row['term']}?")
        student_answer = input("Answer: ").strip()
        if answer_looks_correct(student_answer, due_row["meaning"]):
            print("Remembered")
            progress_data["wrong"] = [
                row for row in progress_data["wrong"] if row["term"] != due_row["term"]
            ]
            progress_data["next_review"][due_row["term"]] = (
                now_time + timedelta(hours=12)
            ).isoformat()
        else:
            print(f"Answer: {due_row['meaning']}")
            progress_data["next_review"][due_row["term"]] = (
                now_time + timedelta(hours=6)
            ).isoformat()
    save_json_file(PROGRESS_FILE, progress_data)
    input("\nFinished. Press Enter...")


def browse_by_category(knowledge_rows):
    clear_screen()
    category_map = defaultdict(list)
    for one_row in knowledge_rows:
        category_name = one_row["category"] or "Uncategorized"
        category_map[category_name].append(one_row)
    category_names = sorted(category_map.keys())
    for index_number, category_name in enumerate(category_names, 1):
        print(f"{index_number}. {category_name} ({len(category_map[category_name])})")
    try:
        chosen_name = category_names[int(input("\nCategory number: ")) - 1]
    except Exception:
        print("Invalid choice")
        input("Press Enter...")
        return
    clear_screen()
    for one_row in category_map[chosen_name]:
        print(f"\n- {one_row['term']}\n  {one_row['meaning']}")
    input("\nPress Enter...")


def run_code_deep_dive():
    clear_screen()
    deep_questions = [
        ("Why DictReader?", "Header names become dictionary keys."),
        ("Why load CSV once?", "Avoid repeated disk reads."),
        ("Why while True menu?", "Run until user exits."),
        ("Why random.sample?", "Unique questions per round."),
        ("Why JSON progress?", "Nested wrong lists and review dates."),
    ]
    random.shuffle(deep_questions)
    for question_number, (question_text, model_answer) in enumerate(deep_questions, 1):
        print(f"\n{question_number}. {question_text}")
        input("Your explanation: ")
        print(f"Model answer: {model_answer}")
        input("Press Enter...")


def run_strict_walkthrough():
    clear_screen()
    walk_steps = [
        ("Imports and constants", "Tools and file names."),
        ("load_knowledge_rows", "CSV becomes list of dictionaries."),
        ("answer_looks_correct", "Flexible checking."),
        ("pick_quiz_questions", "Unique random selection."),
        ("main loop", "Menu until exit."),
    ]
    for step_title, step_text in walk_steps:
        clear_screen()
        print(f"=== {step_title} ===\n{step_text}")
        input("\nPress Enter...")


def open_exercises_mode():
    clear_screen()
    try:
        from exercises import run_exercises_menu
    except ImportError:
        print("ERROR: exercises.py not found in this folder.")
        input("Press Enter...")
        return
    run_exercises_menu()


def main():
    knowledge_rows = load_knowledge_rows()
    print(f"Loaded {len(knowledge_rows)} items")
    while True:
        menu_choice = show_main_menu()
        if menu_choice == "1":
            run_mixed_quiz(knowledge_rows)
        elif menu_choice == "2":
            run_reverse_practice(knowledge_rows)
        elif menu_choice == "3":
            review_all_concepts(knowledge_rows)
        elif menu_choice == "4":
            review_wrong_answers()
        elif menu_choice == "5":
            run_spaced_repetition()
        elif menu_choice == "6":
            browse_by_category(knowledge_rows)
        elif menu_choice == "7":
            run_code_deep_dive()
        elif menu_choice == "8":
            run_strict_walkthrough()
        elif menu_choice == "9":
            open_exercises_mode()
        elif menu_choice == "0":
            print("Keep practising.")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()