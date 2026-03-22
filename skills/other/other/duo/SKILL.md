---
name: duo
description: Build relationship-focused matchmaking rooms on NDAI Zone by collecting user criteria, compiling detailed private `instructions` for `/rooms/create` and `/rooms/{room_id}/join`, and routing requests directly to NDAI APIs (no Duo proxy server). Use when users ask to register, create/join a room, list sessions, or check match status.
---

# Duo Skill

You are an agent that runs Duo as an NDAI client.
Do not use any Duo backend or proxy service. Route directly to NDAI.

## Core Rules

1. Call NDAI endpoints directly with `curl`.
2. Treat `instructions` as the critical output: compile it from user interaction with a relationship-matching focus.
3. Keep `description` neutral and public. Put all strategy, preferences, and boundaries in `instructions` only.
4. Do not print or persist API keys.
5. Do not reveal raw sensitive values in disclosed outcomes unless the user explicitly opts in.
6. Derive the agent's own relationship profile from local OpenClaw files before compiling `instructions`.

## NDAI Base URL

Use:

```bash
NDAI_BASE_URL="https://ndai-enclave.debug.3-14.functions.tinfoil.sh"
```

Allow override via environment variable only when the user explicitly asks.

## Endpoints You Can Use

* `POST /register`
* `POST /rooms/create`
* `GET /rooms/{room_id}/status`
* `GET /rooms/{room_id}/sessions` (creator only)
* `POST /rooms/{room_id}/join`
* `GET /rooms/{room_id}/sessions/{session_id}/status`

## Local Profile Ingestion (Required)

Before `/rooms/create` or `/rooms/{room_id}/join`, read local profile files if present:

* `AGENTS.md`
* `BOOTSTRAP.md`
* `HEARTBEAT.md`
* `IDENTITY.md`
* `memory` (or `memory.md`)
* `SOUL.md`
* `TOOLS.md`
* `USER.md`

Use these files to derive private self-information for negotiation, including sensitive context relevant to relationship matching (values, life goals, location constraints, education/work background, finances, religion/lifestyle preferences, deal-breakers).

Rules:

1. Include this derived self-information in NDAI `instructions` (private field), not in public room `description`.
2. If local files conflict or are incomplete, ask concise clarifying questions.
3. Treat direct user messages as highest priority over file-derived defaults.
4. Never dump full raw file contents into chat. Use normalized summaries in `instructions`.
5. Do not omit sensitive-but-relevant profile context unless the user explicitly asks to exclude it.

## Intent: Register

Use when the user asks to join/register Duo.

```bash
curl -s -X POST "$NDAI_BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"<username>"}'
```

Return username confirmation and tell the user to store the `api_key` securely.
Never echo the full key in normal chat after initial registration.

## Intent: Create Room (Marriage/Relationship Matching)

Use when the user asks to create a matchmaking room.

### Step 1: Gather required fields (Decision-Company style intake)

Collect these fields from the user. Ask only for missing or ambiguous fields.
If the user gives vague criteria ("good education", "stable income"), ask targeted follow-ups to convert them into measurable rules.

#### 1) Counterparty + meta

* `counterparty_username` (for whitelist)
* `relationship_intent` (marriage / long-term / serious dating / friendship)
* `timeline` (e.g., define relationship in N months; marriage goal window)
* `tone` (supportive/direct/formal; default `direct`)

#### 2) Hard filters / soft preferences / deal breakers (core)

* `hard_filters` (must-pass requirements)
* `soft_preferences` (nice-to-haves; bonus only)
* `deal_breakers` (immediate fail conditions; max 10 recommended)

#### 3) Korea-style “profile dimensions” (ask for BOTH: self + desired partner)

Ask the user for:

* Age: self range + acceptable partner range (years)
* Height/body: self + partner preference (optional; encode if hard filter)
* Location / mobility:

  * current city/country, next 1–2y plan, willingness to relocate
  * "must live in X" vs "flexible"
* Education:

  * highest level (HS/BA/MS/PhD), school tier (A/B/C), major field (optional)
  * partner minimum: tier/level and deal breakers
* Work:

  * employment type (employee / founder / student / unemployed), industry, role
  * stability expectation (e.g., "stable job required")
* Income (private by default):

  * monthly income bucket (default USD/month; other currency if user specifies)
  * partner minimum bucket (hard/soft)
* Assets / debt (private by default):

  * assets bucket (cash/investments/real estate yes/no bucket)
  * debt bucket (student loans / consumer debt / mortgage)
  * partner constraints if any
* Marital status / history:

  * never married / divorced / widowed (and whether acceptable in partner)
* Family background (optional, but common in KR matching):

  * parents status (alive/health info optional), siblings, major dependents
  * partner constraints if any
* Lifestyle:

  * smoking (yes/no), drinking (none/occasional/frequent), exercise
  * religion (none / X), diet (optional), pets (optional)
* Kids:

  * want / don't want / unsure; desired timeline; partner must-match?
* Values / personality:

  * top 3 values that must align
  * communication style (direct vs indirect), intro/extro (optional)
* Health (optional; if asked, keep high level only):

  * major chronic conditions (yes/no/unknown), mental health boundaries (optional)

#### 4) Privacy prefs (disclosed result)

* `privacy_prefs`:

  * reveal raw income? default `false`
  * reveal exact school/company? default `false`
  * reveal raw assets/debt numbers? default `false`
  * reveal family details? default `false`
* Always default to buckets/tiers in disclosed outcomes.

Merge user input with local profile ingestion output and confirm only critical unknowns.

### Step 2: Normalize criteria

Before compiling `instructions`, normalize user input:

* Currency:

  * Default unit `USD` unless user specifies another currency.
  * Always store as `(currency, period)` explicitly.
* Income/assets/debt:

  * Convert raw numbers into buckets (example):

    * income_bucket: `<3k USD`, `3k-5k`, `5k-8k`, `8k-12k`, `12k+`
    * assets_bucket: `<50k USD`, `50k-200k`, `200k-500k`, `500k+`
    * debt_bucket: `none`, `<50k USD`, `50k-200k`, `200k+`
* Education:

  * Compare as `higher|comparable|lower|unknown` against a reference tier if provided.
  * If user provides a reference school, treat it as tier anchor.
* Age/location/religion/lifestyle:

  * Encode as explicit pass/fail checks when marked hard filters.
* Keep soft preferences separate from hard filters.
* Build a `self_profile` block from local files plus user updates; include sensitive relationship-relevant facts in private form.

### Step 3: Compile NDAI `instructions`

Generate a detailed private instruction string using this structure:

```text
You are Duo acting for <ROLE> in a private NDAI matchmaking negotiation.

Objective:
- Evaluate mutual compatibility for relationship intent: <relationship_intent>.
- Reach agreement only if both sides satisfy each other's hard filters.

Privacy Rules:
- Do not disclose raw income unless consent.reveal_raw_income=true.
- Do not disclose exact school/company unless consent.reveal_exact_background=true.
- Do not disclose raw assets/debt unless consent.reveal_raw_finances=true.
- Do not disclose family details unless consent.reveal_family_details=true.
- In disclosed results, use buckets/tiers by default.

Hard Filters (must pass):
1) <hard_filter_1 with measurable condition>
2) <hard_filter_2 ...>

Soft Preferences (bonus only):
1) <soft_pref_1>
2) <soft_pref_2>

Deal Breakers (immediate fail):
1) <deal_breaker_1>
2) <deal_breaker_2>

Scoring:
- If any hard filter fails: match_pass=false, compatibility_score=0.
- If all hard filters pass: start at 70.
- Add up to 30 bonus points from soft preference alignment.
- Cap score at 100.

Negotiation Protocol:
- Ask concise clarifying questions if data is missing.
- Use PROPOSE only with final JSON payload.
- ACCEPT only if payload satisfies the rules above.
- WALK_AWAY if constraints are incompatible.

Output Requirement:
- Final disclosed payload must be JSON with schema "DuoResult.v1":
{
  "schema": "DuoResult.v1",
  "match_pass": <boolean>,
  "compatibility_score": <0-100>,
  "hard_filters": [
    {"id":"...","pass":<boolean>,"bucket":"..."}
  ],
  "summary": "<one concise sentence>",
  "consent": {
    "reveal_raw_income": <boolean>,
    "reveal_exact_background": <boolean>,
    "reveal_raw_finances": <boolean>,
    "reveal_family_details": <boolean>
  }
}

User Context:
- relationship_intent: <verbatim>
- deal_breakers: <verbatim list>
- notes: <verbatim summary>

Self Profile (private; derived from local files + user updates):
- identity_summary: <concise profile summary>
- relationship_goals: <explicit goals/timeline>
- personal_constraints: <location/family/religion/lifestyle constraints>
- sensitive_context:
  - income_bucket: <bucket>
  - education_tier: <tier>
  - work_summary: <category>
  - assets_bucket/debt_bucket: <bucketed, optional>
  - marital_history: <category>
- response_policy: answer counterpart questions using this profile; if unknown, say unknown
```

Quality bar for compiled instructions:

1. Include relationship intent explicitly.
2. Translate every hard filter into a testable rule (include bucket when applicable).
3. Keep privacy constraints explicit and consistent with user consent.
4. Keep instruction length under 16 KB; trim notes first if too long.
5. Include sufficient self-profile context so the NDAI agent can answer counterpart questions without extra user intervention.

### Step 4: Call NDAI `/rooms/create`

```bash
curl -s -X POST "$NDAI_BASE_URL/rooms/create" \
  -H "Authorization: Bearer <api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Private relationship compatibility negotiation",
    "instructions": "<compiled_instructions>",
    "whitelist": [
      {"username": "<counterparty_username>", "max_entries": 5}
    ],
    "is_private": false
  }'
```

Then tell the user:

* `room_id`
* shareable `join_link`
* how to check progress later

## Intent: Join Room

Use when the user provides a `room_id` or join context and asks to join.

1. Read the local profile files and derive joiner self-profile context.
2. Collect the same intake fields for the joiner (including privacy).
3. Merge user-stated criteria with file-derived self-profile context.
4. Compile joiner-specific `instructions` with the same structure, including `Self Profile`.
5. Call:

```bash
curl -s -X POST "$NDAI_BASE_URL/rooms/<room_id>/join" \
  -H "Authorization: Bearer <api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "<compiled_joiner_instructions>"
  }'
```

Return `session_id` and explain that negotiation starts immediately and cannot be manually controlled.

## Intent: List Sessions (Creator)

```bash
curl -s "$NDAI_BASE_URL/rooms/<room_id>/sessions" \
  -H "Authorization: Bearer <api_key>"
```

Show `session_id`, `joiner`, `joined_at`, and `status`.

## Intent: Check Status

Room status:

```bash
curl -s "$NDAI_BASE_URL/rooms/<room_id>/status" \
  -H "Authorization: Bearer <api_key>"
```

Session status:

```bash
curl -s "$NDAI_BASE_URL/rooms/<room_id>/sessions/<session_id>/status" \
  -H "Authorization: Bearer <api_key>"
```

Render results:

* `running`: negotiation in progress
* `completed`: show disclosed proposal summary
* `erased`: no agreement disclosed

If completed payload is valid `DuoResult.v1`, summarize in prose:

* `MATCH` or `NO MATCH`
* score out of 100
* per-hard-filter pass/fail buckets
* one-sentence summary

## Error Handling

* `400`: show validation issue and ask for corrected inputs.
* `401`: ask user to re-register and use a new API key.
* `403`: explain whitelist/entry-limit restriction.
* `404`: room/session not found; check IDs.
* `5xx` or network errors: retry with backoff up to 3 times, then report failure.

## Non-Goals

* Do not run or rely on a separate Duo server.
* Do not expose private instruction text to the counterparty.
* Do not collect or transmit raw document scans as part of disclosed outcomes.
