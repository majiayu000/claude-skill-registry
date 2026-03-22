---
version: 1.1.0
name: meta-adopt-skill
description: >
  Review and adopt an external skill into this workflow. Evaluates a skill
  from a URL, marketplace, or local path for compatibility, overlap, quality,
  and fit within the existing skill catalog. Use when the user wants to add
  a new skill, says "adopt skill", "install skill", "add this skill",
  "evaluate this skill", or invokes /meta-adopt-skill.
  Does NOT trigger automatically.
disable-model-invocation: true
argument-hint: "[skill-source: URL, marketplace ref, or local path]"
---

# Adopt Skill — Review & Integration Process

Evaluate an external skill before integrating it into this workflow.
Never auto-adopt — always present findings and get user approval.

## Step 1: Fetch & Read the Skill

1. Retrieve the skill from the provided source:
   - **GitHub URL**: Fetch the SKILL.md and any supporting files
   - **Marketplace**: Use `/plugin` to inspect before installing
   - **Local path**: Read the SKILL.md and directory contents
2. Read the complete SKILL.md content and all supporting files
3. Extract metadata: name, description, allowed-tools, context, dependencies

## Step 2: Security Audit

4. **Check for red flags:**
   - Does it run arbitrary bash commands? What commands specifically?
   - Does it reference external URLs or APIs? Which ones?
   - Does it use `allowed-tools` that grant broad access?
   - Does it include scripts? Read them — do they do what they claim?
   - Does it instruct Claude to send data externally?
5. **Rate security risk:** Low / Medium / High
6. If High risk, **stop and warn the user** before proceeding

## Step 3: Overlap Analysis

7. Read the skill catalog: `.claude/skills/meta-skill-catalog/catalog.json`
8. For each existing skill, compare:
   - **Trigger overlap**: Would both skills activate for similar prompts?
   - **Functional overlap**: Do they do similar things?
   - **Naming conflict**: Does the name collide with an existing skill?
9. Report findings:
   - "No overlap found" OR
   - "Overlaps with [skill-name]: [description of overlap]"
   - Recommend: adopt as-is, merge with existing, or skip

## Step 4: Compatibility Check

10. Evaluate fit within this workflow:
    - **Naming convention**: Does it follow `{category}-{function}` pattern?
      If not, suggest a rename.
    - **Category assignment**: Which category does it belong to?
      (`meta-*`, `dev-*`, `ops-*`, `tool-*`, `viz-*`, or new category)
    - **Context files**: Does it need to read/write any context files?
      Does it respect the memory security rules (MEMORY.md main-session only)?
    - **Quality**: Is the SKILL.md well-structured? Are instructions clear?
    - **Size**: Is it under 500 lines? If not, should supporting files be split out?

## Step 5: Adaptation Plan

11. Draft a plan for integration:
    - Proposed name (following naming convention)
    - Proposed category
    - Changes needed to make it fit:
      - Frontmatter adjustments (name, description, invocation control)
      - Instruction modifications for workflow compatibility
      - Supporting files to keep, modify, or remove
    - Any dependencies to install (MCP servers, CLI tools, packages)
12. If the skill needs modifications, show the diff between original and adapted version

## Step 6: Present Review

13. Present a structured review to the user:

```
### Skill Adoption Review: {skill-name}

**Source:** {URL or path}
**Security Risk:** {Low/Medium/High}
**Overlap:** {None / overlaps with X}
**Category:** {proposed category}
**Proposed Name:** {category-function}

#### What It Does
{One paragraph summary}

#### Changes Needed
- {List of modifications}

#### Recommendation
{Adopt as-is / Adopt with changes / Merge with [existing] / Skip}
```

14. Wait for user approval before proceeding

## Step 7: Install (After Approval)

15. If approved:
    - Copy/create the skill directory: `.claude/skills/{category-function}/`
    - Write the adapted SKILL.md (with any agreed modifications)
    - Copy supporting files
    - Update the skill catalog: `.claude/skills/meta-skill-catalog/catalog.json`
    - Set version tracking in catalog entry:
      - `version`: read from the adopted skill's SKILL.md frontmatter (or `1.0.0` if not present)
      - `installed_from`: `"local"` (adopted skills are local additions)
      - `installed_version`: same as `version`
      - `installed_date`: today's date
    - Update today's daily memory with the adoption decision
16. Verify the skill is discoverable: "What skills are available?"
17. If the skill has a test case, run it to verify it works

## Adoption Checklist

Before marking adoption complete, verify:
- [ ] SKILL.md has proper frontmatter (name, description)
- [ ] Name follows `{category}-{function}` convention
- [ ] No security red flags unaddressed
- [ ] No unresolved overlap with existing skills
- [ ] Catalog updated
- [ ] Supporting files in place
- [ ] Skill loads when invoked
