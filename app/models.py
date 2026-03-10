from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    difficulty: float
    topic: str
    tags: List[str]

class QuestionResponse(BaseModel):
    id: str
    question: str
    options: List[str]
    difficulty: float
    topic: str

class AnswerSubmission(BaseModel):
    session_id: str
    question_id: str
    selected_answer: str

class AnswerRecord(BaseModel):
    question_id: str
    difficulty: float
    correct: bool

class UserSession(BaseModel):
    user_id: str
    current_ability: float = 0.5
    questions_answered: List[AnswerRecord] = []
    current_question: Optional[str] = None
    status: str = "active"

class StudyPlanResponse(BaseModel):
    plan: str