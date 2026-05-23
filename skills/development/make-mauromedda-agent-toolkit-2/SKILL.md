---
name: make
description: >-
  Guide for writing idiomatic, maintainable Makefiles following modern best practices.
  Enforces safety headers (SHELL, .SHELLFLAGS, .DELETE_ON_ERROR), self-documenting help,
  .PHONY declarations, modular includes. Triggers on "makefile", "Makefile", "make target",
  "make rule", "make pattern", "make help", "make template", ".mk file", "make include",
  "make variable", "make phony", "make dependency", "build system", "make clean",
  "make install", "make test", "make build", "make all", "make default", "task runner",
  "make automation", "GNU make", "make recipe", "make prerequisite".
  PROACTIVE: MUST invoke when writing ANY Makefile or *.mk file.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Make skill for idiomatic, maintainable Makefiles with modular patterns
# ABOUTME: Emphasizes safety, self-documentation, modularity, and orchestration focus

# Make Skill

## Quick Reference

| Rule | Enforcement |
|------|-------------|
| **Safety First** | Always set `SHELL`, `.SHELLFLAGS`, `.DELETE_ON_ERROR` |
| **Self-Documenting** | Every target has `## comment`; use `##@` for groups |
| **.PHONY** | Declare ALL non-file targets as phony |
| **Explicit** | No magic; clear variable names and dependencies |
| **Modular** | Split into `*.mk` files; use `include` |
| **Orchestration** | Make orchestrates; scripts do complex logic |
| **Naming** | Hyphen-case; verb-noun prefixes (e.g., `stack-up`) |
| **Help Default** | `.DEFAULT_GOAL := help` |

## 🛑 FILE OPERATION CHECKPOINT (BLOCKING)

**Before EVERY `Write` or `Edit` tool call on a `Makefile` or `*.mk` file:**

```
╔══════════════════════════════════════════════════════════════════╗
║  🛑 STOP - MAKE SKILL CHECK                                      ║
║                                                                  ║
║  You are about to modify a Makefile.                             ║
║                                                                  ║
║  QUESTION: Is /make skill currently active?                      ║
║                                                                  ║
║  If YES → Proceed with the edit                                  ║
║  If NO  → STOP! Invoke /make FIRST, then edit                    ║
║                                                                  ║
║  This check applies to:                                          ║
║  ✗ Write tool with file_path containing "Makefile"               ║
║  ✗ Edit tool with file_path containing "Makefile"                ║
║  ✗ Write/Edit with file_path ending in .mk                       ║
║  ✗ ANY Makefile, regardless of conversation topic                ║
║                                                                  ║
║  Examples that REQUIRE this skill:                               ║
║  - "add a build target" (edits Makefile)                         ║
║  - "update the docker targets" (edits make/docker.mk)            ║
║  - "fix the help target" (edits any Makefile)                    ║
╚══════════════════════════════════════════════════════════════════╝
```

**Why this matters:** Makefiles without safety headers can fail silently or
produce corrupt builds. The skill ensures `.DELETE_ON_ERROR` and proper `.PHONY`.

## 🔄 RESUMED SESSION CHECKPOINT

**When a session is resumed from context compaction, verify Makefile development state:**

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION RESUMED - MAKE SKILL VERIFICATION                  │
│                                                             │
│  Before continuing Makefile implementation:                 │
│                                                             │
│  1. Was I in the middle of writing Makefiles?               │
│     → Check summary for "Makefile", "make target", ".mk"    │
│                                                             │
│  2. Did I follow all Make skill guidelines?                 │
│     → Safety headers (SHELL, .SHELLFLAGS, .DELETE_ON_ERROR) │
│     → .PHONY declarations for non-file targets              │
│     → Self-documenting help target                          │
│     → ABOUTME headers on new files                          │
│                                                             │
│  3. Check Makefile quality before continuing:               │
│     → Run: make -n <target> (dry run)                       │
│     → Verify help target works: make help                   │
│                                                             │
│  If implementation was in progress:                         │
│  → Review the partial Makefile for completeness             │
│  → Ensure safety headers are present                        │
│  → Verify no recipes exceed 5 lines (move to scripts)       │
│  → Re-invoke /make if skill context was lost                │
└─────────────────────────────────────────────────────────────┘
```

## When to Use Make

**Use Make for orchestration and build tasks:**

- Build automation (compile, link, bundle)
- Development workflow commands (start, stop, test, lint)
- Multi-service orchestration (Docker, Terraform)
- CI/CD pipeline steps
- Task runners with dependencies

**Do NOT use Make for:**

- Complex business logic (use Python, Go, etc.)
- Scripts requiring conditionals/loops (use Bash scripts)
- Anything requiring error recovery
- Configuration management (use dedicated tools)

**Size guideline:** If a Makefile exceeds ~300 lines, split into modular `*.mk` files.

**Recipe rule:** If a recipe exceeds 5 lines or contains `if/else`, move it to a script and invoke the `/bash` skill.

## Core Principles

### 1. Safety Headers

Every Makefile starts with strict settings (like Bash's `set -euo pipefail`):

```makefile
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
```

| Setting | Purpose |
|---------|---------|
| `SHELL := bash` | Use Bash instead of `/bin/sh` |
| `.SHELLFLAGS` | `-e` exit on error, `-u` error on undefined, `-o pipefail` |
| `.DELETE_ON_ERROR` | Remove target if recipe fails (prevents corrupt state) |
| `--warn-undefined-variables` | Catch typos in variable names |
| `--no-builtin-rules` | Disable implicit rules for clarity |

### 2. Self-Documenting Help System

Every Makefile must have a help target as default:

```makefile
.DEFAULT_GOAL := help

##@ General
.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} \
		/^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } \
		/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
```

**Documentation syntax:**

```makefile
##@ Section Header        # Creates bold section in help output
target: ## Description    # Documents the target
```

### 3. Phony Targets

Declare ALL non-file-producing targets:

```makefile
.PHONY: help build test clean deploy
.PHONY: docker-up docker-down
.PHONY: logs-%  # Pattern rules too
```

**Why:** Prevents conflicts with files named `build`, `test`, etc.

### 4. Explicit Over Implicit

- Use `$(VARIABLE)` not `$VARIABLE`
- Quote paths: `"$(PATH_VAR)"`
- Name variables clearly: `DOCKER_COMPOSE_FILES` not `DCF`
- Avoid automatic variables in complex contexts

### 5. Modular Design

Split large Makefiles into focused modules:

```makefile
# Root Makefile
include make/common.mk
include make/docker.mk
include make/test.mk

# Optional includes (won't fail if missing)
-include make/local.mk
```

See `resources/common.mk` for a reusable library pattern.

### 6. Orchestration Focus

Make orchestrates; it doesn't implement:

```makefile
# GOOD: Make orchestrates
test: ## Run tests
	@./scripts/run-tests.sh

# BAD: Complex logic in Make
test:
	@if [ -f .env ]; then \
		source .env && \
		for dir in $(TEST_DIRS); do \
			cd $$dir && npm test || exit 1; \
		done \
	fi
```

### 7. Consistent Naming

**Prefixes for semantic grouping:**

| Prefix | Purpose | Example |
|--------|---------|---------|
| `stack-` | Full application stack | `stack-up`, `stack-down` |
| `infra-` | Infrastructure only | `infra-network`, `infra-wait` |
| `docker-` | Docker operations | `docker-build`, `docker-ps` |
| `test-` | Test execution | `test-unit`, `test-e2e` |
| `db-` or `migrate-` | Database operations | `db-migrate`, `db-seed` |

**Verbs:**

| Verb | Meaning |
|------|---------|
| `up` / `start` | Create and run |
| `down` / `stop` | Stop and remove |
| `restart` | Stop then start |
| `build` | Build only |
| `rebuild` | Build and start |
| `logs` | Stream logs |
| `status` | Show current state |

## Standard Template

Use `resources/template.mk` as a starter:

```bash
cp ~/.claude/skills/make/resources/template.mk ./Makefile
```

The template includes:
- Safety headers
- Color definitions
- Logging macros
- Help system
- Example targets

## Variable Patterns

### Path Resolution (Portable)

```makefile
# Get directory containing this Makefile
MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# Project root (if Makefile is in project root)
PROJECT_ROOT := $(MAKEFILE_DIR)

# Relative paths from Makefile location
SRC_DIR := $(PROJECT_ROOT)src
BUILD_DIR := $(PROJECT_ROOT)build
```

### Default Values

```makefile
# Use ?= for overridable defaults
COMPOSE_PROJECT_NAME ?= myproject
PORT ?= 8080

# Use := for computed values
TIMESTAMP := $(shell date +%Y%m%d-%H%M%S)
GIT_SHA := $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
```

### Environment Exports

```makefile
# Export for child processes
export DOCKER_BUILDKIT := 1
export COMPOSE_DOCKER_CLI_BUILD := 1

# Pass through from environment
export API_KEY
export DATABASE_URL
```

### Conditional Variables

```makefile
# Makefile conditionals (evaluated at parse time)
ifeq ($(CI),true)
    VERBOSE := 1
endif

ifdef DEBUG
    BUILD_FLAGS += -v
endif

ifndef REQUIRED_VAR
    $(error REQUIRED_VAR is not set)
endif
```

## Macros (define/endef)

### Logging Macros

```makefile
# Color codes
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
BOLD := \033[1m
NC := \033[0m

define log_info
	@printf "$(CYAN)[INFO]$(NC) %s\n" "$(1)"
endef

define log_success
	@printf "$(GREEN)[OK]$(NC) %s\n" "$(1)"
endef

define log_warn
	@printf "$(YELLOW)[WARN]$(NC) %s\n" "$(1)"
endef

define log_error
	@printf "$(RED)[ERROR]$(NC) %s\n" "$(1)"
endef

define log_step
	@printf "$(BOLD)>>> %s$(NC)\n" "$(1)"
endef

# Usage
build:
	$(call log_step,Building project)
	@go build ./...
	$(call log_success,Build completed)
```

### Utility Macros

```makefile
# Check if command exists
define check_cmd
	@command -v $(1) >/dev/null 2>&1 || { \
		printf "$(RED)[ERROR]$(NC) $(1) is required but not installed\n"; \
		exit 1; \
	}
endef

# Ensure directory exists
define ensure_dir
	@mkdir -p $(1)
endef

# Confirm dangerous action
define confirm
	@read -p "Are you sure? [y/N] " ans && [ "$${ans:-N}" = "y" ]
endef

# Usage
deploy: ## Deploy to production
	$(call check_cmd,kubectl)
	$(call confirm)
	$(call log_step,Deploying to production)
	@kubectl apply -f manifests/
```

## Pattern Rules

### Dynamic Targets with %

```makefile
# logs-<service> - tail logs for any service
.PHONY: logs-%
logs-%: ## Tail logs for a specific service
	docker compose logs -f $*

# docker-exec-<service> - exec into any container
.PHONY: exec-%
exec-%: ## Execute shell in a container
	docker compose exec $* sh

# build-<component> - build specific component
.PHONY: build-%
build-%:
	$(call log_step,Building $*)
	@cd $* && make build
```

**Automatic variables:**

| Variable | Meaning |
|----------|---------|
| `$@` | Target name |
| `$<` | First prerequisite |
| `$^` | All prerequisites |
| `$*` | Stem matched by `%` |

### No-op Targets for Arguments

```makefile
# Allow: make logs backend
# These are filter arguments, not real targets
.PHONY: backend frontend api worker
backend frontend api worker:
	@:

.PHONY: logs
logs: ## Tail logs (usage: make logs <service>)
	@component="$(filter-out $@,$(MAKECMDGOALS))"; \
	if [ -n "$$component" ]; then \
		docker compose logs -f $$component; \
	else \
		docker compose logs -f; \
	fi
```

## Modular Library Pattern

### Structure

```
project/
├── Makefile              # Root: includes modules, defines high-level targets
└── make/
    ├── common.mk         # Shared: variables, colors, logging macros
    ├── docker.mk         # Docker Compose operations
    ├── test.mk           # Test orchestration
    └── app-python.mk     # Language-specific targets
```

### Root Makefile

```makefile
# Include order matters: common first, then specific
include make/common.mk
include make/docker.mk
include make/test.mk

# Optional local overrides
-include make/local.mk

##@ Stack Management
.PHONY: up
up: docker-up ## Start all services
	$(call log_success,Stack is running)

.PHONY: down
down: docker-down ## Stop all services
	$(call log_success,Stack stopped)
```

### Consumer Pattern (Multi-Repo)

For projects that consume a shared Makefile library:

```makefile
# Define path to shared infra
INFRA_DIR ?= $(HOME)/projects/shared-infra

# Clone if missing
$(if $(wildcard $(INFRA_DIR)),,$(shell git clone git@github.com:org/shared-infra.git $(INFRA_DIR)))

# Include shared modules
-include $(INFRA_DIR)/make/common.mk
-include $(INFRA_DIR)/make/app.mk
-include $(INFRA_DIR)/make/app-python.mk
```

See `resources/common.mk` for a complete reusable library.

## Dependency Management

### Prerequisite Chains

```makefile
# Direct dependencies
deploy: build test ## Deploy (requires build and test)
	@./scripts/deploy.sh

# Chain dependencies
clean-all: clean-build clean-test clean-docker

# Order-only prerequisites (directory must exist, but changes don't trigger rebuild)
$(BUILD_DIR)/output: source.c | $(BUILD_DIR)
	gcc -o $@ $<

$(BUILD_DIR):
	mkdir -p $@
```

### Conditional Dependencies

```makefile
.PHONY: start
start: ## Start services (optionally with migrations)
ifeq ($(MIGRATE),1)
	$(call log_info,Running migrations first)
	@$(MAKE) db-migrate
endif
	@docker compose up -d
```

### Sentinel Files (Complex Dependencies)

For dependencies that don't produce predictable files (like `npm install`):

```makefile
# Sentinel file tracks when install was last run
.stamps:
	@mkdir -p .stamps

.stamps/npm-install: package.json package-lock.json | .stamps
	npm ci
	@touch $@

.stamps/pip-install: requirements.txt | .stamps
	pip install -r requirements.txt
	@touch $@

# Depend on sentinel, not directory
build: .stamps/npm-install
	npm run build

clean:
	rm -rf .stamps node_modules
```

## Integration Patterns

### Docker Compose

```makefile
# Compose file configuration
COMPOSE_FILES := -f docker-compose.yml
ifdef CI
    COMPOSE_FILES += -f docker-compose.ci.yml
endif

COMPOSE := docker compose $(COMPOSE_FILES)

.PHONY: docker-up
docker-up: ## Start Docker services
	$(COMPOSE) up -d

.PHONY: docker-down
docker-down: ## Stop Docker services
	$(COMPOSE) down
```

### Terraform

```makefile
TF_DIR := terraform

.PHONY: tf-init
tf-init: ## Initialize Terraform
	cd $(TF_DIR) && terraform init

.PHONY: tf-plan
tf-plan: ## Plan Terraform changes
	cd $(TF_DIR) && terraform plan -out=tfplan

.PHONY: tf-apply
tf-apply: ## Apply Terraform changes
	$(call confirm)
	cd $(TF_DIR) && terraform apply tfplan
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Spaces instead of tabs** | Recipes won't run | Use tabs for recipe lines |
| **Missing .PHONY** | Target skipped if file exists | Declare all non-file targets |
| **Bare `rm` without `-f`** | Fails if file missing | Use `rm -f` or `rm -rf` |
| **Ignoring errors silently** | `@command \|\| true` hides failures | Handle errors explicitly |
| **Complex shell logic** | Unmaintainable, error-prone | Move to script; invoke `/bash` |
| **Recursive make without $(MAKE)** | Breaks parallelism, options | Use `$(MAKE) -C subdir` |
| **Hardcoded paths** | Not portable | Use variables with defaults |
| **No help target** | Users don't know available commands | Always provide `help` |
| **Excessive `@` silencing** | Can't debug issues | Only silence noise, not errors |

## Validation

Run the validation script to check Makefile quality:

```bash
~/.claude/skills/make/scripts/validate_makefile.sh [Makefile]
```

The script checks:
- Safety headers present
- Help target exists
- `.PHONY` declarations
- Forbidden patterns (complex shell logic, missing error handling)
- Uses `checkmake` if available

## Checklist

Before committing a Makefile:

- [ ] Safety headers present (`SHELL`, `.SHELLFLAGS`, `.DELETE_ON_ERROR`)
- [ ] `.DEFAULT_GOAL := help` set
- [ ] `help` target with awk-based documentation parser
- [ ] All non-file targets declared `.PHONY`
- [ ] Variables use `$(VAR)` syntax (not `$VAR`)
- [ ] Paths are quoted where needed
- [ ] No recipes exceed 5 lines (moved to scripts)
- [ ] No complex shell logic (if/else, loops) in recipes
- [ ] Logging macros used for user feedback
- [ ] Dependencies declared correctly
- [ ] Runs `validate_makefile.sh` without errors
- [ ] Tested with `make -n <target>` (dry run)
