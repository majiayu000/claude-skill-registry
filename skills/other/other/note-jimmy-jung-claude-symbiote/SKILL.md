---
name: note
description: Compaction 내성 메모장. 중요한 컨텍스트, 결정 사항, 진행 상태를 작업별 state 폴더에 저장하여 컨텍스트 윈도우 초과나 세션 전환 시에도 정보가 보존됩니다. .gitignore로 관리되어 프로젝트를 오염시키지 않습니다. Use when you need to persist important context across compaction boundaries or session transitions.
---

# Note — Compaction 내성 메모장

중요한 컨텍스트를 작업별 state 폴더에 저장하여, 컨텍스트 윈도우 초과(compaction) 시에도 정보가 보존됩니다.
`.gitignore`로 git 추적에서 제외되어 프로젝트를 오염시키지 않습니다.

## 저장 경로

`.claude/project/state/{task-folder}/notepad.md`

task-folder 네이밍: `{ISO8601-basic}_{task-name}`
예시: `2026-02-13T1430_login-feature`

경로 결정 방법:
1. 현재 작업의 task-folder가 이미 존재하면 그 폴더 사용
2. 없으면 현재 시각과 작업명으로 task-folder 생성

## 특성

- `.gitignore`에 의해 git 추적 제외 (`.claude/project/state/`)
- 같은 세션 내에서 compaction 내성 보장
- 여러 작업이 task-folder로 격리됨
- `/clean` 커맨드로 완료된 작업 폴더 정리 가능

## 언제 사용하는가

- 복잡한 작업 중 핵심 결정 사항을 기록할 때
- Ralph Loop / Autopilot 반복 간 상태를 전달할 때
- 디버깅 중 발견한 단서를 누적할 때
- 사용자의 중요한 요구사항을 기록할 때
- 에이전트 간 정보를 전달할 때

## 저장 형식

```markdown
# Notepad

## 작업 컨텍스트
- 현재 작업: [설명]
- 목표: [설명]

## 핵심 결정
- [타임스탬프] [결정 내용]

## 발견 사항
- [타임스탬프] [발견 내용]

## 진행 상태
- [x] 완료된 항목
- [ ] 남은 항목

## 에이전트 메모
- [에이전트명] [메모 내용]
```

## 워크플로우

### 저장 (Write)
1. task-folder가 없으면 Shell tool로 생성: `mkdir -p .claude/project/state/{task-folder}`
2. `notepad.md`에 새 항목을 추가 (기존 내용 보존)
3. 타임스탬프를 포함하여 시간순 추적 가능

### 읽기 (Read)
1. 작업 시작 시 `.claude/project/state/{task-folder}/notepad.md` 존재 여부 확인
2. 존재하면 Read tool로 이전 컨텍스트 복원
3. 파일이 없으면 새로 시작
4. 현재 작업과 관련된 항목을 활용

### 정리 (Clean)
1. 작업 완료 시 `/clean` 커맨드로 task-folder 전체를 삭제
2. 또는 수동으로: `rm -rf .claude/project/state/{task-folder}`

## 자율 루프 연동

Ralph Loop / Autopilot의 각 iteration에서:
- iteration 시작: notepad.md 읽어 이전 상태 복원 (없으면 새로 생성)
- iteration 중: 발견 사항, 수정 내역 기록
- iteration 종료: 다음 iteration을 위한 상태 기록

## 원칙

- 간결하게 기록 (핵심만)
- 항상 추가 모드 (기존 내용 덮어쓰지 않음)
- 타임스탬프 포함
- 작업 완료 후 `/clean`으로 정리
- task-folder가 없어도 정상 동작 (graceful degradation)
