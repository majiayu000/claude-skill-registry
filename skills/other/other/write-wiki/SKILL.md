---
name: write-wiki
description: >
  Create user documentation for the HMIS wiki following writing guidelines. Use when
  creating documentation for end users (pharmacy staff, nurses, doctors, administrators).
  Creates documentation directly in the sibling ../hmis.wiki directory.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, Bash
argument-hint: "[module/Feature-Name]"
---

# Write Wiki Documentation

Create end-user documentation directly in the sibling `../hmis.wiki` directory following the project's wiki writing guidelines.

**IMPORTANT**: Wiki files live ONLY in the sibling `../hmis.wiki` directory. Do NOT create wiki markdown files inside the main project repository - this causes git submodule issues.

## Arguments

- `$0` - Module and feature name (e.g., `Pharmacy/Stock-Transfer`)

## Target Audience

- Pharmacy staff, nurses, doctors, administrators
- Non-technical healthcare professionals
- Focus on **how to use features**, not implementation details

## Required Structure

Every wiki page must include these sections:

1. **Overview** - What the feature does and why (2-3 sentences)
2. **When to Use** - Specific scenarios and business triggers
3. **How to Use** - Step-by-step with navigation paths
4. **Understanding Messages** - Success, warning, and error messages
5. **Best Practices** - Tips for effective use
6. **Troubleshooting** - Common problems and solutions
7. **Configuration (Admin)** - Settings that affect the feature
8. **FAQ** - Common questions

## Writing Rules

- **Active voice**: "Click the Submit button" (not "The button should be clicked")
- **Imperative mood**: "Enter the patient ID"
- **Bold UI elements**: **Pharmacy** > **Reports** > **Stock Ledger**
- **One action per step** in numbered procedures
- **No code, no technical details** - no Java classes, SQL, file paths, or method names

## What NOT to Include

- Code snippets, file paths, line numbers
- Java class names, method signatures
- Database schema or SQL queries
- JSF component IDs or backend beans
- Developer debugging information

## File Location

Create files at: `../hmis.wiki/$0.md`

Ensure the wiki repo exists first:
```bash
test -d "../hmis.wiki" || (cd .. && git clone https://github.com/hmislk/hmis.wiki.git && cd hmis)
```

After creating, suggest using `/publish-wiki` to commit and push to the GitHub Wiki.
