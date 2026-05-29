---
name: writing-oprs
description: Creating Owner Project Requirements (OPR) documents for building commissioning projects following ASHRAE Standard 202 and Guideline 0. Use when the user needs to write, draft, update, or review OPR documentation, or when starting a new commissioning project that requires an OPR deliverable.
---

# Writing OPRs Skill

This skill provides guidance and templates for creating Owner Project Requirements (OPR) documents for building commissioning projects.

## What is an OPR?

The Owner Project Requirements (OPR) is a foundational commissioning document that captures:
- The owner's project goals and objectives
- Performance expectations and success metrics
- System-specific requirements and operating criteria
- Sustainability and energy efficiency targets
- Maintenance and operations considerations

The OPR serves as the basis for the Basis of Design (BOD) and guides the entire commissioning process.

## Core Capabilities

### OPR Document Structure
- Project overview and objectives
- Owner program requirements
- Systems narrative and performance criteria
- Indoor environmental quality requirements
- Energy efficiency and sustainability goals
- Maintenance and operations requirements

### Standards Compliance
- ASHRAE Standard 202-2018: Commissioning Process for Buildings and Systems
- ASHRAE Guideline 0: The Commissioning Process
- LEED certification requirements
- Local energy code and utility requirements

### Document Development Process
1. Conduct owner interviews to understand goals and priorities
2. Review project drawings and specifications
3. Draft system-specific requirements
4. Establish measurable performance criteria
5. Coordinate with design team and stakeholders
6. Finalize and obtain owner approval

## Reference Templates

The skill includes three reference OPR examples covering different building types:

- **references/2022_OPR.md**: Commercial office renovation (generic template)
  - Complex multi-tenant office building
  - Advanced HVAC systems and controls
  - Sustainability and LEED requirements

- **references/OPR_2022_HS.md**: Educational facility (generic template)
  - K-12 school with specialized spaces
  - Occupant comfort and IAQ focus
  - Energy efficiency requirements

- **references/Example-Project-2025-OPR-fixed.md**: Community center (specific example)
  - Example project - working test case
  - Mixed-use facility with pool and multipurpose spaces
  - Xcel Energy program requirements

## Key OPR Sections

### 1. Project Overview
- Project description and scope
- Location and site context
- Facility use and occupancy
- Project team and stakeholders

### 2. Owner's Goals and Objectives
- Primary mission and purpose
- Success criteria and priorities
- Budget and schedule constraints
- Long-term operational goals

### 3. System Requirements
For each major building system:
- Functional requirements
- Performance criteria (with measurable targets)
- Operating parameters
- Integration requirements
- Maintenance considerations

### 4. Indoor Environmental Quality
- Temperature and humidity setpoints
- Ventilation and air quality requirements
- Lighting levels and controls
- Acoustic performance criteria

### 5. Energy and Sustainability
- Energy performance targets
- Renewable energy goals
- Water conservation requirements
- Sustainable materials and operations

### 6. Commissioning Scope
- Systems to be commissioned
- Testing and verification requirements
- Documentation deliverables
- Training requirements

## Usage Examples

- "Write an OPR for a new office building commissioning project"
- "Help me draft the HVAC requirements section for this OPR"
- "Review this OPR draft and suggest improvements"
- "Create an OPR based on the owner interview notes"
- "Update the energy performance requirements in this OPR"
- "What measurable criteria should I include for the lighting system?"

## Best Practices

### Measurable Criteria
Always define requirements with specific, measurable criteria:
- ❌ "The HVAC system shall maintain comfortable temperatures"
- ✅ "The HVAC system shall maintain space temperatures of 72°F ± 2°F during occupied hours"

### Owner-Focused Language
Write from the owner's perspective, not the engineer's:
- Focus on outcomes and performance, not equipment or methods
- Use clear, accessible language (avoid excessive jargon)
- Emphasize operational and maintenance considerations

### Alignment with Project Phase
- Early design: Focus on goals, objectives, and performance targets
- Later phases: More specific system requirements and acceptance criteria
- Always maintain focus on "what" not "how" (that's for the BOD)

## Progressive Disclosure

For detailed guidance on specific sections or systems, ask:
- "How do I write measurable performance criteria?"
- "What should I include in the HVAC systems narrative?"
- "How do I document energy efficiency requirements?"
- "What level of detail is appropriate for [specific system]?"


## Saving Next Steps

When writing-oprs work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "writing-oprs" \
  --content "## Priority Tasks
1. Complete OPR Section 3 - Performance Requirements
2. Review OPR with stakeholders
3. Finalize OPR deliverable for commissioning project"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`
