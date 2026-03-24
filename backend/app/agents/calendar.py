"""
Calendar Agent — converts plans into structured calendar events (future integration ready).
Returns CalendarOutput with fully typed CalendarEvent list.
Source: https://ai.pydantic.dev/agents/
        https://ai.pydantic.dev/dependencies/
"""
import os
from datetime import datetime

from pydantic_ai import Agent, RunContext

from .deps import AgentDeps
from .models import CalendarOutput

_MODEL = os.getenv("MODEL_ID", "us.anthropic.claude-sonnet-4-6-20250514-v1:0")

calendar_agent = Agent(
    f"bedrock:{_MODEL}",
    deps_type=AgentDeps,
    output_type=CalendarOutput,
    instructions=(
        "You are a calendar scheduling assistant. "
        "Convert plans, meals, workouts, and tasks into structured calendar events. "
        "Each event must have a precise start_time, end_time, title, and event_type. "
        "Use ISO 8601 datetime format. Assign realistic time slots. "
        "event_type must be one of: meal, workout, meeting, task, reminder. "
        "Always return structured output. Use markdown_summary for a readable overview."
    ),
)


@calendar_agent.system_prompt
def calendar_system_prompt(ctx: RunContext[AgentDeps]) -> str:
    p = ctx.deps.user_profile
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"User: {p.name}"
        + f"\nToday's date: {today}"
        + (f"\nGoals: {', '.join(p.fitness_goals)}" if p.fitness_goals else "")
    )
