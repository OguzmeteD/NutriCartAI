"""
Chat router — POST /chat endpoint.
Authenticated via Bearer token; delegates to the multi-agent pipeline.
"""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.agents import AgentUserProfile, ManagerResponse, run_pipeline
from app.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    # Optional profile fields — enrich AgentUserProfile beyond what auth provides.
    # These will be replaced by the memory layer once it is implemented.
    name: Optional[str] = None
    age: Optional[int] = None
    dietary_restrictions: list[str] = []
    fitness_goals: list[str] = []
    monthly_budget: Optional[float] = None


class ChatResponse(BaseModel):
    session_id: str
    response: ManagerResponse


@router.post("", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    current_user: dict = Depends(get_current_user),
) -> ChatResponse:
    """
    Send a message to the NutriCard AI coordinator.

    The manager agent decides which specialist agents to invoke
    (planner, budget, sport_coach, calendar) and returns a unified response.
    """
    session_id = str(uuid.uuid4())

    user_profile = AgentUserProfile(
        user_id=current_user["user_id"],
        name=body.name or current_user.get("email", "User"),
        age=body.age,
        dietary_restrictions=body.dietary_restrictions,
        fitness_goals=body.fitness_goals,
        monthly_budget=body.monthly_budget,
    )

    try:
        result = await run_pipeline(
            user_message=body.message,
            user_profile=user_profile,
            session_id=session_id,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Agent pipeline error: {exc}",
        ) from exc

    return ChatResponse(session_id=session_id, response=result)
