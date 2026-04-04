---
name: spawn-search-agents
description: 정보 수집이 필요할 때 검색 에이전트 활용 가이드. 코드 탐색, 레퍼런스, 웹검색
allowed-tools: Task, Read, Glob, Grep
---

# 검색 에이전트 활용 가이드

정보 수집이 필요할 때 적절한 검색 에이전트를 선택하고 활용하는 방법입니다.

## 언제 사용하나?

- 코드 구조 파악이 필요할 때
- 기존 패턴/컨벤션 확인이 필요할 때
- 외부 라이브러리 문서가 필요할 때
- 유사 구현 예제가 필요할 때

## 중요: /orchestrate는 직접 검색 금지

**/orchestrate 커맨드는 Glob, Grep, Search를 직접 사용하면 안 됩니다.**
반드시 아래 검색 에이전트를 Task tool로 spawn해야 합니다.

### 절대 금지: Bash로 claude 명령어 실행

- ❌ `claude --agent {agent-name}` 사용 금지
- ❌ `claude task --subagent {agent-name}` 사용 금지
- ❌ Bash tool로 claude CLI 실행 금지

**반드시 Task tool (function call)을 사용하세요.**

## 에이전트별 역할

| 에이전트 | 용도 | 모델 |
|---------|------|------|
| codebase-search-agent | 프로젝트 내 코드 탐색 | Sonnet |
| reference-agent | 예제/템플릿 코드 탐색 | Haiku |
| web-search-agent | 외부 문서/API 레퍼런스 | Haiku |

**중요: 반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

### codebase-search-agent

**용도:**
- 관련 파일, 함수, 클래스 찾기
- 의존성 관계 분석
- 기존 코드 패턴 파악
- 코드 컨벤션 확인

**Spawn 예시:**
```
Task tool 호출:
  subagent_type: "codebase-search-agent"
  run_in_background: true
  prompt: |
    사용자 인증 관련 코드를 찾아줘. 로그인, 세션, 토큰 관련 파일과 함수를 파악해줘.
    .claude/agents/codebase-search-agent.md 의 지시를 따르고,
    작업 완료 후 결과만 요약해서 보고해줘.
```

### reference-agent

**용도:**
- 프로젝트 내 예제 코드 찾기
- 템플릿 파일 탐색
- 유사 구현 사례 발굴

**Spawn 예시:**
```
Task tool 호출:
  subagent_type: "reference-agent"
  run_in_background: true
  prompt: |
    API 엔드포인트 구현 예제를 찾아줘. examples/, samples/ 폴더와 README를 확인해줘.
    .claude/agents/reference-agent.md 의 지시를 따르고,
    작업 완료 후 결과만 요약해서 보고해줘.
```

### web-search-agent

**용도:**
- 공식 문서 검색
- API 레퍼런스 조회
- 베스트 프랙티스 검색
- 에러 해결책 검색

**Spawn 예시:**
```
Task tool 호출:
  subagent_type: "web-search-agent"
  run_in_background: true
  prompt: |
    React 18의 useEffect 변경사항에 대해 검색해줘. 공식 문서 위주로 찾아줘.
    .claude/agents/web-search-agent.md 의 지시를 따르고,
    작업 완료 후 결과만 요약해서 보고해줘.
```

## 병렬 Spawn 패턴

시간 단축을 위해 **동시에** Task tool 호출 (단일 메시지에 여러 호출):

```
Task tool #1:
  subagent_type: "codebase-search-agent"
  run_in_background: true
  prompt: "프로젝트 내 관련 코드 탐색..."

Task tool #2:
  subagent_type: "reference-agent"
  run_in_background: true
  prompt: "예제/템플릿 탐색..."

Task tool #3 (필요시):
  subagent_type: "web-search-agent"
  run_in_background: true
  prompt: "외부 문서 검색..."
```

## 결과 활용

### 정보 수집 완료 후

1. 각 에이전트 결과 취합
2. todo-list-agent로 작업 분해
3. task 파일 생성
4. coder-agent에 정보 전달

### 결과가 불충분할 때

- 키워드 변경하여 재탐색
- 다른 에이전트 추가 spawn
- 사용자에게 추가 정보 요청

## 주의사항

- 검색 에이전트는 **정보 수집만** 담당
- 코드 작성/수정은 coder-agent에게 위임
- 결과는 500자 이내 요약으로 받음

---
<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->
