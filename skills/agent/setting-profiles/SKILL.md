---
name: setting-profiles
description: Use this skill when switch model profile for kata agents (quality/balanced/budget). Triggers include "set profile", "set profile".
metadata:
  version: "0.1.0"
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Bash
---

<user_command>/kata:set-profile</user_command>


<objective>
Switch the model profile used by Kata agents. This controls which Claude model each agent uses, balancing quality vs token spend.
</objective>

<profiles>
| Profile      | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| **quality**  | Opus everywhere except read-only verification                  |
| **balanced** | Opus for planning, Sonnet for execution/verification (default) |
| **budget**   | Sonnet for writing, Haiku for research/verification            |
</profiles>

<process>

## 1. Validate argument

```
if $ARGUMENTS.profile not in ["quality", "balanced", "budget"]:
  Error: Invalid profile "$ARGUMENTS.profile"
  Valid profiles: quality, balanced, budget
  STOP
```

## 2. Check for project

```bash
ls .planning/config.json 2>/dev/null
```

If no `.planning/` directory:
```
Error: No Kata project found.
Run /kata:new-project first to initialize a project.
```

## 3. Update config.json

Read current config:
```bash
cat .planning/config.json
```

Update `model_profile` field (or add if missing):
```json
{
  "model_profile": "$ARGUMENTS.profile"
}
```

Write updated config back to `.planning/config.json`.

## 4. Confirm

```
✓ Model profile set to: $ARGUMENTS.profile

Agents will now use:
[Show table from model-profiles.md for selected profile]

Next spawned agents will use the new profile.
```

</process>

<examples>

**Switch to budget mode:**
```
/kata:set-profile budget

✓ Model profile set to: budget

Agents will now use:
| Agent         | Model  |
| ------------- | ------ |
| kata-planner  | sonnet |
| kata-executor | sonnet |
| kata-verifier | haiku  |
| ...           | ...    |
```

**Switch to quality mode:**
```
/kata:set-profile quality

✓ Model profile set to: quality

Agents will now use:
| Agent         | Model  |
| ------------- | ------ |
| kata-planner  | opus   |
| kata-executor | opus   |
| kata-verifier | sonnet |
| ...           | ...    |
```

</examples>
