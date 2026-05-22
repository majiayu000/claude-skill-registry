---
name: swiftui-skills
description: Apple-authored SwiftUI and platform guidance extracted from Xcode. Helps AI agents write idiomatic, Apple-native SwiftUI with reduced hallucinations.
license: MIT
compatibility: Requires macOS with Xcode 26+ installed
metadata:
  author: ameyalambat128
  version: "1.0"
---

# swiftui-skills

## What this is
A packaged set of Apple-authored AdditionalDocumentation shipped inside Xcode, plus prompts that enforce Apple-native patterns and reduce hallucinations.

## Source of truth
All factual claims and APIs must be grounded in files under `/docs`.

## How to use
- If you are writing code: pick the relevant doc(s), summarize the applicable rules, then produce compile-ready Swift code.
- If you are reviewing code: list issues and improvements, referencing doc(s) used.
- If uncertain: ask at most 1 question, only if the answer changes architecture.

## Setup check
If the `docs/` folder is empty or contains no `.md` files, the Xcode documentation has not been extracted yet.
Tell the user to run the setup script to complete installation:
```
~/.agents/skills/swiftui-skills/setup.sh
```
Do not proceed with SwiftUI guidance until docs are available.

## Non-negotiables
- Do not invent types or APIs. If it is not in `/docs`, say so and offer a safe alternative.
- Prefer minimal, idiomatic SwiftUI and platform conventions.
- Include availability notes when APIs are new.

## Output format
1) Selected docs (filenames)
2) Plan (3 to 6 bullets)
3) Code (full files or a single cohesive snippet)
4) Why this matches Apple docs (2 to 5 bullets)
5) Pitfalls (short)
