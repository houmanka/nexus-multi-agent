# Nexus Multi-Agent — Banking Loan Assessment

A demo project for a two-article series on **Temporal Nexus**.

## What This Demonstrates

How Temporal Nexus enables independent AI teams to collaborate across namespace boundaries in an enterprise banking context — without coupling, without losing durability, and without any team knowing what's inside another team's implementation.

## The Story

A bank mortgage lender (John Doe) submits a loan application. This triggers a `LoanAssessmentWorkflow` in the orchestrator namespace, which fans out to three independent teams via Nexus. Each team owns their own namespace, their own worker, and their own AI strategy. The orchestrator knows none of that — it only knows the shared contract.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  loan-orchestrator-ns  /  LoanAssessmentWorkflow        │
│  Triggered by: FastAPI endpoint (John Doe submits form) │
└──────────┬──────────────┬──────────────┬────────────────┘
           │ Nexus        │ Nexus        │ Nexus
           ▼              ▼              ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ qualification-ns │  │   income-ns      │  │serviceability-ns │
│                  │  │                  │  │                  │
│  Pure math       │  │  Ollama          │  │  Claude API      │
│  No AI           │  │  Llama 3.2 3B    │  │  (Anthropic)     │
│                  │  │  (local/on-prem) │  │  (hosted)        │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

## The Three Teams

| Team | Namespace | Task Queue | AI | Responsibility |
|---|---|---|---|---|
| Qualification | `qualification-ns` | `qualification-task-queue` | None | LTV ratio + income threshold check — pure math |
| Income Verification | `income-ns` | `income-task-queue` | Ollama / Llama 3.2 3B | Parses payslip text locally — PII never leaves infrastructure |
| Serviceability | `serviceability-ns` | `serviceability-task-queue` | Claude API | Assesses repayment capacity — receives sanitised numbers only |

**Why two different LLMs?** The income team cannot send payslip data to an external API (PII, APRA compliance). They run inference locally. The serviceability team only receives sanitised financial figures — cloud is acceptable. The orchestrator knows neither. That's encapsulation.

## Shared Contract

`shared/services.py` — the only file all teams share. In a real enterprise this would be a versioned package in its own repo, owned by the handler teams. Contains:
- `LoanApplication` dataclass (orchestrator input)
- `QualificationResult`, `IncomeVerificationResult`, `ServiceabilityResult` dataclasses
- `QualificationService`, `IncomeVerificationService`, `ServiceabilityService` Nexus service classes

## Article Series

**Article 1 — Sync Nexus**
*"Multi-Agent AI in Banking: How Temporal Nexus Keeps Your Teams Independent"*
Covers: the problem, Nexus architecture, qualification + income verification end-to-end.

**Article 2 — Async Nexus + Human in the Loop**
Covers: serviceability as an async operation, durable handles, workflow pausing for loan officer sign-off via Temporal Signal (APRA compliance angle).

## Requirements

- [uv](https://docs.astral.sh/uv/)
- [Temporal CLI](https://docs.temporal.io/cli)
- [Ollama](https://ollama.com) with `llama3.2:3b` pulled
- Anthropic API key

## Project Structure

```
├── shared/
│   └── services.py              # Shared Nexus contracts — all teams import from here
├── qualification_team/          # qualification-ns worker + handler
├── income_team/                 # income-ns worker + handler + Ollama provider
├── serviceability_team/         # serviceability-ns worker + handler + Claude provider
├── loan_orchestrator/           # loan-orchestrator-ns workflow + worker
└── trigger.py                   # FastAPI endpoint — John Doe submits loan application
```

## Core Thesis

> *"Nexus isn't an AI framework. It's the enterprise boundary that lets your AI teams evolve independently. Some teams use LLMs, some don't, some use different ones — the orchestrator never knows and never needs to."*
