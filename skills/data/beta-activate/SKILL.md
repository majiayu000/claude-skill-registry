---
name: beta-activate
description: Activate a beta feature using an activation code
---

# Beta Feature Activation

Activate early access to new Dex features using an activation code.

## Usage

```
/beta-activate [CODE]
```

Or just `/beta-activate` and provide the code when prompted.

---

## Process

### Step 1: Get the Activation Code

If no code was provided with the command, ask:

```
What's your beta activation code?

> Enter your code (e.g., PILAUNCH2026)
```

### Step 2: Validate the Code

Call the beta MCP to validate:

```python
validate_beta_code(code="[USER_CODE]")
```

**If invalid:**

```
That code doesn't match any active beta features.

- Double-check for typos (codes are case-sensitive)
- Make sure you're using a current, unexpired code
- Contact support if you believe this is an error
```

**If valid but already activated:**

```
You've already activated [Feature Name]!

Run `/beta-status` to see your active betas, or `/pi` (example) to use the feature.
```

### Step 3: Activate the Feature

If valid and not yet activated:

```python
activate_beta_feature(code="[USER_CODE]")
```

### Step 4: Show Welcome Message

Display activation confirmation:

```markdown
# Welcome to [Feature Name] Beta!

**Version:** [version]
**Activated:** [timestamp]

## What You Can Do Now

[List capabilities from the feature config]

## Getting Started

[Read and display the instructions file content]

---

Have questions or feedback? Run `/beta-feedback [feature]` anytime.
```

### Step 5: Load Instructions (if available)

Call:

```python
get_beta_instructions(feature="[feature_key]")
```

If instructions exist, display them as part of the welcome message.

---

## Examples

### Example 1: Direct Activation

User: `/beta-activate PILAUNCH2026`

```
# Welcome to Pi Integration Beta!

**Version:** 0.1.0
**Activated:** 2026-02-03 14:32

## What You Can Do Now

- Delegate complex coding tasks to Pi
- Review Pi's work before applying
- Communicate via MCP bridge

## Getting Started

1. Ensure Pi is installed and running
2. Configure the MCP bridge (see System/Beta/pi/README.md)
3. Try your first delegation: "Hey Pi, create a new MCP server for..."

---

Have questions or feedback? Run `/beta-feedback pi` anytime.
```

### Example 2: Prompted Activation

User: `/beta-activate`

```
What's your beta activation code?
```

User: `WRONGCODE`

```
That code doesn't match any active beta features.

- Double-check for typos (codes are case-sensitive)
- Make sure you're using a current, unexpired code
- Contact support if you believe this is an error
```

---

## Error Handling

### No Beta System Configured

If `System/beta-features.yaml` doesn't exist:

```
The beta features system isn't configured yet.

This is a system setup issue. Contact support for assistance.
```

### User Profile Missing

If `System/user-profile.yaml` doesn't exist:

```
You need to complete onboarding before activating beta features.

Run `/setup` to get started with Dex.
```

---

## Notes

- Activation codes are case-sensitive
- Each code unlocks one specific feature
- Activations are permanent (no expiration by default)
- Feature status is stored in `System/user-profile.yaml`
