from fastapi import APIRouter

from app.models.schemas import (
    InterviewFinalInput,
    InterviewFinalResponse,
    InterviewStartInput,
    InterviewStartResponse,
    InterviewTurnInput,
    InterviewTurnResponse,
)
from app.prompts.interview import (
    build_interview_final_prompt,
    build_interview_start_prompt,
    build_interview_turn_prompt,
    domain_guidance,
)
from app.services.gemini_service import format_history, run_json_prompt

router = APIRouter()


@router.post("/api/interview/start", response_model=InterviewStartResponse)
async def interview_start(payload: InterviewStartInput):
    evaluation_focus = domain_guidance(payload.domain)
    result = run_json_prompt(
        build_interview_start_prompt(),
        {
            "domain": payload.domain,
            "difficulty": payload.difficulty,
            "evaluation_focus": evaluation_focus,
        },
        {
            "question": "Tell me about a system or concept you would use to solve this problem.",
            "score": 0,
            "round_number": 1,
        },
    )
    return InterviewStartResponse(**result)


@router.post("/api/interview/turn", response_model=InterviewTurnResponse)
async def interview_turn(payload: InterviewTurnInput):
    evaluation_focus = domain_guidance(payload.domain)
    result = run_json_prompt(
        build_interview_turn_prompt(),
        {
            "domain": payload.domain,
            "difficulty": payload.difficulty,
            "evaluation_focus": evaluation_focus,
            "latest_answer": payload.latest_answer,
            "history": format_history(payload.history),
        },
        {
            "evaluation": "Thanks for the answer.",
            "follow_up": "Can you go one level deeper on the trade-offs you mentioned?",
            "score": 50,
            "round_number": payload.round_number,
            "should_end": False,
        },
    )
    return InterviewTurnResponse(**result)


@router.post("/api/interview/finalize", response_model=InterviewFinalResponse)
async def interview_finalize(payload: InterviewFinalInput):
    evaluation_focus = domain_guidance(payload.domain)
    result = run_json_prompt(
        build_interview_final_prompt(),
        {
            "domain": payload.domain,
            "difficulty": payload.difficulty,
            "evaluation_focus": evaluation_focus,
            "history": format_history(payload.history),
        },
        {
            "overall_score": 60,
            "verdict": "Solid foundation with clear room to sharpen interview execution.",
            "strengths": ["Communicates clearly"],
            "weaknesses": ["Needs stronger depth on trade-offs"],
            "next_steps": ["Practice another round", "Review core patterns"],
        },
    )
    return InterviewFinalResponse(**result)
