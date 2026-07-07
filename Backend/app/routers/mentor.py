from fastapi import APIRouter

from app.models.schemas import AIResponse, ChatInput, CodeInput
from app.prompts.mentor import build_socratic_continue_prompt, build_socratic_start_prompt
from app.services.gemini_service import format_history, run_text_prompt

router = APIRouter()


def _fallback_response(problem: str) -> str:
    return (
        "I’m having trouble reaching the AI model right now, so I can’t generate a live response. "
        "For this problem, start by restating the brute-force idea, then ask what pattern would let you "
        "avoid checking every pair. If you share your current approach, I can still help you reason through it."
    )


@router.post("/api/start_session", response_model=AIResponse)
async def start_session(user_input: CodeInput):
    try:
        message = run_text_prompt(
            build_socratic_start_prompt(),
            {
                "language": user_input.language,
                "topic": user_input.topic,
                "problem": user_input.problem,
                "code": user_input.code,
            },
        )
    except Exception:
        message = _fallback_response(user_input.problem)
    return AIResponse(**{"from": "ai", "text": message})


@router.post("/api/chat", response_model=AIResponse)
async def chat_session(chat_input: ChatInput):
    try:
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
    except Exception:
        message = _fallback_response(chat_input.problem)
    return AIResponse(**{"from": "ai", "text": message})
