---
name: setup
description: Claude Code 프로젝트 부트스트랩. 코드베이스를 분석하여 프로젝트 스택을 감지하고, 프로젝트 컨텍스트 규칙과 CLAUDE.local.md를 자동 생성합니다. 새 프로젝트에 .claude를 처음 적용할 때 사용합니다. Use when initializing .claude configuration for a new project.
disable-model-invocation: true
---

# Setup Skill — Claude Code 프로젝트 부트스트랩

코드베이스를 분석하여 프로젝트 스택을 감지하고, Claude Code에 맞는 프로젝트 컨텍스트와 규칙을 자동 생성합니다.

## 진입 조건

`.claude/project/.initialized` 파일이 존재하지 않을 때만 실행합니다.
이미 존재하면 setup을 건너뛰고 /evolve를 사용하도록 안내합니다.

---

## 워크플로우

### Step 0: 환경 준비 (Environment Preparation)

- `.claude/hooks/*.sh` 파일에 실행 권한 부여: `chmod +x .claude/hooks/*.sh`
- `.claude/project/usage-data/` 내부 기존 데이터 초기화 (씨앗에서 이전 프로젝트 데이터가 남아있을 수 있음)
- `.claude/project/usage-data/`에 4개 카테고리 디렉터리 생성: skills, commands, agents, subagents
- `.claude/project/usage-data/.tracked-since`에 현재 ISO8601 타임스탬프 기록

### Step 1: 프로젝트 감지 (Project Detection)

Glob, Grep, Read를 병렬로 실행하여 프로젝트 스택을 종합 분석합니다.

#### Track A — 언어 감지

- Glob으로 파일 확장자 검색: `*.swift`, `*.kt`, `*.ts`, `*.tsx`, `*.js`, `*.py`, `*.go`, `*.rs`, `*.java`, `*.rb`, `*.cs`, `*.cpp`, `*.c`, `*.m`, `*.h`
- 확장자별 파일 수 카운트
- primary/secondary 언어 결정 (예: Swift 85%, Objective-C 15%)

#### Track B — 패키지 매니저 감지

| 파일 | 패키지 매니저 |
|------|---------------|
| `Package.swift` | SPM |
| `package.json` | npm/yarn/pnpm |
| `requirements.txt`, `pyproject.toml` | pip/poetry |
| `build.gradle`, `build.gradle.kts` | Gradle |
| `Cargo.toml` | Cargo |
| `go.mod` | Go Modules |
| `Gemfile` | Bundler |
| `*.csproj` | NuGet |
| `Podfile`, `Cartfile` | CocoaPods/Carthage |

#### Track C — 프레임워크 감지

- Grep import: `import UIKit`, `import SwiftUI`, `import React`, `from 'react'`, `import django`, `import flask`, `import express` 등
- Grep 프레임워크별 패턴 (예: `@StateObject`, `createStore`, `Redux`)

#### Track D — 아키텍처 감지

- 아키텍처 패턴 검색: MVVM, MVC, Redux, Clean Architecture, VIPER, TCA
- 폴더 구조 힌트: `/features/`, `/domain/`, `/data/`, `/presentation/`, `/components/`, `/views/`, `/models/`

#### Track E — CI/CD 감지

- `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitrise.yml`, `fastlane/`

#### Track F — 빌드 도구 감지

- Tuist: `Project.swift`
- Xcode: `*.xcodeproj`
- Web: `webpack`, `vite`, `next.config`, `turbo.json`, `nx.json`

### Step 1.5: 이전 버전 감지 (Previous Version Detection)

프로젝트 감지와 병렬로, `.claude.back` 디렉터리 존재 여부를 확인합니다.

#### 감지

- Glob으로 `.claude.back/` 디렉터리 존재 여부 확인
- 존재하지 않으면 Step 2로 진행 (클린 설치)

#### 사용자 확인

`.claude.back`이 존재하면 사용자에게 질문:

```
이전 버전 .claude.back이 감지되었습니다.
기존 설정을 기반으로 새 환경을 구성할까요?

- "예": 이전 설정을 분석하여 커스텀 파일을 이관합니다
- "아니오": 클린 설치로 진행합니다
```

"아니오" 응답 시 Step 2로 진행합니다.

#### 이전 설정 분석 (Legacy Config Analysis)

"예" 응답 시, `.claude.back`의 다음 항목을 Read/Glob으로 분석합니다:

| 경로 | 추출 대상 |
|------|-----------|
| `rules/project-context.md` | 프로젝트 컨텍스트, 코딩 컨벤션 |
| `project/.initialized` | 프로젝트 스택, 기본 설정값 |
| `rules/*.md` | 프로젝트별 커스텀 룰 |
| `skills/*/SKILL.md` | 스킬 |
| `agents/*.md` | 에이전트 정의 |
| `settings.json` (hooks 섹션) + `hooks/*.sh` | 훅 설정 |
| `commands/*.md` | 커맨드 |

각 파일을 origin/custom으로 분류합니다.
분류 시 `.claude.back`의 파일에 source 태그가 있는지 확인하고, 새 `.claude`의 동일 경로 파일과 내용을 비교합니다:

source 태그 위치:
- 스킬/룰: YAML frontmatter 내 `source: origin`
- 커맨드: 파일 최상단 `<!-- source: origin -->`
- 훅 스크립트: shebang 다음 줄 `# source: origin`

| 기준 | source | 처리 |
|------|--------|------|
| 새 `.claude`에 동일 경로로 존재 + `source: origin` 태그 + 내용 동일 | `origin` | 새 버전 사용 (이관 스킵) |
| 새 `.claude`에 동일 경로로 존재 + `source: origin` 태그 + 내용 다름 | `origin (modified)` | 새 버전을 존중하되, 사용자 수정 사항을 보고 |
| 새 `.claude`에 없는 파일 | `custom` | 이관 대상 |

`origin (modified)` 감지 방법:
- `.claude.back`의 파일에 `source: origin` 태그가 있음 (원래 번들 파일)
- 새 `.claude`의 동일 경로 파일과 내용을 비교하여 차이가 있음
- 사용자가 origin 파일을 커스터마이징한 것으로 판단
- 새 버전의 origin을 항상 존중 (사용자 수정은 덮어씀)

분석 결과를 사용자에게 보고합니다:

```
이전 설정 분석 결과:
- 프로젝트: [name] ([type])
- origin (새 버전으로 대체): N개
- origin (사용자 수정 감지, 새 버전으로 대체): N개
  - skills/code-accuracy/SKILL.md (수정됨)
  - rules/synapse-delegation.md (수정됨)
  주의: 이전 버전에서 수정한 내용은 새 버전에 반영되지 않습니다.
  수정했던 파일은 .claude/project/history/modified-origins/ 에 백업됩니다.
  수정 내용을 유지하려면, 이관 후 해당 파일을 직접 수정하세요.
- custom (이관 대상):
  - 룰: N개 (rules/project-context.md, ...)
  - 스킬: N개 (skills/my-project-feature, ...)
  - 에이전트: N개 (agents/custom-explorer.md, ...)
  - 훅: N개
  - 커맨드: N개

이관을 진행할까요?
```

#### 이전 설정 이관 (Legacy Config Migration)

사용자가 이관을 승인하면:

1. `origin (modified)` 파일의 이전 버전(사용자가 수정한 버전)을 `.claude/project/history/modified-origins/`에 참고용으로 백업 (새 버전의 origin은 그대로 유지)
2. custom 파일을 새 `.claude`로 복사
3. 이전 `project-context.md`에서 프로젝트 컨텍스트, 코딩 컨벤션을 추출하여 Step 3에서 새 `project-context.md` 생성 시 반영
4. 이전 `.initialized`에서 프로젝트 스택 정보를 Step 3에서 seed로 활용
5. 용어 변경 자동 적용 (예: 이름 변경된 에이전트/스킬 경로 등)
6. 호환성 문제가 있는 파일은 경고 출력 후 사용자에게 수동 확인 요청
7. `origin (modified)` 파일이 있었다면, 백업 경로와 수정했던 파일 목록을 안내하여 필요시 수동으로 재적용할 수 있도록 함

이관 완료 후 Step 2로 진행합니다 (추가 스킬팩 첨부 기회 제공).

### Step 2: 스킬팩 / 참고자료 요청

프로젝트 스택 감지 결과를 사용자에게 보여준 뒤, 다음을 질문합니다:

```
감지된 프로젝트 스택: [언어], [프레임워크], [아키텍처]

이 프로젝트에 적용할 플랫폼별 스킬팩이나 참고할 코딩 가이드가 있으면 첨부해주세요.
(예: 코딩 컨벤션 문서, 아키텍처 가이드, 기존 rules 파일 등)

첨부 없이 진행하면 범용 스킬만으로 구성합니다.
```

사용자 응답에 따른 분기:

| 응답 | 처리 |
|------|------|
| 파일 첨부됨 | 분석하여 `.claude/skills/` 하위에 프로젝트 특화 스킬 생성 |
| 참고 자료 URL | WebFetch로 내용 수집하여 스킬 생성 |
| "없음" 또는 스킵 | 범용 스킬만으로 진행 |

첨부 파일 기반 스킬 생성 시:
- 핵심 규칙, 패턴, 체크리스트 추출
- `.claude/skills/{project-name}/SKILL.md` 형태로 생성
- YAML frontmatter에 `name`, `description` 포함
- 500줄 이하로 유지

### Step 3: 프로젝트 컨텍스트 규칙 생성

`.claude/rules/project-context.md`에 프로젝트 컨텍스트를 작성합니다.
이 파일은 Claude Code가 자동으로 로드하는 규칙 파일입니다.
Step 1.5에서 이전 설정이 이관된 경우, 이전 `project-context.md`의 내용을 seed로 활용합니다.

```yaml
---
description: "프로젝트 컨텍스트. 기술 스택, 아키텍처 패턴, 코딩 컨벤션을 정의합니다."
---
```

포함 내용:
- 프로젝트 이름, 타입 (mobile-app, web-app, library, cli, monorepo, backend)
- 기술 스택 요약 (언어, 프레임워크, 빌드 도구, CI/CD)
- 아키텍처 패턴 (감지된 구조)
- 기존 코드에서 추출한 코딩 컨벤션
- 파일 네이밍 패턴
- 커스텀 에이전트 목록 (16개: analyst, planner, critic, architect, implementer, debugger, build-fixer, migrator, tdd-guide, reviewer, qa-tester, security-reviewer, doc-writer, designer, researcher, vision)
- 활성화된 스킬 경로

### Step 4: CLAUDE.local.md 생성 (선택)

프로젝트 루트에 `CLAUDE.local.md`가 없으면 생성합니다:

```markdown
# 로컬 프로젝트 설정 (개인용, gitignore)

> 이 파일은 `.gitignore`에 추가하세요.
> 팀에 공유되지 않는 개인 설정을 여기에 작성합니다.

## 개인 선호사항

- 응답 언어: 한국어

## 로컬 환경

- 환경 변수나 로컬 경로 설정이 필요하면 여기에 작성
```

`.gitignore`에 `CLAUDE.local.md`가 없으면 추가를 안내합니다.

### Step 5: 프로젝트별 규칙 생성 (선택)

감지된 스택에 따라 `.claude/rules/` 에 추가 규칙 생성:

| 규칙 파일 | 생성 조건 | 내용 |
|-----------|-----------|------|
| `platform-conventions.md` | 언어/플랫폼 감지 시 | 언어별 코딩 컨벤션 |
| `framework-patterns.md` | 프레임워크 감지 시 | 프레임워크별 패턴, 베스트 프랙티스 |
| `architecture-guide.md` | 아키텍처 감지 시 | 아키텍처 레이어, 의존성 규칙 |

각 규칙 파일의 frontmatter:

```yaml
---
description: "[규칙 내용 요약]. [언제 적용되는지 설명]."
---
```

### Step 6: 초기화 완료

1. `.claude/project/.initialized` 마커 파일 생성 (내용: 날짜 + 감지 요약)
2. `.claude/project/VERSION`에 `1.0.0` 기록
3. 사용자에게 setup 요약 출력:

```
Setup 완료

감지된 스택:
- 언어: [primary] + [secondary]
- 프레임워크: [frameworks]
- 아키텍처: [architecture]
- 빌드 도구: [build tool]
- CI/CD: [cicd]

생성된 파일:
- .claude/rules/project-context.md (프로젝트 컨텍스트)
- .claude/rules/platform-conventions.md (선택)
- .claude/rules/framework-patterns.md (선택)
- .claude/rules/architecture-guide.md (선택)
- CLAUDE.local.md (선택)
- .claude/project/.initialized
- .claude/project/VERSION

이관 이력: (Step 1.5 실행 시)
- .claude.back에서 이관: custom N개, origin (modified) N개
- 백업: .claude/project/history/modified-origins/

다음 단계:
- /deep-index: 코드베이스 상세 인덱싱 (권장)
- /doctor: 설정 유효성 검사
- project-context.md를 검토하고 필요 시 수정하세요
```

---

## Claude Code 설정 구조 참조

setup이 생성/참조하는 파일 구조:

```
project-root/
├── CLAUDE.local.md                    # 로컬 개인 설정 (gitignore)
│
└── .claude/
    ├── CLAUDE.md                      # Synapse 오케스트레이터 (기존)
    ├── settings.json                  # hooks + permissions (기존)
    │
    ├── rules/                         # 자동 로드 규칙
    │   ├── claude-code-reference.md   # 파일 품질 게이트 (기존)
    │   ├── synapse-delegation.md      # 에이전트 위임 규칙 (기존)
    │   ├── synapse-skills.md          # 스킬 조합 전략 (기존)
    │   ├── project-context.md         # ← setup이 생성
    │   ├── platform-conventions.md    # ← setup이 생성 (선택)
    │   ├── framework-patterns.md      # ← setup이 생성 (선택)
    │   └── architecture-guide.md      # ← setup이 생성 (선택)
    │
    ├── agents/                        # 커스텀 에이전트 (16개)
    │   ├── analyst.md
    │   ├── architect.md
    │   ├── build-fixer.md
    │   ├── critic.md
    │   ├── debugger.md
    │   ├── designer.md
    │   ├── doc-writer.md
    │   ├── implementer.md
    │   ├── migrator.md
    │   ├── planner.md
    │   ├── qa-tester.md
    │   ├── researcher.md
    │   ├── reviewer.md
    │   ├── security-reviewer.md
    │   ├── tdd-guide.md
    │   └── vision.md
    │
    ├── skills/                        # 스킬
    │   └── {project-name}/SKILL.md    # ← setup이 생성 (선택)
    │
    └── project/                       # 프로젝트 상태
        ├── .initialized               # ← setup이 생성 (마커)
        └── VERSION                    # ← setup이 생성
```

## deep-index 연동

- setup 완료 후 deep-index Skill 실행 권장
- 코드베이스 상세 분석 시 project-context.md 보강에 활용

## evolve 연동

- setup 완료 후 `.initialized`가 존재하므로, 이후 프로젝트 변경 시 /evolve 사용
