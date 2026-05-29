---
document_name: "user-content.skill.md"
location: ".claude/skills/user-content.skill.md"
codebook_id: "CB-SKILL-USERCONTENT-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for user-facing content"
skill_metadata:
  category: "content"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Voice & tone guidelines"
    - "Audience understanding"
category: "skills"
status: "active"
tags:
  - "skill"
  - "content"
  - "user-facing"
ai_parser_instructions: |
  This skill defines procedures for user-facing content.
  Used by Copywriter agent.
---

# User Content Skill

=== PURPOSE ===

Procedures for creating user-facing content beyond microcopy.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(copywriter) @ref(CB-AGENT-COPY-001) | Primary skill for user content |

=== PROCEDURE: Onboarding Copy ===

**Welcome Screen:**
```markdown
## Template

### Headline
Welcome to [Product]! (or persona-specific greeting)

### Subheadline
[One sentence about what they can do]

### CTA
Get started / Take a quick tour / Skip for now
```

**Step-by-Step Onboarding:**
```markdown
## Step 1 of 3: [Action]

### Headline
[What to do]

### Body
[Why this matters - 1-2 sentences]

### CTA
[Action verb] / Skip

### Progress
Step 1 of 3
```

**Checklist Onboarding:**
```markdown
## Get started with [Product]

Complete these steps to get the most out of [Product]:

- [ ] Connect your account
- [ ] Invite team members
- [ ] Create your first project
- [x] Completed step
```

=== PROCEDURE: Email Templates ===

**Transactional Email Template:**
```markdown
## Subject Line
[Action-oriented, specific]

## Preview Text
[First 50 characters shown in inbox]

## Body

Hi [Name],

[One sentence about what happened/why we're emailing]

[Details if needed - keep brief]

[Clear CTA button]

[Closing]
[Team/Company name]

## Footer
[Unsubscribe link, address, etc.]
```

**Email Types:**
| Type | Subject Pattern | Tone |
|------|-----------------|------|
| Welcome | "Welcome to [Product]!" | Warm, helpful |
| Confirmation | "Your [action] is confirmed" | Clear, factual |
| Password reset | "Reset your password" | Direct, urgent |
| Notification | "[Action]: [Details]" | Informative |
| Marketing | "[Benefit/News]" | Engaging |

=== PROCEDURE: Help Content ===

**FAQ Format:**
```markdown
## Frequently Asked Questions

### How do I [common task]?
[Direct answer in 1-2 sentences]

[Steps if needed:]
1. First step
2. Second step
3. Third step

### Why can't I [problem]?
This usually happens because [reason].

To fix it:
1. Try [solution 1]
2. If that doesn't work, [solution 2]
3. Still stuck? [Contact support]
```

**Troubleshooting Format:**
```markdown
## Troubleshooting: [Problem]

### Symptoms
- [What the user sees/experiences]
- [Another symptom]

### Cause
[Brief explanation]

### Solution
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Still having issues?
[Contact link or next steps]
```

=== PROCEDURE: Release Notes ===

**User-Facing Format:**
```markdown
## What's New (Month YYYY)

### New Features

#### [Feature Name]
[One sentence benefit-focused description]
[Screenshot or GIF if helpful]

### Improvements
- **[Area]:** [What improved and why it matters]
- **[Area]:** [What improved and why it matters]

### Bug Fixes
- Fixed issue where [problem description]
- Resolved [problem] that caused [symptom]
```

**Writing Guidelines:**
- Lead with benefits, not features
- Use plain language (no tech jargon)
- Focus on what users can do now
- Keep it scannable

=== PROCEDURE: In-App Announcements ===

**Banner:**
```
[Icon] [Short message - max 100 chars] [CTA or Dismiss]
```

**Modal:**
```markdown
## [Headline - what's new/important]

[1-3 sentences explaining the change/feature]

[Image/illustration if helpful]

[Primary CTA] [Secondary action or dismiss]
```

**Tooltip/Coach Mark:**
```
[Arrow pointing to element]
[What this is/does - max 100 chars]
[Got it / Next]
```

=== PROCEDURE: Content Audit ===

**Review Checklist:**
- [ ] Accurate and current
- [ ] Clear and concise
- [ ] Consistent with voice/tone
- [ ] Accessible language
- [ ] Action-oriented
- [ ] No jargon
- [ ] Proofread for errors

**Questions to Ask:**
1. Who is reading this?
2. What do they need to know?
3. What should they do next?
4. Is anything confusing or unclear?
5. Can this be shorter?

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(microcopy) | Short-form UI text |
| @skill(voice-tone) | Consistency |
