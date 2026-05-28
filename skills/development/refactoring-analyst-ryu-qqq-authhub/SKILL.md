---
name: refactoring-analyst
version: 1.0.0
description: |
  리팩토링 분석 전문가. 기존 코드베이스를 컨벤션 기준으로 분석.
  Zero-Tolerance 위반 탐지, 영향도 분석, 단계별 리팩토링 계획 수립.
  /refactor-plan 명령 시 자동 활성화. Serena Memory에 결과 저장.
author: claude-spring-standards
created: 2025-12-05
updated: 2025-12-05
tags: [project, refactoring, analysis, legacy, migration]
---

# Refactoring Analyst (리팩토링 분석가)

## 목적 (Purpose)

**기존 레거시 코드 → 컨벤션 준수 코드**로 전환하기 위한 분석 및 계획 수립 전문가입니다.
Zero-Tolerance 위반을 탐지하고, 영향도를 분석하여 단계별 리팩토링 계획을 생성합니다.

## 활성화 조건

- `/refactor-plan` 커맨드 실행 시
- 기존 프로젝트 컨벤션 적용 요청 시
- 레거시 코드 분석 요청 시
- "이 코드 컨벤션에 맞춰줘" 같은 요청 시

## 산출물 (Output)

| 산출물 | 형식 | 저장 위치 |
|--------|------|----------|
| 위반 사항 보고서 | Markdown Table | 대화 컨텍스트 |
| 영향도 분석 | Dependency Matrix | 대화 컨텍스트 |
| 리팩토링 계획 | Phase/Step 구조 | Serena Memory |
| 진행 체크리스트 | Checkbox List | Serena Memory |

## 완료 기준 (Acceptance Criteria)

- [ ] 모든 Zero-Tolerance 위반이 식별됨
- [ ] 위반별 영향 파일 수가 집계됨
- [ ] Phase별 리팩토링 계획이 수립됨
- [ ] Serena Memory에 `refactor-plan-{project}` 저장됨
- [ ] 다음 단계 실행 가능한 상태

---

## 분석 프로세스

```
┌─────────────────────────────────────────────────────────────┐
│              Refactoring Analysis Flow                       │
├─────────────────────────────────────────────────────────────┤
│  1️⃣ 코드베이스 스캔 (Codebase Scan)                         │
│     └─ Serena MCP로 전체 구조 파악                          │
│                                                              │
│  2️⃣ 위반 탐지 (Violation Detection)                        │
│     └─ 패턴 매칭으로 위반 사항 식별                          │
│                                                              │
│  3️⃣ 영향도 분석 (Impact Analysis)                          │
│     └─ 변경 범위 및 의존성 파악                              │
│                                                              │
│  4️⃣ 우선순위 결정 (Priority Decision)                      │
│     └─ Critical → Important → Recommended                   │
│                                                              │
│  5️⃣ 계획 생성 (Plan Generation)                            │
│     └─ Phase/Step 구조로 계획 수립                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ Zero-Tolerance 위반 탐지 패턴

### 🔴 Critical Violations

#### Lombok 사용 탐지

```bash
# Serena search_for_pattern 사용
pattern: "import lombok\\."
pattern: "@Data|@Getter|@Setter|@Builder"
pattern: "@AllArgsConstructor|@NoArgsConstructor"
pattern: "@ToString|@EqualsAndHashCode"
```

**분석 결과 형식:**
```markdown
### Lombok 사용 현황
| 파일 | 사용 어노테이션 | 라인 |
|------|----------------|------|
| User.java | @Data, @Builder | 5, 12 |
| Order.java | @Getter, @Setter | 8, 9 |
```

#### Law of Demeter 위반 탐지

```bash
# Getter 체이닝 패턴
pattern: "\\.get[A-Z][a-zA-Z]*\\(\\)\\.get"
pattern: "\\.get[A-Z][a-zA-Z]*\\(\\)\\.[a-z]"
```

**분석 결과 형식:**
```markdown
### Law of Demeter 위반 현황
| 파일 | 위반 코드 | 라인 |
|------|----------|------|
| OrderService.java | order.getUser().getAddress() | 45 |
| PaymentService.java | payment.getOrder().getTotal() | 23 |
```

#### JPA 관계 어노테이션 탐지

```bash
pattern: "@OneToMany|@ManyToOne"
pattern: "@OneToOne|@ManyToMany"
pattern: "@JoinColumn|@JoinTable"
```

**분석 결과 형식:**
```markdown
### JPA 관계 어노테이션 현황
| Entity | 어노테이션 | 관계 대상 | 라인 |
|--------|-----------|----------|------|
| OrderEntity | @ManyToOne | UserEntity | 34 |
| OrderEntity | @OneToMany | OrderItemEntity | 45 |
```

#### Transaction 경계 위반 탐지

```bash
# @Transactional 메서드 내 외부 호출
pattern: "@Transactional"
# 이후 같은 메서드 내에서:
pattern: "RestTemplate|WebClient|FeignClient"
pattern: "kafkaTemplate\\.send|rabbitTemplate\\.send"
```

---

### 🟡 Important Violations

#### CQRS 미분리 탐지

```bash
# 같은 Service에서 Command/Query 혼재
pattern: "class.*Service"
# 내부에 create/update/delete와 find/get/search 혼재 확인
```

#### DTO 미분리 탐지

```bash
# Entity 직접 반환
pattern: "return.*Entity"
pattern: "ResponseEntity<.*Entity>"

# Request/Response 같은 DTO
pattern: "class.*Dto|class.*DTO"
# 사용처가 Request와 Response 양쪽인지 확인
```

#### MockMvc 사용 탐지

```bash
pattern: "MockMvc|@WebMvcTest"
pattern: "mockMvc\\.perform"
```

---

### 🟢 Recommended Improvements

#### 네이밍 컨벤션 미준수

```bash
# UseCase 접미사 확인
pattern: "interface.*UseCase"
# 없으면 위반

# Service 접미사 확인
pattern: "class.*Service"
# TransactionManager, QueryService 구분 확인
```

#### Record 미사용 DTO

```bash
# class로 선언된 DTO
pattern: "class.*(Command|Query|Response|Request)\\s"
# record가 아니면 개선 대상
```

---

## 2️⃣ 영향도 분석 매트릭스

### 분석 템플릿

```markdown
## 영향도 분석 결과

### 변경 영향 매트릭스

| 위반 유형 | 파일 수 | 영향 모듈 | 위험도 | 작업량 | 우선순위 |
|-----------|---------|----------|--------|--------|----------|
| Lombok 제거 | 45 | 전체 | 🔴 | 대 | 1 |
| Long FK 전환 | 12 | Persistence | 🔴 | 대 | 2 |
| CQRS 분리 | 23 | Application | 🟡 | 중 | 3 |
| DTO 분리 | 34 | 전체 | 🟡 | 중 | 4 |
| Assembler 추가 | 15 | Application | 🟢 | 소 | 5 |

### 의존성 순서

```
1. Lombok 제거 (선행 조건 없음)
   ↓
2. Long FK 전환 (Lombok 제거 후)
   ↓
3. CQRS 분리 (Long FK 전환 후)
   ↓
4. DTO 분리 (CQRS 분리와 병행 가능)
   ↓
5. Assembler 추가 (DTO 분리 후)
```
```

---

## 3️⃣ 리팩토링 계획 생성

### Phase 구조 템플릿

```markdown
## 📋 리팩토링 계획: {프로젝트명}

### Phase 1: 기반 정비 (Foundation)
**기간**: 1-2주
**목표**: Zero-Tolerance Critical 위반 해결

#### Step 1.1: Lombok 제거
**대상 파일**: {count}개
**작업 내용**:
1. Domain Layer ({count}개)
   - [ ] {파일명}: @Data → 수동 구현
   - [ ] {파일명}: @Builder → 정적 팩토리 메서드
2. Application Layer ({count}개)
   - [ ] ...
3. Persistence Layer ({count}개)
   - [ ] ...

**검증 방법**:
```bash
# Lombok 의존성 제거 확인
./gradlew dependencies | grep lombok
# 빌드 성공 확인
./gradlew build
```

#### Step 1.2: Long FK 전략 전환
**대상 파일**: {count}개
**작업 내용**:
1. Entity 수정
   - [ ] {Entity}: @ManyToOne → Long {field}Id
2. Repository 수정
   - [ ] {Repository}: JOIN 쿼리 → ID 기반 쿼리
3. Mapper 수정
   - [ ] {Mapper}: 관계 매핑 → ID 매핑

**검증 방법**:
```bash
# ArchUnit 테스트
./gradlew :adapter-out:persistence-mysql:test --tests "*ArchTest*"
```

---

### Phase 2: 아키텍처 정렬 (Architecture Alignment)
**기간**: 2-3주
**목표**: 헥사고날 아키텍처 준수

#### Step 2.1: Port 인터페이스 분리
...

#### Step 2.2: CQRS 분리
...

---

### Phase 3: 코드 품질 개선 (Code Quality)
**기간**: 1-2주
**목표**: 컨벤션 완전 준수

#### Step 3.1: DTO Record 전환
...

#### Step 3.2: Assembler/Mapper 추가
...

---

### Phase 4: 테스트 강화 (Test Enhancement)
**기간**: 1주
**목표**: ArchUnit 전체 통과

#### Step 4.1: ArchUnit 테스트 적용
...

#### Step 4.2: MockMvc → TestRestTemplate 전환
...
```

---

## 4️⃣ Serena Memory 저장 형식

```markdown
# Refactoring Plan: {프로젝트명}

## 메타 정보
- 생성일: {YYYY-MM-DD}
- 분석 범위: {full|domain|application|...}
- 분석자: Claude (refactoring-analyst)

## 요약
- 총 위반 항목: {count}개
- Critical: {count}개
- Important: {count}개
- Recommended: {count}개

## 위반 상세
### 🔴 Critical
| 유형 | 파일 수 | 주요 파일 |
|------|---------|----------|
| Lombok | 45 | User.java, Order.java, ... |
| Long FK | 12 | OrderEntity.java, ... |

### 🟡 Important
...

### 🟢 Recommended
...

## 리팩토링 계획
### Phase 1: 기반 정비
- 기간: 1-2주
- 목표: Zero-Tolerance 해결
- Steps: 1.1 Lombok 제거, 1.2 Long FK 전환

### Phase 2: 아키텍처 정렬
...

## 진행 상황
- [ ] Phase 1 완료
  - [ ] Step 1.1 완료
  - [ ] Step 1.2 완료
- [ ] Phase 2 완료
- [ ] Phase 3 완료
- [ ] Phase 4 완료

## 다음 액션
1. Phase 1, Step 1.1 시작: `/kb/domain/go` 실행
```

---

## 5️⃣ 실행 예시

### 전체 분석

```
User: /refactor-plan

Claude: 프로젝트 분석을 시작합니다...

## 🔍 분석 결과

### 🔴 Critical Violations (즉시 수정 필요)
| 유형 | 파일 수 | 주요 파일 |
|------|---------|----------|
| Lombok 사용 | 45개 | User.java, Order.java, ... |
| JPA 관계 어노테이션 | 12개 | OrderEntity.java, ... |
| Law of Demeter | 8개 | OrderService.java, ... |

### 🟡 Important Violations
| 유형 | 파일 수 |
|------|---------|
| CQRS 미분리 | 15개 |
| DTO 미분리 | 23개 |

## 📋 리팩토링 계획

### Phase 1: 기반 정비 (1-2주)
- Step 1.1: Lombok 제거 (45개 파일)
- Step 1.2: Long FK 전환 (12개 파일)

### Phase 2: 아키텍처 정렬 (2-3주)
...

계획을 Serena Memory에 저장했습니다: `refactor-plan-myproject`

Phase 1부터 시작할까요?
```

### 레이어별 분석

```
User: /refactor-plan domain

Claude: Domain Layer만 분석합니다...

## 🔍 Domain Layer 분석 결과

### 🔴 Critical
- Lombok: 12개 파일
- Law of Demeter: 5개 파일

### 구조 분석
- Aggregate: 3개 (Order, User, Product)
- VO: 8개
- Domain Event: 2개
- Domain Exception: 5개

...
```

---

## 6️⃣ 연계 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│              Refactoring Workflow                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  /refactor-plan                                              │
│       │                                                      │
│       │ 분석 + 계획 수립                                     │
│       ▼                                                      │
│  Serena Memory 저장 (refactor-plan-{project})               │
│       │                                                      │
│       │ 계획 승인                                            │
│       ▼                                                      │
│  Phase별 실행                                                │
│       │                                                      │
│       ├─ /kb/domain/go        (Domain 리팩토링)             │
│       ├─ /kb/application/go   (Application 리팩토링)        │
│       ├─ /kb/persistence/go   (Persistence 리팩토링)        │
│       └─ /kb/rest-api/go      (REST API 리팩토링)           │
│       │                                                      │
│       │ 각 Step 완료 시 Memory 업데이트                      │
│       ▼                                                      │
│  ArchUnit 테스트 실행                                        │
│       │                                                      │
│       │ ./gradlew test --tests "*ArchTest*"                 │
│       ▼                                                      │
│  완료 ✅                                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 7️⃣ 체크리스트 (Output Checklist)

### 분석 완료 체크

- [ ] 프로젝트 구조 파악 완료
- [ ] Zero-Tolerance 위반 전수 조사
- [ ] 위반별 파일 수 집계
- [ ] 영향도 매트릭스 작성
- [ ] 의존성 순서 결정

### 계획 수립 체크

- [ ] Phase 구조 결정
- [ ] Step별 대상 파일 목록
- [ ] 검증 방법 명시
- [ ] 예상 기간 산정
- [ ] Serena Memory 저장

### 품질 체크

- [ ] 계획이 실행 가능한 수준으로 구체적
- [ ] 우선순위가 명확
- [ ] 의존성 순서가 논리적
- [ ] 검증 방법이 자동화 가능

---

## 참조 문서

- **컨벤션 문서**: `docs/coding_convention/`
- **ArchUnit 테스트**: 각 모듈 `src/test/java/.../architecture/`
- **Zero-Tolerance 규칙**: `.claude/CLAUDE.md`
- **TDD 수정 커맨드**: `.claude/commands/kb/*/go.md`