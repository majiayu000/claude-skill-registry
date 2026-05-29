---
name: proposal-review
description: Facilitate methodical review of proposals (technical designs, product specs, feature requests). Use when asked to "review this proposal", "give feedback on this doc", "help me review this RFC", or when presented with a document that needs structured feedback. Handles markdown files, GitHub gists/issues/PRs, and other text formats. Chunks proposals intelligently, predicts reviewer reactions, and produces feedback adapted to the proposal's format.
---

# Proposal Review

Methodically review proposals by chunking content, predicting feedback, and producing actionable output for the proposer.

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. INTAKE: Read entire proposal, identify source format    │
├─────────────────────────────────────────────────────────────┤
│  2. CHUNK: Split into reviewable sections (smart hybrid)    │
├─────────────────────────────────────────────────────────────┤
│  3. REVIEW LOOP: For each chunk:                            │
│     • Present chunk content                                 │
│     • Predict 3-4 likely reactions                          │
│     • Use AskUserQuestion for feedback                      │
│     • Record response                                       │
├─────────────────────────────────────────────────────────────┤
│  4. SYNTHESIZE: Compile feedback, infer overall sentiment   │
├─────────────────────────────────────────────────────────────┤
│  5. OUTPUT: Generate feedback document matching source      │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: Intake

Read the entire proposal. Identify:

- **Source format**: Local file, GitHub PR/issue/gist, Google Doc export, etc.
- **Structure**: Headers, sections, numbered lists, or flowing prose
- **Length**: Estimate chunk count (aim for 3-8 chunks for typical proposals)

Do not summarize or share initial impressions. Proceed directly to chunking.

## Phase 2: Chunking Strategy

Use smart hybrid chunking:

| Proposal Structure | Chunking Approach |
|-------------------|-------------------|
| Clear headers/sections | One chunk per major section |
| Large section (>500 words) | Split at natural paragraph breaks |
| Small adjacent sections (<100 words each) | Merge into single chunk |
| Numbered lists of items | Group 3-5 related items per chunk |
| Flowing prose without structure | Split at topic transitions (~300-400 words) |

**Chunk ordering**: Present in document order unless there's a clear dependency (e.g., "Alternatives" before "Proposed Solution" if alternatives inform the solution review).

## Phase 3: Review Loop

For each chunk:

### 3.1 Present the Chunk

Quote or summarize the chunk content. For longer chunks, quote key sentences and summarize the rest. Use a clear header like:

```
### Chunk 2 of 5: Technical Architecture
```

### 3.2 Predict Reactions

Generate 3-4 predicted reactions spanning these categories:

| Category | Example Predictions |
|----------|-------------------|
| **Clarification** | "This is unclear—what does X mean?", "How does this interact with Y?" |
| **Concern** | "This scope seems too large", "Have you considered Z risk?" |
| **Approval** | "This approach makes sense", "Good tradeoff analysis" |
| **Suggestion** | "Consider alternative A", "This needs more detail on B" |

Select predictions that feel most relevant to this specific chunk. Not every chunk needs all categories.

### 3.3 Collect Feedback

Use AskUserQuestion with:
- Predicted reactions as options (2-4 most likely)
- User can select one OR provide custom feedback via "Other"
- Keep option labels concise (under 10 words), use description for detail

Example:

```
question: "What's your reaction to this technical architecture section?"
header: "Architecture"
options:
  - label: "Looks good"
    description: "The proposed architecture is sound and well-reasoned"
  - label: "Scope concern"
    description: "This feels too ambitious for the timeline"
  - label: "Need clarification"
    description: "Some technical details are unclear or missing"
  - label: "Consider alternative"
    description: "There may be a simpler or better approach"
```

### 3.4 Record Response

Store each response with:
- Chunk identifier (number + title)
- Selected option or custom text
- Any quoted content the feedback references

## Phase 4: Synthesis

After all chunks reviewed:

1. **Group feedback by theme**: Consolidate similar concerns across chunks
2. **Infer overall sentiment**: Based on feedback distribution:
   - Mostly approvals → Positive with minor suggestions
   - Mixed → Conditional support, needs revisions
   - Mostly concerns → Significant issues to address
3. **Identify patterns**: Note if same concern appears multiple times

Then ask:

```
question: "Would you like me to include suggested next steps for the proposer?"
header: "Next Steps"
options:
  - label: "Yes, include action items"
    description: "Generate concrete next steps based on feedback"
  - label: "No, just the feedback"
    description: "Keep output to observations and reactions only"
```

## Phase 5: Output Generation

Adapt output format to source:

| Source | Output Format |
|--------|--------------|
| GitHub PR | PR review comment with quoted lines and threaded feedback |
| GitHub Issue | Comment with sections matching issue structure |
| Markdown file | Companion `*-feedback.md` with inline references |
| Google Doc | Structured comment list with section references |
| Generic/unknown | Structured markdown with clear sections |

### Output Structure

```markdown
## Feedback Summary

**Overall**: [Inferred sentiment - 1 sentence]

## Section-by-Section Feedback

### [Section Name]
[Feedback with quotes where relevant]

### [Section Name]
...

## Key Themes
- [Theme 1]: [Consolidated feedback]
- [Theme 2]: ...

## Next Steps (if requested)
- [ ] [Action item 1]
- [ ] [Action item 2]
```

### Tone Guidelines

- Direct but constructive
- Quote specific text when critiquing
- Frame concerns as questions when possible ("Have you considered..." vs "This won't work")
- Acknowledge what works, not just what doesn't

## Edge Cases

**Very short proposals (<300 words)**: Skip chunking, review as single unit with 4-5 predicted reactions.

**Very long proposals (>3000 words)**: Cap at 8-10 chunks. Merge aggressively or offer to focus on specific sections.

**Unclear structure**: Ask user which sections matter most before chunking.

**Multiple proposals**: Review one at a time. Ask user for order preference if not obvious.
