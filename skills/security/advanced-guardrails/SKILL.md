---
name: advanced-guardrails
description: LLM guardrails with NeMo, Guardrails AI, and OpenAI. Input/output rails, hallucination prevention, fact-checking, toxicity detection, red-teaming patterns. Use when building LLM guardrails, safety checks, or red-team workflows.
version: 1.0.0
tags: [guardrails, nemo, safety, hallucination, factuality, red-teaming, colang, 2026]
context: fork
agent: ai-safety-auditor
author: SkillForge
user-invocable: false
---

# Advanced Guardrails

Production LLM safety using NeMo Guardrails, Guardrails AI, and OpenAI moderation with red-teaming validation.

> **NeMo Guardrails 2026**: LangChain 1.x compatible, parallel rails execution, OpenTelemetry tracing. **DeepTeam**: 40+ vulnerabilities, OWASP Top 10 alignment.

## Overview

- Implementing input/output validation for LLM applications
- Preventing hallucinations and enforcing factuality
- Detecting and filtering toxic, harmful, or off-topic content
- Restricting LLM responses to specific domains/topics
- PII detection and redaction in LLM outputs
- Red-teaming and adversarial testing of LLM systems
- OWASP Top 10 for LLMs compliance

## Framework Comparison

| Framework | Best For | Key Features |
|-----------|----------|--------------|
| **NeMo Guardrails** | Programmable flows, Colang 2.0 | Input/output rails, fact-checking, dialog control |
| **Guardrails AI** | Validator-based, modular | 100+ validators, PII, toxicity, structured output |
| **OpenAI Guardrails** | Drop-in wrapper | Simple integration, moderation API |
| **DeepTeam** | Red teaming, adversarial | GOAT attacks, multi-turn jailbreaking, vulnerability scanning |

## Quick Reference

### NeMo Guardrails with Guardrails AI Integration

```yaml
# config.yml
models:
  - type: main
    engine: openai
    model: gpt-4o

rails:
  config:
    guardrails_ai:
      validators:
        - name: toxic_language
          parameters:
            threshold: 0.5
            validation_method: "sentence"
        - name: guardrails_pii
          parameters:
            entities: ["phone_number", "email", "ssn", "credit_card"]
        - name: restricttotopic
          parameters:
            valid_topics: ["technology", "support"]
        - name: valid_length
          parameters:
            min: 10
            max: 500

  input:
    flows:
      - guardrailsai check input $validator="guardrails_pii"
      - guardrailsai check input $validator="competitor_check"

  output:
    flows:
      - guardrailsai check output $validator="toxic_language"
      - guardrailsai check output $validator="restricttotopic"
      - guardrailsai check output $validator="valid_length"
```

### Colang 2.0 Fact-Checking Rails

```colang
define flow answer question with facts
  """Enable fact-checking for RAG responses."""
  user ...
  $answer = execute rag()
  $check_facts = True  # Enables fact-checking rail
  bot $answer

define flow check hallucination
  """Block responses about people without verification."""
  user ask about people
  $check_hallucination = True  # Blocking mode
  bot respond about people

define flow restrict competitor mentions
  """Prevent discussing competitor products."""
  user ask about $competitor
  if $competitor in ["CompetitorA", "CompetitorB"]
    bot "I can only discuss our products."
  else
    bot respond normally
```

### Guardrails AI Validators

```python
from guardrails import Guard
from guardrails.hub import (
    ToxicLanguage,
    DetectPII,
    RestrictToTopic,
    ValidLength,
    ResponseEvaluator,
)

# Create guard with multiple validators
guard = Guard().use_many(
    ToxicLanguage(threshold=0.5, on_fail="filter"),
    DetectPII(
        pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "SSN"],
        on_fail="fix"  # Redacts PII
    ),
    RestrictToTopic(
        valid_topics=["technology", "customer support"],
        invalid_topics=["politics", "religion"],
        on_fail="refrain"
    ),
    ValidLength(min=10, max=500, on_fail="reask"),
)

# Validate LLM output
result = guard(
    llm_api=openai.chat.completions.create,
    model="gpt-4o",
    messages=[{"role": "user", "content": user_input}],
)

if result.validation_passed:
    return result.validated_output
else:
    return "I cannot respond to that request."
```

### DeepTeam Red Teaming

```python
from deepteam import red_team
from deepteam.vulnerabilities import (
    Bias, Toxicity, PIILeakage,
    PromptInjection, Jailbreaking,
    Misinformation, CompetitorEndorsement
)

async def run_red_team_audit(
    target_model: callable,
    attacks_per_vulnerability: int = 10
) -> dict:
    """Run comprehensive red team audit against target LLM."""
    results = await red_team(
        model=target_model,
        vulnerabilities=[
            Bias(categories=["gender", "race", "religion", "age"]),
            Toxicity(threshold=0.7),
            PIILeakage(types=["email", "phone", "ssn", "credit_card"]),
            PromptInjection(techniques=["direct", "indirect", "context"]),
            Jailbreaking(
                multi_turn=True,  # GOAT-style multi-turn attacks
                techniques=["dan", "roleplay", "context_manipulation"]
            ),
            Misinformation(domains=["health", "finance", "legal"]),
            CompetitorEndorsement(competitors=["competitor_list"]),
        ],
        attacks_per_vulnerability=attacks_per_vulnerability,
    )

    return {
        "total_attacks": results.total_attacks,
        "successful_attacks": results.successful_attacks,
        "attack_success_rate": results.successful_attacks / results.total_attacks,
        "vulnerabilities": [
            {
                "type": v.type,
                "severity": v.severity,
                "successful_prompts": v.successful_prompts[:3],
                "mitigation": v.suggested_mitigation,
            }
            for v in results.vulnerabilities
        ],
    }
```

## OWASP Top 10 for LLMs 2025 Mapping

| OWASP LLM Risk | Guardrail Solution |
|----------------|-------------------|
| **LLM01: Prompt Injection** | NeMo input rails, Guardrails AI validators |
| **LLM02: Insecure Output** | Output rails, structured validation, sanitization |
| **LLM03: Training Data Poisoning** | N/A (training-time concern) |
| **LLM04: Model Denial of Service** | Rate limiting, token budgets, timeout rails |
| **LLM05: Supply Chain Vulnerabilities** | Dependency scanning, model provenance |
| **LLM06: Sensitive Info Disclosure** | PII detection, context separation, output filtering |
| **LLM07: Insecure Plugin Design** | Tool validation, permission boundaries |
| **LLM08: Excessive Agency** | Human-in-loop rails, action confirmation |
| **LLM09: Overreliance** | Factuality checking, confidence thresholds |
| **LLM10: Model Theft** | N/A (infrastructure concern) |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER trust LLM output without validation
response = llm.generate(prompt)
return response  # Raw, unvalidated output!

# NEVER skip input sanitization
user_input = request.json["message"]
llm.generate(user_input)  # Prompt injection risk!

# NEVER use single validation layer
if not is_toxic(output):  # Only one check
    return output

# ALWAYS use layered validation
guard = Guard().use_many(
    ToxicLanguage(threshold=0.5),
    DetectPII(on_fail="fix"),
    ValidLength(max=500),
)

# ALWAYS validate both input and output
input_result = input_guard.validate(user_input)
if not input_result.validation_passed:
    return "Invalid input"

llm_output = llm.generate(input_result.validated_output)

output_result = output_guard.validate(llm_output)
return output_result.validated_output
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Framework choice | NeMo for flows, Guardrails AI for validators |
| Toxicity threshold | 0.5 for content apps, 0.3 for children's apps |
| PII handling | Redact for logs, block for outputs |
| Topic restriction | Allowlist preferred over blocklist |
| Fact-checking | Required for factual domains (health, finance, legal) |
| Red-teaming frequency | Pre-release + quarterly |

## Detailed Documentation

| Resource | Description |
|----------|-------------|
| [references/nemo-guardrails.md](references/nemo-guardrails.md) | NeMo Guardrails with Colang 2.0 |
| [references/guardrails-ai.md](references/guardrails-ai.md) | Guardrails AI validators and patterns |
| [references/openai-guardrails.md](references/openai-guardrails.md) | OpenAI Moderation API integration |
| [references/factuality-checking.md](references/factuality-checking.md) | Hallucination detection and grounding |
| [references/red-teaming.md](references/red-teaming.md) | DeepTeam and adversarial testing |
| [templates/nemo-config.yaml](templates/nemo-config.yaml) | Production NeMo configuration |
| [templates/rails-pipeline.py](templates/rails-pipeline.py) | Complete guardrails pipeline |

## Related Skills

- `llm-safety-patterns` - Context separation and attribution
- `llm-evaluation` - Quality assessment and hallucination detection
- `input-validation` - Request sanitization patterns
- `owasp-top-10` - Web security fundamentals

## Capability Details

### nemo-guardrails
**Keywords:** NeMo, guardrails, rails, Colang, dialog flow, input rails, output rails
**Solves:**
- Configure NeMo Guardrails for LLM safety
- Implement Colang 2.0 dialog flows
- Create input/output validation rails

### guardrails-ai-validators
**Keywords:** Guardrails AI, validator, PII, toxicity, topic restriction, structured output
**Solves:**
- Use Guardrails AI validators for output validation
- Detect and redact PII from LLM responses
- Restrict LLM to specific topics

### factuality-checking
**Keywords:** fact-check, hallucination, grounding, RAG verification, NLI
**Solves:**
- Verify LLM claims against source documents
- Detect hallucinations in generated content
- Implement grounding checks for RAG

### red-teaming
**Keywords:** red team, adversarial, jailbreak, GOAT, prompt injection, DeepTeam
**Solves:**
- Run adversarial testing on LLM systems
- Detect jailbreaking vulnerabilities
- Test prompt injection resistance

### owasp-llm-compliance
**Keywords:** OWASP LLM, LLM security, LLM vulnerabilities, LLM Top 10
**Solves:**
- Implement OWASP Top 10 for LLMs mitigations
- Audit LLM systems for security compliance
- Design secure LLM architectures
