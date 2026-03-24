"""
NutriCard AI Agent Pipeline — entry point for the full multi-agent system.
Sets up Langfuse tracing via OpenTelemetry (logfire → OTLP → Langfuse).

Required env vars (in .env):
    MODEL_ID              — Bedrock model ID
    LANGFUSE_PUBLIC_KEY   — Langfuse project public key
    LANGFUSE_SECRET_KEY   — Langfuse project secret key
    LANGFUSE_HOST         — Langfuse host (default: https://cloud.langfuse.com)

Source: https://ai.pydantic.dev/logfire/#using-opentelemetry
        https://ai.pydantic.dev/multi-agent-applications/#agent-delegation
"""
import base64
import os

import logfire

from .deps import AgentDeps, AgentUserProfile
from .manager import manager_agent
from .models import ManagerResponse


def configure_langfuse_tracing() -> None:
    """
    Wire PydanticAI instrumentation to Langfuse via OTel.
    Call once at app startup (called from main.py lifespan).
    Source: https://ai.pydantic.dev/logfire/#using-opentelemetry
    """
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
    host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    if not public_key or not secret_key:
        return  # tracing disabled — no credentials

    credentials = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{host}/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {credentials}"

    logfire.configure(send_to_logfire=False)
    logfire.instrument_pydantic_ai()  # auto-traces all agents + tools


async def run_pipeline(
    user_message: str,
    user_profile: AgentUserProfile,
    session_id: str,
) -> ManagerResponse:
    """
    Run the full NutriCard AI pipeline for a single user turn.

    Args:
        user_message:  Raw text from the user.
        user_profile:  Agent-layer user profile (goals, budget, restrictions).
        session_id:    Unique session identifier (used in traces).

    Returns:
        ManagerResponse with final_answer + structured sub-agent outputs.
    """
    deps = AgentDeps(user_profile=user_profile, session_id=session_id)
    result = await manager_agent.run(user_message, deps=deps)
    return result.output
