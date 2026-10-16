from utils import clear_screen, grade_student_answer, score_label
from progress import update_progress_after_attempt


def practice_one_exercise(exercise_data):
    clear_screen()
    print(f"{exercise_data['id']} - {exercise_data['title']} ({exercise_data['level']})")
    print("\nBROKEN / TASK CODE:")
    print(exercise_data["broken_code_text"])
    print("\nSYMPTOM / SCENARIO:")
    print(exercise_data["symptom_text"])
    print("\nTASKS:")
    for task_number, task_text in enumerate(exercise_data["task_list"], 1):
        print(f"{task_number}. {task_text}")

    model_answer_text = exercise_data["model_answer_text"]
    attempt_number = 0
    best_score_ratio = 0.0

    while attempt_number < 5:
        attempt_number += 1
        print(f"\n--- Attempt {attempt_number}/5 ---")
        student_answer = input("Your solution/explanation:\n> ").strip()
        score_ratio = grade_student_answer(student_answer, model_answer_text)
        best_score_ratio = max(best_score_ratio, score_ratio)
        print(f"Result: {score_label(score_ratio)} ({int(score_ratio * 100)}%)")

        if attempt_number == 4 and score_ratio < 0.50:
            print("Rejected on 4th attempt (< 50% correctness). Try again.")
            attempt_number -= 1
            continue

        if attempt_number >= 5:
            print("\nMODEL ANSWER:")
            print(model_answer_text)
            break

        print("Model answer is locked until attempt 5.")

    update_progress_after_attempt(
        exercise_data["id"], attempt_number, best_score_ratio
    )

    print(f"\nSaved. Best score for {exercise_data['id']}: {int(best_score_ratio * 100)}%")
    input("Press Enter...")

