---
name: mise-task-configuration
description: Use when defining and configuring Mise tasks in mise.toml. Covers task definitions, dependencies, file tasks, and parallel execution.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Mise - Task Configuration

Defining and managing tasks in Mise for build automation, testing, and development workflows.

## Basic Task Definition

### Simple TOML Tasks

```toml
# mise.toml
[tasks.build]
description = "Build the project"
run = "cargo build --release"

[tasks.test]
description = "Run all tests"
run = "cargo test"

[tasks.lint]
description = "Run linter"
run = "cargo clippy -- -D warnings"
```

### Running Tasks

```bash
# Run a task
mise run build
mise build  # Shorthand if no command conflicts

# Run multiple tasks
mise run build test lint

# List available tasks
mise tasks ls

# Show task details
mise tasks info build
```

## Task Dependencies

### Sequential Dependencies

```toml
[tasks.deploy]
description = "Deploy the application"
depends = ["build", "test"]
run = "./deploy.sh"
```

### Parallel Dependencies

```toml
[tasks.ci]
description = "Run CI checks"
depends = ["lint", "test", "security-scan"]
run = "echo 'All checks passed'"
```

Mise automatically runs dependencies in parallel when possible.

## File Tasks

### Creating File Tasks

```bash
# Create task directory
mkdir -p .mise/tasks

# Create executable task file
cat > .mise/tasks/deploy <<'EOF'
#!/usr/bin/env bash
# mise description="Deploy the application"
# mise depends=["build", "test"]

echo "Deploying..."
./scripts/deploy.sh
EOF

chmod +x .mise/tasks/deploy
```

### File Task Metadata

```bash
#!/usr/bin/env bash
# mise description="Task description"
# mise depends=["dependency1", "dependency2"]
# mise sources=["src/**/*.rs"]
# mise outputs=["target/release/app"]

# Task implementation
```

## Advanced Task Configuration

### Task Arguments

```toml
[tasks.test]
description = "Run tests with optional filter"
run = '''
if [ -n "$1" ]; then
  cargo test "$1"
else
  cargo test
fi
'''
```

```bash
# Run all tests
mise test

# Run specific test
mise test user_tests
```

### Environment Variables in Tasks

```toml
[tasks.build]
description = "Build with specific configuration"
env = { RUST_ENV = "production", OPTIMIZATION = "3" }
run = "cargo build --release"

[tasks.dev]
description = "Start development server"
env = { NODE_ENV = "development", PORT = "3000" }
run = "npm run dev"
```

### Task Aliases

```toml
[tasks.b]
alias = "build"

[tasks.t]
alias = "test"

[tasks.d]
alias = "dev"
```

```bash
# Use aliases
mise b  # Runs build
mise t  # Runs test
```

## File Watching

### Watch Mode Tasks

```toml
[tasks.watch]
description = "Watch and rebuild on changes"
run = "cargo watch -x build"

[tasks."test:watch"]
description = "Watch and run tests"
run = "cargo watch -x test"
```

```bash
# Built-in watch with mise
mise watch --task build
```

## Monorepo Task Patterns

### Workspace Tasks

```toml
# Root mise.toml
[tasks.build-all]
description = "Build all packages"
depends = ["pkg-a:build", "pkg-b:build", "pkg-c:build"]
run = "echo 'All packages built'"

[tasks."pkg-a:build"]
description = "Build package A"
run = "cd packages/pkg-a && cargo build"

[tasks."pkg-b:build"]
description = "Build package B"
run = "cd packages/pkg-b && cargo build"
```

### Per-Package Tasks

```toml
# packages/pkg-a/mise.toml
[tasks.build]
description = "Build package A"
run = "cargo build"

[tasks.test]
description = "Test package A"
depends = ["build"]
run = "cargo test"
```

## Task Validation

### Validate Task Configuration

```bash
# Validate all tasks
mise tasks validate

# Check specific task
mise tasks info build
```

### Common Validation Errors

```toml
# Error: Missing required fields
[tasks.broken]
run = "echo test"  # Missing description

# Error: Invalid dependency
[tasks.deploy]
description = "Deploy"
depends = ["nonexistent-task"]
run = "./deploy.sh"

# Error: Circular dependency
[tasks.a]
description = "Task A"
depends = ["b"]
run = "echo a"

[tasks.b]
description = "Task B"
depends = ["a"]  # Circular!
run = "echo b"
```

## Best Practices

### Organize Tasks by Purpose

```toml
# Build tasks
[tasks.build]
description = "Build production binary"
run = "cargo build --release"

[tasks."build:debug"]
description = "Build debug binary"
run = "cargo build"

# Test tasks
[tasks.test]
description = "Run all tests"
run = "cargo test"

[tasks."test:unit"]
description = "Run unit tests only"
run = "cargo test --lib"

[tasks."test:integration"]
description = "Run integration tests"
run = "cargo test --test '*'"

# Development tasks
[tasks.dev]
description = "Start development server"
run = "cargo run"

[tasks.watch]
description = "Watch and rebuild"
run = "cargo watch -x run"
```

### Use Descriptive Names

```toml
# Good: Clear, descriptive names
[tasks."test:integration:api"]
description = "Run API integration tests"
run = "pytest tests/integration/api"

# Avoid: Vague names
[tasks.t1]
description = "Some test"
run = "pytest"
```

### Leverage Dependencies

```toml
# Good: Explicit dependencies
[tasks.deploy]
description = "Deploy to production"
depends = ["lint", "test", "build"]
run = "./scripts/deploy.sh"

# Avoid: Manual sequencing in run command
[tasks.deploy]
description = "Deploy to production"
run = '''
cargo clippy
cargo test
cargo build --release
./scripts/deploy.sh
'''
```

### Use Environment Variables

```toml
# Access mise environment variables
[tasks.info]
description = "Show task info"
run = '''
echo "Task: $MISE_TASK_NAME"
echo "Project root: $MISE_PROJECT_ROOT"
echo "Config root: $MISE_CONFIG_ROOT"
'''
```

## Common Patterns

### Pre/Post Hooks

```toml
[tasks.build]
description = "Build with pre/post hooks"
depends = ["pre-build"]
run = "cargo build"

[tasks.pre-build]
description = "Run before build"
run = "echo 'Preparing build...'"

[tasks.post-build]
description = "Run after build"
run = "echo 'Build complete!'"

[tasks."build:full"]
description = "Build with all hooks"
depends = ["pre-build", "build", "post-build"]
run = "echo 'Full build pipeline complete'"
```

### Conditional Execution

```toml
[tasks.deploy]
description = "Deploy only if tests pass"
run = '''
if mise test; then
  ./scripts/deploy.sh
else
  echo "Tests failed, deployment cancelled"
  exit 1
fi
'''
```

### Multi-Stage Builds

```toml
[tasks.build]
description = "Multi-stage build"
depends = ["compile", "optimize", "package"]
run = "echo 'Build complete'"

[tasks.compile]
description = "Compile source"
run = "cargo build --release"

[tasks.optimize]
description = "Optimize binary"
depends = ["compile"]
run = "strip target/release/app"

[tasks.package]
description = "Create package"
depends = ["optimize"]
run = "tar -czf app.tar.gz target/release/app"
```

## Anti-Patterns

### Don't Hardcode Paths

```toml
# Bad: Hardcoded absolute paths
[tasks.build]
description = "Build"
run = "cd /Users/me/project && cargo build"

# Good: Use relative paths and environment variables
[tasks.build]
description = "Build"
run = "cd $MISE_PROJECT_ROOT && cargo build"
```

### Don't Duplicate Logic

```toml
# Bad: Duplicated test logic
[tasks."test:unit"]
run = "cargo test --lib"

[tasks."test:integration"]
run = "cargo test --test '*'"

[tasks."test:all"]
run = "cargo test --lib && cargo test --test '*'"

# Good: Use dependencies
[tasks."test:all"]
depends = ["test:unit", "test:integration"]
run = "echo 'All tests complete'"
```

### Don't Ignore Exit Codes

```toml
# Bad: Swallowing errors
[tasks.ci]
run = '''
cargo clippy || true
cargo test || true
echo "CI complete"
'''

# Good: Fail fast
[tasks.ci]
depends = ["lint", "test"]
run = "echo 'CI checks passed'"
```

## Related Skills

- **tool-management**: Managing tool versions with Mise
- **environment-management**: Environment variables and configuration
