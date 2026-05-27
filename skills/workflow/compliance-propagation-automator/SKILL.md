---
name: compliance-propagation-automator
version: "1.0.0"
category: coordination
description: "Compliance Propagation Automator"
---

# Compliance Propagation Automator

> **Version:** 1.0.0
> **Created:** 2026-01-05
> **Category:** workspace-hub
> **Related Skills:** compliance-check, repo-sync, knowledge-base-system

## Overview

Automates propagation of standards, configurations, and compliance requirements across all 26+ repositories. Ensures consistency using existing propagation scripts in `scripts/compliance/`.

## Core Propagation Scripts

### Available Scripts

```bash
scripts/compliance/
├── propagate_claude_config.py       # CLAUDE.md sync
├── propagate_guidelines.sh          # AI guidelines
├── propagate_interactive_mode.sh    # Interactive mode
├── setup_compliance.sh              # Initial setup
├── install_compliance_hooks.sh      # Git hooks
└── verify_compliance.sh             # Verification
```

## Quick Commands

### Full Compliance Setup

```bash
# Setup compliance in all repos
./scripts/compliance/setup_compliance.sh

# Install git hooks
./scripts/compliance/install_compliance_hooks.sh

# Verify compliance
./scripts/compliance/verify_compliance.sh
```

### Propagate Configurations

```bash
# Propagate CLAUDE.md to all repos
python ./scripts/compliance/propagate_claude_config.py

# Propagate AI guidelines
./scripts/compliance/propagate_guidelines.sh

# Enable interactive mode
./scripts/compliance/propagate_interactive_mode.sh
```

## Workflow

### 1. Initial Compliance Setup

```bash
#!/bin/bash
# scripts/compliance/setup_all.sh

# Read repositories
repos=$(cat config/repos.conf | grep -v '^#' | cut -d'=' -f1)

for repo in $repos; do
    if [ -d "$repo" ]; then
        echo "Setting up compliance in $repo..."

        # Create .agent-os structure
        mkdir -p "$repo/.agent-os/product"
        mkdir -p "$repo/.agent-os/specs"

        # Copy product documentation
        cp .agent-os/product/mission.md "$repo/.agent-os/product/"
        cp .agent-os/product/tech-stack.md "$repo/.agent-os/product/"

        # Copy CLAUDE.md
        cp CLAUDE.md "$repo/CLAUDE.md"

        echo "✓ $repo compliance setup complete"
    fi
done
```

### 2. Standards Propagation

```python
# scripts/compliance/propagate_standards.py

def propagate_standards(standard_file, repositories):
    """Propagate standard to all repositories."""
    for repo in repositories:
        target = repo / "docs/standards" / standard_file.name

        # Create directory if needed
        target.parent.mkdir(parents=True, exist_ok=True)

        # Copy standard
        shutil.copy(standard_file, target)

        # Git add
        subprocess.run(
            ["git", "-C", str(repo), "add", str(target)],
            check=True
        )

    print(f"✓ Propagated {standard_file.name} to {len(repositories)} repos")
```

### 3. Git Hooks Installation

```bash
#!/bin/bash
# scripts/compliance/install_hooks_all.sh

for repo in $(cat config/repos.conf | grep -v '^#' | cut -d'=' -f1); do
    if [ -d "$repo/.git" ]; then
        echo "Installing git hooks in $repo..."

        # Copy pre-commit hook
        cp hooks/pre-commit "$repo/.git/hooks/"
        chmod +x "$repo/.git/hooks/pre-commit"

        # Copy post-commit hook
        cp hooks/post-commit "$repo/.git/hooks/"
        chmod +x "$repo/.git/hooks/post-commit"

        echo "✓ Hooks installed in $repo"
    fi
done
```

### 4. Verification

```bash
#!/bin/bash
# scripts/compliance/verify_all.sh

echo "Verifying compliance across all repositories..."

fail_count=0

for repo in $(cat config/repos.conf | grep -v '^#' | cut -d'=' -f1); do
    if [ -d "$repo" ]; then
        echo "Checking $repo..."

        # Check CLAUDE.md exists
        if [ ! -f "$repo/CLAUDE.md" ]; then
            echo "✗ Missing CLAUDE.md"
            ((fail_count++))
        fi

        # Check .agent-os structure
        if [ ! -d "$repo/.agent-os/product" ]; then
            echo "✗ Missing .agent-os/product"
            ((fail_count++))
        fi

        # Check git hooks
        if [ ! -f "$repo/.git/hooks/pre-commit" ]; then
            echo "✗ Missing pre-commit hook"
            ((fail_count++))
        fi
    fi
done

if [ $fail_count -eq 0 ]; then
    echo "✓ All repositories compliant!"
else
    echo "✗ $fail_count compliance issues found"
    exit 1
fi
```

## Standards to Propagate

### Critical Standards

```yaml
standards:
  - name: "AI_AGENT_GUIDELINES.md"
    priority: CRITICAL
    target: "docs/modules/ai/"

  - name: "HTML_REPORTING_STANDARDS.md"
    priority: MANDATORY
    target: "docs/modules/standards/"

  - name: "FILE_ORGANIZATION_STANDARDS.md"
    priority: MANDATORY
    target: "docs/modules/standards/"

  - name: "TESTING_FRAMEWORK_STANDARDS.md"
    priority: MANDATORY
    target: "docs/modules/standards/"

  - name: "LOGGING_STANDARDS.md"
    priority: MANDATORY
    target: "docs/modules/standards/"
```

### Configuration Files

```yaml
configs:
  - name: "CLAUDE.md"
    target: "."

  - name: "tsconfig.json"
    target: "."

  - name: "pytest.ini"
    target: "."

  - name: ".coveragerc"
    target: "."
```

## Selective Propagation

```python
def propagate_selective(standard, filter_func):
    """Propagate to filtered repositories only."""
    all_repos = load_repositories()

    # Filter repositories
    target_repos = [r for r in all_repos if filter_func(r)]

    # Propagate
    propagate_standards(standard, target_repos)
```

**Examples:**

```python
# Propagate to Python repositories only
propagate_selective(
    standard="TESTING_FRAMEWORK_STANDARDS.md",
    filter_func=lambda r: (r / "pyproject.toml").exists()
)

# Propagate to web application repos only
propagate_selective(
    standard="HTML_REPORTING_STANDARDS.md",
    filter_func=lambda r: (r / "package.json").exists()
)
```

## Batch Operations

```bash
# Commit and push compliance changes to all repos
./scripts/repository_sync commit all -m "Update compliance standards"
./scripts/repository_sync push all
```

## Monitoring Compliance

```python
def generate_compliance_report():
    """Generate compliance status report."""
    repos = load_repositories()
    report = []

    for repo in repos:
        status = {
            "repository": repo.name,
            "claude_md": (repo / "CLAUDE.md").exists(),
            "agent_os": (repo / ".agent-os/product").exists(),
            "git_hooks": (repo / ".git/hooks/pre-commit").exists(),
            "standards": check_standards_present(repo),
            "compliant": True
        }

        # Overall compliance
        status["compliant"] = all([
            status["claude_md"],
            status["agent_os"],
            status["git_hooks"],
            len(status["standards"]) >= 4
        ])

        report.append(status)

    return report
```

## Automation Triggers

### Git Hooks (Per Repository)

```bash
# .git/hooks/post-commit
# After committing to workspace-hub, propagate changes

if [ -f "scripts/compliance/auto_propagate.sh" ]; then
    ./scripts/compliance/auto_propagate.sh
fi
```

### CI/CD (Workspace-Hub)

```yaml
# .github/workflows/propagate-compliance.yml
name: Propagate Compliance

on:
  push:
    branches: [main]
    paths:
      - 'docs/modules/standards/**'
      - 'CLAUDE.md'
      - '.agent-os/product/**'

jobs:
  propagate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Propagate Standards
        run: |
          python scripts/compliance/propagate_claude_config.py
          ./scripts/compliance/propagate_guidelines.sh

      - name: Verify Compliance
        run: ./scripts/compliance/verify_compliance.sh
```

---

**Maintain consistency across all 26+ repositories automatically!** 🔄
