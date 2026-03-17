---
name: create-agent
description: |
  Claude Code 커스텀 에이전트를 만들고 실행할 때 사용하는 스킬.
  사용자가 "에이전트 만들어", "Claude agent 생성", "--agents 설정"을 요청하면 활성화됩니다.
argument-hint: "[agent-name] [agent-description]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# Claude Code 에이전트 생성/실행 가이드

요청: $ARGUMENTS

이 스킬은 **Claude CLI에서 확인한 실제 방식**만 사용한다.

- 에이전트 정의 주입: `--agents <json>`
- 실행 에이전트 선택: `--agent <name>`

## 1) 생성 규칙

1. 에이전트 이름은 `lowercase-hyphen` 형식으로 만든다.
2. 에이전트 정의는 JSON 객체로 작성한다.
3. 각 엔트리는 아래 키를 사용한다.
   - `description`: 언제 쓰는지 한 줄 설명
   - `prompt`: 에이전트 시스템 지시문

예시:

```json
{
  "issue-infer-extract-symptom": {
    "description": "증상 텍스트를 추출하는 에이전트",
    "prompt": "너는 증상 추출 전문가다. ..."
  }
}
```

## 2) 저장 위치

프로젝트 기준 아래 경로를 기본으로 사용한다.

- `.claude/agents/agents.json`
- 필요 시 에이전트별 원문 프롬프트 문서: `.claude/agents/<agent-name>.md`

## 3) 실행 방법

### 단발 실행

```bash
claude -p \
  --agents "$(cat .claude/agents/agents.json)" \
  --agent <agent-name> \
  "<실행 프롬프트>"
```

### 대화형 시작

```bash
claude --agents "$(cat .claude/agents/agents.json)"
```

필요하면 시작 시 바로 선택:

```bash
claude --agents "$(cat .claude/agents/agents.json)" --agent <agent-name>
```

## 4) 변환(마이그레이션) 작업 지침

OpenCode/기타 형식에서 변환 요청을 받으면 아래 순서로 처리한다.

1. 원본 frontmatter의 `name`, `description`을 우선 보존한다.
2. 본문 지시문은 `prompt`로 이동한다.
3. OpenCode 전용 필드(`mode`, `tools` 등)는 Claude JSON에 직접 넣지 않는다.
4. 결과를 `.claude/agents/agents.json`에 합친다.
5. 최소 1개 에이전트는 `claude -p --agents ... --agent ...`로 실행 검증한다.

## 5) 완료 보고 형식

작업 완료 시 아래를 반드시 보고한다.

- 생성/수정 파일 목록
- 사용한 실행 명령
- 검증 결과(성공/실패 + 핵심 로그)
- 다음 액션(필요 시)
