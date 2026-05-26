---
name: aitask-refresh-code-models
description: Research latest AI code agent models via web and update models_*.json configuration files.
---

## Workflow

### Step 1: Read Current Model Configurations

Read all model config files and the project defaults:

1. Use `Glob` to find all `aitasks/metadata/models_*.json` files
2. Read each file to get the current model list per agent
3. Read `aitasks/metadata/codeagent_config.json` to identify which models are configured as defaults for each operation (these will be marked "IN USE" in the change report)

Extract the agent name from each filename: `models_claudecode.json` → `claudecode`, `models_geminicli.json` → `geminicli`, etc.

### Step 2: Select Agents to Update

Present the discovered agents to the user for selection.

Use `AskUserQuestion` (multiSelect):
- Question: "Which code agents do you want to refresh models for?"
- Header: "Agents"
- Options:
  - "All agents" (description: "Refresh models for all discovered agents")
  - One option per discovered agent (label: agent name, description: "N models currently configured")

If "All agents" is selected, process all discovered agents. Otherwise, process only the selected agents.

### Step 3: Research Latest Models

Process each selected agent sequentially. For each agent:

1. **WebSearch** with a targeted query based on the agent (see Research Queries below)
2. **WebFetch** on the canonical documentation URLs listed in the Research URLs section
3. Extract from the results:
   - Model display names
   - CLI model IDs (the exact string passed to `--model` or `-m` flag)
   - Brief descriptions and capability notes
   - Release status (stable, preview, deprecated)
4. Focus on models suitable for **coding and agentic tasks** only — skip embedding models, vision-only models, audio models, etc.

If a WebFetch URL fails (404, redirect to different content), fall back to WebSearch results. If WebSearch also returns no relevant results for an agent, report "No updates found for \<agent\>" and continue to the next agent.

**OpenCode special handling:** OpenCode models are discovered exclusively via CLI — web research is NOT used. If `opencode` is selected:
1. Check if the `opencode` binary is available: `command -v opencode`
2. If available, run the discovery script directly: `bash .aitask-scripts/aitask_opencode_models.sh`
3. The script handles all discovery, merging, and updating of `aitasks/metadata/models_opencode.json`
4. Models no longer available from connected providers are marked `"status": "unavailable"` (never deleted, verified scores preserved)
5. If `opencode` is NOT installed, inform the user: "OpenCode binary not found — cannot refresh OpenCode models. Install OpenCode first." and skip OpenCode.

#### Research Queries

Use generic terms — do NOT hardcode year references:

- **Claude**: `"Anthropic Claude models API model IDs latest"`
- **Gemini**: `"Google Gemini API models latest available"`
- **Codex**: `"OpenAI Codex CLI models latest"`
- **OpenCode**: Uses CLI discovery only (see below) — web research is NOT used for OpenCode

### Step 4: Compare Current vs. Discovered

For each selected agent, compare the current `models_*.json` content against the web research results. Categorize each model:

 - **NEW**: Discovered in web research but not present in current config (match by `cli_id`). Generate:
   - `name`: following the naming convention (see Model Naming Convention below)
   - `cli_id`: exact API/CLI model ID from documentation
   - `notes`: brief description from documentation
   - `verified`: `{ "pick": 0, "explain": 0, "batch-review": 0 }`
   - `verifiedstats`: `{}`

- **UPDATED**: Model exists in config but notes/status changed significantly (e.g., moved from preview to stable, description updated). Propose updated `notes` field.

- **DEPRECATED?**: Model exists in config but was NOT found in current documentation. Flag as potentially deprecated — do NOT automatically remove.

- **UNCHANGED**: Model exists in both config and documentation with no significant changes.

### Step 5: Present Changes to User

Display a structured change report. For each selected agent:

```
### <Agent Name>
- NEW: <cli_id> (<proposed_name>) — "<notes>"
- UPDATED: <cli_id> (<name>) — notes changed: "<old>" → "<new>"
- DEPRECATED?: <cli_id> (<name>) — not found in current docs
- UNCHANGED: <cli_id> (<name>) [IN USE: pick, explain]
```

Mark models as `[IN USE: <operations>]` if they appear in `codeagent_config.json` defaults.

If no changes were found for any agent, inform the user and end the workflow.

Use `AskUserQuestion`:
- Question: "Review the model update report above. How would you like to proceed?"
- Header: "Update"
- Options:
  - "Apply all changes" (description: "Add new models and update changed notes. Do not remove deprecated.")
  - "Apply selectively" (description: "Choose which changes to apply per agent")
  - "Apply and remove deprecated" (description: "Add new, update changed, AND remove deprecated models")
  - "Abort" (description: "No changes will be made")

**If "Apply selectively":** For each agent that has changes, use `AskUserQuestion` (multiSelect) to let the user pick which specific changes to apply.

**If "Abort":** End the workflow.

### Step 6: Update JSON Files

For each agent with approved changes:

1. Read the current `aitasks/metadata/models_<agent>.json`
2. Apply the approved changes:
   - **Add new models**: Append to the `models` array
   - **Update notes**: Modify the `notes` field for updated models
   - **Remove deprecated** (only if explicitly approved): Remove from the array
3. **Preserve all existing `verified` scores and `verifiedstats` data** for unchanged and updated models
4. Write the updated JSON back to `aitasks/metadata/models_<agent>.json`
    - Maintain 2-space indentation
    - Maintain field ordering used by the existing file when possible; current files may include `status`, `verified`, and `verifiedstats`

For new models, initialize both `verified` and `verifiedstats` even if no feedback has been recorded yet.

**Seed sync (conditional):**
- Check if the `seed/` directory exists in the repository root
- If it exists, copy each updated `models_<agent>.json` to `seed/models_<agent>.json`
- If `seed/` does not exist, skip this step

### Step 7: Verify Research URLs

After updating model files, verify that the research URLs listed in this SKILL.md are still reachable.

For each URL in the Research URLs section:
- Use `WebFetch` with prompt: "Is this page accessible? Return the page title and a one-line summary."
- If a URL returns an error (404, connection failure, or redirects to unrelated content):
  - Report to the user: "Research URL \<url\> appears to be broken or has changed. Consider updating the SKILL.md."

This step is **informational only** — do not automatically edit the SKILL.md. The user should manually review and update URLs if needed.

### Step 8: Commit

Stage and commit the changes using the appropriate git commands:

**Metadata files** (task data branch):
```bash
./ait git add aitasks/metadata/models_claudecode.json aitasks/metadata/models_geminicli.json aitasks/metadata/models_codex.json aitasks/metadata/models_opencode.json
./ait git commit -m "ait: Refresh code agent model configurations"
```

Only include files that were actually modified — skip unchanged agent files.

**Seed files** (main branch, only if `seed/` exists and files were updated):
```bash
git add seed/models_claudecode.json seed/models_geminicli.json seed/models_codex.json seed/models_opencode.json
git commit -m "ait: Sync refreshed models to seed templates"
```

Display summary: "Model configurations updated. N new models added, M models updated, K models flagged as deprecated."

### Step 9: Satisfaction Feedback

Execute the **Satisfaction Feedback Procedure** (see `.claude/skills/task-workflow/satisfaction-feedback.md`) with `skill_name` = `"refresh-code-models"`.

## Model Naming Convention

When generating `name` fields for new models, follow these rules:

- **Lowercase only**, no uppercase letters
- **Underscores** replace dots, hyphens, and spaces (e.g., Opus 4.6 → `opus4_6`)
- **Version numbers** are concatenated without separators (e.g., 3.1 → `3_1`, 2.5 → `2_5`)
- **No dots** in the name field (dots are only in `cli_id`)
- **Suffix conventions**: `_preview` for preview models, `_max` for max-context variants, `_flash` for flash/fast variants

Examples:
| Display Name | name | cli_id |
|---|---|---|
| Claude Opus 4.6 | `opus4_6` | `claude-opus-4-6` |
| Gemini 2.5 Pro | `gemini2_5pro` | `gemini-2.5-pro` |
| GPT-5.3 Codex Spark | `gpt5_3codex_spark` | `gpt-5.3-codex-spark` |
| Kimi K2.5 | `kimi_k2_5` | `kimi-k2.5` |

## Research URLs

These URLs are used during the web research phase (Step 3). They are checked for validity in Step 7 and should be updated if they become stale.

### Claude (Anthropic)
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://platform.claude.com/docs/en/about-claude/models/all-models
- Key info: Claude Code uses `--model` flag. Prefer explicit versioned IDs (e.g., `claude-opus-4-6`) over aliases (`opus`).

### Gemini (Google)
- https://ai.google.dev/gemini-api/docs/models
- https://github.com/google-gemini/gemini-cli/discussions
- Key info: Gemini CLI uses `-m` flag. Model IDs may include `-preview` suffix.

### Codex (OpenAI)
- https://platform.openai.com/docs/models
- https://developers.openai.com/codex/models/
- Key info: Codex CLI uses `-m` flag. Models are GPT-based codex variants.

### OpenCode
- https://opencode.ai/docs/providers/
- https://github.com/anomalyco/opencode
- Key info: OpenCode uses `--model` flag. Provider-based model IDs from multiple AI providers.

## Notes

- This skill uses Claude's built-in `WebSearch` and `WebFetch` tools — no external scripts needed
- The skill never auto-removes models. Deprecated flags are informational only; removal requires explicit user approval
- When updating, existing `verified` scores and `verifiedstats` history are always preserved — only new models get all-zero scores and empty stats objects
- Both `aitasks/metadata/` (via `./ait git`) and `seed/` (via plain `git`) are updated when applicable
- If web research fails for a specific agent, the skill continues with other agents rather than aborting
- The self-update URL check (Step 7) only reports issues — it does not modify this SKILL.md automatically
