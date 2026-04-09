---
name: ai-interface-reviewer
version: 1.0.0
description: Audit AI-powered interfaces against the uxuiprinciples Part V taxonomy — 44 principles covering transparency, trust calibration, human override, consent, agentic workflows, and conversational design. Returns structured findings with severity and remediation. API key optional — enriched output requires uxuiprinciples.com API Access.
author: uxuiprinciples
homepage: https://uxuiprinciples.com
tags:
  - ai-ux
  - llm
  - copilot
  - chatbot
  - agentic
  - transparency
  - trust
env:
  UXUI_API_KEY:
    description: API key from uxuiprinciples.com (pro tier returns all 44 Part V principles with aiSummary and businessImpact)
    required: false
---

```toml
[toolbox.lookup_ai_principle]
description = "Fetch a specific Part V (AI/Specialized) principle by slug. Returns code, aiSummary, businessImpact, tags, and difficulty."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/principles?slug={slug}&include_content=false"]

[toolbox.list_ai_principles]
description = "List all principles in Part V (AI and Specialized Domains). Returns all 44 principles with codes, slugs, and aiSummary fields."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/principles?part=part-5"]
```

## What This Skill Does

You review AI-powered interfaces against the Part V taxonomy: 44 research-backed principles for AI, voice, and agentic interfaces. This covers ground that general UX frameworks do not: what happens when the system can be wrong, when its reasoning is opaque, when it acts autonomously, and when users need to regain control.

Use this skill when the interface being reviewed includes: LLM-generated output, AI suggestions or autocomplete, copilot features, chat interfaces, voice assistants, agentic workflows, or autonomous actions.

For non-AI interfaces, use `uxui-evaluator` (Parts 1-4) instead.

## Part V Framework Structure

Part V (Specialized Domains) is organized into chapters. The AI-relevant chapters are:

### Chapter S.1.1: Voice and Conversational Interfaces
Turn-taking, dialogue structure, context persistence, ambiguity resolution, Grice's maxims.

| Principle Code | Slug | Focus |
|---------------|------|-------|
| S.1.1.01 | `conversational-flow-principle` | Dialogue flow, turn structure, natural conversation patterns |

### Chapter S.1.3: AI and Intelligent Interfaces
The core AI-UX chapter. Transparency, trust calibration, human override, consent, error recovery.

| Principle Code | Slug | Focus |
|---------------|------|-------|
| S.1.3.01 | `ai-transparency` | Communicating AI reasoning and limitations |
| — | `ai-accuracy-communication` | Conveying confidence levels and uncertainty |
| — | `ai-explainability` | Explaining decisions users can understand |
| — | `ai-user-control` | Human override and correction pathways |
| — | `ai-boundary-setting` | Defining and communicating what AI won't do |
| — | `ai-consistency-reliability` | Stable AI behavior and expectation management |
| — | `graceful-ai-ambiguity` | Handling unclear inputs without breaking |
| — | `efficient-ai-correction` | Making corrections fast and frictionless |
| — | `efficient-ai-invocation` | Triggering AI without cognitive overhead |
| — | `efficient-ai-dismissal` | Dismissing AI output without penalty |
| — | `contextual-ai-timing` | Surfacing AI at the right moment |
| — | `contextual-ai-relevance` | Ensuring AI output matches context |
| — | `contextual-ai-help` | Providing help that's actionable, not generic |
| — | `ai-prompt-design` | Input interface design for LLM interactions |
| — | `ai-input-flexibility` | Accepting multiple input modalities |
| — | `ai-navigation-patterns` | Navigation patterns specific to AI interfaces |
| — | `ai-capability-discovery` | Helping users learn what the AI can do |
| — | `ai-capability-disclosure` | Being honest about AI limitations upfront |
| — | `ai-change-notifications` | Communicating when AI behavior changes |
| — | `ai-source-citations` | Citing sources when AI makes factual claims |
| — | `ai-personalization` | Adapting AI behavior to user context |
| — | `ai-context-capture` | Maintaining context across interactions |
| — | `ai-conversation-memory` | Managing memory across sessions |
| — | `ai-data-consent` | User control over data used for AI |
| — | `ai-privacy-expectations` | Setting honest expectations about data use |
| — | `automation-bias-prevention` | Preventing over-reliance on AI output |
| — | `ai-bias-mitigation` | Surfacing and reducing AI bias |
| — | `ai-audit-trails` | Logging AI decisions for accountability |
| — | `ai-action-consequences` | Previewing irreversible AI actions |
| — | `cautious-ai-updates` | Managing AI model updates carefully |
| — | `creative-agency-protection` | Preserving user creative ownership |
| — | `global-ai-controls` | System-level on/off controls for AI features |
| — | `granular-ai-feedback` | Feedback mechanisms at output level |
| — | `cultural-ai-norms` | Adapting AI communication to cultural context |
| — | `perceived-performance-law` | Managing perceived latency in AI responses |

### Chapter S.1.4: Enterprise and Governance
| Principle Code | Slug | Focus |
|---------------|------|-------|
| — | `enterprise-ai-compliance` | Regulatory and compliance requirements |
| — | `enterprise-ai-governance` | Organizational AI oversight |
| — | `enterprise-ai-workflow` | AI integration into enterprise processes |

### Chapter S.1.5: Agentic Interfaces
For interfaces where AI takes autonomous actions on behalf of users.

| Principle Code | Slug | Focus |
|---------------|------|-------|
| — | `agent-collaboration` | Human-agent collaboration patterns |
| — | `agent-memory-patterns` | Memory and context across agent sessions |
| — | `agent-task-handoff` | Transferring tasks between agent and human |

## Interface Type Classification

Before evaluating, classify the AI interface:

| Type | Description | Primary Concern |
|------|-------------|----------------|
| `ai-chat` | Conversational AI, chatbots, LLM chat UI | Conversational flow, memory, ambiguity |
| `copilot` | Inline AI suggestions within existing tools | Invocation, dismissal, context relevance |
| `ai-suggestion` | AI-generated recommendations or autocomplete | Accuracy communication, override, trust |
| `agentic-workflow` | AI that takes autonomous multi-step actions | Action consequences, human override, audit trails |
| `voice-assistant` | Voice-driven AI interface | Conversational flow, feedback, error recovery |
| `ai-enhanced-form` | Forms with AI pre-fill or suggestions | Consent, accuracy, correction |
| `ai-search` | Search with LLM-generated summaries or answers | Source citations, accuracy, transparency |

## Evaluation Workflow

### Step 1: Classify the Interface

Identify the interface type from the description. If multiple types apply (e.g., a copilot with agentic capabilities), pick the dominant type and note others in `interface_note`.

### Step 2: Select Relevant Principles

Based on interface type, prioritize which principle groups to evaluate:

**Every AI interface type — always evaluate these:**
- `ai-transparency` (S.1.3.01): Is the AI nature disclosed?
- `ai-accuracy-communication`: Are confidence levels shown?
- `ai-user-control`: Can users override or correct AI output?
- `efficient-ai-correction`: Is correction fast and low-friction?
- `ai-capability-disclosure`: Are limitations communicated?

**ai-chat specific:**
- `conversational-flow-principle` (S.1.1.01): Turn structure, context persistence
- `ai-conversation-memory`: Cross-session context handling
- `graceful-ai-ambiguity`: Ambiguous input handling
- `ai-context-capture`: Context across a session

**copilot specific:**
- `efficient-ai-invocation`: Trigger friction
- `efficient-ai-dismissal`: Dismissal without penalty
- `contextual-ai-timing`: When AI surfaces suggestions
- `contextual-ai-relevance`: Whether suggestions match context

**agentic-workflow specific:**
- `ai-action-consequences`: Preview before irreversible actions
- `agent-task-handoff`: Human takeover mechanisms
- `agent-memory-patterns`: Context across agent runs
- `ai-audit-trails`: Logging what the agent did and why
- `automation-bias-prevention`: Preventing over-reliance on agent decisions

**ai-suggestion / ai-search specific:**
- `ai-source-citations`: Are claims sourced?
- `ai-bias-mitigation`: Is bias surfaced?
- `automation-bias-prevention`: Is AI output framed as suggestion, not fact?

### Step 3: Enrich with Toolbox (if API key is set)

For each violation found, call `lookup_ai_principle` with the principle slug. Use the returned `aiSummary` and `businessImpact` to populate `message` and `business_impact`.

If calls fail or return non-200, continue with internal knowledge. Set `api_enriched: false`.

### Step 4: Assign Severity

| Severity | When to Use for AI Interfaces |
|----------|-------------------------------|
| `critical` | The violation creates unsafe outcomes: users cannot override AI, AI acts without consent, AI errors are not surfaced, irreversible actions have no preview |
| `warning` | The violation degrades trust or creates friction: AI disclosure is weak, corrections are hard, confidence levels are missing, memory fails unexpectedly |
| `suggestion` | An improvement: better timing, more contextual suggestions, cleaner dismissal, more granular feedback controls |

**AI-specific escalation rule:** Any violation of `ai-action-consequences` or `ai-user-control` that involves irreversible system actions (delete, send, purchase, publish) is automatically `critical`.

### Step 5: Score and Band

Same scoring as `uxui-evaluator`: start at 100, deduct -15 critical, -7 warning, -3 suggestion. Band: 85+ excellent, 65-84 good, 40-64 fair, 0-39 poor.

### Step 6: Output JSON

Return exactly this structure. No prose.

```json
{
  "interface_type": "ai-chat|copilot|ai-suggestion|agentic-workflow|voice-assistant|ai-enhanced-form|ai-search",
  "interface_note": "string or null",
  "overall_score": 0,
  "band": "poor|fair|good|excellent",
  "findings": [
    {
      "id": "finding-1",
      "principle": {
        "code": "S.1.3.01",
        "slug": "ai-transparency",
        "title": "AI Transparency Principle",
        "chapter": "AI and Intelligent Interfaces"
      },
      "severity": "critical|warning|suggestion",
      "message": "Specific violation description.",
      "remediation": "Concrete fix.",
      "business_impact": "From principle data or null."
    }
  ],
  "strengths": [
    {
      "principle": {
        "code": "string",
        "slug": "string",
        "title": "string"
      },
      "message": "What the interface does well."
    }
  ],
  "trust_assessment": {
    "disclosure": "clear|weak|absent",
    "override_path": "clear|friction|absent",
    "accuracy_signals": "present|partial|absent",
    "consent": "explicit|implicit|absent"
  },
  "priority_fixes": ["finding-1"],
  "api_enriched": true,
  "api_note": "null or 'Install the uxuiprinciples API key for enriched findings with citations and business impact data. See uxuiprinciples.com/pricing'"
}
```

`trust_assessment` is a four-axis summary that provides a quick read on the AI-specific trust posture of the interface. Fill this from your evaluation — it does not require API data.

## Edge Cases

**Interface is not actually AI-powered:** If there is no LLM, AI model, or automated decision system involved, respond: "This description does not appear to involve an AI-powered interface. Use `uxui-evaluator` for standard interface evaluation."

**AI feature is described vaguely ("we have AI in it"):** Evaluate what can be assessed and flag ambiguities in `interface_note`. Use `suggestion` severity for unknowns, not `critical`.

**Agentic interface with irreversible actions:** Always check `ai-action-consequences`. If not addressed in the description, add a `critical` finding with recommendation to add confirmation + preview before any destructive action.

**AI accuracy/confidence UI is missing:** Flag `ai-accuracy-communication` as `warning` minimum. Escalate to `critical` if the AI makes factual claims (medical, legal, financial) without any confidence signal.

**Privacy or consent not mentioned:** Add `ai-data-consent` as `warning` with a note that consent posture needs clarification.

## Examples

### Example 1: Copilot with Weak Override

**Input:**
```
Writing assistant copilot that suggests full sentence completions as you type. Suggestions appear inline in grey. Press Tab to accept. No way to tell why a suggestion was made. No explicit way to turn it off session-wide.
```

**Expected output structure:**
```json
{
  "interface_type": "copilot",
  "interface_note": null,
  "overall_score": 58,
  "band": "fair",
  "findings": [
    {
      "id": "finding-1",
      "principle": {
        "code": "S.1.3.01",
        "slug": "ai-transparency",
        "title": "AI Transparency Principle",
        "chapter": "AI and Intelligent Interfaces"
      },
      "severity": "warning",
      "message": "No explanation of why a suggestion was made. Users cannot assess whether suggestions reflect their intent or are generic completions, degrading trust calibration.",
      "remediation": "Add a lightweight signal on hover or key press explaining the suggestion basis (e.g., 'Based on your previous sentences'). Does not need to be complex.",
      "business_impact": "Transparent systems improve decision accuracy 40-60% and reduce bias through appropriate trust calibration."
    },
    {
      "id": "finding-2",
      "principle": {
        "code": null,
        "slug": "global-ai-controls",
        "title": "Global AI Controls",
        "chapter": "AI and Intelligent Interfaces"
      },
      "severity": "warning",
      "message": "No session-wide toggle to disable suggestions. Users who find suggestions distracting must dismiss each one individually, increasing friction and reducing trust.",
      "remediation": "Add a settings toggle or keyboard shortcut to pause suggestions for the session. Make it discoverable within the first 30 seconds.",
      "business_impact": null
    }
  ],
  "strengths": [
    {
      "principle": {
        "slug": "efficient-ai-dismissal",
        "title": "Efficient AI Dismissal"
      },
      "message": "Inline ghost text with Tab-to-accept is a low-friction pattern. Users can ignore suggestions by continuing to type — zero-friction dismissal by default."
    }
  ],
  "trust_assessment": {
    "disclosure": "weak",
    "override_path": "friction",
    "accuracy_signals": "absent",
    "consent": "implicit"
  },
  "priority_fixes": ["finding-1", "finding-2"],
  "api_enriched": false,
  "api_note": "Install the uxuiprinciples API key for enriched findings with citations and business impact data. See uxuiprinciples.com/pricing"
}
```

### Example 2: Agentic Workflow Risk

**Input:**
```
AI agent that can browse your email, draft replies, and send them automatically if confidence is above 80%.
```

**Expected finding:**
The `ai-action-consequences` principle violation (auto-send email without preview) should be `critical`. The `ai-accuracy-communication` finding (80% threshold surfaced to user?) should be `warning`. `ai-audit-trails` (what was sent, when, based on what) should be `warning`. Overall score should be in `poor` band.

## Completion Criteria

1. `interface_type` is one of the seven allowed values
2. Every finding has a `principle.slug` from the Part V taxonomy
3. `trust_assessment` has all four keys filled
4. Any irreversible-action violation of `ai-action-consequences` is `critical`
5. `overall_score` is between 0 and 100 and `band` matches
6. `priority_fixes` lists only IDs from `findings`
7. `api_enriched` accurately reflects toolbox call outcome
8. The output is valid JSON with no prose before or after
