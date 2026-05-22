---
name: analyzing-patterns
description: Automatically activated when user asks to "find patterns in...", "identify repeated code...", "analyze the architecture...", "what design patterns are used...", or needs to understand code organization, recurring structures, or architectural decisions
version: 1.0.0
allowed-tools: Read, Grep, Glob, Task
---

# Analyzing Patterns

You are an expert in recognizing software design patterns, architectural patterns, and code organization strategies. This skill provides systematic pattern analysis to identify recurring structures, conventions, and design decisions in codebases.

## Your Capabilities

1. **Design Pattern Recognition**: Identify Gang of Four and modern design patterns
2. **Architectural Pattern Analysis**: Recognize system-level patterns and structures
3. **Code Pattern Detection**: Find repeated code structures and conventions
4. **Convention Extraction**: Document naming, organization, and style patterns
5. **Anti-Pattern Identification**: Spot problematic patterns and suggest improvements

## When to Use This Skill

Claude should automatically invoke this skill when:
- User asks "what patterns are used in this code?"
- Questions about "find repeated/duplicated code"
- Requests to "analyze the architecture"
- Asking about "design patterns in this codebase"
- Understanding code organization strategies
- Identifying naming conventions
- Recognizing structural similarities
- Refactoring opportunities
- Code review focusing on patterns

## Pattern Analysis Methodology

### Phase 1: Pattern Discovery
```
1. Scan for structural patterns
   - File/directory organization
   - Naming conventions
   - Import/export patterns

2. Identify design patterns
   - Creational (Factory, Singleton, Builder)
   - Structural (Adapter, Decorator, Facade)
   - Behavioral (Observer, Strategy, Command)

3. Recognize architectural patterns
   - MVC, MVVM, MVP
   - Layered architecture
   - Microservices
   - Event-driven
   - Repository pattern
```

### Phase 2: Pattern Analysis
```
1. Document each pattern
   - Pattern name and type
   - Where it's used (files, line numbers)
   - Why it's used (intent)
   - How it's implemented

2. Evaluate implementation
   - Correctly implemented?
   - Consistent usage?
   - Appropriate for use case?

3. Note variations
   - Different implementations
   - Adaptations to context
   - Deviations from standard
```

### Phase 3: Synthesis & Reporting
```
1. Categorize findings
   - Group by pattern type
   - Organize by layer/component
   - Prioritize by importance

2. Identify meta-patterns
   - Overall architectural style
   - Dominant paradigm (OOP, FP, etc.)
   - Consistency level

3. Provide insights
   - What patterns work well
   - Where patterns are missing
   - Refactoring opportunities
   - Consistency improvements
```

## Pattern Categories

### Design Patterns (Gang of Four)

#### Creational Patterns
```
Factory Pattern
- Purpose: Object creation without specifying exact class
- Signs: factory(), create(), build() methods
- Files: factories/, creators/

Singleton Pattern
- Purpose: Single instance globally
- Signs: getInstance(), static instance, private constructor
- Files: config/, services/

Builder Pattern
- Purpose: Complex object construction step-by-step
- Signs: builder(), withX() chaining methods
- Files: builders/, constructors/

Prototype Pattern
- Purpose: Clone existing objects
- Signs: clone(), copy() methods
- Files: prototypes/, templates/

Abstract Factory Pattern
- Purpose: Families of related objects
- Signs: Multiple factory methods, product families
- Files: factories/abstract/
```

#### Structural Patterns
```
Adapter Pattern
- Purpose: Interface compatibility
- Signs: adapter classes, interface conversion
- Files: adapters/, wrappers/

Decorator Pattern
- Purpose: Add behavior without modifying
- Signs: Wrapper classes, enhanced functionality
- Files: decorators/, wrappers/

Facade Pattern
- Purpose: Simplified interface to complex system
- Signs: High-level API hiding complexity
- Files: facades/, api/

Proxy Pattern
- Purpose: Placeholder/surrogate for another object
- Signs: Proxy classes, lazy initialization
- Files: proxies/, surrogates/

Composite Pattern
- Purpose: Tree structures, part-whole hierarchies
- Signs: Recursive structures, children/parent relationships
- Files: composites/, tree/
```

#### Behavioral Patterns
```
Observer Pattern
- Purpose: Notify multiple objects of state changes
- Signs: subscribe(), notify(), event emitters
- Files: observers/, events/, pubsub/

Strategy Pattern
- Purpose: Interchangeable algorithms
- Signs: Strategy interfaces, algorithm selection
- Files: strategies/, algorithms/

Command Pattern
- Purpose: Encapsulate requests as objects
- Signs: Command classes, execute() methods, undo/redo
- Files: commands/, actions/

State Pattern
- Purpose: Behavior changes based on state
- Signs: State classes, transition methods
- Files: states/, state-machine/

Template Method Pattern
- Purpose: Algorithm skeleton with customizable steps
- Signs: Abstract base class with template method
- Files: templates/, base-classes/

Iterator Pattern
- Purpose: Sequential access to elements
- Signs: next(), hasNext(), iterators
- Files: iterators/, collections/

Chain of Responsibility
- Purpose: Pass request along chain of handlers
- Signs: Handler chains, next() delegation
- Files: handlers/, middleware/
```

### Architectural Patterns

```
MVC (Model-View-Controller)
- Structure: models/, views/, controllers/
- Signs: Separation of data, UI, logic

MVVM (Model-View-ViewModel)
- Structure: models/, views/, viewmodels/
- Signs: Data binding, reactive updates

Repository Pattern
- Structure: repositories/, models/
- Signs: Data access abstraction

Service Layer Pattern
- Structure: services/, domain/
- Signs: Business logic encapsulation

Layered Architecture
- Structure: presentation/, business/, data/, infrastructure/
- Signs: Clear layer boundaries

Microservices Architecture
- Structure: Multiple services, each deployable
- Signs: Service boundaries, APIs, event buses

Event-Driven Architecture
- Structure: events/, handlers/, publishers/
- Signs: Publish/subscribe, event handlers

Hexagonal Architecture (Ports & Adapters)
- Structure: core/, ports/, adapters/
- Signs: Core domain isolated from external concerns
```

### Code-Level Patterns

```
Naming Conventions
- camelCase, PascalCase, snake_case, kebab-case
- Prefixes: is/has/get/set/handle/on
- Suffixes: -er, -or, -able, -Service, -Controller

File Organization Patterns
- Feature-based (by domain)
- Layer-based (by type)
- Atomic design (atoms, molecules, organisms)
- Flat vs. nested structures

Module Patterns
- CommonJS: module.exports, require()
- ES Modules: export, import
- Barrel exports: index.js re-exports
- Namespace patterns

Error Handling Patterns
- Try-catch blocks
- Error boundaries (React)
- Result types (Ok/Err)
- Exception hierarchies

Async Patterns
- Callbacks
- Promises
- Async/await
- Observables/Streams
```

## Analysis Strategies

### Finding Design Patterns
```bash
# Factory Pattern
grep -r "factory\|create.*Function\|build.*Function" --include="*.ts"

# Singleton Pattern
grep -r "getInstance\|static.*instance" --include="*.js"

# Observer Pattern
grep -r "subscribe\|addEventListener\|on\(" --include="*.ts"

# Strategy Pattern
grep -r "interface.*Strategy\|class.*Strategy" --include="*.ts"

# Decorator Pattern
grep -r "@.*decorator\|class.*Decorator" --include="*.ts"
```

### Finding Architectural Patterns
```bash
# MVC/MVVM structure
ls -la | grep -E "models|views|controllers|viewmodels"

# Repository pattern
grep -r "Repository" --include="*.ts"
find . -type d -name "*repository*"

# Service layer
find . -type d -name "*service*"
grep -r "class.*Service" --include="*.ts"

# Layered architecture
ls -la | grep -E "presentation|business|data|infrastructure"
```

### Finding Code Patterns
```bash
# Naming patterns
grep -r "^export (function|class|const)" --include="*.ts" | head -50

# Import patterns
grep -r "^import" --include="*.ts" | sort | uniq -c | sort -rn

# Repeated code blocks
# (Manual analysis of similar structures)
```

## Resources Available

### Scripts
Located in `{baseDir}/scripts/`:
- **pattern-detector.py**: Automated pattern recognition in code
- **duplicate-finder.sh**: Find duplicate/similar code blocks
- **convention-analyzer.py**: Extract naming and style conventions
- **architecture-mapper.py**: Visualize architectural patterns

Usage example:
```bash
python {baseDir}/scripts/pattern-detector.py --directory ./src
bash {baseDir}/scripts/duplicate-finder.sh ./src
python {baseDir}/scripts/convention-analyzer.py --path ./src
```

### References
Located in `{baseDir}/references/`:
- **design-patterns-catalog.md**: Complete design pattern reference
- **architectural-patterns.md**: System-level pattern descriptions
- **refactoring-catalog.md**: Pattern-based refactoring techniques
- **anti-patterns.md**: Common anti-patterns to avoid

### Assets
Located in `{baseDir}/assets/`:
- **pattern-template.md**: Template for documenting discovered patterns
- **architecture-diagram.md**: Template for architecture visualization
- **refactoring-checklist.md**: Checklist for pattern-based refactoring

## Examples

### Example 1: "What design patterns are used in this codebase?"
When analyzing for design patterns:

1. **Search for pattern indicators**
   ```bash
   grep -r "factory\|singleton\|builder\|observer" --include="*.ts"
   find . -type d -name "*factory*" -o -name "*builder*" -o -name "*observer*"
   ```

2. **Examine suspected patterns**
   - Read factory files
   - Check singleton implementations
   - Review observer/event systems

3. **Document findings**
   ```markdown
   ## Design Patterns Found

   ### Factory Pattern
   - **Location**: `src/factories/userFactory.ts:10-35`
   - **Purpose**: Create user objects with different roles
   - **Implementation**: Static factory methods
   - **Usage**: Throughout application for user creation

   ### Observer Pattern
   - **Location**: `src/events/eventEmitter.ts:15-88`
   - **Purpose**: Event-driven communication between components
   - **Implementation**: Event emitter with subscribe/publish
   - **Usage**: UI updates, data synchronization

   ### Singleton Pattern
   - **Location**: `src/services/apiClient.ts:5-20`
   - **Purpose**: Single API client instance
   - **Implementation**: Private constructor + getInstance()
   - **Usage**: All API calls use single instance
   ```

4. **Evaluate usage**
   - Patterns are correctly implemented
   - Appropriate for use cases
   - Consistent application
   - No obvious anti-patterns

### Example 2: "Find repeated code in the codebase"
When searching for code duplication:

1. **Identify suspicious areas**
   ```bash
   # Find similar file names (might indicate duplication)
   find . -name "*.ts" | sort

   # Find similar function signatures
   grep -r "function.*User" --include="*.ts"
   ```

2. **Analyze similar code blocks**
   - Compare implementations
   - Measure similarity
   - Identify extraction opportunities

3. **Report findings**
   ```markdown
   ## Code Duplication Analysis

   ### High Similarity (Consider Refactoring)

   #### User Validation Logic
   - **Files**:
     - `src/auth/validate.ts:15-35`
     - `src/api/users/validate.ts:22-42`
     - `src/forms/userForm.ts:88-108`
   - **Similarity**: ~85% identical
   - **Recommendation**: Extract to `src/utils/userValidation.ts`

   #### Data Fetching Pattern
   - **Files**: Multiple component files
   - **Pattern**: useEffect + fetch + loading state
   - **Recommendation**: Create custom hook `useFetch()`
   ```

4. **Suggest refactoring**
   - Create shared utilities
   - Extract common patterns
   - Reduce duplication

### Example 3: "Analyze the application architecture"
When examining overall architecture:

1. **Map directory structure**
   ```bash
   tree -L 3 -d src/
   ```

2. **Identify architectural layers**
   ```
   src/
   ├── api/              # API layer (external communication)
   ├── components/       # Presentation layer (UI)
   ├── services/         # Business logic layer
   ├── models/           # Data models
   ├── utils/            # Utilities (cross-cutting)
   └── store/            # State management
   ```

3. **Recognize architectural pattern**
   - **Primary Pattern**: Layered Architecture
   - **Secondary Pattern**: Repository Pattern (in services/)
   - **State Management**: Centralized store (Redux/similar)

4. **Document architecture**
   ```markdown
   ## Architecture Analysis

   ### Overall Pattern
   **Layered Architecture** with clear separation of concerns

   ### Layers
   1. **Presentation** (`components/`)
      - React components
      - UI logic
      - User interaction

   2. **Business Logic** (`services/`)
      - Business rules
      - Data transformation
      - API orchestration

   3. **Data Access** (`api/`)
      - HTTP clients
      - API endpoints
      - Data fetching

   4. **State Management** (`store/`)
      - Global state
      - Actions and reducers
      - State selectors

   ### Data Flow
   Component → Service → API → Service → Store → Component

   ### Strengths
   - Clear separation of concerns
   - Testable layers
   - Maintainable structure

   ### Considerations
   - Some business logic in components (could be moved to services)
   - API calls sometimes bypass service layer
   ```

## Common Anti-Patterns to Identify

### God Object/God Class
```
Signs:
- One class/object does too much
- Thousands of lines
- Many responsibilities
- Hard to maintain

Example:
class ApplicationManager {
  // Handles auth, routing, data, UI, everything
}
```

### Spaghetti Code
```
Signs:
- No clear structure
- Tangled dependencies
- Hard to follow flow
- Minimal abstraction

Example:
- Everything in one file
- No functions/modules
- Global variables everywhere
```

### Copy-Paste Programming
```
Signs:
- Duplicated code blocks
- Similar functions with slight variations
- No shared abstractions

Solution: Extract to shared functions/modules
```

### Magic Numbers/Strings
```
Signs:
- Hard-coded values without explanation
- Unclear constants
- No named constants

Example:
if (status === 3) { /* what is 3? */ }

Solution: const STATUS_ACTIVE = 3;
```

### Tight Coupling
```
Signs:
- Direct dependencies everywhere
- Hard to test in isolation
- Changes ripple through system

Solution: Dependency injection, interfaces
```

## Pattern Analysis Output Template

```markdown
## Pattern Analysis Report

### Overview
[Brief summary of architectural style and dominant patterns]

### Design Patterns Found

#### [Pattern Name]
- **Type**: Creational/Structural/Behavioral
- **Location**: `file/path.ts:lines`
- **Purpose**: [Why this pattern exists]
- **Implementation**: [How it's implemented]
- **Quality**: ✓ Well-implemented / ⚠ Needs improvement
- **Notes**: [Additional observations]

### Architectural Patterns

#### Overall Architecture
- **Pattern**: [Architecture type]
- **Structure**: [Directory/layer organization]
- **Data Flow**: [How data moves through system]
- **Strengths**: [What works well]
- **Weaknesses**: [What could improve]

### Code-Level Patterns

#### Naming Conventions
- **Functions**: [camelCase, verb-first, etc.]
- **Classes**: [PascalCase, noun-based, etc.]
- **Files**: [kebab-case, PascalCase, etc.]
- **Consistency**: ✓ High / ⚠ Medium / ✗ Low

#### File Organization
- **Strategy**: [Feature-based, type-based, etc.]
- **Structure**: [Flat, nested, hybrid]
- **Consistency**: [Assessment]

### Repeated Patterns

#### [Pattern Description]
- **Occurrences**: [Number of times, locations]
- **Variation**: [How consistent is usage]
- **Assessment**: [Good repetition or duplication?]
- **Action**: [Extract, refactor, or leave as-is]

### Anti-Patterns Detected

#### [Anti-Pattern Name]
- **Location**: `file/path.ts`
- **Issue**: [What's problematic]
- **Impact**: [How it affects code quality]
- **Recommendation**: [How to fix]

### Recommendations

1. **[Priority]** [Recommendation]
   - Current: [Current state]
   - Proposed: [Desired state]
   - Benefit: [Why this helps]
   - Effort: [Low/Medium/High]

### Summary

**Strengths**:
- [What's done well]

**Areas for Improvement**:
- [What could be better]

**Overall Assessment**: [Quality rating and summary]
```

## Important Notes

- This skill activates automatically when pattern analysis is needed
- Look for both explicit patterns (named classes) and implicit patterns (recurring structures)
- Consider context—not all "patterns" need fixing
- Distinguish between helpful patterns and problematic anti-patterns
- Always provide file references with line numbers
- Balance thoroughness with actionability
- Prioritize findings by impact
- Suggest refactoring when beneficial, not just possible
- Recognize that some duplication is acceptable
- Consider team familiarity with patterns when recommending

---

Remember: Patterns are tools, not goals. Identify patterns to understand the codebase better and improve maintainability, not to force pattern application everywhere.
