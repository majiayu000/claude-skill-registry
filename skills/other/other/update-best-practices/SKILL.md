---
name: update-best-practices
description: "Fetch upstream Chromium documentation and merge guidelines into our best practices files. Detects new rules, conflicts, and outdated entries. Triggers on: update best practices, merge upstream best practices, sync best practices, fetch chromium guidelines."
argument-hint: <url1> [url2] [url3...]
---

# Update Best Practices from Upstream Docs

Fetch upstream Chromium documentation URLs, extract guidelines and rules, compare against our existing best practices, and merge new/corrected content. Detects inter-rule conflicts across all best practices files.

---

## The Job

When the user invokes `/update-best-practices <urls...>`:

1. **Parse URLs** from the arguments (space-separated or comma-separated)
2. **Read all existing best practices files** to understand current state
3. **Fetch each upstream URL** and extract all guidelines/rules
4. **Compare** upstream content against existing best practices
5. **Detect inter-rule conflicts** across all best practices files
6. **Update best practices files** with new rules, corrections, and upstream links
7. **Generate a summary report** of all changes

If no URLs are provided, use the known upstream reference URLs (see below).

---

## Known Upstream Reference URLs

These are authoritative Chromium documentation pages relevant to our best practices. Use these as defaults when no URLs are specified:

| URL | Maps To |
|-----|---------|
| https://www.chromium.org/developers/smart-pointer-guidelines/ | `coding-standards.md`, `architecture.md` |
| https://www.chromium.org/developers/design-documents/cookbook/ | `architecture.md` |
| https://www.chromium.org/chromium-os/developer-library/guides/testing/cpp-writing-tests/ | `testing-async.md`, `testing-isolation.md` |
| https://chromium.googlesource.com/chromium/src/+/HEAD/styleguide/c++/c++.md | `coding-standards.md` |
| https://chromium.googlesource.com/chromium/src/+/HEAD/base/containers/README.md | `coding-standards.md` |

The user may also provide any other Chromium documentation URL.

---

## Step 1: Read All Existing Best Practices

Read every file in `docs/best-practices/` to build a complete picture of current rules:

```
docs/best-practices/architecture.md
docs/best-practices/coding-standards.md
docs/best-practices/testing-async.md
docs/best-practices/testing-isolation.md
docs/best-practices/testing-javascript.md
docs/best-practices/testing-navigation.md
docs/best-practices/frontend.md
docs/best-practices/chromium-src-overrides.md
docs/best-practices/build-system.md
```

Also read `BEST-PRACTICES.md` (the index file).

For each file, catalog every rule by its heading/title so you can check for duplicates and conflicts.

---

## Step 2: Fetch Upstream Documentation

For each URL provided (or from the known list):

1. Use `WebFetch` to retrieve the page content
2. Extract every guideline, rule, convention, and recommendation
3. Include code examples where provided
4. Note the source URL for each extracted rule

**Be thorough** - extract ALL rules from each document, not just the ones that seem relevant at first glance.

---

## Step 3: Compare and Categorize

For each upstream rule, classify it:

### A. Already Covered (No Action)
The rule is already present in our best practices with correct and complete information.

### B. Partially Covered (Update)
We have a related rule but it's incomplete, less detailed, or missing important nuances from upstream. Update the existing section.

### C. Conflicts with Existing Rule (Fix)
The upstream documentation directly contradicts something in our best practices. This is the highest priority to fix.

### D. New Rule (Add)
The upstream rule covers something we don't have at all. Add it to the appropriate best practices file.

### E. Not Applicable (Skip)
The rule is about Chromium-internal processes that don't apply to Brave's workflow.

---

## Step 4: Detect Inter-Rule Conflicts

Scan ALL best practices files for internal contradictions. Common conflict patterns:

- One file says "always do X", another says "never do X"
- A rule in `architecture.md` contradicts a rule in `coding-standards.md`
- A "banned" item in one file is described as "use carefully" in another
- Testing guidance that contradicts coding standards

**Pay special attention to:**
- Smart pointer usage rules (unique_ptr, shared_ptr, scoped_refptr, raw_ptr, WeakPtr)
- Thread safety and callback patterns (Unretained, WeakPtr, PostTask)
- Feature flag guidance (when to guard, where to check)
- Ownership and lifetime rules
- Layering and dependency rules

---

## Step 5: Apply Changes

### For Conflicts (Category C - highest priority)
- Fix the incorrect rule to match upstream
- Add a link to the authoritative upstream document
- If both rules have merit, reconcile them into a single consistent rule

### For Partial Coverage (Category B)
- Enhance the existing section with missing details
- Add code examples from upstream where helpful
- Add link to upstream doc for more detail

### For New Rules (Category D)
- Add to the most appropriate best practices file based on topic:
  - Architecture/layering/services/factories -> `architecture.md`
  - C++ style/naming/memory/APIs -> `coding-standards.md`
  - Async testing/synchronization -> `testing-async.md`
  - Test isolation/mocking/patterns -> `testing-isolation.md`
  - JavaScript in tests -> `testing-javascript.md`
  - Navigation/timing in tests -> `testing-navigation.md`
  - Build system/GN/deps -> `build-system.md`
  - chromium_src overrides -> `chromium-src-overrides.md`
- Follow the existing format: `## <emoji> <Title>` with BAD/GOOD code examples
- Keep entries concise - link to upstream for full details

### For Inter-Rule Conflicts
- Fix the incorrect rule
- Add a cross-reference comment if the rules are related but address different aspects

---

## Step 6: Update BEST-PRACTICES.md

If new upstream reference URLs were processed, add them to the References section in `BEST-PRACTICES.md`.

---

## Step 7: Generate Summary Report

Output a summary to the user with:

```markdown
# Best Practices Update Summary

## Upstream URLs Processed
- <url1> - <number of rules extracted>
- <url2> - <number of rules extracted>

## Changes Made

### Conflicts Fixed
- **<file>: <rule title>** - <what was wrong> -> <what it says now>

### Rules Updated (Partial Coverage)
- **<file>: <rule title>** - <what was added/changed>

### New Rules Added
- **<file>: <rule title>** - <brief description>

### Inter-Rule Conflicts Found and Fixed
- **<file1> vs <file2>**: <description of conflict> -> <resolution>

## Already Covered (No Changes Needed)
- <list of upstream rules that were already correctly documented>

## Skipped (Not Applicable)
- <list of upstream rules that don't apply to Brave>
```

---

## Important

- **Upstream docs are authoritative** - when our docs conflict with Chromium docs, fix ours (unless it's a deliberate Brave-specific deviation, which should be documented as such)
- **Keep entries concise** - link to upstream for full details rather than duplicating everything
- **Preserve existing format** - match the `## <emoji> <Title>` heading style with BAD/GOOD examples
- **Don't remove Brave-specific rules** - rules about Brave patterns (e.g., `Brave*` prefix convention) have no upstream equivalent and should be kept
- **Do NOT include Co-Authored-By attribution in commits**
- **Check for inter-rule conflicts** even if the user only asks about a specific URL
