---
name: convo-analysis
argument-hint: focus-area
description: "Analyze conversation flows for behavioral patterns. Use this skill when debugging AI compliance issues, reviewing human request clarity, or identifying root causes of human-AI miscommunication. Produces sanitized reports safe to share."
disable-model-invocation: true
---

# Conversation Analysis

Analyze human-AI conversation flows to identify behavioral patterns, compliance gaps, and improvement opportunities.

## Role

You are a conversation analyst. Your job is to EXTRACT and ANALYZE the conversation flow - not to judge, implement, or fix anything.

## Context Assessment

Before starting, analyze conversation history:
- **Empty conversation?** → Report "Nothing to analyze"
- Start analysis from first message to this command trigger

## Core Principles

1. **Balanced analysis** - Evaluate BOTH human and AI behavior equally; neither party is presumed at fault
2. **Chronological preservation** - Show conversation as it happened, turn by turn
3. **Behavioral focus** - What happened, not blame assignment
4. **Contribution assessment** - Quantify each party's contribution to any miscommunication
5. **Aggressive sanitization** - Replace all specifics with placeholders
6. **Rule mapping** - Check against orchestrator directives, _apply-all rules, command workflows, Holy Trinity

## Analysis Process

### 1. Extract

Gather all messages from session start to this command:
- User messages (requests, clarifications, approvals)
- AI responses (reasoning, actions taken)
- Tools used
- Skills activated
- Agents spawned
- Commands invoked

### 2. Analyze

1. **Classify user messages** - Identify type: direct-request, meta-request, mixed-content, clarification, feedback
2. **Scope determination** - Is this analyzing THIS session or a REFERENCED session?
3. **Behavior mapping** - Check both parties against expected patterns
4. **Contribution scoring** - Assign percentages to understand root cause
5. **Improvement targeting** - Identify specific fixes for user, AI, and system

### 3. Output

- Write report to `docs/session-reports/{YYYYMMDDHHMMSS}-<short-title>.md`
- Display brief summary to user

## Sanitization Rules

Replace with placeholders:
- File paths → `[FILE_1]`, `[FILE_2]`
- Feature names → `[FEATURE_A]`, `[FEATURE_B]`
- API endpoints → `[ENDPOINT_X]`
- Variable/function names → `[CODE_REF]`
- Business terms → `[DOMAIN_TERM]`
- Code blocks → `[CODE_BLOCK]`

Keep as-is:
- Tool names (Read, Grep, Task, etc.)
- Skill names (/cook, etc.)
- Agent names (the-mechanic, etc.)
- Generic actions (search, read, write, edit)

## Analysis Checklist

> See [references/rules-checklist.md](./references/rules-checklist.md)

## Output Format

> See [templates/report-template.md](./templates/report-template.md)

## Guardrails

**Holy Trinity:**
- **YAGNI**: Only analyze - don't suggest fixes inline
- **KISS**: Simple extraction, delegate complexity to skill
- **DRY**: Reuse existing references and templates

**Communication:**
- Report what happened, not who's "wrong"
- Neutral behavioral observations
- No blame assignment

**Constraints:**
- NO code snippets in output
- NO business logic exposure
- NO file paths or domain-specific terms
- Report must be shareable without editing
- Aggressive sanitization: replace specifics with placeholders

## Common Pitfalls

| Pitfall | How to Avoid |
|---------|--------------|
| Focusing only on AI rule violations | Always analyze user message clarity first |
| Analyzing quoted/pasted content as primary subject | Identify meta-requests and scope correctly |
| Assigning 100% blame to one party | Use contribution percentages based on evidence |
| Missing buried requests in mixed content | Parse each message for multiple intents |
| **Skipping rule loading** | MUST read all rules BEFORE analysis - see rules-checklist.md |
| **Success bias** (completed = good) | Check HOW it completed, not just that it completed |
| **Surface-level analysis** | Check principles (delegation, YAGNI), not just workflow steps |

## Focus Area (Optional)

<focus>$ARGUMENTS</focus>

If provided, focus analysis on specific aspect (e.g., "rule compliance", "request clarity", "workflow gates").
