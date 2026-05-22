---
description: Write user-facing documentation for features and products
disable-model-invocation: false
---

# Write User Docs

Create clear, helpful documentation for end users.

## When to Use

- When launching a new feature
- When users are asking support questions
- When creating help center content
- When writing in-app guidance

## Used By

- Customer Support (primary owner)
- Content Creator (writing)
- Product Manager (requirements)
- UI/UX Designer (in-app copy)

---

## Documentation Types

### 1. Help Article
Full documentation for a feature or workflow

### 2. FAQ Entry
Quick answer to common questions

### 3. In-App Guidance
Tooltips, empty states, onboarding text

### 4. Troubleshooting Guide
Steps to resolve common issues

---

## Help Article Template

```markdown
# [Action-Oriented Title]

Brief intro paragraph explaining what this article covers and who it's for.

---

## Before You Start

What users need before following this guide:

- [Prerequisite 1]
- [Prerequisite 2]
- [Account type or permission required]

---

## [Main Task]

### Step 1: [Clear action]

[Explanation of what to do]

![Screenshot placeholder](screenshot-url)

> **Tip**: [Helpful tip for this step]

### Step 2: [Clear action]

[Explanation of what to do]

### Step 3: [Clear action]

[Explanation of what to do]

---

## [Secondary Task] (if applicable)

Steps for related functionality...

---

## Troubleshooting

### [Common Issue 1]

**Problem**: [What the user experiences]

**Solution**:
1. [Step to resolve]
2. [Step to resolve]

### [Common Issue 2]

**Problem**: [What the user experiences]

**Solution**: [How to fix it]

---

## Frequently Asked Questions

**Q: [Common question]?**

A: [Clear answer]

**Q: [Common question]?**

A: [Clear answer]

---

## Related Articles

- [Related Article 1](link)
- [Related Article 2](link)

---

## Need Help?

If you're still having trouble, [contact support](link) and we'll help you out.
```

---

## FAQ Template

```markdown
## [Question in user's words?]

[Direct answer to the question - lead with the answer, not background]

### More Details

[Additional context if needed]

### Related
- [Link to full article if exists]
- [Related FAQ]
```

---

## In-App Copy Guidelines

### Empty States

**Structure**:
1. What this area is for
2. Why it's empty
3. How to fill it

**Example**:
```
No projects yet

Create your first project to start tracking your work.

[Create Project]
```

### Tooltips

**Rules**:
- Keep under 100 characters
- Explain the action, not the obvious
- Include "why" when helpful

**Good**:
```
Export your data as CSV for analysis in other tools
```

**Bad**:
```
Click to export
```

### Error Messages

**Structure**:
1. What happened (briefly)
2. What to do next

**Example**:
```
Couldn't save changes

Check your internet connection and try again.
[Retry]
```

**Anti-patterns**:
```
❌ Error 500
❌ Failed to save
❌ Invalid input
❌ Something went wrong
```

### Confirmation Messages

**Structure**:
1. Confirm what was done
2. Next action (optional)

**Example**:
```
Project created successfully

[View Project] or [Create Another]
```

### Loading States

**Keep it simple**:
```
Loading...
Saving...
Processing...
```

**Or be specific**:
```
Uploading file... 45%
Generating report...
Connecting to [Service]...
```

---

## Writing Principles

### 1. Use Plain Language

**Do**:
- "Click the Save button"
- "Your changes are saved"
- "Enter your email address"

**Don't**:
- "Execute the save operation"
- "Modifications have been persisted"
- "Input your electronic mail identifier"

### 2. Lead with the Action

**Do**:
- "To create a project, click the + button"
- "Export your data from Settings > Export"

**Don't**:
- "The + button, which is located in the top right corner of the interface, can be used to create a new project"

### 3. Use Second Person ("You")

**Do**:
- "Your account"
- "You can export..."
- "Your changes are saved"

**Don't**:
- "The user's account"
- "Users can export..."
- "The changes are saved"

### 4. Be Specific, Not Vague

**Do**:
- "Enter a password with at least 8 characters"
- "This file is 2.4 MB (maximum: 5 MB)"

**Don't**:
- "Enter a secure password"
- "File size must be acceptable"

### 5. Explain Why (When Helpful)

**Do**:
- "Archive this project to free up your dashboard while keeping all data"
- "Set up 2-factor authentication to protect your account"

**Don't**:
- Over-explain obvious actions

---

## Troubleshooting Guide Template

```markdown
# Troubleshooting: [Problem Category]

## Quick Fixes

Try these first:

1. [ ] Refresh the page
2. [ ] Clear browser cache
3. [ ] Try a different browser
4. [ ] Check internet connection

---

## [Specific Problem 1]

### Symptoms
- [What user sees or experiences]
- [Related error messages]

### Cause
[Brief explanation of why this happens]

### Solution

**Option A**: [First solution]
1. [Step 1]
2. [Step 2]

**Option B**: [If Option A doesn't work]
1. [Step 1]
2. [Step 2]

### Prevention
[How to avoid this in the future]

---

## [Specific Problem 2]

[Same structure as above]

---

## Still Having Issues?

If none of the above solutions work:

1. **Collect information**:
   - Browser and version
   - Screenshots of the issue
   - Steps to reproduce

2. **Contact support**:
   - [Support link]
   - Include the information above

---

## Related Articles

- [Related troubleshooting guide]
- [Feature documentation]
```

---

## Documentation Checklist

### Before Publishing

- [ ] Title is action-oriented
- [ ] Language is plain and clear
- [ ] Steps are numbered and specific
- [ ] Screenshots are included (if helpful)
- [ ] Prerequisites are listed
- [ ] Troubleshooting included
- [ ] Related articles linked
- [ ] Tested by someone unfamiliar with feature

### Content Quality

- [ ] Answers the user's question
- [ ] Scannable (headers, bullets, short paragraphs)
- [ ] Accurate and up-to-date
- [ ] Consistent with product UI text
- [ ] Accessible (alt text, clear structure)

### After Publishing

- [ ] Update when product changes
- [ ] Review support tickets for gaps
- [ ] Track page views and search terms
- [ ] Update based on user feedback

---

## Voice and Tone Guide

### Be Helpful
Guide users to success, don't just document features.

### Be Clear
Use simple words, short sentences, direct instructions.

### Be Friendly
Conversational but professional. Not robotic, not too casual.

### Be Confident
"Click Save" not "You might want to click Save"

### Be Respectful
Don't blame users for errors. "Something went wrong" not "You did something wrong"
