---
version: 1.0.0
name: doc-rfc
description: >
  Generate a Request for Comments document from template. Use when the user says
  "write an RFC", "propose a change", "technical proposal", or "I want to discuss
  an approach before building it".
disable-model-invocation: false
user-invocable: true
argument-hint: "[proposal title or topic]"
---

# Generate RFC

## Path Resolution

1. Read `workflow.json` in the project root
2. If it exists and `docsRepo` is `"."`: this IS the docs repo — use local paths
3. If it exists and `docsRepo` is a repo name: resolve via `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>` to get the docs root path. Templates at `<resolved>/templates/`, output to `<resolved>/rfc/`
4. If no `workflow.json`: templates at `templates/`, output to `docs/rfc/`

## Instructions

1. **Resolve paths** (see Path Resolution above)
2. **Read the template** at `<templates>/rfc.md`
3. **Understand the proposal** — ask if needed:
   - What change is being proposed?
   - What's the current state and what's wrong with it?
   - Are there constraints or preferences?
3. **Generate the RFC** filling in all sections:
   - **Summary**: One paragraph, clear and complete
   - **Motivation**: Focus on the "why" — pain points, use cases
   - **Detailed Design**: Be technical and specific
   - **Alternatives**: Include at least 2 real alternatives with honest pros/cons
   - **Drawbacks**: Be genuinely critical of the proposal
4. **Save** to `<output>/[number]-[slug].md` (auto-increment the RFC number)
5. **Assign the next RFC number** by checking existing files in the output directory

## Quality Checklist

- [ ] Summary is self-contained (reader gets the gist without reading further)
- [ ] Motivation explains why NOW (not just why in general)
- [ ] Detailed design is implementable (not hand-wavy)
- [ ] At least 2 alternatives with genuine pros, not strawmen
- [ ] Drawbacks section is honest
- [ ] Unresolved questions are flagged
- [ ] Migration strategy is included if changing existing behavior

## Tips

- An RFC is a discussion document, not a decision record — keep the tone exploratory
- Include code snippets for API changes
- Reference the codebase when describing current state
- If this leads to a decision, create an ADR to record the outcome
