---
name: oss-write-docs
description: |
  Contribute documentation improvements to an OSS repo. Identifies doc gaps,
  studies the docs system, and verifies accuracy against source code. Use when
  contributing documentation to an open source project, fixing outdated setup
  instructions, adding missing API docs, or improving README clarity. Not for
  writing docs for your own project — this is for contributing docs to someone
  else's repo.
---

# Write Docs

Contribute documentation that a maintainer would write — accurate, audience-aware, and verified against the actual code. Docs contributions have different mechanics than code PRs: you need to understand who reads the docs, verify every claim against source code, and test every example.

## Purpose

Documentation contributions are undervalued by contributors and overvalued by maintainers. Most contributors skip docs because they don't feel like "real" contributions. But outdated docs cause more user frustration than most bugs, and maintainers rarely have time to keep docs current. This skill guides you through finding real documentation gaps, verifying accuracy against the code, and writing docs that match the repo's voice and style.

## When to Use

- You've found outdated setup instructions (you followed them and they didn't work)
- Public API methods or functions lack documentation
- README assumes knowledge that new users don't have
- Code examples in docs don't run or produce wrong output
- Error messages reference docs that don't exist
- **NOT** for writing docs for your own project
- **NOT** for adding inline code comments — that's part of code contributions
- **NOT** when the repo has no docs infrastructure at all — discuss with maintainers first

## Prerequisites

- Repo forked, cloned, and set up (from `oss-prep-to-contribute`)
- You've actually tried to USE the docs and found problems (not just skimming)
- Understanding of the area you're documenting (or willingness to build it)

## Process

### 1. Identify documentation gaps

The best doc contributions come from actually using the docs and finding where they fail.

```bash
# Find docs files
find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" | head -30
ls docs/ doc/ documentation/ wiki/ 2>/dev/null

# Check for docs framework
ls docusaurus.config.* mkdocs.yml conf.py book.toml .readthedocs.yml 2>/dev/null

# Find broken links in docs
grep -rn '\[.*\](.*\.md)' docs/ README.md | while read line; do
  file=$(echo "$line" | sed -n 's/.*(\([^)]*\.md\)).*/\1/p')
  [ -n "$file" ] && [ ! -f "$file" ] && echo "Broken link: $line"
done

# Find code examples and check if they reference current APIs
grep -rn '```' docs/ README.md --include="*.md" | head -20
```

**High-value doc gaps** (prioritize these):
- Setup instructions that don't work (you tried them)
- API methods with no docs but active usage in the codebase
- Examples that reference renamed or removed functions
- Config options documented nowhere
- Error messages that say "see docs" but the docs don't exist

**Low-value doc gaps** (skip these):
- Typos in low-traffic pages
- Style inconsistencies (unless extreme)
- Adding docs for internal/private APIs

### 2. Understand the docs system

Every repo has documentation conventions. Learn them before writing.

```bash
# Check how docs are built
cat package.json 2>/dev/null | grep -i "doc\|docs\|build.*doc"
cat Makefile 2>/dev/null | grep -i doc
cat pyproject.toml 2>/dev/null | grep -i doc

# Read the docs contribution guide (if separate from CONTRIBUTING.md)
cat docs/CONTRIBUTING.md docs/contributing.md 2>/dev/null

# Check the docs config
cat docusaurus.config.js mkdocs.yml conf.py 2>/dev/null | head -50
```

Document:
- **Docs framework**: Docusaurus, MkDocs, Sphinx, mdBook, rustdoc, JSDoc, plain markdown?
- **File structure**: how are docs organized? (by topic, by API, by tutorial?)
- **Build process**: how to preview locally?
- **Style guide**: formal or casual? second person ("you") or imperative? code-heavy or prose-heavy?
- **Versioning**: are docs versioned alongside releases?

### 3. Verify the gap by reading code

Every documentation claim must be traceable to actual code. Don't write docs from memory or assumption.

```bash
# If documenting a function, read its implementation
grep -rn "function functionName\|def functionName\|func functionName" src/ --include="*.ts" --include="*.py" --include="*.go"

# If documenting config options, find where they're read
grep -rn "config\.\|getenv\|process\.env\." src/ --include="*.ts" --include="*.py"

# If documenting CLI flags, find the argument parser
grep -rn "argparse\|commander\|clap\|flag\." src/ --include="*.py" --include="*.ts" --include="*.rs" --include="*.go"
```

For each claim you plan to write:
- Find the source code that implements the behavior
- Note the file and line number (for your own reference, not for the docs)
- Check if the behavior has changed since the last docs update

```bash
# When was this doc last updated vs when was the code last changed?
git log --oneline -5 -- "docs/path/to/page.md"
git log --oneline -5 -- "src/path/to/implementation.ts"
```

### 4. Thinking gate — user explains the audience

> "Before writing anything:
> 1. Who reads this documentation? (New users? API consumers? Contributors? Ops/deploy engineers?)
> 2. What do they already know when they arrive at this page?
> 3. What are they trying to accomplish? (Not 'learn about X' — what task are they doing?)
> 4. What's the single most important thing this page should communicate?"

Wait for their answer. If they say "everyone" or "developers in general," push back: "Look at the existing docs — who is the implicit audience? What level of knowledge do they assume?"

### 5. User writes the docs

The user drafts the documentation. The LLM helps with:
- Verifying claims against source code ("you wrote that this accepts 3 arguments, but the function signature shows 4")
- Checking code examples actually work
- Matching the repo's documentation voice and style
- Pointing to similar pages as format reference

**What the LLM DOES**:
- Fact-check every claim against the source code
- Test code examples mentally (or by running them if possible)
- Review for clarity — flag jargon the target audience wouldn't know
- Point to existing docs pages as style reference

**What the LLM DOES NOT DO**:
- Write the documentation for the user
- Add promotional language ("this amazing feature...")
- Expand scope beyond what the user identified

### 6. Test and verify

Before submitting, verify everything:

```bash
# Build docs locally
# {repo-specific docs build command — found in step 2}

# If the docs framework supports link checking
# {repo-specific link check command}
```

**Manual verification**:
- Click every link in your changes — both internal and external
- Run every code example and verify the output matches what you documented
- Read the page as if you're the target audience — does it answer their question?
- Check that your page is reachable from the navigation/sidebar (not an orphan)

```bash
# Verify code examples work
# Copy-paste each example and run it
```

### 7. Thinking gate — user reviews their own writing

> "Read your docs one more time and answer:
> 1. Can the target user accomplish their task using only what you wrote? (No unstated prerequisites?)
> 2. Is every code example copy-paste-runnable? (No missing imports, no assumed setup?)
> 3. Does anything you wrote contradict what the code actually does? (Check the source again)
> 4. If the function changes next release, which parts of your docs would break?"

This catches the most common doc bugs: assumed context, stale examples, and version-coupled language.

## Related Skills

- **Previous step**: ← `oss-prep-to-contribute` — set up the repo
- **Alternative entry**: ← `oss-find-real-issues` — if you found doc gaps while exploring
- **Next step**: → `oss-submit-pr` — submit the docs PR
- **If unfamiliar with the code**: → `oss-learn-stack` or `oss-explore-repo` — understand the feature before documenting it

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "I'll just fix the typos I found" | Typo-only PRs are low-signal. They're welcome, but they don't build trust or demonstrate understanding. Pair typo fixes with substantive improvements. |
| "I know how this feature works, I don't need to read the code" | You know how you THINK it works. Read the source. Every undocumented edge case, default value, and error condition is in the code, not in your head. |
| "I'll write comprehensive docs for everything" | Scope creep. Pick one page, make it excellent, and submit. A focused PR gets reviewed and merged faster than an omnibus docs overhaul. |
| "The code example probably works, I'll just write it" | Untested examples are the #1 source of docs bugs. Run it. If it doesn't run, your docs are already outdated on merge day. |
| "I'll match my preferred writing style" | This isn't your repo. Match the existing docs voice. If the repo uses "you" and imperative mood, don't switch to formal third person. |

## Red Flags

- User writes docs for features they haven't used — they'll document the API, not the experience
- Code examples are written from imagination, not tested — they'll break
- Docs describe what the code CAN do rather than what users SHOULD do — feature lists aren't documentation
- User wants to restructure the entire docs site — that's a conversation with maintainers, not a PR
- Every claim is hedged ("this should work", "this might return") — if you're not sure, read the code

## Verification Checklist

- [ ] Doc gap identified by actually using the docs (not just skimming)
- [ ] Docs system and conventions understood (step 2)
- [ ] Every claim verified against source code (step 3)
- [ ] Target audience explicitly identified (step 4)
- [ ] All code examples tested and working (step 6)
- [ ] All links verified (step 6)
- [ ] Docs build successfully (step 6)
- [ ] User reviewed their own writing for unstated prerequisites and stale coupling (step 7)

## Anti-patterns

- **DO NOT** write documentation without reading the source code — docs must be traceable to implementation
- **DO NOT** write code examples without testing them — untested examples are bugs
- **DO NOT** ignore the repo's documentation style — match voice, format, and structure exactly
- **DO NOT** document internal/private APIs — document what users interact with
- **DO NOT** submit docs PRs that restructure the docs site — keep scope to content, not architecture
