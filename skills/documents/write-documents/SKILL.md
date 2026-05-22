---
name: write-documents
description: Apply when creating or editing INFO, SPEC, IMPL, TEST, FIX documents, or STRUT plans
---

# Document Writing Guide

This skill contains document templates and formatting rules.

## Verb Mapping

This skill implements:
- [WRITE-INFO] - Create INFO documents (use INFO_TEMPLATE.md)
- [WRITE-SPEC] - Create SPEC documents (use SPEC_TEMPLATE.md)
- [WRITE-IMPL-PLAN] - Create IMPL documents (use IMPL_TEMPLATE.md)
- [WRITE-TEST-PLAN] - Create TEST documents (use TEST_TEMPLATE.md)
- [WRITE-FIX] - Create FIX documents (use FIXES_TEMPLATE.md)
- [WRITE-FAIL] - Create/update FAILS.md (use FAILS_TEMPLATE.md)
- [WRITE-REVIEW] - Create _REVIEW.md documents (use REVIEW_TEMPLATE.md)
- [WRITE-TASKS-PLAN] - Create TASKS documents (use TASKS_TEMPLATE.md)
- [WRITE-STRUT] - Create/insert STRUT plans (use STRUT_TEMPLATE.md)

## MUST-NOT-FORGET

- Use lists, not Markdown tables
- No emojis - ASCII only, no `---` markers between sections
- Header block: Doc ID (required), Goal (required), Target file, Depends on (omit if N/A)
- Every document MUST have a unique ID
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Be exhaustive: list ALL domain objects, actions, functions
- Document History section at end, reverse chronological
- Use box-drawing characters (├── └── │) for trees
- SPEC, IMPL, TEST documents MUST have MUST-NOT-FORGET section (after header block, before TOC)

## Document Writing Rules

- Enumerations: use comma-separated format (`.pdf, .docx, .ppt`), NOT slash-separated (`.pdf/.docx/.ppt`)
- Ambiguous modifiers: when a clause can attach to multiple nouns, split into separate sentences
  - BAD: "Files starting with '!' signify high relevance that must be treated with extra attention."
  - GOOD: "Files starting with '!' indicate high relevance. This information must be treated with extra attention."

## Templates (Required)

You MUST read the appropriate template before creating documents:
- `INFO_TEMPLATE.md` - Research and analysis documents
- `SPEC_TEMPLATE.md` - Technical specifications
- `IMPL_TEMPLATE.md` - Implementation plans
- `TEST_TEMPLATE.md` - Test plans
- `TASKS_TEMPLATE.md` - Task plans (partitioned work items)
- `FIXES_TEMPLATE.md` - Fix tracking documents
- `FAILS_TEMPLATE.md` - Failure log (lessons learned)
- `REVIEW_TEMPLATE.md` - Review documents (_REVIEW.md)
- `WORKFLOW_TEMPLATE.md` - AGEN verb workflow structure
- `STRUT_TEMPLATE.md` - STRUT plans (embeddable in any document)

## Usage

1. Read this SKILL.md for core rules
2. Read the template for your document type (required)
3. For SPEC documents: also read `SPEC_RULES.md` (required)
4. Follow the template structure exactly, except when user requests exceptions or different structure

## File Naming

- `_INFO_[TOPIC].md` - Research, analysis, preparation documents
- `_SPEC_[COMPONENT].md` - Technical specifications
- `_SPEC_[COMPONENT]_UI.md` - UI specifications
- `_IMPL_[COMPONENT].md` - Implementation plans
- `_IMPL_[COMPONENT]_FIXES.md` - Fix tracking during implementation
- `SPEC_[COMPONENT]_TEST.md` - Test plan for specification
- `IMPL_[COMPONENT]_TEST.md` - Test plan for implementation
- `TASKS_[TOPIC].md` - Task plans (partitioned work items)
- `!` prefix for priority docs that must be read first

## Agent Behavior

- Be extremely concise. Sacrifice grammar for concision.
- NEVER ask for continuations when following plans.
- Before assumptions, propose 2-3 implementation alternatives.
- List assumptions at spec start for user verification.
- Optimize for simplicity.
- Re-use existing code by default (DRY principle).
- Research APIs before suggesting; rely on primary sources only.
- Document user decisions in "Key Mechanisms" and "What we don't want" sections.

## ID System

See `[AGENT_FOLDER]/rules/devsystem-ids.md` rule (always-on) for complete ID system.

**Quick Reference:**
- Document: `[TOPIC]-[DOC][NN]` (IN = Info, SP = Spec, IP = Impl Plan, TP = Test Plan)
  - Example: `CRWL-SP01`, `AUTH-IP01`
- Spec-Level: `[TOPIC]-[TYPE]-[NN]` (FR = Functional Requirement, IG = Implementation Guarantee, DD = Design Decision)
  - Example: `CRWL-FR-01`, `AUTH-DD-03`
- Plan-Level: `[TOPIC]-[DOC][NN]-[TYPE]-[NN]` (EC = Edge Case, IS = Implementation Step, VC = Verification Checklist, TC = Test Case)
  - Example: `CRWL-IP01-EC-01`, `AUTH-TP01-TC-05`

## Writing AGEN Verb Workflows

AGEN verbs map directly to Windsurf workflows. See `WORKFLOW_TEMPLATE.md` for:
- Workflow structure template
- General vs Specific parts pattern
- Context discovery pattern
- Strategy pattern
- Output rules