---
name: create-ai-tool
description: >
  AI 도구 유형(Skill/Agent)을 결정하고 생성을 안내합니다.
  도구 유형 선택, 스킬 vs 에이전트, 어떤 걸 만들어야 할지 요청 시 활성화.
---

# AI Tool Creator

사용자 요구사항을 분석하여 적절한 유형(Skill/Agent)을 결정하고 생성을 안내합니다.

## 유형 결정 질문

| 질문 | YES | NO |
|------|-----|-----|
| 컨텍스트 격리 필요? | Agent | Skill |
| 도구 제한 필요? | Agent | Skill |
| 대량 출력/병렬 처리? | Agent | Skill |

## 빠른 의사결정 트리

```
[요청 분석]
    │
    ├─ 컨텍스트 격리 필요? ─────────────────┐
    │   (대량 출력, 병렬 처리, 도구 제한)     │
    │                                  ↓
    │                                 Agent
    │
    └─ 그 외 모든 경우 ──────────────────→ Skill
```

## 다음 단계

유형이 결정되면:

- **Skill 생성** → `/create-skill` 또는 [create-skill](../create-skill/SKILL.md)
- **Agent 생성** → `/create-agent` 또는 [create-agent](../create-agent/SKILL.md)

## 핵심 차이

| 구분 | Skill | Agent |
|------|-------|-------|
| 컨텍스트 | 메인 대화 공유 | 별도 격리 |
| 목적 | 지식/지침 추가 | 태스크 위임 |
| 호출 | `/skill-name` | Claude 자동 위임 |
| 도구 제어 | `allowed-tools` | `tools`, `disallowedTools` |

## 사용 사례별 선택

| 사용 사례 | 유형 | 핵심 설정 |
|----------|------|----------|
| 코딩 컨벤션, 스타일 가이드 | Skill | `user-invocable: false` |
| 단계별 작업 지침 | Skill | 기본값 |
| 배포, DB 작업 (부작용) | Skill | `disable-model-invocation: true` |
| 코드 리뷰, 디버깅 (격리) | Agent | `tools`, `disallowedTools` |
| 병렬 리서치 | Agent | `tools` |

## 상세 의사결정

복잡한 판단이 필요하면:
- [의사결정 트리](references/decision-tree.md) - 상세 판단 기준
