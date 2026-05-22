---
name: token-formatter
description: Convert verbose docs/markdown/text into token-efficient formats. Use when user wants to reduce token count, compress content for LLM context, or optimize for AI consumption.
author: George Khananaev
---

# Token Formatter Skill

Convert verbose documentation, markdown, and text files into token-efficient formats while preserving essential information.

## When to Use

Invoke this skill when:
- User wants to reduce token count in documentation
- User needs to compress markdown/text for LLM context
- User asks to optimize content for AI consumption
- Commands: `/token-format`, `/compress`, `/toon`

## Token Reduction Rules

### 1. Remove Redundancy

**Before:**
```markdown
## Introduction

In this document, we will explore and discuss the various different ways
that you can implement authentication in your application. We will cover
multiple approaches and methods that are available to developers.
```

**After:**
```markdown
## Auth Implementation

Methods covered:
- JWT tokens
- Session-based
- OAuth2
```

### 2. Use Symbols & Abbreviations

| Verbose | Compressed |
|---------|------------|
| function | fn |
| return | ret |
| string | str |
| number | num |
| boolean | bool |
| array | arr |
| object | obj |
| parameter | param |
| configuration | config |
| environment | env |
| authentication | auth |
| authorization | authz |
| application | app |
| database | db |
| repository | repo |
| directory | dir |
| reference | ref |
| implementation | impl |
| documentation | docs |
| information | info |
| example | ex |
| required | req |
| optional | opt |
| default | def |
| maximum | max |
| minimum | min |
| and | & |
| or | \| |
| with | w/ |
| without | w/o |
| versus | vs |
| approximately | ~  |
| greater than | > |
| less than | < |
| equals | = |
| not equals | != |
| therefore | => |
| because | bc |

### 3. Compress Lists

**Before:**
```markdown
The following features are included:
- User authentication with JWT tokens
- Role-based access control for authorization
- Password hashing using bcrypt algorithm
- Session management with Redis store
- Two-factor authentication support
```

**After:**
```markdown
Features:
- JWT auth
- RBAC authz
- bcrypt passwords
- Redis sessions
- 2FA support
```

### 4. Remove Filler Words

Remove these words when possible:
- "basically", "essentially", "actually", "really"
- "in order to" → "to"
- "due to the fact that" → "because"
- "at this point in time" → "now"
- "in the event that" → "if"
- "for the purpose of" → "for"
- "has the ability to" → "can"
- "it is important to note that" → (remove)
- "please note that" → (remove)
- "as mentioned previously" → (remove)

### 5. Structured Data Format

**Before (prose):**
```markdown
The API endpoint accepts three parameters. The first parameter is called
"userId" which is a required string that identifies the user. The second
parameter is "limit" which is an optional number that defaults to 10.
The third parameter is "offset" which is also optional and defaults to 0.
```

**After (structured):**
```
Params:
- userId: str (req) - user ID
- limit: num (opt, def=10)
- offset: num (opt, def=0)
```

### 6. Code Block Compression

**Before:**
```typescript
// This function validates the user input
// It checks if the email is valid and the password meets requirements
function validateUserInput(email: string, password: string): boolean {
  // Check if email is valid
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const isEmailValid = emailRegex.test(email);

  // Check if password is at least 8 characters
  const isPasswordValid = password.length >= 8;

  // Return true if both are valid
  return isEmailValid && isPasswordValid;
}
```

**After:**
```typescript
fn validateUserInput(email: str, password: str): bool {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) && password.length >= 8;
}
```

### 7. Table Compression

**Before:**
```markdown
| Parameter Name | Type | Required | Default Value | Description |
|---------------|------|----------|---------------|-------------|
| userId | string | yes | none | The unique identifier for the user |
| limit | number | no | 10 | Maximum number of results to return |
| offset | number | no | 0 | Number of results to skip |
```

**After:**
```
| Param | Type | Req | Def | Desc |
|-------|------|-----|-----|------|
| userId | str | Y | - | user ID |
| limit | num | N | 10 | max results |
| offset | num | N | 0 | skip count |
```

### 8. Heading Compression

**Before:**
```markdown
# Comprehensive Guide to User Authentication and Authorization

## Chapter 1: Introduction to Authentication Concepts

### Section 1.1: Understanding the Basics of User Identity
```

**After:**
```markdown
# Auth Guide

## 1. Intro

### 1.1 Identity Basics
```

### 9. URL & Path Compression

**Before:**
```markdown
The configuration file is located at `/Users/username/Documents/Projects/MyApp/config/settings.json`
```

**After:**
```markdown
Config: `~/Projects/MyApp/config/settings.json`
```

### 10. Error Message Compression

**Before:**
```markdown
Error: The authentication token that was provided in the request header
is either invalid, expired, or has been revoked. Please obtain a new
token by logging in again through the authentication endpoint.
```

**After:**
```markdown
Err: Invalid/expired token. Re-authenticate at /auth/login
```

## Compression Process

### Step 1: Analyze Content
1. Identify content type (docs, code, config, etc.)
2. Find repetitive patterns
3. Locate verbose sections
4. Note essential vs non-essential info

### Step 2: Apply Rules
1. Remove filler words
2. Apply abbreviations
3. Convert prose to structured data
4. Compress code blocks
5. Shorten headings

### Step 3: Validate
1. Ensure meaning preserved
2. Check readability
3. Verify no critical info lost
4. Test comprehension

## Output Format

```markdown
# [Compressed Title]

## Summary
[1-2 line summary]

## Content
[Compressed content using rules above]

---
Original: X tokens | Compressed: Y tokens | Saved: Z%
```

## Compression Levels

### Level 1: Light (20-30% reduction)
- Remove filler words
- Shorten obvious terms
- Keep full sentences

### Level 2: Medium (40-50% reduction)
- Apply abbreviations
- Use structured format
- Remove redundancy

### Level 3: Heavy (60-70% reduction)
- Maximum compression
- Symbols over words
- Minimal prose

## Examples

### Example 1: API Documentation

**Original (847 tokens):**

    # User Management API Documentation

    ## Introduction

    Welcome to the User Management API documentation. This comprehensive guide
    will walk you through all the available endpoints and explain how to use
    them effectively in your application.

    ## Authentication

    Before making any API requests, you need to authenticate your application.
    Authentication is handled through JWT (JSON Web Tokens). To obtain a token,
    send a POST request to the `/auth/login` endpoint with your credentials.

    ### Request Format

    The request should be sent as JSON with the following structure:
    {"email": "user@example.com", "password": "your_password"}

    ### Response Format

    A successful authentication will return:
    {"token": "eyJhbGciOiJIUzI1NiIs...", "expiresIn": 3600, "tokenType": "Bearer"}

**Compressed (312 tokens):**

    # User API

    ## Auth

    JWT-based. Get token via POST `/auth/login`

    Req: {"email": "user@example.com", "password": "..."}
    Res: {"token": "eyJ...", "expiresIn": 3600, "tokenType": "Bearer"}

    ---
    Saved: 63%

### Example 2: README

**Original:**

    # My Awesome Project

    ## About This Project

    This project was created to solve the problem of managing user data in
    a scalable and efficient manner. It provides a comprehensive set of tools
    and utilities that developers can use to build robust applications.

    ## Installation Instructions

    To install this project, you will need to have Node.js version 18 or
    higher installed on your system. Run: npm install && npm run dev

**Compressed:**

    # My Project

    Scalable user data management tools.

    ## Install

    Requires: Node.js 18+
    Run: npm install && npm run dev

## Do NOT Compress

- Code syntax (keep valid)
- API keys/secrets (keep exact)
- Version numbers
- URLs/endpoints
- Error codes
- Mathematical formulas
- Legal text
- Security-critical info

## Automation

Two Python scripts are available in the `scripts/` directory to help automate the compression and validation process.

### Prerequisites

For accurate token counting (optional but recommended), install `tiktoken`:
```bash
pip install tiktoken
```
(If not installed, scripts will fallback to character count estimation).

### 1. Compression Script (`compress.py`)

Automatically applies common compression rules (filler removal, abbreviations, symbols).

**Usage:**
```bash
# Compress a file
python .claude/skills/token-formatter/scripts/compress.py input.md > compressed.md

# Compress input from pipe
cat input.md | python .claude/skills/token-formatter/scripts/compress.py --level 2

# Show stats
python .claude/skills/token-formatter/scripts/compress.py input.md --stats
```

### 2. Token Counter (`count_tokens.py`)

Counts tokens in files or text input.

**Usage:**
```bash
# Count tokens in files
python .claude/skills/token-formatter/scripts/count_tokens.py document.md README.md

# Count tokens from pipe
echo "Hello World" | python .claude/skills/token-formatter/scripts/count_tokens.py
```

## TOON Format (Data Serialization → TOON for LLM Input)

TOON replaces **data serialization formats** when sending to LLMs. ~40% fewer tokens.

### Formats to convert → TOON:
- **JSON** / **JSON compact**
- **YAML**
- **XML**

### Do NOT convert to TOON:
- **Markdown** - keep as markdown
- **Plain text** - keep as text
- **Code files** - keep original syntax
- **CSV** - already compact for flat tables

### TOON sweet spot:
Uniform arrays of objects (same fields per item) from JSON/YAML/XML.

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

### When to ask:
"This contains JSON/YAML/XML data for LLM input. Convert to TOON for ~40% token savings?"

See: `.claude/skills/document-skills/toon/SKILL.md`

## Quick Reference Card

### Abbreviations
```
fn=function  ret=return  str=string  num=number
bool=boolean arr=array   obj=object  param=parameter
config=configuration     env=environment
auth=authentication      authz=authorization
db=database  repo=repository  dir=directory
req=required opt=optional def=default
max=maximum  min=minimum  ex=example
impl=implementation      docs=documentation
```

### Symbols
```
&   = and           |   = or
w/  = with          w/o = without
=>  = therefore     ~   = approximately
Y   = yes           N   = no
-   = none/null
```
