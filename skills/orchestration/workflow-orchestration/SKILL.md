---
name: workflow-orchestration
description: Standard agent pipelines for audit, coding, new project, refactor, and simple workflows. Defines 5 workflow types with specific agent sequences (AUDIT: BA→PM→Workers→Reviewer→PM, CODING: Architect→PM→Workers→Validator→Reviewer→PM, NEW_PROJECT and REFACTOR follow coding pipeline, SIMPLE: direct processing). Includes agent contracts, workflow detection logic, and orchestration best practices. Use when /ms command needs to determine workflow type and coordinate multi-agent execution.
---

# Workflow Orchestration Skill

**Purpose:** This skill defines the standard agent pipelines for different task types. The `/ms` command uses this skill to orchestrate complex tasks with consistent agent ordering and handoffs.

---

## When to Use This Skill

- When `/ms` command needs to determine workflow type
- When orchestrating multi-agent pipelines
- When coordinating agent handoffs and dependencies
- When consolidating results from parallel worker agents

---

## Workflow Types

### AUDIT Workflow

**Pipeline:**

```
Business Analyst → Project Manager → Workers (parallel) → Reviewer → PM (Consolidation)
```

**Use Cases:**

- Monorepo configuration audits
- Code quality assessments
- Compliance checks
- Security audits
- Standards validation

**Characteristics:**

- BA analyzes requirements and defines scope
- PM plans worker deployment
- Workers execute audits in parallel (no dependencies)
- Reviewer assesses overall findings
- PM consolidates into final report

---

### CODING Workflow

**Pipeline:**

```
Architect → Project Manager → Workers (wave-based) → Production Validator → Reviewer → PM (Consolidation)
```

**Use Cases:**

- Feature implementation
- API development
- Database schema changes
- Component creation
- Service integration

**Characteristics:**

- Architect designs solution and identifies dependencies
- PM orchestrates wave-based execution
- Workers execute in dependency order (contracts → tests → database → services → UI)
- Validator ensures build/lint/test pass
- Reviewer assesses code quality
- PM consolidates results

---

### NEW PROJECT Workflow

**Pipeline:**

```
Architect → Project Manager → Workers (wave-based) → Production Validator → Reviewer → PM (Consolidation)
```

**Use Cases:**

- Scaffolding new projects
- Initializing repositories
- Creating new workspaces
- Setting up infrastructure

**Characteristics:**

- Architect designs project structure
- PM plans initialization sequence
- Workers set up components in order
- Validator verifies project builds
- Reviewer checks standards compliance
- PM consolidates setup report

---

### REFACTOR Workflow

**Pipeline:**

```
Architect → Project Manager → Workers (wave-based) → Production Validator → Reviewer → PM (Consolidation)
```

**Use Cases:**

- Code restructuring
- Architecture migrations
- Pattern updates
- Dependency upgrades
- Technical debt reduction

**Characteristics:**

- Architect plans refactoring strategy
- PM coordinates safe migration path
- Workers execute changes incrementally
- Validator ensures no regressions
- Reviewer validates improvements
- PM consolidates migration report

---

### SIMPLE Workflow

**Pipeline:**

```
Direct Processing (no orchestration)
```

**Use Cases:**

- Single file edits
- Quick questions
- Simple lookups
- Minor fixes

**Characteristics:**

- No multi-agent coordination needed
- Direct execution by single agent
- No consolidation phase

---

## Agent Contracts

### Business Analyst Output → PM Input

```typescript
interface AuditRequirements {
  // Scope definition
  scope: "full" | "partial" | "specific";

  // Domain areas to audit
  domains: string[];

  // Success criteria description
  criteria: string;

  // Quantifiable success metrics
  successMetrics: Record<string, number>;

  // Example:
  // {
  //   scope: "full",
  //   domains: ["eslint", "prettier", "typescript", "vitest", "turbo"],
  //   criteria: "All config files follow MetaSaver patterns",
  //   successMetrics: {
  //     minComplianceRate: 95,
  //     maxViolations: 10,
  //     requiredDocumentation: 100
  //   }
  // }
}
```

---

### Architect Output → PM Input

```typescript
interface ArchitecturalDesign {
  // Type of feature being implemented
  featureType: string;

  // Development methodology
  methodology: "sparc" | "tdd" | "standard";

  // List of agents needed for implementation
  agentsNeeded: string[];

  // Order in which agents should execute
  implementationOrder: string[];

  // Dependency relationships between agents
  // Each array represents agents that must complete before next wave
  dependencies: string[][];

  // Example:
  // {
  //   featureType: "CRUD API with Database",
  //   methodology: "sparc",
  //   agentsNeeded: [
  //     "contracts-agent",
  //     "tester",
  //     "prisma-database-agent",
  //     "data-service-agent",
  //     "react-component-agent"
  //   ],
  //   implementationOrder: [
  //     "contracts-agent",      // Wave 1: Specification
  //     "tester",               // Wave 2: Tests first (TDD)
  //     "prisma-database-agent",// Wave 3: Data layer
  //     "data-service-agent",   // Wave 4: API layer
  //     "react-component-agent" // Wave 5: UI layer
  //   ],
  //   dependencies: [
  //     ["contracts-agent"],                    // Wave 1
  //     ["tester"],                             // Wave 2 (needs contracts)
  //     ["prisma-database-agent"],              // Wave 3 (needs contracts)
  //     ["data-service-agent"],                 // Wave 4 (needs database)
  //     ["react-component-agent"]               // Wave 5 (needs API)
  //   ]
  // }
}
```

---

### PM Output → /ms Execution

```typescript
interface ExecutionPlan {
  // Waves of agent execution
  waves: Wave[];

  // Total number of agents to spawn
  totalAgents: number;

  // Execution strategy description
  strategy: string;

  // Specific instructions for spawning each agent
  spawnInstructions: string[];
}

interface Wave {
  // Wave number (1-based)
  waveNumber: number;

  // Agents to execute in this wave (parallel)
  agents: string[];

  // Dependencies from previous waves
  dependsOn: string[];

  // Expected outputs from this wave
  expectedOutputs: string[];
}

// Example:
// {
//   waves: [
//     {
//       waveNumber: 1,
//       agents: ["eslint-agent", "prettier-agent", "typescript-agent"],
//       dependsOn: [],
//       expectedOutputs: ["eslint_audit", "prettier_audit", "typescript_audit"]
//     },
//     {
//       waveNumber: 2,
//       agents: ["vitest-agent", "turbo-config-agent"],
//       dependsOn: ["eslint_audit", "prettier_audit"],
//       expectedOutputs: ["vitest_audit", "turbo_audit"]
//     }
//   ],
//   totalAgents: 5,
//   strategy: "Parallel execution with dependency waves",
//   spawnInstructions: [
//     "Spawn eslint-agent with scope: validate configuration",
//     "Spawn prettier-agent with scope: validate configuration",
//     "Spawn typescript-agent with scope: validate configuration"
//   ]
// }
```

---

### Worker Output → PM Consolidation

```typescript
interface WorkerResult {
  // Agent that produced this result
  agent: string;

  // Execution status
  status: "success" | "partial" | "failed";

  // Findings from the work
  findings: AuditFindings | CodingResult | any;

  // Quantifiable metrics
  metrics: Record<string, number>;
}

interface AuditFindings {
  // File or domain audited
  target: string;

  // Issues discovered
  violations: Violation[];

  // Compliance percentage
  complianceRate: number;

  // Recommendations for improvement
  recommendations: string[];
}

interface CodingResult {
  // Files created or modified
  filesChanged: string[];

  // Tests written
  testsAdded: number;

  // Build status
  buildPassing: boolean;

  // Lint status
  lintPassing: boolean;
}

// Example:
// {
//   agent: "eslint-agent",
//   status: "success",
//   findings: {
//     target: ".eslintrc.json",
//     violations: [
//       { rule: "missing-env-es2022", severity: "warning" }
//     ],
//     complianceRate: 95,
//     recommendations: ["Add env.es2022 to configuration"]
//   },
//   metrics: {
//     filesScanned: 45,
//     violationsFound: 3,
//     autoFixable: 2
//   }
// }
```

---

### PM Consolidation Output → User

```typescript
interface ConsolidatedReport {
  // Executive summary
  summary: string;

  // Status by domain/agent
  statusByDomain: Record<string, string>;

  // Aggregated metrics
  totalMetrics: Record<string, number>;

  // Actionable recommendations
  recommendations: string[];

  // Overall success status
  overallStatus: "pass" | "partial" | "fail";
}

// Example:
// {
//   summary: "Monorepo audit completed with 92% compliance. 3 critical issues require attention.",
//   statusByDomain: {
//     "eslint": "PASS (95% compliant)",
//     "prettier": "PASS (100% compliant)",
//     "typescript": "PARTIAL (85% compliant)",
//     "vitest": "PASS (98% compliant)",
//     "turbo": "FAIL (70% compliant)"
//   },
//   totalMetrics: {
//     totalAgentsExecuted: 5,
//     totalViolations: 12,
//     averageCompliance: 92,
//     criticalIssues: 3,
//     warningIssues: 9
//   },
//   recommendations: [
//     "Fix turbo.json pipeline dependencies",
//     "Add missing TypeScript strict options",
//     "Update ESLint env configuration"
//   ],
//   overallStatus: "partial"
// }
```

---

## Workflow Detection

```typescript
function detectWorkflowType(request: string): WorkflowType {
  const lower = request.toLowerCase();

  // AUDIT workflow triggers
  if (
    lower.includes("audit") ||
    lower.includes("validate") ||
    lower.includes("check") ||
    lower.includes("compliance") ||
    lower.includes("assess") ||
    lower.includes("review all") ||
    lower.includes("scan")
  ) {
    return "AUDIT"; // BA → PM → Workers → Reviewer → PM
  }

  // NEW PROJECT workflow triggers
  if (
    lower.includes("new project") ||
    lower.includes("scaffold") ||
    lower.includes("initialize") ||
    lower.includes("bootstrap") ||
    lower.includes("create new") ||
    lower.includes("setup project")
  ) {
    return "NEW_PROJECT"; // Architect → PM → Workers → Validator → Reviewer → PM
  }

  // REFACTOR workflow triggers
  if (
    lower.includes("refactor") ||
    lower.includes("restructure") ||
    lower.includes("migrate") ||
    lower.includes("upgrade") ||
    lower.includes("modernize") ||
    lower.includes("convert")
  ) {
    return "REFACTOR"; // Architect → PM → Workers → Validator → Reviewer → PM
  }

  // CODING workflow triggers
  if (
    lower.includes("build") ||
    lower.includes("create") ||
    lower.includes("implement") ||
    lower.includes("add feature") ||
    lower.includes("develop") ||
    lower.includes("write code")
  ) {
    return "CODING"; // Architect → PM → Workers → Validator → Reviewer → PM
  }

  // Default to SIMPLE for straightforward tasks
  return "SIMPLE"; // Direct processing, no orchestration
}

type WorkflowType = "AUDIT" | "CODING" | "NEW_PROJECT" | "REFACTOR" | "SIMPLE";
```

---

## Complete Workflow Examples

### Example 1: Audit Workflow - Monorepo Configuration Audit

**User Request:** "Audit all monorepo configurations"

**Workflow Execution:**

1. **/ms detects AUDIT workflow**

   ```
   Request contains "audit" → AUDIT workflow selected
   Pipeline: BA → PM → Workers → Reviewer → PM
   ```

2. **Spawn business-analyst**

   ```typescript
   Task(
     "business-analyst",
     "Analyze monorepo audit requirements. Define scope, domains, and success criteria for comprehensive configuration audit."
   );
   ```

3. **BA returns AuditRequirements**

   ```typescript
   {
     scope: "full",
     domains: [
       "eslint", "prettier", "typescript", "vitest", "turbo",
       "pnpm-workspace", "docker", "github-workflows", "husky",
       "commitlint", "editorconfig", "gitignore", "gitattributes"
     ],
     criteria: "All configuration files follow MetaSaver monorepo patterns",
     successMetrics: {
       minComplianceRate: 95,
       maxCriticalViolations: 0,
       maxTotalViolations: 20,
       requiredDocumentation: 100
     }
   }
   ```

4. **Spawn project-manager with BA output**

   ```typescript
   Task(
     "project-manager",
     "Create execution plan for 13-domain audit. Organize into parallel waves based on dependencies."
   );
   ```

5. **PM returns ExecutionPlan**

   ```typescript
   {
     waves: [
       {
         waveNumber: 1,
         agents: ["eslint-agent", "prettier-agent", "typescript-agent", "editorconfig-agent"],
         dependsOn: [],
         expectedOutputs: ["eslint_audit", "prettier_audit", "typescript_audit", "editorconfig_audit"]
       },
       {
         waveNumber: 2,
         agents: ["vitest-agent", "turbo-config-agent", "pnpm-workspace-agent"],
         dependsOn: [],
         expectedOutputs: ["vitest_audit", "turbo_audit", "pnpm_audit"]
       },
       {
         waveNumber: 3,
         agents: ["docker-compose-agent", "github-workflow-agent", "husky-agent"],
         dependsOn: [],
         expectedOutputs: ["docker_audit", "github_audit", "husky_audit"]
       },
       {
         waveNumber: 4,
         agents: ["commitlint-agent", "gitignore-agent", "gitattributes-agent"],
         dependsOn: [],
         expectedOutputs: ["commitlint_audit", "gitignore_audit", "gitattributes_audit"]
       }
     ],
     totalAgents: 13,
     strategy: "Parallel execution in 4 waves for resource management",
     spawnInstructions: [
       "Wave 1: Spawn 4 code quality agents in parallel",
       "Wave 2: Spawn 3 build tool agents in parallel",
       "Wave 3: Spawn 3 infrastructure agents in parallel",
       "Wave 4: Spawn 3 version control agents in parallel"
     ]
   }
   ```

6. **/ms executes Wave 1 (4 agents in parallel)**

   ```typescript
   // All spawned concurrently
   Task("eslint-agent", "Audit ESLint configuration for MetaSaver compliance");
   Task(
     "prettier-agent",
     "Audit Prettier configuration for MetaSaver compliance"
   );
   Task(
     "typescript-agent",
     "Audit TypeScript configuration for MetaSaver compliance"
   );
   Task("editorconfig-agent", "Audit EditorConfig for MetaSaver compliance");
   ```

7. **/ms executes Wave 2 (3 agents in parallel)**

   ```typescript
   Task("vitest-agent", "Audit Vitest configuration for MetaSaver compliance");
   Task(
     "turbo-config-agent",
     "Audit Turbo configuration for MetaSaver compliance"
   );
   Task(
     "pnpm-workspace-agent",
     "Audit pnpm workspace configuration for MetaSaver compliance"
   );
   ```

8. **/ms executes Wave 3 (3 agents in parallel)**

   ```typescript
   Task(
     "docker-compose-agent",
     "Audit Docker configuration for MetaSaver compliance"
   );
   Task(
     "github-workflow-agent",
     "Audit GitHub workflows for MetaSaver compliance"
   );
   Task("husky-agent", "Audit Husky hooks for MetaSaver compliance");
   ```

9. **/ms executes Wave 4 (3 agents in parallel)**

   ```typescript
   Task(
     "commitlint-agent",
     "Audit Commitlint configuration for MetaSaver compliance"
   );
   Task("gitignore-agent", "Audit .gitignore for MetaSaver compliance");
   Task("gitattributes-agent", "Audit .gitattributes for MetaSaver compliance");
   ```

10. **Spawn reviewer with all worker results**

    ```typescript
    Task(
      "reviewer",
      "Review all 13 audit results. Assess overall compliance, identify patterns, validate findings."
    );
    ```

11. **Reviewer returns quality assessment**

    ```typescript
    {
      overallQuality: "good",
      consistencyScore: 88,
      coverageComplete: true,
      missedAreas: ["Environment variable security"],
      recommendations: ["Add security audit for .env patterns"]
    }
    ```

12. **Spawn project-manager with all results for consolidation**

    ```typescript
    Task(
      "project-manager",
      "Consolidate 13 audit results into executive report. Calculate total metrics, prioritize recommendations."
    );
    ```

13. **PM returns ConsolidatedReport**

    ```typescript
    {
      summary: "Monorepo audit completed with 91% average compliance. 2 critical issues in Turbo configuration require immediate attention.",
      statusByDomain: {
        "eslint": "PASS (96%)",
        "prettier": "PASS (100%)",
        "typescript": "PASS (94%)",
        "vitest": "PASS (98%)",
        "turbo": "FAIL (72%)",
        "pnpm-workspace": "PASS (95%)",
        "docker": "PASS (90%)",
        "github-workflows": "PARTIAL (85%)",
        "husky": "PASS (100%)",
        "commitlint": "PASS (92%)",
        "gitignore": "PASS (88%)",
        "gitattributes": "PASS (95%)",
        "editorconfig": "PASS (100%)"
      },
      totalMetrics: {
        totalAgentsExecuted: 13,
        totalViolations: 47,
        criticalViolations: 2,
        warningViolations: 45,
        averageCompliance: 91,
        domainsAudited: 13,
        domainsPassing: 11
      },
      recommendations: [
        "CRITICAL: Fix Turbo pipeline dependencies (outputs not properly configured)",
        "CRITICAL: Add missing task hashes in turbo.json",
        "WARNING: Update GitHub workflow to use latest Node version",
        "WARNING: Add missing file patterns to .gitignore",
        "INFO: Consider adding environment security audit to workflow"
      ],
      overallStatus: "partial"
    }
    ```

14. **/ms presents final report to user**

---

### Example 2: Coding Workflow - Add Product Entity with CRUD API

**User Request:** "Add Product entity with CRUD API"

**Workflow Execution:**

1. **/ms detects CODING workflow**

   ```
   Request contains "Add" + "entity" → CODING workflow selected
   Pipeline: Architect → PM → Workers → Validator → Reviewer → PM
   ```

2. **Spawn architect**

   ```typescript
   Task(
     "architect",
     "Design architecture for Product entity with CRUD API. Determine methodology, agents needed, and implementation order with dependencies."
   );
   ```

3. **Architect returns ArchitecturalDesign**

   ```typescript
   {
     featureType: "CRUD Entity with REST API",
     methodology: "sparc",
     agentsNeeded: [
       "contracts-agent",
       "tester",
       "prisma-database-agent",
       "data-service-agent",
       "react-component-agent"
     ],
     implementationOrder: [
       "contracts-agent",      // Specification first
       "tester",               // Tests before implementation (TDD)
       "prisma-database-agent",// Database schema
       "data-service-agent",   // REST API
       "react-component-agent" // UI components
     ],
     dependencies: [
       ["contracts-agent"],                    // Wave 1: No dependencies
       ["tester"],                             // Wave 2: Needs contracts
       ["prisma-database-agent"],              // Wave 3: Needs contracts
       ["data-service-agent"],                 // Wave 4: Needs database + tests
       ["react-component-agent"]               // Wave 5: Needs API + contracts
     ]
   }
   ```

4. **Spawn project-manager with Architect output**

   ```typescript
   Task(
     "project-manager",
     "Create execution plan for 5-agent SPARC implementation with strict dependency ordering."
   );
   ```

5. **PM returns ExecutionPlan**

   ```typescript
   {
     waves: [
       {
         waveNumber: 1,
         agents: ["contracts-agent"],
         dependsOn: [],
         expectedOutputs: ["product_types", "product_interfaces", "api_contracts"]
       },
       {
         waveNumber: 2,
         agents: ["tester"],
         dependsOn: ["product_types", "product_interfaces"],
         expectedOutputs: ["product_unit_tests", "product_integration_tests"]
       },
       {
         waveNumber: 3,
         agents: ["prisma-database-agent"],
         dependsOn: ["product_types"],
         expectedOutputs: ["product_schema", "product_migrations"]
       },
       {
         waveNumber: 4,
         agents: ["data-service-agent"],
         dependsOn: ["product_schema", "product_unit_tests"],
         expectedOutputs: ["product_service", "product_routes", "product_controllers"]
       },
       {
         waveNumber: 5,
         agents: ["react-component-agent"],
         dependsOn: ["product_service", "product_types"],
         expectedOutputs: ["product_list_component", "product_form_component", "product_hooks"]
       }
     ],
     totalAgents: 5,
     strategy: "Sequential wave execution with strict dependencies (SPARC methodology)",
     spawnInstructions: [
       "Wave 1: Define Product TypeScript types and API contracts",
       "Wave 2: Write comprehensive tests for Product (TDD approach)",
       "Wave 3: Create Prisma schema and migrations for Product",
       "Wave 4: Implement REST API service, routes, and controllers",
       "Wave 5: Build React components for Product CRUD UI"
     ]
   }
   ```

6. **/ms executes Wave 1 (contracts-agent)**

   ```typescript
   Task(
     "contracts-agent",
     "Create Product entity types: id, name, description, price, sku, stock, createdAt, updatedAt. Define ProductCreateInput, ProductUpdateInput, ProductResponse interfaces."
   );
   ```

7. **/ms executes Wave 2 (tester - TDD first)**

   ```typescript
   Task(
     "tester",
     "Write comprehensive tests for Product CRUD: unit tests for service methods, integration tests for API endpoints, validation tests for inputs. Use contracts from Wave 1."
   );
   ```

8. **/ms executes Wave 3 (prisma-database-agent)**

   ```typescript
   Task(
     "prisma-database-agent",
     "Create Product model in Prisma schema matching contracts. Add indexes, constraints, generate migration."
   );
   ```

9. **/ms executes Wave 4 (data-service-agent)**

   ```typescript
   Task(
     "data-service-agent",
     "Implement ProductService with CRUD operations. Create Express routes for /api/products. Implement validation, error handling, pagination."
   );
   ```

10. **/ms executes Wave 5 (react-component-agent)**

    ```typescript
    Task(
      "react-component-agent",
      "Build ProductList, ProductForm, ProductDetail components. Create useProducts hook. Implement CRUD UI with proper state management."
    );
    ```

11. **Spawn production-validator**

    ```typescript
    Task(
      "production-validator",
      "Validate Product implementation: run pnpm build, pnpm lint, pnpm test. Verify all checks pass."
    );
    ```

12. **Validator returns build/lint/test status**

    ```typescript
    {
      buildStatus: "pass",
      lintStatus: "pass",
      testStatus: "pass",
      testCoverage: 87,
      warnings: ["Consider adding index on Product.sku for performance"],
      blockers: []
    }
    ```

13. **Spawn reviewer**

    ```typescript
    Task(
      "reviewer",
      "Review Product implementation: code quality, architecture adherence, security, performance, best practices."
    );
    ```

14. **Reviewer returns code quality assessment**

    ```typescript
    {
      overallQuality: "excellent",
      adherenceToSPARC: true,
      securityIssues: [],
      performanceIssues: ["Consider lazy loading for ProductList"],
      codeSmells: [],
      recommendations: [
        "Add rate limiting to Product API endpoints",
        "Consider adding Product search functionality",
        "Add soft delete support"
      ]
    }
    ```

15. **Spawn project-manager with all results**

    ```typescript
    Task(
      "project-manager",
      "Consolidate Product implementation results. Summarize deliverables, validate all SPARC phases completed."
    );
    ```

16. **PM returns ConsolidatedReport**

    ```typescript
    {
      summary: "Product CRUD implementation completed successfully using SPARC methodology. All builds passing, 87% test coverage achieved.",
      statusByDomain: {
        "Specification (Contracts)": "COMPLETE - Types and interfaces defined",
        "Pseudocode (Tests)": "COMPLETE - Unit and integration tests written",
        "Architecture (Database)": "COMPLETE - Prisma schema with migrations",
        "Refinement (API)": "COMPLETE - REST service with validation",
        "Completion (UI)": "COMPLETE - React components with hooks"
      },
      totalMetrics: {
        totalAgentsExecuted: 5,
        filesCreated: 12,
        testsWritten: 24,
        testCoverage: 87,
        buildTime: 45,
        lintIssues: 0
      },
      recommendations: [
        "Add rate limiting to API endpoints",
        "Consider implementing search functionality",
        "Add soft delete for data retention",
        "Optimize ProductList with lazy loading"
      ],
      overallStatus: "pass"
    }
    ```

17. **/ms presents final report to user**

---

## Best Practices

1. **Always follow the defined pipeline order**
   - AUDIT: BA → PM → Workers → Reviewer → PM
   - CODING: Architect → PM → Workers → Validator → Reviewer → PM
   - Never skip phases

2. **Never skip validator for coding workflows**
   - Production Validator must verify build/lint/test
   - Catches integration issues before consolidation
   - Ensures deliverable quality

3. **PM bookends orchestration**
   - PM Phase 1: Planning and scheduling
   - PM Phase 2: Consolidation and reporting
   - PM provides consistency across workflows

4. **BA handles audit analysis, Architect handles design**
   - Business Analyst: Requirements, scope, success criteria
   - Architect: Technical design, dependencies, methodology
   - Clear separation of concerns

5. **Workers execute in parallel when no dependencies**
   - Maximize throughput for independent tasks
   - Use waves for dependent tasks
   - Resource management through wave sizing

6. **Consolidation must aggregate all results**
   - PM receives all worker outputs
   - Calculates aggregate metrics
   - Prioritizes recommendations
   - Provides actionable summary

7. **Workflow detection should be clear**
   - Use explicit keywords for detection
   - Default to SIMPLE for ambiguous cases
   - Allow manual override if needed

8. **Contracts ensure type safety**
   - All agent outputs follow defined interfaces
   - PM can reliably aggregate results
   - Enables tooling and validation

---

## Integration with /ms Command

The `/ms` command uses this skill to:

1. **Detect workflow type** from user request
2. **Load appropriate pipeline** from this skill
3. **Execute phases** in correct order
4. **Enforce contracts** between agents
5. **Handle wave execution** for parallel/sequential balance
6. **Consolidate results** through PM
7. **Present final report** to user

This skill ensures consistent, predictable orchestration across all task types while maximizing parallelism and maintaining quality gates.
