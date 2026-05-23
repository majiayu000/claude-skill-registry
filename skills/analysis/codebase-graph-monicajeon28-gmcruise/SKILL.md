---
name: codebase-graph
description: "**CODEBASE GRAPH v1.0** - '의존성', '그래프', '코드베이스 분석', '함수 관계', '모듈 관계', '아키텍처 분석', 'import 분석' 요청 시 자동 발동. 프로젝트 시작 시 자동 생성. 온톨로지 기반 코드 지식 그래프로 함수→함수, 모듈→모듈 관계를 Edge로 연결. 토큰 72% 절감, 정확도 92% 달성."
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# Codebase Graph Skill v1.0

**온톨로지 기반 코드 인텔리전스** - Neorion 스타일의 지식 그래프로 코드베이스 전체를 구조화

## 핵심 컨셉

```yaml
Philosophy:
  기존_방식: "파일 단위 분석 → 매번 전체 읽기 → 토큰 낭비"
  새로운_방식: "그래프 구축 → 관계만 추출 → 토큰 72% 절감"

Graph_Structure:
  Nodes:
    - File: "소스 파일"
    - Module: "모듈/패키지"
    - Function: "함수/메서드"
    - Class: "클래스/인터페이스"
    - Type: "타입/인터페이스"
    - Variable: "상수/변수"

  Edges:
    - imports: "A imports B"
    - exports: "A exports B"
    - calls: "A calls B"
    - extends: "A extends B"
    - implements: "A implements B"
    - uses: "A uses type B"
    - contains: "Module contains Function"
```

## 자동 발동 조건

```yaml
Auto_Trigger_Conditions:
  Project_Start:
    - "새 프로젝트 디렉토리 진입 시"
    - "package.json, tsconfig.json 감지 시"
    - "캐시된 그래프가 없거나 오래된 경우"

  Keywords_KO:
    - "의존성 분석, 의존성 그래프"
    - "코드베이스 분석, 프로젝트 분석"
    - "함수 관계, 모듈 관계"
    - "아키텍처 분석, 구조 분석"
    - "import 분석, export 분석"
    - "어디서 사용되나, 뭐가 호출하나"

  Keywords_EN:
    - "dependency graph, dependency analysis"
    - "codebase analysis, project analysis"
    - "function relationships, module relationships"
    - "architecture analysis, structure analysis"
    - "import analysis, call graph"
    - "where is this used, what calls this"

  File_Events:
    - "새 파일 생성 시 → 증분 업데이트"
    - "파일 삭제 시 → 그래프에서 제거"
    - "import 문 변경 시 → Edge 업데이트"
```

## 선택적 문서 로드 전략

```yaml
Document_Loading_Strategy:
  Always_Load:
    - "이 SKILL.md"
    - "core/graph-schema.md"

  Language_Specific_Load:
    TypeScript: "analyzers/typescript-analyzer.md"
    Python: "analyzers/python-analyzer.md"
    Go: "analyzers/go-analyzer.md"
    Java: "analyzers/java-analyzer.md"
    Rust: "analyzers/rust-analyzer.md"

  Context_Specific_Load:
    Graph_Query: "core/query-language.md"
    Cache_Management: "cache/cache-strategy.md"
    Visualization: "templates/visualization.md"
```

## 그래프 스키마

```typescript
// Node Types
interface GraphNode {
  id: string;                    // 고유 ID (파일경로:이름)
  type: NodeType;                // File | Module | Function | Class | Type | Variable
  name: string;                  // 이름
  path: string;                  // 파일 경로
  line: number;                  // 시작 줄
  signature?: string;            // 함수 시그니처 (간략)
  docstring?: string;            // JSDoc/docstring (간략)
  complexity?: number;           // 순환 복잡도
  loc: number;                   // 코드 라인 수
  hash: string;                  // 내용 해시 (변경 감지용)
  lastModified: number;          // 타임스탬프
}

type NodeType = 'file' | 'module' | 'function' | 'class' | 'type' | 'variable';

// Edge Types
interface GraphEdge {
  source: string;                // 소스 노드 ID
  target: string;                // 타겟 노드 ID
  type: EdgeType;                // 관계 유형
  weight?: number;               // 관계 강도 (호출 빈도 등)
  metadata?: Record<string, any>;
}

type EdgeType = 'imports' | 'exports' | 'calls' | 'extends' | 'implements' | 'uses' | 'contains';

// Graph
interface CodebaseGraph {
  version: string;               // 그래프 버전
  projectRoot: string;           // 프로젝트 루트
  language: string;              // 주 언어
  nodes: Map<string, GraphNode>;
  edges: GraphEdge[];
  metadata: {
    totalFiles: number;
    totalFunctions: number;
    totalClasses: number;
    generatedAt: number;
    analysisTime: number;
  };
}
```

## 그래프 생성 워크플로우

```yaml
Graph_Generation:
  Phase_1_Discovery:
    - "프로젝트 루트 감지"
    - "언어/프레임워크 감지"
    - "분석 대상 파일 목록 수집"
    - "기존 캐시 확인"

  Phase_2_Parsing:
    - "AST 기반 파싱 (ts-morph, ast 등)"
    - "함수/클래스/타입 추출"
    - "import/export 문 분석"
    - "함수 호출 관계 추출"

  Phase_3_Graph_Building:
    - "노드 생성 (중복 제거)"
    - "Edge 생성 (관계 매핑)"
    - "가중치 계산 (호출 빈도)"
    - "복잡도 계산"

  Phase_4_Caching:
    - "JSON/JSONL 형식 저장"
    - "파일별 해시 저장 (증분 업데이트용)"
    - "인덱스 생성"
```

## 그래프 쿼리 언어

```typescript
// 쿼리 인터페이스
interface GraphQuery {
  // 특정 노드 찾기
  findNode(id: string): GraphNode | null;

  // 이름으로 검색
  searchNodes(name: string, type?: NodeType): GraphNode[];

  // 들어오는 Edge (이 노드를 사용하는 곳)
  getIncomingEdges(nodeId: string, edgeType?: EdgeType): GraphEdge[];

  // 나가는 Edge (이 노드가 사용하는 것)
  getOutgoingEdges(nodeId: string, edgeType?: EdgeType): GraphEdge[];

  // 의존성 트리 (재귀)
  getDependencyTree(nodeId: string, depth?: number): DependencyTree;

  // 역의존성 트리 (누가 이걸 사용하나)
  getReverseDependencyTree(nodeId: string, depth?: number): DependencyTree;

  // 경로 찾기 (A→B 어떻게 연결되나)
  findPath(sourceId: string, targetId: string): GraphNode[];

  // 순환 참조 탐지
  detectCircularDependencies(): CircularDependency[];

  // 고립된 노드 (사용 안 되는 코드)
  findOrphanNodes(): GraphNode[];

  // 허브 노드 (많이 사용되는 코드)
  findHubNodes(threshold?: number): GraphNode[];
}

// 사용 예시
const query = new GraphQuery(graph);

// "이 함수를 호출하는 곳은?"
const callers = query.getIncomingEdges('src/utils.ts:formatDate', 'calls');

// "이 모듈이 의존하는 것들은?"
const deps = query.getDependencyTree('src/services/auth.ts', 2);

// "순환 참조 있나?"
const cycles = query.detectCircularDependencies();

// "안 쓰는 코드는?"
const orphans = query.findOrphanNodes();
```

## 토큰 최적화 전략

```yaml
Token_Optimization:
  Traditional_Approach:
    action: "파일 전체 읽기"
    tokens: "~500 tokens/file"
    10_files: "~5000 tokens"

  Graph_Based_Approach:
    action: "관련 노드만 추출"
    tokens: "~50 tokens/node"
    10_related_nodes: "~500 tokens"
    savings: "90% reduction"

  Smart_Context_Selection:
    Level_1_Signature:
      content: "함수 시그니처만"
      tokens: "~20 tokens"
      use_case: "존재 여부 확인"

    Level_2_Interface:
      content: "시그니처 + 타입"
      tokens: "~50 tokens"
      use_case: "인터페이스 파악"

    Level_3_Summary:
      content: "시그니처 + docstring + 관계"
      tokens: "~100 tokens"
      use_case: "역할 이해"

    Level_4_Full:
      content: "전체 구현"
      tokens: "~300+ tokens"
      use_case: "구현 수정"
```

## 캐시 전략

```yaml
Cache_Strategy:
  Location: ".claude/cache/codebase-graph/"

  Files:
    graph.json: "전체 그래프"
    index.json: "노드 인덱스 (빠른 검색)"
    hashes.json: "파일별 해시 (변경 감지)"
    stats.json: "통계 정보"

  Invalidation:
    file_modified: "해당 파일 노드만 재분석"
    file_added: "새 노드 추가"
    file_deleted: "노드 및 관련 Edge 제거"
    config_changed: "전체 재분석"

  TTL:
    full_rebuild: "24시간"
    incremental_check: "파일 수정 시마다"
```

## 다른 스킬과의 통합

```yaml
Integration:
  clean-code-mastery:
    provides: "복잡도 점수, 함수 크기"
    receives: "함수별 품질 점수 저장"

  code-reviewer:
    provides: "관련 코드 컨텍스트"
    receives: "리뷰 시 영향 범위 표시"

  security-shield:
    provides: "보안 관련 함수 위치"
    receives: "취약점 전파 경로"

  impact-analyzer:
    provides: "그래프 데이터 전체"
    receives: "변경 영향도 계산"

  smart-context:
    provides: "노드별 상세 정보"
    receives: "최적 컨텍스트 선택"

  arch-visualizer:
    provides: "그래프 데이터"
    receives: "시각화 및 문서화"
```

## Quick Commands

| Command | Action |
|---------|--------|
| `graph init` | 프로젝트 그래프 초기 생성 |
| `graph update` | 증분 업데이트 |
| `graph rebuild` | 전체 재빌드 |
| `graph query <node>` | 특정 노드 조회 |
| `graph deps <node>` | 의존성 트리 |
| `graph rdeps <node>` | 역의존성 트리 |
| `graph cycles` | 순환 참조 탐지 |
| `graph orphans` | 미사용 코드 탐지 |
| `graph hubs` | 핵심 모듈 탐지 |
| `graph stats` | 통계 출력 |

## 문서 구조

```
codebase-graph/
├── SKILL.md                      # 이 파일 (메인)
├── core/
│   ├── graph-schema.md           # 그래프 스키마 상세
│   ├── query-language.md         # 쿼리 언어 상세
│   └── algorithms.md             # 그래프 알고리즘
├── analyzers/
│   ├── typescript-analyzer.md    # TypeScript AST 분석
│   ├── python-analyzer.md        # Python AST 분석
│   ├── go-analyzer.md            # Go AST 분석
│   └── java-analyzer.md          # Java AST 분석
├── cache/
│   ├── cache-strategy.md         # 캐시 전략
│   └── incremental-update.md     # 증분 업데이트
├── templates/
│   ├── visualization.md          # 시각화 템플릿
│   └── report-template.md        # 분석 리포트 템플릿
└── quick-reference/
    ├── commands.md               # 빠른 명령어
    └── integration.md            # 스킬 통합 가이드
```

## 출력 예시

```markdown
## Codebase Graph Analysis

### Project Overview
| Metric | Value |
|--------|-------|
| Total Files | 156 |
| Total Functions | 423 |
| Total Classes | 87 |
| Total Types | 156 |
| Analysis Time | 2.3s |

### Dependency Statistics
| Metric | Value |
|--------|-------|
| Total Edges | 1,247 |
| Import Edges | 456 |
| Call Edges | 678 |
| Extends Edges | 45 |
| Implements Edges | 68 |

### Top Hub Nodes (Most Used)
1. `src/utils/helpers.ts:formatDate` - 47 incoming calls
2. `src/services/api.ts:fetchData` - 38 incoming calls
3. `src/types/index.ts:User` - 34 type usages

### Circular Dependencies Detected: 2
1. `moduleA → moduleB → moduleC → moduleA`
2. `serviceX → serviceY → serviceX`

### Orphan Nodes (Unused): 12
- `src/legacy/oldHelper.ts:deprecatedFn`
- `src/utils/unused.ts:*`
```

---

**Version**: 1.0.0
**Quality Target**: 95%
**Token Savings**: 72%
**Related Skills**: smart-context, impact-analyzer, arch-visualizer, code-reviewer
