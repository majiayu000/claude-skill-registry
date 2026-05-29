---
name: update-experience
description: Add or update career experience in XML files under /experience. Use when user wants to add new work experience, update previous roles, add activities/achievements, update credentials, or modify career data. Enforces STAR format (Situation, Task, Action, Result) for all activities. Handles unstructured text input by extracting relevant information and asking clarifying questions to complete STAR requirements.
---

# Update Experience

Add or update career experience in the XML files under `/experience`. All activities must follow STAR format.

## Workflow

```
1. PARSE INPUT
   └─ Determine: Add new or update existing? What type (position, activity, credential)?

2. IDENTIFY TARGET
   └─ Find existing element to update, or determine where new element belongs

3. VALIDATE STAR
   └─ Check if input has all STAR components; identify gaps

4. CLARIFY (if needed)
   └─ Ask questions to complete missing STAR elements

5. GENERATE XML
   └─ Create properly formatted XML with tags

6. UPDATE FILE
   └─ Edit the appropriate experience/*.xml file(s)
```

## Update Types

| Type | Description | Target File |
|------|-------------|-------------|
| **New Position** | Add a new job/role | career-profile.xml |
| **New Activity** | Add achievement to existing position | career-profile.xml |
| **Update Activity** | Modify existing STAR content | career-profile.xml |
| **New Initiative** | Add project grouping under position | career-profile.xml |
| **Credentials** | Education, certifications, speaking | career-profile.xml |
| **Expertise** | Skills, technologies, domains | career-profile.xml |
| **Key Metrics** | Headline numbers | career-profile.xml |

## STAR Format Requirements

Every activity MUST have all four STAR elements:

```xml
<activity id="{position-id}-{year}-{topic}" type="{strategic|technical|leadership}">
  <situation>Context that created the need (business problem, gap, opportunity)</situation>
  <task>Specific responsibility assigned (what you were asked to do)</task>
  <action>What was done (power verbs, specific steps taken)</action>
  <result>Quantified outcome with inline metrics ($, %, numbers)</result>
  <tags>
    <domain ref="{domain-id}">
      <skill>Specific skill demonstrated</skill>
      <technology>Tool or technology used</technology>
    </domain>
  </tags>
</activity>
```

## Clarifying Questions

When input lacks STAR components, ask targeted questions:

**Missing Situation:**
- "What was the business context or problem that created this need?"
- "What was happening in the organization that led to this work?"

**Missing Task:**
- "What was your specific responsibility or assignment?"
- "What were you asked to accomplish?"

**Missing Action:**
- "What specific steps did you take?"
- "What methods, tools, or approaches did you use?"

**Missing Result:**
- "What was the measurable outcome?"
- "Can you quantify the impact (revenue, time saved, users, scale)?"

**Missing Tags:**
- "Which skills from your expertise does this demonstrate?"
- "What technologies or tools were involved?"

## Processing Unstructured Input

When user provides blob text:

1. **Extract identifiable STAR elements** from the text
2. **Identify the position** it relates to (by company, date, or context)
3. **Map to existing initiatives** if applicable
4. **List what's missing** and ask specific questions
5. **Propose the XML structure** for user confirmation before updating

**Example:**
```
User: "At Google I built a training program that got 500 people certified"

Missing:
- Situation: Why was training needed?
- Task: What was your specific role?
- Action: What did you actually do to build it?
- Result: Has number but needs context (what certifications? timeframe?)
- Tags: Which domains/skills?

Questions:
1. "What prompted the need for this training program?"
2. "What was your specific responsibility - did you design it, run it, or both?"
3. "What's the timeframe for the 500 certifications?"
```

## Activity Types

| Type | Indicators | Examples |
|------|------------|----------|
| `strategic` | Enterprise-wide impact, long-term planning, C-level visibility | Architecture design, strategy development |
| `technical` | Hands-on implementation, technical decisions | Building agents, coding, system design |
| `leadership` | Team management, program coordination, training | Program management, mentoring, training |

## Tag Domains

Reference domains from the `<expertise>` section using the `ref` attribute:

**Tier 1** (10+ years): `enterprise-architecture`, `cloud-platforms`, `technology-evangelism`, `program-management`

**Tier 2** (5-10 years): `ai-ml`, `value-engineering`, `sales-enablement`, `business-development`

**Tier 3** (2-5 years): `six-sigma`, `martech-loyalty`, `software-development`

## XML Schema Reference

See `references/xml-schema.md` for complete element hierarchy and attribute documentation.

## File Update Process

1. **Read current file** - Load the target XML file
2. **Locate insertion point** - Find the right position/initiative
3. **Generate activity ID** - Format: `{position-id}-{year}-{topic-slug}`
4. **Insert new element** - Maintain proper indentation (2 spaces)
5. **Validate XML** - Ensure well-formed after edit
6. **Update career-summary.xml** - If adding new position or major achievement, update condensed version

## Example: Adding New Activity

**Input:** "I just presented the AI strategy to the board last week"

**Process:**
1. Identify: New activity for current position (mcd-2024)
2. Check STAR:
   - Situation: ❌ Missing - why board presentation?
   - Task: ❌ Missing - what was the goal?
   - Action: ⚠️ Partial - "presented"
   - Result: ❌ Missing - what was outcome?

3. Ask:
   - "What was the purpose of presenting to the board?"
   - "What specific content or recommendations did you present?"
   - "What was the outcome - approvals, feedback, next steps?"

4. After answers, generate:
```xml
<activity id="mcd-2024-board-ai" type="strategic">
  <situation>Board required visibility into enterprise AI strategy...</situation>
  <task>Present comprehensive AI roadmap and investment recommendations...</task>
  <action>Delivered executive presentation covering 10-layer architecture...</action>
  <result>Secured board approval for AI investment roadmap...</result>
  <tags>
    <domain ref="ai-ml">
      <skill>AI governance</skill>
    </domain>
    <domain ref="technology-evangelism">
      <skill>Executive presentations</skill>
    </domain>
  </tags>
</activity>
```
