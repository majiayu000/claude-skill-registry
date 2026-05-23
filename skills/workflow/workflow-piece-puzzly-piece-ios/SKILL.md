---
name: workflow
version: 3.0.0
description: 복잡도 기반 적응형 워크플로우 관리
user-invocable: true
---

# /workflow 스킬 v3

복잡도에 맞는 프로세스를 자동 선택하고, Memory 시스템으로 세션 간 컨텍스트를 유지하는 통합 워크플로우입니다.

## 핵심 철학

```
1. 복잡도에 맞는 프로세스 (Right-sized process)
2. 문서보다 메모리 (Memory over documents)
3. 학습하는 시스템 (Learning system)
```

## 사용법

```
/workflow              # 진행 중인 작업 확인 또는 새 작업 시작
/workflow <설명>       # 새 작업 시작 (설명 기반 복잡도 판단)
/workflow spec         # _workflow-spec 직접 호출 (스펙 정의)
/workflow plan         # _workflow-plan 직접 호출 (계획 작성)
/workflow implement    # _workflow-implement 직접 호출 (구현)
```

---

## 서브커맨드 처리

**Step 0: 서브커맨드 파싱**

인자가 `spec`, `plan`, `implement` 중 하나인 경우 해당 재사용 스킬을 직접 호출합니다.

| 서브커맨드 | 호출 스킬 | 용도 |
|-----------|----------|------|
| `spec` | `_workflow-spec` | 스펙 정의만 진행 |
| `plan` | `_workflow-plan` | 계획 작성만 진행 |
| `implement` | `_workflow-implement` | 구현만 진행 |

**IF** 인자가 서브커맨드인 경우:
→ 해당 스킬 참조하여 실행 후 종료

**ELSE**:
→ Step 1부터 정상 워크플로우 진행

---

## 실행 워크플로우

### Step 1: Memory 로드 및 Failures 경고

`.claude/memory/` 에서 세션 컨텍스트와 학습 패턴을 로드합니다.

```
📂 Memory 로드 중...
├── session.json   → 진행 중인 작업 확인
├── instincts.json → 학습된 패턴 로드
└── failures.json  → 실패 기록 확인
```

#### 1.1 Failures 경고 체크

작업 설명의 키워드를 failures.json과 매칭하여 이전 실패 경고를 표시합니다.

**매칭 로직**:
```
1. 작업 설명에서 키워드 추출 (컴포넌트명, 기능명 등)
2. failures.json의 category, issue, keywords 필드와 매칭
3. 관련 실패 기록이 있으면 경고 표시
```

**경고 표시 예시**:
```
⚠️ 이전 실패 기록 발견

📋 관련 이슈:
• [swiftui-lifecycle] Task cancellation 누락 (2회)
  → async 작업 시 Task 저장 후 cancel 필수

이 패턴들을 주의하며 작업하세요.
```

**3회 이상 반복 시 승격 제안**:

→ AskUserQuestion 도구로 질문:

```typescript
AskUserQuestion({
  questions: [{
    question: "이 패턴을 instincts로 승격할까요?",
    header: "승격",
    options: [
      { label: "승격", description: "instincts.json에 추가하여 영구 저장" },
      { label: "나중에", description: "이번에는 건너뛰기" }
    ],
    multiSelect: false
  }]
})
```

승격 선택 시:
1. instincts.json에 새 패턴 추가
2. failures.json에서 해당 항목의 `promoted: true` 표시

---

**session.json에 current가 있는 경우**:
→ Step 2-A (진행 중인 작업 처리)

**current가 없는 경우**:
→ Step 2-B (새 작업 시작)

---

### Step 2-A: 진행 중인 작업 처리

진행 중인 작업이 있으면 상태를 표시하고 선택지를 제시합니다:

```
📋 진행 중인 작업 발견

🎯 작업: {제목}
📍 상태: {phase}
🕐 마지막: {lastTask}
📅 업데이트: {lastUpdated}
```

→ AskUserQuestion 도구로 질문:

```typescript
AskUserQuestion({
  questions: [{
    question: "어떻게 진행할까요?",
    header: "작업",
    options: [
      { label: "이어하기", description: "마지막 작업 지점부터 계속" },
      { label: "새 작업", description: "현재 작업 보류, 새 작업 시작" },
      { label: "완료 처리", description: "현재 작업을 완료로 표시" }
    ],
    multiSelect: false
  }]
})
```

**이어하기 선택 시**:
1. 관련 instincts 표시
2. 마지막 컨텍스트 복원
3. 해당 단계 계속 진행

---

### Step 2-B: 새 작업 시작

#### 2-B-1. 브랜치 확인

```bash
git branch --show-current
```

- `feat/*`, `fix/*` → 브랜치명에서 작업 설명 추출
- `main`, `develop` → 사용자에게 작업 설명 입력받기

#### 2-B-2. 작업 설명 수집

사용자가 `/workflow <설명>`으로 설명을 제공했거나, 추가 설명을 대기:

```
📝 새 작업을 시작합니다.

무엇을 구현하려고 하시나요?
(설명, Figma 링크, API 스펙 등을 자유롭게 알려주세요)
```

#### 2-B-3. 복잡도 자동 판단

사용자 설명을 바탕으로 복잡도를 추정합니다:

| 신호 | 복잡도 |
|------|--------|
| "수정", "변경", "버그", 1-2개 파일 언급 | 🟢 Simple |
| "추가", "연동", 3-5개 파일 예상 | 🟡 Medium |
| "새 화면", "새 기능", Figma 링크, 복잡한 요구사항 | 🔴 Complex |

→ AskUserQuestion 도구로 질문:

```typescript
AskUserQuestion({
  questions: [{
    question: "복잡도가 맞나요?",
    header: "복잡도",
    options: [
      { label: "🟢 Simple", description: "1-2 파일, 바로 구현" },
      { label: "🟡 Medium", description: "3-5 파일, 간단 플랜 후 구현" },
      { label: "🔴 Complex", description: "5+ 파일, 전체 워크플로우" }
    ],
    multiSelect: false
  }]
})
```

---

### Step 3: 복잡도별 실행

#### 🟢 Simple (Quick)

**프로세스**: 바로 구현

```
🟢 Simple 모드

📌 작업: {작업 설명}
💡 관련 패턴: {instincts에서 로드}

바로 구현을 시작합니다.
```

1. 관련 instincts 표시
2. 바로 구현 시작
3. 완료 시 Memory 업데이트

**문서 생성**: 없음 (Memory만 사용)

---

#### 🟡 Medium (Standard)

**프로세스**: 간단 플랜 → 구현

```
🟡 Medium 모드

📌 작업: {작업 설명}
💡 관련 패턴: {instincts에서 로드}

간단한 플랜을 세우고 구현합니다.
```

1. **간단 플랜** (구두 또는 짧은 목록)
   - 수정할 파일 목록
   - 작업 순서
   - 주의사항

2. **구현**
   - 플랜에 따라 순차 진행
   - TDD 필요 시 적용

3. **Memory 업데이트**

**문서 생성**: 아래 조건 중 하나 이상 해당 시 plan.md 권장
- 파일 4개 이상
- 2+ 도메인 수정
- 외부 의존성 (API, Figma)
- TDD 대상 포함

---

#### 🔴 Complex (Full)

**프로세스**: spec → plan → implement

```
🔴 Complex 모드

📌 작업: {작업 설명}
💡 관련 패턴: {instincts에서 로드}

전체 워크플로우를 진행합니다.
```

1. **Spec 작성** (`_workflow-spec` 참조)
   - 요구사항 구체화
   - Figma/Swagger 연동
   - UI/API 스펙 정리

2. **Plan 작성** (`_workflow-plan` 참조)
   - 코드베이스 분석
   - 작업 계획 수립
   - Phase 그룹화

3. **Implement** (`_workflow-implement` 참조)
   - Phase별 순차 실행
   - TDD 적용
   - 검증

**문서 생성**: `.claude/work-docs/`
- spec.md
- plan.md

---

### Step 4: Memory 업데이트

#### 작업 시작 시

```json
// session.json
{
  "current": {
    "feature": "signup-nudge",
    "branch": "feat/signup-nudge",
    "level": "medium",
    "description": "회원가입 유도 화면 구현",
    "startedAt": "2025-01-30T01:00:00Z",
    "lastUpdated": "2025-01-30T01:00:00Z",
    "context": {
      "phase": null,
      "lastTask": null,
      "notes": []
    }
  }
}
```

#### 작업 중

중요한 진행 상황이나 결정 사항을 `context.notes`에 추가:

```json
{
  "context": {
    "phase": "implement",
    "lastTask": "useVerifyPhone 훅 구현",
    "notes": [
      "API 응답 형식이 spec과 다름 - 백엔드 확인 필요",
      "기존 useCountdown 훅 재사용"
    ]
  }
}
```

#### 작업 완료 시

```json
{
  "current": null,
  "history": [
    {
      "feature": "signup-nudge",
      "level": "medium",
      "completedAt": "2025-01-30T03:00:00Z",
      "duration": "2시간",
      "filesChanged": 5
    }
  ]
}
```

---

### Step 5: Instincts 학습

작업 중 다음 상황에서 새로운 instinct를 제안합니다:

#### 학습 트리거

| 트리거 | 예시 |
|--------|------|
| 사용자 수정 | Claude 작성 → 사용자가 수정 |
| 반복 패턴 | 같은 코드 패턴 3회 이상 |
| 에러 해결 | 특정 에러 → 해결 방법 |

#### 학습 제안

```
💡 새로운 패턴 학습

발견: API 호출 시 항상 try-catch로 감싸고 있습니다.

- trigger: "API 호출 시"
- action: "try-catch로 감싸고 에러 상태 관리"
```

→ AskUserQuestion 도구로 질문:

```typescript
AskUserQuestion({
  questions: [{
    question: "이 패턴을 instinct로 저장할까요?",
    header: "학습",
    options: [
      { label: "저장", description: "instincts.json에 그대로 저장" },
      { label: "수정 후 저장", description: "trigger/action을 수정한 뒤 저장" },
      { label: "무시", description: "저장하지 않음" }
    ],
    multiSelect: false
  }]
})
```

---

## 상태 표시

### 워크플로우 시작 시

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Workflow v3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 작업: 회원가입 유도 화면
📊 복잡도: 🟡 Medium
🌿 브랜치: feat/signup-nudge

💡 관련 패턴:
  • API 호출 시 → try-catch로 감싸기

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 작업 완료 시

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 작업 완료!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 요약:
  • 파일 변경: 5개
  • 소요 시간: 2시간
  • 복잡도: 🟡 Medium

💾 Memory 업데이트:
  • session.json → history에 기록
  • instincts.json → 새 패턴 1개 추가

▶️ 다음: /commit으로 커밋하기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Memory 파일 위치

```
.claude/memory/
├── instincts.json   # ❌ git 제외 - 개인 학습 패턴
├── session.json     # ❌ git 제외 - 개인 세션 컨텍스트
└── failures.json    # ❌ git 제외 - 개인 실패 기록
```

---

## 재사용 스킬과의 관계

| 재사용 스킬 | 역할 | 호출 방법 |
|------------|------|----------|
| `_workflow-spec` | 스펙 정의 | `/workflow spec` 또는 🔴 Complex 내부 호출 |
| `_workflow-plan` | 계획 작성 | `/workflow plan` 또는 🔴 Complex 내부 호출 |
| `_workflow-implement` | 구현 | `/workflow implement` 또는 모든 모드에서 재사용 |

---

## 주의사항

1. **복잡도는 사용자가 최종 결정**: 자동 판단은 제안일 뿐
2. **Memory 파일 직접 수정 가능**: 사용자가 수동으로 편집해도 됨
3. **문서 생성은 필요시만**: Simple/Medium에서는 문서 없이 진행 가능
4. **학습은 제안 후 승인**: 자동 저장하지 않음, 사용자 확인 필요
