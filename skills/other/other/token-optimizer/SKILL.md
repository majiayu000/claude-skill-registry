---
name: token-optimizer
description: Reduce token count in prompts, docs, and prose. Covers prompt compression (40-60% savings), doc formatting, TOON data serialization, and Strunk's prose clarity rules. Use when compressing prompts, optimizing docs for LLM context, or writing clear technical prose.
author: George Khananaev
replaces: [prompt-compressor, token-formatter, elements-of-style]
---

# Token Optimizer

Reduce tokens in prompts, docs, and prose while preserving meaning.

## When to Use

- Prompt >1500 tokens or contains redundant phrasing
- Docs/markdown need compression for LLM context
- Writing prose for humans (docs, commits, PRs, error messages)
- Converting JSON/YAML/XML data for LLM input (TOON)

## Quick Routing

| Input Type | Go To |
|-----------|-------|
| User prompt / chat message | Section 1: Prompt Compression |
| Docs / markdown / README | Section 2: Doc Formatting |
| Commits / PRs / error messages | Section 3: Prose Clarity |
| JSON / YAML / XML data | Section 4: TOON Format |

## Compression Levels

| Level | Reduction | Use When |
|-------|-----------|----------|
| Light | 20-30% | Keep readability, human-facing prose |
| Medium | 40-50% | Default for LLM context |
| Heavy | 60-70% | Max compression, symbols over words |

---

## 1. Prompt Compression

### Process

1. Identify core intent
2. Extract essential context only
3. Remove filler phrases
4. Apply abbreviations & symbols
5. Output compressed version w/ token savings %

### Remove Phrases

| Remove | Transform To |
|--------|--------------|
| "Please help me with" | (delete) |
| "I need you to" | (delete) |
| "Could you please" | (delete) |
| "I would like to" | (delete) |
| "I think", "Maybe", "Perhaps" | (delete) |
| "This might be a dumb question" | (delete) |
| "For your reference" | (delete) |
| "As I mentioned before" | (delete) |

### Transform Patterns

| Verbose | Compressed |
|---------|------------|
| "I want to create a fn that takes X and returns Y" | `fn(X) -> Y` |
| "The error message says..." | `Error: ...` |
| "In the file located at..." | `File: ...` |
| "I'm trying to..." | `Goal: ...` |
| "Here is my code..." | `Code:` |
| "The problem is that..." | `Issue: ...` |

### Example

**Before (847 tokens):**
```
Hello! I hope you're doing well. I was wondering if you could help me.
I'm trying to build a React app and I need a custom hook that fetches
user data from /api/users. It returns JSON. I'd like loading, error
states, and caching. I think useEffect and useState but not sure...
```

**After (156 tokens):**
```
Goal: React hook for user data fetching
- Endpoint: /api/users -> JSON user obj
- Handle: loading, error states
- Cache response
Stack: React (useEffect, useState)
```

---

## 2. Doc Formatting

### Remove Filler Words

Remove when possible: "basically", "essentially", "actually", "really"

| Verbose | Compressed |
|---------|------------|
| "in order to" | "to" |
| "due to the fact that" | "because" |
| "at this point in time" | "now" |
| "in the event that" | "if" |
| "has the ability to" | "can" |
| "it is important to note that" | (remove) |

### Compress Lists

**Before:**
```markdown
The following features are included:
- User authentication with JWT tokens
- Role-based access control for authorization
- Password hashing using bcrypt algorithm
```

**After:**
```markdown
Features:
- JWT auth
- RBAC authz
- bcrypt passwords
```

### Structured Data Over Prose

**Before:**
```
The API accepts three parameters. The first is "userId" which is a
required string. The second is "limit", optional number, defaults to 10.
```

**After:**
```
Params:
- userId: str (req) - user ID
- limit: num (opt, def=10)
```

### Heading Compression

**Before:** `# Comprehensive Guide to User Authentication and Authorization`
**After:** `# Auth Guide`

### Table Compression

Shorten column headers, use abbreviations in cells:

| Param | Type | Req | Def | Desc |
|-------|------|-----|-----|------|
| userId | str | Y | - | user ID |
| limit | num | N | 10 | max results |

### Code Block Compression

Remove comments that restate the code. Collapse trivial logic:

**Before:**
```typescript
// Check if email is valid
const isEmailValid = emailRegex.test(email);
// Check if password is at least 8 characters
const isPasswordValid = password.length >= 8;
// Return true if both are valid
return isEmailValid && isPasswordValid;
```
**After:**
```typescript
return emailRegex.test(email) && password.length >= 8;
```

### URL & Path Compression

Replace full home paths: `/Users/username/Documents/Projects/MyApp/config/settings.json` -> `~/Projects/MyApp/config/settings.json`

### Error Message Compression

Keep error codes and stack traces exact. Compress surrounding prose:
`Err: Invalid/expired token. Re-authenticate at /auth/login`

---

## 3. Prose Clarity (Strunk's Rules)

Apply when writing prose for humans (docs, commits, PRs, errors).

### Grammar Essentials

1. Form possessive singular by adding 's
2. Use comma after each term in series except last
3. Don't join independent clauses by comma (use semicolon or period)
4. Participial phrase at beginning refers to grammatical subject

### Composition Essentials

1. One paragraph per topic
2. Begin paragraph with topic sentence
3. Express coordinate ideas in similar form
4. Keep related words together
5. Place emphatic words at end of sentence

### Limited Context Strategy

When context is tight: write draft, dispatch subagent with draft + these rules, have subagent copyedit and return revision.

### Core Principles

**Omit needless words:**

| Wordy | Concise |
|-------|---------|
| the question as to whether | whether |
| there is no doubt but that | no doubt |
| he is a man who | he |
| the reason why is that | because |

**Use active voice:**

| Passive | Active |
|---------|--------|
| The file was deleted by the user | The user deleted the file |
| Errors are logged by the system | The system logs errors |

**Positive form over negative:**

| Negative | Positive |
|----------|----------|
| did not remember | forgot |
| not important | trifling |
| not honest | dishonest |

**Specific over vague:**

| Vague | Specific |
|-------|----------|
| A period of unfavorable weather set in | It rained every day for a week |
| The data was processed | The server parsed 10,000 records |

### Technical Writing

```
# Commit: Bad
Made some changes to fix the bug that was causing issues

# Commit: Good
Fix null pointer in user authentication

# Error: Bad
An error occurred while processing your request

# Error: Good
Database connection failed: timeout after 30s

# Doc: Bad
This function is used for the purpose of validating user input

# Doc: Good
Validates user input
```

### Editing Checklist

- [ ] Unnecessary words (especially "that", "very", "really", "just")
- [ ] Passive voice -> convert to active
- [ ] Negative statements -> make positive
- [ ] Vague language -> make specific
- [ ] Long sentences -> break up or simplify

---

## 4. TOON Format (Data Serialization)

TOON replaces JSON/YAML/XML data serialization when sending to LLMs. ~40% fewer tokens.

**Convert to TOON:** JSON, YAML, XML (data objects/arrays only)
**Keep as-is:** Markdown, plain text, code files, CSV

**Precedence note:** TOON converts the *data format structure* (braces, quotes, colons). The "Never Compress" rules protect *values* inside data (API keys, URLs, version numbers). Both apply: convert structure to TOON, but preserve exact values.

**JSON:**
```json
{"users":[{"id":1,"name":"John","role":"admin"},{"id":2,"name":"Jane","role":"user"}]}
```

**TOON:**
```toon
users[2]{id,name,role}:
  1,John,admin
  2,Jane,user
```

See: `.claude/skills/document-skills/toon/SKILL.md`

---

## Never Compress

See `references/never_compress.md` for full list:
- Auth tokens, API keys, credentials, secrets
- Error stack traces (keep full)
- Code blocks, inline code, regex
- URLs, UUIDs, version numbers
- SQL queries, shell commands
- JSON keys, config values, date formats
- Legal text, mathematical formulas

---

## Abbreviations

```
fn=function  ret=return  str=string  num=number
bool=boolean arr=array   obj=object  param=parameter
config=configuration     env=environment
auth=authentication      authz=authorization
db=database  repo=repository  dir=directory
req=required opt=optional def=default
max=maximum  min=minimum  ex=example
impl=implementation      docs=documentation
app=application          info=information
```

## Symbols

```
-> = returns/produces    & = and
|  = or                  w/ = with
w/o = without            ~ = approximately
=> = therefore           bc = because
Y  = yes                 N  = no
-  = none/null
```

## Output Format

```markdown
## Compressed

[Content]

---
Original: X tokens | Compressed: Y tokens | Saved: Z%
```

## Scripts

```bash
# Compress text
python scripts/compress.py input.md > compressed.md
python scripts/compress.py input.md --stats
python scripts/compress.py --level 2 < input.md

# Count tokens
python scripts/count_tokens.py document.md

# Compress prompt
python scripts/compress_prompt.py "your prompt text"
python scripts/compress_prompt.py --file prompt.txt --level heavy
```

## Integration

**Called by:** `brainstorm` (Phase 5 docs), any skill producing documentation
**Pairs with:** `document-skills/toon` (data serialization)
