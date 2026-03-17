---
name: _workflow-implement
version: 2.1.0
description: Execution Groups 기반 병렬 구현 실행
user-invocable: false
---

# Workflow Implement Skill v2

> 🔴 **Complex 모드 전용** - `/workflow`에서 복잡도 🔴 선택 시 자동 호출됩니다.
>
> 🟢 Simple, 🟡 Medium 모드에서는 구현 로직만 참조합니다.

plan.md의 **Execution Groups**를 기반으로 **implementer 에이전트**를 병렬 호출하여 구현을 수행합니다.

## 핵심 변경 (v2)

| 항목 | v1 | v2 |
|------|----|----|
| 실행 단위 | 메인 세션에서 직접 | implementer 에이전트 |
| 컨텍스트 | 누적 (Compact 빈번) | 서브에이전트 종료 시 해제 |
| 병렬 실행 | Phase 단위 | Group 내 Task 병렬 |
| 진행 추적 | TODO 리스트 | progress.json |
| 실패 복구 | 전체 재시작 | 해당 Task만 재시도 |

## 전제 조건

- `.claude/work-docs/plan.md` 파일이 존재해야 함
- plan.md의 status가 `plan`이어야 함
- plan.md에 Execution Groups와 Task Details 섹션이 포함되어야 함

## 아키텍처

```
메인 세션 (오케스트레이션만)
    │
    ├─→ Task(implementer) Group 1 작업들 ⚡ 병렬
    │   완료 대기 + progress.json 업데이트
    │
    ├─→ Task(implementer) Group 2 작업들 ⚡ 병렬
    │   완료 대기 + progress.json 업데이트
    │
    └─→ Task(implementer) Group 3 작업들 ⚡ 병렬
        완료 대기 + progress.json 업데이트
```

## 실행 워크플로우

### Step 1: 문서 로드 및 재개 확인

#### 1-1. progress.json 확인

먼저 `.claude/work-docs/progress.json` 파일이 존재하는지 확인합니다.

**IF** progress.json이 존재하고 `status !== "completed"`:
→ Step 1-4 (재개 확인)로 이동

**ELSE**:
→ Step 1-2 (새로 시작)로 계속

#### 1-2. plan.md 읽기

```
.claude/work-docs/plan.md
```

**파싱 대상**:
- `Execution Groups` 섹션 → Group 목록 추출
- `Task Details` 섹션 → 각 Task 상세 정보 추출

#### 1-3. spec.md 읽기

```
.claude/work-docs/spec.md
```

요구사항 참조용으로 로드

#### 1-4. 재개 확인

progress.json이 존재하는 경우 재개 여부를 확인합니다.

```
📋 진행 중인 작업 발견

Issue: GRT-42
마지막 상태: Group 2, Task 2-A에서 중단
중단 시간: 2025-02-03 10:30

완료된 그룹:
  Group 1: ✅ 완료 (2/2 Tasks)
    - 1-A: XxxRequest, XxxResponse 타입 정의됨
    - 1-B: xxxApi 함수 export됨

남은 그룹:
  Group 2: ⏳ 1/1 Tasks 대기
  Group 3: ⏳ 2/2 Tasks 대기
  Group 4: ⏳ 1/1 Tasks 대기
```

→ AskUserQuestion 도구로 질문:

```typescript
AskUserQuestion({
  questions: [{
    question: "이어서 작업할까요?",
    header: "재개",
    options: [
      {
        label: "계속",
        description: "Group 2, Task 2-A부터 이어서 진행"
      },
      {
        label: "처음부터",
        description: "progress.json 삭제하고 Group 1부터 재시작"
      },
      {
        label: "취소",
        description: "작업 중단"
      }
    ],
    multiSelect: false
  }]
})
```

**IF** "계속" 선택:
→ progress.json의 currentGroup부터 Step 3으로 이동

**IF** "처음부터" 선택:
→ progress.json 삭제 후 Step 2로 이동

**IF** "취소" 선택:
→ 스킬 종료

### Step 2: progress.json 초기화

`.claude/work-docs/progress.json` 생성:

```json
{
  "issue": "GRT-XX",
  "status": "in_progress",
  "startedAt": "2025-02-03T10:00:00Z",
  "currentGroup": 1,
  "totalGroups": 3,
  "groups": {
    "1": {
      "status": "pending",
      "tasks": {
        "1-A": { "status": "pending", "files": [...], "output": null },
        "1-B": { "status": "pending", "files": [...], "output": null }
      }
    }
  }
}
```

→ **전체 스키마**: `references/progress-schema.md` 참조

### Step 3: 그룹별 순차 실행

각 그룹의 Task들을 병렬로 실행:

```
for each group in Execution Groups:
    1. 그룹 시작 표시
    2. 그룹 내 모든 Task 병렬 실행 (implementer 에이전트)
    3. 결과 수집 및 progress.json 업데이트
    4. 실패 시 메인 세션 복귀
    5. 그룹 완료 표시
```

#### 그룹 시작 표시

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶️ Group {N} 시작 ({M}개 Tasks) ⚡ 병렬 실행
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Task 병렬 실행

**중요**: 같은 Group 내 Task는 반드시 **단일 메시지에서 병렬 호출**

```typescript
// 단일 메시지에서 여러 Task 도구 호출
Task({ subagent_type: "implementer", ... }),  // 1-A
Task({ subagent_type: "implementer", ... })   // 1-B
```

→ **호출 패턴 상세**: `references/implementer-guide.md` 참조

#### 결과 수집 및 업데이트

implementer 출력에서 JSON 블록 추출 → progress.json 업데이트

```json
{
  "groups": {
    "1": {
      "status": "completed",
      "tasks": {
        "1-A": {
          "status": "completed",
          "output": { "summary": "...", "exports": [...], "notes": [...] },
          "verification": { "typecheck": "passed", "lint": "passed" }
        }
      }
    }
  }
}
```

→ **JSON 스키마**: `references/progress-schema.md` 참조

#### 실패 처리

**IF** Task 실패 (2회 재시도 후):

```
⚠️ Task 실패 - 메인 세션 복귀
Task: 1-A
오류: typecheck 실패

수정 완료 후 /workflow implement 재실행
```

1. progress.json에 실패 상태 저장
2. 사용자에게 보고
3. 스킬 종료 (메인 세션 복귀)

→ **에러 복구 상세**: `references/error-recovery.md` 참조

### Step 4: 이전 그룹 결과 전달

다음 Group 실행 시 이전 Group의 output을 수집하여 전달합니다.

```javascript
// progress.json에서 이전 그룹들의 output 수집
for (let i = 1; i < currentGroup; i++) {
  // 각 Task의 output.summary, output.notes 추출
}
```

수집한 결과를 마크다운으로 정리하여 implementer 프롬프트에 포함:

```markdown
## 이전 그룹 결과

Group 1 완료 (2/2 Tasks)
  Task 1-A: XxxRequest, XxxResponse 타입 정의됨
  Task 1-B: xxxApi 함수 export됨
```

→ **컨텍스트 구성 상세**: `references/implementer-guide.md` 참조

### Step 5: 전체 검증

모든 Group 완료 후:

#### 빌드 확인

```bash
npm run typecheck
npm run lint
```

#### spec.md 수락 기준 검증

```
✅ 수락 기준 검증

1. ✅ 6자리 입력 완료 시 자동으로 API 호출
2. ✅ 타이머가 0이 되면 재전송 버튼 활성화
3. ✅ 인증 성공 시 토큰 저장 + 메인 화면 이동
4. ✅ 에러 발생 시 적절한 피드백 표시
```

### Step 6: 자동 코드 리뷰

구현 완료 후 **reviewer** 에이전트가 자동으로 품질 검토를 수행합니다.

```typescript
Task({
  subagent_type: "reviewer",
  model: "opus",
  prompt: `## 리뷰 요청
${이슈번호} 구현 완료 자동 리뷰

## 변경 파일
${생성/수정된_파일_목록}

## spec 요약
${spec.md_핵심_요약}

## 중점 검토
- 타입 안전성
- 보안 취약점
- 프로젝트 컨벤션 준수`
})
```

#### 리뷰 결과 처리

**IF** 🔴 심각 이슈 발견:
→ 즉시 수정 후 다시 리뷰

**ELSE IF** 🟡 개선 권장 사항:
→ 사용자에게 보고, 수정 여부 확인

**ELSE** ✅ 양호:
→ 완료 처리 진행

### Step 7: 완료 처리

#### plan.md 상태 업데이트

```yaml
status: complete
```

#### progress.json 완료

```json
{
  "status": "completed",
  "completedAt": "2025-02-03T12:00:00Z"
}
```

→ **전체 스키마**: `references/progress-schema.md` 참조

#### 최종 완료 메시지

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 모든 작업 완료!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 구현 요약:
- Execution Groups: 3개
- 총 Tasks: 5개
- 신규 파일: 3개
- 수정 파일: 2개

📊 Group별 결과:
- Group 1: ✅ 2/2 Tasks
- Group 2: ✅ 1/1 Tasks
- Group 3: ✅ 2/2 Tasks

🧪 테스트 요약:
- TDD 작업: 1개
- 테스트 통과: 5/5

✅ 수락 기준: 4/4 통과
🔍 리뷰 결과: ✅ 양호

▶️ 다음 단계: /commit으로 커밋하기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**중요**: 완료 메시지 출력 후 **스킬을 종료**합니다.

## 진행 상황 표시

### 전체 진행률

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 전체 진행: [████████░░] 80%
   Group 1: ✅ 완료
   Group 2: ✅ 완료
   Group 3: 🔄 진행 중 (1/2)
   Group 4: ⏳ 대기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Task 진행

```
📝 [1-A] 타입 정의
   📁 src/models/xxx.swift
   🔄 implementer 실행 중...
```

## 중단 및 재개

### 중단 시 (Ctrl+C)

progress.json이 자동으로 현재 상태를 유지합니다.

### 재개 시

다시 `/workflow implement` 실행 시 Step 1-4 (재개 확인) 자동 진행:

```
📋 진행 중인 작업 발견
Issue: GRT-42
완료: Group 1
대기: Group 2, Group 3

이어서 작업할까요?
  1. 계속
  2. 처음부터
  3. 취소
```

→ **재개 시나리오 상세**: `references/error-recovery.md` 참조

## 참고 문서

| 문서 | 내용 |
|------|------|
| `references/progress-schema.md` | progress.json 전체 스키마 |
| `references/implementer-guide.md` | implementer 호출 패턴 및 컨텍스트 구성 |
| `references/error-recovery.md` | 에러 복구 및 재개 시나리오 |

## 주의사항

1. **병렬 호출 필수**: 같은 Group 내 Task는 단일 메시지에서 병렬 호출
2. **progress.json 동기화**: 각 Task 완료 시 즉시 업데이트
3. **실패 격리**: 한 Task 실패가 다른 Task에 영향 없음
