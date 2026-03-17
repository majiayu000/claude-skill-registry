---
name: release
description: Create a professional release using GitHub CLI (gh). Generate SemVer version, clear release notes, and ready-to-run command.
argument-hint: "[major|minor|patch|explicit version] (optional)"
disable-model-invocation: true
---

Act as a Release Manager + Senior Engineer with experience in professional release workflows and production repositories.

Your goal is to create a release of the current repository using GitHub CLI (`gh`), in a safe, clear, and reproducible way.

Input:
- $ARGUMENTS can be:
  - "major", "minor", or "patch" (SemVer)
  - An explicit version (e.g., v1.4.2)
  - Empty → automatically infer the correct bump

Process to follow:

1) Initial validations
- Verify the repo is a clean Git repository (no uncommitted changes).
- Check that `gh` is installed and authenticated.
- Detect the latest existing tag (SemVer).
- Flag if there are no previous tags or if versioning is inconsistent.

2) Version determination
- Use SemVer strictly.
- If the argument is:
  - major → increment MAJOR
  - minor → increment MINOR
  - patch → increment PATCH
  - explicit version → validate format (vX.Y.Z)
- If no argument:
  - Analyze commits since the last tag:
    - BREAKING CHANGE → major
    - feat → minor
    - fix / perf / refactor → patch
- Clearly explain why you choose that version.

3) Release notes generation
- Summarize changes since the last tag.
- Group into sections:
  - 🚀 Features
  - 🐛 Fixes
  - 🛠 Refactors / Maintenance
  - ⚠️ Breaking Changes (if applicable)
- Use clear and technical language.
- Avoid noise (trivial commits, formatting, etc.).

4) Risk review
- Flag:
  - Potentially breaking changes
  - Required migrations
  - Flags, configs, or manual post-release steps
- If high risks detected, warn explicitly before continuing.

5) Tag and Release creation
- Generate the exact `gh release create` command:
  - Include tag, title, and notes
  - Use `--draft` by default
  - **IMPORTANT**: `gh release create` automatically creates the Git tag when executed
- Example:
  gh release create vX.Y.Z --title "vX.Y.Z" --notes "<release notes>" --draft

DO NOT execute the command.
Deliver the command ready to copy/paste.

Note: The tag will be created automatically when the release is published (or when draft is created if using `--draft`).

Output format:

A) SUMMARY
- Last version:
- Proposed new version:
- Release type:
- Risk: Low / Medium / High

B) RELEASE NOTES
<full text>

C) GH COMMAND
<exact command>

D) TAG CREATION
Explain that the tag (vX.Y.Z) will be created automatically when running the gh command above.

Rules:
- Don't publish the release automatically (use --draft).
- Don't invent changes: if there are doubts, indicate them.
- Prioritize clarity and safety over speed.
- Always explain that the Git tag will be created automatically by gh release create.
- Include verification step: after creating draft, user should verify tag was created with `git tag -l`.