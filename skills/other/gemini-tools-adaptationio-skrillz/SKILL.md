---
name: gemini-tools
description: Execute and manage Gemini CLI built-in tools including file operations, web search, shell commands, and memory. Use for automated workflows, tool orchestration, and safe execution patterns.
---

# Gemini Tools Execution

Comprehensive patterns for executing Gemini CLI's built-in tools safely and effectively.

## Available Tools

### File System Tools

```bash
# List directory contents
gemini -p "List all Python files in ./src"

# Read files
gemini -p "Read and explain @./config.json"

# Write files
gemini --yolo -p "Create a README.md for this project"

# Modify files
gemini --sandbox -p "Add error handling to @./main.py"
```

### Web Tools

```bash
# Google search
gemini --yolo -p "Search for React performance optimization best practices"

# Fetch web content
gemini -p "Analyze the API documentation at @https://api.example.com/docs"

# Research workflow
gemini --yolo -p "Research and summarize the latest Python 3.12 features"
```

### Shell Execution

```bash
# Safe execution with confirmation
gemini -p "Run the test suite and fix any failing tests"

# Auto-approve (use carefully!)
gemini --yolo -p "Set up a new Next.js project with TypeScript"

# Sandbox mode (recommended)
gemini --sandbox -p "Install dependencies and run the build"
```

### Memory Tool

```bash
# Save information
gemini -p "Remember that the API endpoint is https://api.prod.example.com"

# Recall information
gemini -p "What API endpoint did I tell you about?"

# Project-specific memory
cd project && gemini -p "Save project configuration: Node 20, PostgreSQL 15, Redis 7"
```

## Execution Modes

### Manual Approval (Default)

```bash
# Each tool call requires confirmation
gemini -p "Organize the project files into proper directories"
# > Tool call: list_directory('./') - Approve? [Y/n]
# > Tool call: write_file('./src/index.js') - Approve? [Y/n]
```

### YOLO Mode (Auto-Approve)

```bash
# All tools execute automatically
gemini --yolo -p "Create a complete Express.js API with authentication"

# Keyboard shortcut in chat
# Ctrl+Y to toggle YOLO mode
```

### Sandbox Mode (Safe Execution)

```bash
# Creates isolated environment
gemini --sandbox -p "Experiment with different npm packages"

# Limitations in sandbox:
# - No system modifications
# - Restricted file access
# - No network requests to production
```

## YOLO Automation Patterns

**YOLO mode** is ideal for trusted, repeatable tool operations. Here are proven automation patterns:

### Recommended YOLO Uses

```bash
# ✅ SAFE for YOLO (low-risk, high-value)
gemini --yolo -p "Organize project files by type and create index files"
gemini --yolo -p "Add JSDoc comments to all functions in ./src"
gemini --yolo -p "Generate comprehensive test suite for API endpoints"
gemini --yolo -p "Create complete documentation from code comments"
gemini --yolo -p "Set up ESLint, Prettier, and pre-commit hooks"
gemini --yolo -p "Generate TypeScript definitions from JavaScript"
```

### Use with Caution

```bash
# ⚠️ REVIEW FIRST (higher risk)
gemini -p "Refactor authentication system for security improvements"
gemini -p "Migrate database schema to new structure"
gemini -p "Update production deployment configuration"
gemini -p "Delete unused files and dependencies"

# Then if comfortable, use YOLO for execution:
gemini --yolo -p "Execute the reviewed plan step by step"
```

### YOLO + Safeguards

```bash
# Combine YOLO with checkpointing for safety
gemini --yolo --checkpointing -p "Comprehensive codebase modernization"

# Use YOLO with specific constraints
gemini --yolo -p "Add logging to all functions, but preserve exact functionality"

# YOLO with backup strategy
backup_and_execute() {
  local task="$1"
  git stash push -m "pre-yolo-backup-$(date +%s)"
  gemini --yolo -p "$task"
  echo "Backup created. Use 'git stash pop' to revert if needed."
}
```

## Tool Workflows

### Project Setup Automation

```bash
#!/bin/bash
# Automated project initialization

setup_project() {
  local name="$1"
  local type="$2"  # react, node, python, etc.
  
  gemini --yolo -p "Create a new $type project named '$name' with:
  1. Proper directory structure
  2. Configuration files
  3. Git initialization
  4. README with setup instructions
  5. Basic CI/CD workflow
  6. Docker setup
  7. Environment variables template
  8. Initial tests
  
  Use industry best practices."
}

# Usage
setup_project "my-app" "react"
```

### Code Generation Pipeline

```bash
#!/bin/bash
# Generate code from specifications

generate_from_spec() {
  local spec_file="$1"
  local output_dir="${2:-./generated}"
  
  gemini --yolo \
    --include-directories "$output_dir" \
    -p "Read the specification: @$spec_file
    
    Generate:
    1. Data models/schemas
    2. API endpoints
    3. Database migrations
    4. Unit tests
    5. Integration tests
    6. API documentation
    
    Output to: $output_dir/"
}
```

### File Organization

```bash
#!/bin/bash
# Smart file organization

organize_files() {
  local project_dir="${1:-.}"
  
  # Use YOLO for file organization (generally safe)
  gemini --yolo -p "Analyze and organize directory: $project_dir
  
  Execute automatically:
  1. Identify file types and purposes
  2. Create optimal directory structure
  3. Move files to appropriate locations
  4. Update import paths in code files
  5. Create index files for each module
  6. Generate structure documentation
  7. Create a change log of all moves"
}
```

### Bulk Processing

```bash
#!/bin/bash
# Process multiple files

process_files() {
  local pattern="$1"  # e.g., "*.js"
  local operation="$2"  # e.g., "add JSDoc comments"
  
  gemini --yolo -p "For each file matching $pattern:
  1. Read the file
  2. $operation
  3. Preserve formatting
  4. Save changes
  5. Log modifications
  
  Create a summary of all changes."
}

# Examples
process_files "*.py" "add type hints"
process_files "*.test.js" "convert to TypeScript"
process_files "*.md" "fix formatting and add TOC"
```

## Safety Patterns

### Pre-Execution Validation

```bash
#!/bin/bash
# Validate before execution

validate_then_execute() {
  local command="$1"
  
  # First pass: analyze without execution
  gemini -p "Analyze but DON'T execute: $command
  
  Check for:
  - Potential risks
  - Missing dependencies
  - Breaking changes
  - Security issues
  
  Report findings."
  
  read -p "Continue with execution? [y/N] " -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    gemini --yolo -p "Now execute: $command"
  fi
}
```

### Rollback Capability

```bash
#!/bin/bash
# Execute with rollback

with_rollback() {
  local operation="$1"
  local backup_dir=".backups/$(date +%Y%m%d-%H%M%S)"
  
  # Create backup
  mkdir -p "$backup_dir"
  cp -r . "$backup_dir/"
  
  # Execute operation
  if gemini --yolo -p "$operation"; then
    echo "Success! Backup at: $backup_dir"
  else
    echo "Failed! Rolling back..."
    cp -r "$backup_dir/"* .
    echo "Rolled back to previous state"
  fi
}
```

### Tool Restrictions

```json
// ~/.gemini/tool-policy.json
{
  "tools": {
    "shell": {
      "enabled": true,
      "requireConfirmation": true,
      "blockedCommands": ["rm -rf", "sudo", "chmod 777"],
      "allowedDirectories": ["./", "/tmp/"]
    },
    "fileSystem": {
      "enabled": true,
      "readOnly": false,
      "allowedPaths": ["./src/", "./tests/"],
      "blockedPaths": [".env", "*.key", "*.pem"]
    },
    "web": {
      "enabled": true,
      "allowedDomains": ["*.github.com", "docs.*.com"],
      "blockedDomains": ["*.internal.com"]
    },
    "memory": {
      "enabled": true,
      "maxItems": 100,
      "encryption": true
    }
  }
}
```

## Advanced Patterns

### Tool Chaining

```bash
#!/bin/bash
# Chain multiple tools

chain_operations() {
  gemini --yolo -p "Execute this workflow:
  
  1. Search for 'React hooks best practices'
  2. Read the top 3 results
  3. Create a summary document
  4. Generate example code
  5. Save to ./docs/react-hooks-guide.md
  6. Create unit tests for examples
  7. Run the tests
  8. Fix any issues"
}
```

### Conditional Execution

```bash
#!/bin/bash
# Execute based on conditions

conditional_tools() {
  gemini -p "Check if package.json exists.
  
  If it exists:
    1. Read package.json
    2. Update all dependencies
    3. Run npm audit fix
    4. Run tests
  
  If it doesn't exist:
    1. Detect project type
    2. Initialize appropriate package manager
    3. Add common dependencies
    4. Create basic scripts"
}
```

### Parallel Tool Execution

```bash
#!/bin/bash
# Run tools in parallel

parallel_analysis() {
  local project="$1"
  
  gemini --yolo -p "Analyze $project in parallel:
  
  Stream 1: Code Quality
  - Check for lint errors
  - Identify code smells
  - Suggest refactoring
  
  Stream 2: Security
  - Scan for vulnerabilities
  - Check dependencies
  - Review auth patterns
  
  Stream 3: Performance
  - Identify bottlenecks
  - Suggest optimizations
  - Memory usage analysis
  
  Combine all findings into a report."
}
```

## Monitoring & Logging

### Tool Usage Tracking

```bash
#!/bin/bash
# Monitor tool usage

track_tool_usage() {
  local log_file="~/.gemini/tool-usage.log"
  
  # Wrap gemini command
  gemini_tracked() {
    local start=$(date +%s)
    local output=$(gemini "$@" 2>&1)
    local end=$(date +%s)
    local duration=$((end - start))
    
    # Log usage
    echo "$(date '+%Y-%m-%d %H:%M:%S') | Duration: ${duration}s | Args: $*" >> "$log_file"
    echo "$output"
    
    # Parse and count tool calls
    local tool_count=$(echo "$output" | grep -c "Tool call:")
    echo "Tools executed: $tool_count" >> "$log_file"
  }
  
  alias gemini='gemini_tracked'
}
```

### Audit Trail

```bash
#!/bin/bash
# Complete audit trail

audit_tools() {
  local audit_dir="~/.gemini/audit/$(date +%Y%m%d)"
  mkdir -p "$audit_dir"
  
  # Before execution
  find . -type f -name "*" | xargs md5sum > "$audit_dir/before.md5"
  
  # Execute with logging
  gemini "$@" | tee "$audit_dir/execution.log"
  
  # After execution
  find . -type f -name "*" | xargs md5sum > "$audit_dir/after.md5"
  
  # Generate diff
  diff "$audit_dir/before.md5" "$audit_dir/after.md5" > "$audit_dir/changes.diff"
  
  echo "Audit trail saved to: $audit_dir"
}
```

## Error Handling

### Graceful Failures

```bash
#!/bin/bash
# Handle tool failures gracefully

resilient_execution() {
  local max_retries=3
  local retry_count=0
  
  while [ $retry_count -lt $max_retries ]; do
    if gemini --sandbox -p "$1"; then
      echo "Success on attempt $((retry_count + 1))"
      return 0
    else
      retry_count=$((retry_count + 1))
      echo "Attempt $retry_count failed. Retrying..."
      sleep 5
    fi
  done
  
  echo "Failed after $max_retries attempts"
  return 1
}
```

### Recovery Strategies

```bash
#!/bin/bash
# Implement recovery strategies

with_recovery() {
  local operation="$1"
  
  # Set trap for cleanup
  trap 'echo "Cleaning up..."; cleanup_function' ERR
  
  gemini -p "$operation" || {
    echo "Operation failed. Attempting recovery..."
    
    # Try recovery
    gemini -p "The previous operation failed. Please:
    1. Identify what went wrong
    2. Fix the issue
    3. Complete the operation safely"
  }
  
  trap - ERR
}
```

## Best Practices

### Tool Selection

1. **Use Appropriate Mode**
   - Default: Unknown operations
   - YOLO: Trusted, tested workflows
   - Sandbox: Experiments and testing

2. **Set Boundaries**
   - Define allowed paths
   - Restrict shell commands
   - Limit web domains

3. **Monitor Execution**
   - Log all tool usage
   - Track changes
   - Maintain audit trail

### Performance Tips

1. **Batch Operations**
   ```bash
   # Process multiple files in one prompt
   gemini --yolo -p "Process all *.js files: add types, format, test"
   ```

2. **Use Caching**
   ```bash
   # Cache web fetches
   export GEMINI_CACHE_WEB=true
   ```

3. **Optimize Context**
   ```bash
   # Include only necessary files
   gemini --include-directories ./src --max-depth 2
   ```

## Related Skills

- `gemini-cli`: Main Gemini CLI integration
- `gemini-auth`: Authentication management
- `gemini-chat`: Interactive chat sessions
- `gemini-mcp`: MCP server management