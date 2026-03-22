---
name: advising-legal
description: "Use when providing educational legal structure guidance for entrepreneurs. Covers business entity selection, liability considerations, IP protection, and professional referral triggers. Educational only - not legal advice."
---

# Advising Legal Skill

Educational legal guidance for entrepreneurs navigating business structure and IP protection decisions.

**This skill provides informational purposes only and is not legal advice.**

---

## Disclaimer Enforcement

Every output produced by this skill MUST include a disclaimer header within the first 10 lines. The disclaimer is automatically prepended before any substantive content, including in standalone mode. Every output file and all output sections include the disclaimer.

Use the canonical disclaimer template file at `references/disclaimer-template.md`. If the disclaimer template is missing, HALT immediately.

---

## Step 1: Read User Profile at Session Start

Read the user profile file to adjust explanation depth based on experience level:

```
Read(file_path="user-profile.yaml")
```

- The user profile is **read-only** - this skill does not modify the profile file and must not write to or mutate user profile data
- The user profile is **profile optional** - if absent or missing, apply graceful fallback with **no error** produced

## Step 2: Determine Experience Level and Adjust Explanation Depth

Adjust explanation depth to match the detected experience level:

| Experience Level | Verbosity | Behavior |
|-----------------|-----------|----------|
| **beginner** | High verbosity - full explanations with definitions, examples, step-by-step walkthroughs | Adjust pacing to be slower and more thorough |
| **intermediate** | Moderate verbosity - concise explanations assuming basic knowledge | Standard detail level for most users |
| **advanced** | Low verbosity - brief summaries, direct recommendations | Adjust pacing to be faster and more direct |

**Fallback behavior:** When user profile is absent or experience level is not specified, **fallback to intermediate** as the default experience level with silent fallback.

## Step 3: Detect Mode (Standalone vs Project-Anchored)

Determine operating mode by checking for project context:

```
Read(file_path="devforgeai/specs/context/source-tree.md")
```

**If source-tree.md is present** -> **Project-anchored mode**: Read context files in read-only mode and enrich guidance with project-specific details. Cite source context file and line range in recommendations.

```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
```

**If source-tree.md is absent** -> **Standalone mode**: Complete the full guided legal assessment without project context. Gracefully omit project-specific references and inform the user that project-anchored enrichment is unavailable. The skill operates without a project directory and handles context missing scenarios by continuing with general guidance only.

## Step 4: Load Reference for Requested Topic

Load the appropriate reference file based on the workflow order declared below. Each legal guidance phase is sourced from a separate reference file via progressive loading.

**Business Structure Guidance:**

```
Read(file_path=".claude/skills/advising-legal/references/business-structure-guide.md")
```

Walk the user through decision factors: revenue expectations, partners/co-founders, liability exposure, tax preferences.

**IP Protection Guidance:**

```
Read(file_path=".claude/skills/advising-legal/references/ip-protection-checklist.md")
```

Walk the user through IP protection considerations for software projects.

**Professional Referral Guidance:**

```
Read(file_path=".claude/skills/advising-legal/references/when-to-hire-professional.md")
```

When a user asks about finding or working with a business attorney, or when complexity indicators are triggered, load this reference to provide guidance on when to hire professional counsel versus self-help, how to find a qualified attorney, how to prepare for a consultation, and how to evaluate attorney fit.

## Step 5: Generate Recommendation Output

Based on user responses, generate the recommendation artifact.

In project-anchored mode, cite source context file references with line range for project-specific citations.

In standalone mode, produce general recommendations without project-specific context.

All output MUST automatically prepend the disclaimer header from the canonical disclaimer template before any substantive content.

---

## References

| Reference | Path | Purpose |
|-----------|------|---------|
| Business Structure Guide | `references/business-structure-guide.md` | Decision tree, entity descriptions, referral triggers |
| IP Protection Checklist | `references/ip-protection-checklist.md` | Software IP protection considerations |
| When to Hire a Professional | `references/when-to-hire-professional.md` | Complexity indicators, professional referral, self-help thresholds |
| Disclaimer Template | `references/disclaimer-template.md` | Canonical disclaimer template file for all output |

---

## Constraints

- This skill provides **educational only** guidance, never prescriptive legal advice
- All recommendations use "consider" language, never "you should" or "you must"
- Professional referral triggers halt the branch when complexity exceeds educational scope
- User profile access is strictly read-only with no mutation permitted
- Context files are read-only - this skill must never Write or Edit context files
- Disclaimer enforcement is non-negotiable - missing template means HALT
