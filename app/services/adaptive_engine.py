from typing import List
from math import exp
from app.database import questions_collection


def clamp(value, min_val=0.1, max_val=1.0):
    return max(min_val, min(value, max_val))


def expected_probability(ability: float, difficulty: float) -> float:
    """
    Logistic function estimating probability that user answers correctly.
    """
    return 1 / (1 + exp(-(ability - difficulty)))


def update_ability(current_ability: float, difficulty: float, correct: bool) -> float:
    """
    Improved adaptive update rule using prediction error.

    If user performs better than expected -> ability increases
    If worse than expected -> ability decreases
    """

    learning_rate = 0.2

    expected = expected_probability(current_ability, difficulty)
    actual = 1.0 if correct else 0.0

    error = actual - expected

    new_ability = current_ability + learning_rate * error

    return clamp(new_ability)


async def select_next_question(ability: float, asked_question_ids: List[str]):
    """
    Select question whose difficulty is closest to current ability.
    """

    cursor = questions_collection.find(
        {"id": {"$nin": asked_question_ids}}
    )

    questions = await cursor.to_list(length=100)

    if not questions:
        return None

    best = min(
        questions,
        key=lambda q: abs(q["difficulty"] - ability)
    )

    return best