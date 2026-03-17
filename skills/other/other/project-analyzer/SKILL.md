---
name: project-analyzer
description: Analyzes project structure and generates appropriate Claude Code subagents based on detected tech stack
---

# Project Analyzer Skill

This skill automatically analyzes your project's technology stack and generates appropriate Claude Code subagents tailored to your specific setup.

## Purpose

Save time by automatically:
- Detecting your project's tech stack (Next.js, FastAPI, Go, etc.)
- Identifying testing frameworks and tools
- Generating optimized subagents for your specific stack
- Following Anthropic's Progressive Disclosure pattern

## How It Works

### 1. Detection Phase

The skill examines your project files to identify:

**Primary Framework Detection**:
- `package.json` → Node.js/JavaScript/TypeScript projects
- `requirements.txt`, `pyproject.toml` → Python projects
- `go.mod` → Go projects
- `pubspec.yaml` → Dart/Flutter projects

**Framework Specifics**:
- Next.js: `next.config.js`, `app/` or `pages/` directory
- FastAPI: `from fastapi import` in Python files
- React: `package.json` contains `"react"`
- And more...

**Tooling Detection**:
- Testing: Jest, Vitest, pytest, Go test
- Styling: Tailwind CSS, styled-components, CSS Modules
- State Management: Zustand, Redux, Pinia
- Type Safety: TypeScript, mypy, Go types

### 2. Confirmation Phase (Progressive Disclosure)

After detection, you'll see:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detected Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Framework:  Next.js 14
Language:   TypeScript
Styling:    Tailwind CSS
Testing:    Vitest + Testing Library
Confidence: 95%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate these subagents? [Y/n]
  ✓ nextjs-tester (Vitest + Testing Library)
  ✓ component-reviewer (React best practices)
  ✓ type-checker (TypeScript strict mode)
```

**You choose** what gets generated. No surprises.

### 3. Generation Phase

When confirmed, the skill:
1. Creates `.claude/agents/` directory (if needed)
2. Generates subagent markdown files from templates
3. Configures tools and prompts for your specific stack
4. Reports what was created

## Usage

### Automatic Invocation

This skill is configured to run automatically when you:
- Open a new project in Claude Code
- Request tech stack analysis
- Ask to "set up subagents"

### Manual Invocation

You can also invoke it explicitly:

```
Analyze this project and generate appropriate subagents
```

Or more specifically:

```
Use project-analyzer skill to detect my tech stack
```

## What Gets Generated

### For Next.js Projects

- **nextjs-tester**: Specialized in Vitest/Jest + Testing Library
- **component-reviewer**: React component best practices
- **type-checker**: TypeScript strict mode enforcement
- **api-handler**: API route testing and validation (if API routes detected)

### For FastAPI Projects

- **fastapi-tester**: pytest + TestClient specialist
- **api-reviewer**: REST API best practices
- **db-schema-checker**: SQLAlchemy/Pydantic schema validation
- **async-reviewer**: async/await pattern enforcement

### For Go Projects

- **go-tester**: go test + testify specialist
- **go-reviewer**: Go idioms and best practices
- **concurrency-checker**: Goroutine and channel patterns

## Configuration Override

Don't like auto-detection? Override it:

Create `.claude/project.yml`:

```yaml
adaptive-agents:
  stack_override:
    framework: nextjs
    language: typescript
    testing: vitest

  # Skip certain subagents
  skip_agents:
    - type-checker

  # Add custom agents
  custom_agents:
    - ./my-custom-agent.md
```

## How Detection Works

The skill uses Python scripts that leverage:

**File-based Detection**:
```python
# Using serena MCP for efficient file discovery
files = mcp__serena__find_file("package.json", project_path)
```

**Content Analysis**:
```python
# Search for framework-specific patterns
matches = mcp__serena__search_for_pattern(
    '"next":',
    path="package.json",
    output_mode="content"
)
```

**Confidence Scoring**:
```python
confidence = (
    0.4 if has_package_json else 0.0 +
    0.3 if has_next_config else 0.0 +
    0.2 if has_app_dir else 0.0 +
    0.1 if has_next_dependency else 0.0
)
```

## Error Handling

### Unknown Tech Stack

```
⚠️  Could not confidently detect tech stack

Found files: package.json, src/

Options:
  1. Manually specify stack in .claude/project.yml
  2. Use generic templates
  3. Skip auto-generation

Choose [1/2/3]:
```

### Ambiguous Detection

```
⚠️  Multiple frameworks detected

Candidates:
  - Next.js (confidence: 0.7)
  - Vite + React (confidence: 0.6)

Which is primary? [1/2]:
```

### Missing Dependencies

```
⚠️  Testing framework not detected

Framework: Next.js
Issue: No test files or config found

Suggestions:
  - Install Vitest: npm install -D vitest
  - Install Jest: npm install -D jest
  - Skip test agent generation

Proceed without test agent? [Y/n]:
```

## Implementation Files

This skill uses these helper scripts:

### `analyze_project.py`

Main entry point. Orchestrates detection and generation.

```bash
python analyze_project.py /path/to/project
```

### `detect_stack.py`

Tech stack detection logic. Returns structured data about framework, tools, confidence scores.

### `generate_agents.py`

Reads templates and generates customized subagent files.

## Best Practices

### 1. Run After Major Changes

Re-analyze when you:
- Add a new framework
- Change testing tools
- Restructure your project

```
Re-analyze project and update subagents
```

### 2. Review Generated Agents

Always review what was created:

```bash
ls .claude/agents/
cat .claude/agents/nextjs-tester.md
```

### 3. Customize as Needed

Generated agents are starting points. Edit them to fit your team's practices.

### 4. Commit to Version Control

```bash
git add .claude/agents/
git commit -m "Add auto-generated Claude Code subagents"
```

This way your team uses the same agents.

## Transparency

The skill logs its reasoning:

```
Detection Log: .claude/detection.log

[2025-01-19 18:30:00] INFO: Starting project analysis
[2025-01-19 18:30:00] INFO: Found package.json
[2025-01-19 18:30:01] INFO: Detected dependency: "next": "^14.0.0"
[2025-01-19 18:30:01] INFO: Found next.config.js
[2025-01-19 18:30:01] INFO: Confidence score: 0.95
[2025-01-19 18:30:01] INFO: Framework: Next.js 14
```

## Troubleshooting

### Issue: "Skill not found"

**Cause**: Skill not in global Skills directory

**Solution**:
```bash
# Copy to global Claude Skills
cp -r skills/project-analyzer ~/.claude/skills/
```

### Issue: "Permission denied" on file access

**Cause**: Insufficient file permissions

**Solution**:
```bash
# Ensure read permissions
chmod -R u+r /path/to/project
```

### Issue: "Low confidence detection"

**Cause**: Unusual project structure

**Solution**: Use manual override in `.claude/project.yml`

## References

- [Anthropic Progressive Disclosure](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/progressive-disclosure)
- [serena MCP Documentation](https://github.com/serenaai/serena-mcp)
- [Project Best Practices](../../docs/BEST_PRACTICES.md)
- [Stack Analyzer Subagent](../../.claude/agents/stack-analyzer.md)

## Contributing

Found a framework we don't support? Add detection logic:

1. Edit `detect_stack.py`
2. Add framework detection function
3. Create template in `templates/your-framework/`
4. Test with real project
5. Submit PR!

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-01-19
**Maintainer**: SawanoLab
