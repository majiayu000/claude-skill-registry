---
name: voice-generate
description: Generate text in a learned writing voice using extracted voice
  profiles and register selection. Frames source material as raw notes for
  optimal output quality. Use when writing blog posts, essays, emails, or
  any prose in the user's trained voice.
version: 1.9.0
globs: "**/*.{md,txt}"
alwaysApply: false
category: writing-quality
tags:
- voice
- generation
- style-transfer
- writing
- registers
tools:
- Read
- Write
- Bash
- Glob
- Agent
- TodoWrite
complexity: high
model_hint: opus
estimated_tokens: 2400
progressive_loading: true
modules:
- source-framing
- register-selection
- generation-pipeline
dependencies:
- scribe:voice-extract
- scribe:slop-detector
---

# Voice Generation Skill

Generate text in a user's extracted writing voice.

## Core Principle: Source Material Framing

The single largest variable in output quality is how source
material is framed in the prompt. Material framed as "raw
notes I'm still thinking through" produces text that feels
like thinking. Material framed as summaries produces reporting.

Always frame user-provided source material as raw notes unless
the user explicitly requests otherwise.

## Required TodoWrite Items

1. `voice-generate:profile-loaded` - Voice profile read
2. `voice-generate:register-selected` - Register chosen
3. `voice-generate:source-framed` - Material framed as notes
4. `voice-generate:generated` - Text produced
5. `voice-generate:review-dispatched` - Sent to review agents

## Step 1: Load Voice Profile

```bash
PROFILE_DIR="$HOME/.claude/voice-profiles/{name}"
```

Read in order:
1. `extraction.md` - Core voice features
2. `registers/{register}.md` - Active register
3. `craft-rules.md` - Shared craft techniques (if exists)
4. `banned-phrases.md` - Anti-patterns to avoid (if exists)

Check for per-project override:
```bash
if [ -f ".voice/override.md" ]; then
  # Merge project overrides with profile
fi
```

## Step 2: Register Selection

Load: `@modules/register-selection`

Select register by:
1. Explicit user request ("use casual register")
2. Context matching from register metadata
3. Default fallback to `registers/default.md`

## Step 3: Frame Source Material

Load: `@modules/source-framing`

**Default framing** (always use unless user overrides):

```
Below are my rough notes on this topic. I'm still thinking
through these ideas. Use them as the raw material for the
piece, not as a structure to follow:

---
{user_provided_source_material}
---
```

**Alternative framings** (only if user requests):
- "structured outline" - when user wants to preserve structure
- "key points to cover" - when user provides bullet points
- "conversation to draw from" - when source is a transcript

## Step 4: Generation Prompt

Compose the generation prompt:

```
You are writing a piece in a specific voice. The voice
features below were extracted from the writer's own work.
Follow them as concrete instructions, not suggestions.

## Voice Features

{extraction.md content}

## Active Register: {register_name}

{register content}

## Craft Techniques (apply all)

- Concrete-first: Lead with specific, physical details before
  any abstraction
- Naming: When you describe a pattern in 2+ sentences, compress
  it into a 2-4 word label
- Opening moves: Start mid-thought, with a specific moment, or
  with a counterintuitive claim. Never start with throat-clearing
- Human-moment anchoring: Ground every abstraction in a specific
  scene or lived experience
- Aphoristic destinations: At least one sentence per section
  should be worth repeating out of context

## Banned (never use)

{banned_phrases content, or default list:}
- Em dashes (use commas, colons, semicolons, parentheses)
- "delve", "utilize", "leverage", "facilitate"
- "it's important to note", "in today's world"
- "here's the thing", "let that sink in"
- "furthermore", "moreover", "comprehensive"
- Negation-correction patterns ("This isn't X. This is Y.")

## Source Material

{framed source material from Step 3}

## Task

Write the piece. Follow the voice features precisely. Apply
craft techniques. Do not use any banned phrases. The output
should read as if the writer produced it themselves.

Length: {user_specified or ~same as source material}
Format: {user_specified or prose paragraphs}
```

## Step 5: Post-Generation

After generation:
1. Scan output for banned phrases (auto-fix silently)
2. Check for em dashes (replace with appropriate punctuation)
3. Dispatch to voice-review skill if user wants review
4. Save pre-review snapshot if learning mode is active

## Model Routing

- **Generation**: Use Opus. Tonal shifts, parenthetical
  subversion, and subtle voice qualities require the larger
  model. Sonnet flattens these.
- **Banned phrase scan**: Can run locally (regex/grep)
- **Review agents**: Sonnet is sufficient (structured prompts)

## Per-Project Voice

If `.voice/override.md` exists in the current project:
- Read override content
- Merge with profile (overrides take precedence)
- Note in output: "Applied project voice override"

## Exit Criteria

- Text generated in the specified voice
- No banned phrases present
- Craft techniques applied (concrete-first, naming, etc.)
- Source material framed as raw notes
- Review dispatched (if requested)
- Snapshot saved (if learning mode active)
