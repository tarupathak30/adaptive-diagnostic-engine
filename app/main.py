from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.session_routes import router as session_router
from app.routes.question_routes import router as question_router

app = FastAPI(title="Adaptive Test Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_router)
app.include_router(question_router)