import os


def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def grade_student_answer(student_answer, model_answer):
    student_text = student_answer.strip().lower()
    model_text = model_answer.strip().lower()
    if not student_text or len(student_text) < 3:
        return 0.0
    if student_text == model_text:
        return 1.0
    if student_text in model_text or model_text in student_text:
        return 0.85
    student_words = {
        word
        for word in student_text.replace(".", " ").replace(",", " ").split()
        if len(word) > 2
    }
    model_words = {
        word
        for word in model_text.replace(".", " ").replace(",", " ").split()
        if len(word) > 2
    }
    if not model_words:
        return 0.0
    same_words = len(student_words & model_words)
    return min(1.0, same_words / max(len(model_words), 1))


def score_label(score_ratio):
    if score_ratio >= 0.80:
        return "Correct"
    if score_ratio >= 0.50:
        return "Partially correct"
    return "Incorrect"

