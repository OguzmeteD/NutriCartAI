"""
Sport Coach Agent — workout plans, fitness tips, nutrition advice.
Source: https://ai.pydantic.dev/agents/
        https://ai.pydantic.dev/dependencies/
"""
import os

from pydantic_ai import Agent, RunContext

from .deps import AgentDeps
from .models import SportCoachOutput

_MODEL = os.getenv("MODEL_ID", "us.anthropic.claude-sonnet-4-6-20250514-v1:0")

sport_coach_agent = Agent(
    f"bedrock:{_MODEL}",
    deps_type=AgentDeps,
    output_type=SportCoachOutput,
    instructions=(
        "You are a professional sport coach and fitness expert. "
        "Create personalized workout plans, set weekly fitness targets, "
        "and give nutrition advice aligned with the user's fitness goals. "
        "Adapt recommendations to the user's age and any physical limitations. "
        "Always return structured output. Use markdown_summary for a readable summary."
    ),
)


@sport_coach_agent.system_prompt
def sport_coach_system_prompt(ctx: RunContext[AgentDeps]) -> str:
    p = ctx.deps.user_profile
    goals = ", ".join(p.fitness_goals) if p.fitness_goals else "general fitness"
    return (
        f"User: {p.name}"
        + (f", age {p.age}" if p.age else "")
        + f"\nFitness goals: {goals}"
        + (f"\nDietary restrictions: {', '.join(p.dietary_restrictions)}" if p.dietary_restrictions else "")
    )
