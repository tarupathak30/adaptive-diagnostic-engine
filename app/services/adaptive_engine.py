import random
from typing import List, Dict
from math import exp
from bson import ObjectId
from app.database import questions_collection


LEARNING_RATE = 0.2
ABILITY_MIN = 0.1
ABILITY_MAX = 1.0

DIFFICULTY_BAND = 0.15
EXPLORATION_BAND = 0.30
EXPLORATION_RATE = 0.12


def clamp(value: float, min_val: float = ABILITY_MIN, max_val: float = ABILITY_MAX) -> float:
    return max(min_val, min(value, max_val))


def expected_probability(ability: float, difficulty: float) -> float:
    return 1 / (1 + exp(-(ability - difficulty)))


def update_ability(current_ability: float, difficulty: float, correct: bool) -> float:
    expected = expected_probability(current_ability, difficulty)
    actual = 1.0 if correct else 0.0
    error = actual - expected
    return clamp(current_ability + LEARNING_RATE * error)


def initialize_ability() -> float:
    return 0.5


def _to_object_ids(asked_ids: List[str]) -> List[ObjectId]:
    """Safely convert string IDs to ObjectIds, skipping malformed ones."""
    result = []
    for i in asked_ids:
        try:
            result.append(ObjectId(str(i)))
        except Exception:
            pass
    return result


def _serialize_question(q: dict) -> dict:
    """Normalize ObjectId to string so the question is JSON-safe."""
    q["_id"] = str(q["_id"])
    return q


async def select_next_question(
    ability: float,
    asked_question_ids: List[str]
) -> Dict:

    asked_object_ids = _to_object_ids(asked_question_ids)

    # Check if any questions remain
    remaining = await questions_collection.count_documents(
        {"_id": {"$nin": asked_object_ids}}
    )

    if remaining == 0:
        return {
            "question": None,
            "test_finished": True,
            "message": "You have reached the end of the test."
        }

    # Exploration: pick randomly within a wider band
    if random.random() < EXPLORATION_RATE:
        pipeline = [
            {"$match": {
                "_id": {"$nin": asked_object_ids},
                "difficulty": {
                    "$gte": ability - EXPLORATION_BAND,
                    "$lte": ability + EXPLORATION_BAND
                }
            }},
            {"$sample": {"size": 1}}
        ]
        results = await questions_collection.aggregate(pipeline).to_list(1)

        # If nothing in exploration band, fall through to normal selection
        if results:
            return {
                "question": _serialize_question(results[0]),
                "test_finished": False
            }

    # Primary: fetch a small pool within the tight difficulty band, pick randomly
    primary_pipeline = [
        {"$match": {
            "_id": {"$nin": asked_object_ids},
            "difficulty": {
                "$gte": ability - DIFFICULTY_BAND,
                "$lte": ability + DIFFICULTY_BAND
            }
        }},
        {"$sample": {"size": 5}}
    ]
    candidates = await questions_collection.aggregate(primary_pipeline).to_list(5)

    if candidates:
        q = random.choice(candidates)
        return {
            "question": _serialize_question(q),
            "test_finished": False
        }

    # Fallback: no candidates in band — pick the closest difficulty question
    fallback_pipeline = [
        {"$match": {"_id": {"$nin": asked_object_ids}}},
        {"$addFields": {
            "dist": {"$abs": {"$subtract": ["$difficulty", ability]}}
        }},
        {"$sort": {"dist": 1}},
        {"$limit": 1}
    ]
    fallback = await questions_collection.aggregate(fallback_pipeline).to_list(1)

    if fallback:
        return {
            "question": _serialize_question(fallback[0]),
            "test_finished": False
        }

    # Shouldn't reach here given the count check above, but safety net
    return {
        "question": None,
        "test_finished": True,
        "message": "No suitable question found."
    }
