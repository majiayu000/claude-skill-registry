---
name: knowledge-base-update
description: >
  Use this skill whenever you learn something important during a conversation:
  a key architectural decision, a project-specific convention, a bug root-cause,
  a 3rd-party API quirk, or any fact that would help a future agent avoid
  re-doing the same research. Writes structured entries to the project's
  knowledge base so that context persists across conversations and agents.
---

<!--
  TÜRKÇE AÇIKLAMA
  ───────────────
  Bu skill, konuşma sırasında öğrenilen önemli bilgilerin kaybolmaması için kullanılır.
  Mimari kararlar, proje kuralları, bug köken nedenleri, 3. parti servis tuzakları veya
  tekrar araştırılmasını istemediğin her şeyi yapılandırılmış biçimde .agent/knowledge/
  dizinine yazar. Böylece gelecekteki agent'lar aynı soruyu sıfırdan araştırmak zorunda kalmaz.

  NE ZAMAN: Önemli bir karar alındığında, sürpriz bir bug çözüldüğünde,
            bir API davranışı belgelendiğinde, yeni bir proje kuralı oluşturulduğunda.
  ÇIKTI:    .agent/knowledge/<slug>.md + INDEX.md satırı
-->

# Knowledge Base Update Skill

## When to Trigger

Activate this skill when any of the following occur:

- An architectural or tech-stack decision is made (and the *why* matters)
- A non-obvious bug is fixed (root cause + fix documented)
- A 3rd-party service/API has a quirk, limit, or gotcha discovered
- A project convention is established (naming, folder structure, patterns)
- A research question is answered after significant investigation
- A "we tried X and it failed because Y" moment happens

## Step-by-Step Process

### 1. Identify the Entry Type

Choose the category that best describes what was learned:

| Type | When to Use |
|------|------------|
| `decision` | Architecture, tech choices, trade-offs |
| `convention` | Naming rules, code patterns, folder structures |
| `bug` | Root cause + fix for a non-obvious problem |
| `gotcha` | 3rd-party quirk, env issue, edge case trap |
| `research` | Answer to a question requiring significant investigation |

### 2. Determine the File Path

Write to: `.agent/knowledge/<slug>.md`

- `slug` = kebab-case summary of the topic (e.g., `auth-token-refresh-strategy`)
- If an entry for this topic already exists, **update it** rather than creating a new file
- Group related topics under subfolders: `.agent/knowledge/auth/`, `.agent/knowledge/infra/`, etc.

### 3. Write the Entry

Use this exact template:

```markdown
---
type: <decision|convention|bug|gotcha|research>
topic: <Short human-readable title>
date: <YYYY-MM-DD>
tags: [<tag1>, <tag2>]
---

## Summary
<One or two sentences — what was learned, bottom line up front>

## Context
<Why this came up. What problem were we solving?>

## Decision / Finding
<The actual content. Be specific. Include code snippets if helpful.>

## Rationale
<Why this choice over alternatives. What alternatives were rejected and why.>

## Consequences
<What does this affect going forward? What to watch out for?>

## References
- <File path, PR link, conversation snippet, or external URL>
```

### 4. Update the Index

After writing the entry, append a one-line summary to `.agent/knowledge/INDEX.md`:

```
| <date> | <type> | [<topic>](./<path>.md) | <one-line summary> |
```

If `INDEX.md` doesn't exist yet, create it with this header first:

```markdown
# Project Knowledge Base

| Date | Type | Topic | Summary |
|------|------|-------|---------|
```

### 5. Confirm to User

After writing, report:
- What was saved and where
- The one-line summary that was added to the index

## Rules

- **Never summarize vaguely.** "We decided to use X" is useless without *why*.
- **Include the anti-pattern.** If something was tried and rejected, document it — that's often the most valuable knowledge.
- **Keep entries atomic.** One topic per file. Don't bundle unrelated decisions.
- **Date is mandatory.** Future agents need to know how fresh this knowledge is.
- **If in doubt, write it.** The cost of a redundant entry is low. The cost of a missing one is re-doing the work.
