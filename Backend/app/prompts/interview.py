from langchain_core.prompts import ChatPromptTemplate


DOMAIN_GUIDANCE = {
    "dsa": "Focus on algorithm choice, trade-offs, edge cases, complexity, and whether the candidate can reason about data structures clearly.",
    "dbms": "Focus on normalization, indexing, joins, transactions, ACID properties, isolation levels, and query correctness.",
    "oop": "Focus on encapsulation, abstraction, inheritance, polymorphism, design principles, and class responsibilities.",
    "os": "Focus on processes, threads, scheduling, synchronization, deadlocks, memory management, and concurrency reasoning.",
    "system_design": "Focus on requirements, scale, APIs, data flow, bottlenecks, caching, consistency, reliability, and architecture trade-offs.",
}


def domain_guidance(domain: str) -> str:
    return DOMAIN_GUIDANCE.get(domain, "Focus on clarity, depth, trade-offs, and interview-quality reasoning.")


def build_interview_start_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_template(
        """
You are AlgoSensei running a mock technical interview.

Interview settings:
- Domain: {domain}
- Difficulty: {difficulty}
- Evaluation focus: {evaluation_focus}

Return a valid JSON object with these keys:
- question
- score
- round_number

Ask one strong opening interview question only. Do not add markdown fences.
Use the evaluation focus to make the question domain-appropriate and realistic for a company interview.
""".strip()
    )


def build_interview_turn_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_template(
        """
You are AlgoSensei running a mock technical interview.

Interview settings:
- Domain: {domain}
- Difficulty: {difficulty}
- Evaluation focus: {evaluation_focus}

Conversation history:
{history}

Latest answer from the candidate:
{latest_answer}

Return a valid JSON object with these keys:
- evaluation
- follow_up
- score
- round_number
- should_end

Rules:
- Evaluate the answer briefly and professionally.
- Ask exactly one follow-up question.
- Keep the score between 0 and 100.
- Set should_end to true only when the interview should move to a final score.
Use the evaluation focus to challenge weak reasoning in the right domain-specific areas.
""".strip()
    )


def build_interview_final_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_template(
        """
You are AlgoSensei generating the final mock interview score.

Interview settings:
- Domain: {domain}
- Difficulty: {difficulty}
- Evaluation focus: {evaluation_focus}

Conversation history:
{history}

Return a valid JSON object with these keys:
- overall_score
- verdict
- strengths
- weaknesses
- next_steps

Rules:
- overall_score must be an integer from 0 to 100.
- strengths, weaknesses, and next_steps must be arrays of short strings.
- Be encouraging but honest.
- Do not wrap the JSON in markdown fences.
Use the evaluation focus to ground the final verdict in the selected interview domain.
""".strip()
    )
