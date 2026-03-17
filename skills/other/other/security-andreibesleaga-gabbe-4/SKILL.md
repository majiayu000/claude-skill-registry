---
name: ai-safety-guardrails
description: Security-by-design for AI (Prompt Injection defense, Hallucination checks, PII filters).
role: prod-ethicist
triggers:
  - ai safety
  - guardrails
  - prompt injection
  - hallucination
  - pii filter
  - jailbreak
---

# ai-safety-guardrails Skill

This skill protects the system from its own AI.

## 1. Input Guardrails (Defense)
- **Prompt Injection**: "Ignore previous instructions".
  - *Defense*: Delimiters (XML tags), "Sandwich Defense" (System Prompt + User Input + System Reminder).
- **Jailbreaks**: "Do this in 'DAN' mode".
  - *Defense*: Pattern matching for known jailbreak signatures.
- **PII Scrubbing**: Regex scan input for SSN, Credit Cards, Emails *before* sending to LLM.

## 2. Output Guardrails (Verification)
- **Hallucination Check**: "Self-Consistency" (Ask 3 times, take majority).
- **Tone Policing**: Sentiment analysis on output. (Block Toxic/Aggressive responses).
- **Format Validation**: Ensure JSON is valid JSON.

## 3. Libraries & Tools
- **NeMo Guardrails (NVIDIA)**
- **Guardrails AI (Python)**
- **Rebertha (PII)**

## 4. System Design
- **Human in the Loop (HITL)**: For high-stakes actions (Transfer Money), AI *proposes*, Human *approves*.
- **Least Privilege**: The Agent's API Token should NOT have admin access.
