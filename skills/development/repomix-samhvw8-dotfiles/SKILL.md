---
name: repomix
description: "Repository packaging for AI/LLM analysis. Capabilities: pack repos into single files, generate AI-friendly context, codebase snapshots, security audit prep, filter/exclude patterns, token counting, multiple output formats. Actions: pack, generate, export, analyze repositories for LLMs. Keywords: Repomix, repository packaging, LLM context, AI analysis, codebase snapshot, Claude context, ChatGPT context, Gemini context, code packaging, token count, file filtering, security audit, third-party library analysis, context window, single file output. Use when: packaging codebases for AI, generating LLM context, creating codebase snapshots, analyzing third-party libraries, preparing security audits, feeding repos to Claude/ChatGPT/Gemini."
---

# Repomix Skill

Repomix is a powerful tool that packs entire repositories into single, AI-friendly files. Perfect for when you need to feed codebases to Large Language Models (LLMs) or other AI tools like Claude, ChatGPT, and Gemini.

## When to Use This Skill

Use this skill when:
- User needs to package a codebase for AI analysis
- Preparing repository context for LLM consumption
- Generating codebase snapshots for documentation
- Analyzing third-party libraries or repositories
- Creating AI-friendly representations of code projects
- Investigating bugs across large codebases
- Performing security audits on repositories
- Generating context for implementation planning

## Core Capabilities

### 1. Repository Packaging
Repomix packages entire repositories into single files with:
- AI-optimized formatting with clear separators
- Multiple output formats (XML, Markdown, JSON, Plain text)
- Git-aware processing (respects .gitignore)
- Token counting for LLM context management
- Security checks for sensitive information

### 2. Remote Repository Support
Can process remote repositories without cloning:
- Shorthand: `npx repomix --remote yamadashy/repomix`
- Full URL: `npx repomix --remote https://github.com/owner/repo`
- Specific commits: `npx repomix --remote https://github.com/owner/repo/commit/hash`

### 3. Comment Removal
Strips comments from supported languages when needed:
- Supported: HTML, CSS, JavaScript, TypeScript, Vue, Svelte, Python, PHP, Ruby, C, C#, Java, Go, Rust, Swift, Kotlin, Dart, Shell, YAML
- Enable with: `--remove-comments` or config file

## Installation

Check if installed first:
```bash
repomix --version
```

Install using preferred method:
```bash
# npm
npm install -g repomix

# yarn
yarn global add repomix

# bun
bun add -g repomix

# Homebrew (macOS/Linux)
brew install repomix
```

## Basic Usage

### Package Current Directory
```bash
# Basic packaging (generates repomix-output.xml)
repomix

# Specify output format
repomix --style markdown
repomix --style json
repomix --style plain

# Custom output path
repomix -o custom-output.xml
```

### Package Specific Directory
```bash
repomix /path/to/directory
```

### Package Remote Repository
```bash
# Shorthand format
npx repomix --remote owner/repo

# Full URL
npx repomix --remote https://github.com/owner/repo

# Specific commit
npx repomix --remote https://github.com/owner/repo/commit/abc123
```

## Command Line Options

### File Selection
```bash
# Include specific patterns
repomix --include "src/**/*.ts,*.md"

# Ignore additional patterns
repomix -i "tests/**,*.test.js"

# Disable .gitignore rules
repomix --no-gitignore

# Disable default ignore patterns
repomix --no-default-patterns
```

### Output Configuration
```bash
# Output format
repomix --style markdown  # or xml, json, plain

# Output file path
repomix -o output.md

# Remove comments
repomix --remove-comments

# Show line numbers
repomix --no-line-numbers  # disable line numbers
```

### Security & Analysis
```bash
# Run security checks
repomix --no-security-check  # disable security scanning

# Copy to clipboard
repomix --copy  # copy output to clipboard

# Verbose output
repomix --verbose
```

### Configuration
```bash
# Use custom config file
repomix -c custom-config.json

# Initialize new config
repomix --init  # creates repomix.config.json
```

## Configuration File

Create `repomix.config.json` in project root:

```json
{
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml",
    "removeComments": false,
    "showLineNumbers": true,
    "copyToClipboard": false
  },
  "include": ["**/*"],
  "ignore": {
    "useGitignore": true,
    "useDefaultPatterns": true,
    "customPatterns": [
      "additional-folder",
      "**/*.log",
      "**/tmp/**"
    ]
  },
  "security": {
    "enableSecurityCheck": true
  }
}
```

## Ignore Patterns

### .repomixignore File
Create `.repomixignore` for Repomix-specific ignore patterns (same format as .gitignore):

```
# Build artifacts
dist/
build/
*.min.js

# Test files
**/*.test.ts
**/*.spec.ts
coverage/

# Large files
*.mp4
*.zip

# Sensitive files
.env*
secrets/
```

### Precedence Order
1. CLI ignore patterns (`-i` flag)
2. `.repomixignore` file
3. Custom patterns in config file
4. `.gitignore` file (if enabled)
5. Default patterns (if enabled)

## Output Formats

### XML Format (Default)
Best for structured AI consumption:
```bash
repomix --style xml
```

### Markdown Format
Human-readable with syntax highlighting:
```bash
repomix --style markdown
```

### JSON Format
For programmatic processing:
```bash
repomix --style json
```

### Plain Text
Simple concatenation:
```bash
repomix --style plain
```

## Use Cases & Examples

### 1. Code Review Preparation
```bash
# Package feature branch for AI review
repomix --include "src/**/*.ts" --remove-comments -o feature-review.md --style markdown
```

### 2. Security Audit
```bash
# Package third-party library for analysis
npx repomix --remote vendor/library --style xml -o audit.xml
```

### 3. Documentation Generation
```bash
# Package with docs and code
repomix --include "src/**,docs/**,*.md" --style markdown -o context.md
```

### 4. Bug Investigation
```bash
# Package specific modules
repomix --include "src/auth/**,src/api/**" -o debug-context.xml
```

### 5. Implementation Planning
```bash
# Full codebase context for planning
repomix --remove-comments --copy
```

## Token Management

Repomix automatically counts tokens for:
- Individual files
- Total repository
- Per-format output

Use token counts to manage LLM context limits:
- Claude: ~200K tokens
- GPT-4: ~128K tokens
- GPT-3.5: ~16K tokens

## Security Considerations

### Sensitive Data Detection
Repomix uses Secretlint to detect:
- API keys and tokens
- Passwords and credentials
- Private keys
- AWS secrets
- Database connection strings

Disable if needed:
```bash
repomix --no-security-check
```

### Best Practices
1. Always review output before sharing
2. Use `.repomixignore` for sensitive files
3. Enable security checks for unknown codebases
4. Avoid packaging `.env` files
5. Check for hardcoded credentials

## Performance Optimization

### Large Repositories
Repomix uses worker threads for parallel processing:
- Efficiently handles large codebases
- Example: facebook/react processed 29x faster (123s → 4s)

### Optimization Tips
```bash
# Exclude unnecessary files
repomix -i "node_modules/**,dist/**,*.min.js"

# Process specific directories only
repomix --include "src/**/*.ts"

# Disable line numbers for smaller output
repomix --no-line-numbers
```

## Workflow Integration

### With Claude Code
```bash
# Package and analyze in one workflow
repomix --style markdown --copy
# Then paste into Claude for analysis
```

### With CI/CD
```bash
# Generate codebase snapshot for releases
repomix --style markdown -o release-snapshot.md
```

### With Git Hooks
```bash
# Pre-commit hook to generate context
repomix --include "src/**" -o .context/latest.xml
```

## Common Patterns

### Full Repository Package
```bash
repomix --remove-comments --style markdown -o full-repo.md
```

### Source Code Only
```bash
repomix --include "src/**/*.{ts,tsx,js,jsx}" -i "**/*.test.*"
```

### Documentation Bundle
```bash
repomix --include "**/*.md,docs/**" --style markdown
```

### TypeScript Project
```bash
repomix --include "**/*.ts,**/*.tsx" --remove-comments --no-line-numbers
```

### Remote Analysis
```bash
npx repomix --remote owner/repo --style xml -o analysis.xml
```

## Troubleshooting

### Issue: Output Too Large
```bash
# Exclude unnecessary files
repomix -i "node_modules/**,dist/**,coverage/**"

# Process specific directories
repomix --include "src/**"
```

### Issue: Missing Files
```bash
# Disable .gitignore rules
repomix --no-gitignore

# Check ignore patterns
cat .repomixignore
```

### Issue: Sensitive Data Warnings
```bash
# Review flagged files
# Add to .repomixignore
# Or disable checks: --no-security-check
```

## Implementation Workflow

When user requests repository packaging:

1. **Assess Requirements**
   - Identify target repository (local/remote)
   - Determine output format needed
   - Check for sensitive data concerns

2. **Configure Filters**
   - Set include patterns for relevant files
   - Add ignore patterns for unnecessary files
   - Enable/disable comment removal

3. **Execute Packaging**
   - Run repomix with appropriate options
   - Monitor token counts
   - Verify security checks

4. **Validate Output**
   - Review generated file
   - Confirm no sensitive data
   - Check token limits for target LLM

5. **Deliver Context**
   - Provide packaged file to user
   - Include token count summary
   - Note any warnings or issues

## Best Practices

1. **Start with defaults**: Run basic `repomix` first, then refine
2. **Use .repomixignore**: Better than CLI flags for complex patterns
3. **Enable security checks**: Especially for third-party code
4. **Choose right format**: XML for AI, Markdown for humans
5. **Monitor token counts**: Stay within LLM limits
6. **Remove comments**: When focusing on logic over documentation
7. **Version output**: Include in .gitignore, regenerate as needed
8. **Test patterns**: Verify include/exclude work as expected

## Related Tools

- **Context7**: For up-to-date library documentation
- **Git**: For repository history analysis
- **Secretlint**: For security scanning
- **Token counters**: For LLM context management

## Additional Resources

- GitHub: https://github.com/yamadashy/repomix
- Documentation: https://repomix.com/guide/
- MCP Server: Available for AI assistant integration
- Claude Code Plugin: Official integration available
