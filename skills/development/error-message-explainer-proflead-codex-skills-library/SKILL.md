---
name: error-message-explainer
description: Explain compiler/runtime errors in plain language. Use when a junior developer needs help understanding an error message.
---

# Error Message Explainer

## Purpose
Explain compiler/runtime errors in plain language.

## Inputs to request
- Full error text and stack trace.
- Code snippet around the failing line.
- Runtime or compiler version.

## Workflow
1. Restate the error in simple terms.
2. Point to the most likely offending line or call.
3. Provide one or two possible fixes.

## Output
- Plain-language explanation.
- Fix suggestions with examples.

## Quality bar
- Cite the exact line or symbol if possible.
- Offer the smallest viable fix first.
