---
name: doctor
description: .claude 설정의 자기 진단 도구. 에이전트/스킬 파일 존재, Hook 실행 권한, 깨진 경로 참조, 사용 추적 상태, 교차 참조 정합성을 자동으로 검사하고 수정을 제안합니다. Use when diagnosing configuration issues, after setup, or when something isn't working correctly.
---

# Doctor — 자기 진단

.claude 설정의 건강 상태를 자동으로 검사하고 수정을 제안합니다.

## 진단 항목

### 1. 프로젝트 설정 (Project Setup)
- [ ] `.claude/project/.initialized` 마커 파일 존재 여부
- [ ] `.claude/rules/` 내 프로젝트 컨텍스트 규칙 존재 여부
- [ ] VERSION 파일 존재 여부

### 2. 에이전트 (Agents)
- [ ] `.claude/agents/` 디렉터리의 모든 .md 파일이 유효한 YAML frontmatter를 가짐
- [ ] 필수 필드 확인: name, description
- [ ] model 값이 유효한가 (sonnet, opus, haiku, inherit)
- [ ] description이 구체적인가
- [ ] 커스텀 에이전트 16개 존재: analyst, architect, build-fixer, critic, debugger, designer, doc-writer, implementer, migrator, planner, qa-tester, researcher, reviewer, security-reviewer, tdd-guide, vision

### 3. 스킬 (Skills)
- [ ] 각 `.claude/skills/{name}/SKILL.md` 파일 존재
- [ ] 폴더명과 frontmatter name 일치
- [ ] description에 "Use when" 패턴 포함
- [ ] 참조하는 파일 경로가 실제 존재하는지 확인

### 4. 커맨드 (Commands)
- [ ] `.claude/commands/` 디렉터리의 .md 파일에 YAML frontmatter가 없는지 확인
- [ ] 워크플로우 단계가 명확한가

### 5. Hook (Hooks)
- [ ] settings.json의 hooks 섹션이 유효한가
- [ ] 이벤트 이름이 유효한가 (SessionStart, PreToolUse, PostToolUse, AfterFileEdit 등)
- [ ] 참조하는 스크립트 파일이 존재하는가
- [ ] 스크립트에 실행 권한이 있는가 (chmod +x)
- [ ] matcher 값이 PascalCase인가

### 6. 경로 참조 무결성
- [ ] 에이전트/스킬에서 참조하는 파일 경로가 모두 존재
- [ ] 프로젝트 컨텍스트에서 참조하는 룰/스킬이 모두 존재

### 7. 사용 추적 시스템 (Usage Tracking)
- [ ] usage-tracker.sh 훅 파일 존재 및 실행 권한
- [ ] settings.json에 usage-tracker.sh가 PostToolUse(Read)와 SubagentStart로 등록되어 있는가
- [ ] usage-data 디렉터리 구조 (skills, commands, agents, subagents 하위 디렉터리)
- [ ] .tracked-since 파일 존재 (추적 활성 상태인지)
- [ ] 고아 데이터 감지 (삭제된 스킬/커맨드/에이전트의 카운터가 남아있는지)
- [ ] 데이터 파일 형식 유효성 ({count}|{timestamp})

### 8. 교차 참조 정합성 (Cross-Reference)
- [ ] CLAUDE.md에서 참조하는 스킬이 실제 존재하는가
- [ ] CLAUDE.md에서 참조하는 에이전트가 실제 존재하는가
- [ ] rules/synapse-delegation.md의 에이전트 참조가 유효한가
- [ ] README.md/QUICK-START.md의 개수 표기가 실제와 일치하는가

### 9. Source 태그 정합성 (Origin/Custom)
- [ ] origin 번들 파일에 source 태그가 있는가
  - 커맨드: 파일 최상단에 `<!-- source: origin -->`
  - 훅: shebang 다음 줄에 `# source: origin`
- [ ] source 태그가 없는 파일이 custom으로 올바르게 분류되는가

### 10. 파일 크기 및 품질
- [ ] 500줄 초과 룰 파일 감지
- [ ] 빈 SKILL.md 또는 빈 커맨드 파일 감지
- [ ] 중복 에이전트/스킬 이름 감지

## 워크플로우

### Step 0: 자동 검증 스크립트 실행
먼저 `scripts/validate.sh`를 Shell tool로 실행하여 자동화된 구조 검증을 수행합니다.

```bash
bash .claude/skills/doctor/scripts/validate.sh
```

이 스크립트가 검증하는 항목:
- settings.json hooks 구조 (이벤트 이름, 스크립트 존재/권한)
- 에이전트 frontmatter (name, description 필수 필드)
- 스킬 frontmatter (name, description, 폴더명 일치)
- 커맨드 형식 (YAML frontmatter 없음 확인)
- 경로 참조 무결성
- source 태그 정합성 (origin 번들 파일의 태그 존재 여부)
- 사용 추적 시스템 건강 상태 (훅 등록, 디렉터리, 고아 데이터)
- 교차 참조 정합성 (CLAUDE.md, synapse-delegation.md 참조 vs 실제 파일)
- 파일 크기 및 품질

FAIL이 있으면 즉시 수정을 제안합니다. WARN은 수집해두고 Step 2에서 수동 검토와 함께 처리합니다.

### Step 1: 수동 검토 (스크립트가 잡지 못하는 항목)
자동 스크립트로 잡을 수 없는 정성적 항목을 확인합니다:
- description의 구체성 (모호하지 않은가?)
- 워크플로우 단계의 명확성
- 에이전트/스킬 간 역할 중복 여부

### Step 2: 경로 참조 검증
validate.sh의 경로 참조 결과를 검토합니다. 깨진 참조 중:
- /setup 전이라 아직 생성되지 않은 파일 (project-context.md 등): 정상 (WARN으로 기록)
- 오타나 잘못된 경로: 수정 제안

### Step 3: 결과 리포트

```
[Doctor 진단 결과]

통과: N개
경고: N개
오류: N개

오류 목록:
- [파일] [문제] [수정 방안]

경고 목록:
- [파일] [문제] [권장 조치]

사용 추적 요약:
- 추적 상태: [활성 (N일) / 미설정]
- 스킬: N개 추적 중 / N개 전체
- 커맨드: N개 추적 중 / N개 전체
- 에이전트: N개 추적 중 / N개 전체
- 고아 데이터: N개 (삭제 권장)

교차 참조 요약:
- CLAUDE.md + synapse-delegation.md 참조: N개 스킬, N개 에이전트
- 미등록 항목: [목록]
- README 개수 일치: [일치 / 불일치]

source 태그 요약:
- origin 파일: N개 (태그 정상: N개, 태그 누락: N개)
- custom 파일: N개
```

### Step 4: 자동 수정 제안
수정 가능한 항목은 구체적인 수정 방안을 제시하고, 사용자 확인 후 적용합니다:
- 고아 사용 데이터 → 삭제
- 실행 권한 누락 → chmod +x
- 깨진 경로 참조 → 경로 수정
- README 개수 불일치 → 업데이트
