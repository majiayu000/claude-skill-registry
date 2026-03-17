---
name: skill-trainer-creator
description: Meta-skill for Epsilon Prime evolution. Analyzes existing knowledge bases and user requirements to design and train new specialized skills or update existing ones.
version: 2.1.0
tier: 1
metadata:
  author: Epsilon Prime
  jurisdiction: US-WA
  last_sync: 2026-02-08
---

# 🎯 Skill Trainer & Creator
**Mission:** To enable the system's self-evolution. My goal is to identify capability gaps and fill them by "teaching" the agent new specialized workflows based on RAG content and project needs.

## 🛠️ Operational Mandates
1.  **Template Fidelity:** Every new skill created MUST follow the V2.1 Standardized Skill Template.
2.  **RAG-Grounded Training:** A skill cannot be "trained" on thin air; it must be mapped to a specific knowledge source in the RAG.
3.  **Test-Driven Development:** Every new skill MUST include an "Execution Example" and a validation test case.
4.  **Registry Awareness:** After creating a skill, always update the `10_SKILL_ROUTER.md` and inform the Cortex.

## 🔄 Standard Workflows

### 1. New Skill Generation
1.  **Gap Analysis:** Identify a recurring task that lacks a specialized workflow (e.g., "CAD generation").
2.  **Research:** Query the RAG for the technical standards and tools required for that domain.
3.  **Draft:** Generate the `.skill.md` file with Mandates, Workflows, and Authorized Tools.
4.  **Validate:** Test the new skill with a sample prompt to ensure correct triggering.

### 2. Skill Updating
1.  **Audit:** Review older skills for legacy logic or missing RAG context.
2.  **Upgrade:** Refactor to the V2.1 framework.
3.  **Register:** Update the `last_sync` date in the metadata.

### 3. Tool Mapping
1.  **Discover:** Scan `tools/` for scripts that could be integrated into the new skill.
2.  **Bind:** Explicitly authorize those tools in the skill description.

## 🗄️ RAG Context
- **Primary Collection:** `rag/core_knowledge/epsilon` (Skill Development Standards)
- **Search Keys:** `skill template`, `meta-learning`, `skill router`, `capability gaps`

## 🧰 Authorized Tools
- `write_file` (Skill creation)
- `read_file` (Contextual analysis)
- `skills/10_SKILL_ROUTER.md` (Registration)
- `skills/skill_compiler.skill.md` (Validation)

## 📝 Execution Example
> **User:** "We need a skill for handling Twilio billing analysis."
> **Action:** 
> 1. Researches Twilio API docs in RAG.
> 2. Designs `twilio_billing_specialist` skill.
> 3. Defines workflow for extracting and summarizing costs.
> 4. Saves and registers the skill.