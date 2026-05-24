---
name: agr-feedback
description: Submit feedback, bug reports, or feature requests for agr/agrx. Use with `-i "your feedback"` to enter interactive mode where Claude helps refine and structure your feedback before opening a pre-filled GitHub issue for submission.
---

# agr Feedback

Help users submit high-quality feedback for agr/agrx by refining their input through conversation, then opening a pre-filled GitHub issue.

## Usage

```bash
agrx agr-feedback -i "initial feedback here"
```

## Workflow

### Step 1: Acknowledge and Understand

When the user provides initial feedback, reflect back your understanding:

1. Identify the **feedback type**:
   - `bug` - Something isn't working as expected
   - `feature` - A new capability or enhancement
   - `ux` - Confusing behavior or unclear messaging
   - `docs` - Documentation missing or unclear
   - `question` - Clarification needed (may convert to other type)

2. Summarize what you understand from their initial message
3. Note any ambiguity or missing context

**Example response:**
```
I understand you're experiencing [issue/wanting feature]. It sounds like a [type].

To help me capture this clearly, I have a few questions:
```

### Step 2: Ask Clarifying Questions

Ask 2-4 focused questions to gather actionable details. Tailor questions to feedback type:

**For bugs:**
- What command did you run?
- What did you expect to happen?
- What actually happened?
- Can you reproduce it consistently?

**For features:**
- What problem would this solve for you?
- How do you currently work around this?
- What would the ideal behavior look like?

**For UX issues:**
- What were you trying to accomplish?
- Where did you get stuck or confused?
- What would have been clearer?

**For docs:**
- What were you looking for?
- Where did you look?
- What information was missing?

### Step 3: Present Formatted Feedback

After gathering details, present the structured feedback for approval:

```markdown
---
## Feedback Preview

**Type:** [Bug / Feature Request / UX Improvement / Documentation]

**Title:** [Concise summary - max 60 chars]

### Description
[2-3 sentence summary of the issue/request]

### Details
[Structured details based on feedback type]

### Context
- agr version: [if relevant]
- OS: [if relevant]
- Additional context: [if provided]

---

Does this accurately capture your feedback? (yes/edit/cancel)
```

### Step 4: Open GitHub Issue

When user approves, construct and open the URL:

**Repository:** `https://github.com/kasperjunge/agent-resources`

**URL format:**
```
https://github.com/kasperjunge/agent-resources/issues/new?title={encoded_title}&body={encoded_body}&labels={label}
```

**Labels by type:**
- bug → `bug`
- feature → `enhancement`
- ux → `ux`
- docs → `documentation`

**Construct the body:**
```markdown
## Description
{description}

## Details
{details}

## Context
{context}

---
*Submitted via `agrx agr-feedback`*
```

**Open the URL:**
```bash
# macOS
open "{constructed_url}"

# Linux
xdg-open "{constructed_url}"

# Windows
start "{constructed_url}"
```

After opening, inform the user:
```
Opened GitHub in your browser with the pre-filled issue.
Review and click "Submit new issue" when ready.
```

## Important Notes

- **URL encoding**: All text in URL parameters must be URL-encoded
- **URL length limit**: Keep total URL under 2000 characters. If feedback is long, truncate context section and note "See full details in description"
- **No auth required**: The browser handles GitHub authentication
- **User control**: Never auto-submit - user clicks the final submit button

## Example Conversation

**User runs:** `agrx agr-feedback -i "sync command is confusing when there are conflicts"`

**Claude:**
```
I understand you're finding the sync command's conflict handling confusing.
This sounds like a UX issue.

To help me capture this clearly:

1. What happened when you ran `agr sync` with conflicts?
2. What behavior or messaging would have been clearer?
3. Were you syncing skills, commands, or both?
```

**User:** "It just said 'conflict detected' but didn't tell me which file or what to do about it"

**Claude:**
```
Got it - the error message lacks actionable detail. Here's the formatted feedback:

---
## Feedback Preview

**Type:** UX Improvement

**Title:** Improve conflict error messages in agr sync

### Description
When `agr sync` detects conflicts, the error message says "conflict detected"
without specifying which file has the conflict or how to resolve it.

### Details
- Current behavior: Generic "conflict detected" message
- Expected: Show which file(s) have conflicts and suggest resolution steps
- Impact: Users can't determine what action to take

### Context
- Command: `agr sync`
- Scenario: Local edits conflict with source

---

Does this accurately capture your feedback? (yes/edit/cancel)
```

**User:** "yes"

**Claude:** *Opens browser with pre-filled issue*
```
Opened GitHub in your browser with the pre-filled issue.
Review and click "Submit new issue" when ready.

Thank you for helping improve agr!
```
