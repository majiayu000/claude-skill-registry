---
name: dapp-sdd:plan
description: Use when creating a phased implementation plan from a specification, with review gates after each phase.
---

# Plan Skill

Creates a phased implementation plan with mandatory review gates.

## Input

- `.dapp-sdd/spec.md` - The expanded specification
- `dapp-sdd:constitution` - Quality standards to follow

## Output

A phased plan saved to `.dapp-sdd/plan.md` with:
- Clear phases (small, focused chunks)
- Review gates after each phase
- Skill references for each task

## Phase Structure

Every plan follows this structure:

### Phase 1: Project Setup
- Verify `create-mn-app` scaffold
- Set up linting/formatting
- Configure TypeScript strict mode
- Add `.dapp-sdd/` to `.gitignore`
- **REVIEW GATE**

### Phase 2: Contract Implementation
- Create contract skeleton
- Implement core circuits
- Add state management
- **REVIEW GATE**

### Phase 3: TypeScript Integration
- Create deployment script
- Create CLI interface
- Add provider configuration
- **REVIEW GATE**

### Phase 4: Testing
- Write contract unit tests
- Write integration tests
- Verify all tests pass
- **REVIEW GATE**

### Phase 5: Documentation & Polish
- Update README with final documentation
- Add educational comments
- Clean up code
- **FINAL REVIEW GATE**

## Plan Format

```markdown
# {DApp Name} Implementation Plan

## Phase 1: Project Setup

**Goal:** Establish project foundation with quality tooling

### Tasks
1. Verify create-mn-app scaffold is complete
2. Configure ESLint with strict rules
3. Configure Prettier for formatting
4. Verify TypeScript strict mode
5. Add `.dapp-sdd/` to `.gitignore`

**Skills:** `midnight-tooling:midnight-setup`

### Review Gate
- [ ] `compact-reviewer:compact-reviewer` (if contracts exist)
- [ ] `devs:code-reviewer`

---

## Phase 2: Contract Implementation

**Goal:** Implement the Compact smart contract

### Tasks
1. Create contract skeleton in `contracts/{name}.compact`
2. Define ledger state
3. Implement circuit: `{circuit_name}`
4. Add witness functions

**Skills:** `compact-core:language-reference`, `compact-core:contract-patterns`, `compact-core:standard-library`

### Review Gate
- [ ] `compact-reviewer:compact-reviewer`
- [ ] `devs:code-reviewer`

---

(Continue for remaining phases...)
```

## Process

1. Load specification from `.dapp-sdd/spec.md`
2. Load constitution from `dapp-sdd:constitution`
3. Analyze user stories to determine complexity
4. Create appropriate number of phases (typically 4-5)
5. Assign tasks to phases based on dependencies
6. Add review gates after each phase
7. Reference appropriate skills for each phase
8. Save to `.dapp-sdd/plan.md`

## Skill References

Reference these skills in the plan:
- `compact-core:contract-patterns` - Contract design patterns
- `compact-core:typescript-integration` - TS integration patterns
- `midnight-proofs:*` - Proof generation approach
- `midnight-tooling:midnight-setup` - Tooling configuration
