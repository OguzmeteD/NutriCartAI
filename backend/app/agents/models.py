"""
Structured output models for all NutriCard AI agents.
Sub-agents return these Pydantic models; manager merges them into ManagerResponse.
Source: https://ai.pydantic.dev/agents/ (output_type section)
"""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Sub-agent outputs
# ---------------------------------------------------------------------------

class PlannerOutput(BaseModel):
    """Planner agent structured output — daily/weekly plan + meal schedule."""
    markdown_summary: str
    tasks: list[str]
    meal_plan: list[str] = []
    weekly_schedule: list[str] = []


class BudgetOutput(BaseModel):
    """Budget agent structured output — cost estimates and recommendations."""
    markdown_summary: str
    estimated_total_cost: Optional[float] = None
    budget_breakdown: dict[str, float] = {}
    recommendations: list[str] = []
    within_budget: Optional[bool] = None


class SportCoachOutput(BaseModel):
    """Sport coach agent structured output — workout plan + nutrition tips."""
    markdown_summary: str
    workout_plan: list[str] = []
    fitness_tips: list[str] = []
    nutrition_advice: Optional[str] = None
    weekly_targets: dict[str, str] = {}


# ---------------------------------------------------------------------------
# Calendar agent — fully structured (future calendar integration ready)
# ---------------------------------------------------------------------------

EventType = Literal["meal", "workout", "meeting", "task", "reminder"]


class CalendarEvent(BaseModel):
    """A single calendar event with all fields required for calendar APIs."""
    title: str
    start_time: datetime
    end_time: datetime
    event_type: EventType
    description: Optional[str] = None
    location: Optional[str] = None
    recurrence: Optional[str] = None  # e.g. "RRULE:FREQ=DAILY"


class CalendarOutput(BaseModel):
    """Calendar agent structured output — list of calendar events."""
    events: list[CalendarEvent] = []
    markdown_summary: str


# ---------------------------------------------------------------------------
# Manager final response
# ---------------------------------------------------------------------------

class ManagerResponse(BaseModel):
    """
    Final unified response returned by the manager agent to the API caller.
    agents_consulted lists which sub-agents were actually invoked.
    """
    final_answer: str
    agents_consulted: list[str]
    planner: Optional[PlannerOutput] = None
    budget: Optional[BudgetOutput] = None
    sport_coach: Optional[SportCoachOutput] = None
    calendar: Optional[CalendarOutput] = None
