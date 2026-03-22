---
name: write-blog
description: "End-to-end blog creation pipeline from topic to publish-ready draft. Orchestrates research, planning, diagram generation, and writing in sequence with approval checkpoints. Use when user wants to create a complete blog post from scratch on a given topic."
disable-model-invocation: true
---

# Full Blog Pipeline Orchestrator

## Input
$ARGUMENTS = the topic in natural language
(e.g., "sliding window attention", "mixture of experts", "flash attention")

## Pipeline

Execute these phases IN ORDER. Each phase must complete before the next begins.
Include approval checkpoints at critical stages.

---

### Phase 1: Deep Research
**Goal:** Understand the topic thoroughly.

1. Run the research-topic skill with the given topic.
2. Wait for completion.
3. Verify research/<topic-slug>.md exists and is substantial.
4. Report to user:
   - Number of sources found
   - Key concepts identified
   - Number of visual opportunities found
5. Ask: "Research complete. Ready to proceed to planning?"
6. **STOP and wait for user approval.**

---

### Phase 2: Article Planning
**Goal:** Create a detailed outline with diagram specifications.

1. Run the plan-article skill.
2. Wait for completion.
3. Verify plan/<topic-slug>_outline.md exists.
4. Show the user:
   - Complete section outline
   - List of all planned diagrams (with count)
   - The running example that will be used
5. Ask: "Here is the article outline with X planned diagrams.
   Happy with this? Any sections to add, remove, or reorder?"
6. **STOP and wait for user approval.**
7. If user requests changes, update the plan and re-present.

---

### Phase 3: Diagram Generation
**Goal:** Create all visual assets using PaperBanana.

1. Run the generate-diagrams skill.
2. Wait for completion.
3. Show user the generation report:
   - How many diagrams generated successfully
   - Any failures or quality concerns
4. Ask: "All diagrams generated. Want to review any specific
   diagram or regenerate any?"
5. **STOP and wait for user approval.**
6. If user requests regeneration, update .txt and retry.

---

### Phase 4: Article Writing
**Goal:** Write the full article following the style guide.

1. Run the write-article skill.
2. Wait for completion.
3. Verify drafts/<topic-slug>.md exists.
4. Show user:
   - Title and word count
   - Figure count
   - First 3 paragraphs as preview
   - Self-review checklist results
5. Ask: "Draft complete. Please review the full article at
   drafts/<topic-slug>.md. Any changes needed?"
6. **STOP and wait for user feedback.**
7. If user requests edits, make them and re-present.

---

### Phase 5: Publish Preparation
**Goal:** Format and prepare for final publishing.

1. Run the publish skill.
2. This will present the final article to the user.
3. **STOP. Wait for explicit user approval before any publishing.**

---

## Important Notes
- This skill runs the FULL pipeline. It may take significant time.
- Each phase has its own approval checkpoint.
- The user can interrupt at any phase to make changes.
- If context gets large, suggest clearing between phases.
- Never skip the approval checkpoints.
- Never publish without explicit "yes, publish" from the user.
