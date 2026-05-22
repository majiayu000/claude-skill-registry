---
name: documentation
description: "Generate and maintain comprehensive documentation. Use when writing README, API docs, code comments, or technical documentation."
enabled: true
visibility: default
allowedTools: ["read", "write", "edit", "grep", "glob"]
---

# Documentation Skill

Create clear, comprehensive, and maintainable documentation for code projects.

## Documentation Types

### 1. README.md
**Purpose**: Project overview and quick start guide

**Essential Sections**:
```markdown
# Project Name

Brief description (1-2 sentences)

## Features
- Key feature 1
- Key feature 2

## Installation
```bash
npm install package-name
```

## Quick Start
```javascript
const lib = require('package-name');
lib.doSomething();
```

## Usage
[Detailed examples]

## API Reference
[Link to detailed API docs]

## Contributing
[How to contribute]

## License
MIT
```

---

### 2. Code Comments

**When to Comment**:
- ✅ Complex algorithms
- ✅ Non-obvious decisions
- ✅ Workarounds for bugs
- ✅ Public APIs
- ❌ Self-explanatory code
- ❌ What code does (code shows that)

**Good Comments**:
```python
# Calculate tax using 2024 progressive rates
# See: https://irs.gov/tax-rates-2024
def calculate_tax(income):
    # ...

# HACK: API returns string "null" instead of null
# TODO: Remove once API v2 is deployed
if response == "null":
    response = None
```

**Bad Comments**:
```python
# Increment i
i = i + 1  # Obvious from code

# This function adds two numbers
def add(a, b):  # Function name is clear
    return a + b
```

---

### 3. Function Documentation

**Python (Docstrings)**:
```python
def calculate_discount(price: float, discount_pct: float) -> float:
    """
    Calculate discounted price.

    Args:
        price: Original price in dollars
        discount_pct: Discount percentage (0-100)

    Returns:
        Final price after discount

    Raises:
        ValueError: If discount_pct is not between 0 and 100

    Examples:
        >>> calculate_discount(100, 20)
        80.0
    """
    if not 0 <= discount_pct <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_pct / 100)
```

**JavaScript (JSDoc)**:
```javascript
/**
 * Calculate discounted price
 * @param {number} price - Original price in dollars
 * @param {number} discountPct - Discount percentage (0-100)
 * @returns {number} Final price after discount
 * @throws {Error} If discountPct is not between 0 and 100
 * @example
 * calculateDiscount(100, 20) // Returns 80
 */
function calculateDiscount(price, discountPct) {
    if (discountPct < 0 || discountPct > 100) {
        throw new Error('Discount must be between 0 and 100');
    }
    return price * (1 - discountPct / 100);
}
```

---

### 4. API Documentation

**REST API Example**:
```markdown
## GET /api/users/:id

Retrieve user by ID.

### Parameters
- `id` (path, required): User ID

### Query Parameters
- `include` (optional): Comma-separated relations to include
  - Values: `profile`, `posts`, `comments`

### Response
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Status Codes
- `200 OK`: User found
- `404 Not Found`: User doesn't exist
- `401 Unauthorized`: Missing or invalid token

### Example
```bash
curl -H "Authorization: Bearer TOKEN" \
     https://api.example.com/api/users/123?include=profile
```
```

---

### 5. Architecture Documentation

**System Overview**:
```markdown
## Architecture

### High-Level Design
```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Client  │─────▶│   API    │─────▶│ Database │
└──────────┘      └──────────┘      └──────────┘
                        │
                        ▼
                  ┌──────────┐
                  │  Cache   │
                  └──────────┘
```

### Components

#### API Server
- **Technology**: Node.js + Express
- **Responsibility**: Handle HTTP requests, business logic
- **Scaling**: Horizontal (load balanced)

#### Database
- **Technology**: PostgreSQL 15
- **Responsibility**: Persistent data storage
- **Backup**: Daily automated backups

#### Cache
- **Technology**: Redis
- **Responsibility**: Session storage, API response cache
- **TTL**: 5 minutes for API responses
```

---

## Documentation Best Practices

### Writing Guidelines

1. **Be Clear and Concise**
   - Use simple language
   - Avoid jargon (or explain it)
   - Short sentences and paragraphs

2. **Use Examples**
   - Show don't just tell
   - Include common use cases
   - Provide working code samples

3. **Keep Updated**
   - Update docs with code changes
   - Mark deprecated features
   - Version documentation

4. **Structure Logically**
   - Start with overview
   - Organize by use case
   - Use clear headings

5. **Make Searchable**
   - Use descriptive headings
   - Include keywords
   - Add table of contents

### Format Tips

**Use Code Blocks**:
````markdown
```python
# Code here
```
````

**Use Tables**:
```markdown
| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| name      | string | yes      | User name   |
```

**Use Lists**:
```markdown
- Item 1
- Item 2
  - Sub-item 2.1
```

**Use Emphasis**:
```markdown
**Bold** for important terms
*Italic* for emphasis
`code` for inline code
```

---

## Documentation Templates

### README Template
```markdown
# Project Name

One-line description

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Features
- Feature 1
- Feature 2

## Installation

### Prerequisites
- Node.js 18+
- npm or yarn

### Steps
```bash
git clone https://github.com/user/repo.git
cd repo
npm install
```

## Usage

### Basic Example
```javascript
const lib = require('lib');
lib.doSomething();
```

### Advanced Example
[More complex usage]

## API Reference

See [API.md](./API.md) for detailed API documentation.

## Configuration

Create `.env` file:
```env
API_KEY=your_key
DATABASE_URL=postgresql://...
```

## Development

```bash
npm run dev        # Start dev server
npm test          # Run tests
npm run lint      # Lint code
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) file

## Contact

- GitHub: [@username](https://github.com/username)
- Email: email@example.com
```

### CHANGELOG Template
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- New feature X

### Changed
- Updated dependency Y

### Fixed
- Bug Z in component W

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Feature A
- Feature B

### Security
- Fixed vulnerability CVE-XXXX
```

### CONTRIBUTING Template
```markdown
# Contributing Guide

Thank you for contributing!

## Code of Conduct

Be respectful and inclusive.

## How to Contribute

### Reporting Bugs
- Check existing issues first
- Use bug report template
- Include reproduction steps
- Specify environment details

### Suggesting Features
- Check roadmap and existing requests
- Use feature request template
- Explain use case and benefits

### Pull Requests

#### Before Submitting
1. Fork and create branch
2. Follow coding standards
3. Add tests
4. Update documentation
5. Run linter and tests

#### PR Guidelines
- Clear description of changes
- Link related issues
- Keep changes focused
- Update CHANGELOG.md

## Development Setup

```bash
git clone https://github.com/user/repo.git
cd repo
npm install
npm run dev
```

## Testing

```bash
npm test              # Run all tests
npm run test:watch    # Watch mode
npm run test:coverage # Coverage report
```

## Code Style

- Follow ESLint configuration
- Use Prettier for formatting
- Write descriptive commit messages

## Commit Messages

Format: `type(scope): description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructure
- `test`: Tests
- `chore`: Maintenance

Example: `feat(auth): add password reset`
```

---

## Documentation Checklist

Before finalizing documentation:

- [ ] README exists and is complete
- [ ] Installation instructions clear
- [ ] Usage examples provided
- [ ] API documented (if applicable)
- [ ] Code has appropriate comments
- [ ] Complex logic explained
- [ ] Configuration documented
- [ ] Contributing guide exists
- [ ] License specified
- [ ] CHANGELOG maintained
- [ ] Links work correctly
- [ ] Code examples tested
- [ ] Spelling/grammar checked
- [ ] Formatting consistent

---

## Automation Tips

### Auto-Generate API Docs
```javascript
// JSDoc to Markdown
npm install -g jsdoc-to-markdown
jsdoc2md src/**/*.js > API.md
```

### Documentation Testing
```python
# Python: Test docstring examples
python -m doctest module.py

# Or use pytest
pytest --doctest-modules
```

### Keep Docs in Sync
```bash
# Pre-commit hook to check docs
#!/bin/bash
if git diff --cached --name-only | grep -q "^src/"; then
    if ! git diff --cached --name-only | grep -q "^docs/"; then
        echo "Warning: Code changed but docs not updated"
        exit 1
    fi
fi
```

---

## Remember

- Documentation is part of the code
- Good docs save time for everyone
- Update docs with every code change
- Write for your future self
- Examples are worth a thousand words
