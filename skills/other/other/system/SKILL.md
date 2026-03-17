---
context: fork
---

# /system

Create a comprehensive System note documenting an enterprise system, application, platform, or infrastructure component with full architecture knowledge graph metadata.

## Usage

```
/system <name>
/system <name> --type <type>
/system <name> --quick
/system SAP S/4HANA
/system DataPlatform --type platform
/system Kong API Gateway --quick
```

## Instructions

This skill uses progressive disclosure to efficiently gather system information while providing sensible defaults.

### Phase 1: Parse Input & Duplicate Check

1. Extract system name from command
2. Query graph index for existing systems:
   ```
   node scripts/graph-query.js --type System --search "<name>"
   ```
3. If similar system found, show it:
   - "Found: [[System - SAP S/4HANA]]. Did you mean this one?"
   - Offer to open existing instead of creating duplicate
4. Check for `--quick` flag (skip optional phases)
5. Check for `--type` flag (pre-set system type)

### Phase 2: Essential Information (Always Ask)

Gather required fields with defaults:

```
Creating System note for: <name>

1️⃣ System ID (for CMDB/integrations):
   Default: <AUTO from name: SAP-S4HANA>
   User input: [optional override]

2️⃣ Aliases (alternative names, acronyms):
   Examples: PAD, Aerospace & Defence, A&D
   → Search System Catalog in Confluence for known aliases
   → Check LegacyEngineeringSystemF space System Catalogue
   Default: []
   User input: [comma-separated list]

3️⃣ APM Number (Application Portfolio Management ID):
   Format: APM0001234
   → Search Confluence System Catalog (AL space) for APM number
   → Link: https://yourorg.atlassian.net/wiki/spaces/AL/
   Default: null
   User input: [APM number if known]

4️⃣ System Type:
   - application (business application)
   - platform (shared infrastructure)
   - database (data store)
   - middleware (integration layer)
   - saas (cloud service)
   - infrastructure (compute/network)
   Default: application
   User input: [selection]

5️⃣ Owner (person or team):
   Search existing: [[Person - Name]]
   Default: Current user or unassigned
   User input: [name to search and link]

6️⃣ Status:
   - active (in production)
   - planned (not yet deployed)
   - deprecated (being retired)
   Default: active
   User input: [selection]
```

### Phase 3: Classification (Brief)

Ask for quick context:

```
7️⃣ Criticality to operations:
   - critical (business stops if down)
   - high (significant impact)
   - medium (moderate impact)
   - low (minimal impact)
   Default: medium
   User input: [selection]

8️⃣ Where is it hosted:
   - on-prem | aws | azure | gcp | saas | hybrid
   Default: on-prem (for enterprise systems)
   User input: [selection]

9️⃣ Confluence Documentation:
   → Search System Catalog (AL) for system page
   → Search LegacyEngineeringSystemF System Catalogue
   → Provide URL if found
   Default: null
   User input: [URL or search term]
```

### Phase 4: Optional Enhancement (Skip if --quick)

```
Would you like to add more details now? (Y/n)
- Technology stack (languages, frameworks, databases)
- Integration connections (what systems it connects to)
- Operational SLAs (availability, latency targets)
- Cost information (annual run-rate)
- Security classification (GDPR/confidential/secret)

Default: n
```

If YES, gather these fields:

**Technology Stack:**
```
Technologies used (comma-separated):
- Languages: java, python, node, go, etc.
- Frameworks: spring, django, fastapi, etc.
- Databases: postgres, oracle, dynamodb, etc.
- Messaging: kafka, rabbitmq, sqs, etc.
- Other: kubernetes, docker, serverless, etc.
Default: []
```

**Integration Connections:**
```
Does this system connect to others?
"Integrates with: DataPlatform, Snowflake, Kong"
→ Auto-search for [[System - DataPlatform]], etc.
→ Confirm each link before adding to connectsTo
Default: []
```

**Operational Details:**
```
Availability SLA: 99.95 (%)
Default: 99.95

Recovery Time Objective (RTO): 4 (hours)
Default: 4

Is this system critical for a project?
Link to: [[Project - Name]]
Default: none
```

**Cost Information:**
```
Annual cost (£): 250000
Default: null

Cost center: 4521
Default: null
```

**Data Classification:**
```
Data classification:
- public | internal | confidential | secret
Default: internal

Contains PII or sensitive data? (Y/n)
Default: n

GDPR applicable? (Y/n)
Default: n
```

### Phase 5: Auto-Link Discovery

While gathering input, watch for system mentions:
- If user types "connects to DataPlatform", search for [[System - DataPlatform]]
- If user mentions "SAP", suggest [[System - SAP S/4HANA]]
- For each found system, ask: "Add [[System - Name]] to connectsTo? (Y/n)"

### Phase 6: Generate Frontmatter

Create complete YAML frontmatter from gathered data:

```yaml
type: System
title: "{{systemName}}"

# Essential
systemId: "{{systemId}}"
aliases: [{{aliases}}]  # Alternative names, acronyms
apmNumber: "{{apmNumber}}"  # APM0001234
systemType: {{type}}
owner: "[[{{owner}}]]"
status: {{status}}
criticality: {{criticality}}
hosting: {{hosting}}

# External References
confluenceUrl: "{{confluenceUrl}}"  # System Catalog link
cmdbId: null
documentationUrl: null

# From optional fields (if provided)
technology: [{{technologies}}]
vendor: null (auto-link if known)
annualCost: {{cost}}
costCenter: {{costCenter}}
dataClassification: {{classification}}
gdpr-applicable: {{gdpr}}
pii-handled: {{pii}}
connectsTo: [{{autoDiscoveredSystems}}]

# Defaults
confidence: medium
freshness: current
verified: false
reviewed: 2026-01-14

created: 2026-01-14
modified: 2026-01-14
tags: [type/system, {{autoTags}}]
```

### Phase 7: Generate Body Content

Create markdown body with:

1. **Overview Section**: AI-generated 2-3 paragraph summary based on system type and name
   ```
   # {{systemName}}

   ## Overview
   {{AI summary: what does this system do, role in enterprise}}
   ```

2. **System Properties Table**: Quick reference of key facts

3. **Technology Stack Section**: Organized by component (Language, Database, Messaging)

4. **Architecture Diagram**: Mermaid diagram placeholder showing system context
   ```mermaid
   graph TB
       Users["Users/Systems"]
       System["<b>{{systemName}}</b>"]
       Deps["Dependencies"]

       Users -->|Uses| System
       System -->|Integrates| Deps
   ```

5. **Integrations Section**: Dataview queries for related Integration notes
   ```dataview
   TABLE targetSystem, pattern, frequency
   FROM ""
   WHERE type = "Integration" AND contains(sourceSystem, this.file.name)
   ```

6. **Data & Security Section**: Classification, encryption, compliance

7. **Operational Details**: SLA, monitoring, maintenance windows

8. **Related Documentation**: Links to ADRs, Projects, Architecture notes

9. **Quick Links**: Owner, vendor, related projects (for quick navigation)

### Phase 8: Create File & Suggest Next Steps

**File Location**: Vault root directory

**Filename**: `System - {{systemName}}.md`

**Output**:
```
✅ Created: System - {{systemName}}.md

Next steps:
1. Add integrations: /integration {{systemName}} <target-system>
2. Document data: /datasource <datasource-name>
3. Generate diagram: /c4-diagram [[System - {{systemName}}]]
4. Add to architecture: /architecture --relate-system {{systemName}}
5. Or continue with: /system <next-system-name>
```

## Skill Interaction Map

```
/system creates System note
  ├─ User can then create: /integration <source> <target>
  ├─ User can then create: /datasource <name>
  ├─ Skill can generate: /c4-diagram [[System - {{name}}]]
  └─ Skill can analyse: /impact-analysis [[System - {{name}}]]
```

## Example Interaction

```
User: /system SAP S/4HANA