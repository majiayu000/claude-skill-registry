---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session. Dispatches fresh subagent for each task with code review between tasks.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Task
license: MIT
metadata:
  author: obra/superpowers
  version: "1.0"
---

# Subagent-Driven Development

구현 계획을 서브에이전트를 통해 실행하는 오케스트레이션 스킬입니다.

## When to Use

다음 조건을 모두 만족할 때:

```
✅ 완성된 구현 계획이 있음
✅ 대부분 독립적인 태스크들
✅ 현재 세션에서 진행해야 함
```

그렇지 않으면:
- 수동 실행
- 또는 parallel-session "executing-plans" 사용

## Execution Loop

각 태스크에 대해:

```
1. Implementer 서브에이전트 디스패치
   - 전체 태스크 텍스트와 컨텍스트 제공

2. 명확화 질문 답변
   - 구현 시작 전 모든 질문에 답변

3. Implementer 실행
   - 테스팅, 커밋, 셀프 리뷰

4. Spec Compliance Review
   - 원래 요구사항 대비 검증

5. Code Quality Review
   - 구현 표준 승인

6. 문제 발견 시 수정 루프
   - 같은 implementer가 수정하고 재제출

7. 완료 마킹 → 다음 태스크
```

## Review Flow

```
                    ┌─────────────────┐
                    │  Implementer    │
                    │  (서브에이전트) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Spec Compliance │◄──┐
                    │     Review      │   │ 실패 시
                    └────────┬────────┘   │ 수정 요청
                             │            │
                    통과     ▼            │
                    ┌─────────────────┐   │
                    │  Code Quality   │───┘
                    │     Review      │
                    └────────┬────────┘
                             │
                    통과     ▼
                    ┌─────────────────┐
                    │    Complete     │
                    └─────────────────┘
```

## Red Flags

```
❌ 리뷰 단계 건너뛰기
❌ 미수정 이슈가 있는데 진행
❌ Spec 리뷰 전에 Code Quality 리뷰 시작
❌ 서브에이전트 질문에 불완전한 답변
```

## Task Dispatch Template

```markdown
## Task
[태스크 설명]

## Context
- 관련 파일: [파일 목록]
- 의존성: [선행 태스크]
- 제약: [제약 조건]

## Acceptance Criteria
- [ ] [기준 1]
- [ ] [기준 2]

## Test Requirements
- 필요한 테스트 케이스
```

## Review Templates

### Spec Compliance Review

```markdown
## Requirement Checklist
- [ ] 기능 요구사항 충족
- [ ] 엣지 케이스 처리
- [ ] 에러 핸들링
- [ ] 성능 요구사항

## Verdict
✅ PASS / ❌ NEEDS_REVISION

## Issues (있을 경우)
- [이슈 설명]
```

### Code Quality Review

```markdown
## Quality Checklist
- [ ] 코드 스타일 준수
- [ ] 테스트 커버리지
- [ ] 명명 규칙
- [ ] 문서화

## Verdict
✅ PASS / ❌ NEEDS_REVISION

## Suggestions
- [개선 제안]
```

## Final Review

모든 태스크 완료 후:

```
1. 전체 변경사항 리뷰
2. 통합 테스트 실행
3. 문서 업데이트 확인
4. 머지 준비 완료 확인
```
