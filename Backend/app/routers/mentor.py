from fastapi import APIRouter

from app.models.schemas import AIResponse, ChatInput, CodeInput
from app.prompts.mentor import build_socratic_continue_prompt, build_socratic_start_prompt
from app.services.gemini_service import format_history, run_text_prompt

router = APIRouter()


@router.post("/api/start_session", response_model=AIResponse)
async def start_session(user_input: CodeInput):
    message = run_text_prompt(
        build_socratic_start_prompt(),
        {
            "language": user_input.language,
            "topic": user_input.topic,
            "problem": user_input.problem,
            "code": user_input.code,
        },
    )
    return AIResponse(**{"from": "ai", "text": message})


@router.post("/api/chat", response_model=AIResponse)
async def chat_session(chat_input: ChatInput):
    message = run_text_prompt(
        build_socratic_continue_prompt(),
        {
            "language": chat_input.language,
            "topic": chat_input.topic,
            "problem": chat_input.problem,
            "code": chat_input.code,
            "history": format_history(chat_input.history),
        },
    )
    return AIResponse(**{"from": "ai", "text": message})
