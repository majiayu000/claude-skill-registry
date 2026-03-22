---
description: "Create new Cursor skills following the Agent Skills spec. Use when: (1) creating automation for repeatable tasks, (2) documenting team patterns, (3) packaging domain knowledge for reuse. Guides through skill qualification, structure, frontmatter, content organization, and validation."
tags: [skill-authoring, automation, documentation]
---

# Create New Skill

## When to Use

- Creating automation for repeatable tasks
- Documenting team patterns and workflows
- Packaging domain knowledge for reuse
- Building new skills following the Agent Skills spec

## Skill Structure (Agent Skills Spec)

Based on the [Agent Skills specification](https://agentskills.io/specification). See `references/agent-skills-spec.md` for the full spec.

Each skill is a **folder** containing a `SKILL.md` file:

```
skill-name/
├── SKILL.md           # Required - main skill file
├── scripts/           # Optional - executable helpers
├── references/        # Optional - reference docs
└── assets/            # Optional - templates, images, data files
```

### Frontmatter

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | **Yes** | Must match folder name. Lowercase, hyphens only, 1-64 chars. |
| `description` | **Yes** | What it does + when to use it. Max 1024 chars. |
| `tags` | No | List of lowercase kebab-case strings for catalog discovery. |
| `license` | No | License name or reference to bundled file. |
| `compatibility` | No | Environment requirements (tools, network, etc). |
| `metadata` | No | Arbitrary key-value pairs (author, version, etc). |

Example:
```yaml
---
name: my-skill
description: "Does X and Y. Use when: (1) scenario A, (2) scenario B."
tags: [workflow, git]
metadata:
  author: orshalev
  version: "1.0"
---
```

### Progressive Disclosure (from spec)

1. **Metadata** (~100 tokens): `name` + `description` loaded at startup for ALL skills
2. **Instructions** (<5000 tokens): full SKILL.md body loaded when skill activates
3. **Resources** (on demand): files in scripts/, references/, assets/ loaded only when needed

Keep SKILL.md under 500 lines. Move detailed reference material to separate files.

**⚠️ Obsolete fields:** `alwaysApply`, `globs` - DO NOT USE in skills

---

## 0. Skill Qualification

Before writing a skill, verify it’s needed:

* [ ] Is the task repeatable across features or teams?
* [ ] Does the task require specific domain knowledge?
* [ ] Are there already related skills that offer reusable structure?

If YES to any → proceed. If NO → use inline prompt or comment instead.

## 1. Overview (# Why?)

This skill ensures new Cursor skills are created with adequate context by referencing existing ones. It guides the agent to reuse working patterns, enforce domain-specific expectations, and apply context augmentation for stateless correctness.

## 2. Requirements (# What?)

* Reference at least 2 similar rules for structure/patterns.
* **Analyze 5-10 real codebase implementations** to identify gaps and patterns.
* Use the full 6-part task rule structure with **progressive disclosure**.
* Include domain-specific sections when needed (types, keys, state, flags, UI).
* **Apply conditional language** to distinguish defaults from alternatives.
* Provide testing scaffold, naming conventions, and pitfalls.
* **Assess success rate** against real implementations (target 90%+ coverage).
* Clarify file triggers with `globs` and explain `alwaysApply`.

## 3. Progress Tracker

* [ ] ✅ Find 2 similar existing rules
* [ ] ✅ Analyze real codebase implementations
* [ ] ✅ Identify patterns and gaps systematically
* [ ] ✅ Draft metadata and description
* [ ] ✅ Write core structure with progressive disclosure
* [ ] ✅ Add domain-specific sections (type, naming, flags)
* [ ] ✅ Apply conditional language for alternatives
* [ ] ✅ Validate rule completeness and success rate

## 4. Implementation Plan

### Phase 1: Research

1. Search existing skills and rules for similar patterns:
   - Local skills: `.cursor/skills/*/SKILL.md`
   - Personal skills: `.cursor/skills/personal/*/SKILL.md`
   - Community catalog: `.cursor/skills/community/catalog.json` (if linked — see `examine-skills`)
   - Legacy rules: `.cursor/rules/**.mdc`
2. Prioritize similar:

   * Domains (state, services, analytics, feature flags)
   * Trigger files (`globs`), structure, or behavior
3. Copy excerpts or summarize styles:

   #### Similar Rule Summary

   * Rule: `@persistent_state_add_property.mdc`

     * Patterns: Type-specific encode/decode, `Behavior` test scaffold
     * Gotchas: Forgetting key naming and triple mapping
   * Rule: `@assignments_add_experiment_group.mdc`

     * Patterns: Feature flag, test matrix, state-to-UI linkage

### Phase 1A: Download Supporting Assets (OPTIONAL)
If the user provides Google Drive URLs for screenshots, PDFs, or other assets,
download them and store alongside the skill for future reference.

```bash
# One-time setup (see scripts/gdrive_cli/README.md for credentials.json)
cd scripts/gdrive_cli
uv run gdrive auth

# Download asset into the new skill's references folder
uv run gdrive download "URL" -o "skills/<skill-name>/references"
# Use --format when exporting Docs/Sheets/Slides (e.g. --format pdf or --format md)
```

Reference the downloaded files in the "Context & References" section.

### Phase 1B: Real Codebase Analysis (CRITICAL)

3B. **Analyze actual implementations** to identify gaps and patterns:

   ```bash
   # Find 5-10 real implementation files, not just examples
   find . -name "*ExperimentGroup*.swift" | head -10
   find . -name "*Reducer*.swift" | head -10
   find . -name "*PresentationState*.swift" | head -10
   ```

3C. **Systematic Gap Analysis**:
   * What patterns appear in 70%+ of files but aren't in current rules?
   * What advanced patterns exist for complex cases?
   * What alternative approaches do experienced developers use?
   * What architecture mistakes do files reveal?

3D. **Categorize findings**:
   * **Standard Requirements**: Must always be included
   * **Preferred Alternatives**: Recommend first, show alternatives
   * **Optional Additions**: Use when specific needs arise
   * **Advanced Patterns**: For complex cases only

### Phase 2: Define Rule Header

4. Set:

   * `description`: What this rule automates or enforces
   * `globs`: Pattern like `**/PersistentState*.swift` (AVOID – see note below)
   * `alwaysApply`: **Always `false`**. Only tech leads are allowed to choose otherwise.

   **[!IMPORTANT] About File Triggers:**
   - Most rules should be **manually triggered** by tagging (`@rule_name`).
   - Avoid using `globs` unless absolutely necessary.
   - Rules with extensive instructions (>500 lines) should **NEVER** auto-apply.
   - Auto-applying can consume significant context window and interfere with routine edits.

### Phase 3: Write Rule Content with Progressive Disclosure

5. Include these standard sections:

#### Overview

Explain the problem or context driving this rule.

#### Requirements

Checklist of outcomes or constraints.

#### Progress Tracker

Step-by-step visual indicator.

#### Implementation Plan

Organize by phases. Use imperative markdown bullets.
**CRITICAL**: Use progressive disclosure - show DEFAULT patterns first, then alternatives.

#### Context & References

List any:

* `@file.swift` or `@existing-rule.mdc`
* APIs or data contracts
* Screenshots: `<!-- Screenshot: mdc:/assets/example.png -->`

#### Constraints & Done

What NOT to change. Completion criteria.

5B. **Apply Progressive Disclosure Strategy**:
   * Show **common/default** patterns prominently
   * Mark **alternatives** clearly as such
   * Use **conditional guidance**: "Use when...", "Optional for...", "Required when..."
   * Avoid overwhelming beginners with advanced patterns upfront

### Phase 3B: Progressive Disclosure Principles

**[!CRITICAL] Always structure information from common to rare:**

1. **Lead with defaults (80 % cases)**
   - Show the standard approach prominently.
   - Mark with `// ✅ PREFERRED:` or `### ✅ Common Case (DEFAULT):`.

2. **Present alternatives conditionally**
   - Use `// ⚠️ ALTERNATIVE:` for less common approaches.
   - Always explain WHEN to use: "only when [specific condition]".
   - Consider commenting out alternative code blocks with `/* */`.

3. **Critical user decisions**
   - Mark with `[!IMPORTANT] Ask the user before choosing.`
   - Never assume configuration choices (e.g., "should run in China", "should run on iPad").
   - List options clearly for user selection.

4. **Avoid encouraging shared resource modifications**
   - Don't encourage adding to shared enums (e.g., `CommonUserAffectedReason`).
   - Frame as: "only when multiple use cases arise **AND** with explicit approval".

### Phase 3C: Quality Gate & Validation Checklist

Before finalizing the rule, run these mandatory checks to avoid the most common author-ing mistakes noticed in past reviews:

1. **PR/Commit Accuracy**
   * Verify the PR description and commit body mention **only** the rules/files actually added or changed.
   * Remove stale references to rules that were **NOT** part of the diff.

2. **Reference Integrity**
   * For any referenced code file that might be deleted in the future, paste a **minimal self-contained snippet** inside the rule rather than only the file path.

3. **User-Driven Decisions**
   * Replace any domain-specific default assumption (e.g. _runInChina_, _reasonsAffectedUser_) with `// TODO(ask-user)` placeholders that cause a compile-time error (`#error("Ask user")` in Swift) until the user provides explicit instructions.

4. **Naming & Enum Accuracy**
   * Double-check domain names against the source code (e.g. `CommonUserAffectedReason` vs `UserAffectedReason`).
   * Ensure property names in examples conform to actual conventions (alphabetical order, suffixes, etc.).

5. **Anti-Pattern Sweep**
   * Search the draft for known anti-patterns such as `loadOptional(.key) ?? defaultValue` and replace with the canonical API (`load(.key, default:)`).

6. **Context Budget**
   * Keep examples concise (<20 lines each) and remove super-fluous design-specific code that does not affect the logical flow.

7. **Checklist Completion**
   * Confirm all items in this Quality Gate are ticked before marking the rule as complete.

### Phase 4: Add Domain-Specific Sections with Conditional Language

6. **Structure domain-specific guidance using progressive disclosure patterns**:

   Domain-specific sections guide users through different implementation paths based on their specific needs. The key is showing the most common pattern first, then progressively revealing alternatives for more complex scenarios.

   **Core Principles:**
   - Lead with the DEFAULT/common case (80% usage)
   - Mark alternatives clearly with conditions
   - Use visual markers (✅, ⚠️) for quick scanning
   - Include inline comments for decision points

   **Structural Patterns to Use:**

   ```markdown
   ## [Number]. [Domain-Specific Topic]

   ### ✅ [Common Case] (DEFAULT):
   [Code/guidance for the standard approach]

   ### ✅ [Alternative Case] (when [specific condition]):
   [Code/guidance for this variant]

   ### ⚠️ [Rare/Advanced Case] (only when [edge condition]):
   [Code/guidance for exceptional situations]
   ```

   **Example from Persistent State:**
   ```markdown
   ## 5. Type-Specific Handling

   ### ✅ Dates, Bools, Ints:
   - Encode as-is using `loadOptional(.key)`
   - Use `StoringBehavior<Date?>` for optional dates

   ### ✅ Enums:
   [Enum pattern with .Stored wrapper]

   ### ✅ Arrays & Dictionaries:
   - Encode directly if elements are primitives
   - For custom types, convert to `.Stored` then encode
   ```

   **Decision Points Pattern:**
   ```swift
   // ✅ PREFERRED: Use existing CommonUserAffectedReason when possible.
   static func reasonsAffectedUser(params: AppRDXParams) -> [String] {
     return CommonUserAffectedReason.getReasonStrings(...)
   }

   // ⚠️ ALTERNATIVE: Create custom logic only when CommonUserAffectedReason insufficient.
   /*
   static func reasonsAffectedUser(params: AppRDXParams) -> [String] {
     // Custom implementation
   }
   */
   ```

   **Critical User Decisions:**
   ```markdown
   [!IMPORTANT] Ask the user before choosing.
   - Option A: Use when [specific condition]
   - Option B: Use when [different condition]
   ```

   **Optional Sections Pattern:**
   ```markdown
   ### Phase 2B: Add Static Helpers (OPTIONAL - for complex eligibility):
   // Only add when business logic is reused across multiple files
   ```

7. If defining **keys/constants**:

#### Naming Conventions

* Specify specific format: `someStorageKey_MM_YY`, `someExperimentGroupName_MM_YYYY`, `SomeProtocolsIMPL`
* Must describe purpose and have version suffix

8. If crossing **services/state/UI**:

#### Data Flow Touchpoints

* Update: `stateModel → manager → UI bindings`
* Integration points: list all required files

9. If using **feature flags**:

#### Experiment Handling

* Describe expected gating: `if (featureGate.isEnabled()) { ... }`
* Include default behavior and test matrix

10. If UI is affected:

#### UI Notes

* Link design spec or include:
  `<!-- Screenshot: mdc:/assets/foo.png -->`

11. If common mistakes exist:

#### Common Gotchas

* Example: "Don’t forget to map all 3 key paths"

## 7. Common Rule Writing Pitfalls to Avoid

**DO NOT:**
* Set `alwaysApply: true` (unless you're a tech lead with specific reasons).
* Create rules >500 lines that auto-apply via globs.
* Assume user preferences (always use `[!IMPORTANT]` for decisions).
* Encourage modifications to shared resources without approval.
* Include overly specific design details that change frequently.
* Provide instructions for actions agents cannot perform.
* Use incorrect terminology without verifying in codebase.

**DO:**
* Default to manual triggering with `alwaysApply: false`.
* Use progressive disclosure (common → alternative → advanced).
* Mark critical decisions for user input.
* Focus on patterns and references rather than rigid implementations.
* Acknowledge platform limitations explicitly.
* Verify all names, properties, and conventions from actual code.

### Phase 5: Validate and Assess Success Rate

12. Match structure to `@persistent_state_add_property` and `@assignments_add_experiment_group`
13. Ensure headings, checkboxes, codeblocks follow Lightricks standards
14. Check all provided code is minimal, real, and copyable

### Phase 5B: Success Rate Assessment

15. **Test rule effectiveness** against real codebase files:
   * Would this rule successfully guide creation of 5-10 analyzed files?
   * What percentage of common use cases are covered?
   * What percentage of complex use cases have guidance?
   * Estimate: Simple cases ___%, Medium cases ___%, Complex cases ___%

16. **Identify remaining gaps**:
   * What patterns are still missing?
   * What would fail with current rule guidance?
   * What requires expert knowledge not captured?

### Phase 5C: Iteration and User Feedback

17. **Be prepared to iterate** when users provide corrections:
   * Architecture mistakes happen - user corrections are valuable
   * Update patterns based on real usage experience
   * Adjust progressive disclosure based on feedback
   * Don't override existing requirements - add alternatives instead

## 5. Context & References

* Referenced rules:
  * `@persistent_state_add_property.mdc`
  * `@assignments_add_experiment_group.mdc` - **Recently updated using this methodology**

* **Successful Case Study**: Experiment Group Rule Update
  * Analyzed 10 real ExperimentGroup files systematically
  * Identified 10 critical gaps through codebase analysis
  * Applied progressive disclosure strategy (30% → 90% success rate)
  * Used conditional language to avoid breaking existing patterns
  * Integrated user feedback to correct architecture mistakes

* Cursor Docs: Rule triggers and types

## 6. Constraints & Done

* DO NOT guess APIs or file paths — use existing ones.
* DO NOT write rules without researching prior art.
* **DO NOT override common patterns** — add alternatives instead.
* **DO NOT force advanced patterns** — use progressive disclosure.
* ✅ **Quality Gate checklist completed**
* ✅ All 6 core sections written
* ✅ **Real codebase analysis completed** (5-10 files)
* ✅ **Progressive disclosure applied** (defaults → alternatives → advanced)
* ✅ **Conditional language used** (PREFERRED vs ALTERNATIVE)
* ✅ Domain scaffolds added (types, keys, UI, flags)
* ✅ **Success rate assessed** (target 90%+ coverage)
* ✅ Refs to prior rules included
* ✅ Globs and triggering logic defined

### Phase 5D: Skill Validation Checklist

Before finalizing, verify compliance with [Agent Skills spec](https://agentskills.io/specification):

- [ ] **Folder structure**: `{skill-name}/SKILL.md` (not a standalone file)
- [ ] **`name` field** in frontmatter matches folder name (lowercase, hyphens only, 1-64 chars)
- [ ] **`description` field** clearly describes what the skill does and when to use it (max 1024 chars)
- [ ] **No obsolete fields** (`alwaysApply`, `globs`) in frontmatter
- [ ] **SKILL.md under 500 lines** — move details to references/
- [ ] Optional: `tags` for catalog discovery
- [ ] Optional: `references/` folder for supporting docs
- [ ] Optional: `scripts/` folder for automation helpers

Additional quality checks:
- [ ] Progressive disclosure applied (defaults → alternatives)
- [ ] User decisions marked with `[!IMPORTANT]`
- [ ] All terminology verified against codebase
- [ ] Platform limitations acknowledged
