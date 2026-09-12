---
name: create-skill
description: |
  Create new marketing skills for the mktg playbook. Use when the agent needs to add a new capability, someone says 'create a skill', 'new skill', 'add a marketing skill', 'extend the playbook', 'I need a skill for X', 'build a skill', 'make a skill for Y', or 'add capability for Z'. Also use when someone wants to capture a marketing workflow they just did into a reusable skill, or when they say 'turn this into a skill'. Reads the skill contract, generates SKILL.md with correct frontmatter and structure, creates the directory, and reminds the agent to register in the manifest.
allowed-tools: []
---

# /create-skill — Skill Creator

Meta-skill for extending the mktg marketing playbook. You create new skills that follow the drop-in contract so they work immediately with `/cmo`, `mktg doctor`, and the full skill ecosystem.

For brand memory protocol, see /cmo [rules/brand-memory.md](../cmo/rules/brand-memory.md).

## On Activation

1. Read the skill contract: [workflows/create-new-skill.md](workflows/create-new-skill.md)
2. Read the template: [templates/marketing-skill.md](templates/marketing-skill.md)
3. Read `skills-manifest.json` in the project root to understand existing skills and avoid overlap.
4. Ask: **What marketing capability should this skill add?**

## Phase 0: Validate the Need

Gate check. Before creating a new skill, verify it doesn't already exist:

| Signal | Action |
|--------|--------|
| Capability covered by existing skill | Skip. Point to the existing skill. |
| Slight variation of existing skill | Skip. Suggest extending the existing skill instead. |
| Genuinely new marketing capability | Proceed. |
| Orchestrator chaining existing skills | Proceed. Mark as orchestrator layer. |

Check `skills-manifest.json` for the full list. Common near-misses:
- "social media copy" → `/content-atomizer` already handles this
- "brand guidelines" → `/brand-voice` covers this
- "SEO strategy" → `/keyword-research` + `/seo-audit` cover this

## Phase 1: Gather Requirements

Ask these questions (one at a time, stop when clear):

1. **Name** — What should the skill be called? (kebab-case, e.g., `webinar-funnel`)
2. **Trigger phrases** — What would someone say to invoke this? (5-8 natural phrases)
3. **Category** — Where does it fit? (foundation / strategy / copy-content / distribution / creative / seo / conversion / growth / knowledge)
4. **Layer** — What layer? (foundation / strategy / execution / orchestrator)
5. **Tier** — How essential? (must-have / nice-to-have / experimental)
6. **Brand reads** — Which `brand/` files does it need? (voice-profile.md, audience.md, etc.)
7. **Brand writes** — Which `brand/` files does it update?
8. **Dependencies** — Which skills should run first? (e.g., `brand-voice`, `audience-research`)
9. **Core workflow** — What are the main phases? (3-5 phases typical)

## Phase 2: Generate the Skill

1. Copy the template from [templates/marketing-skill.md](templates/marketing-skill.md).
2. Fill in all frontmatter fields from Phase 1 answers.
3. Write the skill body following this structure:
   - **Title line** — `# /<name> — <Short Description>`
   - **Opening paragraph** — What this skill does and why it matters (2-3 sentences)
   - **Brand memory reference** — Link to `/cmo` brand-memory rules
   - **On Activation** — Steps to load context and assess the request
   - **Phases 1-N** — The core workflow (3-5 phases)
   - **Worked Example** — One concrete example showing the skill in action
   - **Anti-Patterns** — Table of common mistakes and corrections
   - **YAGNI Principles** — What NOT to add
4. Write the description field carefully — it's used for routing. Include:
   - What the skill does (first sentence)
   - When to use it (second sentence)
   - Trigger phrases (remaining text)

## Phase 3: Create the Directory

```
skills/<name>/
├── SKILL.md              # Required — the skill itself
├── templates/            # Optional — reusable templates
├── workflows/            # Optional — step-by-step procedures
└── references/           # Optional — supporting knowledge
```

Only create subdirectories if the skill genuinely needs them. Most skills are a single SKILL.md.

## Phase 4: Register and Validate

1. **Remind** the agent (or user) to add an entry to `skills-manifest.json`:
   ```json
   "<name>": {
     "source": "new",
     "category": "<category>",
     "layer": "<layer>",
     "tier": "<tier>",
     "reads": ["<file1>.md"],
     "writes": ["<file1>.md"],
     "depends_on": ["<skill1>"],
     "triggers": ["<phrase1>", "<phrase2>"],
     "review_interval_days": 60
   }
   ```
2. **Validate** with `mktg skill validate <name>` if the CLI is available. If CLI is unavailable, manually verify:
   - Frontmatter has `name`, `description`, `allowed-tools` fields
   - `name` matches the directory name exactly
   - Description includes trigger phrases for routing
   - All referenced brand files use valid names from the standard set
   - No trigger phrases conflict with existing skills (check manifest)
3. **Test** by invoking `/<name>` and verifying the On Activation flow works.

Do NOT modify `skills-manifest.json` directly in this skill — that's a separate step to avoid merge conflicts.

### Handling Modification Requests

If the user wants to modify an existing skill (not create a new one):
- "Update skill X" or "add a mode to Y" → Read the existing SKILL.md, understand its structure, make targeted edits. Do not use the creation workflow.
- "Merge skill X into skill Y" → Read both, propose the merge, confirm, then edit the target skill.
- Route here only for genuinely new capabilities.

---

## Key Principles

### Frontmatter Contract

Every SKILL.md must have this exact frontmatter structure:

```yaml
---
name: <kebab-case-name>
description: |
  <Multi-line description. First sentence: what it does.
  Second sentence: when to use it. Remaining: trigger phrases.>
allowed-tools: []
---
```

- `name` must match the directory name
- `description` is used by Claude for skill routing — be specific and include trigger phrases
- `allowed-tools` is always `[]` for marketing skills (they use the agent's default tools)

### The On Activation Pattern

Every skill starts with On Activation — the first thing that runs when invoked:

1. Load brand context (read `brand/` files)
2. Show what loaded (visual tree with checkmarks)
3. Assess the request
4. Gate check (skip if wrong skill)

This pattern matters because it's what makes progressive enhancement work — skills produce useful output at zero context but get noticeably better with brand memory. Skipping it means the skill either errors on missing files or ignores context that would make output 3x better.

### Progressive Enhancement

Skills must NEVER gate on brand files. They enhance output but are never required:

```
# Good
1. Read `brand/voice-profile.md` if it exists. Adapt tone accordingly.
2. If not available, use defaults (direct, conversational).

# Bad
1. Read `brand/voice-profile.md`. ERROR if not found.
```

---

## Writing Good Skill Content

The template gives structure. Here's how to fill it with substance:

- **Phase instructions:** Use imperative verbs ("Read X," "Generate Y," "Ask the user Z"). Specify inputs and outputs for each phase. Include conditional logic where decisions vary ("If the user has a URL, scrape it. If not, ask 3 questions.").
- **Worked examples:** Pick a realistic scenario the target user would actually encounter. Walk through key decision points, not just the happy path. Show what the output looks like, not just what it contains.
- **Calibrating prescriptiveness:** Be specific where consistency matters (output format, file paths, frontmatter). Leave room for agent judgment where creativity matters (copy tone, strategic recommendations, question sequencing).
- **Anti-patterns:** Think about the 3 most common ways this skill could go wrong. Usually: doing too much, doing too little, or doing the wrong thing entirely.

## Anti-Patterns

| Anti-pattern | Instead | Why |
|-------------|---------|-----|
| Creating a skill that overlaps with an existing one | Check manifest first, extend existing skill | Duplicate skills confuse routing — /cmo won't know which to pick, and the builder gets inconsistent results depending on which triggers. |
| Skipping the description field or writing it vaguely | Description IS routing — be specific, include triggers | Claude decides whether to use a skill based almost entirely on the description. A vague description means the skill never gets invoked, no matter how good the content is. |
| Making brand files required | Progressive enhancement — enhance, never gate | Brand files build up over time. A skill that errors on missing files is useless for new projects, which is exactly when builders need the most help. |
| Adding 10+ phases | 3-5 phases. If more, split into multiple skills | Long skills are hard for agents to follow consistently. Each additional phase increases the chance of drift or skipped steps. |
| Hardcoding file paths outside `brand/` and `campaigns/` | Use the standard directories | Non-standard paths break cross-skill references. If one skill writes to `output/` and another looks in `brand/`, the context chain is broken. |
| Skills that call other skills | Skills read/write files. `/cmo` orchestrates | Skill-to-skill calls create hidden dependencies and ordering problems. Files are the API — they're inspectable, debuggable, and don't create call chains. |
| Forgetting the worked example | Every skill needs one concrete example | Examples are worth more than abstract instructions. An agent reading a worked example can infer patterns that no amount of rules can convey. |

## YAGNI Principles

- Don't create orchestrator skills unless you have 3+ skills to chain
- Don't add references/ directory for a simple skill — one SKILL.md is fine
- Don't over-specify the workflow — leave room for the agent's judgment
- Don't duplicate knowledge that lives in another skill
- The skill contract is the source of truth, not this skill — if they diverge, update this skill
