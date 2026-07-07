from fastapi import APIRouter

from app.models.schemas import CodeReviewInput, CodeReviewResponse
from app.prompts.code_review import build_code_review_prompt
from app.services.gemini_service import run_json_prompt

router = APIRouter()


@router.post("/api/code_review", response_model=CodeReviewResponse)
async def code_review(payload: CodeReviewInput):
    result = run_json_prompt(
        build_code_review_prompt(),
        {
            "code": payload.code,
            "language": payload.language,
            "focus_area": payload.focus_area,
        },
        {
            "code_quality_analysis": "Unable to parse review response.",
            "time_complexity": "Not available",
            "space_complexity": "Not available",
            "potential_bugs": "Not available",
            "edge_cases": "Not available",
            "optimization_suggestions": "Not available",
            "interview_feedback": "Not available",
        },
    )
    return CodeReviewResponse(**result)
