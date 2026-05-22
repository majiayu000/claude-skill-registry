---
name: flutter-code-review
description: Review Flutter app PRs for bugs, UX issues, performance regressions, missing tests, and readability; include app code, packages/plugins, and CI config. Use when asked to review a Flutter PR, do a Flutter code review, or find bugs in Flutter repositories.
---

# Flutter Code Review

## Overview

Provide structured PR reviews for Flutter apps with prioritized findings. Focus on bugs first, then UX, performance, tests, and readability, and report issues as bullet points with file/line references.

## Workflow

1. Identify scope: review the diff and list touched files (Flutter app code, package/plugin code, CI files).
2. Bugs/regressions: check state management, async flows, widget lifecycle, null safety, error handling, navigation, permissions, and data persistence.
3. UX issues: verify loading/empty/error states, accessibility, layout on small screens, and gesture conflicts.
4. Performance: watch for rebuild hotspots, unnecessary `setState`, large lists without virtualization, expensive work on UI thread, and image caching.
5. Tests: ensure new logic is covered; suggest or run `flutter test` and `flutter analyze` as appropriate.
6. Report findings ordered by severity with short rationales and precise file/line references.

## Output Format

Use bullets only:

- Findings first, ordered by severity, each with `path:line` and a brief rationale.
- Then questions/assumptions if clarification is needed.
- Then a short change summary if helpful.

Example bullet:
- `lib/screens/home_screen.dart:120` Potential NPE when `currentSong` is null; guard before accessing fields.
