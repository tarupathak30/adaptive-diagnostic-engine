from bson import ObjectId
from app.database import questions_collection
from app.services.adaptive_engine import select_next_question


async def get_question_by_id(question_id: str):
    return await questions_collection.find_one({"_id": ObjectId(question_id)})


async def validate_answer(question_id: str, selected_answer: str):

    question = await get_question_by_id(question_id)

    if not question:
        raise ValueError("Question not found")

    correct = question["correct_answer"] == selected_answer

    return correct, question["difficulty"], question["topic"]


async def get_next_adaptive_question(ability, asked_ids):

    result = await select_next_question(ability, asked_ids)

    if not result:
        return None

    # if no more questions available
    if result["test_finished"]:
        return None

    question = result["question"]

    print("QUESTION OBJECT:", question)



    return {
    "id": question["id"],                 # for frontend display
    "mongo_id": str(question["_id"]),     # for backend filtering
    "question": question["question"],
    "options": question["options"],
    "difficulty": question["difficulty"],
    "topic": question["topic"]
}