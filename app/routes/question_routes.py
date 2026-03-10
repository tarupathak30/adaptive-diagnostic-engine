from fastapi import APIRouter
from bson import ObjectId
from app.database import sessions_collection
from app.services.question_service import get_next_adaptive_question

router = APIRouter()


@router.get("/next-question/{session_id}")
async def next_question(session_id: str):

    session = await sessions_collection.find_one(
        {"_id": ObjectId(session_id)}
    )

    asked = [q["question_id"] for q in session["questions_answered"]]

    question = await get_next_adaptive_question(
        session["current_ability"],
        asked
    )

    return question