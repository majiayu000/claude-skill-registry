---
name: "V3 QE DDD Architecture"
description: "Domain-Driven Design architecture for Agentic QE v3. Implements modular, bounded context architecture with clean separation of concerns for quality engineering domains."
---

# V3 QE DDD Architecture

## What This Skill Does

Designs and implements Domain-Driven Design (DDD) architecture for Agentic QE v3, decomposing quality engineering concerns into bounded contexts, implementing clean architecture patterns, and enabling modular, testable code structure optimized for AI-powered testing workflows.

## Quick Start

```bash
# Initialize DDD architecture analysis
Task("QE Architecture analysis", "Analyze current architecture and design DDD boundaries for quality engineering", "qe-quality-analyzer")

# Domain modeling (parallel)
Task("Domain decomposition", "Break down monolithic QE components into domains", "system-architect")
Task("Context mapping", "Map bounded contexts and relationships", "system-architect")
Task("Interface design", "Design clean domain interfaces for QE services", "system-architect")
```

## QE-Specific DDD Implementation Strategy

### Current Architecture Analysis
```
CURRENT: Monolithic QE Services
├── src/mcp/tools/ - All tool handlers in single directory
├── src/core/agents/ - Mixed agent responsibilities
├── src/core/memory/ - Multiple memory implementations
└── Tight coupling between test generation and execution

TARGET: Modular DDD Architecture for QE
├── src/domains/
│   ├── test-generation/        # AI test generation bounded context
│   ├── test-execution/         # Parallel test execution bounded context
│   ├── coverage-analysis/      # Coverage gap detection bounded context
│   ├── quality-assessment/     # Quality gates and metrics bounded context
│   ├── defect-intelligence/    # Defect prediction and analysis bounded context
│   └── learning-optimization/  # AI learning and pattern recognition bounded context
└── src/shared/
    ├── interfaces/             # Cross-domain interfaces
    ├── value-objects/          # Shared value objects
    └── domain-events/          # QE domain events
```

### Domain Boundaries for Quality Engineering

#### 1. Test Generation Domain
```typescript
// src/domains/test-generation/
interface TestGenerationDomain {
  // Entities
  TestCase: TestCaseEntity;
  TestSuite: TestSuiteEntity;
  TestPattern: TestPatternEntity;

  // Value Objects
  TestCaseId: TestCaseIdVO;
  CoverageTarget: CoverageTargetVO;
  TestStrategy: TestStrategyVO;  // unit, integration, e2e, property-based

  // Services
  AITestGenerator: AITestGenerationService;
  PatternRecognizer: PatternRecognitionService;
  MutationTestGenerator: MutationTestService;

  // Repository
  TestCaseRepository: ITestCaseRepository;
  PatternRepository: IPatternRepository;
}

// Domain Events
class TestCaseGeneratedEvent extends DomainEvent {
  constructor(
    testCaseId: string,
    sourceFile: string,
    coverageImpact: number,
    aiConfidence: number
  ) {
    super(testCaseId);
  }
}
```

#### 2. Test Execution Domain
```typescript
// src/domains/test-execution/
interface TestExecutionDomain {
  // Entities
  TestRun: TestRunEntity;
  ExecutionResult: ExecutionResultEntity;
  FlakyTestRecord: FlakyTestRecordEntity;

  // Value Objects
  ExecutionId: ExecutionIdVO;
  TestStatus: TestStatusVO;  // passed, failed, skipped, flaky
  Duration: DurationVO;

  // Services
  ParallelExecutor: ParallelExecutionService;
  FlakyDetector: FlakyTestDetectionService;
  RetryHandler: RetryHandlerService;

  // Repository
  TestRunRepository: ITestRunRepository;
  FlakyTestRepository: IFlakyTestRepository;
}
```

#### 3. Coverage Analysis Domain
```typescript
// src/domains/coverage-analysis/
interface CoverageAnalysisDomain {
  // Entities
  CoverageReport: CoverageReportEntity;
  CoverageGap: CoverageGapEntity;
  RiskZone: RiskZoneEntity;

  // Value Objects
  CoveragePercentage: CoveragePercentageVO;
  RiskScore: RiskScoreVO;
  FileComplexity: FileComplexityVO;

  // Services
  SublinearAnalyzer: SublinearCoverageAnalyzer;  // O(log n) analysis
  GapDetector: CoverageGapDetectionService;
  RiskScorer: RiskScoringService;

  // Repository
  CoverageRepository: ICoverageRepository;
}
```

#### 4. Quality Assessment Domain
```typescript
// src/domains/quality-assessment/
interface QualityAssessmentDomain {
  // Entities
  QualityGate: QualityGateEntity;
  QualityMetric: QualityMetricEntity;
  DeploymentDecision: DeploymentDecisionEntity;

  // Value Objects
  QualityScore: QualityScoreVO;
  GateStatus: GateStatusVO;  // pass, fail, warn
  Threshold: ThresholdVO;

  // Services
  QualityEvaluator: QualityEvaluationService;
  TrendAnalyzer: TrendAnalysisService;
  DeploymentAdvisor: DeploymentAdvisoryService;

  // Repository
  QualityMetricsRepository: IQualityMetricsRepository;
}
```

#### 5. Defect Intelligence Domain
```typescript
// src/domains/defect-intelligence/
interface DefectIntelligenceDomain {
  // Entities
  Defect: DefectEntity;
  RootCause: RootCauseEntity;
  DefectPrediction: DefectPredictionEntity;

  // Value Objects
  DefectId: DefectIdVO;
  Severity: SeverityVO;
  DefectCategory: DefectCategoryVO;

  // Services
  DefectPredictor: DefectPredictionService;
  RootCauseAnalyzer: RootCauseAnalysisService;
  PatternLearner: DefectPatternLearningService;

  // Repository
  DefectRepository: IDefectRepository;
}
```

## Microkernel Architecture Pattern for QE

### Core QE Kernel
```typescript
// src/core/kernel/qe-kernel.ts
export class QEKernel {
  private domains: Map<string, Domain> = new Map();
  private eventBus: DomainEventBus;
  private dependencyContainer: Container;

  async initialize(): Promise<void> {
    // Load core QE domains
    await this.loadDomain('test-generation', new TestGenerationDomain());
    await this.loadDomain('test-execution', new TestExecutionDomain());
    await this.loadDomain('coverage-analysis', new CoverageAnalysisDomain());
    await this.loadDomain('quality-assessment', new QualityAssessmentDomain());
    await this.loadDomain('defect-intelligence', new DefectIntelligenceDomain());

    // Wire up domain events for cross-domain communication
    this.setupDomainEventHandlers();
  }

  private setupDomainEventHandlers(): void {
    // When test is generated, trigger coverage analysis
    this.eventBus.subscribe(TestCaseGeneratedEvent, async (event) => {
      const coverageDomain = this.getDomain<CoverageAnalysisDomain>('coverage-analysis');
      await coverageDomain.analyzeCoverageImpact(event.testCaseId);
    });

    // When test run completes, update quality metrics
    this.eventBus.subscribe(TestRunCompletedEvent, async (event) => {
      const qualityDomain = this.getDomain<QualityAssessmentDomain>('quality-assessment');
      await qualityDomain.evaluateQualityGates(event.runId);
    });
  }
}
```

### Plugin Architecture for QE Extensions
```typescript
// src/plugins/
interface QEPlugin {
  name: string;
  version: string;
  dependencies: string[];

  initialize(kernel: QEKernel): Promise<void>;
  shutdown(): Promise<void>;
}

// Example: n8n Workflow Testing Plugin
export class N8nWorkflowPlugin implements QEPlugin {
  name = 'n8n-workflow-testing';
  version = '3.0.0';
  dependencies = ['test-execution'];

  async initialize(kernel: QEKernel): Promise<void> {
    const testDomain = kernel.getDomain<TestExecutionDomain>('test-execution');

    // Register n8n-specific test execution strategies
    this.workflowExecutor = new N8nWorkflowExecutor(testDomain);
    kernel.registerService('n8n-executor', this.workflowExecutor);
  }
}

// Example: Visual Regression Testing Plugin
export class VisualTestingPlugin implements QEPlugin {
  name = 'visual-regression';
  version = '3.0.0';
  dependencies = ['test-execution', 'coverage-analysis'];

  async initialize(kernel: QEKernel): Promise<void> {
    kernel.registerService('visual-tester', new VisualRegressionService());
  }
}
```

## Domain Events & Integration

### Event-Driven Communication Between QE Domains
```typescript
// src/shared/domain-events/
abstract class QEDomainEvent {
  public readonly eventId: string;
  public readonly aggregateId: string;
  public readonly occurredOn: Date;
  public readonly eventVersion: number;

  constructor(aggregateId: string) {
    this.eventId = crypto.randomUUID();
    this.aggregateId = aggregateId;
    this.occurredOn = new Date();
    this.eventVersion = 1;
  }
}

// Test Generation Events
export class TestSuiteCreatedEvent extends QEDomainEvent {
  constructor(
    suiteId: string,
    public readonly testCount: number,
    public readonly targetCoverage: number,
    public readonly aiModel: string
  ) {
    super(suiteId);
  }
}

// Test Execution Events
export class TestRunCompletedEvent extends QEDomainEvent {
  constructor(
    runId: string,
    public readonly passed: number,
    public readonly failed: number,
    public readonly flaky: number,
    public readonly duration: number
  ) {
    super(runId);
  }
}

// Coverage Events
export class CoverageGapDetectedEvent extends QEDomainEvent {
  constructor(
    reportId: string,
    public readonly filePath: string,
    public readonly uncoveredLines: number[],
    public readonly riskScore: number
  ) {
    super(reportId);
  }
}

// Quality Gate Events
export class QualityGateEvaluatedEvent extends QEDomainEvent {
  constructor(
    gateId: string,
    public readonly status: 'pass' | 'fail' | 'warn',
    public readonly metrics: QualityMetrics,
    public readonly recommendation: string
  ) {
    super(gateId);
  }
}

// Event Handlers for Cross-Domain Coordination
@EventHandler(CoverageGapDetectedEvent)
export class CoverageGapHandler {
  constructor(
    private testGenerator: AITestGenerationService,
    private riskScorer: RiskScoringService
  ) {}

  async handle(event: CoverageGapDetectedEvent): Promise<void> {
    // Automatically generate tests for high-risk coverage gaps
    if (event.riskScore > 0.7) {
      await this.testGenerator.generateForGap(
        event.filePath,
        event.uncoveredLines
      );
    }
  }
}
```

## Clean Architecture Layers for QE

```typescript
// Architecture layers
┌─────────────────────────────────────────┐
│              Presentation               │  <- MCP Tools, CLI Commands
├─────────────────────────────────────────┤
│              Application                │  <- Use Cases, QE Orchestration
├─────────────────────────────────────────┤
│               Domain                    │  <- Entities, Services, Events
├─────────────────────────────────────────┤
│            Infrastructure               │  <- AgentDB, SQLite, AI Models
└─────────────────────────────────────────┘

// Dependency direction: Outside → Inside
// Domain layer has NO external dependencies
```

### Application Layer (QE Use Cases)
```typescript
// src/application/use-cases/
export class GenerateTestsUseCase {
  constructor(
    private testGenerator: AITestGenerationService,
    private coverageAnalyzer: SublinearCoverageAnalyzer,
    private patternRepository: IPatternRepository,
    private eventBus: DomainEventBus
  ) {}

  async execute(command: GenerateTestsCommand): Promise<GenerateTestsResult> {
    // 1. Analyze current coverage gaps (O(log n) with sublinear algorithm)
    const gaps = await this.coverageAnalyzer.findGaps(command.sourceFiles);

    // 2. Retrieve successful patterns from memory
    const patterns = await this.patternRepository.findByContext(
      command.framework,
      command.testType
    );

    // 3. Generate AI-powered tests with learned patterns
    const tests = await this.testGenerator.generate({
      sourceFiles: command.sourceFiles,
      coverageGaps: gaps,
      learnedPatterns: patterns,
      framework: command.framework,
      aiModel: command.aiModel || 'claude-sonnet'
    });

    // 4. Publish domain events
    for (const test of tests) {
      this.eventBus.publish(new TestCaseGeneratedEvent(
        test.id,
        test.sourceFile,
        test.coverageImpact,
        test.aiConfidence
      ));
    }

    return GenerateTestsResult.success(tests);
  }
}
```

## ADR Integration for QE v3

### ADR-001: Adopt DDD for QE Bounded Contexts
- **Decision**: Decompose QE services into 5 core bounded contexts
- **Rationale**: Clear separation enables parallel development and testing
- **Consequences**: Migration effort required, but long-term maintainability improved

### ADR-002: Event-Driven Domain Communication
- **Decision**: Use domain events for cross-domain coordination
- **Rationale**: Loose coupling, enables reactive test generation
- **Consequences**: Event store required, eventual consistency model

### ADR-003: Plugin Architecture for QE Extensions
- **Decision**: Implement microkernel pattern with plugin system
- **Rationale**: Enables n8n, visual, performance testing as plugins
- **Consequences**: Plugin API must remain stable

### ADR-004: Sublinear Algorithms for Scale
- **Decision**: Use O(log n) algorithms for coverage analysis
- **Rationale**: QE must scale to large codebases efficiently
- **Consequences**: HNSW indexing required in AgentDB

## Migration Strategy

### Phase 1: Extract Domain Services (Week 1-2)
```typescript
const extractionPlan = {
  week1: [
    'TestGenerator → test-generation domain',
    'TestExecutor → test-execution domain'
  ],
  week2: [
    'CoverageAnalyzer → coverage-analysis domain',
    'QualityGate → quality-assessment domain'
  ],
  week3: [
    'DefectAnalyzer → defect-intelligence domain',
    'Wire up domain events'
  ]
};
```

## Success Metrics

- [ ] **Domain Isolation**: 5 QE domains with clean boundaries
- [ ] **Plugin Architecture**: Core + optional QE plugins loading
- [ ] **Clean Architecture**: Dependency inversion maintained
- [ ] **Event-Driven Communication**: Loose coupling between domains
- [ ] **Test Coverage**: >90% domain logic coverage
- [ ] **Sublinear Performance**: O(log n) coverage analysis maintained

## Related V3 Skills

- `v3-qe-test-generation` - AI test generation implementation
- `v3-qe-coverage-optimization` - Sublinear coverage analysis
- `v3-qe-quality-gates` - Quality gate evaluation
- `v3-qe-learning-system` - AI pattern learning

## Usage Examples

### Complete QE Domain Extraction
```bash
# Full DDD architecture implementation for QE
Task("QE DDD architecture implementation",
     "Extract monolithic QE services into DDD domains with clean architecture",
     "system-architect")
```

### Single Domain Implementation
```bash
# Implement specific QE domain
Task("Test generation domain",
     "Implement test generation domain with AI-powered generation and pattern learning",
     "qe-test-generator")
```
