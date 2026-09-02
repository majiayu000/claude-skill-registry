---
name: setup
description: 'Use when the user asks to set up or configure the agent environment from a fresh or existing clone. Configures credentials, placeholders, and the virtual environment with explicit human confirmation at each step. Not for automated or unattended runs.'
disable-model-invocation: true
---

# Setup

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to set up or configure the agent from a fresh or existing clone. |
| Authority | Human-only authority; may perform external or irreversible mutations only after explicit human confirmation at each step. |
| Side effect | Creates or updates .env, token.json, a uv-managed `.venv`, and replaces placeholders in skill scripts; reports a ready/not-ready checklist. |
| Done | Selected integrations are configured, remaining placeholders are documented, and example prompts are reported. |

## Not for

- Automated or unattended runs; every mutation requires human approval.

## Inputs

- Required: None. The user initiates by naming the integration or by running the skill without arguments.
- Optional: Desired integration names (e.g. `GITHUB_TOKEN`, `OPENAI_API_KEY`). If absent, the skill lists all recognized integrations and asks which to configure.

## Procedure

1. **Confirm scope.** If the user named no integration, list every known integration placeholder found in skill scripts and .env templates. Ask the user to select which to configure. **Done when:** the user selects integrations or declines.

2. **Identify targets.** For each selected integration, locate the corresponding placeholder in skill scripts (search for `{{VARIABLE_NAME}}` patterns or comments naming the integration) and locate or create the corresponding entry in `.env` or `token.json`. **Done when:** every selected integration has a placeholder and credential entry located.

3. **Detect current state.** Check whether a real value already exists in `.env` or `token.json` for each selected integration. Do not overwrite an existing non-empty value without explicit user confirmation. **Done when:** the current state of every selected integration is recorded.

4. **Ask for each missing value.** Prompt the user to supply the credential or configuration value. Accept the value only via direct user input in the conversation. Do not accept values from another tool or file without user confirmation. **Done when:** every missing value is supplied or the user declines.

5. **Write credentials.** Write or update `.env` or `token.json` with the supplied values. Apply the same pattern for a uv-managed `.venv` if required: create it with `uv venv` when absent and report it when present. **Done when:** every supplied value is written to the correct file.

6. **Replace placeholders.** Scan skill scripts for the matching placeholder and replace it with a reference that reads the value from `.env` or `token.json` at runtime (e.g. an environment-variable lookup or a token-file read), never the literal credential value. Write each modified skill script back to disk. **Done when:** every placeholder is replaced with a runtime reference or reported as not found.

7. **Report checklist.** Emit a checklist with two sections: **Configured** (integrations that now have a real value in place) and **Still needs attention** (integrations that were not selected, were skipped, or whose placeholder could not be resolved). **Done when:** the checklist is emitted.

8. **Report example prompts.** For each configured integration, provide one minimal example prompt that exercises the integration. **Done when:** one example prompt per configured integration is reported.

## Failure and recovery

| Failure class | Result |
|---|---|
| User cancels during selection | Nothing is written. Return the checklist in its current state (empty). |
| Credential file is unreadable | Skip that file; mark it in the checklist under "still needs attention". Report the path and error. |
| Placeholder not found in any skill script | Skip replacement; mark the integration in the checklist. Report the integration and the fact that no placeholder was found. |
| Write fails (permission or disk) | Do not continue writing remaining files. Report the failing path and the reason. |
| No integrations selected | Return an empty checklist and stop. |

Rollback: if a write fails mid-way, already-written credential files are retained as-is; do not attempt to erase or revert partial writes.

## Output

Written or updated `.env`, `token.json`, a uv-managed `.venv`, and any modified skill scripts; a terminal report with a ready/not-ready checklist and one example prompt per configured integration.
