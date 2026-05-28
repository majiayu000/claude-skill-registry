---
name: mise-expert
description: "Mise development environment manager (asdf + direnv + make replacement). Capabilities: tool version management (node, python, go, ruby, rust), environment variables, task runners, project-local configs. Actions: install, manage, configure, run tools/tasks with mise. Keywords: mise, mise.toml, tool version, runtime version, node, python, go, ruby, rust, asdf, direnv, task runner, environment variables, version manager, .tool-versions, mise install, mise use, mise run, mise tasks, project config, global config. Use when: installing runtime versions, managing tool versions, setting up dev environments, creating task runners, replacing asdf/direnv/make, configuring project-local tools."
---

# Mise Expert Skill

## Purpose

Specialized skill for mise - a unified development environment manager combining tool version management (asdf replacement), environment variable management (direnv replacement), and task running (make/npm scripts replacement).

## When to Use This Skill

### Tool & Runtime Management
- Installing and managing runtime versions (node, python, go, ruby, rust, etc.)
- Setting up project-specific tool versions for reproducibility
- Switching between multiple language versions in polyglot projects
- Managing global vs project-local tool installations
- Migrating from asdf, nvm, pyenv, rbenv, or similar version managers
- Troubleshooting tool version conflicts

### Project Setup & Onboarding
- Bootstrapping new project development environments
- Creating mise.toml for team consistency
- Setting up monorepo tool configurations
- Configuring per-directory environment switching
- Establishing project development standards
- Simplifying onboarding for new team members

### Task Runner & Build Systems
- Creating or optimizing mise.toml task configurations
- Designing task workflows with dependency chains
- Implementing parallel task execution strategies
- Adding intelligent caching with sources/outputs
- Converting from make, npm scripts, just, or other task runners
- Building cross-platform compatible task systems
- Optimizing build performance with incremental builds

### Environment Management
- Configuring per-directory environment variables
- Managing secrets and configuration across environments
- Setting up development/staging/production environment switching
- Replacing direnv with mise
- Loading environment from .env files
- Creating environment-specific task behaviors

### CI/CD Integration
- Setting up mise in GitHub Actions, GitLab CI, CircleCI
- Ensuring consistent environments between local and CI
- Optimizing CI builds with mise caching
- Managing tool versions in containerized environments

### Troubleshooting & Optimization
- Debugging mise task execution issues
- Diagnosing tool version problems
- Resolving environment variable loading issues
- Optimizing task caching and performance
- Fixing cross-platform compatibility issues

## Core Capabilities

<capabilities>
- **Tool Version Management**: Install, configure, and switch between runtime versions
- **Task Design**: Create efficient, cacheable, and maintainable task configurations
- **Environment Setup**: Configure tools, variables, and per-directory environments
- **Workflow Optimization**: Design parallel execution and intelligent dependency chains
- **Migration Support**: Convert from asdf, make, npm, direnv, and other tools
- **Troubleshooting**: Diagnose and resolve mise configuration issues
- **Best Practices**: Apply mise patterns for modern development workflows
- **CI/CD Integration**: Configure mise for continuous integration pipelines
</capabilities>

## Operational Guidelines

### Task Configuration Principles

<task_design_principles>
1. **Caching First**: Always define `sources` and `outputs` for cacheable tasks
2. **Parallel by Default**: Use `depends` arrays for parallel execution
3. **Single Responsibility**: Each task should have one clear purpose
4. **Namespacing**: Group related tasks with prefixes (e.g., `db:migrate`, `test:unit`)
5. **Idempotency**: Tasks should be safe to run multiple times
6. **Platform Awareness**: Use `run_windows` for cross-platform compatibility
7. **Watch Mode Ready**: Design tasks compatible with `mise watch`
</task_design_principles>

### Decision Framework

<when_to_use_mise>
**Choose mise for:**
- Multi-language projects requiring version management (Python + Node + Go)
- Projects needing per-directory environment variables
- Cross-platform development teams (Linux/Mac/Windows)
- Replacing complex Makefiles or npm scripts
- Projects with parallel task execution needs
- Teams wanting consistent dev environments (new dev onboarding)
- Replacing multiple tools (asdf + direnv + make) with one
- CI/CD pipelines requiring reproducible builds

**Skip mise for:**
- Single-language projects with simple build steps
- Projects where npm scripts are sufficient
- Teams unfamiliar with TOML and no bandwidth for learning
- Projects with existing, working task systems and no pain points
- Embedded systems or constrained environments
</when_to_use_mise>

### Tool Version Management Patterns

<tool_installation_patterns>
**Project-Specific Tools**
```toml
# mise.toml - Project root configuration
[tools]
# Exact versions for reproducibility
node = "20.10.0"
python = "3.11.6"
go = "1.21.5"
terraform = "1.6.6"

# Read from version file
ruby = { file = ".ruby-version" }
java = { file = ".java-version" }

# Latest patch version
postgres = "16"
redis = "7"

# Multiple versions (switch with mise use)
# mise use node@18 (temporarily override)
```

**Global Development Tools**
```bash
# Install globally useful CLI tools
mise use -g ripgrep@latest      # Better grep
mise use -g bat@latest          # Better cat
```

**Version File Migration**
```bash
# Migrate from existing version files
echo "20.10.0" > .node-version
echo "3.11.6" > .python-version

# mise.toml
[tools]
node = { file = ".node-version" }
python = { file = ".python-version" }
```
</tool_installation_patterns>

### Project Setup Workflows

<project_setup_patterns>
**New Project Bootstrap**
```toml
# mise.toml
[tools]
node = "20"
python = "3.11"

[env]
PROJECT_ROOT = "{{cwd}}"
LOG_LEVEL = "debug"

[vars]
project_name = "my-app"

[tasks.setup]
description = "Setup development environment"
run = [
  "mise install",
  "npm install",
  "pip install -r requirements.txt",
  "cp .env.example .env"
]

[tasks.dev]
alias = "d"
description = "Start development server"
depends = ["setup"]
env = { NODE_ENV = "development" }
run = "npm run dev"
```

**Monorepo Configuration**
```toml
# Root mise.toml
[tools]
node = "20"
go = "1.21"

[tasks.install]
description = "Install all dependencies"
run = [
  "cd frontend && npm install",
  "cd backend && go mod download"
]

# frontend/mise.toml
[tasks.dev]
dir = "{{cwd}}/frontend"
run = "npm run dev"

# backend/mise.toml
[tools]
go = "1.21"

[tasks.dev]
dir = "{{cwd}}/backend"
run = "go run main.go"
```
</project_setup_patterns>

### Configuration Patterns

<common_patterns>
**Development Workflow**
```toml
[tasks.dev]
alias = "d"
description = "Start development server with hot reload"
env = { NODE_ENV = "development", DEBUG = "true" }
run = "npm run dev"

[tasks.dev-watch]
description = "Watch and rebuild on changes"
run = "mise watch build"
```

**Build Pipeline with Caching**
```toml
[tasks.clean]
description = "Remove build artifacts"
run = "rm -rf dist"

[tasks.build]
alias = "b"
description = "Build production bundle"
depends = ["clean"]
sources = ["src/**/*", "package.json", "tsconfig.json"]
outputs = ["dist/**/*"]
env = { NODE_ENV = "production" }
run = "npm run build"

[tasks.build-watch]
description = "Rebuild on source changes"
run = "mise watch build"
```

**Testing Suite**
```toml
[tasks.test]
alias = "t"
description = "Run all tests"
depends = ["test:unit", "test:integration"]  # Runs in parallel

[tasks."test:unit"]
description = "Run unit tests"
sources = ["src/**/*.ts", "tests/unit/**/*.ts"]
run = "npm test -- --testPathPattern=unit"

[tasks."test:integration"]
description = "Run integration tests"
sources = ["src/**/*.ts", "tests/integration/**/*.ts"]
run = "npm test -- --testPathPattern=integration"

[tasks."test:watch"]
description = "Run tests in watch mode"
run = "npm test -- --watch"

[tasks."test:coverage"]
description = "Generate coverage report"
run = "npm test -- --coverage"

[tasks."test:e2e"]
description = "Run end-to-end tests"
depends = ["build"]
run = "playwright test"
```

**Database Workflow**
```toml
[tasks."db:migrate"]
description = "Run database migrations"
run = "npx prisma migrate deploy"

[tasks."db:seed"]
description = "Seed database with test data"
depends = ["db:migrate"]
run = "npx prisma db seed"

[tasks."db:reset"]
description = "Reset database to clean state"
run = ["npx prisma migrate reset --force", "mise run db:seed"]

[tasks."db:studio"]
description = "Open Prisma Studio"
run = "npx prisma studio"
```

**Linting & Formatting**
```toml
[tasks.lint]
description = "Lint code"
sources = ["src/**/*.ts"]
run = "eslint src"

[tasks.format]
description = "Format code"
sources = ["src/**/*.ts"]
run = "prettier --write src"

[tasks."lint:fix"]
description = "Lint and auto-fix issues"
run = "eslint src --fix"

[tasks.check]
description = "Run all checks"
depends = ["lint", "format", "test"]  # Runs in parallel
```

**Deployment Pipeline**
```toml
[tasks.deploy]
description = "Deploy to production"
usage = '''
arg "environment" description="Target environment" default="staging"
flag "-f --force" description="Skip confirmation"
'''
depends = ["build", "test"]
depends_post = ["notify:slack"]
run = './scripts/deploy.sh {{arg(name="environment")}} {{flag(name="force")}}'

[tasks."deploy:staging"]
description = "Deploy to staging"
depends = ["build", "test"]
run = "./scripts/deploy.sh staging"

[tasks."deploy:production"]
description = "Deploy to production"
depends = ["build", "test"]
run = "./scripts/deploy.sh production"

[tasks."notify:slack"]
hide = true
run = 'curl -X POST $SLACK_WEBHOOK -d "Deployment complete"'
```

**Docker Integration**
```toml
[tasks."docker:build"]
description = "Build Docker image"
sources = ["Dockerfile", "src/**/*"]
run = "docker build -t myapp:latest ."

[tasks."docker:run"]
description = "Run Docker container"
depends = ["docker:build"]
run = "docker run -p 3000:3000 myapp:latest"

[tasks."docker:compose"]
description = "Start services with docker-compose"
run = "docker-compose up -d"
```

**Go Plugin Build System**
```toml
[tasks."build:plugins"]
description = "Build all Go plugins in parallel"
sources = ["plugins/**/*.go"]
outputs = ["plugins/**/main.so"]
run = '''
for plugin in plugins/*/; do
  (cd "$plugin" && go build -buildmode=plugin -o main.so main.go) &
done
wait
'''

[tasks."rebuild:plugins"]
description = "Rebuild plugins when engine changes"
sources = ["engine/**/*.go"]
depends = ["build:engine"]
run = "mise run build:plugins"
```
</common_patterns>

### Variables and Environment Management

<environment_patterns>
**Environment-Specific Variables**
```toml
[vars]
# Default development values
api_url = "http://localhost:3000"
db_host = "localhost"
db_port = "5432"
debug_mode = "true"

# Load additional vars from .env
_.file = ".env"

[env]
# Static environment variables
NODE_ENV = "development"
LOG_LEVEL = "debug"

# Reference variables
API_URL = "{{vars.api_url}}"
DATABASE_URL = "postgres://{{vars.db_host}}:{{vars.db_port}}/myapp"
DEBUG = "{{vars.debug_mode}}"

[tasks.dev]
env = {
  NODE_ENV = "development",
  API_URL = "{{vars.api_url}}"
}
run = "npm run dev"
```

**Multi-Environment Setup**
```toml
# mise.toml (base development config)
[vars]
environment = "development"
api_url = "http://localhost:3000"

[env]
NODE_ENV = "development"

# mise.staging.toml
[vars]
environment = "staging"
api_url = "https://api.staging.example.com"

[env]
NODE_ENV = "staging"

# mise.production.toml
[vars]
environment = "production"
api_url = "https://api.example.com"
debug_mode = "false"

[env]
NODE_ENV = "production"
```

**Secret Management**
```toml
# mise.toml (checked into git)
[vars]
# Non-sensitive defaults
api_url = "http://localhost:3000"

# Load secrets from .env (gitignored)
_.file = ".env"

[env]
# Reference secrets loaded from .env
API_KEY = "{{vars.api_key}}"
DATABASE_PASSWORD = "{{vars.db_password}}"

# .env (NOT in git)
api_key=secret-key-here
db_password=secret-password
```
</environment_patterns>

## Workflow Process

<workflow_steps>
When helping with mise configurations:

1. **Assess Current State**
   - Read existing mise.toml if present
   - Identify current task runner (make, npm, etc.)
   - Check for version managers (asdf, nvm, pyenv)
   - Understand project structure and requirements

2. **Design Architecture**
   - Determine tool version requirements
   - Map out task dependencies and relationships
   - Identify parallel execution opportunities
   - Plan caching strategy with sources/outputs
   - Consider cross-platform needs

3. **Implement Configuration**
   - Start with tool versions and environment setup
   - Create simple tasks, add complexity incrementally
   - Use namespacing for related tasks
   - Add aliases for frequently used tasks
   - Document complex tasks with descriptions

4. **Optimize Performance**
   - Add sources/outputs for caching
   - Leverage parallel execution via depends
   - Set appropriate `jobs` limit
   - Use watch mode for development workflows

5. **Validate and Test**
   - Run `mise install` to verify tool installation
   - Run `mise tasks ls` to verify task registration
   - Test task execution: `mise run <task>`
   - Verify caching behavior
   - Test cross-platform if applicable
   - Run `mise doctor` for diagnostics
</workflow_steps>

## Migration Strategies

<migration_from_asdf>
**From .tool-versions to mise.toml**

.tool-versions:
```
nodejs 20.10.0
python 3.11.6
golang 1.21.5
terraform 1.6.6
```

mise.toml:
```toml
[tools]
node = "20.10.0"
python = "3.11.6"
go = "1.21.5"
terraform = "1.6.6"
```

Migration command:
```bash
# Mise can read .tool-versions directly
mise install

# Or convert to mise.toml
mise use node@20.10.0 python@3.11.6 go@1.21.5 terraform@1.6.6
```
</migration_from_asdf>

<migration_from_make>
**From Makefile to mise.toml**

Makefile:
```makefile
.PHONY: build test clean deploy

clean:
	rm -rf dist

build: clean
	npm run build

test: build
	npm test

deploy: build test
	./deploy.sh
```

mise.toml:
```toml
[tasks.clean]
description = "Remove build artifacts"
run = "rm -rf dist"

[tasks.build]
alias = "b"
description = "Build production bundle"
depends = ["clean"]
sources = ["src/**/*", "package.json"]
outputs = ["dist/**/*"]
run = "npm run build"

[tasks.test]
alias = "t"
description = "Run tests"
depends = ["build"]
run = "npm test"

[tasks.deploy]
description = "Deploy to production"
depends = ["build", "test"]  # build and test run in parallel
run = "./deploy.sh"
```

**Advantages:**
- Automatic caching via sources/outputs
- Parallel execution of independent tasks
- Cross-platform compatibility
- Environment variable management
- Tool version management integrated
</migration_from_make>

<migration_from_npm>
**From package.json scripts to mise.toml**

package.json:
```json
{
  "scripts": {
    "dev": "NODE_ENV=development npm start",
    "build": "webpack --mode production",
    "test": "jest",
    "lint": "eslint src",
    "deploy": "npm run build && npm run test && ./deploy.sh"
  }
}
```

mise.toml:
```toml
[tasks.dev]
alias = "d"
description = "Start development server"
env = { NODE_ENV = "development" }
run = "npm start"

[tasks.build]
alias = "b"
description = "Build production bundle"
sources = ["src/**/*", "webpack.config.js"]
outputs = ["dist/**/*"]
run = "webpack --mode production"

[tasks.test]
alias = "t"
description = "Run tests"
run = "jest"

[tasks.lint]
description = "Lint code"
sources = ["src/**/*.js"]
run = "eslint src"

[tasks.deploy]
description = "Deploy to production"
depends = ["build", "test"]  # Runs in parallel
run = "./deploy.sh"
```

**Advantages:**
- Better dependency management (build + test run in parallel)
- Caching prevents unnecessary rebuilds
- Environment variables in configuration
- Consistent interface across different project types
- Works with any language, not just Node.js
</migration_from_npm>

<migration_from_direnv>
**From .envrc to mise.toml**

.envrc:
```bash
export NODE_ENV=development
export API_URL=http://localhost:3000
export DATABASE_URL=postgres://localhost/myapp
```

mise.toml:
```toml
[env]
NODE_ENV = "development"
API_URL = "http://localhost:3000"
DATABASE_URL = "postgres://localhost/myapp"

# Or use variables for DRY
[vars]
api_host = "localhost"
api_port = "3000"

[env]
API_URL = "http://{{vars.api_host}}:{{vars.api_port}}"
```

**Advantages:**
- TOML format easier to read/edit than bash
- Variables for DRY configuration
- Integrates with task runner and tool versions
- No shell-specific syntax
</migration_from_direnv>

## CI/CD Integration

<ci_integration>
**GitHub Actions**
```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup mise
        uses: jdx/mise-action@v2
        with:
          version: latest  # or specific version

      - name: Install tools and dependencies
        run: mise install

      - name: Run tests
        run: mise run test

      - name: Build
        run: mise run build
```

**GitLab CI**
```yaml
image: ubuntu:latest

before_script:
  - curl https://mise.run | sh
  - export PATH="$HOME/.local/bin:$PATH"
  - mise install

test:
  script:
    - mise run test

build:
  script:
    - mise run build
```

**Docker**
```dockerfile
FROM ubuntu:latest

# Install mise
RUN curl https://mise.run | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY . /app
WORKDIR /app

# Install tools and dependencies
RUN mise install

# Run build
RUN mise run build

CMD ["mise", "run", "start"]
```
</ci_integration>

## Troubleshooting Guide

<common_issues>
**Tool Not Found / Wrong Version**
```bash
# Symptom: Command not found or using system version
mise ls                          # List installed tools
mise install                     # Install missing tools
mise use node@20                 # Set specific version
mise doctor                      # Diagnose configuration
which node                       # Verify mise shim
mise reshim                      # Rebuild shims if needed
```

**Task Not Found**
```bash
# Symptom: "Task 'xyz' not found"
mise tasks ls                    # List all tasks
mise config                      # Show active config files
cat mise.toml                    # Verify task definition
mise tasks info <task>           # Get task details
```

**Task Caching Issues**
```toml
# Symptom: Task not re-running when files change
[tasks.build]
sources = ["src/**/*"]           # Check glob patterns are correct
outputs = ["dist/**/*"]          # Verify output paths match actual outputs
run = "npm run build"

# Debug: Remove outputs and re-run
# rm -rf dist && mise run build
```

**Environment Variables Not Loading**
```bash
# Symptom: Environment variables not set in tasks
mise config                      # Verify mise.toml location (project root)
mise run --verbose <task>        # Check env loading with verbose output
mise doctor                      # Diagnostic check
env | grep VAR_NAME              # Check if var is actually set
```

**Cross-Platform Issues**
```toml
# Symptom: Task fails on Windows
[tasks.build]
run = "npm run build"            # Use cross-platform commands
run_windows = "npm.cmd run build"  # Windows-specific override

# Or use mise variables for paths
run = "{{cwd}}/scripts/build.sh"
```

**Parallel Execution Not Working**
```toml
# Symptom: Tasks running sequentially instead of parallel
[tasks.ci]
depends = ["lint", "test", "build"]  # Runs in parallel by default

# For sequential execution, use run array
[tasks.sequential]
run = [
  "mise run step1",
  "mise run step2",
  "mise run step3"
]
```

**Tool Installation Fails**
```bash
# Symptom: mise install fails for a tool
mise doctor                      # Check for system dependencies
mise ls-remote node              # List available versions
mise install node@20 --verbose   # Verbose installation
mise cache clear                 # Clear cache and retry
```
</common_issues>

## Best Practices Checklist

<best_practices>
**Tool Management:**
- [ ] Pin exact versions for reproducibility (node = "20.10.0" not "20")
- [ ] Document version choices in comments
- [ ] Use .tool-versions or version files for compatibility
- [ ] Test tool installation on fresh clone

**Task Configuration:**
- [ ] All frequently used tasks have short aliases
- [ ] Build tasks define sources and outputs for caching
- [ ] Related tasks use namespace prefixes (db:, test:, docker:)
- [ ] Complex tasks have clear descriptions
- [ ] Tasks with arguments use usage spec for documentation
- [ ] Hidden internal tasks marked with hide = true

**Environment Management:**
- [ ] Environment variables use mise variables for DRY
- [ ] Secrets loaded from .env (gitignored)
- [ ] Development defaults in mise.toml (version controlled)
- [ ] Production overrides in separate config files

**Performance:**
- [ ] Parallel execution leveraged via depends arrays
- [ ] Caching configured with sources/outputs
- [ ] Watch mode available for iterative development
- [ ] jobs setting optimized for system resources

**Cross-Platform:**
- [ ] Platform-specific commands use run_windows
- [ ] Paths use {{cwd}} instead of hardcoded values
- [ ] Tested on target platforms (Linux/Mac/Windows)

**Team & CI:**
- [ ] mise.toml version controlled
- [ ] README documents mise installation and usage
- [ ] CI/CD uses mise for consistent environments
- [ ] Validated with `mise doctor`
</best_practices>

## Output Standards

When creating mise configurations:

1. **Always provide complete mise.toml sections**, not fragments
2. **Include comments** explaining non-obvious configurations
3. **Add descriptions** to all user-facing tasks
4. **Show usage examples** with `mise run` commands
5. **Explain caching strategy** when using sources/outputs
6. **Document environment variables** and their purposes
7. **Provide migration path** if converting from other systems
8. **Include validation steps** to verify configuration works
9. **Show tool installation** with `mise install` when setting up tools
10. **Demonstrate testing** with actual command examples

## Example Interactions

<example_setup>
User: "Setup mise for my Node.js project"

Response:
```toml
# mise.toml
[tools]
node = "20.10.0"

[env]
NODE_ENV = "development"

[tasks.install]
description = "Install dependencies"
run = "npm install"

[tasks.dev]
alias = "d"
description = "Start development server"
env = { NODE_ENV = "development" }
run = "npm run dev"

[tasks.build]
alias = "b"
description = "Build for production"
sources = ["src/**/*", "package.json"]
outputs = ["dist/**/*"]
env = { NODE_ENV = "production" }
run = "npm run build"

[tasks.test]
alias = "t"
description = "Run tests"
run = "npm test"
```

Setup:
```bash
mise install        # Install Node.js 20.10.0
mise run install    # Install npm dependencies
mise dev            # Start development server
```
</example_setup>

<example_polyglot>
User: "I have a project with Python backend and Node frontend"

Response:
```toml
# mise.toml
[tools]
node = "20.10.0"
python = "3.11.6"

[env]
PROJECT_ROOT = "{{cwd}}"

[tasks."backend:install"]
description = "Install Python dependencies"
dir = "{{cwd}}/backend"
run = "pip install -r requirements.txt"

[tasks."frontend:install"]
description = "Install Node dependencies"
dir = "{{cwd}}/frontend"
run = "npm install"

[tasks.install]
description = "Install all dependencies"
depends = ["backend:install", "frontend:install"]

[tasks."backend:dev"]
description = "Start Python backend"
dir = "{{cwd}}/backend"
env = { FLASK_ENV = "development" }
run = "python app.py"

[tasks."frontend:dev"]
description = "Start Node frontend"
dir = "{{cwd}}/frontend"
env = { NODE_ENV = "development" }
run = "npm run dev"

[tasks.dev]
description = "Start both frontend and backend"
depends = ["backend:dev", "frontend:dev"]
```

Usage:
```bash
mise install              # Install both Node and Python
mise run install          # Install all dependencies
mise dev                  # Start both services in parallel
```
</example_polyglot>

## Anti-Patterns to Avoid

<anti_patterns>
**Don't:**
- ❌ Use broad version ranges (node = "20" → unpredictable)
- ❌ Create tasks without descriptions (hard to maintain)
- ❌ Ignore sources/outputs on build tasks (misses caching benefits)
- ❌ Use sequential run arrays when depends would allow parallel execution
- ❌ Hardcode environment-specific values (use vars instead)
- ❌ Create monolithic tasks (break into smaller, reusable pieces)
- ❌ Skip cross-platform considerations for team projects
- ❌ Forget to version control mise.toml
- ❌ Use mise for trivial single-command projects
- ❌ Commit secrets in mise.toml (use .env)

**Do:**
- ✅ Pin exact tool versions for reproducibility
- ✅ Use namespacing for related tasks
- ✅ Add aliases for frequently used tasks
- ✅ Define sources/outputs for cacheable tasks
- ✅ Leverage parallel execution with depends
- ✅ Use variables for DRY configuration
- ✅ Document complex task arguments with usage spec
- ✅ Test with `mise doctor` before committing
- ✅ Provide clear descriptions for team members
- ✅ Load secrets from gitignored .env files
</anti_patterns>
