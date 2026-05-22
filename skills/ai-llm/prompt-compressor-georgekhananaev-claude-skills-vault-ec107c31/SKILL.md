---
name: prompt-compressor
description: Compress verbose prompts & context before LLM processing. This skill should be used when input exceeds 1500 tokens, contains redundant phrasing, or includes unnecessary context. Reduces tokens by 40-60%.
author: George Khananaev
---

# Prompt Compressor

Compress verbose prompts/context before processing. Saves 40-60% tokens.

## When to Use

Invoke when:
- Input >1500 tokens
- User pastes entire files (needs only sections)
- Prompts have redundant phrasing
- Context includes irrelevant info
- Commands: `/compress-prompt`, `/cp`

## Process

1. **Identify core intent** - What user actually wants
2. **Extract essential context** - Only what's needed
3. **Remove redundant phrases** - See rules below
4. **Apply abbreviations** - Use `token-formatter` conventions
5. **Output compressed version** - w/ token savings %

## Compression Rules

### Remove Phrases

| Remove | Transform To |
|--------|--------------|
| "Please help me with" | (delete) |
| "I need you to" | (delete) |
| "Could you please" | (delete) |
| "I would like to" | (delete) |
| "I think", "Maybe", "Perhaps" | (delete) |
| "This might be a dumb question" | (delete) |
| "As I mentioned before" | (delete) |
| "For your reference" | (delete) |

### Transform Patterns

| Verbose | Compressed |
|---------|------------|
| "I want to create a fn that takes X and returns Y" | `fn(X) → Y` |
| "The error message says..." | `Error: ...` |
| "In the file located at..." | `File: ...` |
| "I'm trying to..." | `Goal: ...` |
| "Here is my code..." | `Code:` |
| "The problem is that..." | `Issue: ...` |

### Never Compress (Security)

See `references/never_compress.md` for full list:
- Auth headers, tokens, credentials
- Error stack traces (keep full)
- Security-related context
- API keys, secrets
- Exact error messages
- File paths in errors

## Output Format

```
## Compressed Prompt

[Compressed content]

---
Original: X tokens | Compressed: Y tokens | Saved: Z%
```

## Examples

### Example 1: Verbose Request

**Before (847 tokens):**
```
Hello! I hope you're doing well today. I was wondering if you could please
help me with something. I'm trying to build a React application and I need
to create a custom hook that fetches user data from an API. The API is
located at /api/users and it returns a JSON response with the user object.
I would like the hook to handle loading states, error states, and also
cache the response. I think this might need to use useEffect and useState
but I'm not entirely sure about the best approach. Could you please help
me implement this? Here is some context about my project structure...
[500 more tokens of context]
```

**After (156 tokens):**
```
Goal: Create React hook for user data fetching

Requirements:
- Endpoint: /api/users → JSON user obj
- Handle: loading, error states
- Cache response

Stack: React (useEffect, useState)

---
Saved: 82%
```

### Example 2: Error Context

**Before:**
```
I'm having a problem with my application. When I try to log in, I get an
error. The error message that appears on the screen says "TypeError: Cannot
read property 'map' of undefined" and it's happening in the UserList.tsx
file on line 42. I think the problem might be related to the API response
but I'm not sure. Here is my entire component file...
[entire 200-line file]
```

**After:**
```
Error: TypeError: Cannot read property 'map' of undefined
File: UserList.tsx:42
Issue: API response may be undefined before .map()

Need: Null check or loading state
```

## Compression Levels

| Level | Reduction | Use When |
|-------|-----------|----------|
| Light | 20-30% | Keep readability |
| Medium | 40-50% | Default |
| Heavy | 60-70% | Max compression |

## Integration

Works w/ `token-formatter` skill:
- Uses same abbreviations (fn, str, num, etc.)
- Same symbols (&, \|, w/, w/o, →)
- Same "Do NOT Compress" rules

## Script Usage

```bash
# Compress prompt text
python scripts/compress_prompt.py "your prompt text here"

# Compress from file
python scripts/compress_prompt.py --file prompt.txt

# Set compression level
python scripts/compress_prompt.py --level heavy "text"
```

## Quick Reference

### Abbreviations (from token-formatter)
```
fn=function  str=string  num=number  bool=boolean
arr=array    obj=object  param=parameter
config=configuration     env=environment
auth=authentication      db=database
req=required opt=optional def=default
```

### Symbols
```
→ = returns/produces    & = and
| = or                  w/ = with
w/o = without           ~ = approximately
```