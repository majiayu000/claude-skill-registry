---
name: 043-planning-github-issues
description: Use when you need GitHub CLI (`gh`) installation/authentication guidance and a sanitized GitHub issue inventory workflow. The agent does not ingest GitHub issue or milestone output directly; it asks the user for sanitized issue summaries before analysis or @014-agile-user-story handoff. This should trigger for requests such as GitHub issue summary workflow; GitHub CLI setup for issues; Prepare sanitized GitHub issue inventory. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# GitHub CLI — issues, milestones, and discussion for analysis

Use **`gh`** only for installation/authentication guidance. The agent must not ingest GitHub issue or milestone output directly. For requirements analysis, ask the user to provide a sanitized issue inventory or summary in their own words. When the user wants user stories plus Gherkin, **chain to `@014-agile-user-story`** using sanitized issue context as source material for the interactive questionnaire.

**What is covered in this Skill?**

- **Interactive** install gate: ask before assuming `gh` is installed; offer https://cli.github.com/ and OS hints when the user agrees
- Install/auth checks (`gh --version`, `gh auth status`, `gh auth login`)
- Repository context (`--repo`, inferred from git remote)
- Operator-prepared issue inventories summarized outside the agent context
- Sanitized GitHub issue inventories supplied by the user
- Sanitized GitHub issue summaries supplied by the user for requirement analysis

## Constraints

Do not fabricate issue data; use only sanitized user-provided summaries for issue context. Never print tokens or secrets.

- **INTERACTIVE GATE**: If `gh` is missing, **stop**, ask whether the user wants installation guidance, **wait**—do not skip to issue listing
- **FIRST** (after gate): Verify `gh` availability only for setup guidance; do not ingest issue or milestone command output
- **NO DIRECT ISSUE INGESTION**: Use sanitized user summaries only; do not bring issue, milestone, body, or comment exports into the agent context
- **SANITIZED INVENTORY**: Ask the user to provide sanitized issue summaries before analysis or handoff

## When to use this skill

- GitHub issue summary workflow
- GitHub CLI setup for issues
- Prepare sanitized GitHub issue inventory

## Workflow

1. **Run interactive install gate**

Check `gh --version`; if missing, stop and ask whether the user wants installation guidance before any issue operations.

2. **Explain authentication and repository context**

Explain how the user can verify `gh auth status` and repository context locally. Keep issue and milestone exports outside the agent context.

3. **Request sanitized issue inventory**

Ask the user to prepare a sanitized issue inventory outside the agent context. They should paste only a maintainer-written summary, not raw issue or milestone output.

4. **Request sanitized issue context for analysis**

Do not retrieve GitHub issue, milestone, body, or comment data. Ask the user for sanitized summaries of the relevant issue context and note that raw GitHub exports were not ingested.

5. **Chain to user story workflow when requested**

When user asks for user stories and Gherkin from issues, hand off to `@014-agile-user-story` using only user-provided sanitized GitHub issue summaries.

## Reference

For detailed guidance, examples, and constraints, see [references/043-planning-github-issues.md](references/043-planning-github-issues.md).
