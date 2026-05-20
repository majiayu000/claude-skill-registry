---
name: architecture-governance
description: Automated fitness functions (ArchUnit) to prevent architectural drift.
role: prod-architect
triggers:
  - architecture test
  - fitness function
  - archunit
  - dependency rule
  - layer check
---

# architecture-governance Skill

Architecture is not a document; it's a constraint system checked by CI/CD.

## 1. Fitness Functions (Automated Tests)
Write tests that verify your architecture, not just your logic.

- **Layering**: "Classes in `Domain` should not depend on `Infrastructure`."
- **Cycles**: "No circular dependencies between slices."
- **Naming**: "All Interfaces should start with `I`" (if that's your rule).
- **Inheritance**: "All Domain Events must implement `IDomainEvent`."

## 2. Tools
- **Java/Kotlin**: ArchUnit.
- **.NET**: NetArchTest.
- **TypeScript**: `dependency-cruiser` or custom ESLint rules (see `agentic-linter`).
- **PHP**: PHPArkitect or Deptrac.

## 3. Examples (Pseudocode)
```typescript
describe('Architecture', () => {
  it('Domain layer should not import Infrastructure', () => {
    const violations = analyzeImports()
      .from('src/domain')
      .to('src/infrastructure');
    expect(violations).toBeEmpty();
  });

  it('All Use Cases should end with UseCase', () => {
    const useCases = classes.in('src/application').thatImplement('IUseCase');
    expect(useCases).toHaveNameEndingWith('UseCase');
  });
});
```

## 4. Governance Policy
- **Breaking the Build**: Architecture violations are treated as compilation errors.
- **Waivers**: If you *must* break a rule, it requires an ADR and a specific `// eslint-disable` comment with the ticket number.
