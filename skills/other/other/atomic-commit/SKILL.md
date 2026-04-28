---
name: atomic-commit
description: Review staged + unstaged changes and split them into one commit per logical change. Use whenever the user says "atomic commit", "commit my changes", "split this into commits", or has multiple unrelated edits sitting in the working tree — even if they don't say "atomic". Runs repo-native type-checker and linter before each commit and refuses to bundle unrelated changes.
---
# Atomic Commit
Review staged + unstaged changes. Group by mechanism/file boundary.
Create one commit per logical change. Run repo-native type-checker and linter before each commit.
Do NOT bundle unrelated changes.
