from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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


# serve front end 
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="ui")

app.include_router(session_router, prefix="")   # already at root, fine
app.include_router(question_router, prefix="")