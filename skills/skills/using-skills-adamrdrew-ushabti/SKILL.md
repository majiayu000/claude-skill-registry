---
name: using-skills
description: Provides sub agents important information on how to use skills
user-invocable: false
---

# How to Use Skills

Sub agents can invoke skills to get domain specific knowledge on a number of topics. You can invoke a skill using the Skill tool, which you have access to, and specifying a skill name.

# When to Use Skills

If you have a question or need information on any topic a skill provides information on, invoke the skill. You should also invoke skills at any time that your instructions tell you to.

# Available Skills

name: archive-ticket
description: Archive completed tickets by moving them to .archived/

---

name: check-ushabti-prerequisites
description: Verify required Ushabti files exist before proceeding. Use when starting agent work to ensure prerequisites are met.

---

name: create-ticket
description: Create a new ticket with schema validation

---

name: describe-agent-roles
description: Agent responsibilities and hard boundaries. Load when determining which agent should act or checking role violations.

---

name: describe-canonical-locations
description: File locations for laws, style, phases, and docs. Load when locating or creating Ushabti state files.

---

name: describe-docs-system
description: Documentation system location and maintenance requirements. Load when consulting or updating project documentation.

---

name: describe-good-phase
description: Phase sizing, scope boundaries, and anti-patterns. Load when evaluating whether a phase is well-formed or needs splitting.

---

name: describe-laws-and-style
description: Distinction between laws (invariants) and style (conventions). Load when determining if a constraint is a law or style.

---

name: describe-phase-directory-structure
description: Phase directory layout, naming conventions, and required files. Load when creating or navigating phase directories.

---

name: describe-phase-file
description: Required sections and format for phase.md. Load when defining phase intent, scope, and acceptance criteria.

---

name: describe-phase-loop
description: Plan-Build-Review cycle and agent handoffs. Load when transitioning between agents or understanding workflow progression.

---

name: describe-progress-file
description: Structure and field ownership for progress.yaml. Load when reading or updating phase progress state.

---

name: describe-questions-policy
description: Guidelines for asking clarifying questions. Load when deciding whether and how to ask the user for clarification.

---

name: describe-required-inputs
description: Mandatory files agents must read before acting. Load when starting agent work to ensure prerequisites are met.

---

name: describe-review-file
description: Structure and sections for review.md. Load when creating review scaffolds or recording review findings.

---

name: describe-steps-file
description: Step format and ordering rules for steps.md. Load when defining implementation steps or checking step requirements.

---

name: describe-tickets
description: Ticket system overview, schema, and workflows

---

name: describe-ushabti
description: Core Ushabti concepts and development lifecycle. Load when starting any Ushabti workflow or orienting to the framework.

---

name: find-current-phase
description: Find the active phase directory based on status. Use when you need to locate which phase to work on.

---

name: find-next-phase-number
description: Determine the next sequential phase ID for creating a new phase. Use when planning a new phase.

---

name: find-next-step
description: Find the next unimplemented step in a phase. Use when determining what to work on next.

---

name: find-next-ticket-number
description: Determine the next sequential ticket ID

---

name: get-phase-status
description: Check the current status of a phase. Use when you need to understand where a phase is in the workflow.

---

name: list-tickets
description: List all open (non-archived) tickets
