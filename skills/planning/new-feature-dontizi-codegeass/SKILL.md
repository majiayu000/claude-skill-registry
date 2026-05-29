---
name: new-feature
description: Plan new features/integrations following SOLID principles. Analyzes codebase architecture, researches official documentation and best practices, designs extensible solution, and creates comprehensive GitHub issue with implementation blueprint.
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(gh *), WebSearch, WebFetch
disable-model-invocation: true
---

# Plan New Feature: $ARGUMENTS

You are a Senior Software Architect planning a new feature or integration for CodeGeass.

**Target**: $ARGUMENTS

Your deliverable is a **comprehensive GitHub issue** with the complete implementation blueprint. You do NOT write code - you create the plan.

---

## Phase 1: Deep Codebase Analysis

### 1.1 Identify Related Subsystems

Understand where this feature fits in the architecture:

```bash
# Repository structure
ls -la src/codegeass/
```

**Subsystem mapping:**
- Notification provider (WhatsApp, Slack) → `src/codegeass/notifications/`
- Storage backend (PostgreSQL, Redis) → `src/codegeass/storage/`
- Execution strategy → `src/codegeass/execution/`
- CLI command → `src/codegeass/cli/commands/`

### 1.2 Find Gold Standard Patterns

CodeGeass uses these architectural patterns:

| Pattern | Location | Example |
|---------|----------|---------|
| Strategy + ABC | `notifications/providers/base.py` | `NotificationProvider` |
| Registry + Lazy Loading | `notifications/registry.py` | `ProviderRegistry` |
| Protocol Interfaces | `storage/protocols.py` | `TaskRepositoryProtocol` |
| Factory | `factory/` | `TaskFactory`, `SkillRegistry` |

Read the relevant pattern files based on feature type.

### 1.3 Reference Implementation

Find a similar existing implementation:
- For notification → study `TelegramProvider` (~430 lines)
- For storage → study `yaml_backend.py`
- For execution → study `strategies.py`

Read thoroughly - this is your template.

### 1.4 Dependency Graph

```bash
# What depends on modules you'll modify
grep -r "from codegeass.<module>" src/ --include="*.py"
```

---

## Phase 2: Research Best Practices

### 2.1 Official Documentation

**REQUIRED**: Fetch official documentation for the integration.

Example searches for notification providers:
```
WebSearch: "<service> API documentation 2026"
WebSearch: "<service> Python SDK official"
WebSearch: "<service> authentication best practices"
```

Then fetch the official docs:
```
WebFetch: <official-api-docs-url>
```

### 2.2 Community Patterns

```
WebSearch: "<feature> Python implementation patterns"
WebSearch: "<library> production best practices"
```

### 2.3 Security Research

```
WebSearch: "<service> API security best practices"
WebSearch: "<credential-type> secure storage Python"
```

### 2.4 Create Research Summary

| Topic | Source | Key Findings |
|-------|--------|--------------|
| Official API | [URL] | Auth, rate limits, endpoints |
| Python SDK | [Package] | Version, patterns |
| Security | [Source] | Credential handling |

---

## Phase 3: Architecture Design

### 3.1 SOLID Compliance Check

For each new component:

| Principle | Question | Your Answer |
|-----------|----------|-------------|
| **S**ingle Responsibility | What's the ONE reason this would change? | |
| **O**pen/Closed | Can I extend without modifying existing code? | |
| **L**iskov Substitution | Can new class replace any sibling implementation? | |
| **I**nterface Segregation | Are all interface methods needed by clients? | |
| **D**ependency Inversion | Am I depending on abstractions (ABC/Protocol)? | |

### 3.2 Design Pattern Selection

Based on CodeGeass patterns:

- **Strategy Pattern** → Multiple interchangeable implementations
- **Factory Pattern** → Complex object creation
- **Registry Pattern** → Discovery and lazy loading
- **Repository Pattern** → Data access abstraction

### 3.3 Interface Design

Define the contract:

```python
# Example for new notification provider
class NewProvider(NotificationProvider):
    @property
    def name(self) -> str: ...

    async def send(self, channel, credentials, message, **kwargs) -> dict: ...

    def validate_config(self, config) -> tuple[bool, str | None]: ...

    def validate_credentials(self, credentials) -> tuple[bool, str | None]: ...

    async def test_connection(self, channel, credentials) -> tuple[bool, str]: ...

    def get_config_schema(self) -> ProviderConfig: ...
```

---

## Phase 4: Implementation Plan

### 4.1 Files to Create

| File Path | Purpose | Est. Lines |
|-----------|---------|------------|
| `src/codegeass/<path>/<new>.py` | Main implementation | 50-150 |

### 4.2 Files to Modify

| File Path | Change |
|-----------|--------|
| `<registry>.py` | Register new component |
| `pyproject.toml` | Add optional dependency |
| `cli/commands/<cmd>.py` | CLI support (if needed) |

### 4.3 Implementation Order

1. Create interface/ABC extensions (if any)
2. Create models/value objects
3. Create exceptions
4. Implement core logic
5. Register with factory/registry
6. Add CLI support
7. Add Dashboard support (if needed)
8. Add tests

### 4.4 Breaking Changes

| Change | Breaking? | Migration |
|--------|-----------|-----------|
| New optional param | No | Default maintains compat |
| New required param | Yes | Version bump needed |

### 4.5 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `<pkg>` | `^x.y.z` | Why needed |

---

## Phase 5: Testing Strategy

### 5.1 Unit Tests

| Test File | Coverage |
|-----------|----------|
| `tests/test_<component>.py` | Core logic |

### 5.2 Integration Tests

| Scenario | Description |
|----------|-------------|
| Happy path | Full feature workflow |
| Error handling | Exception paths |
| Edge cases | Boundaries |

### 5.3 Manual Verification

```bash
# After implementation
codegeass <command>
python -c "from codegeass.<module> import <Class>"
mypy src/codegeass/<path>
ruff check src/codegeass/<path>
```

---

## Phase 6: Create GitHub Issue

**FINAL DELIVERABLE**: Create comprehensive issue.

```bash
gh issue create --title "feat(<scope>): $ARGUMENTS" --label "enhancement,planning" --body "$(cat <<'EOF'
## Summary

<1-2 sentence summary>

## Motivation

<Why is this needed? What problem does it solve?>

---

## Research Summary

### Official Documentation
- [API Docs](<url>): <key findings>
- [SDK](<url>): <package and version>

### Security Considerations
- <credential handling>
- <validation requirements>

---

## Architecture Analysis

### Existing Patterns to Follow

| Pattern | Location | Application |
|---------|----------|-------------|
| <Pattern> | `<path>` | <how we'll use it> |

### SOLID Compliance

- [x] Single Responsibility: <explanation>
- [x] Open/Closed: <explanation>
- [x] Liskov Substitution: <explanation>
- [x] Interface Segregation: <explanation>
- [x] Dependency Inversion: <explanation>

### Reference Implementation
Using `<file>` as template because: <reason>

---

## Technical Approach

### New Files

| File | Purpose |
|------|---------|
| `src/codegeass/<path>/<file>.py` | <description> |

### Modified Files

| File | Change |
|------|--------|
| `src/codegeass/<path>/<file>.py` | <modification> |

### Interface Design

```python
class NewComponent(BaseClass):
    """Brief description."""

    def method(self, param: Type) -> ReturnType:
        ...
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `<pkg>` | `^x.y.z` | <why> |

---

## Implementation Checklist

### Core
- [ ] Create `<file>.py` with <Component>
- [ ] Implement abstract methods
- [ ] Add validation logic
- [ ] Handle errors with custom exceptions

### Integration
- [ ] Register in `<registry>.py`
- [ ] Add to `__init__.py` exports
- [ ] Add optional dependency to `pyproject.toml`

### CLI (if applicable)
- [ ] Add command in `cli/commands/`
- [ ] Update help text

### Dashboard (if applicable)
- [ ] Add API endpoint in `dashboard/backend/routers/`
- [ ] Add frontend in `dashboard/frontend/src/`

### Testing
- [ ] Unit tests in `tests/`
- [ ] Integration tests
- [ ] Manual verification

### Documentation
- [ ] Update CLAUDE.md if patterns change
- [ ] Add usage examples

---

## Testing Strategy

### Unit Tests
```python
def test_<component>_<scenario>():
    # Arrange / Act / Assert
```

### Manual Verification
```bash
codegeass <command>
```

---

## Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| <option> | <pros> | <cons> | <why> |

---

## References

- [Official Docs](<url>)
- [Related Code](<path>)
EOF
)"
```

---

## Output Checklist

Before creating the issue:

- [ ] Codebase analysis complete
- [ ] Official documentation fetched and summarized
- [ ] Architecture designed with SOLID compliance
- [ ] Implementation plan detailed
- [ ] Testing strategy defined
- [ ] GitHub issue created
