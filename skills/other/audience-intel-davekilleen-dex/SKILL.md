---
name: audience-intel
description: Synthesize what we're learning about our audience
role_groups: [marketing, product]
jtbd: |
  Understanding your audience requires synthesizing insights from customer conversations, 
  feedback, and behavior patterns. This reviews recent interactions, identifies persona 
  patterns, surfaces pain points and motivations, and updates your audience understanding 
  so marketing stays targeted and relevant.
time_investment: "10-15 minutes per review"
---

## Purpose

Aggregate audience insights from all sources to refine persona understanding and inform marketing strategy.

## Usage

- `/audience-intel` - Full audience analysis
- `/audience-intel [persona]` - Focus on specific persona/segment

---

## Steps

1. **Gather audience data:**
   - Search 00-Inbox/Meetings/ for customer conversations
   - Check People/ for customer person pages
   - Reference `/customer-intel` output if available

2. **Identify patterns:**
   - Common roles/titles
   - Shared pain points
   - Similar goals/motivations
   - Buying triggers
   - Decision criteria

3. **Segment insights:**
   - Group by persona/role
   - Note differences between segments
   - Identify underserved audiences

4. **Extract messaging insights:**
   - What language do they use?
   - What problems do they describe?
   - What outcomes do they want?
   - What objections do they raise?

5. **Generate intelligence report with:**
   - Persona patterns
   - Pain points by segment
   - Motivations and goals
   - Messaging implications
   - Content recommendations

---

## Output Format

```markdown
# 👥 Audience Intelligence

**Period:** [Timeframe]
**Interactions analyzed:** [Count]

## Persona Patterns

### [Persona Name] (Primary Audience)
- **Typical roles:** [Titles]
- **Company size:** [Range]
- **Top pain points:**
  1. [Pain point 1]
  2. [Pain point 2]
- **Key motivations:** [What drives them]
- **Decision criteria:** [What they care about]

## Messaging Insights

### Language They Use
- "[Quote 1]" - [Persona]
- "[Quote 2]" - [Persona]

### Problems They Describe
1. [Problem description in their words]
2. [Problem description]

## Content Recommendations
1. [Content idea] - Addresses [pain point] for [persona]
2. [Content idea] - Targets [motivation] for [persona]
```
