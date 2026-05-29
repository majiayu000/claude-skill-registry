---
name: epic-postmortem
description: Create or update epic retrospective documents. Use when user mentions "postmortem", "post-mortem", "post mortem", "retrospective", or "retro" for a completed epic or feature. Distinct from workflow-postmortem which tracks execution issues.
---

# Epic Postmortem Skill

**Purpose:** Document learnings from completed epics/features for team improvement
**Output:** `docs/epics/backlog/{project-code}-{epic-code}-post-mortem.md` in metasaver-marketplace repo

---

## Modes

| Mode     | When to Use               | Action                      |
| -------- | ------------------------- | --------------------------- |
| `create` | New post-mortem for epic  | Generate from template      |
| `update` | Add learnings to existing | Append to relevant sections |

---

## Workflow

### Mode: create

1. **Gather info:** Ask user for project code, epic code, epic description
2. **Validate:** Check file does not already exist at target path
3. **Generate:** Use template from `templates/post-mortem-template.md`
4. **Interview:** Prompt user for each section (what went well, wrong, learnings)
5. **Write:** Save to `docs/epics/backlog/{project}-{epic}-post-mortem.md`
6. **Confirm:** Report file path to user

### Mode: update

1. **Locate:** Find existing post-mortem by project-epic code
2. **Read:** Load current content
3. **Interview:** Ask user what new learnings to add
4. **Append:** Add entries to appropriate sections with timestamp
5. **Save:** Write updated file
6. **Confirm:** Report changes to user

---

## File Naming Convention

**Pattern:** `{project-code}-{epic-code}-post-mortem.md`

| Component    | Format    | Example |
| ------------ | --------- | ------- |
| project-code | 2-4 chars | `msc`   |
| epic-code    | 2-4 chars | `lct`   |

**Examples:**

- `msc-lct-post-mortem.md` (MetaSaver Com - Listing Contacts)
- `chb-air-post-mortem.md` (Chatbot - AI Routing)

---

## Output Location

**Repository:** metasaver-marketplace (centralized)
**Path:** `docs/epics/backlog/`

---

## Template Sections

See `templates/post-mortem-template.md` for full structure:

| Section         | Purpose                            |
| --------------- | ---------------------------------- |
| Epic Info       | Project, code, description, dates  |
| What Went Well  | Successes to repeat                |
| What Went Wrong | Failures to avoid                  |
| Learnings       | Actionable improvements for future |
| Action Items    | Specific follow-ups with owners    |

---

## Examples

**Create new post-mortem:**

```
User: "Create a postmortem for the MSC listing contacts epic"

Agent:
1. Asks: "What is the epic code?" -> "lct"
2. Asks: "Brief description?" -> "CRUD for listing contacts"
3. Asks: "What went well?" -> user provides bullet points
4. Asks: "What went wrong?" -> user provides bullet points
5. Asks: "Key learnings?" -> user provides bullet points
6. Asks: "Action items?" -> user provides with owners
7. Writes: docs/epics/backlog/msc-lct-post-mortem.md
```

**Update existing post-mortem:**

```
User: "Add learnings to the MSC-LCT post-mortem"

Agent:
1. Reads: docs/epics/backlog/msc-lct-post-mortem.md
2. Asks: "What new learnings to add?"
3. Appends: New entries with timestamp
4. Saves: Updated file
```

---

## Distinction from workflow-postmortem

| Aspect       | epic-postmortem                | workflow-postmortem                |
| ------------ | ------------------------------ | ---------------------------------- |
| **Scope**    | Project/epic retrospective     | Single workflow execution          |
| **Content**  | Team learnings, process issues | Agent mistakes, skipped steps      |
| **Location** | `docs/epics/backlog/`          | `docs/epics/in-progress/{folder}/` |
| **Trigger**  | User request after epic done   | Automatic during /build, /ms       |
| **Audience** | Team/stakeholders              | Developer debugging workflows      |

<!-- Trigger version bump test: 2026-01-07 -->
