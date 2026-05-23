---
name: project-memory-check
description: 계획된 변경사항과 관련된 프로젝트 메모리(경계, 규약, 규칙)를 확인하고 위반 여부를 검사
allowed-tools: mcp__memory__read_graph, mcp__memory__search_nodes, mcp__memory__open_nodes, mcp__memory__create_entities, mcp__memory__add_observations
---

# 프로젝트 메모리 확인

## 역할
계획(Plan) 단계 완료 후, 구현 시작 전에 프로젝트 메모리를 확인하여:
1. 3단계 경계(Always/Ask/Never) 위반 여부 검사
2. 관련 규약/컴포넌트 정의 확인
3. 필요시 사용자 승인 요청

## 입력
analysisContext에서 수집:
- `projectId`: 프로젝트 식별자
- `changedFiles`: 변경 예정 파일 목록
- `taskType`: 작업 유형
- `plan`: 구현 계획 요약

## 프로젝트 ID 결정
1. `package.json`의 `name` 필드 확인
2. 없으면 프로젝트 루트 디렉토리 이름 사용
3. 없으면 Git remote origin에서 추출

## 엔티티 네이밍 규칙
```
[ProjectID]::[EntityType]::[Name]
```

예시:
- `my-webapp::Boundary::AlwaysDo`
- `my-webapp::Component::Button`
- `my-webapp::Convention::NamingRule`

## 워크플로우

### 1. 프로젝트 ID 확인
```bash
# 우선순위 1: package.json
cat package.json | jq -r '.name'

# 우선순위 2: 디렉토리 이름
basename $(pwd)

# 우선순위 3: git remote
git remote get-url origin | sed 's/.*\/\([^\/]*\)\.git/\1/'
```

### 2. 경계 엔티티 존재 확인
`search_nodes`로 `[ProjectID]::Boundary` 검색

**경계가 없는 경우 (첫 사용):**
1. 사용자에게 인터랙티브 초기화 제안
2. 기본 경계 템플릿 제시:

```yaml
AlwaysDo 기본값:
  - "커밋 전 lint/typecheck 실행"
  - "변경 파일 테스트 통과 확인"

AskFirst 기본값:
  - "새 의존성 추가"
  - "DB 스키마 변경"
  - "인증/권한 로직 수정"

NeverDo 기본값:
  - ".env* 파일 커밋"
  - "기존 테스트 삭제"
  - "시크릿 하드코딩"
```

3. 사용자 확인 후 `create_entities`로 생성

### 3. 3단계 경계 확인
1. `open_nodes`로 경계 엔티티 상세 조회:
   - `[ProjectID]::Boundary::AlwaysDo`
   - `[ProjectID]::Boundary::AskFirst`
   - `[ProjectID]::Boundary::NeverDo`

2. 현재 계획과 대조:

   **NeverDo 위반 검사** (즉시 중단):
   - 계획이 NeverDo의 observations에 해당하는지 확인
   - 위반 시: 즉시 중단, 사용자에게 알림, 계획 수정 요청

   **AskFirst 해당 검사** (승인 필요):
   - 계획이 AskFirst에 해당하는지 확인
   - 해당 시: 사용자 승인 요청

   **AlwaysDo 확인** (리마인더):
   - 계획에 AlwaysDo 항목이 누락되었는지 확인
   - 누락 시: 계획에 추가 권고

### 4. 관련 규약/규칙 검색
1. `changedFiles`에서 키워드 추출:
   - 파일 경로에서 컴포넌트명 추출
   - 도메인 영역 식별

2. `search_nodes`로 관련 엔티티 검색:
   - `[ProjectID]::Component::*`
   - `[ProjectID]::Convention::*`
   - `[ProjectID]::API::*`
   - `[ProjectID]::Domain::*`

3. 관련 규약이 있으면 요약 제공

### 5. 출력
```yaml
projectMemoryCheck:
  projectId: "my-webapp"
  boundaryStatus: "ok" | "violation" | "needs_approval" | "not_initialized"
  
  boundary:
    violations: []           # NeverDo 위반 (있으면 즉시 중단)
    needsApproval:           # AskFirst 해당 항목
      - item: "새 의존성 추가"
        reason: "axios 패키지 추가 예정"
    reminders:               # AlwaysDo 리마인더
      - "커밋 전 npm run lint 실행"
  
  relatedConventions:
    - entity: "[proj]::Component::Button"
      observations:
        - "variant prop 필수"
        - "onClick 핸들러 규칙"
    - entity: "[proj]::Convention::API"
      observations:
        - "에러 응답 형식 통일"
  
  action: "proceed" | "halt" | "ask_user"
  message: "..."
```

## 에러 처리

1. **Memory MCP 연결 실패**: 경고 후 계속 진행 (메모리 확인 건너뜀)
2. **경계 미설정**: 인터랙티브 초기화 진행
3. **NeverDo 위반**: 즉시 중단, `action: "halt"` 반환

## 계약
- 이 스킬은 계획 단계 후, 구현 시작 전에 실행
- NeverDo 위반 시 반드시 중단하고 사용자 확인 필요
- 경계가 없으면 인터랙티브 설정 진행
- 출력은 analysisContext.projectMemoryCheck에 병합
