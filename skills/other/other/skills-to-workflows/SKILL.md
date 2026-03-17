---
name: skills_to_workflows
description: "Sync or migrate skills from `.codex/skills/` to `.agent/workflows/`. Converts directory-based skills into flat markdown workflow files. Use when you need to update the agent's available workflows from the core skill repository."
---

# Skills to Workflows Sync

This workflow automates the process of converting complex skill structures into flat workflow files for the agent.

## Process Overview

1.  **Identify Sources**: Check `.codex/skills/` for all available skill directories.
2.  **Mapping**: Each directory (e.g., `01-step-one`) corresponds to a workflow file (`01-step-one.md`).
3.  **Extraction**: The content of `SKILL.md` inside each directory is copied to the workflow file.

## CLI Execution

Run the following command in the project root to perform a full sync:

```bash
# Ensure target directory exists
mkdir -p .agent/workflows

# Sync all SKILL.md files to .agent/workflows/ as {foldername}.md
for dir in .codex/skills/*/; do
    foldername=$(basename "$dir")
    cp "$dir/SKILL.md" ".agent/workflows/$foldername.md"
done
```

## Verification

After sync, verify the workflows are recognized by listing the directory:

```bash
ls -la .agent/workflows
```

## When to Use
- After creating a new skill in `.codex/skills/`.
- When you want to "publish" local skills to the agentic workflow system.
- To ensure consistency between different agents that might prefer one format over the other.