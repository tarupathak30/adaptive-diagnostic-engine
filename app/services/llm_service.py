import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2
)


async def generate_study_plan(ability, topics_missed, correct_count):

    prompt = f"""
You are an academic tutor.

Student ability score: {ability}
Correct answers: {correct_count}
Weak topics: {topics_missed}

Generate a concise 3-step study plan tailored to improve the student's weak areas.
Keep it clear and actionable.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return response.content