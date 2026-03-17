---
name: spawn-markdown-writer
description: 비정형 마크다운 작성을 markdown-writer-agent에 위임
allowed-tools: Task, Read
---

# Markdown Writer Agent 활용 가이드

비정형 마크다운 콘텐츠 생성을 markdown-writer-agent에 위임하는 방법입니다.

## 핵심 원칙

**정형 콘텐츠는 템플릿, 비정형 콘텐츠는 markdown-writer-agent**

---

## 판단 기준

### 템플릿 사용 (markdown-templates 스킬)

- Task 파일 골격
- 테스트 케이스 골격
- 에이전트 결과 형식
- Step 상태 형식
- 반복되는 고정 구조

### markdown-writer-agent 사용

- 테스트 항목 상세 설명
- 에러 분석 내용
- 사용자 안내 메시지
- 동적 콘텐츠 생성
- 요약문/설명문

---

## Spawn 방법

**반드시 Task tool을 사용합니다. Bash 명령어로 실행하지 마세요.**

### 기본 형식

```
Task tool 호출:
  subagent_type: "markdown-writer-agent"
  run_in_background: true
  prompt: |

콘텐츠 유형: {summary | description | guide | error_report | test_items}
컨텍스트: {작성에 필요한 정보}
길이 힌트: {short | medium | long}
형식: {plain | bullet_list | numbered_list | table | checklist}

.claude/agents/markdown-writer-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 테스트 항목 생성

```
Task tool 호출:
  subagent_type: "markdown-writer-agent"
  run_in_background: true
  prompt: |

콘텐츠 유형: test_items
컨텍스트: JWT 토큰 검증 테스트. 유효/만료/변조 케이스 포함.
길이 힌트: medium
형식: checklist

.claude/agents/markdown-writer-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 에러 분석 보고서

```
Task tool 호출:
  subagent_type: "markdown-writer-agent"
  run_in_background: true
  prompt: |

콘텐츠 유형: error_report
컨텍스트: TypeScript 빌드 에러. 순환 참조 감지. 파일: src/types/index.ts
길이 힌트: medium
형식: bullet_list

.claude/agents/markdown-writer-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

### 요약문 생성

```
Task tool 호출:
  subagent_type: "markdown-writer-agent"
  run_in_background: true
  prompt: |

콘텐츠 유형: summary
컨텍스트: {작업 완료 내용}
길이 힌트: short
형식: plain

.claude/agents/markdown-writer-agent.md 의 지시를 따르고,
작업 완료 후 결과만 요약해서 보고해줘."
```

---

## 결과 처리

### 성공 시

```markdown
## markdown-writer-agent 결과
- 상태: COMPLETED
- 콘텐츠 유형: test_items
- 길이: 320자

### 생성된 내용
[생성된 마크다운 콘텐츠]
```

**처리:**
1. `### 생성된 내용` 이후 텍스트 추출
2. 템플릿의 해당 변수 위치에 삽입
3. 최종 파일 생성

### 실패 시 (드문 경우)

호출 에이전트가 직접 간단한 내용 생성

---

## 워크플로우 통합

### test-case-agent 연동

```
1. test-case-agent: 테스트 케이스 구조 설계
2. markdown-templates 스킬로 test-case-template.md 읽기
3. 기본 변수 치환 (TEST_ID, TASK_ID 등)
4. markdown-writer-agent spawn → TEST_ITEMS 생성
5. 결과를 {{TEST_ITEMS}} 위치에 삽입
6. 최종 파일 Write
```

### task-manager-agent 연동

```
1. task-manager-agent: 액션 결정
2. markdown-templates 스킬로 템플릿 읽기
3. 기본 변수 치환
4. 동적 내용 필요시 markdown-writer-agent spawn
5. 결과 삽입
6. 파일 업데이트
```

### builder-agent 연동

```
빌드 에러 발생 시:
1. 에러 정보 수집
2. markdown-writer-agent spawn (error_report)
3. 결과를 LESSONS_LEARNED.md에 추가
```

---

## 콘텐츠 유형별 가이드

### summary
- 길이: short (1-3줄)
- 형식: plain
- 용도: 작업 완료 요약, 결과 한줄 요약

### description
- 길이: medium (1단락)
- 형식: plain 또는 bullet_list
- 용도: Step 설명, 기능 설명

### guide
- 길이: medium ~ long
- 형식: numbered_list 또는 bullet_list
- 용도: 사용자 안내, 설치 가이드

### error_report
- 길이: medium
- 형식: bullet_list
- 용도: 에러 분석, 해결책 제안

### test_items
- 길이: medium ~ long
- 형식: checklist
- 용도: 테스트 케이스 항목 생성

---

## 주의사항

1. **컨텍스트 충분히 제공**: 생성 품질에 직접 영향
2. **형식 명확히 지정**: 원하는 출력 형태 명시
3. **템플릿 우선 확인**: 정형이면 템플릿 사용
4. **결과 검증**: 생성된 내용이 적절한지 확인

---
<!-- SKILL-PROJECT-CONFIG-START -->
<!-- 프로젝트 특화 설정이 /orchestration-init에 의해 이 위치에 추가됩니다 -->
<!-- SKILL-PROJECT-CONFIG-END -->
