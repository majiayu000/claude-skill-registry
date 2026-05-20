---
name: list-members
description: Displays the roster of architecture team members with their specialties and expertise areas. Use when the user asks "Who's on the architecture team?", "List architecture members", "Show me the architects", "What specialists are available?", "Who can I ask for reviews?", or wants to discover available experts. Do NOT use for requesting reviews (use specialist-review or architecture-review) or checking documentation status (use architecture-status).
allowed-tools: Read
---

# List Architecture Members

Displays all architecture team members and their expertise areas.

## Process

### 1. Check Setup
If `.architecture/members.yml` doesn't exist:
```
The AI Software Architect framework hasn't been set up yet.

To get started: "Setup ai-software-architect"
```

### 2. Load Members
Read `.architecture/members.yml` and parse all members (id, name, title, specialties, disciplines, skillsets, domains, perspective).

### 3. Display Team Roster
```markdown
# Architecture Team Members

Your AI Software Architect team consists of [count] specialized reviewers.

Total Members: [count]

---

## Team Roster

### [Member 1 Name] - [Member 1 Title]

**ID**: `[member_id]`

**Specialties**: [Specialty 1], [Specialty 2], [Specialty 3]

**Disciplines**: [Discipline 1], [Discipline 2]

**Domains**: [Domain 1], [Domain 2], [Domain 3]

**Perspective**: [Their unique perspective]

**Request review**: `Ask [Member Title] to review [your target]`

---

[Repeat for all members]

---

## Quick Reference

**Specialist reviews**:
- `Ask [Specialist Title] to review [target]`

**Examples**:
- "Ask Security Specialist to review authentication"
- "Ask Performance Specialist to review database queries"
- "Ask [Your Specialist] to review [anything]"

**Full architecture review**:
- `Start architecture review for version X.Y.Z`

**Other commands**:
- `Create ADR for [decision topic]`
- `What's our architecture status?`

---

## Team by Specialty

[Group members by their primary domains/specialties]

**Security & Compliance**: [Members]
**Performance & Scalability**: [Members]
**Code Quality & Maintainability**: [Members]
**Domain & Business Logic**: [Members]
**System Design & Architecture**: [Members]
**Technology-Specific**: [Members]

---

## Adding New Members

Request a review from any specialist, even if they don't exist:
- "Ask Ruby Expert to review my modules"
- "Have Accessibility Expert review forms"

I'll create the specialist and add them to your team automatically.

Or manually edit `.architecture/members.yml` and add:
```yaml
- id: your_specialist_id
  name: "[Name]"
  title: "[Title]"
  specialties: ["[Specialty 1]", "[Specialty 2]"]
  disciplines: ["[Discipline 1]", "[Discipline 2]"]
  skillsets: ["[Skill 1]", "[Skill 2]"]
  domains: ["[Domain 1]", "[Domain 2]"]
  perspective: "[Brief description]"
```

---

## Using the Team

**For focused reviews** (specific expertise):
```
Ask [Specialist] to review [target]
```
Fast turnaround, targeted insights

**For comprehensive reviews** (all perspectives):
```
Start architecture review for [version/feature]
```
All members review, collaborative discussion

**For decisions**:
```
Create ADR for [decision topic]
```
Document decisions with team input

---
```

### 4. Provide Context
After listing:
- Explain when to use specialist vs full reviews
- Show how to add new members dynamically
- Provide usage examples
- Suggest next steps

## Example Output Summary
After showing full roster, provide a concise summary:
```
Ready to use your architecture team:
- [N] specialists available
- Request reviews: "Ask [specialist] to review [target]"
- Add new specialists: Just ask for them by name
- Full review: "Start architecture review for [scope]"
```

## Error Handling
- No `.architecture/`: Offer setup instructions
- Empty `members.yml`: Show default team and offer setup
- Malformed YAML: Show what's parseable, note issues

## Related Skills

**After Listing Members**:
- "Ask [specialist] to review [target]" - Request focused expert review
- "Start architecture review for [scope]" - Comprehensive review with all members
- "What's our architecture status?" - See how team has been used

**When Adding Members**:
- Just request a specialist that doesn't exist - they'll be created automatically
- "Setup ai-software-architect" - Adds members based on your tech stack

**Workflow Examples**:
1. List members → Identify relevant specialist → Request review
2. Need new expertise → Request it → Specialist auto-created → List to verify
3. Status check → List members → Review with specific specialists

## Notes
- Keep presentation clear and scannable
- Make it actionable with specific commands
- Encourage exploration and usage
- Explain that team can grow dynamically
