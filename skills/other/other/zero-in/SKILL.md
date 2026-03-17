---
name: zero-in
description: |
  Before searching a codebase, forces you to zero in on the target: what exactly
  are you looking for, what would it look like, where would it live, what else
  might it be called. Activates on "find", "where is", "search for", or when
  exploration begins. Prevents grep-and-pray.
allowed-tools: |
  bash: grep, find, git
  file: read
---

# Zero In

<purpose>
The #1 search failure: jumping straight to grep without thinking. You search
"auth", get 200 results, grep again with "login", still garbage. The problem
isn't the search - it's that you didn't zero in first. This skill forces the
targeting that should happen BEFORE you hit enter.
</purpose>

## When To Activate

<triggers>
- "Where is the..."
- "Find the code that..."
- "Search for..."
- "How does X work in this codebase?"
- About to explore an unfamiliar codebase
- Previous search returned too many/wrong results
- User says "I can't find..."
</triggers>

## Instructions

### Before ANY Search

Answer these four questions:

<scope>
## 1. What exactly am I looking for?

State it in one sentence. Be specific.

```
BAD:  "authentication stuff"
GOOD: "the function that validates JWT tokens on API requests"
```

If you can't state it in one sentence, you don't know what you're looking for.
</scope>

<shape>
## 2. What would the answer look like?

Describe what you expect to find:

- File type? (`.ts`, `.py`, `.go`, config file?)
- Function, class, or config?
- Roughly how big? (one-liner vs module?)
- What would it import/use?

```
Example: "Probably a middleware function in TypeScript, imports jsonwebtoken
or jose, has 'verify' or 'validate' in the name, 20-50 lines"
```
</shape>

<where>
## 3. Where would it live?

Based on project conventions:

- Which directory? (`src/`, `lib/`, `middleware/`, `utils/`?)
- What would the file be named?
- Near what other code?

```
Example: "Likely in src/middleware/ or src/auth/, file probably named
auth.ts, jwt.ts, or middleware.ts"
```

Check the project structure first if unsure:
```bash
ls -la src/
find . -type d -name "*auth*" -o -name "*jwt*"
```
</where>

<aliases>
## 4. What else might it be called?

List synonyms, abbreviations, variations:

```
Example for JWT validation:
- verify, validate, check, authenticate
- jwt, token, bearer, authorization
- middleware, handler, guard, interceptor
```

Your first search term is rarely the one the codebase uses.
</aliases>

### Then Search

Now search, using insights from scoping:

```bash
# Start with WHERE + ALIASES
grep -r "verify.*token" src/middleware/
grep -r "jwt" src/auth/

# If needed, broaden
grep -r "token" src/ --include="*.ts"
```

### Verify The Result

Before declaring "found it":

- [ ] Does this match what I described in step 2?
- [ ] Is this THE thing, or just A thing that mentions it?
- [ ] If it's a function, trace who calls it
- [ ] If it's config, trace what uses it

## Output Format

```markdown
## Search Scope

**Looking for:** [one sentence]

**Would look like:** [description]

**Likely location:** [directories/files]

**Search terms:** [list of aliases]

## Search Results

Found: [file:line]

Verified: [Yes/No - why]
```

## NEVER

- Start grepping without answering the four questions
- Search for vague terms ("stuff", "thing", "code")
- Stop at the first result without verifying it's THE answer
- Broaden search before narrowing location
- Ignore project structure/conventions

## ALWAYS

- State what you're looking for in one sentence first
- Check project structure before searching
- List 3+ aliases/synonyms for your search term
- Verify the result matches your expected shape
- Narrow by location before broadening by term

## Example

**User:** "Find where we handle rate limiting"

**Scoping:**

> **Looking for:** The middleware or function that tracks request counts and returns 429 when limit exceeded
>
> **Would look like:** Middleware function, probably uses Redis or in-memory store, has "rate" or "limit" or "throttle" in name, checks request count, returns 429
>
> **Likely location:** `src/middleware/`, maybe `src/api/`, file named `rateLimit.ts` or `throttle.ts`
>
> **Search terms:** rate, limit, throttle, 429, tooMany, requests

**Search:**
```bash
# Check structure first
ls src/middleware/
# Found: auth.ts, cors.ts, rateLimit.ts  <-- bingo

# Verify
grep -n "429\|rate\|limit" src/middleware/rateLimit.ts
```

**Result:** `src/middleware/rateLimit.ts:23` - `rateLimiter` middleware using Redis, returns 429 after 100 req/min.

**Verified:** Yes - matches expected shape (middleware, uses Redis, returns 429).

## The Failure That Spawned This Skill

Grepping "auth" in a 50k line codebase. 200+ results. Refined to "login".
Still 80 results. Spent 20 minutes reading wrong files. Finally found it
in `src/middleware/session.ts` - wasn't called "auth" or "login" anywhere.
Should have asked "where would session validation live?" first.
