---
name: querying-gemini
description: Queries Gemini 3 Flash for high-speed code analysis, generation, and complex coding questions. Provides P0-P3 prioritized analysis reports, architecture audits, and code generation with configurable thinking levels (minimal/low/medium/high). 1M context, 64K output. Pro-level intelligence at Flash pricing.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Querying Gemini 3 Flash

Queries Gemini 3 Flash for fast, intelligent code analysis, generation, and complex technical questions. Leverages Gemini 3 Flash's 1M token context window and configurable thinking levels to provide comprehensive analysis with P0-P3 prioritized findings.

## Quick Reference

Gemini 3 Flash provides four specialized capabilities via standalone scripts:

| Script | Purpose | Use Case |
|--------|---------|----------|
| `gemini_query.py` | General queries | Complex coding questions, algorithm design, concept explanations |
| `gemini_analyze.py` | Code analysis | Pre-merge reviews, architecture audits, security scans |
| `gemini_code.py` | Code generation | Generate production-ready code with best practices |
| `gemini_fix.py` | Root-cause fixes | Bug debugging that addresses underlying issues (not symptoms) |

**Key Features:**
- 1,000,000 token context window (analyze very large codebases)
- 64,000 token output limit (comprehensive responses)
- Configurable thinking levels (minimal/low/medium/high)
- Structured P0-P3 prioritization for findings
- Jan 2025 knowledge cutoff
- Pro-level intelligence at Flash pricing ($0.50/1M input, $3/1M output)

## Scripts

### gemini_query.py

General-purpose queries with configurable thinking levels.

**Usage:**
```bash
python .claude/skills/querying-gemini/scripts/gemini_query.py \
  --prompt "How should I implement retry logic with exponential backoff?" \
  --thinking-level high \
  --timeout 300 \
  --output-format markdown
```

**Arguments:**
| Argument | Required | Default | Values | Description |
|----------|----------|---------|--------|-------------|
| `--prompt` | Yes | - | string | The question or request |
| `--thinking-level` | No | high | minimal/low/medium/high | Thinking depth |
| `--timeout` | No | 300 | float | Max wait time in seconds |
| `--output-format` | No | markdown | markdown/json | Output format |

**Example:**
```bash
# Ask about Python async patterns
python .claude/skills/querying-gemini/scripts/gemini_query.py \
  --prompt "What are the best practices for handling asyncio.CancelledError?"

# Complex algorithm design
python .claude/skills/querying-gemini/scripts/gemini_query.py \
  --prompt "Design a rate limiter using token bucket algorithm" \
  --thinking-level high
```

### gemini_analyze.py

Comprehensive code analysis for single files or complete projects.

**Usage:**
```bash
python .claude/skills/querying-gemini/scripts/gemini_analyze.py \
  --target "app/core/" \
  --focus-areas "security,performance" \
  --analysis-type comprehensive \
  --timeout 600 \
  --output-format markdown
```

**Arguments:**
| Argument | Required | Default | Values | Description |
|----------|----------|---------|--------|-------------|
| `--target` | Yes | - | path | File or directory to analyze |
| `--focus-areas` | No | all | security/performance/architecture/testing/quality/all | Analysis dimensions (comma-separated) |
| `--analysis-type` | No | comprehensive | quick/comprehensive/deep | Analysis depth |
| `--timeout` | No | 600 | float | Max wait time in seconds |
| `--output-format` | No | markdown | markdown/json | Output format |

**Example:**
```bash
# Security audit of API endpoints
python .claude/skills/querying-gemini/scripts/gemini_analyze.py \
  --target "app/api/" \
  --focus-areas "security" \
  --analysis-type deep

# Quick quality check before merge
python .claude/skills/querying-gemini/scripts/gemini_analyze.py \
  --target "app/services/new_feature.py" \
  --analysis-type quick
```

### gemini_code.py

High-quality code generation with best practices.

**Usage:**
```bash
python .claude/skills/querying-gemini/scripts/gemini_code.py \
  --request "Implement a rate limiter using token bucket algorithm" \
  --language python \
  --context "FastAPI application with async support" \
  --thinking-level high \
  --timeout 300 \
  --output-format markdown
```

**Arguments:**
| Argument | Required | Default | Values | Description |
|----------|----------|---------|--------|-------------|
| `--request` | Yes | - | string | Description of code to generate |
| `--language` | No | - | string | Target programming language |
| `--context` | No | - | string | Additional context about requirements |
| `--thinking-level` | No | high | minimal/low/medium/high | Thinking depth |
| `--timeout` | No | 300 | float | Max wait time in seconds |
| `--output-format` | No | markdown | markdown/json | Output format |

**Example:**
```bash
# Generate a FastAPI endpoint
python .claude/skills/querying-gemini/scripts/gemini_code.py \
  --request "Create a REST endpoint for user authentication with JWT tokens" \
  --language python \
  --context "FastAPI with Pydantic models, SQLAlchemy ORM"

# Generate a React component
python .claude/skills/querying-gemini/scripts/gemini_code.py \
  --request "Create a responsive data table with sorting and pagination" \
  --language typescript \
  --context "React 18 with Tailwind CSS"
```

### gemini_fix.py

Root-cause bug fixing (NOT monkey patches).

**Usage:**
```bash
python .claude/skills/querying-gemini/scripts/gemini_fix.py \
  --target "app/api/endpoints.py" \
  --issues "TypeError: 'NoneType' object is not subscriptable on line 45 when session expires" \
  --fix-scope root_cause \
  --timeout 600 \
  --output-format markdown
```

**Arguments:**
| Argument | Required | Default | Values | Description |
|----------|----------|---------|--------|-------------|
| `--target` | Yes | - | path | File or directory containing the issue |
| `--issues` | Yes | - | string | Detailed problem description (include error messages, stack traces) |
| `--fix-scope` | No | root_cause | root_cause/minimal/comprehensive | Fix approach |
| `--timeout` | No | 600 | float | Max wait time in seconds |
| `--output-format` | No | markdown | markdown/json | Output format |

**Example:**
```bash
# Fix a concurrency bug
python .claude/skills/querying-gemini/scripts/gemini_fix.py \
  --target "app/core/session.py" \
  --issues "Race condition in session cleanup: multiple cleanup tasks running simultaneously causing KeyError"

# Fix with full stack trace
python .claude/skills/querying-gemini/scripts/gemini_fix.py \
  --target "app/services/" \
  --issues "$(cat error.log)" \
  --fix-scope comprehensive
```

## When to Use

Use this skill for tasks requiring fast, intelligent analysis:

### Code Analysis
- Pre-merge code reviews
- Architecture audits across multiple files
- Security vulnerability scanning
- Performance bottleneck identification
- Technical debt assessment

### Code Generation
- Generate boilerplate with best practices
- Create API endpoints and handlers
- Build UI components
- Implement algorithms and data structures

### Root-Cause Debugging
- Complex bugs requiring tracing through call chains
- Race conditions and concurrency issues
- Memory leaks or performance degradation
- Architectural flaws causing repeated issues

### Complex Questions
- Algorithm design and optimization
- Framework integration strategies
- Best practices for specific patterns
- Trade-off analysis for technical decisions

## When NOT to Use

Avoid this skill for:

- **Simple queries** - Use Claude directly for straightforward questions
- **Real-time streaming** - Gemini 3 Flash doesn't stream in this skill
- **Tasks requiring MCP tools** - Use standard Claude Code capabilities
- **Quick fixes** - For obvious typos or simple bugs, direct editing is faster

## Limitations

### File Size Constraints
- 500KB maximum per file
- 2MB total for all files in analysis
- Files exceeding limits are automatically excluded

### Security Restrictions
- System directories blocked: `/etc`, `/usr`, `/bin`, `/sbin`, `/var`, `/root`
- `.env` files automatically excluded (prevents secret exposure)
- Path traversal attacks prevented

### Output Constraints
- Output truncated at 100,000 characters
- JSON output available for programmatic parsing
- Markdown output optimized for human readability

## Environment Setup

Requires a Google API key:

```bash
# Option 1: GEMINI_API_KEY
export GEMINI_API_KEY=your-api-key

# Option 2: GOOGLE_API_KEY
export GOOGLE_API_KEY=your-api-key

# Or add to .env file
echo "GEMINI_API_KEY=your-api-key" >> .env
```

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

## See Also

- @CAPABILITIES.md - Gemini 3 Flash model specifications, thinking levels, file limits
- @PROMPTS.md - System prompt documentation with P0-P3 dimension descriptions
