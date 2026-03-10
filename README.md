# Adaptive Test Engine
![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-4ea94b)
![Groq](https://img.shields.io/badge/LLM-Groq-F55036)
![Architecture](https://img.shields.io/badge/Architecture-Modular-brightgreen)
![API](https://img.shields.io/badge/API-REST-blue)
![Project](https://img.shields.io/badge/Type-Adaptive%20Testing%20Engine-blueviolet)
![Status](https://img.shields.io/badge/Status-Prototype-orange)



#AI-powered adaptive testing prototype built with FastAPI and MongoDB.

## Overview

This system dynamically adjusts question difficulty based on the student's performance.

Ability score begins at **0.5** and updates after each answer.

The engine selects the next question whose difficulty is closest to the student's ability.

After the test, an AI-generated study plan is produced.

---

## Tech Stack

- FastAPI
- MongoDB
- Motor async driver
- OpenAI API

---

## Setup

Install dependencies:

pip install -r requirements.txt

Create environment variables:

cp .env.example .env

Run server:

uvicorn app.main:app --reload

Seed database:

python seed/seed_questions.py

---

## API Endpoints

POST /start-session  
POST /submit-answer  
GET /next-question/{session_id}  
GET /generate-study-plan/{session_id}

---

## Adaptive Algorithm

Ability starts at 0.5.

Correct answer:

ability = ability + 0.1 × (1 − difficulty)

Incorrect answer:

ability = ability − 0.1 × difficulty

Ability is clamped between 0.1 and 1.0.

The next question selected has difficulty closest to the student's ability.

---

## AI Log

AI tools were used to:

- Generate initial code scaffolding
- Assist with FastAPI routing structure
- Design adaptive logic
- Help build LLM prompt templates for study plans

All generated code was reviewed and adapted manually during development.
