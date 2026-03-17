---
name: markdown-templates
description: 정형화된 마크다운 문서 템플릿 사용 가이드
allowed-tools: Read, Write, Edit
---

# Markdown Templates

정형화된 마크다운 문서 생성을 위한 템플릿 모음입니다.

## 핵심 원칙

**정형 콘텐츠는 템플릿, 비정형 콘텐츠는 markdown-writer-agent**

---

## 템플릿 목록

| 템플릿 | 위치 | 용도 |
|--------|------|------|
| task-template.md | `.claude/templates/` | Task 파일 골격 |
| test-case-template.md | `.claude/templates/` | 테스트 케이스 골격 |
| agent-result-template.md | `.claude/templates/` | 에이전트 결과 형식 |
| step-status-template.md | `.claude/templates/` | Step 상태 형식 |

---

## 변수 치환 규칙

템플릿 내 변수는 `{{VARIABLE_NAME}}` 형식:

### 공통 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `{{TIMESTAMP}}` | ISO 형식 시간 | 2024-01-15T10:30:00 |
| `{{STATUS}}` | 상태 값 | pending, in_progress, completed |

### Task 템플릿 변수

| 변수 | 설명 |
|------|------|
| `{{TASK_ID}}` | Task 식별자 (TASK-001) |
| `{{TITLE}}` | Task 제목 |
| `{{CREATED_AT}}` | 생성 시간 |
| `{{UPDATED_AT}}` | 업데이트 시간 |
| `{{REQUEST_CONTENT}}` | 사용자 요청 원문 |
| `{{CODEBASE_SEARCH_RESULT}}` | codebase-search 결과 |
| `{{REFERENCE_RESULT}}` | reference-agent 결과 |
| `{{WEB_SEARCH_RESULT}}` | web-search 결과 |
| `{{STEPS_CONTENT}}` | Step 목록 |
| `{{AGENT_RESULTS}}` | 에이전트 결과들 |
| `{{TEST_RESULTS}}` | 테스트 결과들 |
| `{{USER_INTERACTIONS}}` | 사용자 상호작용 기록 |

### Test Case 템플릿 변수

| 변수 | 설명 |
|------|------|
| `{{TEST_ID}}` | 테스트 식별자 (TASK-001-T01) |
| `{{TEST_TITLE}}` | 테스트 제목 |
| `{{STEP_NUMBER}}` | 관련 Step 번호 |
| `{{IMPLEMENTATION_SUMMARY}}` | 구현 내용 요약 |
| `{{TEST_PURPOSE}}` | 테스트 목적 |
| `{{TEST_ENVIRONMENT}}` | 테스트 환경 |
| `{{TEST_ITEMS}}` | 테스트 항목 목록 |
| `{{RELATED_FILES}}` | 관련 파일 목록 |
| `{{NOTES}}` | 참고사항 |
| `{{TEST_RESULT_ROWS}}` | 결과 테이블 행 |
| `{{FINAL_RESULT}}` | 최종 결과 |
| `{{TEST_DATE}}` | 테스트 일시 |
| `{{TESTER}}` | 테스터 |

### Agent Result 템플릿 변수

| 변수 | 설명 |
|------|------|
| `{{AGENT_NAME}}` | 에이전트 이름 |
| `{{RESULT_DETAILS}}` | 결과 상세 내용 |
| `{{NEXT_ACTIONS}}` | 다음 작업 |

### Step Status 템플릿 변수

| 변수 | 설명 |
|------|------|
| `{{STEP_NUMBER}}` | Step 번호 |
| `{{STEP_TITLE}}` | Step 제목 |
| `{{STEP_STATUS}}` | Step 상태 |
| `{{ASSIGNED_AGENT}}` | 담당 에이전트 |
| `{{START_TIME}}` | 시작 시간 |
| `{{END_TIME}}` | 완료 시간 |
| `{{STEP_DESCRIPTION}}` | 작업 내용 |
| `{{STEP_RESULT}}` | 결과 |
| `{{MODIFIED_FILES}}` | 수정 파일 목록 |

---

## 사용 방법

### 1. 템플릿 읽기

```
Read 도구로 템플릿 파일 읽기:
.claude/templates/task-template.md
```

### 2. 변수 값 준비

```
TASK_ID = "TASK-001"
TITLE = "사용자 인증 구현"
STATUS = "pending"
CREATED_AT = "2024-01-15T10:30:00"
...
```

### 3. 변수 치환

템플릿 내용에서 `{{변수명}}`을 실제 값으로 교체

### 4. 파일 생성

```
Write 도구로 결과 파일 저장:
./tasks/TASK-001.md
```

---

## 동적 콘텐츠 처리

일부 변수는 동적 생성이 필요합니다:

### 정형 동적 콘텐츠 (직접 생성)
- `{{STEPS_CONTENT}}`: step-status-template 반복 적용
- `{{TEST_RESULT_ROWS}}`: 테이블 행 생성

### 비정형 동적 콘텐츠 (markdown-writer-agent 활용)
- `{{TEST_ITEMS}}`: 테스트 항목 상세 설명
- `{{NOTES}}`: 참고사항 설명
- `{{STEP_DESCRIPTION}}`: Step 작업 내용

---

## 워크플로우 예시

### Task 파일 생성

```
1. task-template.md 읽기
2. 기본 변수 치환 (TASK_ID, TITLE, STATUS 등)
3. 검색 결과 삽입 (CODEBASE_SEARCH_RESULT 등)
4. Steps 생성:
   - step-status-template.md 반복 적용
   - STEPS_CONTENT에 삽입
5. 최종 파일 생성
```

### Test Case 파일 생성

```
1. test-case-template.md 읽기
2. 기본 변수 치환 (TEST_ID, TASK_ID 등)
3. markdown-writer-agent spawn → TEST_ITEMS 생성
4. 결과 삽입
5. 최종 파일 생성
```

---

## 주의사항

1. **템플릿 우선**: 정형 콘텐츠는 항상 템플릿 사용
2. **변수 누락 확인**: 모든 `{{}}` 변수가 치환되었는지 확인
3. **비정형은 위임**: 복잡한 설명은 markdown-writer-agent 활용

---
<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->
