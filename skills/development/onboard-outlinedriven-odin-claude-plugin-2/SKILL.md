---
name: onboard
description: 'Use when the user asks for onboarding, orientation, a repository tour, or where to start. Produces an evidence-backed seven-section map, deep-reads real files, and asks for the next move.'
---

# Onboard

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user invites onboarding, orientation, a tour, or guidance on where to start in a repository. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Return an in-chat repository orientation and next-move question; make no repository changes. |
| Done | Return the applicable seven sections in order, grounded in observed evidence; deep-read two or three real files when available; and ask the user to choose the next move. |

## Inputs

- Repository root, defaulting to the current working directory. It must resolve to an existing directory.
- Depth: `quick`, `normal`, or `deep`; default `normal`. Depth changes collection breadth, not the output sections.
- Optional focus: an area, feature, language, package, or entry point. It constrains the deep read and follow-up guidance, not the initial repository map.

## Procedure

1. Resolve the repository root, validate that it is an existing directory, normalize the depth, and record any focus. Stop with an input failure if the root or depth is invalid. Done when: the root is validated, depth is normalized, and focus is recorded or rejected.
2. Collect bounded evidence before explaining the repository:
   - Parse present root and workspace manifests to identify packages, languages, scripts, binaries, and build configuration.
   - Walk directories to a maximum depth of three, excluding generated, dependency, cache, coverage, and version-control directories.
   - Read the repository README and any local contributor or execution instructions, following a one-line Markdown redirect when present.
   - Inspect present CI workflows, container files, service composition, process declarations, and root deployment manifests.
   - When the root is a Git worktree, read its branch, origin, latest commit, shallow status, commit count, recent contributors, and files changed during the last 180 days. Treat absence of Git metadata as a degradation, not a failure.
   - Locate entry points, exported surfaces, tests, and call or import flow with available structural code search. If structural search is unavailable, use language-specific text search over source and manifests. Do not infer architecture from filenames alone.
   - If a read-only whole-repository digest facility is available, use it only to corroborate stack, module boundaries, and naming conventions. Its absence or failure does not block the orientation.
   Done when: bounded evidence collection is attempted across all applicable classes.
3. Synthesize a concise orientation using these sections in this exact order:
   1. **What it does**: one or two plain-language sentences supported by the README and manifests.
   2. **Tech stack + CI**: observed languages, frameworks, package managers, build and test tools, and CI jobs.
   3. **Where execution starts**: observed binaries and CLIs, application or server bootstrap, framework-loaded configuration, library exports, and test or benchmark entry points, grouped by kind.
   4. **Project structure, annotated**: important directories, their evidenced purpose, and unusual layout details; do not paste an exhaustive tree.
   5. **Active development: hotspots + owners**: recent high-churn files and contributors when Git evidence exists.
   6. **Code health**: only evidenced drift, debris, or test gaps, graded `HIGH` for direct tool evidence, `MEDIUM` for repeated independent signals, or `LOW` for an explicitly marked inference.
   7. **Getting started: exact runnable commands**: commands copied from manifests, CI, build files, or the README. Omit rather than invent an ungrounded command.
   Done when: all seven sections are synthesized in order with evidence grounding.
4. Attempt every applicable collection class. If evidence for a section is unavailable, state the reason once in that section rather than fabricating content or repeating the limitation. Done when: every section either has evidence or states its degradation once.
5. Deep-read two or three real files after forming the map: the primary structural entry point, a central file in the largest observed module, and one representative test, in that order. If fewer exist, read every available category and state the degradation. Connect the files through observed imports, calls, exports, or test targets; label any remaining inference `[INFERENCE]`. Done when: two or three real files are deep-read with connections and inference labels.
6. End by asking the user to select exactly one next move, marking **Explore an area** as recommended for first-time onboarding:
   - Explore an area: choose a directory or package and inspect its central exports and most-connected implementation file.
   - Trace a feature: request the feature name, locate its entry point, trace its call or import flow, and identify two or three key files.
   - Make a first change: request the desired change, map risk from hotspots, ownership, and tests, and identify files to inspect before editing.
   - Where can I help?: derive file-level opportunities from hotspots, test gaps, stale documentation, low-ownership areas, and bounded cleanup candidates.
   Use an available single-select interaction; otherwise present the four numbered options and stop after the question. Done when: the next-move question is presented with Explore an area marked as recommended.

## Failure and recovery

- Invalid input: If the root does not exist or depth is outside the closed set, return the rejected value and required correction; do not inspect a substitute path.
- Unreadable or missing evidence: Continue with independently available evidence, identify the affected section once, and lower certainty. A manifest, README, Git metadata, CI configuration, structural index, or digest may be absent without invalidating observed results.
- Insufficient source: If no real source file can be read, return the seven-section partial orientation but classify the result as blocked because the deep-read predicate is unmet. If only one or two qualifying files exist, read them and report that exact degradation.
- Conflicting evidence: Present the conflict with file paths or metadata sources and do not choose a claim without support.
- Partial-result rule: Preserve useful observed findings, clearly separate unavailable evidence and `[INFERENCE]`, and never claim the done predicate when a blocking gate failed.
- Recovery: Retry only with a narrower read or an available read-only search method. Never recover by widening beyond the repository root, mutating state, running paid operations, or inventing evidence.

## Output

In-chat orientation with the seven ordered sections, certainty labels where needed, a two-or-three-file source deep read with concrete paths and relationships, explicit degradations, and a single-select next-move question. Terminal classification: `complete` only when the root is valid, core evidence collection was attempted, at least one real source file was read, commands are grounded, and the next-move question is present; otherwise `blocked` with the unmet predicate and the useful partial orientation.
