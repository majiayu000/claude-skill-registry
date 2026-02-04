---
name: beta-status
description: View your activated beta features and their status
---

# Beta Status

Show all activated beta features and their current status.

## Usage

```
/beta-status
```

---

## Process

### Step 1: Get Beta Status

Call the beta MCP:

```python
get_beta_status()
```

### Step 2: Display Results

**If no betas activated:**

```markdown
# Beta Features

You haven't activated any beta features yet.

## Available Betas

[Call list_available_betas() and show available features]

Got an activation code? Run `/beta-activate [CODE]` to unlock a feature.
```

**If betas are activated:**

```markdown
# Your Beta Features

You have **[N] beta feature(s)** activated.

---

## [Feature Name]

- **Status:** Active
- **Version:** [version]
- **Activated:** [date]
- **Capabilities:** [list capabilities]

[Repeat for each activated feature]

---

## Quick Actions

- `/beta-feedback [feature]` - Share your thoughts
- `/beta-activate [code]` - Activate another feature

---

*Feedback submitted: [N] time(s)*
```

### Step 3: Check for Updates

Compare `version_at_activation` with current version:

If feature has been updated since activation:

```
**Note:** [Feature Name] has been updated from v[old] to v[new] since you activated.
Check the instructions for what's new.
```

---

## Examples

### Example 1: Active Betas

```markdown
# Your Beta Features

You have **1 beta feature** activated.

---

## Pi Integration

- **Status:** Active
- **Version:** 0.1.0
- **Activated:** 2026-02-03
- **Capabilities:**
  - Delegate tasks to Pi
  - Review Pi's work
  - MCP bridge communication

---

## Quick Actions

- `/beta-feedback pi` - Share your thoughts
- `/beta-activate [code]` - Activate another feature

---

*Feedback submitted: 0 times*
```

### Example 2: No Betas

```markdown
# Beta Features

You haven't activated any beta features yet.

## Available Betas

There is **1 beta feature** available:

### Pi Integration
Self-extending AI capabilities via Pi coding agent.

Got an activation code? Run `/beta-activate [CODE]` to unlock a feature.
```

---

## Notes

- Status is read from `System/user-profile.yaml`
- Feature config is read from `System/beta-features.yaml`
- Feedback count includes all submissions for all features
