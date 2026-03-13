from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import sessions_collection
from app.models import AnswerSubmission
from app.services.question_service import (
    validate_answer,
    get_next_adaptive_question
)
from app.services.adaptive_engine import update_ability
from app.services.llm_service import generate_study_plan

router = APIRouter()


@router.post("/start-session")
async def start_session(user_id: str):

    session = {
        "user_id": user_id,
        "current_ability": 0.5,
        "questions_answered": [],
        "current_question": None,
        "status": "active"
    }

    result = await sessions_collection.insert_one(session)

    first_question = await get_next_adaptive_question(0.5, [])

    if not first_question:
        raise HTTPException(500, "No questions available")

    await sessions_collection.update_one(
        {"_id": result.inserted_id},
        {
            "$set": {
                "current_question": first_question["mongo_id"]
            }
        }
    )

    return {
        "session_id": str(result.inserted_id),
        "question": first_question
    }


@router.post("/submit-answer")
async def submit_answer(payload: AnswerSubmission):

    session = await sessions_collection.find_one(
        {"_id": ObjectId(payload.session_id)}
    )

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    correct, difficulty, topic = await validate_answer(
        payload.question_id,
        payload.selected_answer
    )

    ability = update_ability(
        session["current_ability"],
        difficulty,
        correct
    )

    session["questions_answered"].append({
        "question_id": payload.question_id,   # must be Mongo _id
        "difficulty": difficulty,
        "correct": correct,
        "topic": topic
    })

    asked_ids = [q["question_id"] for q in session["questions_answered"]]

    next_q = await get_next_adaptive_question(
        ability,
        asked_ids
    )

    next_question_id = next_q["mongo_id"] if next_q else None

    await sessions_collection.update_one(
        {"_id": ObjectId(payload.session_id)},
        {
            "$set": {
                "current_ability": ability,
                "questions_answered": session["questions_answered"],
                "current_question": next_question_id
            }
        }
    )

    return {
        "correct": correct,
        "new_ability": ability,
        "next_question": next_q
    }


@router.get("/generate-study-plan/{session_id}")
async def generate_plan(session_id: str):
    # Guard against "null" or garbage IDs from frontend
    if not session_id or session_id == "null" or len(session_id) != 24:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    session = await sessions_collection.find_one(
        {"_id": ObjectId(session_id)}
    )

    if not session:
        raise HTTPException(status_code=404)

    answers = session["questions_answered"]

    if len(answers) < 10:
        raise HTTPException(
            status_code=400,
            detail="Need at least 10 questions answered"
        )

    topics_missed = [
        a["topic"] for a in answers if not a["correct"]
    ]

    correct_count = sum(
        1 for a in answers if a["correct"]
    )

    plan = await generate_study_plan(
        session["current_ability"],
        topics_missed,
        correct_count
    )

    return {"study_plan": plan}