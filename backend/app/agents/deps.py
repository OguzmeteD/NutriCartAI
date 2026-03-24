"""
Shared dependency types for all NutriCard AI agents.
Source: https://ai.pydantic.dev/dependencies/
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentUserProfile:
    """
    User context passed through every agent run.
    Separate from app.models.user.UserProfile (auth model).
    Will be extended by the memory layer in future iterations.
    """
    user_id: str
    name: str
    age: Optional[int] = None
    dietary_restrictions: list[str] = field(default_factory=list)
    fitness_goals: list[str] = field(default_factory=list)
    monthly_budget: Optional[float] = None
    # Flexible dict for future memory-layer preferences
    preferences: dict = field(default_factory=dict)


@dataclass
class AgentDeps:
    """
    Shared dependencies injected into all agents via RunContext.
    Sub-agents receive the same deps instance forwarded from the manager tool call.
    Source: https://ai.pydantic.dev/dependencies/#accessing-dependencies
    """
    user_profile: AgentUserProfile
    session_id: str
