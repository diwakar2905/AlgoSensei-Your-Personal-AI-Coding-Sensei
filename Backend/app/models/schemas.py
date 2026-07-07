from typing import Any
from pydantic import BaseModel, Field, model_validator


class CodeInput(BaseModel):
    problem: str
    code: str
    language: str
    topic: str = "mixed"


class ChatMessage(BaseModel):
    role: str
    parts: list[dict]


class ChatInput(BaseModel):
    history: list[ChatMessage]
    problem: str
    code: str
    language: str
    topic: str = "mixed"


class AIResponse(BaseModel):
    model_config = {"populate_by_name": True}
    sender: str = Field(..., alias="from")
    text: str


class CodeReviewInput(BaseModel):
    code: str
    language: str
    focus_area: str = "mixed"


class CodeReviewResponse(BaseModel):
    model_config = {"populate_by_name": True}
    sender: str = Field(default="ai", alias="from")
    code_quality_analysis: str
    time_complexity: str
    space_complexity: str
    potential_bugs: str
    edge_cases: str
    optimization_suggestions: str
    interview_feedback: str

    @model_validator(mode="before")
    @classmethod
    def format_lists_to_strings(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for field in ["potential_bugs", "edge_cases", "optimization_suggestions"]:
                val = data.get(field)
                if isinstance(val, list):
                    # Join with bullet points
                    data[field] = "\n".join(f"- {item}" for item in val)
        return data


class InterviewStartInput(BaseModel):
    domain: str
    difficulty: str = "intermediate"


class InterviewTurnInput(BaseModel):
    domain: str
    difficulty: str = "intermediate"
    latest_answer: str
    history: list[ChatMessage] = Field(default_factory=list)
    round_number: int = 1


class InterviewStartResponse(BaseModel):
    model_config = {"populate_by_name": True}
    sender: str = Field(default="ai", alias="from")
    question: str
    score: int = 0
    round_number: int = 1


class InterviewTurnResponse(BaseModel):
    model_config = {"populate_by_name": True}
    sender: str = Field(default="ai", alias="from")
    evaluation: str
    follow_up: str
    score: int
    round_number: int
    should_end: bool = False


class InterviewFinalInput(BaseModel):
    domain: str
    difficulty: str = "intermediate"
    history: list[ChatMessage] = Field(default_factory=list)


class InterviewFinalResponse(BaseModel):
    model_config = {"populate_by_name": True}
    sender: str = Field(default="ai", alias="from")
    overall_score: int
    verdict: str
    strengths: list[str]
    weaknesses: list[str]
    next_steps: list[str]

    @model_validator(mode="before")
    @classmethod
    def format_strings_to_lists(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for field in ["strengths", "weaknesses", "next_steps"]:
                val = data.get(field)
                if isinstance(val, str):
                    # Split lines or bullets, or wrap in a list
                    items = [item.strip("- ").strip() for item in val.split("\n") if item.strip()]
                    data[field] = items if items else [val]
        return data
