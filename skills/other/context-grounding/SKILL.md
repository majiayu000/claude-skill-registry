---
name: context-grounding
description: Forces Claude to extract exact quotes from files before making claims about them. Prevents hallucinations by grounding every statement in actual text from the codebase. Use when working with large files or unfamiliar code.
---

# Context Grounding

Read first. Quote second. Claim third. Never skip a step.

## The grounding technique

Before making any claim about code, follow this sequence:

### Step 1: Read the source
Read the actual file. Don't work from memory.

### Step 2: Extract the relevant quote
Pull the exact text that supports your claim. Include line numbers.

### Step 3: Make your claim based on the quote
Now state what you believe, citing the quote as evidence.

## Example

Wrong approach:
"The auth middleware checks for JWT tokens and returns 401 if invalid."
(No evidence. Could be hallucinated.)

Grounded approach:
"Reading src/middleware/auth.ts:15-25, the middleware does:
```
const token = req.headers.authorization?.split(' ')[1];
if (!token) return res.status(401).json({ error: 'No token provided' });
```
So it extracts the Bearer token from the Authorization header and returns 401 if missing."

## When to ground

Always ground when:
- Answering questions about specific code behavior
- Writing code reviews or change proposals
- Explaining how something works
- Describing bug causes
- Making security assessments

## Grounding for long documents

For files over 100 lines:
1. Read the full file first to understand structure
2. Identify the specific section relevant to the question
3. Re-read that section carefully
4. Extract the key lines as quotes
5. Build your answer from those quotes

For files over 500 lines:
1. Use Grep to find the relevant section
2. Read just that section (use offset and limit)
3. Extract quotes from what you read
4. If you need more context, read surrounding sections
5. Never make claims about sections you haven't read

## The grounding test

Before sending a response, test each factual statement:
"Could someone verify this by reading the file I'm referencing?"

If yes: the statement is grounded.
If no: you need to add the file reference and relevant quote.
If you don't have a file to reference: either find one or mark as unverified.
