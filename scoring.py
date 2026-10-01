"""Scoring functions for the work-style diagnosis."""

from collections import defaultdict


ANSWER_TO_PERCENT = {1: 0.0, 2: 25.0, 3: 50.0, 4: 75.0, 5: 100.0}


def calculate_scores(questions, answers, axes):
    """Return the first-pole percentage for every axis.

    A response of 5 gives 100 points to the pole named by ``agree_pole``.
    Reverse-keyed questions are converted automatically.
    """
    grouped_scores = defaultdict(list)

    for question in questions:
        question_id = question["id"]
        if question_id not in answers:
            raise ValueError(f"Question {question_id} has not been answered.")

        answer = answers[question_id]
        if answer not in ANSWER_TO_PERCENT:
            raise ValueError(f"Question {question_id} has an invalid answer: {answer}")

        axis_id = question["axis"]
        first_pole = axes[axis_id]["first_code"]
        agreement_score = ANSWER_TO_PERCENT[answer]

        if question["agree_pole"] == first_pole:
            first_pole_score = agreement_score
        else:
            first_pole_score = 100.0 - agreement_score

        grouped_scores[axis_id].append(first_pole_score)

    return {
        axis_id: sum(values) / len(values)
        for axis_id, values in grouped_scores.items()
    }


def find_tied_axes(scores):
    """Return axes whose two poles are exactly balanced."""
    return [axis_id for axis_id, score in scores.items() if score == 50.0]


def infer_tie_answers(questions, answers, axes, scores):
    """Resolve exact ties without asking an additional question.

    The graph remains 50/50. For the four-letter code only, the strongest
    non-neutral response on that axis is used. If every response is neutral,
    the first pole provides a stable fallback because a four-letter type still
    requires one letter per axis.
    """
    choices = {}

    for axis_id in find_tied_axes(scores):
        axis = axes[axis_id]
        axis_questions = [q for q in questions if q["axis"] == axis_id]
        strongest = max(
            axis_questions,
            key=lambda question: abs(answers[question["id"]] - 3),
        )
        answer = answers[strongest["id"]]

        if answer == 3:
            choices[axis_id] = axis["first_code"]
        elif answer > 3:
            choices[axis_id] = strongest["agree_pole"]
        else:
            choices[axis_id] = (
                axis["second_code"]
                if strongest["agree_pole"] == axis["first_code"]
                else axis["first_code"]
            )

    return choices


def build_type_code(scores, axes, tie_answers=None):
    """Build the four-letter type code in the order defined by ``axes``."""
    tie_answers = tie_answers or {}
    code = []

    for axis_id, axis in axes.items():
        score = scores[axis_id]
        if score > 50.0:
            code.append(axis["first_code"])
        elif score < 50.0:
            code.append(axis["second_code"])
        else:
            if axis_id not in tie_answers:
                raise ValueError(f"Axis {axis_id} requires a tie-break answer.")
            code.append(tie_answers[axis_id])

    return "".join(code)


def display_percentages(first_pole_score):
    """Return integer percentages that always add up to 100."""
    first = int(first_pole_score + 0.5)
    return first, 100 - first


def tendency_label(first_pole_score):
    """Describe how strongly the dominant pole is expressed."""
    dominant = max(first_pole_score, 100.0 - first_pole_score)
    if dominant < 55:
        return "ほぼ均衡"
    if dominant < 65:
        return "やや傾向あり"
    if dominant < 80:
        return "比較的強い傾向"
    return "はっきりした傾向"
