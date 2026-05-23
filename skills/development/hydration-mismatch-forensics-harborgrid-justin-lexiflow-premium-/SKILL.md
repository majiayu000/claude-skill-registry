---
name: hydration-mismatch-forensics
description: Debug and resolve complex hydration mismatches that cause UI thrashing and content layout shifts.
---

# Hydration Mismatch Forensics

## Summary
Debug and resolve complex hydration mismatches that cause UI thrashing and content layout shifts.

## Key Capabilities
- Identify distinct mismatch types (text, attribute, structure).
- Trace server-client state divergence sources (Time, Randomness).
- Implement suppression and recovery strategies for unavoidable mismatches.

## PhD-Level Challenges
- Analyze the performance cost of hydration patching.
- Detect deeper mismatches in third-party library output.
- Automate mismatch detection in CI pipelines.

## Acceptance Criteria
- Deliver a mismatch-free console in production builds.
- Demonstrate automated detection of new mismatches.
- Document common mismatch patterns and fixes.
