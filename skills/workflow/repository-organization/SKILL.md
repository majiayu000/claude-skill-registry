---
name: repository-organization
description: Guidelines for establishing and maintaining a standardized, intuitive, and automated repository environment to minimize technical debt and ensure long-term maintainability.
version: 1.0.0
---

# Project Repository Organization & Maintenance

## 🎯 Purpose
To establish a standardized, intuitive, and automated repository environment that minimizes technical debt, accelerates onboarding, and ensures long-term maintainability.

## 🏗️ Repository Structure (Standardized)
A consistent folder hierarchy is the foundation of a healthy project. Follow the "Logic over Convenience" rule.

```plaintext
├── .github/               # CI/CD workflows, issue templates, and PR templates
├── docs/                  # Project documentation, architecture ADRs, and assets
├── src/                   # Source code (namespaced by domain/module)
├── tests/                 # Unit, integration, and end-to-end tests
├── scripts/               # Utility scripts for setup, migration, or automation
├── data/                  # (If applicable) Sample data or local DB seeds
├── .env.example           # Template for environment variables
├── README.md              # Project entry point
└── SKILL.md               # AI Agent instructions and SOPs
```

## 🛠️ Best Practices for Maintenance

### 1. Git Hygiene & Branching
- **Trunk-Based Development**: Keep the main branch always deployable. Use short-lived feature branches.
- **Atomic Commits**: Each commit should represent a single logical change with a descriptive message (e.g., `feat: add oauth2 provider` instead of `stuff`).
- **Conventional Commits**: Use prefixes like `feat:`, `fix:`, `docs:`, `refactor:`, and `chore:`.

### 2. Automated Governance (CI/CD)
- **Linting & Formatting**: Enforce styles automatically (e.g., Prettier, Black, or ESLint) on every pull request.
- **Dependency Management**: Use automated tools (like Dependabot or Renovate) to keep libraries updated and scan for vulnerabilities.
- **Pre-commit Hooks**: Use `pre-commit` to prevent "broken" code (syntax errors or unformatted code) from ever being committed.

### 3. Documentation as Code
- **README.md**: Must include: "Getting Started," "System Requirements," and "Deployment Steps."
- **ADR (Architecture Decision Records)**: Document why a technology or pattern was chosen to prevent "Chesterton’s Fence" dilemmas later.
- **Inline Documentation**: Code should be self-documenting, but complex logic requires comments explaining the intent, not the action.

## 🧹 Maintenance Workflow

### Weekly "Gardening" Tasks
- [ ] **Stale Branch Cleanup**: Delete merged or abandoned branches older than 14 days.
- [ ] **Issue Triage**: Label new issues and close those that are no longer relevant.
- [ ] **Security Review**: Check for high-severity vulnerabilities in dependencies.

### Monthly Review
- [ ] **Performance Audit**: Review CI/CD build times; optimize slow test suites.
- [ ] **Documentation Sync**: Ensure the `docs/` folder reflects the current state of the production code.

## 📝 Quality Checklist for Pull Requests
- [ ] Does this PR include relevant tests?
- [ ] Is the code formatted according to project standards?
- [ ] Does this change require an update to the README or `docs/`?
- [ ] Are there any new environment variables that need to be added to `.env.example`?
