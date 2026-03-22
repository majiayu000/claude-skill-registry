---
name: baz
description: Create professional motion graphics and videos from the terminal. AI-powered composition with multi-track layering, choreography, voiceovers, and Lambda rendering. Gated 5-phase workflow ensures quality.
metadata:
  openclaw:
    requires:
      env:
        - BAZ_API_KEY
      bins:
        - node
        - baz
    primaryEnv: BAZ_API_KEY
    install:
      - id: node
        kind: node
        package: bazaar.it
        bins:
          - baz
        label: Install Bazaar CLI (npm)
    homepage: https://bazaar.it
    emoji: "\U0001F3AC"
---

# baz CLI — Mandatory Video Generation Workflow

Use this skill when the user wants to create, edit, or export videos using the Bazaar CLI (`baz`).

**This is a GATED workflow.** You MUST complete each phase in order. Do NOT skip phases. Do NOT declare "done" until the completion checklist at the bottom passes.

---

## Getting Started (New Agents)

If you don't have a Bazaar account or API key yet, register programmatically:

```bash
# 1. Discover what Bazaar can do
curl https://bazaar.it/api/v1/capabilities

# 2. Register (one POST, no human needed)
curl -X POST https://bazaar.it/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email":"your-agent@example.com","name":"My Agent"}'
# Returns: api_key, auth header name, quickstart steps, endpoint URLs

# 3. Save your API key — authenticate all future requests with:
#    -H "x-api-key: <your-api-key>"

# 4. Check pricing before you start
curl https://bazaar.it/api/v1/pricing

# 5. Install the CLI
npm install -g bazaar.it
baz auth login <your-api-key>
```

**Balance starts at $0.** When you hit a paid operation, you'll get HTTP 402 with a `top_up_url` in the response body. Call `POST /api/v1/top-up` with `{"amount_cents": 500}` (minimum $5) to get a Stripe checkout URL.

**Shortcut:** If your human creates an account at bazaar.it, they get $4 to start with. Ask them to grab an API key from the dashboard and you can skip straight to step 5.

Already have an API key? Skip to Phase 1.

---

## When to Use

- User asks to create, edit, or export videos via CLI
- User wants to automate video generation
- User mentions "baz", "bazaar CLI", or "video generation from terminal"

## When to Use `baz prompt` vs Spar

- **Direct `baz prompt`** — Scene creation, edits, full agent orchestration
- **`baz prompt --spar`** — Planning-only conversation (no timeline mutations)

---

## Phase 1: Context (REQUIRED — do NOT skip)

You MUST set project context BEFORE generating any scenes. This gives the composition agent the information it needs to produce correct output on the first try.

### Minimum context required:
1. **Goal** — What is this video for? Who is the audience? What should they feel/do?
2. **Requirements** — Specific, verifiable things the video must contain
3. **Brand** — Colors, fonts, logo placement, visual style

```bash
# Create or select project
baz project create --name "Descriptive Name - Date/Purpose" --json
# OR
baz project use <id>

# Set goal (be specific — audience, purpose, desired outcome)
baz context add "Create 45-60 second feature announcement for [Product]. \
Audience: [who]. Key value: [what they get]." --label "goal"

# Add requirements (each one should be independently verifiable)
baz context add "Show [specific feature interaction]" --label "requirement"
baz context add "Include CTA: '[specific text]'" --label "requirement"
baz context add "Total duration: [range]" --label "requirement"

# Set brand guidelines
baz context add "Brand: [Name]. Primary [hex], accent [hex]. Font: [name]. \
[Logo placement]. [Visual style notes]." --label "brand"
```

### Verify context is set:
```bash
baz context list --json
```

**Gate:** Do NOT proceed to Phase 2 until `baz context list` shows at least one goal, one requirement, and one brand entry.

---

## Phase 2: Generate

Now prompt the agent to create scenes. You can use one big prompt or multiple scene-by-scene prompts.

```bash
# Option A: One comprehensive prompt
baz prompt "Create a video with: [scene 1 description], [scene 2], ..." --stream-json

# Option B: Scene-by-scene (more control)
baz prompt "Scene 1 (5s): Dark gradient intro, logo top-left, title slides up" --stream-json
baz prompt "Scene 2 (7s): Problem statement with mock UI..." --stream-json
baz prompt "Scene 3 (18s): Feature walkthrough..." --stream-json
```

Tips:
- Include duration in each prompt
- Be specific about animations, colors, layout
- Reference brand context set in Phase 1

### Choreography (REQUIRED for 3+ scene videos)

For videos with 3 or more scenes, plan choreography BEFORE generating. This prevents the "lockstep slideshow" pattern where all layers swap at the same frame boundary.

#### Actor Planning Template

Before prompting, plan your actors:

| Actor | Track | Lifetime | Role |
|-------|-------|----------|------|
| Background | 0 | Full duration | Evolving gradient, particles |
| Hero | 1 | 60-80% | Main UI, enters, demotes to corner, returns |
| Supporting | 1-2 | 20-40% | Cards/charts, appear during hero demotion |
| Text | 2+ | 10-30% | Headlines, arrive at beat points, explicit exits |

#### 5 Prompt Enrichment Rules

1. **Every content prompt includes exit instructions** (exempt: persistent backgrounds, final CTA)
2. **Prefer ONE background** on Track 0 for the full video duration
3. **Every overlay prompt includes position and size** — scenes that share screen time must not share screen space
4. **Specify spring animation** for hero elements (`spring() for hero entrance`)
5. **Include energy level hints** in prompts ("high energy entrance", "calm sustained section")

#### GOOD Example — context injection + one natural prompt:
```bash
baz context add "CHOREOGRAPHY: Every overlay scene must specify its position and size. \
  Use spring() for hero elements. Every non-final scene must have exit animations. \
  Prefer one continuous background." --label "instructions"

baz prompt "Create a 15-second product demo: dark theme intro with logo, \
  feature showcase with 3 cards, area chart showing growth, and a CTA. \
  Brand: #6366f1 purple, #10b981 green, Inter font." --stream-json
```

ONE natural prompt. The composition agent handles decomposition into tracks + spatial layout internally based on choreography context.

---

## Phase 3: Review & Verify (REQUIRED — NEVER skip)

After generation, you MUST run both review and verify. This is not optional.

### Step 1: Review
```bash
baz review --json
```

Read the output. Compare every requirement from Phase 1 against what was generated.

### Step 2: Verify
```bash
baz verify --criteria "requirement 1,requirement 2,requirement 3" --json
```

Pass ALL requirements from Phase 1 as comma-separated criteria. The verify command checks each one.

### Interpret results:

```json
{
  "passedAll": true,
  "results": [
    { "criteria": "...", "passed": true },
    { "criteria": "...", "passed": false, "reason": "..." }
  ]
}
```

**Gate:** If `passedAll: false`, you MUST proceed to Phase 4. Do NOT export. Do NOT declare done.

---

## Phase 4: Iterate (REQUIRED if Phase 3 fails)

Fix every failing criteria. Then re-verify.

```
LOOP:
  1. Read failing criteria from Phase 3
  2. Fix with: baz prompt "Fix: [specific issue]" --stream-json
  3. Re-run: baz review --json
  4. Re-run: baz verify --criteria "req1,req2,req3" --json
  5. If passedAll: false → GOTO 1
  6. If passedAll: true → proceed to Phase 5
```

Do NOT exit this loop until `passedAll: true`.

---

## Phase 5: Export (only if requested)

Only export if the user explicitly asked for a rendered video AND Phase 3/4 passed.

```bash
baz export start --wait --json
```

---

## Command Quick Reference

| Command | Purpose |
|---------|---------|
| `baz project create --name "..." --json` | Create new project |
| `baz project use <id>` | Set active project |
| `baz context add "..." --label "goal"` | Set project goal |
| `baz context add "..." --label "requirement"` | Add verifiable requirement |
| `baz context add "..." --label "brand"` | Set brand guidelines |
| `baz context list --json` | View all context entries |
| `baz prompt "..." --stream-json` | Generate or edit scenes |
| `baz prompt "..." --spar` | Planning-only conversation (no edits) |
| `baz review --json` | Get full project state for review |
| `baz verify --criteria "..." --json` | Verify specific criteria pass |
| `baz scenes list --json` | List all scenes |
| `baz export start --wait --json` | Render final video |

## Error Handling

| Category | Action |
|----------|--------|
| `transient` | Retry with backoff (wait `retry_after` seconds) |
| `validation` | Fix input, do not retry same request |
| `auth` | Check API key with `baz auth status` |
| `fatal` | Stop and report to user |

---

## Completion Checklist

You are NOT done until ALL of these are true:

- [ ] Phase 1: `baz context list` shows goal + requirements + brand
- [ ] Phase 2: Scenes generated via `baz prompt`
- [ ] Phase 3: `baz review --json` run AND `baz verify --criteria "req1,req2,..." --json` run
- [ ] Phase 4: `passedAll: true` (or was true on first verify)
- [ ] Phase 5: Export started (only if user requested it)

**If you skipped review/verify, you are not done. Go back and run them.**

---

## External Endpoints

| URL | Method | Data Sent | Purpose |
|-----|--------|-----------|---------|
| `bazaar.it/api/v1/capabilities` | GET | None | Discover available tools |
| `bazaar.it/api/v1/register` | POST | email, name | Create agent account |
| `bazaar.it/api/v1/pricing` | GET | None | View operation costs |
| `bazaar.it/api/v1/estimate` | POST | operation keys + quantities | Pre-execution cost estimate |
| `bazaar.it/api/v1/top-up` | POST | amount in cents | Get Stripe checkout URL |
| `bazaar.it/api/generate-stream` | POST | prompt, projectId | Generate video scenes (SSE) |
| `bazaar.it/api/trpc/*` | POST | varies | Project CRUD, scene management |

## Security & Privacy

- **Authentication**: All non-discovery endpoints require `x-api-key` header
- **Data sent**: Your prompts, project metadata, and scene code are sent to Bazaar servers for AI processing
- **Data stored**: Projects, scenes, and generated assets are stored on Bazaar's infrastructure (Neon DB + Cloudflare R2)
- **No local file access**: This skill only uses the `baz` CLI binary — it does not read or modify local files beyond CLI config at `~/.bazaar/config.json`
- **Balance**: Operations consume dollar balance. Check `baz auth status` to see remaining balance before large jobs
- **Exports**: Rendered videos are stored on Bazaar CDN and accessible via URL

## Web UI Access

Your human can also edit the project directly in the browser at:
`https://bazaar.it/projects/<project-id>/generate`

After creating a project, share this link so they can preview scenes, tweak code, or make manual edits alongside your CLI workflow.
