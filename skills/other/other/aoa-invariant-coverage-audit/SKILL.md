---
name: aoa-invariant-coverage-audit
scope: core
status: canonical
summary: Audit whether existing tests or checks actually cover the stable invariants that matter, and identify the smallest bounded gaps that still leave example-only coverage too thin.
invocation_mode: explicit-preferred
technique_dependencies:
  - AOA-T-0017
---

# aoa-invariant-coverage-audit

## Intent

Use invariant-oriented coverage to judge whether an existing validation surface really constrains the stable truth, instead of only repeating examples.

## Trigger boundary

Use this skill when:
- an existing test or check surface needs a review for invariant strength
- the question is whether current checks really constrain the stable rule
- you need to turn a loose example set into a bounded coverage audit

Do not use this skill when:
- the main problem is defining the invariant itself rather than auditing coverage; use `aoa-property-invariants` first
- the invariant itself is still unknown and you need discovery work first
- the task is mostly about presentation details or a narrow snapshot
- you need a full boundary contract review rather than a coverage audit

## Inputs

- target rule or stable truth
- current tests, checks, or examples
- known edge cases and stress cases
- the input space or states that matter most

## Outputs

- invariant coverage map
- gap list for weak or missing checks
- bounded follow-up checks or revisions
- concise verification summary

## Procedure

1. name the stable truth in plain language
2. map each existing check to the invariant it constrains
3. mark weak, redundant, or missing coverage
4. add only bounded cases that strengthen the weakest invariant first
5. report what the suite now proves and what it still does not

## Contracts

- every claimed invariant must be traceable to at least one check
- the audit should distinguish real constraint from mere example repetition
- the result should stay reviewable without sprawling into a full test strategy

## Risks and anti-patterns

- counting examples as if they were invariants
- letting random data hide thin coverage
- widening into generic test design or full suite architecture
- making the audit so abstract that no one can act on it

## Verification

- confirm each core invariant is named and mapped to a check
- confirm the coverage gap list is specific and bounded
- confirm another human can follow why the existing surface is or is not sufficient

## Technique traceability

Manifest-backed techniques:
- AOA-T-0017 from `8Dionysus/aoa-techniques` at `fe7df9aba3937435b431489ed0f9c5d52690a37c` using path `techniques/evaluation/property-invariants/TECHNIQUE.md` and sections: Intent, When to use, When not to use, Inputs, Outputs, Core procedure, Contracts, Risks, Validation

## Adaptation points

Project overlays should add:
- local test or check commands
- domain-specific invariants and edge cases
- notes on where coverage gaps are recorded
- rules for when a coverage audit should escalate into a deeper review
