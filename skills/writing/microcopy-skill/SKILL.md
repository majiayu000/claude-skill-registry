---
document_name: "microcopy.skill.md"
location: ".claude/skills/microcopy.skill.md"
codebook_id: "CB-SKILL-MICROCOPY-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for UI microcopy"
skill_metadata:
  category: "content"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Voice & tone guidelines"
    - "UI/UX context"
category: "skills"
status: "active"
tags:
  - "skill"
  - "content"
  - "microcopy"
  - "ui"
ai_parser_instructions: |
  This skill defines procedures for UI microcopy.
  Used by Copywriter agent.
---

# Microcopy Skill

=== PURPOSE ===

Procedures for creating effective UI microcopy.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(copywriter) @ref(CB-AGENT-COPY-001) | Primary skill for UI text |

=== PROCEDURE: Button Labels ===

**Primary Actions:**
| Pattern | Example | Usage |
|---------|---------|-------|
| Verb | Save | Simple action |
| Verb + Object | Add item | Clarify target |
| Affirmative | Yes, delete | Confirmation |

**Best Practices:**
```
✓ Save
✓ Create project
✓ Send message
✓ Yes, delete it

✗ Submit (vague)
✗ Click here (unhelpful)
✗ OK (unclear)
✗ Do it (unprofessional)
```

**Button Pairs:**
| Primary | Secondary |
|---------|-----------|
| Save | Cancel |
| Confirm | Go back |
| Delete | Keep |
| Yes, continue | No, cancel |

=== PROCEDURE: Form Labels ===

**Label Guidelines:**
```
✓ Email address (clear)
✗ Email (ambiguous - is it input or display?)

✓ Password (8+ characters) (helpful)
✗ Password (missing requirement info)

✓ Company name (optional) (clarifies optional)
✗ Company (unclear if required)
```

**Placeholder Text:**
- Use for examples, not labels
- Format: "e.g., john@example.com"
- Don't duplicate the label

**Help Text:**
```
Field: Password
Help: At least 8 characters, including a number

Field: Username
Help: Letters, numbers, and underscores only
```

=== PROCEDURE: Error Messages ===

**Formula:**
1. What happened (briefly)
2. Why (if helpful)
3. How to fix

**Examples:**
```
✓ "Email already registered. Try signing in instead."
✗ "Error: Duplicate entry."

✓ "Password must be at least 8 characters."
✗ "Invalid password."

✓ "Couldn't connect. Check your internet and try again."
✗ "Network error."

✓ "Card declined. Try a different payment method."
✗ "Transaction failed."
```

**Error Message Checklist:**
- [ ] Uses plain language
- [ ] Explains the problem
- [ ] Suggests a solution
- [ ] Is specific (not generic)
- [ ] Doesn't blame the user

=== PROCEDURE: Success Messages ===

**Patterns:**
```
Completion: "Project created!"
Progress: "Changes saved."
Confirmation: "Email sent to john@example.com"
```

**Guidelines:**
- Keep it brief
- Be specific when helpful
- Match the tone to the action
- Include next steps if relevant

=== PROCEDURE: Empty States ===

**Formula:**
1. What's missing (headline)
2. Why it matters (optional)
3. How to fix (CTA)

**Template:**
```
Headline: No [items] yet
Subtext: [Brief explanation or benefit]
CTA: [Create/Add first item]
```

**Examples:**
```
# No projects yet
Get started by creating your first project.
[Create project]

# No messages
You're all caught up!
(no CTA needed)

# No results found
Try adjusting your search or filters.
[Clear filters]
```

=== PROCEDURE: Tooltips & Help ===

**Tooltip Guidelines:**
- Maximum 150 characters
- Answer "What is this?" or "Why?"
- Don't repeat the label
- Use sentence case

**Examples:**
```
Label: Slug
Tooltip: A URL-friendly version of the title, e.g., "my-first-post"

Icon: [?]
Tooltip: Used to calculate shipping costs

Label: Make private
Tooltip: Only you can see private items
```

=== PROCEDURE: Notifications ===

**Types:**
| Type | Tone | Duration |
|------|------|----------|
| Success | Positive | 3-5 seconds |
| Info | Neutral | Until dismissed |
| Warning | Cautious | Until dismissed |
| Error | Serious | Until fixed |

**Notification Copy:**
```
Success: "Changes saved"
Info: "New features are available"
Warning: "Your session will expire in 5 minutes"
Error: "Couldn't save. Try again."
```

=== PROCEDURE: Loading States ===

**Patterns:**
```
Generic: "Loading..."
Specific: "Loading your projects..."
Progress: "Uploading... 45%"
Humorous (if brand allows): "Fetching the goods..."
```

**Long Operations:**
```
Step 1: "Validating data..."
Step 2: "Processing..."
Step 3: "Almost done..."
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(voice-tone) | Tone guidance |
| @skill(user-content) | Longer content |
