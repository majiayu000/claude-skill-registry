---
version: 1.0.0
name: doc-design
description: >
  Generate a Design Document from template. Use when the user says "write a design doc",
  "technical design", "system design", or "architecture document for this feature".
disable-model-invocation: false
user-invocable: true
argument-hint: "[system or feature name]"
---

# Generate Design Document

## Path Resolution

1. Read `workflow.json` in the project root
2. If it exists and `docsRepo` is `"."`: this IS the docs repo — use local paths
3. If it exists and `docsRepo` is a repo name: resolve via `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>` to get the docs root path. Templates at `<resolved>/templates/`, output to `<resolved>/design/`
4. If no `workflow.json`: templates at `templates/`, output to `docs/design/`

## Instructions

1. **Resolve paths** (see Path Resolution above)
2. **Read the template** at `<templates>/design-doc.md`
3. **Gather context**:
   - Read relevant source code to understand the current architecture
   - Check for existing PRDs, RFCs, or ADRs related to this feature
   - Understand the tech stack and patterns in use
3. **Generate the design doc** with emphasis on:
   - **Architecture**: Include Mermaid C4 diagrams (use `templates/c4-diagrams.md` for syntax)
   - **Component Design**: Detail each component's responsibility and interface
   - **Data Design**: Schema changes, data flow
   - **Cross-cutting concerns**: Security, observability, scalability, reliability
   - **Test Plan**: Concrete testing strategy
4. **Save** to `<output>/[slug].md`

## Quality Checklist

- [ ] Overview is understandable by someone outside the team
- [ ] Goals and non-goals are explicit
- [ ] Architecture includes at least a C4 Context or Container diagram
- [ ] Alternatives section has genuine options (not just "do nothing")
- [ ] Cross-cutting concerns are addressed (security, observability, scalability)
- [ ] Test plan covers unit, integration, and e2e
- [ ] Implementation plan has phased delivery

## Tips

- A design doc is the blueprint — it should be detailed enough that someone else could implement it
- Include C4 diagrams at the appropriate level (Context for new systems, Component for features)
- Link to the PRD for requirements and to ADRs for past decisions
- Call out risks and unknowns explicitly
