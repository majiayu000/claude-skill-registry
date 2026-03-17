---
context: fork
---

# /adr

Create a new Architecture Decision Record (ADR) following the official YourOrg ADR process.

## Usage

```
/adr <title>
/adr <title> for <project>
```

## Examples

```
/adr API Gateway Selection
/adr Kafka vs EventBridge for Project - MyDataIntegration
/adr Standalone Laptop for Offline Database Build
```

## Instructions

### 1. Parse Command and Initial Setup

Parse the command for:

- **title**: The ADR name (required)
- **project**: Related project (optional)

### 2. Discover Relevant Organisational ADRs

**IMPORTANT**: Before creating a new ADR, search for existing organisational ADRs that may constrain or inform this decision.

Search the vault for relevant ADRs:

1. Search `+Sync/Org-ADRs/` for ADRs with `authority: organizational`
2. Search vault root for ADRs with `status: accepted`
3. Look for keywords matching the decision topic

Display found ADRs to the user:

```
📋 Relevant Organisational ADRs Found:

**Must Follow** (authority: organizational):
- [[ADR - API Gateway Selection]] - Mandates Kong for API management
- [[ADR - Cloud Provider Selection]] - Requires AWS for new services

**Consider** (authority: team, related domain):
- [[ADR - Kafka Event Patterns]] - Event-driven patterns for integration
- [[ADR - Data Product Standards]] - Data exchange formats

Would you like to reference any of these in your new ADR's `dependsOn` field?
```

Store selected references for later inclusion in frontmatter.

### 3. Check for Existing Guardrail

**CRITICAL STEP**: Before creating an ADR, check if a relevant guardrail already exists.

Ask the user:

> "Before creating this ADR, have you checked if there's an existing guardrail that covers this decision? If a guardrail exists, you should follow it instead of creating an ADR."

If user confirms no guardrail exists, proceed to step 4.

### 4. Determine ADR Type

Ask the user to select the ADR type (explain each):

**Question**: "What type of ADR is this?"

**Options**:

1. **Technology_ADR** - New technology/tool or significant change to existing technology
   - Examples: New database, cloud service, development tool, infrastructure component
   - Requires SME approvals for the specific technology area

2. **Architecture_ADR** - New guardrail, pattern, or standard
   - Examples: New architectural pattern, coding standard, design principle
   - Creates organizational standard - highest approval level required
   - Becomes future guardrail

3. **Local_ADR** - Following existing guardrails
   - Examples: Team-level decision within established patterns
   - Local architecture process only - minimal approvals

Store the selected type in `adrType` frontmatter field.

### 5. Identify Required Approvers

Based on the ADR type and subject area, identify required approvers using [[Page - YourOrg ADR Approvers and SME (Official)]].

**Core Assessors (Always Required)**:

- Head of Architecture or Engineering
- Principal Solution Architect (if not already involved)
- Cyber Assurance (Security Lead or delegate)

**Ask the user**: "What subject areas does this ADR cover?"

**Common Subject Areas** (select all that apply):

- Application Database/Storage (Database SME / Integration Lead)
- Application Integration (Integration SME / Integration Lead)
- AI (AI/ML Lead / AI Architect)
- Cloud (AWS/Azure/GCP) (Cloud Architect / Cloud Lead)
- Data Products/Integration (Data Product Owner / Data Architect)
- Data Platform (Data Platform Lead / Data Architect)
- Data Privacy (Privacy Officer / dataprotection@yourorg.com)
- PC Hardware/Software (Endpoint Lead / Desktop Architect)
- Mobile (iOS/Android) (Mobile Lead / Mobile Architect)
- Networks (Network Architect / Network Lead)
- Cyber (Security Lead)
- IT Operations (Operations Manager / Service Delivery Lead)
- Software Engineering/DevSecOps (Engineering Lead / DevOps Architect)
- Power Platform (Low-Code Lead / Platform Owner)

Build the complete approvers list from Core + Subject-Specific SMEs.

### 6. Gather ADR Content

Ask the user for key information using the official YourOrg ADR template structure:

#### Context Questions:

1. **Background**: What is the architectural context? What problem led to this decision?
2. **Problem Statement**: What is the specific problem or requirement? What are the constraints?
3. **Goals**: What are the desired outcomes?

#### Alternatives Questions:

1. **What alternatives did you consider?** (minimum 2, recommend 3-5)
2. For each alternative:
   - Description
   - Pros
   - Cons
   - Fit with requirements
   - Why was it rejected?

#### Decision Questions:

1. **What is the decision?** (clear, specific statement)
2. **Why this decision?** (rationale)
3. **How does this address the problem?**

#### Consequences Questions:

1. **Positive impacts**: What are the benefits?
2. **Negative impacts**: What are the drawbacks or risks?
3. **Mitigation strategies**: How will you address negative consequences?

#### Implementation Questions:

1. **Cost model**: What are the costs (one-time, recurring)?
2. **Deployment approach**: How will this be implemented?
3. **Operational model**: How will this be operated and supported?
4. **Migration/rollout**: What are the phases?

#### Compliance Questions:

1. **GDPR compliance**: Does this process personal data?
2. **Security classification**: What data classification (Official, Official-Sensitive)?
3. **Audit requirements**: What audit/traceability is needed?

### 7. Create the ADR

Generate filename: `ADR - {{title}}.md`

Create the ADR in vault root using the structure from `+Templates/ADR.md`:

**Frontmatter**:

```yaml
---
type: Adr
title: {{title}}
description: {{one-line summary}}
status: draft
adrType: {{Technology_ADR | Architecture_ADR | Local_ADR}}
tags: [ADR, architecture, {{additional relevant tags}}]
created: {{DATE}}
modified: {{DATE}}
deciders: [Engineering Architecture Team, {{project team if applicable}}]
approvers:
  # Core Assessors (Required)
  - Head of Architecture or Engineering
  - Principal Solution Architect
  - Cyber Assurance (Security Lead or delegate)
  # Subject-Specific SMEs (from user selections)
  {{list of SME approvers based on subject areas}}
  # Stakeholders
  {{project stakeholders if applicable}}
project: {{project_link or null}}
jiraTicket: null  # To be added when JIRA ticket created

# Source/Provenance
source: local                         # local | confluence
sourcePageId: null                    # Confluence page ID (once published)
sourceSpace: null                     # Confluence space key
sourceUrl: null                       # Link to authoritative version
sourceVersion: null                   # Version number

# Publication
isPublished: false                    # Updated when published to Confluence
publishedDate: null                   # YYYY-MM-DD
publishedUrl: null                    # Confluence URL

# Authority Level
authority: draft                      # draft → local → team → organizational

# Relationships
relatedTo: []
supersedes: []
dependsOn: {{selected_dependencies_from_discovery_step}}

# Quality Indicators
confidence: medium
freshness: current
verified: false
reviewed: {{DATE}}

# Context
summary: {{one-line summary}}
assumptions: []
stakeholders: {{list from approvers}}
---
```

**Content**: Use official YourOrg ADR template structure with all sections filled in from user responses.

Include at the top:

```markdown
> **Based on Official YourOrg ADR Template**: [[Page - YourOrg ADR Template (Official)]]
>
> **ADR Process**: [[Page - YourOrg ADR Process (Official)]]
>
> **Required Approvers**: [[Page - YourOrg ADR Approvers and SME (Official)]]
```

### 8. Provide Next Steps Guidance

After creating the ADR, display:

```
✅ ADR created: ADR - {{title}}.md

📋 Next Steps (Official YourOrg ADR Process):

1. ⏳ REVIEW ADR CONTENT
   - Review all sections for completeness
   - Ensure alternatives are well-documented
   - Verify approvers list is correct

2. ⏳ CREATE JIRA TICKET (CRITICAL - ADR not complete without this)
   - Project: {{user's project or ARCH}}
   - Issue Type: ADR
   - Label: "{{adrType}}"
   - Summary: "ADR - {{title}}"
   - Link this ADR document to JIRA ticket

3. ⏳ ADD APPROVERS IN JIRA
   Use '@' function in Jira to add:
   {{list all approvers from frontmatter}}

4. ⏳ CREATE/LINK CONFLUENCE PAGE
   - Create Confluence page with ADR content
   - Link Confluence page to JIRA ticket

5. ⏳ UPDATE ADR STATUS
   - After JIRA ticket created, update status: draft → proposed
   - Add JIRA ticket reference to frontmatter

6. ⏳ STAKEHOLDER REVIEW
   - Approvers review in Jira
   - Discussion via Jira comments
   - All approvers must agree

7. ⏳ ADR ACCEPTANCE
   - All approvals confirmed in Jira
   - Update status: proposed → accepted

8. ⏳ POST-APPROVAL
   - Close JIRA ticket
   - Tidy Confluence page
   - Add appropriate labels

9. ⏳ PUBLISH TO CONFLUENCE (Final Step)
   - Create Confluence page with ADR content
   - Update vault ADR frontmatter:
     - isPublished: true
     - publishedDate: {{today}}
     - publishedUrl: {{confluence URL}}
     - authority: team (or organizational if it becomes a guardrail)
     - status: accepted

🔄 Authority Progression:
- draft → ADR being created (local work)
- local → Personal decision, not yet shared
- team → Approved by team, in Confluence
- organizational → Company-wide standard/guardrail

📚 References:
- [[Page - YourOrg ADR Process (Official)]] - Full process documentation
- [[Page - YourOrg ADR Approvers and SME (Official)]] - Approvers reference
- [[Page - YourOrg ADR Template (Official)]] - Template structure

⚠️ REMEMBER: ADRs are not complete until JIRA ticket is raised!
```

### 9. Create Associated Task (Optional)

Ask the user: "Would you like me to create a task to track this ADR through the approval process?"

If yes, create a task: `Task - Create ADR - {{title}}.md` with:

- Checklist of all workflow steps above
- Due date (ask user)
- Project reference
- Links to ADR, official process docs

## Important Notes

1. **JIRA Ticket is Mandatory**: Always emphasize that ADR is not complete without JIRA ticket
2. **Official Process**: Always reference the official YourOrg ADR process documentation
3. **Approvers are Required**: Must identify and document required approvers before proceeding
4. **Confluence Integration**: ADRs live in Confluence with JIRA as anchor
5. **Status Progression**: draft → proposed (after JIRA) → accepted (after approvals)
6. **Three ADR Types**: Technology_ADR (most common), Architecture_ADR (new guardrail), Local_ADR (within guardrails)

## Error Handling

- If user skips checking for existing guardrail, remind them this is required
- If user cannot identify appropriate approvers, suggest reviewing [[Page - YourOrg ADR Approvers and SME (Official)]]
- If ADR type is unclear, explain each type with examples
- If user wants to skip JIRA ticket, explain it's mandatory per official process

## Reference Documentation

All guidance based on:

- [[Page - YourOrg ADR Process (Official)]]
- [[Page - YourOrg ADR Approvers and SME (Official)]]
- [[Page - YourOrg ADR Template (Official)]]
