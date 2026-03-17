---
name: Test Framework Detector
description: Automatically detect test frameworks (Jest, pytest, RSpec, xUnit) in projects by analyzing configuration files and dependencies
version: 1.0.0
---

# Test Framework Detector

## Purpose

Automatically identify which test framework(s) a project uses by examining:
- Package manifests (package.json, requirements.txt, Gemfile, *.csproj)
- Test configuration files (jest.config.js, pytest.ini, spec_helper.rb, xunit.runner.json)
- Directory structure and naming conventions

## Usage

This skill is invoked by agents (like deep-debugger) when they need to determine which test framework to use for test generation or execution.

### Detection Script

Run the detection script with the project path:

```bash
node detect-framework.js /path/to/project
```

### Output Format

The script returns a JSON object with detected frameworks:

```json
{
  "detected": true,
  "frameworks": [
    {
      "name": "jest",
      "confidence": 0.95,
      "version": "29.7.0",
      "configFiles": ["jest.config.js", "package.json"],
      "testDirectory": "tests/",
      "testPattern": "**/*.test.js"
    }
  ],
  "primary": "jest"
}
```

## Detection Patterns

The skill uses pattern-based detection defined in `framework-patterns.json`. Each framework has:
- **Package indicators**: Dependencies that suggest framework presence
- **Config files**: Framework-specific configuration files
- **Test file patterns**: Common test file naming conventions

## Supported Frameworks

1. **Jest** (JavaScript/TypeScript)
   - Config: jest.config.js, jest.config.ts, package.json (jest section)
   - Dependencies: jest, @types/jest, ts-jest
   - Patterns: *.test.js, *.spec.js, __tests__/**

2. **pytest** (Python)
   - Config: pytest.ini, pyproject.toml, setup.cfg, tox.ini
   - Dependencies: pytest in requirements.txt or pyproject.toml
   - Patterns: test_*.py, *_test.py, tests/**

3. **RSpec** (Ruby)
   - Config: .rspec, spec/spec_helper.rb
   - Dependencies: rspec in Gemfile
   - Patterns: *_spec.rb, spec/**

4. **xUnit** (C#/.NET)
   - Config: xunit.runner.json, *.csproj
   - Dependencies: xunit, xunit.runner.visualstudio in *.csproj
   - Patterns: *Tests.cs, *Test.cs, Tests/**

## Confidence Scoring

Confidence scores (0.0-1.0) are calculated based on:
- **Config file presence**: +0.4
- **Package dependency found**: +0.3
- **Test directory exists**: +0.2
- **Test files found**: +0.1

Multiple frameworks may be detected (e.g., Jest + pytest in monorepos).

## Example Invocations

**Detect framework in current directory:**
```bash
node skills/test-detector/detect-framework.js .
```

**Detect framework with verbose output:**
```bash
DEBUG=true node skills/test-detector/detect-framework.js /path/to/project
```

## Integration with Agents

Agents should invoke this skill before test generation:

```markdown
1. Invoke test-detector skill with project path
2. Parse JSON output to get primary framework
3. Invoke appropriate test framework skill (jest-test, pytest-test, etc.)
4. Generate or execute tests using framework-specific patterns
```

## Error Handling

If no framework is detected:
```json
{
  "detected": false,
  "frameworks": [],
  "primary": null,
  "message": "No test framework detected. Please specify framework manually."
}
```
