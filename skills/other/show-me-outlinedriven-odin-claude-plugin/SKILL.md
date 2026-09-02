---
name: show-me
description: 'Use when the user says show this or diagram this about the current topic. Emits one ephemeral chat visual and nothing on disk. Not for an auditable decision log: use show-me-your-work.'
---

# Show me

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user says show me or diagram this about the current topic. |
| Authority | Read-only: no file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Emits an ephemeral visual in chat; no files on disk. |
| Done | One (or at most two) smallest views carrying the point, beside its short supporting text. |

## Not for

- An auditable decision trail for unattended work: use show-me-your-work.
- A committed diagram in a document: use embed-diagram.
- An interactive clickable sketch: use prototype-logic.
- Teaching a concept with explanation and examples: use explain-concept.
- A visual walk of review findings one at a time: use show-review.
- A guided multi-turn exploration: use walk-with-me.

## Inputs

The current topic from the user prompt. The skill picks the minimal view type that answers it.

## Procedure

1. Identify the single concept the user asks to see. If the topic is too broad for one visual, ask the user to narrow it before producing more than two views. **Done when:** one concept is identified or the user is asked to narrow.
2. Pick the smallest view that carries the point:

   | The point is | View |
   |---|---|
   | How something works step by step | Pseudocode |
   | Who calls what | Call tree |
   | Component hierarchy | Component tree, naming the file that owns each boundary |
   | What lives where | Shallow file tree, one comment per directory saying what it owns |
   | Relationships or flow | Diagram (Mermaid or nomnoml) |
   | The code itself | Whole block |

   **Done when:** the view type is chosen.
3. Render the view using the appropriate shape. **Done when:** the view is rendered in chat.
4. Shape diffs to match the view they change: a component diff for UI changes, a file-layout diff for file organization, a call-tree diff for call-graph changes, and a pseudocode diff for control-flow changes. **Done when:** the diff matches its view type or no diff is needed.
5. Place each visual adjacent to the short supporting text, not in its own trailing block. **Done when:** the visual sits beside its context.

## Failure and recovery

- Rendering impossible in text format: return the concept in prose instead of a visual.
- Topic too broad for one visual: ask the user to narrow the scope before generating more than two views.
- **Request requires a committed diagram, interactive sketch, concept teaching, review walk, or multi-turn exploration:** stop and name the skill that handles it (see Not for).

## Output

An ephemeral visual shown inline beside its short supporting text; the visual carries the point alone, prose supplies only context the visual cannot; nothing is written to disk.
