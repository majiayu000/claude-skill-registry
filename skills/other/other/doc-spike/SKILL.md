---
version: 1.0.0
name: doc-spike
description: >
  Generate a spike/research report from template. Use when the user says "write up the spike",
  "research report", "document what we found", "investigation results", or "compare options".
disable-model-invocation: false
user-invocable: true
argument-hint: "[research question]"
---

# Generate Spike Report

## Path Resolution

1. Read `workflow.json` in the project root
2. If it exists and `docsRepo` is `"."`: this IS the docs repo — use local paths
3. If it exists and `docsRepo` is a repo name: resolve via `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>` to get the docs root path. Templates at `<resolved>/templates/`, output to `<resolved>/spikes/`
4. If no `workflow.json`: templates at `templates/`, output to `docs/spikes/`

## Instructions

1. **Resolve paths** (see Path Resolution above)
2. **Read the template** at `<templates>/spike.md`
2. **Clarify the research question** — it should be stated as a clear, answerable question
3. **Document findings**:
   - If you performed the research: capture what was found, with evidence
   - If the user did the research: interview them and structure the findings
4. **Generate the spike report**:
   - **Question**: Clear, specific, answerable
   - **Findings**: Organized by topic, each with evidence
   - **Comparison**: Table if comparing options
   - **Recommendation**: Clear and tied back to the question
5. **Save** to `<output>/[slug].md`

## Quality Checklist

- [ ] Question is specific and answerable (not vague)
- [ ] Time-box is stated (spikes are bounded)
- [ ] Each finding has evidence (not just assertions)
- [ ] Comparison table is included if evaluating options
- [ ] Recommendation is clear and justified
- [ ] Open questions are listed (what we still don't know)
- [ ] Next steps are concrete

## Tips

- A spike should answer a question, not build a feature
- Include links to everything consulted (docs, repos, articles)
- If a prototype was built, link to it and describe its limitations
- The recommendation should be actionable: "We should do X because Y"
- If the spike is inconclusive, say so — that's a valid outcome
