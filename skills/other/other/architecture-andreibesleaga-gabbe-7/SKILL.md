---
name: arch-debt
description: Identify architectural anti-patterns — coupling, circular dependencies, God objects — and propose concrete migration paths
triggers: [architecture debt, coupling, God object, Big Ball of Mud, circular dependency, spaghetti, modularize, arch debt]
context_cost: high
---

# Architecture Debt Skill

## Goal
Identify architectural anti-patterns through dependency analysis and propose concrete, phased migration paths. Architecture debt is more expensive than code debt — it blocks entire teams.

## Steps

1. **Run import/dependency graph analysis**

   **JavaScript/TypeScript:**
   ```bash
   # Circular dependency detection
   npx madge --circular --extensions ts,js,tsx src/

   # Full dependency graph visualization
   npx madge --image dependency-graph.svg --extensions ts,js src/

   # Dependency rules enforcement
   npx dependency-cruiser --config .dependency-cruiser.cjs src/
   ```

   **PHP:**
   ```bash
   # Deptrac for DDD layer enforcement
   vendor/bin/deptrac analyse

   # PHPStan for dependency analysis
   vendor/bin/phpstan analyse --level=9

   # PHP Metrics for coupling
   vendor/bin/phpmetrics --report-html=metrics-report/ app/
   ```

   **Python:**
   ```bash
   # Import Linter for layer enforcement
   lint-imports --config .import-linter.ini

   # Pydeps for visualization
   pydeps src/ --noshow --max-bacon 2 --output dependency-graph.svg
   ```

2. **Analyze coupling metrics**

   For each module/class, calculate:
   - **Afferent coupling (Ca):** How many other modules depend on this module?
     - High Ca = unstable to change (many things break when you change it)
   - **Efferent coupling (Ce):** How many modules does this module depend on?
     - High Ce = brittle (dependent on too many things, hard to test)
   - **Instability:** Ce / (Ca + Ce) — 0 = stable/rigid, 1 = unstable/flexible
   - **Abstractness:** ratio of abstract to concrete classes

   **Target:** Core domain (stable = abstract), infrastructure (unstable = concrete)

3. **Classify architecture debt types**

   **Structural Debt** (wrong layers):
   - Domain layer importing from infrastructure
   - Circular dependencies between modules
   - Cross-cutting concerns not in dedicated layer

   **Behavioral Debt** (wrong responsibilities):
   - God classes (> 500 lines, > 20 public methods)
   - Fat controllers (business logic in HTTP layer)
   - Service classes doing everything

   **Evolutionary Debt** (outdated patterns):
   - Older patterns not compatible with current architecture style
   - Inconsistent patterns across the codebase (some DDD, some not)
   - Legacy code using globals or singletons where DI is now standard

4. **Identify specific anti-patterns**

   **God Object → Split by Single Responsibility:**
   ```
   UserService.ts (800 lines, handles: auth, profile, billing, notifications)
   →
   UserAuthService.ts       (authentication logic)
   UserProfileService.ts    (profile management)
   UserBillingService.ts    (billing operations)
   UserNotificationService.ts (notification orchestration)
   ```

   **Fat Controller → Extract Use Cases:**
   ```
   OrderController.create() (80 lines of business logic)
   →
   CreateOrderUseCase.execute() (business logic extracted)
   OrderController.create() (5 lines: validate input, call use case, format response)
   ```

   **Circular Dependency → Extract Shared Abstraction:**
   ```
   UserService → OrderService → UserService (circular)
   →
   IUserQueryPort (interface in domain layer)
   UserService implements nothing from OrderService
   OrderService depends on IUserQueryPort (implemented by UserService)
   ```

   **Strangler Fig for large migrations:**
   ```
   Legacy monolith → New modular structure (gradual migration)
   Step 1: Add facade/gateway in front of legacy code
   Step 2: Route NEW requests to new module
   Step 3: Gradually migrate existing logic to new module
   Step 4: Remove legacy code when fully migrated
   ```

5. **Prioritize architecture debt**

   Use same Impact×Effort as tech-debt.skill:
   - P1: Circular dependencies (prevent compilation, testing, and refactoring)
   - P1: God objects blocking team from working independently
   - P2: Layer violations (allow short-term, expensive long-term)
   - P3: Inconsistent patterns (reduce over time)

6. **Create ADR for major migration approach**
   - Use adr-writer.skill to document the migration approach
   - Major migrations require human approval before starting

7. **Create tasks in project/tasks.md** (15-min rule applies to architecture work too)
   - Decompose into atomic steps: one interface extracted, one class split, etc.
   - Each step must leave the codebase in a working state (all tests pass)

8. **Generate architecture debt report**
   ```markdown
   ## Architecture Debt Report

   ### Circular Dependencies Found
   - [CRITICAL] src/users/UserService.ts <-> src/orders/OrderService.ts
     Fix: Extract IUserQueryPort interface

   ### Layer Violations
   - [HIGH] src/domain/User.ts imports from src/infrastructure/PrismaClient
     Fix: Apply Dependency Inversion (create repository interface in domain)

   ### God Objects
   - [HIGH] UserService.ts: 843 lines, 28 public methods
     Fix: Extract into 4 specialized services

   ### Instability Analysis
   - UserService: Ca=12, Ce=8, Instability=0.4 (acceptable)
   - OrderRepository: Ca=3, Ce=15, Instability=0.83 (too high — too many deps)

   ### Migration Roadmap
   Phase 1 (this sprint): Fix circular deps (2 days)
   Phase 2 (next sprint): Split UserService God object (3 days)
   Phase 3 (following sprint): Fix layer violations via DI (4 days)
   ```

## Constraints
- Never do big-bang architecture rewrites — always Strangler Fig or incremental
- Each migration step must leave all tests passing
- Major architectural changes require an ADR and human approval
- Measure coupling before and after to verify improvement

## Output Format
Architecture debt report + prioritized migration roadmap + ADR for major changes + tasks in project/tasks.md.
