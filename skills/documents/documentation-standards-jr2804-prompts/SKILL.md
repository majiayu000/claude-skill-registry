---
name: documentation-standards
description: Universal documentation standards and best practices for software projects
license: MIT
compatibility: opencode
metadata:
  related_coding_principles: For overall development standards, use skill `coding-principles`
  related_python_guidelines: For Python-specific documentation, use skill `python-guidelines`
---

# Documentation Standards

## What I Do

Provide universal documentation standards and best practices that apply across different projects and domains.

## Universal Documentation Structure

### Documentation Organization

```text
# Universal documentation structure
docs/
├── README.md                    # Project overview
├── architecture/                # System architecture
│   ├── overview.md              # High-level architecture
│   └── components/              # Component details
├── development/                 # Development guidelines
│   ├── setup.md                 # Development environment
│   ├── workflow.md              # Development workflow
│   └── standards.md             # Coding standards
├── api/                         # API documentation
│   ├── reference.md             # API reference
│   └── examples.md              # Usage examples
└── user/                        # User documentation
    ├── getting-started.md       # Quick start guide
    ├── tutorials/               # Step-by-step tutorials
    └── reference/               # Detailed reference
````

### Documentation Formats

**Universal Documentation Standards:**

- **Markdown**: For most documentation (`.md` files)
- **Google Docstrings**: For Python code documentation
- **JSDoc**: For JavaScript/TypeScript documentation
- **Swagger/OpenAPI**: For API documentation

````markdown
# Universal Markdown Standards

## Headings
- Use ATX-style headings (#, ##, ###)
- Maintain consistent heading hierarchy
- Limit to 3-4 heading levels

## Code Blocks
```python
# Always specify language for syntax highlighting
def example_function():
    """Example with proper formatting"""
    return "formatted code"
```

## Lists
- Use consistent list formatting
- Prefer hyphens for bullet points
- Use numbered lists for sequential steps

## Links
- Use relative links for internal references
- Use absolute links for external references
- Include link descriptions
````

## When to Use Me

Use this skill when:

- Setting up documentation for new projects
- Standardizing documentation across teams
- Creating reusable documentation patterns
- Implementing maintainable documentation processes

## Universal Documentation Examples

### API Documentation

````markdown
# Universal API Documentation Template

## Endpoint: `/api/v1/resource`

**Method:** `GET`

**Description:** Retrieve resource information

**Parameters:**
- `id` (string, required): Resource identifier
- `format` (string, optional): Response format (json, xml)

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime",
  "status": "string"
}
```

**Examples:**
```bash
# Request example
curl -X GET "https://api.example.com/v1/resource?id=123&format=json"

# Response example
{
  "id": "123",
  "name": "Sample Resource",
  "created_at": "2023-01-01T00:00:00Z",
  "status": "active"
}
````

```

### Code Documentation

```python
# Universal Python docstring template
class DataProcessor:
    """Process and transform data for analysis.

    This class provides methods for cleaning, normalizing, and
    transforming raw data into analysis-ready formats.

    Attributes:
        config (dict): Configuration parameters for processing
        logger (Logger): Logger instance for tracking operations
    """

    def __init__(self, config=None):
        """Initialize DataProcessor with configuration.

        Args:
            config (dict, optional): Processing configuration.
                Defaults to default configuration.

        Raises:
            ValueError: If configuration is invalid
        """
        self.config = config or self._get_default_config()
        self.logger = self._setup_logger()
        self._validate_config()
```

### Tutorial Documentation

````markdown
# Universal Tutorial Template

## Tutorial: Getting Started with [Feature]

### Prerequisites

- Basic understanding of [related concept]
- [Software] version [version] installed
- Access to [required resources]

### Step 1: Setup
1. Install required dependencies

  ```bash
  pip install required-package
  ```

2. Configure your environment

  ```bash
  export ENV_VAR=value
  ```

### Step 2: Basic Usage
1. Import the module

  ```python
  from package import Module
  ```

2. Create an instance

  ```python
  processor = Module(config)
  ```

### Step 3: Advanced Features
1. Configure advanced options

  ```python
  processor.configure_advanced(option=value)
  ```

2. Process data

  ```python
  result = processor.process(data)
  ```

### Troubleshooting

- **Issue**: Common problem description
  **Solution**: Step-by-step resolution
- **Issue**: Another common problem
  **Solution**: Alternative approach
````

## Best Practices

1. **Consistency**: Apply same documentation standards across projects
2. **Maintainability**: Keep documentation up-to-date with code
3. **Accessibility**: Make documentation easy to find and navigate
4. **Completeness**: Document all public APIs and user-facing features

## Compatibility

Applies to:

- All software projects
- Any documentation system
- Cross-project standardization
- Organizational knowledge management
