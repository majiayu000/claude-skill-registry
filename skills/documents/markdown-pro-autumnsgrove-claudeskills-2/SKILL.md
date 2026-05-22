---
name: markdown-pro
description: "Professional Markdown documentation skill for creating polished README files, changelogs, contribution guides, and technical documentation. Use for: (1) README generation with badges and sections, (2) Automated changelog from git history, (3) Table of contents generation, (4) Contribution guidelines, (5) Technical documentation formatting, (6) Code documentation with syntax highlighting"
---

# Professional Markdown Documentation

## Overview

This skill provides comprehensive guidance for creating professional, well-structured Markdown documentation. It covers README files, changelogs, contribution guides, and technical documentation with modern formatting, badges, and best practices.

## Core Capabilities

### README Generation
- Project overview and description
- Installation instructions
- Usage examples with code blocks
- API documentation
- Badges and shields
- Feature highlights
- Screenshots and demos

### Changelog Automation
- Semantic versioning format
- Git history parsing
- Automated release notes
- Breaking changes highlighting
- Contributor attribution

### Technical Documentation
- Clear section hierarchy
- Code syntax highlighting
- API reference formatting
- Table of contents
- Cross-referencing
- Collapsible sections

## README Structure Best Practices

### Essential Sections

**1. Header with Badges**
```markdown
# Project Name

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](releases)
[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)](builds)

Brief one-line description of what the project does.
```

**2. Table of Contents** (for longer READMEs)
```markdown
## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
```

**3. Features Section**
```markdown
## Features

- **Feature 1**: Clear description with benefits
- **Feature 2**: What problems it solves
- **Feature 3**: Unique selling points
- Cross-platform support (Windows, macOS, Linux)
- Comprehensive test coverage (>90%)
```

**4. Installation Instructions**
```markdown
## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

```bash
pip install package-name
```

### From Source

```bash
git clone https://github.com/username/repo.git
cd repo
pip install -e .
```
```

**5. Usage Examples**
```markdown
## Usage

### Basic Example

```python
from package import Module

# Initialize
client = Module(api_key="your-key")

# Perform operation
result = client.process(data)
print(result)
```

### Advanced Usage

See [examples/](examples/) directory for more detailed use cases.
```

**6. API Documentation**
```markdown
## API Reference

### `Module.process(data, options=None)`

Process input data with optional configuration.

**Parameters:**
- `data` (str|dict): Input data to process
- `options` (dict, optional): Configuration options
  - `verbose` (bool): Enable verbose output (default: False)
  - `format` (str): Output format - 'json', 'yaml', 'xml' (default: 'json')

**Returns:**
- `dict`: Processed results with metadata

**Raises:**
- `ValueError`: If data is invalid
- `APIError`: If API request fails

**Example:**
```python
result = client.process(
    data={"key": "value"},
    options={"verbose": True, "format": "json"}
)
```
```

**7. Contributing Section**
```markdown
## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
```

**8. License and Credits**
```markdown
## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to [Contributor Name] for feature X
- Inspired by [Project Name](link)
- Built with [Technology Stack]
```

## Changelog Format

### Semantic Versioning Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Modification to existing feature

### Deprecated
- Features that will be removed

### Removed
- Deleted features

### Fixed
- Bug fixes

### Security
- Security improvements

## [1.2.0] - 2025-01-15

### Added
- User authentication system (#123)
- Export to CSV functionality (#145)
- Dark mode support (#156)

### Changed
- Updated UI components for better responsiveness (#134)
- Improved error messages (#142)

### Fixed
- Fixed memory leak in background processor (#139)
- Resolved login timeout issue (#148)

## [1.1.0] - 2024-12-01

### Added
- Initial release with core features
```

## Markdown Formatting Best Practices

### Code Blocks with Syntax Highlighting

```markdown
```python
def hello_world():
    """Print hello world message."""
    print("Hello, World!")
```

```javascript
function helloWorld() {
    console.log("Hello, World!");
}
```

```bash
# Install dependencies
npm install

# Run tests
npm test
```
```

### Tables

```markdown
| Feature | Description | Status |
|---------|-------------|--------|
| Auth | User authentication | ✅ Complete |
| API | RESTful API endpoints | ✅ Complete |
| Docs | Documentation | 🚧 In Progress |
| Tests | Unit & Integration | ❌ Planned |
```

### Collapsible Sections

```markdown
<details>
<summary>Click to expand advanced configuration</summary>

## Advanced Options

Configure advanced settings:

```yaml
advanced:
  cache_size: 1000
  timeout: 30
  retry_attempts: 3
```

</details>
```

### Alert Boxes

```markdown
> **Note**: This feature requires Python 3.8 or higher.

> **Warning**: This operation is irreversible!

> **Important**: Always backup your data before upgrading.
```

### Links and References

```markdown
<!-- External link -->
[Documentation](https://docs.example.com)

<!-- Internal link -->
See [Installation](#installation) section.

<!-- Reference-style links -->
Check out [project homepage][homepage] and [documentation][docs].

[homepage]: https://example.com
[docs]: https://docs.example.com
```

### Images

```markdown
<!-- Standard image -->
![Project Logo](assets/logo.png)

<!-- Image with alt text and title -->
![Dashboard Screenshot](screenshots/dashboard.png "Main Dashboard View")

<!-- Linked image -->
[![Demo Video](thumbnail.jpg)](https://youtube.com/watch?v=example)
```

## Badge Creation

### Common Badge Patterns

```markdown
<!-- License -->
![License](https://img.shields.io/badge/license-MIT-blue.svg)

<!-- Version -->
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

<!-- Build Status -->
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)

<!-- Coverage -->
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)

<!-- Language -->
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

<!-- Platform -->
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey.svg)
```

## Helper Scripts

### Generate Table of Contents

Use the helper script to automatically generate TOC from headers:

```bash
python scripts/markdown_helper.py toc README.md
```

### Generate Changelog from Git

Automatically create changelog entries from git history:

```bash
python scripts/markdown_helper.py changelog --since v1.0.0 --output CHANGELOG.md
```

### Validate Markdown Links

Check for broken links in documentation:

```bash
python scripts/markdown_helper.py validate docs/
```

## Templates

### Professional README Template

See `examples/README_template.md` for a complete, production-ready README template with all recommended sections.

### Changelog Template

See `examples/CHANGELOG_template.md` for a properly formatted changelog following Keep a Changelog format.

### Contributing Guidelines

See `examples/CONTRIBUTING.md` for contributor guidelines template including code of conduct, development setup, and PR process.

## Best Practices Summary

### Do's
- Use clear, descriptive headers
- Include code examples for every major feature
- Add badges for quick project status overview
- Keep line length under 100 characters for readability
- Use syntax highlighting for code blocks
- Include table of contents for documents >300 lines
- Add alt text for all images
- Link to related documentation

### Don'ts
- Don't use generic titles like "My Project"
- Don't include wall-of-text paragraphs (break into sections)
- Don't forget to update changelog with releases
- Don't use bare URLs (always use descriptive link text)
- Don't mix heading styles (use consistent hierarchy)
- Don't include screenshots without descriptions
- Don't hardcode version numbers everywhere (use variables/badges)

## Quick Reference

### Header Hierarchy
```markdown
# H1 - Project Title (only one per document)
## H2 - Major Sections
### H3 - Subsections
#### H4 - Minor Points
##### H5 - Rare, for deep nesting
```

### List Formatting
```markdown
<!-- Unordered -->
- Item 1
- Item 2
  - Nested item
  - Another nested item

<!-- Ordered -->
1. First step
2. Second step
3. Third step

<!-- Task list -->
- [x] Completed task
- [ ] Pending task
- [ ] Another pending task
```

### Emphasis
```markdown
*italic* or _italic_
**bold** or __bold__
***bold italic*** or ___bold italic___
~~strikethrough~~
`inline code`
```

## Conclusion

Professional Markdown documentation improves project accessibility, attracts contributors, and provides clear guidance for users. Use the templates in `examples/` as starting points, customize with the helper scripts in `scripts/`, and follow these best practices for polished, maintainable documentation.
