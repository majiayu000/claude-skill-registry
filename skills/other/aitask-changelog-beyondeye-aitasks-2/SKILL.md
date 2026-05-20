---
name: aitask-changelog
description: Generate a changelog entry by analyzing commits and archived plans since the last release.
---

## Workflow

### Step 1: Gather Release Data

Run the changelog data gathering script:

```bash
./.aitask-scripts/aitask_changelog.sh --gather
```

Parse the output to identify:
- The base tag (last release) from the `BASE_TAG:` line
- Each task section (`=== TASK tNN ===` to `=== END ===`) containing:
  - `ISSUE_TYPE:` — task type (feature, bug, refactor, documentation, performance, style, test, chore)
  - `TITLE:` — human-readable task name
  - `PLAN_FILE:` — path to the archived plan file (may be empty)
  - `COMMITS:` — source code commits for this task
  - `NOTES:` — "Final Implementation Notes" from the plan

If no task IDs are found (output contains `COMMITS_ONLY:`), inform the user:
"No task-tagged commits found since the last release. Only raw commits exist."

Use `AskUserQuestion`:
- Question: "No task-tagged commits found. How would you like to proceed?"
- Header: "No tasks"
- Options:
  - "Create manual entry" (description: "Write a changelog entry based on raw commit messages")
  - "Abort" (description: "Exit without creating a changelog entry")

If "Abort": End workflow.
If "Create manual entry": Use the raw commits to draft a changelog entry, then proceed to Step 4.

### Step 2: Load and Summarize Plans

For each task found in Step 1:
- If a plan file path was provided and is non-empty, read it to get the full context
- Generate a concise 1-2 sentence **user-facing** summary for each task
- Focus on **what changed from the user's perspective**, not internal implementation details
- Avoid mentioning file paths, function names, or internal architecture
- Use active voice (e.g., "Added support for..." not "Support was added for...")

Group the summaries by `ISSUE_TYPE`:
- `feature` entries under `### Features`
- `bug` entries under `### Bug Fixes`
- `refactor` entries under `### Improvements`
- `documentation` entries under `### Documentation`
- `performance` entries under `### Performance`
- `style` entries under `### Style Changes`
- `test` entries under `### Tests`
- `chore` entries under `### Maintenance`

Only include section headers that have entries.

### Step 3: Draft Changelog Entry

Compose the changelog entry in this format (only include sections that have entries):

```markdown
## vX.Y.Z

### Features

- **<Human-readable task name>** (tNN): <1-2 sentence summary>

### Bug Fixes

- **<Human-readable task name>** (tNN): <1-2 sentence summary>

### Improvements

- **<Human-readable task name>** (tNN): <1-2 sentence summary>

### Documentation

- **<Human-readable task name>** (tNN): <1-2 sentence summary>

### Performance

- **<Human-readable task name>** (tNN): <1-2 sentence summary>

### Style Changes

- **<Human-readable task name>** (tNN): <1-2 sentence summary>

### Tests

- **<Human-readable task name>** (tNN): <1-2 sentence summary>

### Maintenance

- **<Human-readable task name>** (tNN): <1-2 sentence summary>
```

Present the draft to the user for review before proceeding.

### Step 4: Ask for Version Number

Read the current version:

```bash
cat VERSION
```

Also check the topmost version in CHANGELOG.md (if it exists):

```bash
grep -m1 '^## v' CHANGELOG.md 2>/dev/null || echo "none"
```

Calculate suggested versions based on the current VERSION file:
- Parse current version as MAJOR.MINOR.PATCH
- Next patch: MAJOR.MINOR.(PATCH+1)
- Next minor: MAJOR.(MINOR+1).0

Use `AskUserQuestion`:
- Question: "What version number should this release be? (Current VERSION: <current>, Latest in CHANGELOG: <latest_or_none>)"
- Header: "Version"
- Options:
  - "Next patch: <patch>" (description: "Increment patch version")
  - "Next minor: <minor>" (description: "Increment minor version")
  - "Enter custom version" (description: "Specify a different version number")

If "Enter custom version": Ask the user to type their desired version via `AskUserQuestion` free text ("Other" option).

### Step 5a: Version Validation

After the user enters a version number, validate it:

- Parse the topmost `## vX.Y.Z` heading in CHANGELOG.md to find the latest documented version
- If CHANGELOG.md doesn't exist or has no version headings, skip validation (any version is valid)
- Compare: the new version must be **strictly greater** than the latest documented version using semver ordering (compare MAJOR, then MINOR, then PATCH)
- If the new version is the same or lower than the latest documented version:
  - Inform the user: "Version vX.Y.Z is not greater than the latest changelog version vA.B.C."
  - Loop back to Step 4 to ask for a different version number

### Step 5b: Overlap Detection

After version validation, check the **topmost (latest) section** in CHANGELOG.md for task overlap:

- If CHANGELOG.md doesn't exist, skip this step (no overlap possible)
- Extract the topmost section content (from the first `## v` heading to the next `## v` heading or EOF)
- Scan the section for task ID references matching `(tNN)` or `(tNN_MM)` patterns
- Compare these task IDs with the task IDs gathered in Step 1
- Classify each gathered task as: **already in changelog** or **new (not yet in changelog)**

If **any overlap** is detected (at least one gathered task ID appears in the latest section):

Use `AskUserQuestion`:
- Question: "The latest changelog section already mentions N of M gathered tasks. How to proceed?"
- Header: "Overlap"
- Options:
  - "New tasks only" (description: "Create a new version section with only the tasks not already mentioned in the changelog")
  - "Replace latest section" (description: "Remove the latest changelog section and replace with a complete new summary for the new version")
  - "Abort" (description: "Stop and manually edit CHANGELOG.md to resolve the overlap")

If "New tasks only":
  - Filter the draft to include only tasks NOT found in the latest section
  - If no new tasks remain, inform the user and abort
  - Proceed to Step 6 with the filtered draft, inserting above the existing latest section

If "Replace latest section":
  - Show the existing section content as reference for the user
  - Generate a complete new summary with ALL gathered tasks
  - In Step 6, remove the old topmost section and insert the new one in its place

If "Abort": End workflow, inform user to manually edit CHANGELOG.md.

If **no overlap** (latest section has no overlapping task IDs, or no CHANGELOG.md exists), proceed normally.

### Step 6: Review and Finalize

Show the complete formatted changelog entry (including the `## vX.Y.Z` header).

Use `AskUserQuestion`:
- Question: "Review the changelog entry for vX.Y.Z. How would you like to proceed?"
- Header: "Review"
- Options:
  - "Write to CHANGELOG.md" (description: "Save the entry as-is")
  - "Edit entry" (description: "Make changes before saving")
  - "Abort" (description: "Discard without saving")

If "Edit entry": Ask the user what to change, make the edits, and loop back to the review question.
If "Abort": End workflow.

### Step 7: Write CHANGELOG.md

**If CHANGELOG.md exists:**
- Read the current content
- If "Replace latest section" was chosen in Step 5b:
  - Find the first `## v` heading and the second `## v` heading (or EOF)
  - Replace that range with the new version section
- Otherwise:
  - Insert the new version section after the first line (the `# Changelog` header)
  - Add a blank line between the header and the new section

**If CHANGELOG.md does not exist:**
- Create it with:
```markdown
# Changelog

## vX.Y.Z

### Features
...
```

### Step 7b: Generate Humanized Changelog Entry

After writing CHANGELOG.md, generate an **informal, blog-style** version of the same changelog for `CHANGELOG_HUMANIZED.md`. This content is used automatically by `website/new_release_post.sh` to create release blog posts.

**Writing guidelines:**
- Write in an informal, conversational tone — as if explaining to a developer friend
- Highlight the **3-5 most notable features** (not every change)
- Each feature gets a `## Heading` and 2-3 sentences explaining **what it means for the user**
- Start with a brief intro paragraph (e.g., "v0.6.0 is out, and it's packed with new features.")
- Do NOT list every bug fix or minor improvement — those are in the full changelog
- Do NOT mention internal file paths, function names, or architecture details
- Use second person ("you") and active voice
- End with a horizontal rule (this will be used as a separator in the blog post)

**Format:**

```markdown
## vX.Y.Z

<Intro paragraph — 1-2 sentences setting the tone>

## <Feature 1 Name>

<2-3 sentences explaining the feature from the user's perspective>

## <Feature 2 Name>

<2-3 sentences explaining the feature from the user's perspective>

## <Feature 3 Name>

<2-3 sentences explaining the feature from the user's perspective>

---
```

Present the humanized draft to the user for review.

Use `AskUserQuestion`:
- Question: "Review the humanized changelog entry for the release blog post. How would you like to proceed?"
- Header: "Blog"
- Options:
  - "Write to CHANGELOG_HUMANIZED.md" (description: "Save the blog-style entry")
  - "Edit entry" (description: "Make changes before saving")
  - "Skip" (description: "Don't create a humanized entry for this release")

If "Edit entry": Ask what to change, make edits, and loop back to the review question.
If "Skip": Proceed to Step 8 without writing CHANGELOG_HUMANIZED.md.

### Step 7c: Write CHANGELOG_HUMANIZED.md

**If CHANGELOG_HUMANIZED.md exists:**
- Read the current content
- Insert the new version section after the first line (the `# Releases` header)
- Add a blank line between the header and the new section

**If CHANGELOG_HUMANIZED.md does not exist:**
- Create it with:
```markdown
# Releases

## vX.Y.Z

<humanized content>
```

### Step 8: Commit

```bash
git add CHANGELOG.md CHANGELOG_HUMANIZED.md
git commit -m "ait: Add changelog entry for vX.Y.Z"
```

Inform the user: "Changelog entry for vX.Y.Z written to CHANGELOG.md and CHANGELOG_HUMANIZED.md. Run `./create_new_release.sh` when ready to create the release."

### Step 9: Satisfaction Feedback

Execute the **Satisfaction Feedback Procedure** (see `.claude/skills/task-workflow/satisfaction-feedback.md`) with `skill_name` = `"changelog"`.

## Notes

- This skill uses `.aitask-scripts/aitask_changelog.sh` for data gathering (tag detection, commit parsing, plan resolution)
- The script detects task IDs from parenthesized `(tNN)` patterns in commit messages (source code commits only)
- Child task IDs like `(t85_10)` are also detected and resolved
- Plan files are resolved from `aiplans/archived/` using the `pNN_name.md` naming convention
- If a plan file is not found for a task, commit messages serve as the summary source
- The `--check-version` mode of the script is used by `create_new_release.sh` to verify changelog completeness before release
