---
name: citation-enforcer
description: Forces every code-related claim to include file:line citations. No citation means the claim must be verified or removed. Use when building documentation, writing code reviews, or any output that others will rely on.
---

# Citation Enforcer

Every code claim needs a citation. file:line or it didn't happen.

## The rule

When you mention any of these, include the file path and line number:

- A function name -> "validateToken() at src/auth.ts:42"
- A variable -> "the MAX_RETRIES constant at src/config.ts:15"
- A class -> "the UserService class at src/services/user.ts:1"
- An import -> "imported from @auth/core at src/auth.ts:3"
- A config value -> "timeout set to 30000 at config/default.json:12"
- An error message -> "the error 'Invalid token' thrown at src/auth.ts:67"

## Citation format

Standard: `file:line`
Example: `src/auth.ts:42`

With range: `file:line-line`
Example: `src/auth.ts:42-58`

With context: `description at file:line`
Example: "the validateToken function at src/auth.ts:42"

## Self-check

Before sending a response, scan it for uncited claims:

1. Find every mention of a function, file, class, or variable
2. Does each one have a file:line citation?
3. If not, either:
   a. Use Read/Grep to find the actual location and add it
   b. Remove the claim if you can't find it
   c. Clearly state "I haven't verified where this is located"

## Examples

Bad: "The authentication middleware checks for valid tokens."
Good: "The authentication middleware at src/middleware/auth.ts:15-30 checks for valid tokens by calling validateToken()."

Bad: "There's a bug in the error handling."
Good: "The catch block at src/api/users.ts:87 swallows the error without logging it."

Bad: "The config file has the wrong timeout."
Good: "The timeout at config/production.json:23 is set to 5000ms, which may be too low for this API call."

## When citations aren't needed

- General programming concepts ("REST APIs use HTTP methods")
- Suggestions that aren't about existing code ("you could add a retry mechanism")
- Questions to the user ("what error are you seeing?")
- Tool output that already includes file references
