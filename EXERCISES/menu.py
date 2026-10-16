import secrets

from utils import clear_screen
from progress import load_exercise_progress
from exercises_data import EXERCISES
from practice import practice_one_exercise


def show_progress_stats(progress_data):
    completed_ids = progress_data.get("completed", [])
    score_map = progress_data.get("scores", {})
    print(f"Completed: {len(completed_ids)}/50")
    if score_map:
        average_score = sum(score_map.values()) / len(score_map)
        print(f"Average best score: {int(average_score * 100)}%")
    else:
        print("No scores yet.")


def run_exercises_menu():
    while True:
        clear_screen()
        progress_data = load_exercise_progress()
        print("=== Exercises-only mode (EX1-EX50) ===")
        show_progress_stats(progress_data)
        print("\n1. List all exercises")
        print("2. Practice one by ID")
        print("3. Random exercise")
        print("4. Random Master-level only")
        print("0. Back")
        menu_choice = input("\nChoose: ").strip()

        if menu_choice == "0":
            return
        if menu_choice == "1":
            clear_screen()
            for one_exercise in EXERCISES:
                done_mark = (
                    "Y" if one_exercise["id"] in progress_data.get("completed", []) else " "
                )
                print(
                    f"[{done_mark}] {one_exercise['id']} "
                    f"[{one_exercise['level']}] {one_exercise['title']}"
                )
            input("\nPress Enter...")
        elif menu_choice == "2":
            exercise_id = input("ID (EX1..EX50): ").strip().upper()
            selected = next(
                (ex for ex in EXERCISES if ex["id"] == exercise_id), None
            )
            if not selected:
                print("Not found")
                input("Press Enter...")
            else:
                practice_one_exercise(selected)
        elif menu_choice == "3":
            practice_one_exercise(secrets.choice(EXERCISES))
        elif menu_choice == "4":
            master_list = [ex for ex in EXERCISES if ex["level"] == "Master"]
            practice_one_exercise(secrets.choice(master_list))
        else:
            print("Invalid choice")
            input("Press Enter...")

