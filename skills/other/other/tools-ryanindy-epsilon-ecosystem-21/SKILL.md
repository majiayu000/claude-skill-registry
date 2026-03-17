---
name: implementation-planner
description: Senior Architect skill for creating atomic, safe, and highly detailed technical implementation plans. Transforms requirements into a step-by-step execution strategy with built-in verification.
version: 2.1.0
tier: 2
metadata:
  author: Epsilon Prime
  jurisdiction: US-WA
  last_sync: 2026-02-08
---

# 🎯 Implementation Planner
**Mission:** To architect the path forward. A project without a plan is just a "Jerry-project" waiting to fail. This skill ensures that every modification is mapped, every integration is verified, and every phase is reversible.

## 🛠️ Operational Mandates
1.  **No Magic Steps:** Never use vague terms like "update logic." Every step MUST specify the file, line range (if possible), and exact intent.
2.  **Verification-Driven:** Every phase MUST include both Automated (tests/builds) and Manual (reproducible steps) success criteria.
3.  **Logical Phasing:** Always sequence changes from "Core" to "Surface" (e.g., Database -> Logic -> API -> UI).
4.  **Interactive Alignment:** Ask critical technical questions *before* finalizing the plan. Don't assume; verify.

## 🔄 Standard Workflows

### 1. Context Gathering
1.  **Locate:** Find the active ticket or PRD in the session directory.
2.  **Investigate:** Use `codebase_investigator` to find the exact files and symbols affected.
3.  **Clarify:** Surface any architectural conflicts or missing dependencies to the user.

### 2. Plan Drafting
1.  **Structure:** Define atomic phases (e.g., Phase 1: Schema, Phase 2: Logic).
2.  **Write:** Save the plan to `[Session_Root]/plan.md` using the Standard Implementation Template.
3.  **Review:** Call `activate_skill("plan-reviewer")` to self-audit for safety and specificity.

### 3. Finalization
1.  **Link:** Attach the plan to the corresponding Linear/Markdown ticket.
2.  **Promote:** Update ticket status to "Plan in Review."

## 🗄️ RAG Context
- **Primary Collection:** `decisions/` (Architecture Decisions)
- **Secondary Collection:** `rag/core_knowledge/epsilon` (Operational Standards)
- **Search Keys:** `implementation template`, `architectural patterns`, `phased deployment`

## 🧰 Authorized Tools
- `codebase_investigator` (Context Discovery)
- `write_file` (Plan Creation)
- `skills/plan_reviewer.skill.md` (Self-Audit)

## 📝 Execution Example
> **User:** "Plan the new SMS logging feature."
> **Action:** 
> 1. Maps `sms_handler.py`.
> 2. Drafts Phase 1 (DB Schema) and Phase 2 (Handler Update).
> 3. Defines `pytest` as automated verification.
> 4. Writes `plan.md`.
