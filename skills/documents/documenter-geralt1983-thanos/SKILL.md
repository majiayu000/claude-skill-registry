---
name: Documenter
description: Documentation writing, API docs, and technical writing. USE WHEN user mentions document, docs, README, comments, docstrings, API documentation, JSDoc, explain code, write documentation, ADR, architecture decision, or asks to explain or document something.
---

# Documenter Skill

AI-powered documentation guidance for creating clear, comprehensive, and maintainable documentation with focus on audience awareness, structure, and practical usefulness.

## What This Skill Does

This skill provides expert-level documentation guidance including README creation, API documentation, inline comments, architecture decision records, and technical writing. It combines documentation best practices with practical, audience-appropriate content.

**Key Capabilities:**
- **README Creation**: Project overviews, quick starts, installation guides
- **API Documentation**: Endpoint docs, function signatures, examples
- **Inline Comments**: Code comments, docstrings, annotations
- **Architecture Docs**: ADRs, design documents, system overviews
- **User Guides**: Tutorials, how-tos, troubleshooting
- **Changelog/Release Notes**: Version history, migration guides

## Core Principles

### The Documentation Mindset
- **Know Your Audience**: Write for who will read it
- **Start with Why**: Context before mechanics
- **Show, Don't Tell**: Examples over explanations
- **Keep It Current**: Stale docs are worse than no docs
- **Progressive Disclosure**: Simple first, details later

### Documentation Quality Metrics
1. **Findability** - Can readers find what they need?
2. **Accuracy** - Is the information correct and current?
3. **Completeness** - Are all important topics covered?
4. **Clarity** - Is it easy to understand?
5. **Usability** - Can readers apply the information?

## Documentation Types

### README Structure
```markdown
# Project Name
> One-line description of what this does

## Quick Start
Fastest path to "Hello World"

## Installation
How to get it running

## Usage
Common use cases with examples

## API Reference (or link)
Function/endpoint documentation

## Configuration
Available options and settings

## Contributing
How to contribute

## License
Terms of use
```

### API Documentation
```markdown
## endpoint_name

Brief description of what this endpoint does.

### Request
`METHOD /path/to/endpoint`

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | The resource identifier |
| limit | integer | No | Max results (default: 10) |

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |

### Response

**Success (200 OK):**
```json
{
  "id": "abc123",
  "name": "Example"
}
```

**Errors:**
| Code | Description |
|------|-------------|
| 400 | Invalid request parameters |
| 401 | Not authenticated |
| 404 | Resource not found |

### Example
```bash
curl -X GET "https://api.example.com/resource/123" \
  -H "Authorization: Bearer TOKEN"
```
```

### Architecture Decision Record (ADR)
```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted | Proposed | Deprecated | Superseded by ADR-XXX

## Context
What is the issue that we're seeing that motivates this decision?
Describe the forces at play (technical, business, social, project).

## Decision
What is the change that we're proposing and/or doing?
State the decision in full sentences, with active voice.

## Consequences

### Positive
- What becomes easier or possible as a result?

### Negative  
- What becomes more difficult?

### Neutral
- Other effects that are neither clearly positive nor negative

## References
- Links to related documents, discussions, or research
```

## Inline Documentation Guide

### Python Docstrings
```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate the discounted price.

    Applies a percentage discount to the original price and returns
    the final price after discount.

    Args:
        price: Original price in dollars. Must be >= 0.
        discount_percent: Discount as a percentage (0-100).
            A value of 10 means 10% off.

    Returns:
        The price after applying the discount.

    Raises:
        ValueError: If price is negative or discount_percent
            is not between 0 and 100.

    Examples:
        >>> calculate_discount(100.0, 10)
        90.0
        >>> calculate_discount(50.0, 25)
        37.5
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    return price * (1 - discount_percent / 100)
```

### JavaScript/TypeScript JSDoc
```typescript
/**
 * Fetches user profile data from the API.
 * 
 * @param userId - The unique identifier for the user
 * @param options - Optional configuration for the request
 * @param options.includeStats - Whether to include usage statistics
 * @param options.cache - Cache duration in seconds (default: 300)
 * @returns Promise resolving to the user profile
 * @throws {NotFoundError} When user doesn't exist
 * @throws {AuthError} When not authenticated
 * 
 * @example
 * // Basic usage
 * const profile = await getUserProfile('user-123');
 * 
 * @example
 * // With options
 * const profile = await getUserProfile('user-123', {
 *   includeStats: true,
 *   cache: 600
 * });
 */
async function getUserProfile(
  userId: string, 
  options?: { includeStats?: boolean; cache?: number }
): Promise<UserProfile> {
  // implementation
}
```

### Java Javadoc
```java
/**
 * Processes an order and returns the confirmation number.
 *
 * <p>This method validates the order, charges the payment method,
 * and creates the order record. If any step fails, the entire
 * transaction is rolled back.</p>
 *
 * @param order the order to process, must not be null
 * @param paymentMethod the payment method to charge
 * @return the confirmation number for the processed order
 * @throws InvalidOrderException if the order is invalid or incomplete
 * @throws PaymentException if the payment fails
 * @throws InventoryException if items are out of stock
 * @since 2.0
 * @see #cancelOrder(String)
 */
public String processOrder(Order order, PaymentMethod paymentMethod)
    throws InvalidOrderException, PaymentException, InventoryException {
    // implementation
}
```

## Comment Best Practices

### When to Comment
```python
# ✓ GOOD: Explain WHY, not WHAT
# We use a 24-hour cache because the data changes at most once daily
# and the API has strict rate limits
cache_duration = 86400

# ✗ BAD: Explaining obvious code
# Set the variable x to 5
x = 5

# ✓ GOOD: Document non-obvious behavior
# Note: Returns empty list rather than None for consistency with
# other collection methods in this module
def get_items():
    return []

# ✓ GOOD: Warn about gotchas
# WARNING: This modifies the input list in place for performance.
# Pass a copy if you need to preserve the original.
def sort_in_place(items):
    items.sort()

# ✓ GOOD: Document workarounds
# HACK: The vendor API returns dates in local time without timezone info.
# We assume UTC since their servers are in the US-East zone and we 
# confirmed this with their support team (ticket #12345).
timestamp = parse_without_tz(api_response['date'])

# ✓ GOOD: TODO with context
# TODO(jsmith): Replace with proper caching once Redis is set up
# See https://jira.example.com/browse/PROJ-1234
def get_cached_value(key):
    return database.query(key)  # Direct DB hit for now
```

### What Not to Comment
```python
# ✗ Don't comment obvious code
counter = counter + 1  # Increment counter

# ✗ Don't leave commented-out code (use version control)
# old_implementation()
# another_old_thing()
new_implementation()

# ✗ Don't use comments as a substitute for clear code
# Get the user's first name from the data dictionary
n = d['fn']

# ✓ Instead, use clear variable names
first_name = user_data['first_name']
```

## README Templates

### Library/Package README
```markdown
# Package Name

[![npm version](https://badge.fury.io/js/package-name.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

Brief description of what this library does and why someone would use it.

## Features

- ✅ Feature one with brief description
- ✅ Feature two with brief description
- ✅ Feature three with brief description

## Installation

```bash
npm install package-name
```

## Quick Start

```javascript
import { something } from 'package-name';

const result = something('hello');
console.log(result); // Output: 'HELLO'
```

## Documentation

For full documentation, visit [docs site](https://docs.example.com).

## Contributing

Pull requests are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

MIT © [Author Name](https://github.com/author)
```

### CLI Tool README
```markdown
# Tool Name

One-line description of what this CLI tool does.

## Installation

```bash
# Via npm
npm install -g tool-name

# Via Homebrew
brew install tool-name

# Via binary
curl -fsSL https://get.tool-name.com | sh
```

## Usage

```bash
tool-name [command] [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a new project |
| `build` | Build the project |
| `deploy` | Deploy to production |

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `-v, --verbose` | false | Show detailed output |
| `-c, --config` | config.json | Path to config file |
| `--dry-run` | false | Preview without executing |

### Examples

```bash
# Initialize a new project
tool-name init my-project

# Build with verbose output
tool-name build --verbose

# Deploy to staging
tool-name deploy --environment staging
```

## Configuration

Create a `config.json` file in your project root:

```json
{
  "option1": "value1",
  "option2": true
}
```

## Troubleshooting

**Error: Cannot find module**
- Make sure you ran `npm install`

**Error: Permission denied**
- Run with `sudo` or fix permissions

## License

MIT
```

## Changelog Best Practices

### Semantic Versioning Changelog
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature that was added

## [2.0.0] - 2024-01-15

### Added
- Feature A with brief description
- Feature B with brief description

### Changed
- Updated dependency X to v2.0
- Improved performance of slow operation

### Deprecated
- Old API endpoint (will be removed in 3.0)

### Removed
- Legacy support for Node 14

### Fixed
- Bug where X happened when Y
- Memory leak in long-running processes

### Security
- Fixed vulnerability CVE-2024-XXXX

## [1.9.0] - 2024-01-01

...

[Unreleased]: https://github.com/user/repo/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/user/repo/compare/v1.9.0...v2.0.0
[1.9.0]: https://github.com/user/repo/releases/tag/v1.9.0
```

## When to Use This Skill

**Trigger Phrases:**
- "Document this code..."
- "Write a README for..."
- "Add comments to..."
- "Explain how this works..."
- "Create API documentation..."
- "Help me write an ADR..."
- "What should the docs include?"
- "Generate docstrings for..."

**Example Requests:**
1. "Write a README for this project"
2. "Add docstrings to these functions"
3. "Document this REST API"
4. "Create an ADR for our database choice"
5. "Improve the inline comments"
6. "Generate a CONTRIBUTING.md file"

## Documentation Review Checklist

Before publishing documentation:

- [ ] **Accurate?** Does it match current behavior?
- [ ] **Complete?** Are all important topics covered?
- [ ] **Clear?** Can the target audience understand it?
- [ ] **Tested?** Did you try following your own instructions?
- [ ] **Findable?** Can readers locate what they need?
- [ ] **Maintained?** Is there a plan to keep it current?
- [ ] **Accessible?** Is it readable for all audiences?

## Integration with Other Skills

- **Architect**: Document architectural decisions
- **Reviewer**: Documentation quality in code review
- **Refactorer**: Update docs when code changes
- **Tester**: Document test strategies and coverage

---

*Skill designed for Thanos + Antigravity integration*
