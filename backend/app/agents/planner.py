"""
Planner Agent — creates daily/weekly plans, meal schedules, task lists.
Source: https://ai.pydantic.dev/agents/
        https://ai.pydantic.dev/dependencies/
"""
import os

from pydantic_ai import Agent, RunContext

from .deps import AgentDeps
from .models import PlannerOutput

_MODEL = os.getenv("MODEL_ID", "us.anthropic.claude-sonnet-4-6-20250514-v1:0")

planner_agent = Agent(
    f"bedrock:{_MODEL}",
    deps_type=AgentDeps,
    output_type=PlannerOutput,
    instructions=(
        "You are a personal planning expert. "
        "Create practical daily/weekly plans, meal schedules, and task lists "
        "tailored to the user's goals, dietary restrictions, and preferences. "
        "Always return structured output. Use markdown_summary for a readable markdown plan."
    ),
)


@planner_agent.system_prompt
def planner_system_prompt(ctx: RunContext[AgentDeps]) -> str:
    p = ctx.deps.user_profile
    restrictions = ", ".join(p.dietary_restrictions) if p.dietary_restrictions else "none"
    goals = ", ".join(p.fitness_goals) if p.fitness_goals else "not specified"
    return (
        f"User: {p.name}"
        + (f", age {p.age}" if p.age else "")
        + f"\nDietary restrictions: {restrictions}"
        + f"\nGoals: {goals}"
        + (f"\nMonthly budget: ${p.monthly_budget:.0f}" if p.monthly_budget else "")
    )
