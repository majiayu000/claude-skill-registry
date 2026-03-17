---
name: mvp-design
description: Design Minimum Viable Prototype code following "code-as-documentation" principles. Produces architecture-focused documentation without code snippets, emphasizing design decisions over implementation details.
version: 1.0
---

# MVP Design Skill

Design minimal, production-ready code prototypes with clear architecture and self-documenting code.

## When to Use

Use this skill when you need to:
- Design a new module or subsystem from scratch
- Create a minimal viable prototype (MVP) for rapid iteration
- Establish coding patterns and architectural decisions
- Plan implementation before writing actual code
- Design replacement systems alongside existing ones

## Core Principles

### 1. Code as Documentation
- **Code itself is readable** - clear naming, simple structure
- **Minimal comments** - code explains itself
- **Self-documenting functions** - verb-based naming, obvious parameters

### 2. Documentation as Design
- **No code in documentation** - code lives in the project
- **Document "why", not "how"** - architectural decisions and rationale
- **Focus on design patterns** - data flow, component interaction
- **Interface contracts** - what goes in, what comes out

### 3. Minimal Viable Scope
- **5-6 files maximum** - forces focus on essentials
- **500 lines of code** - small enough to complete quickly
- **Core functionality only** - defer edge cases to later phases

### 4. Architectural Alignment
- **Use existing infrastructure** - leverage project's patterns
- **Follow established conventions** - naming, structure, serialization
- **Zero-intrusive design** - parallel development, not replacement

## Workflow

### Phase 1: Architecture Definition

1. Identify Core Data Structure
   - What is the fundamental entity?
   - Example: MissionInstance (id, kind, status, progress, target)

2. Define Primary Operations
   - What actions can be performed?
   - Example: Participate, AddProgress, AcceptReward

3. Map Infrastructure Dependencies
   - What existing systems to leverage?
   - Example: Tinker serialization, SharedTable config, NetMessage

4. Establish Design Decisions
   - Document "why" for each major choice
   - Example: "Use Save/Load methods for Tinker compatibility"

### Phase 2: Component Design

1. List Required Files
   - Header + Implementation pairs
   - Configuration files
   - Maximum 6 files

2. Define Component Responsibilities
   - What each file does
   - How components interact

3. Design Data Flow
   - Input → Processing → Output
   - Serialization path
   - Database interaction

4. Specify Interface Contracts
   - Function signatures
   - Input/output types
   - Error handling approach

### Phase 3: Documentation Production

**Structure**:
```markdown
# [ModuleName] MVP Design

## 1. Core Architecture
[Architecture diagram showing components and relationships]

## 2. File Inventory
| File | Path | Responsibility |

## 3. Key Design Decisions
[Document "why" for each major decision]

## 4. Implementation Checklist
[Phase-by-phase checklist]

## 5. Integration Points
[How it connects to existing systems]

## 6. Testing Strategy
[How to verify it works]
```

## Design Decisions Template

For each major decision, document:

```markdown
### Decision: [Name]

**Choice**: [What was decided]

**Alternatives Considered**:
- Option A: [Description] → Rejected because [reason]
- Option B: [Description] → Rejected because [reason]

**Rationale**:
- [Why this choice]
- [Benefits]
- [Trade-offs]

**Impact**:
- [How it affects other components]
- [Future considerations]
```

## Best Practices

### ✅ Do
- Focus on architecture and design
- Document "why" not "how"
- Keep scope minimal (5-6 files)
- Align with existing patterns
- Use clear, consistent naming

### ❌ Don't
- Include actual code in documentation
- Over-engineer for edge cases
- Ignore existing conventions
- Skip design rationale
- Expand scope mid-design

## Example Output Structure

```markdown
# PlayerMissionSystem MVP Design

## 1. Core Architecture

```
[MissionInstance] → [PlayerMissionSystem] → [DatabaseMethod]
                         ↓
                   [MissionConfigData]
```

## 2. File Inventory

| File | Path | Responsibility |
|------|------|----------------|
| MissionDefines.h | WorldServer/ | Enums and utilities |
| MissionInstance.h | WorldServer/ | Data structure with Save/Load |
| PlayerMissionSystem.h/cpp | WorldServer/ | Core system implementation |

## 3. Key Design Decisions

### Decision: Use Tinker Save/Load

**Choice**: MissionInstance uses Tinker Save/Load methods

**Alternatives**:
- RTS_PACK → Rejected: bitwise copy too restrictive
- Manual serialization → Rejected: error-prone

**Rationale**:
- Type-safe, extensible
- Consistent with project direction
- Easy to add fields later

## 4. Implementation Checklist

### Phase 1: Data Structures
- [ ] MissionInstance with Save/Load
- [ ] MissionConfigData table structure

### Phase 2: Core System
- [ ] PlayerMissionSystem class
- [ ] Participate, AddProgress, AcceptReward methods

### Phase 3: Integration
- [ ] DatabaseMethod additions
- [ ] Player.h integration

## 5. Integration Points

- Uses: Tinker serialization, SharedTable, NetMessage
- Extends: PlayerSubsystem pattern
- Database: player_mission table

## 6. Testing Strategy

- Unit: MissionInstance Save/Load roundtrip
- Integration: Login → Load → Update → Verify
```

## Integration with Other Skills

- **code-analysis**: Understand existing patterns before designing
- **code-generator**: Generate implementation from design docs
- **knowledge-base-cache**: Store design patterns for reuse

## Version History

- v1.0 (2026-02-10) - Initial release
  - Code-as-documentation principles
  - 3-phase workflow
  - Design decision template
