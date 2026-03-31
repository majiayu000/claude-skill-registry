---
name: update-changelog
description: "Update the Unreleased section of CHANGELOG.md based on current changes. No-op if CHANGELOG.md does not exist. Use when the user asks to \"update changelog\", \"add to changelog\", \"update the changelog\", \"changelog entry\", \"add changelog entry\", or \"log this change\"."
---

# Update Changelog

Update the Unreleased section of the changelog based on the current changes.

## Step 1: Run `/changelog-rules` Skill

Run `/changelog-rules` to load shared changelog conventions.

## Step 2: Check for Changelog

Use `git rev-parse --show-toplevel` to find the repository root. Look for the changelog file per `/changelog-rules`. If it does not exist, skip this skill. Do not create it.

## Step 3: Analyze the Changes

Determine what changed:

- Read `git diff --cached` for staged changes
- If nothing is staged, read `git diff` for unstaged changes
- Use the conversation context for the intent behind the changes

## Step 4: Assess Changelog-Worthiness

Apply the `/changelog-rules` changelog-worthiness criteria. Also skip fixes to code introduced by the same branch/PR, as these are refinements of the in-progress feature, not separate changelog events.

If no changes are changelog-worthy, skip this skill.

## Step 5: Check Existing Unreleased Entries

Read the current Unreleased section of the changelog. Look for entries that relate to the same feature or fix. This prevents duplicates across multiple commits for the same body of work.

- If an existing entry covers the same change, update its wording only if the current commit meaningfully extends or refines the feature. Do not add a duplicate entry.

## Step 6: Update the Unreleased Section

Add or update entries in the Unreleased section following `/changelog-rules` conventions. Create subsection headers as needed (e.g., `### Added`).

## Rules

- Never modify released version sections. Only the Unreleased section is in scope.
- Do not stage the modified file. The caller is responsible for staging.
