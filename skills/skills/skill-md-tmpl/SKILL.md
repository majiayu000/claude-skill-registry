---
name: {{skill_name}}
description: "{{description}}"
license: MIT
tier: {{tier}}
allowed-tools:
  - read_file
  - write_file
{{#if tier_2}}
  - run_terminal_cmd
  - grep
{{/if}}
related: [{{related_skills}}]
---

# {{SKILL_NAME}}

> **"{{tagline}}"**

{{extended_description}}

---

## Protocol

### Step 1: {{step_1_name}}

{{step_1_content}}

### Step 2: {{step_2_name}}

{{step_2_content}}

### Step 3: {{step_3_name}}

{{step_3_content}}

---

## Templates

This skill provides:

| Template | Purpose |
|----------|---------|
| `{{template_1}}` | {{template_1_purpose}} |

---

## See Also

- **[../{{related_1}}/](../{{related_1}}/)** — {{related_1_description}}
- **[../{{related_2}}/](../{{related_2}}/)** — {{related_2_description}}

---

*{{closing_wisdom}}*
