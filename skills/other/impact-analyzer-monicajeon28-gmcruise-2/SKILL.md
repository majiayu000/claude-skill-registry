---
name: impact-analyzer
description: "**IMPACT ANALYZER v1.0** - '영향도', '영향 범위', '변경 영향', '리팩토링 영향', '이거 바꾸면', '어디에 영향', '위험도' 요청 시 자동 발동. codebase-graph 기반 변경 전파 분석. 직접/간접 영향, 위험도 점수, 테스트 범위 제안. 코드 수정 전 필수 분석."
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Impact Analyzer Skill v1.0

**변경 영향도 분석기** - 코드 수정 전 영향 범위를 정확히 파악하여 안전한 변경 보장

## 핵심 컨셉

```yaml
Problem:
  Without_Analysis: "함수 수정 → 예상치 못한 곳에서 에러 → 롤백"
  Reality: "한 줄 변경이 100개 파일에 영향을 줄 수 있음"

Solution:
  Impact_Analysis:
    - "변경 대상의 역의존성 트리 추적"
    - "직접/간접 영향 범위 계산"
    - "위험도 점수 산출"
    - "테스트 범위 자동 제안"

Key_Metrics:
  Direct_Impact: "직접 호출하는 함수들"
  Indirect_Impact: "연쇄적으로 영향받는 범위"
  Risk_Score: "변경 위험도 (0-100)"
  Test_Coverage: "영향 범위 대비 테스트 커버리지"
```

## 자동 발동 조건

```yaml
Auto_Trigger_Conditions:
  Before_Edit:
    - "Edit 도구 사용 전 자동 분석 제안"
    - "공유 코드(shared, utils) 수정 시"
    - "핵심 모듈(auth, api) 수정 시"

  Keywords_KO:
    - "영향도 분석, 영향 범위"
    - "이거 바꾸면 어디 영향?"
    - "변경 영향, 수정 영향"
    - "리팩토링 영향, 리팩토링 범위"
    - "위험도, 얼마나 위험"
    - "테스트 범위, 테스트해야 할 곳"

  Keywords_EN:
    - "impact analysis, impact scope"
    - "what will this affect"
    - "change impact, modification impact"
    - "refactoring scope, refactoring impact"
    - "risk assessment, risk score"
    - "test scope, what to test"

  High_Risk_Patterns:
    - "export 변경/삭제"
    - "함수 시그니처 변경"
    - "타입 정의 변경"
    - "API 엔드포인트 변경"
    - "shared 모듈 변경"
```

## 영향도 분석 알고리즘

```typescript
interface ImpactAnalysisRequest {
  target: string;                 // 변경 대상 노드 ID
  changeType: ChangeType;         // 변경 유형
  depth?: number;                 // 분석 깊이 (기본 3)
}

type ChangeType =
  | 'signature'      // 시그니처 변경 (파라미터, 반환타입)
  | 'implementation' // 구현 변경 (로직)
  | 'rename'         // 이름 변경
  | 'delete'         // 삭제
  | 'move'           // 이동
  | 'type'           // 타입 변경
  ;

interface ImpactResult {
  target: GraphNode;              // 변경 대상
  changeType: ChangeType;
  directImpact: ImpactNode[];     // 직접 영향
  indirectImpact: ImpactNode[];   // 간접 영향
  totalAffected: number;          // 총 영향받는 노드 수
  riskScore: number;              // 위험도 (0-100)
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  testSuggestions: TestSuggestion[];  // 테스트 제안
  warnings: string[];             // 경고 메시지
}

interface ImpactNode {
  node: GraphNode;
  depth: number;                  // 영향 깊이 (1=직접, 2+=간접)
  impactType: 'caller' | 'type-user' | 'importer' | 'extender';
  confidence: number;             // 영향 확실성 (0-1)
  reason: string;                 // 영향 이유
}
```

### 영향 범위 계산

```typescript
class ImpactAnalyzer {
  private graph: CodebaseGraph;

  constructor(graph: CodebaseGraph) {
    this.graph = graph;
  }

  /**
   * 영향도 분석 실행
   */
  analyze(request: ImpactAnalysisRequest): ImpactResult {
    const target = this.graph.findNode(request.target);
    if (!target) {
      throw new Error(`Node not found: ${request.target}`);
    }

    // 1. 직접 영향 수집
    const directImpact = this.collectDirectImpact(target, request.changeType);

    // 2. 간접 영향 수집 (재귀)
    const indirectImpact = this.collectIndirectImpact(
      directImpact,
      request.depth || 3
    );

    // 3. 위험도 계산
    const riskScore = this.calculateRiskScore(target, directImpact, indirectImpact, request.changeType);

    // 4. 테스트 제안 생성
    const testSuggestions = this.generateTestSuggestions(target, directImpact, indirectImpact);

    // 5. 경고 생성
    const warnings = this.generateWarnings(target, directImpact, request.changeType);

    return {
      target,
      changeType: request.changeType,
      directImpact,
      indirectImpact,
      totalAffected: directImpact.length + indirectImpact.length,
      riskScore,
      riskLevel: this.getRiskLevel(riskScore),
      testSuggestions,
      warnings,
    };
  }

  /**
   * 직접 영향 수집
   */
  private collectDirectImpact(target: GraphNode, changeType: ChangeType): ImpactNode[] {
    const impacts: ImpactNode[] = [];

    // 1. 이 노드를 호출하는 함수들
    const callers = this.graph.getIncomingEdges(target.id, 'calls');
    for (const edge of callers) {
      const caller = this.graph.findNode(edge.source);
      if (caller) {
        impacts.push({
          node: caller,
          depth: 1,
          impactType: 'caller',
          confidence: changeType === 'signature' ? 1.0 : 0.7,
          reason: `Calls ${target.name}`,
        });
      }
    }

    // 2. 이 타입을 사용하는 곳
    if (target.type === 'type' || target.type === 'class') {
      const typeUsers = this.graph.getIncomingEdges(target.id, 'uses');
      for (const edge of typeUsers) {
        const user = this.graph.findNode(edge.source);
        if (user) {
          impacts.push({
            node: user,
            depth: 1,
            impactType: 'type-user',
            confidence: changeType === 'type' ? 1.0 : 0.5,
            reason: `Uses type ${target.name}`,
          });
        }
      }
    }

    // 3. 이 모듈을 import하는 파일들
    const importers = this.graph.getIncomingEdges(target.id, 'imports');
    for (const edge of importers) {
      const importer = this.graph.findNode(edge.source);
      if (importer && !impacts.some(i => i.node.id === importer.id)) {
        impacts.push({
          node: importer,
          depth: 1,
          impactType: 'importer',
          confidence: changeType === 'rename' || changeType === 'delete' ? 1.0 : 0.3,
          reason: `Imports from ${target.path}`,
        });
      }
    }

    // 4. 이 클래스를 상속하는 클래스들
    if (target.type === 'class') {
      const extenders = this.graph.getIncomingEdges(target.id, 'extends');
      for (const edge of extenders) {
        const extender = this.graph.findNode(edge.source);
        if (extender) {
          impacts.push({
            node: extender,
            depth: 1,
            impactType: 'extender',
            confidence: 1.0,
            reason: `Extends ${target.name}`,
          });
        }
      }
    }

    return impacts;
  }

  /**
   * 간접 영향 수집 (BFS)
   */
  private collectIndirectImpact(directImpact: ImpactNode[], maxDepth: number): ImpactNode[] {
    const indirect: ImpactNode[] = [];
    const visited = new Set<string>(directImpact.map(i => i.node.id));
    const queue: ImpactNode[] = [...directImpact];

    while (queue.length > 0) {
      const current = queue.shift()!;

      if (current.depth >= maxDepth) continue;

      // 현재 노드의 호출자들 수집
      const callers = this.graph.getIncomingEdges(current.node.id, 'calls');

      for (const edge of callers) {
        if (visited.has(edge.source)) continue;

        const caller = this.graph.findNode(edge.source);
        if (!caller) continue;

        visited.add(caller.id);

        const impactNode: ImpactNode = {
          node: caller,
          depth: current.depth + 1,
          impactType: 'caller',
          confidence: current.confidence * 0.7, // 깊이에 따라 감소
          reason: `Indirect via ${current.node.name}`,
        };

        indirect.push(impactNode);
        queue.push(impactNode);
      }
    }

    return indirect;
  }

  /**
   * 위험도 점수 계산
   */
  private calculateRiskScore(
    target: GraphNode,
    direct: ImpactNode[],
    indirect: ImpactNode[],
    changeType: ChangeType
  ): number {
    let score = 0;

    // 1. 변경 유형 기본 점수
    const changeTypeScores: Record<ChangeType, number> = {
      implementation: 20,
      signature: 50,
      type: 60,
      rename: 40,
      move: 45,
      delete: 80,
    };
    score += changeTypeScores[changeType];

    // 2. 직접 영향 수 (각 +3점, 최대 30점)
    score += Math.min(direct.length * 3, 30);

    // 3. 간접 영향 수 (각 +1점, 최대 20점)
    score += Math.min(indirect.length, 20);

    // 4. 대상 특성 보정
    if (target.isExported) score += 10;           // export된 것
    if (target.path.includes('shared')) score += 15; // shared 모듈
    if (target.path.includes('api')) score += 10;    // API 관련
    if (target.path.includes('auth')) score += 15;   // 인증 관련
    if (target.type === 'type') score += 10;         // 타입 정의

    // 5. 테스트 커버리지 보정
    const hasTests = this.hasTestCoverage(target);
    if (!hasTests) score += 10; // 테스트 없으면 위험

    return Math.min(score, 100);
  }

  /**
   * 위험 수준 결정
   */
  private getRiskLevel(score: number): 'low' | 'medium' | 'high' | 'critical' {
    if (score < 30) return 'low';
    if (score < 50) return 'medium';
    if (score < 75) return 'high';
    return 'critical';
  }

  /**
   * 테스트 제안 생성
   */
  private generateTestSuggestions(
    target: GraphNode,
    direct: ImpactNode[],
    indirect: ImpactNode[]
  ): TestSuggestion[] {
    const suggestions: TestSuggestion[] = [];

    // 1. 대상 테스트
    suggestions.push({
      target: target.id,
      priority: 'critical',
      reason: 'Direct change target',
      testType: 'unit',
    });

    // 2. 직접 영향 테스트
    for (const impact of direct.slice(0, 10)) { // 상위 10개
      suggestions.push({
        target: impact.node.id,
        priority: impact.confidence > 0.8 ? 'high' : 'medium',
        reason: impact.reason,
        testType: impact.impactType === 'caller' ? 'integration' : 'unit',
      });
    }

    // 3. 고확신 간접 영향 테스트
    const highConfidenceIndirect = indirect.filter(i => i.confidence > 0.5);
    for (const impact of highConfidenceIndirect.slice(0, 5)) {
      suggestions.push({
        target: impact.node.id,
        priority: 'low',
        reason: `${impact.reason} (indirect)`,
        testType: 'integration',
      });
    }

    return suggestions;
  }

  /**
   * 경고 생성
   */
  private generateWarnings(
    target: GraphNode,
    direct: ImpactNode[],
    changeType: ChangeType
  ): string[] {
    const warnings: string[] = [];

    // 1. 높은 영향 범위
    if (direct.length > 20) {
      warnings.push(`HIGH IMPACT: This change affects ${direct.length} direct callers`);
    }

    // 2. export 삭제/변경
    if (target.isExported && (changeType === 'delete' || changeType === 'rename')) {
      warnings.push(`BREAKING: Modifying exported symbol may break external consumers`);
    }

    // 3. 핵심 모듈 변경
    if (target.path.includes('shared') || target.path.includes('core')) {
      warnings.push(`CORE MODULE: Changes to shared/core modules require extra caution`);
    }

    // 4. 테스트 부족
    if (!this.hasTestCoverage(target)) {
      warnings.push(`NO TESTS: Target has no test coverage - add tests before changing`);
    }

    // 5. 순환 참조 관련
    const cycles = this.graph.detectCircularDependencies();
    if (cycles.some(c => c.includes(target.id))) {
      warnings.push(`CIRCULAR: Target is part of circular dependency - changes may cascade unpredictably`);
    }

    return warnings;
  }

  private hasTestCoverage(node: GraphNode): boolean {
    // 테스트 파일 존재 확인
    const testPatterns = [
      node.path.replace('.ts', '.test.ts'),
      node.path.replace('.ts', '.spec.ts'),
      node.path.replace('/src/', '/test/'),
    ];

    return testPatterns.some(pattern =>
      this.graph.findNode(pattern) !== null
    );
  }
}
```

## 위험도 점수 기준

```yaml
Risk_Scoring:
  Base_Scores_by_Change_Type:
    implementation: 20    # 로직만 변경
    signature: 50         # 시그니처 변경
    type: 60              # 타입 정의 변경
    rename: 40            # 이름 변경
    move: 45              # 위치 이동
    delete: 80            # 삭제

  Modifiers:
    direct_impact: "+3 per caller (max 30)"
    indirect_impact: "+1 per node (max 20)"
    is_exported: "+10"
    in_shared: "+15"
    in_api: "+10"
    in_auth: "+15"
    is_type: "+10"
    no_tests: "+10"

  Risk_Levels:
    low: "0-29 (안전한 변경)"
    medium: "30-49 (주의 필요)"
    high: "50-74 (신중한 검토 필요)"
    critical: "75-100 (위험, 충분한 테스트 필수)"
```

## 출력 템플릿

```markdown
## Impact Analysis Report

### Target: {{targetName}}
- **Path**: {{targetPath}}:{{targetLine}}
- **Type**: {{targetType}}
- **Change Type**: {{changeType}}

---

### Risk Assessment
| Metric | Value |
|--------|-------|
| Risk Score | {{riskScore}}/100 |
| Risk Level | {{riskLevel}} |
| Direct Impact | {{directCount}} nodes |
| Indirect Impact | {{indirectCount}} nodes |
| Total Affected | {{totalAffected}} nodes |

---

### Direct Impact ({{directCount}} nodes)
| Node | Type | Reason | Confidence |
|------|------|--------|------------|
{{#each directImpact}}
| {{node.name}} | {{impactType}} | {{reason}} | {{confidence}}% |
{{/each}}

---

### Indirect Impact (Top 10 of {{indirectCount}})
| Node | Depth | Reason | Confidence |
|------|-------|--------|------------|
{{#each indirectImpact}}
| {{node.name}} | {{depth}} | {{reason}} | {{confidence}}% |
{{/each}}

---

### Warnings
{{#each warnings}}
- {{this}}
{{/each}}

---

### Recommended Tests
| Target | Priority | Type | Reason |
|--------|----------|------|--------|
{{#each testSuggestions}}
| {{target}} | {{priority}} | {{testType}} | {{reason}} |
{{/each}}

---

### Verdict
{{#if riskLevel === 'critical'}}
**CRITICAL**: Do NOT proceed without comprehensive test coverage and review.
{{else if riskLevel === 'high'}}
**HIGH RISK**: Proceed with caution. Ensure all suggested tests pass.
{{else if riskLevel === 'medium'}}
**MEDIUM RISK**: Safe to proceed with standard review process.
{{else}}
**LOW RISK**: Safe to proceed. Minor change with limited impact.
{{/if}}
```

## Quick Commands

| Command | Action |
|---------|--------|
| `impact <target>` | 기본 영향도 분석 |
| `impact signature <target>` | 시그니처 변경 영향도 |
| `impact delete <target>` | 삭제 영향도 |
| `impact rename <target>` | 이름 변경 영향도 |
| `impact depth <n> <target>` | 깊이 지정 분석 |
| `impact test <target>` | 테스트 제안만 |
| `impact warnings <target>` | 경고만 |

## 다른 스킬과의 통합

```yaml
Integration:
  codebase-graph:
    type: "데이터 소스"
    usage: "그래프 쿼리, 역의존성 추적"

  smart-context:
    type: "협력"
    usage: "영향 범위 컨텍스트 생성"

  code-reviewer:
    type: "소비자"
    usage: "리뷰 시 영향도 표시"

  tdd-guardian:
    type: "소비자"
    usage: "테스트 범위 제안 수신"

  vibe-coding-orchestrator:
    type: "제공자"
    usage: "대규모 리팩토링 전 자동 분석"
```

## 문서 구조

```
impact-analyzer/
├── SKILL.md                      # 이 파일 (메인)
├── core/
│   ├── impact-calculation.md     # 영향도 계산 상세
│   ├── risk-scoring.md           # 위험도 점수 체계
│   └── test-suggestion.md        # 테스트 제안 알고리즘
├── algorithms/
│   ├── reverse-dependency.md     # 역의존성 추적
│   ├── propagation.md            # 영향 전파 알고리즘
│   └── confidence.md             # 확신도 계산
├── templates/
│   ├── report-template.md        # 리포트 템플릿
│   └── warning-templates.md      # 경고 메시지 템플릿
└── quick-reference/
    ├── commands.md               # 명령어 가이드
    └── risk-guide.md             # 위험도 해석 가이드
```

---

**Version**: 1.0.0
**Quality Target**: 95%
**Required Skill**: codebase-graph
**Related Skills**: smart-context, code-reviewer, tdd-guardian
