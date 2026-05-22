---
description: Ruby on Rails backend development patterns for [PROJECT_NAME]
globs:
  - "app/**/*.rb"
  - "lib/**/*.rb"
  - "config/**/*.rb"
  - "db/**/*.rb"
alwaysApply: false
---

# Rails Backend Skill

> Project: [PROJECT_NAME]
> Framework: Ruby on Rails [VERSION]
> Generated: [DATE]

## Quick Reference

### Service Objects
- One class per use case
- `call` method as entry point
- Return Result objects (success/failure)

### Models
- Thin models, fat services
- Validations in model
- Business logic in services

### Controllers
- Thin controllers
- Delegate to services
- Standard REST actions

### Testing
- RSpec for unit/integration tests
- FactoryBot for test data
- Shoulda Matchers for model specs

## Available Modules

| Module | File | Use When |
|--------|------|----------|
| Service Patterns | services.md | Business logic, use cases |
| Model Patterns | models.md | ActiveRecord, validations |
| API Design | api-design.md | Controllers, serializers |
| Testing | testing.md | RSpec, factories |
| Dos and Don'ts | dos-and-donts.md | Project-specific learnings |

## Project Context

### Tech Stack
<!-- Extracted from agent-os/product/tech-stack.md -->
- **Framework:** Ruby on Rails [RAILS_VERSION]
- **Ruby Version:** [RUBY_VERSION]
- **Database:** [DATABASE]
- **Testing:** [TESTING_FRAMEWORK]
- **Background Jobs:** [BACKGROUND_JOBS]
- **Authentication:** [AUTH_LIBRARY]

### Architecture Patterns
<!-- Extracted from agent-os/product/architecture-decision.md -->

**Service Layer:**
[SERVICE_LAYER_PATTERN]

**API Design:**
[API_DESIGN_PATTERN]

**Data Access:**
[DATA_ACCESS_PATTERN]

**Error Handling:**
[ERROR_HANDLING_PATTERN]

### Project Structure
<!-- Extracted from agent-os/product/architecture-structure.md -->
```
[PROJECT_STRUCTURE]
```

### Naming Conventions
[NAMING_CONVENTIONS]

---

## Self-Learning

Wenn du während der Implementierung etwas lernst:
→ Füge es zu `dos-and-donts.md` in diesem Ordner hinzu.
