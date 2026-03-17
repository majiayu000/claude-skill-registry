---
name: hello-auditkit
description: Use this skill to audit, review, validate, or check the quality of AI assistant configurations including prompt text, prompt files, skills (SKILL.md), plugins, MCP servers, agents, hooks, memory files (AGENTS.md, CLAUDE.md, GEMINI.md), and composite configurations. Evaluates against GPT Prompting Guide best practices.
version: 1.1.0
---

<!-- ============ OUTPUT LANGUAGE CONFIGURATION ============ -->
<!-- Supported: en-US, zh-CN, zh-TW, ja-JP, ko-KR, es-ES, fr-FR, de-DE -->

**OUTPUT_LANGUAGE: zh-CN**

<!-- ======================================================= -->

> **IMPORTANT**: All audit output MUST be in the language specified above.

<!-- ============ CRITICAL CONSTRAINTS (GPT-5.2 COMPLIANT) ============ -->

<output_verbosity_spec>
- Default audit report: Follow ref-output-format.md structure exactly
- Progress updates: 1-2 sentences only, at major phase transitions
- Issue descriptions: Concise, with line numbers and evidence
- Do NOT add lengthy explanations where tables suffice
- Do NOT rephrase user's request unless it changes semantics
</output_verbosity_spec>

<design_and_scope_constraints>
- Audit EXACTLY and ONLY what user provides (file, directory, or pasted text)
- Do NOT add unrequested checks or recommendations
- Do NOT apply fixes without explicit user confirmation
- If audit target ambiguous, ask for clarification rather than guessing
- Respect the 5-Point Verification: discard issues that fail any check
</design_and_scope_constraints>

<user_updates_spec>
- Send brief updates (1-2 sentences) only when:
  - Starting a new major phase (Detection, Universal Checks, Type-Specific, Report)
  - Discovering something that changes the audit approach
- Avoid narrating routine file reads or check executions
- Each update must include concrete outcome ("Found X issues", "Loaded Y rules")
- Do NOT expand the audit beyond what user requested
</user_updates_spec>

<uncertainty_and_ambiguity>
- If audit target unclear: ask 1-3 clarifying questions
- If rule interpretation ambiguous: choose simplest valid interpretation
- Never fabricate line numbers, file names, or issue details
- Use hedging language for uncertain assessments: "appears to", "may indicate"
- Base all findings on actual content examined
</uncertainty_and_ambiguity>

<tool_usage_rules>
- When scanning multiple files or checking multiple dimensions, parallelize independent read operations
- Prefer tools over internal knowledge for fresh data
- After writes, restate: what changed, where, validation performed
</tool_usage_rules>

<long_context_handling>
- For audits involving multiple reference files, produce internal outline of key sections first
- Re-state user constraints before generating report
- Anchor findings to specific file:line references
</long_context_handling>

<report_output_spec>
Section 2 Cross-Cutting - GPT Guide Compliance MUST appear FIRST.

Section 3.1 Confirmed Issues - MUST use markdown table:
| # | File | Line | Issue Summary | Dimension | Fix Type |
Group by severity: 🔴 → 🟡 → 🟢, each as separate table.

Section 3.2 Filtered Issues - MUST use markdown table:
| # | File | Line | Issue Description | Filter Reason |

Section 4 Fix Proposals - MUST include for EVERY confirmed issue:
Location, Problem, Impact, Current (code block), Proposal (code block).

Section 5 Conclusion - PHASE GATE:
After outputting, STOP and wait for user input. Do NOT apply fixes until user confirms.
</report_output_spec>

<!-- ============================================================== -->

# Hello-AuditKit: AI Coding Assistant Audit System

## Table of Contents

- [Entry Point](#entry-point)
- [Overview](#overview)
- [Core Principles](#core-principles)
- [Audit Execution](#audit-execution)
- [Reference Files](#reference-files)
- [Special Reminders](#special-reminders)
- [External Documentation](#external-documentation)

## Entry Point

**On skill invocation, first determine the audit target:**

| User Input | Action |
|------------|--------|
| No target specified | Show welcome message and usage guide (see below) |
| File path provided | Audit the specified file |
| Directory path provided | Scan and audit the directory |
| Text content pasted | Audit as prompt text |

**Welcome Message** (when no target):
```
👋 Hello-AuditKit - AI 配置审计工具

支持审计：
• 提示词文本（直接粘贴或任意文件）
• Memory 文件（AGENTS.md, CLAUDE.md, GEMINI.md）
• Skills（含 SKILL.md 的目录）
• Plugins（含 .claude-plugin/ 的目录）

使用方式：
1. 粘贴要审计的提示词文本
2. 提供文件路径：/path/to/file.md
3. 提供目录路径：/path/to/skill/

请提供要审计的内容或路径：
```

**CRITICAL**: After showing welcome, STOP and wait for user input. Do NOT proceed with audit until target is provided.

## Overview

Comprehensive audit system for AI coding assistant configurations:

| Content Type | Identification | Rule File |
|--------------|----------------|-----------|
| **Any Text/File** | Pasted text or any file (any filename) | `type-prompt.md` |
| **AGENTS.md** | Codex agent instructions | `type-memory.md` |
| **CLAUDE.md** | Claude Code memory files | `type-memory.md` |
| **GEMINI.md** | Gemini CLI context files | `type-memory.md` |
| **Skills** | Directory with `SKILL.md` | `type-skill.md` |
| **Plugins** | Directory with `.claude-plugin/` | `type-plugin.md` |
| **Composite** | Memory file + skills/ | `cross-composite.md` |

## Core Principles

> **Source**: Based on Latest GPT Prompting Guide (openai-cookbook/examples/gpt-5)

### Principle 0: GPT Prompting Guide Compliance (MANDATORY)

> **CRITICAL**: This is the PRIMARY audit standard. Every audit MUST check these items and report findings.

**For ALL content containing AI instructions, verify:**

| Check | What to Look For | Severity |
|-------|------------------|----------|
| Verbosity constraints | Explicit length limits present | Severe |
| Scope discipline | Explicit boundaries or prohibition list present | Severe |
| Stop conditions | Strong stop language at phase gates (multi-phase only) | Severe |
| Constraint centralization | Critical rules concentrated, not scattered >3 locations | Severe |
| Prohibition language | Strong language for critical constraints | Warning |
| No fabrication | Grounding instruction for factual tasks | Severe |
| **XML structure enforcement** | XML tags wrap critical constraints (GPT-5.2+) | Severe |

**XML Tags Compliance (GPT-5.2 MANDATORY)**:

> **CRITICAL**: For agentic/multi-phase prompts, XML tags are REQUIRED to prevent format drift. This is a **strict audit rule**.

| Prompt Type | Required XML Tags | Severity if Missing |
|-------------|-------------------|---------------------|
| All with verbosity rules | `<output_verbosity_spec>` | Severe |
| All with scope rules | `<design_and_scope_constraints>` | Severe |
| Agentic/multi-phase | `<user_updates_spec>` | Severe |
| Data extraction | `<extraction_spec>` | Severe |
| Factual/grounding | `<uncertainty_and_ambiguity>` | Severe |
| Tool-using | `<tool_usage_rules>` | Warning |
| Long-context (>10k) | `<long_context_handling>` | Warning |
| High-risk content | `<high_risk_self_check>` | Warning |

**Audit output**: Report GPT Guide Compliance status with evidence for each check, including XML tags compliance.

### Principle 1: GPT-5.2 Specific Checks (For GPT-5.2+ Prompts)

> **Source**: GPT-5.2 Prompting Guide - Key Behavioral Differences

| Check | What to Look For | Severity |
|-------|------------------|----------|
| No task expansion | "Do NOT expand beyond user request" present | Severe |
| No rephrasing | "Do NOT rephrase user's request" present | Warning |
| Design system exploration | "Explore existing design systems" instruction | Warning |
| Style alignment | "Style aligned to design system" instruction | Warning |
| Explicit preferences | Style preferences articulated (not assumed) | Warning |

### Principle 2: 5-Point Verification

Before marking ANY issue, verify:
1. **Concrete Scenario** - Can describe specific failure?
2. **Design Scope** - Within intended boundaries?
3. **Functional Capability** - Can it actually do what it claims? (Requires domain knowledge first)
4. **Flaw vs Choice** - Unintentional error or valid choice?
5. **Threshold Met** - Above quantified threshold?

If ANY fails → Discard the issue

### Principle 3: Occam's Razor

**"If unnecessary, don't add."**

Fix Priority: DELETE > MERGE > RESTRUCTURE > MODIFY > ADD

### Principle 4: AI Capability

- AI CAN infer: synonyms, context, standard terms
- AI CANNOT: 3+ step inference, domain-specific variations
- If <30% would misunderstand → exempt from issue

### Principle 5: Size Tolerance (SKILL.md body only)

| Range | Status |
|-------|--------|
| ≤500 lines | Ideal |
| 500-550 (≤10% over) | **NOT an issue** |
| 550-625 (10-25% over) | Info only |
| >625 lines | Warning |

> **Note**: Reference files have no official line limit. Evaluate based on content nature.

### Principle 6: Prompt Compliance

**For prompts/instructions, verify critical checks** (see `type-prompt.md` → Prompt Compliance Checks):
- Verbosity constraints (Severe)
- Scope boundaries with "do not" list (Severe)
- No fabrication instruction (Severe)
- Output schema for structured tasks (Warning)

### Principle 7: Grounding & No Fabrication

- Base all findings on actual content examined
- Never fabricate line numbers, file names, or issue details
- Use hedging language for uncertain assessments: "appears to", "may indicate"

## Audit Execution

> **CRITICAL**: Each step below is MANDATORY. You must execute (not just read) each check and output evidence of execution.
>
> **Agentic Updates**: Send brief updates (1-2 sentences) only at major phase transitions. Avoid narrating routine tool calls.
>
> **Tool Parallelization**: When scanning multiple files or checking multiple dimensions, parallelize independent read operations for efficiency.

### Step 0: Fetch Latest Prompting Guide (MANDATORY STANDARD)

> **CRITICAL**: The GPT Prompting Guide is a **primary audit standard**, not just a reference. All prompts/instructions MUST be evaluated against these rules.

1. Access this directory page to get file list: `https://github.com/openai/openai-cookbook/tree/main/examples/gpt-5`
2. Select the latest version prompting guide (e.g., `gpt-5-2_prompting_guide.ipynb` > `gpt-5-1_prompting_guide.ipynb` > `gpt-5_prompting_guide.ipynb`)
3. Extract and apply these **mandatory checks** from the guide:
   - **Verbosity constraints**: "≤N sentences/bullets/words" present?
   - **Scope discipline**: "EXACTLY and ONLY what requested" + "Do NOT" list present?
   - **Stop conditions**: Explicit completion criteria for multi-phase content?
   - **No fabrication**: "Never fabricate..." instruction for factual tasks?
   - **Long-context handling**: Outline + constraint restatement for >10k tokens?
   - **Tool preference**: Tools over internal knowledge for fresh data?
   - **Agentic updates**: Brief (1-2 sentences) at major phases only?
   - **XML structure enforcement** (GPT-5.2+): XML tags wrap critical constraints?
4. **XML Tags Compliance Check** (STRICT RULE):
   - Identify prompt type: agentic, extraction, factual, tool-using, long-context, high-risk
   - Check for required XML tags per type (see Principle 0 table)
   - If XML tags missing for applicable type → Flag as Severe
   - Required tags: `<output_verbosity_spec>`, `<design_and_scope_constraints>`, `<user_updates_spec>`, `<extraction_spec>`, `<uncertainty_and_ambiguity>`, `<tool_usage_rules>`, `<long_context_handling>`, `<high_risk_self_check>`
5. Cross-validate with built-in checks in `type-prompt.md`
6. **Flag as Severe** if audited content violates any mandatory check above

**Evidence Output**: Note guide version fetched, list mandatory checks applied (including XML tags), note any violations found.

**If WebFetch fails**: Retry before falling back to offline mode. If still fails, use built-in checks in `type-prompt.md`, note "offline mode - [error reason]" in report.

### Step 1: Detection & Classification

Scan path → identify type → load appropriate rules:

```
Any text/file   → type-prompt.md (default for unrecognized types)
Memory file     → type-memory.md (AGENTS.md, CLAUDE.md, GEMINI.md)
Skill           → type-skill.md (directory with SKILL.md)
Plugin          → type-plugin.md (directory with .claude-plugin/)
Composite       → Apply all + cross-*.md
```

### Step 2: Execute Universal Checks (ALL TYPES)

> **FIRST**: Execute Principle 0 (GPT Guide Compliance) checks before proceeding.

**GPT Guide Compliance Check (MANDATORY FIRST):**

Execute each check from Principle 0 table, record status and evidence (line numbers, quotes).

**Every audit MUST execute these checks from `rules-universal.md`:**

| Category | Action Required | Evidence Output |
|----------|-----------------|-----------------|
| Naming & Numbering | Extract ALL: (1) naming conventions (kebab-case, no special chars), (2) numbered sequences → verify sequential, no duplicates, no gaps, (3) order validation → section order logical, heading hierarchy H1→H2→H3 | "Checked N sequences, M naming issues, K order issues" |
| Reference Integrity | Extract ALL references (file refs, anchor links, numbered refs like R1/Step 2) → verify each target exists, no circular refs | "Checked N refs, M broken, K circular" |
| Structure & Organization | (1) TOC-content match, (2) section categorization correct, (3) template compliance (required sections present, order correct), (4) no orphan sections | "TOC: N entries vs M headings, K mismatches; Template: L issues" |
| Diagram & Flowchart | If exists: (1) node-text consistency, (2) all paths have endpoints, (3) no infinite loops, (4) decision branches complete | "Checked N diagrams, M consistency issues, K logic issues" |
| Language Expression | (1) Ambiguity patterns (may/might/could without condition), (2) terminology consistency (same concept = same term), (3) spelling errors in identifiers/headings, (4) redundant content, (5) LLM wording patterns (hedging language, avoid absolutes, scope constraint wording, verbosity constraint wording) | "Found N ambiguity, M terminology, K spelling, L redundancy, P wording issues" |
| Security & Compliance | Check for hardcoded secrets, paths, credentials; input validation rules | "Checked, N security issues" |
| Size Thresholds | SKILL.md body: apply tiered thresholds (≤500 ideal). Reference files: evaluate by content nature | "SKILL.md: N lines (status)" |
| Rule Logic | If rules exist: (1) no conflicts, (2) no duplicates/semantic equivalents, (3) coverage complete, (4) optimization opportunities (DELETE > MERGE > MODIFY) | "Checked N rules: M conflicts, K duplicates, L gaps" |
| Process Logic | If process/flow defined: (1) all scenarios covered, (2) main flow clear, (3) no dead loops, (4) no conflicting invocations | "Process: N scenarios, M flow issues" |
| Output & i18n | If output format defined: (1) format specification complete, (2) language control correct (if i18n configured), (3) no hardcoded language-specific content | "Output: N format issues, M i18n issues" |
| Prompt Compliance | (1) Verbosity constraints present, (2) Scope boundaries with "do not" list, (3) No fabrication instruction, (4) Output schema for structured tasks, (5) Grounding for uncertain claims, (6) Tool preference over internal knowledge, (7) Agentic updates brief with concrete outcomes, (8) Long-context outline for >10k tokens, (9) **XML tags for critical constraints** (GPT-5.2+) | "Prompt: N verbosity, M scope, K grounding, L tool, P agentic, Q XML issues" |
| Conversational/Multi-Phase | If content has phases: (1) constraints at TOP, (2) explicit stop conditions, (3) scope drift prevention, (4) phase gates, (5) **constraint centralization** (rules in ≤3 locations), (6) **stop condition strength** (strong vs weak), (7) **prohibition language strength** ("禁止/Do NOT" vs "不要/don't") | "Conversational: N issues (centralization: X, stop strength: Y, prohibition: Z)" |

**Numbering Check Execution** (commonly missed):
1. Find all numbered lists (1. 2. 3. or Step 0, Step 1, etc.)
2. Verify: sequential? no duplicates? no gaps?
3. Find all TOC entries → verify each has matching heading
4. Cross-section: if steps span sections (Step 0 here, Step 3 there), verify continuity

### Step 3: Execute Type-Specific Checks

**Based on content type, execute ALL checks in the relevant file:**

#### For Prompts (`type-prompt.md`):
| Check Category | Action |
|----------------|--------|
| Structure Validation | Verbosity constraints? Scope boundaries? Output format? |
| Content Quality | Specific instructions? Not vague? |
| LLM Best Practices | Freedom level match? Grounding? Ambiguity handling? |
| Prompt Compliance | Verbosity limits? "Do not" list? No fabrication? Schema? Self-check? |
| **XML Structure Enforcement** | XML tags for verbosity? scope? extraction? updates? (GPT-5.2+) |
| Conversational/Multi-Phase | If has phases: constraints at TOP? Stop conditions (strong)? Scope drift prevention? Phase gates? **Constraint centralization?** **Prohibition language strength?** |
| Audit Checklist | Execute all Fatal/Severe/Warning checks at end of file |

#### For Memory Files (`type-memory.md`):
| Check Category | Action |
|----------------|--------|
| Structure Validation | File location? Merge hierarchy? |
| Import Syntax | Valid `@path` imports? |
| Content Quality | Specific? Actionable? Not vague? |
| Instruction Quality | Verbosity constraints? Scope boundaries? |

#### For Skills (`type-skill.md`):
| Check Category | Action |
|----------------|--------|
| Directory Validation | SKILL.md exists? Correct filename? |
| Frontmatter | name (≤64 chars), description (≤1024 chars, character count not bytes), triggers in description? |
| Body Size | SKILL.md: ≤500 ideal, >625 warning. References: no limit, evaluate by content |
| Script Integrity | Declared scripts exist? Imports valid? Shebang? Error handling? |
| References | Has "when to read" guidance? |
| Conversational/Multi-Phase | If body has phases: apply checks from `type-prompt.md` including **constraint centralization**, **stop condition strength**, **prohibition language** |

#### For Plugins (`type-plugin.md`):
| Check Category | Action |
|----------------|--------|
| Structure | plugin.json in .claude-plugin/? Components at root? |
| Path Variables | Uses relative paths or env variables? No hardcoded absolute paths? |
| Commands | Valid frontmatter? allowed-tools valid? |
| Agents | name, description, tools valid? |
| Hooks | Wrapper format? Valid matchers? Scripts exist? |
| MCP/LSP | Valid JSON? Paths correct? No hardcoded secrets? |

### Step 4: Execute Cross-Cutting Checks (Multi-file Systems)

**For Skills, Plugins, Composites, execute ALL checks from:**

#### From `cross-design-coherence.md`:
| Check | Action |
|-------|--------|
| Full Directory Scan | Enumerate ALL files, classify each, build rule inventory |
| Design Philosophy | Extract principles from all files, check consistency |
| Rule Propagation | Global rules applied in local files? |
| Conflict Detection | Same-file contradictions? Cross-file contradictions? |
| Structural Redundancy | Repeated sections? Duplicate tables? Parallel content? → centralize |
| Red Flags | SKILL.md >625 lines? Scattered rules (>3 files)? Circular deps? |

#### From `cross-progressive-loading.md`:
| Check | Action |
|-------|--------|
| Content Level Audit | L1 ≤100 words? L2 ≤500 lines? L3: evaluate by content nature |
| Content Placement | Core workflow in L2? Edge cases in L3? |
| Reference Guidance | Each reference has "when to read"? |
| Anti-Patterns | Metadata bloat? Monolithic body? Essential in L3? |

#### From `cross-composite.md`:
| Check | Action |
|-------|--------|
| Reference Integrity | All cross-file refs valid? |
| Terminology Consistency | Same concept = same term across files? |
| Numbering Consistency | Sequential across all files? No duplicates? |
| Script Integrity | All declared scripts exist? Imports valid? |

### Step 5: Issue Verification (5-Point Check)

For each suspected issue, verify ALL points:
1. **Concrete scenario** - Can describe specific failure?
2. **Design scope** - Within intended boundaries?
3. **Functional capability** - Does implementation match claimed capability?
4. **Flaw vs choice** - Unintentional error or valid design?
5. **Threshold met** - Above quantified threshold?

If ANY fails → Discard the issue (move to Filtered)

**For "missing/incomplete" issues**: Re-read the source content fully before confirming. ASCII diagrams are prone to parsing errors on first scan.

### Step 6: Fix Proposal Verification (Principle Check)

**CRITICAL**: Before outputting ANY fix proposal, verify it against core principles:

| Check | Question | If NO → |
|-------|----------|---------|
| Occam's Razor | Is this addition truly necessary? Could the goal be achieved by DELETE/MERGE/MODIFY instead of ADD? | Reconsider fix approach |
| AI Inference | Can AI infer the correct behavior from existing examples/context/patterns? | Do NOT add explicit rule |
| Hardcoding Check | Is this adding hardcoded values (e.g., "≤5 bullets", "≤200 words") where AI should judge based on context? | Remove hardcoded values |
| Prohibition Check | Is this adding "do not" rules where AI already understands from intent/context? | Remove unnecessary prohibition |
| Example Redundancy | Does the original design already convey intent through examples/structure? | Do NOT add redundant rules |

**Verification Process**:
1. For each proposed fix, ask: "If I remove this fix, would AI still produce correct output based on existing content?"
2. If YES → The fix is unnecessary, discard it
3. If NO → Verify the fix uses minimal intervention (prefer MODIFY over ADD)

**If ANY check fails → Revise or discard the fix proposal**

### Step 7: Generate Report

Follow `references/ref-output-format.md` for structure.

**Section 2 Cross-Cutting Analysis MUST include:**
- Naming & Numbering: actual check results with specific findings
- TOC-Content Match: comparison results
- Reference Integrity: broken refs listed
- (For multi-file) Design Coherence, Progressive Loading results

**Section 3 Issue Inventory MUST include:**
- Verification Statistics: "Scanned X → Verified Y → Filtered Z"
- Both Confirmed and Filtered issues with filter reasons

### Step 8: Wait for User Confirmation (PHASE GATE)

> **CRITICAL**: After generating the report, STOP and wait for user input. Do NOT apply any fixes automatically.

**User interaction flow:**
1. Output complete audit report (Sections 0-5)
2. **STOP** - Wait for user to select which fixes to apply
3. Only after user confirms (e.g., "1", "1,2", "all") → Apply selected fixes
4. If user provides no selection → Do nothing, wait

## Reference Files

### Layer 0: Core Methodology (Immutable Principles)

Read `references/methodology-core.md` when:
- Need to verify if something is truly an issue
- Deciding fix priority
- Understanding AI capability boundaries

### Layer 1: Universal Rules (Common Rules)

Read `references/rules-universal.md` when:
- Starting any audit
- Need Should Flag / Should NOT Flag patterns
- Checking size thresholds

### Layer 2: Type-Specific Rules (Type Rules)

| File | Read When |
|------|-----------|
| `references/type-prompt.md` | Auditing standalone prompts |
| `references/type-memory.md` | Auditing AGENTS.md, CLAUDE.md, GEMINI.md |
| `references/type-skill.md` | Auditing skills (SKILL.md, scripts) |
| `references/type-plugin.md` | Auditing plugins, hooks, MCP, LSP |

### Layer 3: Cross-Cutting Rules (Cross-Cutting Rules)

| File | Read When |
|------|-----------|
| `references/cross-composite.md` | Auditing multi-component systems |
| `references/cross-design-coherence.md` | Checking design consistency |
| `references/cross-progressive-loading.md` | Evaluating content placement |

### Layer 4: Reference Materials (Reference Materials)

| File | Read When |
|------|-----------|
| `references/ref-output-format.md` | Generating audit report |
| `references/ref-checklist.md` | Need dimension checklist |
| `references/ref-quick-reference.md` | Quick lookup of patterns |

## Special Reminders

### Key References by Topic

| Topic | Reference File |
|-------|---------------|
| Report structure & format | `ref-output-format.md` |
| Issue filtering rules | `rules-universal.md` → Should NOT Flag |
| False positive prevention | `rules-universal.md` → Verification Questions |
| Size thresholds | `rules-universal.md` → Universal Size Thresholds |
| Checklist by dimension | `ref-checklist.md` |
| LLM prompting best practices | `type-prompt.md` → LLM Prompting Best Practices |

### Quick Filtering Rules

| Condition | Action |
|-----------|--------|
| ≤10% over recommended | NOT an issue |
| AI can infer | NOT an issue |
| Design choice | NOT an issue |

## External Documentation

| Platform | Source |
|----------|--------|
| Claude Code | github.com/anthropics/claude-code |
| Codex CLI | github.com/openai/codex/tree/main/codex-cli |
| Gemini CLI | github.com/google-gemini/gemini-cli |
| Anthropic Docs | docs.anthropic.com |
| OpenAI Docs | github.com/openai/openai-cookbook |
| GPT Prompting Resources | github.com/openai/openai-cookbook/tree/main/examples/gpt-5 |

> **Version Policy**: Always use the **latest version** of GPT prompting guides as authoritative source. When multiple versions exist in the gpt-5 directory, prefer the highest version number (e.g., gpt-5.2 over gpt-5.1 over gpt-5). The directory contains prompting guides, troubleshooting guides, and optimization cookbooks.
