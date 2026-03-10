import asyncio
import random
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["adaptive_testing"]
questions = db["questions"]

def arithmetic_question(i):
    a = random.randint(50,150)
    b = random.randint(10,40)
    correct = a*b
    return {
        "id": f"q{i}",
        "question": f"What is {a} × {b}?",
        "options": [str(correct),
                    str(correct+random.randint(5,30)),
                    str(correct-random.randint(5,30)),
                    str(correct+random.randint(31,60))],
        "correct_answer": str(correct),
        "difficulty": round(random.uniform(0.2,0.4),2),
        "topic": "arithmetic"
    }

def algebra_question(i):
    a = random.randint(2,10)
    b = random.randint(2,10)
    correct = b/a
    return {
        "id": f"q{i}",
        "question": f"Solve for x: {a}x = {b}",
        "options": [str(correct),
                    str(correct+1),
                    str(correct-1),
                    str(correct+2)],
        "correct_answer": str(correct),
        "difficulty": round(random.uniform(0.4,0.6),2),
        "topic": "algebra"
    }

def geometry_question(i):
    r = random.randint(3,10)
    area = round(3.1416*r*r,2)
    return {
        "id": f"q{i}",
        "question": f"What is the area of a circle with radius {r}? (π≈3.14)",
        "options": [str(area),
                    str(area+10),
                    str(area-10),
                    str(area+20)],
        "correct_answer": str(area),
        "difficulty": round(random.uniform(0.5,0.7),2),
        "topic": "geometry"
    }

def calculus_question(i):
    n = random.randint(2,6)
    return {
        "id": f"q{i}",
        "question": f"What is the derivative of x^{n}?",
        "options": [f"{n}x^{n-1}",
                    f"{n-1}x^{n}",
                    f"x^{n}",
                    f"{n+1}x^{n-1}"],
        "correct_answer": f"{n}x^{n-1}",
        "difficulty": round(random.uniform(0.7,0.9),2),
        "topic": "calculus"
    }

generators = [
    arithmetic_question,
    algebra_question,
    geometry_question,
    calculus_question
]

async def seed():
    data = []
    for i in range(1,101):
        generator = random.choice(generators)
        print("at question : ", i+1)
        data.append(generator(i))

    await questions.delete_many({})
    await questions.insert_many(data)

    print("Seeded 100 tougher questions.")

asyncio.run(seed())