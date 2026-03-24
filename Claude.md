# NutriCard AI — CLAUDE.md

## Project
Mobile-first AI planning assistant. Multi-agent backend with iOS as primary client.
Manager agent orchestrates specialized sub-agents and returns a single unified response.

## Stack
- Backend: Python, PydanticAI, Langfuse, Amazon Bedrock
- Mobile: Swift / SwiftUI (primary)
- Web: React + Tailwind CSS (secondary)
- Infra: AWS, Terraform

## Repo Structure
/src
 /backend  → API, orchestration, agents, memory
/mobile   → iOS Swift app
/frontend → React web app
/infra    → Terraform / AWS
/docs     → Architecture notes (this docs will revivew by when change completes. my custom agent user-arch-agent responsible for this)

## Agent Architecture
- Manager agent: sole orchestrator, owns final user response
- Sub-agents: Budget, Health, Meetings, Lifestyle, Memory
- Sub-agents return structured output only — no direct user communication
- Each sub-agent has a single, narrow responsibility

## Non-Negotiable Rules
1. Follow official docs: PydanticAI, Langfuse, AWS Bedrock, Terraform, SwiftUI
2. Never invent SDK behaviors or undocumented patterns
3. Every meaningful agent step must emit a Langfuse trace
4. No hardcoded credentials — use AWS Secrets Manager or env vars
5. Keep agent context efficient; avoid bloated prompts

## Memory
Use AWS AgentCore-compatible memory. Store only: preferences, goal history, planning patterns.
Do not over-store. Keep memory logic separate from orchestration.

## MVP Constraints
- No unnecessary microservices
- No premature infrastructure complexity
- Mobile experience over web in every tradeoff
- Prefer simple, replaceable components

## Summary.md
-after changes you must be write summary.md file source folder of project
-this md file must contains clear explanation about code changes
-writen language is must be turkish just summary.md other way we communicate english

