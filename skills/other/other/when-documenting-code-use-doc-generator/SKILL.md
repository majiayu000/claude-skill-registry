---
name: when-documenting-code-use-doc-generator
version: 1.0.0
description: Automated comprehensive code documentation generation with API docs, README files, inline comments, and architecture diagrams
triggers:
  - "generate documentation"
  - "create API docs"
  - "write README"
  - "add comments"
  - "document this code"
agents:
  - code-analyzer
  - base-template-generator
complexity: medium
tags: [documentation, api-docs, readme, comments, diagrams, automation]
---

# When Documenting Code - Use Doc Generator

## Overview

This skill provides automated, comprehensive documentation generation for codebases. It analyzes code structure, generates API documentation, creates README files, adds inline comments, and produces architecture diagrams using evidence-based documentation patterns.

## Core Capabilities

1. **Code Analysis**: Extract APIs, functions, classes, types, and dependencies
2. **API Documentation**: Generate OpenAPI, JSDoc, TypeDoc, and Python docstrings
3. **README Generation**: Create comprehensive project documentation
4. **Inline Comments**: Add missing documentation with context-aware comments
5. **Diagram Generation**: Produce architecture and flow diagrams (Graphviz, Mermaid)

## SPARC Methodology: Documentation Generation

### Phase 1: SPECIFICATION - Analyze Documentation Requirements

**Objective**: Understand the codebase structure and documentation needs

**Actions**:
1. Scan project structure and identify file types
2. Detect programming languages and frameworks
3. Identify existing documentation (README, API docs, comments)
4. Analyze documentation gaps and missing coverage
5. Determine documentation standards (JSDoc, TSDoc, Python docstrings)

**Deliverables**:
- Project structure analysis
- Documentation gap report
- Recommended documentation strategy
- Style guide selection

**Agent**: `code-analyzer`

**Example Analysis**:
```
Project: express-api-server
Languages: JavaScript (TypeScript), 85% | JSON 10% | Markdown 5%
Frameworks: Express.js, Jest
Current Documentation:
  - README.md: Exists (outdated, 3 months old)
  - API Docs: None
  - Inline Comments: 12% coverage
  - Type Definitions: 45% coverage

Gaps Identified:
  - ❌ No API documentation (12 endpoints undocumented)
  - ❌ Missing installation instructions
  - ❌ No architecture diagrams
  - ⚠️  Low inline comment coverage
  - ✅ Package.json well-documented

Recommended Strategy:
  1. Generate OpenAPI 3.0 spec for REST API
  2. Add JSDoc comments to all public functions
  3. Create comprehensive README with badges
  4. Generate architecture diagram (system overview)
  5. Add usage examples for main features
```

### Phase 2: PSEUDOCODE - Design Documentation Structure

**Objective**: Plan documentation hierarchy and templates

**Actions**:
1. Design documentation structure (README, API, guides)
2. Define comment style and conventions
3. Create templates for each documentation type
4. Plan diagram types and structure
5. Define metadata and frontmatter standards

**Deliverables**:
- Documentation structure outline
- Template designs for each type
- Comment convention guide
- Diagram specifications

**Example Structure**:
```
Documentation Hierarchy:

docs/
├── README.md                 # Project overview
├── INSTALLATION.md          # Setup guide
├── API.md                   # API reference
├── ARCHITECTURE.md          # System design
├── CONTRIBUTING.md          # Contribution guide
├── diagrams/
│   ├── system-overview.svg  # High-level architecture
│   ├── data-flow.svg        # Data flow diagram
│   └── api-endpoints.svg    # API structure
└── examples/
    ├── basic-usage.md
    └── advanced-features.md

Comment Standards:
- JSDoc for all exported functions
- TypeDoc for TypeScript interfaces
- File header with purpose and author
- Inline comments for complex logic only

API Documentation:
- OpenAPI 3.0 specification
- Example requests/responses
- Error code documentation
- Authentication guide
```

### Phase 3: ARCHITECTURE - Define Generation Pipeline

**Objective**: Design the documentation generation workflow

**Actions**:
1. Define code parsing strategy (AST, regex, static analysis)
2. Design template engine for documentation generation
3. Plan diagram generation pipeline (Graphviz/Mermaid)
4. Define validation and quality checks
5. Create update and versioning strategy

**Deliverables**:
- Documentation generation pipeline
- Parser and extractor design
- Template rendering engine
- Validation rules

**Pipeline Architecture**:
```
┌─────────────────┐
│  Source Code    │
│  Repository     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Code Analyzer          │
│  - AST Parsing          │
│  - Extract Functions    │
│  - Extract Types        │
│  - Detect Patterns      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Documentation Engine   │
│  ├─ API Generator       │
│  ├─ README Generator    │
│  ├─ Comment Generator   │
│  └─ Diagram Generator   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Template Renderer      │
│  - Mustache/Handlebars  │
│  - Markdown Formatting  │
│  - Syntax Highlighting  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Validator              │
│  - Link Checking        │
│  - Spelling             │
│  - Completeness         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Output                 │
│  - docs/                │
│  - Inline Comments      │
│  - Generated Diagrams   │
└─────────────────────────┘
```

### Phase 4: REFINEMENT - Generate and Validate Documentation

**Objective**: Execute documentation generation with quality checks

**Actions**:
1. Parse source code and extract documentation targets
2. Generate API documentation from code signatures
3. Create README from templates and project metadata
4. Add inline comments to undocumented code
5. Generate architecture and flow diagrams
6. Validate completeness and accuracy
7. Check links and references
8. Format and style according to standards

**Deliverables**:
- Complete API documentation
- Comprehensive README
- Inline code comments
- Architecture diagrams
- Validation report

**Generation Examples**:

**Before (Undocumented Function)**:
```javascript
function calculateDiscount(price, customerType, quantity) {
  const baseDiscount = customerType === 'premium' ? 0.15 : 0.05;
  const volumeDiscount = quantity > 100 ? 0.1 : quantity > 50 ? 0.05 : 0;
  return price * (1 - baseDiscount - volumeDiscount);
}
```

**After (With JSDoc)**:
```javascript
/**
 * Calculates the final price after applying customer and volume discounts
 *
 * @param {number} price - The original price before discounts
 * @param {('standard'|'premium')} customerType - Customer tier level
 * @param {number} quantity - Number of items purchased
 * @returns {number} The discounted price
 *
 * @example
 * // Premium customer buying 60 items at $100 each
 * calculateDiscount(100, 'premium', 60);
 * // Returns: 80 (15% customer + 5% volume discount)
 *
 * @see {@link https://docs.example.com/pricing|Pricing Documentation}
 */
function calculateDiscount(price, customerType, quantity) {
  // Premium customers receive 15% base discount, standard customers 5%
  const baseDiscount = customerType === 'premium' ? 0.15 : 0.05;

  // Volume discounts: 10% for 100+, 5% for 50+, 0% otherwise
  const volumeDiscount = quantity > 100 ? 0.1 : quantity > 50 ? 0.05 : 0;

  return price * (1 - baseDiscount - volumeDiscount);
}
```

**API Documentation Generation**:
```yaml
# Generated OpenAPI 3.0 Specification
openapi: 3.0.0
info:
  title: E-commerce API
  version: 1.0.0
  description: REST API for e-commerce platform with pricing and inventory

paths:
  /api/v1/products/{id}/price:
    get:
      summary: Calculate product price with discounts
      description: Returns the final price after applying customer tier and volume discounts
      operationId: calculateProductPrice
      tags:
        - Pricing
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          description: Product ID
        - name: quantity
          in: query
          required: true
          schema:
            type: integer
            minimum: 1
          description: Quantity to purchase
        - name: customerType
          in: query
          required: false
          schema:
            type: string
            enum: [standard, premium]
            default: standard
          description: Customer tier level
      responses:
        '200':
          description: Price calculated successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  originalPrice:
                    type: number
                    example: 100.00
                  discountedPrice:
                    type: number
                    example: 80.00
                  discountsApplied:
                    type: array
                    items:
                      type: object
                      properties:
                        type:
                          type: string
                          enum: [customer, volume]
                        percentage:
                          type: number
                          example: 0.15
        '404':
          description: Product not found
```

**README Generation**:
```markdown
# E-commerce API Server

[![Build Status](https://img.shields.io/travis/org/repo.svg)](https://travis-ci.org/org/repo)
[![Coverage](https://img.shields.io/codecov/c/github/org/repo.svg)](https://codecov.io/gh/org/repo)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Production-ready REST API for e-commerce platform with advanced pricing, inventory management, and order processing.

## Features

- ✅ Dynamic pricing with customer tiers and volume discounts
- ✅ Real-time inventory tracking
- ✅ Order processing and fulfillment
- ✅ JWT authentication with role-based access
- ✅ Rate limiting and security middleware
- ✅ Comprehensive API documentation (OpenAPI 3.0)

## Quick Start

### Prerequisites

- Node.js >= 18.0.0
- PostgreSQL >= 14.0
- Redis >= 7.0 (for caching)

### Installation

```bash
# Clone repository
git clone https://github.com/org/ecommerce-api.git
cd ecommerce-api

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
npm run migrate

# Start server
npm start
```

### Usage

```javascript
// Example: Calculate price with discounts
const response = await fetch(
  'http://localhost:3000/api/v1/products/prod-123/price?quantity=60&customerType=premium'
);
const { discountedPrice } = await response.json();
console.log(`Final price: $${discountedPrice}`);
```

## API Documentation

Full API documentation available at:
- **Interactive Docs**: http://localhost:3000/api-docs (Swagger UI)
- **OpenAPI Spec**: [docs/API.md](docs/API.md)

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/products` | List all products |
| GET | `/api/v1/products/{id}` | Get product details |
| GET | `/api/v1/products/{id}/price` | Calculate price with discounts |
| POST | `/api/v1/orders` | Create new order |
| GET | `/api/v1/orders/{id}` | Get order status |

## Architecture

![System Architecture](docs/diagrams/system-overview.svg)

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 3000 |
| `DATABASE_URL` | PostgreSQL connection | - |
| `REDIS_URL` | Redis connection | - |
| `JWT_SECRET` | Authentication secret | - |

## Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run integration tests
npm run test:integration
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT © 2025 Your Organization
```

### Phase 5: COMPLETION - Integrate and Maintain Documentation

**Objective**: Ensure documentation stays synchronized with code

**Actions**:
1. Integrate documentation into build pipeline
2. Set up automated documentation updates
3. Configure pre-commit hooks for comment validation
4. Establish documentation review process
5. Create documentation maintenance schedule

**Deliverables**:
- CI/CD integration
- Git hooks for documentation
- Maintenance schedule
- Documentation metrics dashboard

**Integration Strategy**:
```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Generate API documentation
        run: npm run docs:api

      - name: Generate diagrams
        run: npm run docs:diagrams

      - name: Validate documentation
        run: npm run docs:validate

      - name: Check comment coverage
        run: npm run docs:coverage

      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

**Pre-commit Hook**:
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking documentation coverage..."

# Check for undocumented functions
undocumented=$(npm run --silent docs:check-coverage)

if [ $? -ne 0 ]; then
  echo "❌ Documentation coverage below threshold"
  echo "$undocumented"
  echo ""
  echo "Please add documentation to new functions before committing."
  exit 1
fi

echo "✅ Documentation coverage acceptable"
```

## Usage Patterns

### Basic Documentation Generation

```bash
# Generate all documentation
/doc-generate

# Generate specific documentation type
/doc-api          # API documentation only
/doc-readme       # README generation only
/doc-inline       # Add inline comments only
/doc-diagrams     # Generate diagrams only
```

### Advanced Usage

```bash
# Generate with specific output format
npx claude-flow docs generate --format openapi --output docs/api.yml

# Generate for specific files
npx claude-flow docs generate --files "src/**/*.js" --type jsdoc

# Generate with custom templates
npx claude-flow docs generate --template custom-readme.hbs

# Update existing documentation
npx claude-flow docs update --incremental

# Validate documentation completeness
npx claude-flow docs validate --min-coverage 80
```

## Documentation Standards

### Comment Style Guide

**JavaScript/TypeScript (JSDoc)**:
```javascript
/**
 * Brief description (one sentence, under 100 chars)
 *
 * Detailed description explaining the purpose, behavior, and any
 * important considerations. This can span multiple lines.
 *
 * @param {Type} paramName - Description of parameter
 * @param {Type} [optionalParam=defaultValue] - Optional parameter
 * @returns {Type} Description of return value
 * @throws {ErrorType} When error occurs
 *
 * @example
 * // Example usage
 * const result = functionName(arg1, arg2);
 *
 * @see {@link RelatedFunction}
 * @since 1.0.0
 * @deprecated Use newFunction instead
 */
```

**Python (Google Style)**:
```python
def function_name(param1: str, param2: int = 0) -> bool:
    """Brief description (one sentence).

    Detailed description explaining the purpose and behavior.
    Can span multiple lines with proper formatting.

    Args:
        param1: Description of first parameter
        param2: Description of optional parameter (default: 0)

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input provided
        RuntimeError: When operation fails

    Example:
        >>> result = function_name("test", 5)
        >>> print(result)
        True

    Note:
        Important information or limitations
    """
```

### README Template Structure

```markdown
# Project Title

> Brief description (one sentence tagline)

[Badges: Build, Coverage, License, Version]

## Features

- Key feature 1
- Key feature 2
- Key feature 3

## Quick Start

### Prerequisites
### Installation
### Basic Usage

## Documentation

- [API Reference](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Examples

### Basic Example
### Advanced Example

## Configuration

## Testing

## Deployment

## Support

## License
```

## Quality Metrics

**Documentation Coverage Goals**:
- Public API functions: 100% documented
- Internal functions: 80% documented
- Complex algorithms: 100% with inline comments
- Type definitions: 100% documented
- Examples: At least 1 per major feature

**Validation Checks**:
- ✅ All public functions have JSDoc/docstrings
- ✅ All parameters documented with types
- ✅ Return values documented
- ✅ Examples provided for complex functions
- ✅ Links valid and accessible
- ✅ No spelling errors
- ✅ Consistent formatting

## Troubleshooting

### Common Issues

**Issue**: Generated docs missing some functions
- **Solution**: Check function export syntax, ensure `export` keyword used

**Issue**: Diagrams not rendering
- **Solution**: Install Graphviz: `brew install graphviz` or `apt install graphviz`

**Issue**: JSDoc comments not showing in IDE
- **Solution**: Configure TypeScript to include JSDoc in `tsconfig.json`

**Issue**: README badges not updating
- **Solution**: Check CI/CD pipeline, verify badge URLs

## Best Practices

1. **Write documentation as you code** - Don't defer to later
2. **Keep comments concise** - Explain "why" not "what"
3. **Use examples liberally** - Show, don't just tell
4. **Update diagrams regularly** - Keep architecture docs current
5. **Validate before committing** - Use pre-commit hooks
6. **Review documentation in PRs** - Treat docs as first-class code
7. **Version documentation** - Tag docs with release versions
8. **Link related concepts** - Create documentation graph
9. **Avoid redundancy** - Single source of truth
10. **Test examples** - Ensure code samples actually work

## Integration with Other Skills

- **code-review-assistant**: Validates documentation in PRs
- **tdd-workflow**: Generates test documentation
- **api-design-first**: Creates API docs from specs
- **refactoring-assistant**: Updates docs during refactoring

## References

- [JSDoc Documentation](https://jsdoc.app/)
- [TypeDoc Documentation](https://typedoc.org/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Markdown Guide](https://www.markdownguide.org/)
- [Graphviz Documentation](https://graphviz.org/documentation/)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-30
**Maintainer**: Base Template Generator
**Status**: Production Ready
