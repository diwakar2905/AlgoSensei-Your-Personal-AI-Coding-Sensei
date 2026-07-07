import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.code_review import router as code_review_router
from app.routers.interview import router as interview_router
from app.routers.mentor import router as mentor_router

# Load local environment variables for development.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "python.env"))

# Keep a single FastAPI entrypoint so the current Render start command remains valid.
app = FastAPI(title="AlgoSensei API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mentor_router)
app.include_router(code_review_router)
app.include_router(interview_router)


@app.get("/")
def read_root():
    return {
        "message": "AlgoSensei Backend is running!",
        "architecture": "routers/services/prompts/models",
    }

