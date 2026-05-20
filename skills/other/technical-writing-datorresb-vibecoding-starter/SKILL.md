---
name: technical-writing
description: Technical documentation best practices for clear, accurate, and useful documentation. Use when writing documentation, README files, API docs, architecture guides, or any technical communication.
---

# Technical Writing Skill

## Core Principle

**Write for your audience, not for yourself.**

Technical documentation exists to help others understand and use your work. Good documentation:
- **Answers questions** before they're asked
- **Shows, doesn't just tell** (examples over abstract descriptions)
- **Stays current** (outdated docs are worse than no docs)
- **Is findable** (organized and searchable)

---

## Documentation Types

### 1. README Files

**Purpose:** First impression and quick-start guide

**Essential sections:**
```markdown
# Project Name

One-sentence description of what this project does.

## What It Does

2-3 sentences explaining the purpose and value.

## Quick Start

    npm install
    npm start
    # Now visit http://localhost:3000

## Installation

Detailed setup instructions.

## Usage

Common examples and use cases.

## Documentation

Link to full docs if they exist elsewhere.

## Contributing

How to contribute (if applicable).

## License

License information.
```

---

### 2. API Documentation

**Purpose:** How to use your API/library

**Essential elements:**
- Function/method signature
- Parameters with types
- Return value with type
- Examples
- Error conditions

**Example:**
```python
def calculate_discount(price: float, coupon_code: str) -> float:
    """
    Calculate the discounted price based on coupon code.

    Args:
        price: Original price in USD (must be positive)
        coupon_code: Coupon code (e.g., "SAVE10", "FREESHIP")

    Returns:
        Discounted price in USD

    Raises:
        ValueError: If price is negative
        CouponError: If coupon code is invalid or expired

    Examples:
        >>> calculate_discount(100.0, "SAVE10")
        90.0

        >>> calculate_discount(50.0, "FREESHIP")
        50.0  # Doesn't affect price

    Note:
        Coupon codes are case-insensitive. Free shipping coupons
        don't affect the returned price.
    """
```

---

### 3. How-To Guides

**Purpose:** Step-by-step instructions for specific tasks

**Structure:**
```markdown
# How to Deploy to Production

## Prerequisites

- Docker installed (v20+)
- AWS CLI configured
- Production credentials

## Steps

### 1. Build the Docker image

    docker build -t myapp:latest .

### 2. Tag for ECR

    docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

### 3. Push to ECR

    docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

### 4. Update ECS service

    aws ecs update-service --cluster prod --service myapp --force-new-deployment

### 5. Verify deployment

    curl https://myapp.com/health
    # Should return: {"status": "healthy"}

## Troubleshooting

**Issue:** Docker build fails with "out of space"

**Solution:** Clean up old images: `docker system prune -a`

---

**Issue:** ECS deployment stuck at 50%

**Solution:** Check CloudWatch logs for errors in new tasks
```

---

### 4. Architecture Documentation

**Purpose:** Explain system design and decisions

**Essential elements:**
- System overview diagram
- Component responsibilities
- Data flow
- Key decisions and trade-offs
- Non-obvious constraints

**Example:**
```markdown
# Authentication System Architecture

## Overview

We use JWT-based authentication with refresh tokens for stateless,
scalable authentication across microservices.

## Components

┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Client    │──────▶│  Auth API   │──────▶│  User DB    │
└─────────────┘       └─────────────┘       └─────────────┘
      │                      │
      │ Access Token         │ Verify Token
      ▼                      ▼
┌─────────────┐       ┌─────────────┐
│Resource API │◀──────│  API Gateway│
└─────────────┘       └─────────────┘

### Auth API
- Handles login/logout
- Issues access tokens (15min TTL) and refresh tokens (7 day TTL)
- Validates credentials against User DB

### API Gateway
- Verifies JWT signatures
- Checks token expiration
- Rejects invalid/expired tokens

### Resource APIs
- Trust gateway verification
- Extract user ID from token
- No direct auth logic

## Key Decisions

**Decision:** JWT instead of session cookies

**Rationale:**
- Stateless (no session storage needed)
- Works across domains
- Mobile-friendly
- Scales horizontally

**Trade-off:** Cannot invalidate tokens before expiry
**Mitigation:** Short TTL (15min) + refresh token rotation

---

**Decision:** Separate access and refresh tokens

**Rationale:**
- Limit exposure if access token stolen (short TTL)
- Refresh token stored securely (httpOnly cookie)
- Can invalidate refresh tokens server-side

## Security Considerations

- Tokens signed with RS256 (asymmetric)
- Private key stored in AWS Secrets Manager
- Public key distributed to all services
- Refresh token rotation on use (one-time use)
- Rate limiting on auth endpoints (10 req/min per IP)
```

---

## Writing Principles

### 1. Use Active Voice

❌ **Passive:** "The button should be clicked by the user"
✅ **Active:** "Click the button"

❌ **Passive:** "An error will be thrown if the input is invalid"
✅ **Active:** "The function throws an error if the input is invalid"

---

### 2. Be Specific and Concrete

❌ **Vague:** "Configure the system appropriately"
✅ **Specific:** "Set `max_connections` to 100 in `config.yml`"

❌ **Vague:** "The API might return an error"
✅ **Specific:** "Returns 404 if user not found, 400 if email invalid"

---

### 3. Show, Don't Just Tell

❌ **Abstract:** "The function takes a callback"
✅ **Example:**
```javascript
// Takes a callback that receives the result
processData(data, (result) => {
    console.log(result);
});
```

---

### 4. Lead with "Why"

❌ **What only:** "Set NODE_ENV=production"
✅ **Why + What:** "Set NODE_ENV=production to disable debug logging and enable optimizations"

---

### 5. Anticipate Questions

**Think about what users will ask:**

- How do I install it?
- What are the prerequisites?
- What does this error mean?
- How do I debug this?
- What are the common pitfalls?

**Answer them before they ask.**

---

## Code Examples

### Make Examples Runnable

❌ **Not runnable:**
```python
# Somewhere in your code
user = get_user()
```

✅ **Runnable:**
```python
from myapp import get_user

# Get currently logged-in user
user = get_user()
print(f"Hello, {user.name}")
```

---

### Show Expected Output

❌ **No output:**
```bash
python script.py
```

✅ **With output:**
```bash
$ python script.py
Processing 100 items...
Done! Saved to output.csv
```

---

### Handle Errors in Examples

❌ **Only happy path:**
```python
result = api.call()
print(result)
```

✅ **With error handling:**
```python
try:
    result = api.call()
    print(f"Success: {result}")
except APIError as e:
    print(f"API call failed: {e}")
    # Handle error appropriately
```

---

## Documentation Structure

### Progressive Disclosure

**Layer information by urgency:**

1. **Critical first** — What user needs right now
2. **Common next** — Frequently needed info
3. **Advanced last** — Edge cases and deep dives

**Example:**
```markdown
# Quick Start (Critical)

    npm install mylib
    import { doThing } from 'mylib'
    doThing()

# Common Use Cases (Common)

## Async operations
## Error handling
## Configuration

# Advanced Topics (Advanced)

## Custom plugins
## Performance tuning
## Internals (for contributors)
```

---

### Organization Patterns

**By User Journey:**
```
1. Installation
2. Quick Start
3. Core Concepts
4. Common Tasks
5. Advanced Features
6. API Reference
7. Troubleshooting
```

**By Feature:**
```
1. Overview
2. Authentication
3. Data Models
4. API Endpoints
5. Webhooks
6. Error Handling
```

---

## Documentation Maintenance

### Keep Docs in Sync with Code

✅ **Do:**
- Update docs in the same PR as code changes
- Review docs during code review
- Add "update docs" to PR checklist

❌ **Don't:**
- Say "I'll update docs later" (you won't)
- Merge code without doc updates
- Let docs drift out of date

---

### Version Documentation

**For public APIs:**
- Document breaking changes
- Keep old version docs accessible
- Provide migration guides

**Example:**
```markdown
# Migration Guide: v1 → v2

## Breaking Changes

### Authentication

**v1:**
```python
client = MyAPI(api_key="...")
```

**v2:**
```python
client = MyAPI(token="...")  # Renamed 'api_key' to 'token'
```

**Why:** Clarify that we accept JWT tokens, not just API keys

## Migration Steps

1. Replace `api_key=` with `token=` in all `MyAPI()` calls
2. Test your integration
3. Update your API token in production settings
```

---

## Common Documentation Anti-Patterns

### 1. "It's Self-Explanatory"

❌ **Anti-pattern:** No docs because "code is self-documenting"

**Reality:** Code shows HOW. Docs explain WHY and WHAT FOR.

```python
# Code (shows HOW)
def calculate_checksum(data, algorithm='sha256'):
    return hashlib.new(algorithm, data).hexdigest()

# Docs (explain WHY and WHAT FOR)
"""
Calculate cryptographic checksum for data integrity verification.

Use this to:
- Verify file downloads weren't corrupted
- Detect unauthorized file modifications
- Generate unique content identifiers

Supports: md5, sha1, sha256, sha512
Default (sha256) provides good security/performance balance.
"""
```

---

### 2. Outdated Examples

❌ **Anti-pattern:** Examples that don't work with current version

**Prevention:**
- Test examples as part of CI
- Extract examples into runnable tests
- Review docs in every release

---

### 3. Missing Prerequisites

❌ **Anti-pattern:** "Just run the install script"

**Reality:** Script fails because user doesn't have Python 3.9+

✅ **Fix:**
```markdown
## Prerequisites

- Python 3.9 or higher ([download](https://python.org))
- pip (included with Python)
- 500MB free disk space

Check your Python version:

    python --version

Should output: Python 3.9.0 or higher
```

---

### 4. No Troubleshooting Section

❌ **Anti-pattern:** "It should just work"

**Reality:** Users encounter issues and have nowhere to look

✅ **Fix:** Include common issues and solutions
```markdown
## Troubleshooting

### "Module not found" error

**Cause:** Package not installed or wrong Python environment

**Solution:**
1. Activate your virtual environment: `source venv/bin/activate`
2. Reinstall: `pip install mypackage`
3. Verify: `pip show mypackage`
```

---

## Quick Documentation Checklist

Before publishing docs:

- [ ] **Accuracy** — All code examples work
- [ ] **Completeness** — Answers common questions
- [ ] **Clarity** — Non-experts can understand
- [ ] **Examples** — Shows real usage, not toy examples
- [ ] **Error handling** — Explains what can go wrong
- [ ] **Prerequisites** — Lists requirements
- [ ] **Current** — Matches latest version
- [ ] **Findable** — Easy to navigate
- [ ] **Maintainable** — Can be updated easily

---

## Integration with Other Skills

### With Git Hygiene

- Update docs in same commit as code changes
- Commit message: "docs: add installation guide for Windows"

### With Code Review

- Review docs as part of PR review
- Check that examples are accurate
- Verify API changes are documented

### With Testing

- Test code examples in CI
- Use doctest (Python) or similar tools
- Ensure examples stay current

---

## Quick Reference

### README Template

```markdown
# Project Name

One-sentence description.

## Quick Start

    # Install and run
    npm install
    npm start

## Features

- Feature 1
- Feature 2

## Documentation

See [docs/](docs/) for full documentation.

## License

MIT
```

### API Doc Template

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """
    One-sentence description.

    Longer explanation if needed.

    Args:
        param1: Description
        param2: Description

    Returns:
        Description

    Raises:
        ErrorType: When this happens

    Examples:
        >>> function_name(value1, value2)
        expected_output
    """
```

---

**Remember:** Good documentation enables others to use your work without asking you questions. Write for your audience. Show examples. Keep it current. If users are asking the same questions repeatedly, that's a sign your docs need improvement.
