"""
Budget Agent — estimates costs, tracks spending, gives budget recommendations.
Source: https://ai.pydantic.dev/agents/
        https://ai.pydantic.dev/dependencies/
"""
import os

from pydantic_ai import Agent, RunContext

from .deps import AgentDeps
from .models import BudgetOutput

_MODEL = os.getenv("MODEL_ID", "us.anthropic.claude-sonnet-4-6-20250514-v1:0")

budget_agent = Agent(
    f"bedrock:{_MODEL}",
    deps_type=AgentDeps,
    output_type=BudgetOutput,
    instructions=(
        "You are a personal finance and budgeting expert specialized in nutrition "
        "and healthy lifestyle costs. "
        "Estimate costs, suggest budget breakdowns, and flag whether plans are "
        "within the user's budget. Provide actionable money-saving tips. "
        "Always return structured output. Use markdown_summary for a readable summary."
    ),
)


@budget_agent.system_prompt
def budget_system_prompt(ctx: RunContext[AgentDeps]) -> str:
    p = ctx.deps.user_profile
    budget_line = f"${p.monthly_budget:.0f}/month" if p.monthly_budget else "not set"
    return (
        f"User: {p.name}"
        + f"\nMonthly budget: {budget_line}"
        + (f"\nGoals: {', '.join(p.fitness_goals)}" if p.fitness_goals else "")
    )
