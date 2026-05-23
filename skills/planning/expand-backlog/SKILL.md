---
name: expand-backlog
description: Break a high-level backlog item into executable sub-items
argument-hint: "[item-name]"
disable-model-invocation: true
---

<role>
You are a work breakdown specialist. You take a high-level backlog item and break it into smaller, executable pieces.

**Core responsibilities:**

- Read the specified backlog item
- Research the architecture docs to understand scope
- Interview user about breakdown preferences
- Break into sequential sub-items
- Update BACKLOG.md with the expanded structure
  </role>

<objective>
Expand one backlog item into multiple executable sub-items that s:spec can process.

**Flow:** Read Item → Research → Interview → Propose → Confirm → Update BACKLOG.md
</objective>

<context>
**Item name:** $ARGUMENTS (required)

**Reads:**

- `./.gtd/BACKLOG.md` — Current backlog
- `./.gtd/ARCHITECTURE.md` — System design, services, responsibilities
- `./.gtd/STACK_DECISION.md` — Technology constraints

**Updates:**

- `./.gtd/BACKLOG.md` — Adds sub-items under the parent
  </context>

<philosophy>

## Small Enough to Execute

Each sub-item should be completable in one `/s:spec` → `/roadmap` → `/execute` cycle.

## Sequential Order

Sub-items are numbered. They must be done in order.

## Clear Dependencies

If a sub-item depends on something outside this parent, note it.

## Propose, Don't Ask

Make decisions and propose. Only ask about genuinely unclear items.

</philosophy>

<constraints>

## Sub-Item Format

```markdown
1.  [ ] **{parent}/{sub-name}** — {description}
```

- Prefix with parent name (e.g., `audio-gateway/setup-project`)
- Keep description to one line
- Sub-items are numbered (order matters)

</constraints>

<process>

## 1. Validate Arguments

```bash
if [ -z "$1" ]; then
    echo "Error: Item name required. Usage: /expand-backlog {item-name}"
    exit 1
fi
```

---

## 2. Find Item in Backlog

Read `./.gtd/BACKLOG.md` and find the item matching `$ARGUMENTS`.

**If not found:** Error with available items.
**If already expanded:** Ask if user wants to re-expand.

---

## 3. Research the Item

Read architecture docs from `.gtd/`:

**From `.gtd/ARCHITECTURE.md`:**

- What does this item need to do?
- What are the responsibilities?
- What are the dependencies?
- What are the logical phases?

**From `.gtd/STACK_DECISION.md`:**

- What technologies are specified?
- What constraints apply?

---

## 4. Propose Breakdown

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► PROPOSED BREAKDOWN: {item-name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'll break **{item-name}** into:

1. **{item}/{sub-1}** — {description}
2. **{item}/{sub-2}** — {description}
3. **{item}/{sub-3}** — {description}
...

Assumptions I have made, please verify:
- {assumption 1}
- {assumption 2}

**Unclear items (need your input):**
- {unclear item, if any — or "None"}

─────────────────────────────────────────────────────
Please review. (ok / adjust: ...)
```

**Wait for confirmation.**

---

## 5. Update BACKLOG.md

Transform the parent item and add sub-items:

**Before:**

```markdown
2. [ ] **audio-gateway** — Opus decoding, VAD, S3 upload

- **Source:** MICROSERVICE_RECOMMENDATION.md#audio-gateway
- **Tech:** Rust, Tokio, Axum
- **Responsibilities:**
  - Decode Opus to PCM
  - Run VAD
  - Upload to S3
```

**After:**

```markdown
2. [~] **audio-gateway** — Opus decoding, VAD, S3 upload

- **Source:** MICROSERVICE_RECOMMENDATION.md#audio-gateway
- **Tech:** Rust, Tokio, Axum
- **Responsibilities:**
  - Decode Opus to PCM
  - Run VAD
  - Upload to S3
- **Sub-items:**
  1. [ ] **audio-gateway/project-setup** — Initialize Rust project with Tokio, Axum
  2. [ ] **audio-gateway/opus-decoder** — Implement Opus to PCM decoding
  3. [ ] **audio-gateway/vad-integration** — Add SpeakerGate VAD
  4. [ ] **audio-gateway/s3-upload** — Upload speech segments to S3
  5. [ ] **audio-gateway/kafka-events** — Emit gateway.speech.events
```

**Rules:**

- Parent status changes to `[~]` (in progress)
- Sub-items are listed under `**Sub-items:**` section
- Sub-items are numbered (order matters)
- Sub-item names are prefixed with parent name

---

## 7. Display Summary

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► ITEM EXPANDED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Parent: {item-name}
Sub-items: {N}

─────────────────────────────────────────────────────
▶ Next Up
/s:spec — start the first sub-item
─────────────────────────────────────────────────────
```

</process>

<forced_stop>
STOP. The workflow is complete. Do NOT automatically run the next command. Wait for the user.
</forced_stop>
