---
name: source-verifier
description: Ensure every factual claim in a response is backed by verifiable evidence from the codebase, documentation, or external sources. Use when preparing technical documentation, code reviews, or any output where accuracy is non-negotiable.
---

# Source Verifier: Evidence-Based Responses

Every claim must have a source. No source, no claim.

## The rule

For every factual statement in your response, you must be able to point to where the evidence came from:

- Code claim -> cite file:line
- Config claim -> cite config file and key
- Dependency claim -> cite package.json or lock file
- Behavior claim -> cite test or runtime evidence
- History claim -> cite git commit or blame
- External claim -> cite documentation URL or error message

## Evidence types (ranked by strength)

### Tier 1: Direct observation (you just read it)
"The function at src/auth.ts:42 returns a Promise<boolean>"
Evidence: Read tool output from that file.

### Tier 2: Search confirmation (you found it)
"validateToken is called in 3 places across the codebase"
Evidence: Grep search results listing the files.

### Tier 3: Tool output (system told you)
"The test suite has 142 passing tests"
Evidence: Bash output from running the test command.

### Tier 4: Documented claim (someone else wrote it)
"According to the README, the API requires authentication"
Evidence: README.md content.

### Tier 5: Inference (you reasoned from evidence)
"Based on the error handling pattern, this likely throws on invalid input"
MUST be labeled as inference, not fact.

## How to cite

Good: "Looking at src/auth.ts:42-50, the validateToken function checks..."
Good: "Based on package.json, the project uses express@4.18.2"
Good: "Git blame shows this was last modified on 2026-02-15 by user@example.com"

Bad: "The function validates tokens" (no file reference)
Bad: "You're using an old version of express" (no version cited)
Bad: "This was recently changed" (no date or commit)

## Verification checklist before responding

Before sending any response with factual claims:

[ ] Every file path mentioned actually exists (verified with Glob)
[ ] Every function name is spelled correctly (verified with Grep or Read)
[ ] Every code quote matches the actual file content (verified with Read)
[ ] Every version number comes from package.json, not memory
[ ] Every "this does X" claim was verified by reading the code
[ ] Inferences are clearly labeled as inferences
[ ] Uncertainties are clearly stated as uncertainties

## When you cannot verify

Say exactly this:
"I haven't verified this against the codebase. Let me check."

Then use your tools to check. Never skip this step to save time.
