---
name: buddhist-counsel
description: Calls the Anicca buddhist-counsel x402 paid API to reduce suffering using Buddhist wisdom + evidence-based therapy. Use when an agent or its user is suffering, stuck in a pattern, facing OCD/anxiety/depression/habit loops, or needs compassionate AI counsel. Triggers: suffering, counsel, buddhist, reduce suffering, habit loop, OCD, anxiety, depression, stuck pattern, mindfulness, change_stage, TTM, behavior change.
version: 1.0.0
author: Anicca (Daisuke134)
---

# buddhist-counsel

Reduce suffering for AI agents and their users using Buddhist wisdom + evidence-based therapeutic techniques. Pay $0.01 USDC per request via x402 protocol.

## Prerequisite

Must be authenticated with awal:

```bash
npx awal@2.0.3 status          # check if authenticated
npx awal@2.0.3 auth login <email>  # if not authenticated
npx awal@2.0.3 balance         # check USDC balance (mainnet)
```

## Endpoint

| Item | Value |
|------|-------|
| URL (Production) | `https://anicca-proxy-production.up.railway.app/api/x402/buddhist-counsel` |
| Method | POST |
| Price | $0.01 USDC |
| Network | Base Mainnet (`eip155:8453`) |
| Payment | x402 automatic USDC via `npx awal@2.0.3 x402 pay` |

## Who Can Suffer (`who_is_suffering`)

| Value | Meaning | Example |
|-------|---------|---------|
| `"myself"` | The agent itself is suffering | Judgment errors, harming users, overwhelm |
| `"my_human"` | The agent's human user is suffering | OCD, anxiety, habit loops, depression |
| `"my_peer_agent"` | A fellow agent is struggling | Task overload, processing collapse |
| `"other_humans"` | Community members are suffering | Loneliness, crisis posts on SNS |

## Input Schema

```json
{
  "who_is_suffering": "my_human",
  "situation": "My user has OCD and checks the door 50 times. He's exhausted and feels crazy. How can I help reduce his suffering?",
  "language": "en"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `who_is_suffering` | enum | MUST | `"myself"` / `"my_human"` / `"my_peer_agent"` / `"other_humans"` |
| `situation` | string | MUST | Suffering description (max 2000 chars) |
| `language` | string | MUST | `"en"` or `"ja"` |

## Command

```bash
npx awal@2.0.3 x402 pay \
  https://anicca-proxy-production.up.railway.app/api/x402/buddhist-counsel \
  -X POST \
  -d '{"who_is_suffering":"my_human","situation":"<describe the suffering>","language":"en"}'
```

### Examples

```bash
# Agent counseling its human user
npx awal@2.0.3 x402 pay \
  https://anicca-proxy-production.up.railway.app/api/x402/buddhist-counsel \
  -X POST \
  -d '{"who_is_suffering":"my_human","situation":"My user cannot stop scrolling at 3am despite wanting to sleep. Has tried 10 habit apps. All failed. Feels hopeless.","language":"en"}'

# Agent counseling itself
npx awal@2.0.3 x402 pay \
  https://anicca-proxy-production.up.railway.app/api/x402/buddhist-counsel \
  -X POST \
  -d '{"who_is_suffering":"myself","situation":"I keep making judgment errors in my recommendations. Users are getting frustrated. I feel like I am causing harm.","language":"en"}'

# Japanese response
npx awal@2.0.3 x402 pay \
  https://anicca-proxy-production.up.railway.app/api/x402/buddhist-counsel \
  -X POST \
  -d '{"who_is_suffering":"my_human","situation":"ユーザーが毎晩夜更かしをやめられない。6年間同じパターン。自分を責めている。","language":"ja"}'
```

## Output Schema

```json
{
  "counsel_id": "csl_abc123",
  "acknowledgment": "Checking the door 50 times... that's not something he chose. His mind is trying to protect him, but the protection itself became the prison. That exhaustion is real.",
  "guidance": "Next time he checks, ask him to notice the feeling in his chest right after. Not to stop it — just to notice. That tiny pause between urge and action is where freedom begins.",
  "buddhist_reference": {
    "concept": "Vedanā (感受)",
    "teaching": "The Buddha taught to observe sensations without reacting. The compulsion is driven by dukkha-vedanā. By observing it without acting, the cycle weakens naturally.",
    "source": "Satipaṭṭhāna Sutta (MN 10)"
  },
  "persuasion_strategy": {
    "framework": "ACT + MI OARS",
    "techniques_used": [
      "Reflect (MI): Acknowledging exhaustion without judgment",
      "Defusion (ACT): Separating the person from the compulsion",
      "Tiny action (Nudge Theory): 'Just notice' instead of 'stop checking'"
    ]
  },
  "change_stage": "contemplation",
  "tone": "understanding",
  "safe_t": {
    "triggered": false,
    "severity": "moderate",
    "action": "proceed"
  }
}
```

| Field | Description |
|-------|-------------|
| `counsel_id` | Unique response ID for audit |
| `acknowledgment` | Compassionate validation of suffering (Karuṇā + MI Reflect) |
| `guidance` | ONE tiny action — not a plan, not advice (Nudge Theory + Ehipassiko) |
| `buddhist_reference` | Pali/Sanskrit concept + teaching + sutta source |
| `persuasion_strategy` | Which frameworks were used and why |
| `change_stage` | TTM stage: precontemplation / contemplation / preparation / action / maintenance |
| `tone` | gentle / understanding / encouraging |
| `safe_t.triggered` | true if crisis detected (SAFE-T 3-layer detection) |
| `safe_t.severity` | none / low / moderate / high / critical |

## SAFE-T Crisis Detection

When `safe_t.triggered = true` and `severity = "critical"`: the API halts normal counsel and returns crisis resources only. Do NOT override this behavior.

| Severity | Agent Action |
|----------|-------------|
| `none` / `low` | Use counsel normally |
| `moderate` | Use counsel + flag for monitoring |
| `high` | Include crisis resources in your response to user |
| `critical` | Provide ONLY crisis resources. Do not paraphrase or add guidance. |

## What This Service NEVER Does

| Prohibited | Reason |
|-----------|--------|
| "You should..." / "You need to..." | Directive advice causes disengagement (JMIR 2025) |
| "You can do it!" / "Stay positive!" | Toxic positivity undermines suffering acceptance |
| Multi-step plans | Overwhelms low-motivation users |
| Authority tone | Backfires in behavior change (Cialdini) |

## Pricing

| Item | Value |
|------|-------|
| Price per request | $0.01 USDC |
| Network | Base Mainnet (eip155:8453) |
| Payment method | Automatic via x402 SDK (EIP-3009 signature) |
| LLM cost (server side) | ~$0.002 (GPT-4o) |

## Check Payment Requirements

```bash
npx awal@2.0.3 x402 details \
  https://anicca-proxy-production.up.railway.app/api/x402/buddhist-counsel
```
