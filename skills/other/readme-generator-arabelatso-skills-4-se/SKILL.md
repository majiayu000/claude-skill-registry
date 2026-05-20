---
name: readme-generator
description: Generate comprehensive, user-friendly README.md files for code repositories. Use when creating documentation for new projects, updating existing READMEs, or improving project onboarding. Produces READMEs with project introduction, prerequisites, environment setup, executable usage instructions, and repository structure overview. Supports application projects, libraries, and research codebases.
---

# README Generator

## Overview

Analyze a code repository and generate a comprehensive, reproducible README.md that enables users to quickly understand, set up, and use the project with clear instructions and executable examples.

## Workflow

### 1. Analyze Repository Structure

Explore the repository to understand its organization and purpose:

**Key files to examine**:
- `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` - Project metadata
- `requirements.txt`, `Pipfile`, `pom.xml`, `build.gradle` - Dependencies
- Main entry points (`main.py`, `index.js`, `app.py`, `cmd/main.go`)
- Configuration files (`.env.example`, `config.yaml`, `settings.py`)
- Build/task files (`Makefile`, `package.json` scripts, `tasks.py`)
- Documentation (`docs/`, existing `README.md`, `CONTRIBUTING.md`)

**Information to extract**:
- Project name and version
- Programming language(s) and frameworks
- Project type (application, library, CLI tool, research)
- Main features and capabilities
- Dependencies and system requirements
- Entry points and execution methods

### 2. Generate Project Introduction

Create a clear, compelling introduction section:

**Title and badges**:
```markdown
# Project Name

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Language](https://img.shields.io/badge/python-3.9+-blue.svg)
```

**Description** (2-4 sentences):
- What the project does
- Why it exists (problem it solves)
- Key features or capabilities
- Target audience or use cases

**Example**:
```markdown
## About

[Project Name] is a lightweight web framework for building RESTful APIs with minimal boilerplate. It provides automatic request validation, built-in authentication, and OpenAPI documentation generation. Designed for rapid prototyping and production-ready microservices, it reduces API development time by 50% compared to traditional frameworks.
```

### 3. Document Prerequisites

List all system requirements and dependencies:

**Format**:
```markdown
## Prerequisites

Before you begin, ensure you have the following installed:

- **[Language/Runtime]**: [Version] or higher
  - Download: [URL]
  - Verify: `[command] --version`

- **[Package Manager]**: [Version] or higher
  - Download: [URL]
  - Verify: `[command] --version`

- **[Database/Service]** (optional): [Version]
  - Required for: [specific features]
  - Download: [URL]

- **[System Dependencies]**: [List]
  - Install on macOS: `brew install [packages]`
  - Install on Ubuntu: `sudo apt-get install [packages]`
  - Install on Windows: [instructions]
```

**Include**:
- Minimum versions for all dependencies
- Installation links or commands
- Verification commands to check installation
- Optional vs. required dependencies
- Platform-specific requirements

### 4. Write Installation/Setup Instructions

Provide step-by-step setup instructions that are reproducible:

**Format**:
```markdown
## Installation

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/username/project-name.git
cd project-name
\`\`\`

### 2. Install dependencies

\`\`\`bash
# For Python projects
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# For Node.js projects
npm install

# For Go projects
go mod download
\`\`\`

### 3. Configure environment

\`\`\`bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Required variables:
#   DATABASE_URL=postgresql://localhost/dbname
#   API_KEY=your_api_key_here
\`\`\`

### 4. Initialize database (if applicable)

\`\`\`bash
# Run migrations
npm run migrate
# Or: python manage.py migrate
# Or: make migrate
\`\`\`

### 5. Verify installation

\`\`\`bash
# Run tests to verify setup
npm test
# Or: pytest
# Or: go test ./...
\`\`\`
```

**Best practices**:
- Number each step clearly
- Provide exact commands that can be copy-pasted
- Include platform-specific variations
- Add comments explaining what each command does
- Include verification steps

### 5. Create Usage Instructions

Document how to run and use the project with executable examples:

**For applications**:
```markdown
## Usage

### Running the application

\`\`\`bash
# Development mode with hot reload
npm run dev

# Production mode
npm start

# With custom port
PORT=8080 npm start
\`\`\`

The application will be available at `http://localhost:3000`

### Basic operations

**Create a new resource**:
\`\`\`bash
curl -X POST http://localhost:3000/api/resources \
  -H "Content-Type: application/json" \
  -d '{"name": "example", "value": 42}'
\`\`\`

**List all resources**:
\`\`\`bash
curl http://localhost:3000/api/resources
\`\`\`
```

**For libraries**:
```markdown
## Usage

### Basic example

\`\`\`python
from project_name import Client

# Initialize client
client = Client(api_key="your_key")

# Perform operation
result = client.fetch_data(query="example")
print(result)
\`\`\`

### Advanced usage

\`\`\`python
# With custom configuration
client = Client(
    api_key="your_key",
    timeout=30,
    retry_count=3
)

# Batch operations
results = client.batch_fetch([
    {"query": "item1"},
    {"query": "item2"}
])
\`\`\`
```

**For CLI tools**:
```markdown
## Usage

### Basic commands

\`\`\`bash
# Show help
project-cli --help

# Run with default options
project-cli process input.txt

# Run with custom options
project-cli process input.txt --output result.txt --verbose
\`\`\`

### Common workflows

**Workflow 1: Data processing**
\`\`\`bash
# Step 1: Validate input
project-cli validate data.csv

# Step 2: Process data
project-cli process data.csv --format json

# Step 3: Export results
project-cli export results.json --format pdf
\`\`\`
```

### 6. Generate Repository Structure

Create a visual directory tree showing the codebase organization:

**Format**:
```markdown
## Repository Structure

\`\`\`
project-name/
├── src/                    # Source code
│   ├── api/               # API endpoints
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docs/                  # Documentation
├── scripts/               # Build and deployment scripts
├── config/                # Configuration files
├── .env.example          # Environment variables template
├── package.json          # Project dependencies
├── README.md             # This file
└── LICENSE               # License information
\`\`\`

### Key directories

- **src/api**: REST API endpoints and route handlers
- **src/models**: Database models and schemas
- **src/services**: Core business logic and external integrations
- **tests**: Comprehensive test suite with >80% coverage
- **docs**: Additional documentation and API specifications
```

**Best practices**:
- Show 2-3 levels of directory depth
- Add comments explaining each major directory
- Highlight important files
- Include a "Key directories" section with descriptions
- Keep it concise (don't list every file)

### 7. Add Additional Sections

Include other helpful sections as appropriate:

**Configuration**:
```markdown
## Configuration

The application can be configured via environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `API_KEY` | External API key | - | Yes |
| `PORT` | Server port | 3000 | No |
| `LOG_LEVEL` | Logging level (debug/info/error) | info | No |
```

**Development**:
```markdown
## Development

### Running tests

\`\`\`bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- tests/api.test.js
\`\`\`

### Code formatting

\`\`\`bash
# Check formatting
npm run lint

# Auto-fix issues
npm run lint:fix
\`\`\`
```

**Troubleshooting**:
```markdown
## Troubleshooting

### Common issues

**Issue**: `ModuleNotFoundError: No module named 'xyz'`
**Solution**: Ensure virtual environment is activated and dependencies are installed:
\`\`\`bash
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

**Issue**: Database connection fails
**Solution**: Verify DATABASE_URL in .env and ensure PostgreSQL is running:
\`\`\`bash
pg_isready
\`\`\`
```

**License and Contributing**:
```markdown
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.
```

## README Quality Guidelines

**Clarity**:
- Use simple, direct language
- Avoid jargon unless necessary
- Define technical terms on first use
- Use active voice

**Completeness**:
- Include all steps needed to go from clone to running
- Don't assume prior knowledge
- Provide examples for common use cases
- Link to additional documentation

**Reproducibility**:
- All commands should be copy-pastable
- Include exact versions
- Specify environment variables
- Document platform differences

**Maintainability**:
- Keep instructions up to date with code
- Use relative links for internal docs
- Version badge should match actual version
- Test instructions on clean environment

## Tips

- Test all commands in a fresh environment before finalizing
- Use code blocks with language syntax highlighting
- Include screenshots for UI-heavy projects
- Add a table of contents for long READMEs
- Link to detailed docs for complex topics
- Keep the README focused on getting started
- Update version badges when releasing
- Include a "Quick Start" section at the top for experienced users
