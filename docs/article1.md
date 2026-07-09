# Article 1 — Multi-Agent AI in Banking: How Temporal Nexus Keeps Your Teams Independent

## Story Setup
- John Doe is a bank mortgage lender submitting a loan application for a customer
- This triggers a LoanAssessmentWorkflow in the orchestrator namespace
- The workflow fans out to three independent teams via Nexus

## The Problem (Why Nexus)
- Teams in a bank are genuinely separate — different data access, different compliance obligations, different AI tooling
- Naive approaches and why they fail:
  - Shared namespace → coupling, compliance nightmare
  - HTTP calls → lose Temporal's durability
  - Direct cross-namespace workflow invocation → breaks encapsulation
- Nexus gives each team a typed contract — callers get a durable API, handlers stay fully encapsulated

## The Shared Contract (services.py)
- Design backwards — start from what each service needs to do its job, not from the input
- `services.py` is the only file all teams share — in production this lives in a versioned package in its own repo, owned by the handler teams
- Three services defined: QualificationService, IncomeVerificationService, ServiceabilityService
- Each service has a dedicated input and result dataclass — orchestrator sends only what each team needs, nothing more

## QualificationService
- Input: `QualificationInput` — loan_amount, property_value, stated_income
- Operation: `qualify`
- Result: `QualificationResult` — is_qualified, reason
- Pure math — LTV ratio + income threshold check, no AI
- Fast and sync — deliberate, shows Nexus connects teams regardless of whether they use AI

## IncomeVerificationService
- Input: `IncomeInput` — stated_income, employment_type, payslip_text
- Operation: `verify`
- Result: `IncomeVerificationResult` — verified_income, employer, employment_type, is_verified
- Uses Ollama / Llama 3.2 3B running locally — payslip contains PII, cannot leave the bank's infrastructure
- Mock provider first, wire Ollama when ready (LLMProvider Protocol pattern — same as DataStore in series 1)

## The Two-LLM Encapsulation Point
- Income team runs local Ollama — APRA compliance, PII never leaves infrastructure
- Serviceability team uses Claude API — receives sanitised numbers only, cloud acceptable
- The orchestrator knows neither — that is the encapsulation argument made concrete
- In a real bank, each team independently procures their AI vendor through their own compliance process

## ServiceabilityService (mentioned, built in Article 2)
- Brief mention of the third service and why it is async — teaser for Article 2

## Article 1 Ends With
- Qualification + Income Verification working end-to-end
- The reader has seen two teams with different AI strategies connected by Nexus
- Forward pointer to Article 2: what happens when the LLM call takes longer than 10 seconds
