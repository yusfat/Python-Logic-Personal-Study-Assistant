import json
import os
from datetime import datetime

from config import EXERCISE_PROGRESS_FILE


def load_exercise_progress():
    if os.path.exists(EXERCISE_PROGRESS_FILE):
        try:
            with open(EXERCISE_PROGRESS_FILE, encoding="utf-8") as progress_file:
                return json.load(progress_file)
        except Exception:
            pass
    return {"attempts": {}, "scores": {}, "completed": []}


def save_exercise_progress(progress_data):
    with open(EXERCISE_PROGRESS_FILE, "w", encoding="utf-8") as progress_file:
        json.dump(progress_data, progress_file, indent=2)


def update_progress_after_attempt(exercise_id, attempt_number, best_score_ratio):
    progress_data = load_exercise_progress()
    progress_data.setdefault("attempts", {})
    progress_data.setdefault("scores", {})
    progress_data.setdefault("completed", [])

    progress_data["attempts"][exercise_id] = (
        progress_data["attempts"].get(exercise_id, 0) + attempt_number
    )
    previous_best = progress_data["scores"].get(exercise_id, 0)
    progress_data["scores"][exercise_id] = max(previous_best, best_score_ratio)

    if best_score_ratio >= 0.80 and exercise_id not in progress_data["completed"]:
        progress_data["completed"].append(exercise_id)

    progress_data["last_update"] = datetime.now().isoformat()
    save_exercise_progress(progress_data)
    return progress_data


