from typing import List
from app.database import questions_collection

def clamp(value, min_val=0.1, max_val=1.0):
    return max(min_val, min(value, max_val))


def update_ability(current_ability: float, difficulty: float, correct: bool) -> float:
    """
    Simple adaptive update rule.

    Correct answer:
        increase ability slightly depending on question difficulty

    Incorrect answer:
        decrease ability proportionally to difficulty
    """

    if correct:
        current_ability = current_ability + 0.1 * (1 - difficulty)
    else:
        current_ability = current_ability - 0.1 * difficulty

    return clamp(current_ability)


async def select_next_question(ability: float, asked_question_ids: List[str]):
    """
    Select question with difficulty closest to current ability.
    """

    cursor = questions_collection.find(
        {"_id": {"$nin": asked_question_ids}}
    )

    questions = await cursor.to_list(length=100)

    if not questions:
        return None

    best = min(
        questions,
        key=lambda q: abs(q["difficulty"] - ability)
    )

    return best