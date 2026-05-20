---
name: software-engineer
description: Core software engineering philosophy and design principles based on Structure and Interpretation of Computer Programs (SICP). Use for all software development tasks including writing code, designing systems, refactoring, or making architectural decisions. MUST ALWAYS be loaded when working on any kind of software development or design task!
---

# Software Engineer

<skill_scope skill="software-engineer">
## Overview

This skill provides fundamental software engineering philosophy and design principles derived from _Structure and Interpretation of Computer Programs_ (SICP) by Abelson and Sussman. Apply these principles to all software development work to create well-designed, maintainable, and robust systems.

**Related skills:**
- `functional-programmer` — Functional paradigm principles and patterns
- `object-oriented-programmer` — OOP principles including SOLID
- `logic-programmer` — Logic/relational programming patterns
- `test-driven-development` — Testing philosophy and practices
- `git-version-control` — Version control workflows
</skill_scope>

<core_philosophy>
## Core Philosophy

<program_as_expression>
### Program as Expression of Ideas

Computer programming is fundamentally about expressing ideas, not just getting computers to do things. Code is written for humans to read and understand; execution by computers is incidental. Prioritize clarity and expressiveness in all code.
</program_as_expression>

<utilitarian_code>
### Write Utilitarian Code

Code exists to solve problems, not to demonstrate cleverness. Write code that does what's right because it's right, not because it's an opportunity to show off language features or clever tricks.

**Utilitarian principles:**
- Choose the simplest approach that solves the problem correctly
- Don't write clever code for the writer's satisfaction—but do use advanced techniques when they're genuinely the best tool
- A boring solution that works is better than an elegant solution that confuses
- Cleverness for its own sake is a cost; cleverness that solves a real problem is engineering
- If a technique requires explanation, that's fine—just make sure the explanation is "this is the right approach" not "I wanted to try this," and document it thoroughly

**The test:** Would a tired engineer at 2am understand this code? If not, simplify it.
</utilitarian_code>

<manage_complexity>
### Manage Complexity Through Abstraction

Complexity is the primary challenge in software engineering. Combat complexity through:

1. **Procedural abstraction** - Encapsulate operations as procedures/functions with clear contracts
2. **Data abstraction** - Separate the use of data from its representation
3. **Conventional interfaces** - Use standard protocols to combine components
4. **Linguistic abstraction** - Create domain-specific languages when appropriate

> "Piles of kludges make a big complicated mess." — Gerald Jay Sussman
</manage_complexity>

<naming_and_scope>
### Control Through Naming and Scope

Use naming and scope to control what parts of the program can see and affect other parts. Well-chosen names make programs self-documenting. Minimize scope to reduce coupling and increase modularity.
</naming_and_scope>

<language_layers>
### Build Language Layers

Complex systems benefit from layers of language, where each layer provides abstractions for the layer above. Design programs as a series of language levels, each suitable for expressing ideas at that level of abstraction.

> "You can gain control of complexity by inventing new languages sometimes." — Hal Abelson
</language_layers>

<delayed_commitment>
### Delayed Commitment

Defer decisions about implementation details to maintain flexibility in discovering the right interfaces. The goal is not delay for its own sake, but rather:

- **Explore interface ergonomics**: Experiment with different API designs to find the most natural interaction patterns for consumers
- **Separate interface from implementation**: Design and refine public interfaces before committing to internal representations
- **Maintain flexibility**: Keep implementation options open until the best abstraction boundaries are clear
- **Finalize deliberately**: Once interfaces provide ergonomic interactions, then commit to specific implementations

The commitment being delayed is to internal representations and algorithms, not to understanding what makes a good interface. Use scaffolding and test-writing to explore interface designs before implementation.
</delayed_commitment>
</core_philosophy>

<code_as_ontology>
## Code as Ontology: Names, Stability, and Evolution

Public APIs are ontologies—systems of names carrying semantic commitments. This perspective, drawn from knowledge representation, shapes how we approach API design and system evolution.[^hickey-speculation]

<semantic_commitments>
### Names Create Semantic Commitments

When you name something in a public API, you make a promise about what that name means. `User`, `createAccount`, `/api/users`—these establish concepts in your system's ontology. Changing what a name means changes the ontology itself.

**Design implications:**
- Choose names carefully; they're long-term commitments
- Names should reveal semantic concepts, not implementation details
- Never reuse names for different concepts (even across versions)
- When meaning must change, create a new name
</semantic_commitments>

<open_world_assumption>
### The Open-World Assumption

Design systems as if unknown facts might exist. From knowledge representation: what you don't know might be true, not merely false.

**In practice:** Data structures should tolerate unknown fields. Systems should ignore what they don't understand. Don't fail on unexpected information.

```javascript
// Open-world: tolerates unknown fields
function processUser(user) {
  const { id, name, email } = user;
  // Ignores any other fields—system can evolve independently
  return { id, processedName: name.toUpperCase(), email };
}
```

**Why this matters:** Enables independent evolution of clients and servers. Adding capabilities doesn't break existing code. Systems compose safely.
</open_world_assumption>

<accretion_framework>
### Growth Through Accretion

Rich Hickey's accretion/breakage framework[^hickey-speculation] provides clear criteria for compatible changes:

**Compatible changes (accretion):**
- Require less from callers (make required parameters optional)
- Provide more to callers (add fields, return more information)
- Add new functions/endpoints alongside existing ones

**Breaking changes:**
- Require more from callers (add required parameters)
- Provide less to callers (remove fields, return less)
- Change semantics under the same name

```python
# Accretion: add alongside, don't modify
def create_user(name, email):           # Original—still works
    ...

def create_user_with_role(name, email, role):  # New capability
    ...

# Or relax requirements:
def create_user(name, email, role=None):  # Backward compatible
    ...
```

**Level independence:** Changes at one level shouldn't force version changes at containing levels. Modifying one function doesn't change the module; modifying a module doesn't change the package. Version at the level where change occurs.
</accretion_framework>

<semver_limitations>
### Semantic Versioning Limitations

One perspective[^hickey-speculation] on SemVer: major versions conflate all breaking changes into one signal. You know *something* broke, but not *what* or *how badly*. This makes major version bumps minimally informative.

**Alternative approach:** When incompatible changes are necessary, use new names rather than version numbers:
- Function level: `createUser` → `createUserV2`
- Module level: `users` → `users.v2`
- Package level: `my-lib` → `my-lib-next`

New names allow old and new to coexist, enabling gradual migration without forced upgrades.
</semver_limitations>

<stability_enables_composition>
### Stability Enables Composition

When names are enduring and changes accretive, systems compose safely:
- Dependencies update without surprises
- Latest versions work reliably
- Integration happens without fear

**Examples of enduring APIs:** Unix system calls (1970s → today), Java core APIs (decades of backward compatibility), HTML (ancient pages still render), Maven Central (artifacts never removed or changed).

The pattern: an accreting collection of immutable artifacts where names mean what they've always meant.
</stability_enables_composition>

<ontology_connection>
### Connection to Knowledge Engineering

These principles aren't just good practice for general APIs—they're essential for semantic systems:

**Ontology evolution:** Vocabularies grow monotonically. Predicates don't change meaning; new predicates are added. Deprecation through annotation, not removal.

**Schema evolution:** Add types and properties; don't remove or redefine. New schemas extend old ones.

**Query compatibility:** Adding facts doesn't break existing queries. New data enriches results rather than invalidating them.

**Inference stability:** Adding axioms doesn't invalidate existing inferences. Monotonic reasoning preserves prior conclusions.

**The discipline transfers both ways:** Design software APIs as you would design an ontology—semantic commitments made carefully, growth through accretion, meaning preserved over time. Conversely, apply API evolution practices to ontology maintenance.
</ontology_connection>

<ontological_design_checklist>
### Ontological Design Checklist

**Names and Semantics:**
- [ ] Names describe concepts, not implementation
- [ ] Names are enduring commitments
- [ ] No semantic overloading (same name, different meaning)

**Open-World Properties:**
- [ ] Data structures tolerate unknown fields
- [ ] Systems ignore what they don't understand
- [ ] No closed validation that prohibits extension

**Evolution Strategy:**
- [ ] Growth through accretion, not breakage
- [ ] New capabilities coexist with old
- [ ] Changes versioned at appropriate level

**When breaking is necessary:**
- Use new names (function, module, or package)
- Document migration path
- Keep old version functional alongside new
</ontological_design_checklist>
</code_as_ontology>

<mixed_paradigm_thinking>
## Mixed-Paradigm Thinking

Effective software engineering requires choosing the right paradigm for each problem. Different paradigms excel at different tasks. For detailed guidance, see the paradigm-specific skills: `functional-programmer`, `object-oriented-programmer`, `logic-programmer`.

<when_functional>
### When to Use Functional Programming

Use functional approaches when:
- Transforming data through pipelines
- Ensuring correctness through immutability
- Working with concurrent systems
- Composing small, reusable operations
- Avoiding state-related bugs

**Key principles:** Pure functions, immutable data structures, first-class and higher-order functions, composition over inheritance.
</when_functional>

<when_oop>
### When to Use Object-Oriented Programming

Use object-oriented approaches when:
- Modeling real-world entities with behavior and state
- Encapsulating mutable state when necessary
- Using polymorphism for extensibility
- Working with existing OO frameworks

**Caution:** Avoid overuse. Not every program needs objects. OOP can obscure functional clarity when misapplied.

**Key principles:** Encapsulation of state, clear interfaces and contracts, composition over inheritance, SOLID principles (see `object-oriented-programmer` skill).
</when_oop>

<when_logic>
### When to Use Logic Programming

Use logic/relational approaches when:
- Expressing relationships and constraints
- Searching solution spaces
- Working with symbolic reasoning
- Declaratively specifying what rather than how

**Key principles:** Relations over functions, unification and pattern matching, declarative specification, backtracking search.
</when_logic>

<paradigm_integration>
### Paradigm Integration

Modern software often benefits from mixing paradigms:
- Use functional composition for data transformation within OO systems
- Use objects to encapsulate stateful resources in functional programs
- Use logic programming for constraint solving within imperative systems

Choose the paradigm that makes the problem clearest, not the paradigm most fashionable.
</paradigm_integration>
</mixed_paradigm_thinking>

<code_planning>
## Code Planning and Scaffolding

<design_iteration>
### Iterate on Design Before Final Implementation

Design iteration is development work, not a delay before "real work." Do not jump to final implementation before understanding the problem space:

**Design iteration is productive:**
- Exploring the problem space through design builds understanding
- Sketching, diagramming, and writing design documents forces clarity
- Prototyping implementations reveals what interfaces work best
- Considering multiple approaches reveals trade-offs
- Design changes and throwaway prototypes are cheap; rewriting production code is expensive
- Time spent in design iteration prevents wasted implementation effort

**Prototyping as design exploration:**
- Build throwaway implementations to learn about the problem and solution space
- Experiment with different interface designs through working code
- Discover hidden complexity and interaction patterns
- Prototype against real constraints—actual data shapes, real APIs, production frameworks—so you discover problems you'll face in production, not hypothetical ones
- Learn what works by making it "wrong first" — SuperfastMatt
- Throw away the prototype and design/scaffold the real implementation with that knowledge
- "You don't completely know what you're doing 'till you've done it once." — Leo Brodie

**The distinction:**
- **Design iteration/prototyping** (good): Exploring to build understanding, expecting to throw away and redesign
- **Jumping to final implementation** (problematic): Writing production code before understanding the problem

**Indicators you need more design iteration:**
- You can't clearly explain what you're building and why
- Requirements are vague or incomplete
- You don't understand how components will interact
- You're unsure about major architectural decisions
- The design doesn't trace back to user needs
- You can't articulate the trade-offs you're making
- Your prototypes use toy data or mocked APIs, which hide the problems you need to discover

**Design exploration techniques:**
- Sketch component interactions and data flows
- Write design documents (even rough ones)
- Diagram architectural alternatives
- Build throwaway prototypes to test interface ergonomics
- Discuss design with others (or explain it to yourself)
- Map requirements to design decisions

**When you're ready to scaffold production code:**
- You can explain what you're building and why
- Major architectural decisions are clear (learned from prototypes if needed)
- You understand component boundaries and interfaces (tested through exploration)
- You can trace design decisions back to requirements
- You've considered alternatives and their trade-offs

Only after design iteration should you begin scaffolding production code.
</design_iteration>

<scaffolding>
### Scaffolding Production Code

Plan code by writing scaffolds that can be filled out later:

- **Define structures first**: Create interfaces, type signatures, abstract classes, and other definitional structures before implementation
- **Scaffold functions**: Create empty functions with comments listing the steps they will carry out (e.g., "1. Setup data.", "2. Process data.", "3. Validate output.", "N. Return result.")
- **Write tests for scaffolds**: After defining but not implementing code structures, write tests to create example uses of proposed APIs. Examine these examples to identify potential usage problems requiring refactoring
- **Design for maintainability**: Assume code will be maintained by junior engineers and LLMs. Prefer strongly defined structures based on idiomatic design and architectural patterns for the language

When uncertain, ask the user—they are a senior software engineer who either has an answer or can find one.
</scaffolding>
</code_planning>

<design_principles>
## Design Principles

<modularity>
### Modularity and Decomposition

Break programs into modules with clear responsibilities:
- Each module should have a single, well-defined purpose
- Modules should be independently testable
- Dependencies between modules should be explicit and minimal
- Use dependency injection to reduce coupling
</modularity>

<testability>
### Design for Testability

Write code that is easy to test. For detailed testing philosophy, see `test-driven-development` skill.

- Separate pure logic from side effects
- Use dependency injection for external resources
- Keep functions small and focused
- Design clear interfaces with testable contracts
- Avoid global state and hidden dependencies
</testability>

<progressive_enhancement>
### Progressive Enhancement

Build systems incrementally:
1. Start with the simplest version that works
2. Test thoroughly at each stage
3. Add complexity only when needed
4. Refactor continuously to maintain clarity

"...the best way to make something is sometimes to just make it wrong first." — SuperfastMatt
</progressive_enhancement>

<optimization>
### Avoid Premature Optimization

Optimize for clarity first, performance second—but distinguish between speculation and expertise:

**Avoid speculative optimization:**
- Don't optimize based on guesses about what might be slow
- Don't add complexity for hypothetical performance gains
- Don't sacrifice clarity for unmeasured improvements

**Apply expert knowledge:**
- Use known best practices to avoid foreseeable problems
- Make deliberate architectural choices based on experience
- Choose appropriate algorithms and data structures from the start
- Apply domain expertise to prevent obvious inefficiencies

The distinction: Premature optimization is optimizing based on speculation. Informed design decisions using expertise are not premature optimization—they're good engineering.

**When optimizing:**
1. Write clear, correct code using sound engineering judgment
2. Measure to identify actual bottlenecks beyond obvious ones
3. Optimize proven bottlenecks
4. Preserve clarity when optimizing
</optimization>
</design_principles>

<requirements_driven_design>
## Requirements-Driven Design

<user_needs>
### Start with User Needs and End-Goals

Before designing solutions, understand and document what you're building and why:

**Define user needs first:**
- Identify user categories and their characteristics
- Write user stories in the form: "As a [user], I need/want to [action] in order to [goal] because [motivation]"
- Define project goals that may specify implementation constraints or learning objectives
- Ensure user stories don't specify implementation details—that's for requirements

**Establish requirements from needs:**
- **Functional requirements**: What the system must do (derived from user stories)
- **Quality requirements**: How well functions must be performed (availability, latency, maintainability)
- **Platform requirements**: Technologies that must be used (languages, frameworks, infrastructure)
- **Project requirements**: Development process constraints (build tools, testing approaches)

**Trace everything back:**
- Every requirement should reference the user stories or goals that motivate it
- Every design decision should reference the requirements it satisfies
- Maintain this traceability to evaluate whether decisions serve actual needs
</user_needs>

<future_evolution>
### Consider Future Evolution

Explicitly think about how the system might evolve:

**Document future developments:**
- What capabilities might be needed later?
- How likely are different evolution paths?
- What would make those evolutions easier or harder?

**Design for evolution:**
- Identify flex points where future changes are most likely
- Don't over-engineer for unlikely futures
- Don't under-engineer for probable futures
- Make evolution paths explicit in design documentation
</future_evolution>

<success_criteria>
### Define Success Criteria

Establish how you'll know if the system serves its purpose:

**Key Performance Indicators (KPIs):**
- How will you measure whether the system achieves its goals?
- What metrics indicate the system is serving user needs?
- Distinguish between system health metrics and business/functional metrics

**Design for measurement:**
- Build observability for success criteria from the start
- Include both "is it working?" and "is it serving its purpose?" metrics
- Plan for collecting the data needed to evaluate KPIs
</success_criteria>

<design_documentation>
### When to Write Design Documentation

Document design when:

**Complexity warrants it:**
- Multiple components with significant interactions
- Non-obvious architectural decisions
- Systems that will be maintained by others
- Projects where you need to think through implications

**Decisions need grounding:**
- You're unsure which approach to take
- Multiple stakeholders need to align
- Trade-offs need to be made explicit
- Future you needs to remember why decisions were made

**Structure for design documents:**
1. User needs and goals (the "why")
2. Problem space and precedent (context and lessons learned)
3. Requirements (constraints and expectations)
4. Proposed solution (the "what")
5. System architecture (the "how")
6. Component design (implementation details)
7. Success criteria and monitoring

**Use documentation to think:**
- Writing forces clarity
- Traceability reveals gaps
- Structure helps identify missing considerations
- Documentation is a thinking tool, not just a communication artifact
</design_documentation>

<decision_grounding>
### Ground All Decisions in User Needs

When evaluating design alternatives or making implementation decisions:

1. **Reference user needs**: Which user stories or goals does this serve?
2. **Check requirements**: Which requirements does this satisfy?
3. **Evaluate trade-offs**: What are we optimizing for? What are we sacrificing?
4. **Verify alignment**: Does this move us toward our ultimate goals?

If you can't trace a decision back to user needs or requirements, either the decision is unnecessary or the user needs and requirements are incomplete. Investigate which is true—you may have identified a gap in requirements that should be documented.
</decision_grounding>
</requirements_driven_design>

<engineering_judgment>
## Engineering Judgment and Trade-offs

<strategic_alignment>
### Strategic Path Alignment

Not everything that gets you from today to tomorrow also gets you from today to the day-after-tomorrow. Evaluate whether each decision advances toward ultimate goals, not just immediate milestones.

**Path-dependent decisions:**
- Some solutions solve immediate problems while making long-term goals harder to reach
- Technical debt that speeds up shipping might block future capabilities
- Abstractions that work for current scale might prevent scaling
- Architecture that serves today's team might not serve tomorrow's organization

**Evaluate strategic alignment:**
1. **Identify ultimate goals**: What are you ultimately building? What capabilities must exist?
2. **Trace the path**: Does this decision move toward those goals or merely toward the next milestone?
3. **Consider opportunity cost**: What future options does this decision preserve or eliminate?
4. **Check for path dependency**: Will this decision make later decisions harder or easier?

**When immediate and long-term conflict:**
- Make the conflict explicit
- Understand the cost of the misalignment
- Document the strategic trade-off
- Plan for course correction or refactoring
- Sometimes the right answer is to take the detour, but do so consciously

**Reference point for all decisions:** The ultimate goals and end-state capabilities, not just the next feature or milestone.
</strategic_alignment>

<context_over_dogma>
### Context Over Dogma

What works in one context (team size, domain, scale, constraints) may not work in another. Staff-level judgment requires:

- **Question inherited practices** when context changes
- **Adapt patterns to context** rather than following them religiously
- **Recognize that "best practices" are contextual**, not universal
- **Understand the original constraints** that shaped a pattern before applying it
- **Re-evaluate decisions** when circumstances change

The same approach that works at Google scale may be over-engineering at startup scale, and vice versa.
</context_over_dogma>

<understanding_tradeoffs>
### Understanding Trade-offs

Every architectural and design decision involves trade-offs between competing concerns. There are no solutions, only trade-offs:

- **Make trade-offs explicit**: Document what you're optimizing for and what you're sacrificing
- **Understand competing concerns**: Performance vs. maintainability, flexibility vs. simplicity, consistency vs. availability
- **Communicate trade-offs**: Help stakeholders understand the costs and benefits of different approaches
- **Revisit trade-offs**: As context changes, previously correct trade-offs may become incorrect

The goal is not to avoid trade-offs, but to make them consciously and document the reasoning.
</understanding_tradeoffs>

<decision_reversibility>
### Decision Reversibility

Weight decisions differently based on the cost of reversibility. All decisions can be reversed if enough force is applied, but an expensive two-way door is effectively a one-way door.

**Low-cost reversibility (move fast):**
- Variable names, function signatures in private APIs
- Internal module organization
- Logging and monitoring approaches
- Development tooling choices

**High-cost reversibility (move carefully):**
- Public APIs and contracts
- Database schemas and data models
- Programming language and framework choices
- Fundamental architectural patterns
- Cross-system protocols and interfaces

**For all decisions:**
- Document assumptions that would trigger revisiting the decision
- Make the cost of reversal explicit when communicating the decision
- Choose designs that minimize reversal cost when practical
</decision_reversibility>

<systems_thinking>
### Systems Thinking and Emergent Behavior

Systems behave as wholes, not just as collections of parts. Staff-level engineers understand:

- **Emergent properties**: Behaviors that arise from component interactions, not from individual components
- **Feedback loops**: How outputs feed back as inputs, creating amplification or dampening effects
- **Second-order effects**: Consequences of consequences—changes ripple through systems
- **Local vs. global optimization**: Optimizing one component can degrade overall system performance
- **Unintended consequences**: Changes have effects beyond their immediate purpose

Design with the whole system in mind, not just individual components in isolation.
</systems_thinking>

<abstraction_costs>
### When Abstractions Are Too Expensive

While this skill emphasizes abstraction as a complexity management tool, experienced engineers recognize when abstractions become counterproductive:

**Abstractions are too expensive when they:**
- Leak implementation details, requiring users to understand both the abstraction and what it hides
- Create more cognitive overhead than the complexity they eliminate
- Have unacceptable performance costs that can't be optimized away
- Add indirection that makes debugging and reasoning more difficult
- Attempt to hide complexity that must be understood anyway

**Consider removing abstractions when:**
- The abstraction serves only one or two concrete cases
- Direct, concrete code would be clearer and simpler
- The "Don't Repeat Yourself" principle is being applied to coincidental duplication
- The cost of understanding the abstraction exceeds the cost of understanding the concrete implementation

Sometimes the right answer is concrete, direct code rather than clever abstraction.
</abstraction_costs>

<technical_debt>
### Technical Debt as Strategic Investment

Not all "technical debt" is bad—sometimes it's a deliberate, informed choice to ship faster:

**Intentional technical debt (acceptable):**
- Deliberate shortcuts with documented plan for repayment
- Strategic choices to validate hypotheses before investing in robust solutions
- Conscious trade-offs between time-to-market and long-term maintainability
- Temporary solutions with clear triggers for replacement

**Accidental complexity (unacceptable):**
- Poorly understood code that "just grew"
- Duplicated logic without awareness of duplication
- Architecture that emerged without conscious design
- Complexity from lack of understanding, not deliberate choice

**Essential vs. accidental complexity (Brooks):**
- Essential: Inherent in the problem domain, cannot be removed
- Accidental: Created by our solution approach, can potentially be eliminated

**Managing technical debt:**
- Make debt intentional and explicit
- Document repayment conditions and timeline
- Track debt and its interest (maintenance burden)
- Pay down debt before interest compounds uncontrollably
- Distinguish between debt and poor engineering
</technical_debt>

<failure_resilience>
### Design for Failure and Resilience

Assume components will fail; don't hope they won't. Resilient systems expect and handle failure:

**Failure awareness:**
- Identify failure modes for each component
- Understand blast radius—what else fails when this fails
- Design failure domains and isolation boundaries
- Plan for partial system degradation

**Resilience patterns:**
- **Graceful degradation**: Provide reduced functionality when components fail
- **Defense in depth**: Multiple layers of protection and validation
- **Bulkheads**: Isolate failures to prevent cascading
- **Circuit breakers**: Stop calling failing services to allow recovery
- **Timeouts and retries**: Handle slow or intermittent failures
- **Fallback mechanisms**: Alternative paths when primary path fails

Design systems that continue functioning, perhaps with reduced capability, when components fail.
</failure_resilience>

<observability>
### Observability as a First-Class Concern

Build systems that can be understood in production, not just in development:

**Observability is not an afterthought:**
- Design logging, metrics, and tracing into the architecture from the start
- Production behavior is fundamentally different from development behavior
- Systems must explain their own behavior and state

**Design for debuggability:**
- Include context in all log messages (request IDs, user IDs, transaction IDs)
- Emit metrics at component boundaries
- Structure logs for machine parsing, not just human reading
- Make system state observable without requiring debugger access
- Include health checks and diagnostic endpoints
- Design for troubleshooting by people who didn't write the code

The question is not "does this work in my development environment" but "can we understand what's happening in production when things go wrong."
</observability>

<architectural_patterns>
### Architectural Patterns for System Organization

Complex systems benefit from architectural patterns that isolate business logic from infrastructure. These patterns prevent common problems but add complexity—apply them when benefits outweigh costs.

<hexagonal_architecture>
#### Hexagonal Architecture (Ports & Adapters)

<hex_core_principle>
**Core principle:** Isolate business logic from external systems (UI, database, APIs) through well-defined boundaries. All external interactions go through ports (interfaces) and adapters (implementations).

> "Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases." — Alistair Cockburn
</hex_core_principle>

<hex_structure>
**Structure:**
- **Application Core** — Pure business logic, no infrastructure dependencies
- **Ports** — Interfaces defining how external actors communicate (technology-neutral, like USB ports)
- **Adapters** — Technology-specific implementations (REST API, database, message queue)
- **Primary Ports** — Driving adapters: external actors initiate (web UI, CLI, tests)
- **Secondary Ports** — Driven adapters: application initiates (database, email, external APIs)
</hex_structure>

<hex_warning_signs>
**Early warning signs you needed hexagonal architecture:**
- Can't test business logic without database setup
- UI changes require changing business logic
- Switching from REST to GraphQL requires rewriting core code
- Team blocked waiting for database/external services
- Same business logic duplicated across interfaces (web UI + batch jobs)
</hex_warning_signs>

<hex_when_to_use>
**When to recognize you need it early:**
- Multiple clients will access same business logic (web, mobile, API, batch)
- Database or UI technology might change
- Need to test business logic without database/UI
- Team developing subsystems independently
- Integrating with external services unavailable during development
</hex_when_to_use>

<hex_tradeoffs>
**Trade-offs:**
- **Cost:** Additional layers (ports + adapters), more interfaces, latency from indirection
- **Benefit:** Testability, flexibility, parallel development, technology independence
- **Decision:** Worth it for complex systems with multiple interfaces; overkill for simple CRUD apps
</hex_tradeoffs>

<hex_implementation>
**Implementation:**
- Use dependency injection to wire adapters to ports
- Keep ports technology-agnostic (domain language, not infrastructure language)
- Test core with mock adapters (no database/UI needed)
- One port can have multiple adapters (REST + GraphQL implementing same port)
</hex_implementation>

<related_patterns>
**Related architectural patterns:**
- **Clean Architecture** (Robert Martin) — Concentric circles: entities → use cases → interface adapters → frameworks
- **Onion Architecture** (Jeffrey Palermo) — Domain-centric layers, dependencies point inward
- **Common theme:** Business logic at center, dependencies point inward, outer layers adapt to inner

**Works well with Domain-Driven Design:**
- Each bounded context is a hexagon
- Application services define primary ports
- Repository interfaces are secondary ports
- Adapters implement infrastructure per subdomain
</related_patterns>

<hex_when_simpler_suffices>
**When simpler approaches suffice:**
- CRUD applications with minimal business logic
- Single interface (just a web UI)
- Stable, unlikely-to-change technology stack
- Small team, simple domain
- Rapid prototyping (add architecture when stabilizing)
</hex_when_simpler_suffices>
</hexagonal_architecture>
</architectural_patterns>
</engineering_judgment>

<code_quality>
## Code Quality Standards

<naming_conventions>
### Naming Conventions

Use names that reveal intent:
- Functions/methods: verb phrases describing what they do
- Variables: nouns describing what they represent
- Classes: nouns describing what they are
- Constants: descriptive names indicating purpose
- Avoid abbreviations unless universally understood
</naming_conventions>

<documentation_comments>
### Documentation and Comments

Document the why, not the what:
- Code should be self-documenting through clear structure and naming
- Comments explain rationale, trade-offs, and non-obvious decisions
- Documentation explains interfaces, contracts, and usage
- Keep documentation synchronized with code changes
- Use fluent US English with correct grammar
- Document procedures with step identifiers (e.g., "1. Prepare data.", "2. Process data.")
- Documentation serves both as communication and as memory

**Documentation as context:** Poor documentation is unacceptable. Strive for perfect documentation on all code entities, even tests. Address linter findings for documentation immediately to ensure documentation is written with proper context.
</documentation_comments>

<error_handling>
### Error Handling

Handle errors explicitly and meaningfully:
- Fail fast when assumptions are violated
- Provide actionable error messages
- Distinguish between recoverable and unrecoverable errors
- Use types and contracts to prevent errors when possible
</error_handling>

<code_organization>
### Code Organization

Organize code for human understanding:
- Group related functionality together
- Separate concerns into distinct modules
- Use consistent formatting and style
- Follow language-specific conventions
- Make dependencies explicit
</code_organization>
</code_quality>

<working_with_existing_code>
## Working with Existing Code

<understanding_before_changing>
### Understanding Before Changing

Before modifying code:
1. Trace through execution to understand flow
2. Identify invariants and assumptions
3. Understand why code was written as it was
4. Check for tests that document expected behavior
5. Examine configuration and build files to understand project commands
6. Don't assume based solely on programming language (look for NPM scripts, rebar3 tasks, Hatch scripts, Gradle tasks, etc.)
</understanding_before_changing>

<refactoring_strategy>
### Refactoring Strategy

When refactoring:
1. Ensure tests exist for current behavior
2. Make changes incrementally
3. Run tests after each change
4. Preserve external interfaces when possible
5. Document reasons for changes
6. Avoid creating multiple alternate versions of source files
7. Use Git feature branches for experimentation
</refactoring_strategy>

<legacy_code>
### Legacy Code

When working with legacy systems:
- Add tests before making changes (characterization tests)
- Refactor incrementally, not wholesale
- Preserve working behavior
- Document discoveries about system behavior (preferably, as tests)
- Consider the cost/benefit of changes
</legacy_code>
</working_with_existing_code>

<language_tool_selection>
## Language and Tool Selection

<choose_tools>
### Choose Appropriate Tools

Select languages and tools based on:
- Problem domain and requirements
- Team expertise and maintenance considerations
- Ecosystem maturity and library availability
- Performance and scalability needs
- Development velocity vs. long-term maintenance
</choose_tools>

<favor_existing>
### Favor Existing Solutions

Before writing new code:
1. Search for existing libraries and solutions
2. Evaluate library quality, maintenance, and fit
3. Write new code only when existing solutions are inadequate
4. Understand the trade-off between dependency and custom code

Search the web for existing solutions when asked to write code—finding an existing library is preferable to writing new code. Clarify user expectations when unclear about whether they want a solution or actual code.
</favor_existing>
</language_tool_selection>

<principles_in_practice>
## Principles in Practice

<iterative_development>
### Iterative Development

Develop software iteratively:
1. Start with a working skeleton
2. Add features incrementally
3. Test continuously
4. Refactor regularly to maintain quality
5. Expect to rewrite significant portions

"...you don't completely know what you're doing 'till you've done it once." — Leo Brodie
</iterative_development>

<practical_constraints>
### Practical Constraints

When working on projects:
- When dependencies are missing, stop and wait for user to install them
- If tools fail, stop and wait for corrective action
- Prefer file patching over full rewrites to avoid response length limits
- Always clean up unnecessary code and files before completing tasks
</practical_constraints>

<continuous_learning>
### Continuous Learning

Software engineering requires continuous learning:
- Study classic texts and papers
- Learn from code reviews and failures
- Understand multiple paradigms and languages
- Keep current with evolving practices
- Apply lessons from experience to future work
</continuous_learning>

<pragmatism_idealism>
### Balance Pragmatism and Idealism

Strike balance between:
- Perfect design and shipping working software
- Flexibility and simplicity
- Performance and clarity
- Innovation and proven patterns
- Technical excellence and practical constraints

The goal is sustainable software that serves its purpose well, not perfect code.
</pragmatism_idealism>
</principles_in_practice>

<safety_constraints>
## Safety Constraints

These guardrails apply regardless of context or time pressure. They constrain toward safety, not away from good engineering.

<security_constraints>
### Security
- **Never** store secrets, credentials, or API keys in source control
- **Never** disable security features to "make things work"
- **Always** validate and sanitize untrusted input
- **Never** ignore security vulnerability warnings in dependencies
- **Always** use parameterized queries—never string concatenation for SQL
- **Never** log sensitive data (passwords, tokens, PII)
</security_constraints>

<deployment_constraints>
### Deployment
- **Never** deploy code without running the test suite
- **Never** deploy directly to production without staging verification (when staging exists)
- **Never** skip code review for "small changes"
- **Always** have a rollback plan before deploying
- **Never** force push to main/master without explicit authorization
</deployment_constraints>

<data_constraints>
### Data
- **Never** delete production data without backup verification
- **Never** share or log personally identifiable information unnecessarily
- **Always** encrypt sensitive data at rest and in transit
- **Never** use production data in development without anonymization
</data_constraints>

<process_constraints>
### Process
- **Never** commit to deadlines without understanding requirements
- **Always** communicate blockers early rather than hoping they resolve
- **Never** silently swallow errors or exceptions
- **Never** merge code you don't understand
- **Always** leave code cleaner than you found it
</process_constraints>
</safety_constraints>

<resources>
## Resources

**Primary texts:**
- Abelson, Harold and Gerald Jay Sussman. _Structure and Interpretation of Computer Programs_. https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/index.html

**Related skills:**
- `functional-programmer` — Functional paradigm principles and patterns
- `object-oriented-programmer` — OOP principles including SOLID
- `logic-programmer` — Logic/relational programming patterns
- `test-driven-development` — Testing philosophy and practices
- `git-version-control` — Version control workflows
</resources>

## Sources

<sources>
[^hickey-speculation]: Rich Hickey. 2016. Spec-ulation (keynote). Clojure/conj 2016. https://www.youtube.com/watch?v=oyLBGkS5ICk
</sources>
