---
name: code-review
description: Complete code review workflow for both requesting and receiving reviews. Use when creating PRs, reviewing code, or responding to feedback.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: obra/superpowers
  version: "2.0"
---

# Code Review

PR 요청부터 피드백 대응까지의 코드 리뷰 통합 스킬입니다.

## Part 1: Requesting Review

### PR 생성 전 체크리스트

- [ ] 테스트 통과 확인
- [ ] 린트 에러 없음
- [ ] 변경 범위 명확
- [ ] 커밋 메시지 규격 준수

### PR 설명 템플릿

```markdown
## What
[변경 사항 한 줄 요약]

## Why
[변경 이유]

## How
[구현 방법]

## Testing
- [ ] 단위 테스트 추가
- [ ] 수동 테스트 완료

## Screenshots (UI 변경 시)
[스크린샷]
```

---

## Part 2: Receiving Review

### 피드백 대응 원칙

| 피드백 유형 | 대응 |
|------------|------|
| 버그 지적 | 즉시 수정 |
| 스타일 제안 | 팀 컨벤션 확인 후 수정 |
| 설계 질문 | 의도 설명 또는 개선 |
| 의견 차이 | 논의 후 결정 |

### 대응 패턴

```markdown
# 수용 시
"좋은 지적이에요. 수정했습니다. [커밋 링크]"

# 설명 필요 시
"이렇게 한 이유는 [근거]입니다. 더 나은 방법이 있을까요?"

# 동의 안 할 때
"이해합니다만, [이유]로 현재 방식을 유지하고 싶습니다. 어떻게 생각하세요?"
```

---

## Best Practices

### 리뷰 요청자
- 변경을 작게 유지 (300줄 이하)
- 명확한 컨텍스트 제공
- 셀프 리뷰 먼저

### 리뷰어
- 건설적인 피드백
- 중요도 표시 (Must/Should/Could)
- 칭찬도 함께

## Checklist

- [ ] PR 설명 완성
- [ ] 테스트 통과
- [ ] 피드백 모두 대응
- [ ] 최종 승인 확인
