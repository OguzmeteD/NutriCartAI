"""
Manager Agent — coordinator that routes user requests to sub-agents as tools.
Implements the "agent delegation" pattern from PydanticAI docs.
Source: https://ai.pydantic.dev/multi-agent-applications/#agent-delegation
"""
import os

from pydantic_ai import Agent, RunContext

from .budget import budget_agent
from .calendar import calendar_agent
from .deps import AgentDeps
from .models import (
    BudgetOutput,
    CalendarOutput,
    ManagerResponse,
    PlannerOutput,
    SportCoachOutput,
)
from .planner import planner_agent
from .sport_coach import sport_coach_agent

_MODEL = os.getenv("MODEL_ID", "us.anthropic.claude-sonnet-4-6-20250514-v1:0")

manager_agent = Agent(
    f"bedrock:{_MODEL}",
    deps_type=AgentDeps,
    output_type=ManagerResponse,
    instructions=(
        "You are the NutriCard AI coordinator. "
        "Understand the user's request and delegate to the right specialist agents.\n\n"
        "Available tools:\n"
        "- delegate_to_planner: daily/weekly plans, meals, schedules, tasks\n"
        "- delegate_to_budget: cost estimates, spending, budget advice\n"
        "- delegate_to_sport_coach: workouts, fitness plans, exercise tips\n"
        "- delegate_to_calendar: convert any plan into structured calendar events\n\n"
        "Rules:\n"
        "1. Only call agents that are relevant to the user's request.\n"
        "2. You may call multiple agents if the request spans topics.\n"
        "3. Synthesize all agent responses into a single coherent final_answer in markdown.\n"
        "4. List every agent you called in agents_consulted.\n"
        "5. Never make up information — only use what agents return."
    ),
)


@manager_agent.system_prompt
def manager_system_prompt(ctx: RunContext[AgentDeps]) -> str:
    p = ctx.deps.user_profile
    return f"You are helping {p.name} (session: {ctx.deps.session_id})."


# ---------------------------------------------------------------------------
# Delegation tools — each wraps one sub-agent.
# ctx.usage is forwarded so token usage rolls up to the manager run.
# Source: https://ai.pydantic.dev/multi-agent-applications/#agent-delegation
# ---------------------------------------------------------------------------

@manager_agent.tool
async def delegate_to_planner(
    ctx: RunContext[AgentDeps], user_request: str
) -> PlannerOutput:
    """Delegate planning tasks (meals, schedule, task list) to the Planner Agent."""
    result = await planner_agent.run(user_request, deps=ctx.deps, usage=ctx.usage)
    return result.output


@manager_agent.tool
async def delegate_to_budget(
    ctx: RunContext[AgentDeps], user_request: str
) -> BudgetOutput:
    """Delegate budget and cost estimation tasks to the Budget Agent."""
    result = await budget_agent.run(user_request, deps=ctx.deps, usage=ctx.usage)
    return result.output


@manager_agent.tool
async def delegate_to_sport_coach(
    ctx: RunContext[AgentDeps], user_request: str
) -> SportCoachOutput:
    """Delegate fitness and workout planning to the Sport Coach Agent."""
    result = await sport_coach_agent.run(user_request, deps=ctx.deps, usage=ctx.usage)
    return result.output


@manager_agent.tool
async def delegate_to_calendar(
    ctx: RunContext[AgentDeps], user_request: str
) -> CalendarOutput:
    """Delegate calendar event creation to the Calendar Agent."""
    result = await calendar_agent.run(user_request, deps=ctx.deps, usage=ctx.usage)
    return result.output
