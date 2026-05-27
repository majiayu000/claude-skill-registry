---
name: claude-config-reviewer
description: |
  .claude/ 디렉토리 설정 파일 검토 스킬. 에이전트/스킬/훅의 구조, frontmatter, description 패턴 검증.
  사용 시기: (1) 새 에이전트/스킬/훅 생성 후 (2) 기존 설정 수정 후 (3) .claude/ 전체 리뷰 시 (4) /review-config 호출 시 (project)
---

# Claude Config Reviewer

`.claude/` 디렉토리의 에이전트, 스킬, 훅 파일이 가이드라인에 맞게 작성되었는지 검토합니다.

## Quick Start

```
# 특정 파일 검토
/review-config .claude/agents/my-agent.md

# 전체 .claude/ 검토
/review-config
```

## 검토 워크플로우

1. 대상 파일 읽기
2. 파일 유형 판별 (Agent/Skill/Hook)
3. 해당 체크리스트로 검증
4. 검토 결과 리포트 생성

## 검토 대상별 요약

### Agent (.claude/agents/*.md)

필수 검증 항목:
- Frontmatter: `name`, `description`, `tools`, `model`
- Description: "Use PROACTIVELY" 포함
- 본문: "You are a...", "When invoked:", "Guidelines:"
- 간결성: 30줄 이하 권장

상세: [references/agent-checklist.md](references/agent-checklist.md)

### Skill (.claude/skills/*/SKILL.md)

필수 검증 항목:
- Frontmatter: `name`, `description`
- Description: "사용 시기: (1)...(2)..." 패턴
- 디렉토리: SKILL.md 필수, references/ 권장
- 간결성: 500줄 이하

상세: [references/skill-checklist.md](references/skill-checklist.md)

### Hook (.claude/hooks/*.py, settings.json)

필수 검증 항목:
- 이벤트 선택 적절성
- Matcher 패턴 정확성
- Non-blocking (exit 0)

상세: [references/hook-checklist.md](references/hook-checklist.md)

## 결과 리포트 형식

```markdown
# .claude/ 설정 검토 결과

## 검토 대상
- 파일: {file_path}
- 유형: {Agent|Skill|Hook}

## 검토 결과

### 통과 항목
- [x] {항목1}
- [x] {항목2}

### 개선 필요
- [ ] {항목}: {구체적 문제점과 개선 방안}

## 종합 평가
{전체 평가 및 권장 사항}
```
