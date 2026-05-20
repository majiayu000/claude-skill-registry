---
name: commit
description: Conventional Commits 형식 커밋 메시지 자동 생성. Git 변경사항 분석 후 커밋 수행.
disable-model-invocation: true
---

# /commit - Conventional Commits 자동화

Git 변경사항을 분석하고 Conventional Commits 형식의 커밋 메시지를 자동 생성합니다.

## 사용법

```
/commit [옵션]
```

옵션:
- `--amend`: 이전 커밋 수정 (주의: pre-commit 훅 실패 시에는 사용하지 않음)
- `--dry-run`: 커밋 메시지만 출력하고 실제 커밋하지 않음

## 실행 순서

### 1. 변경사항 분석

```bash
# 스테이지되지 않은 변경사항
git status

# 스테이지된 변경사항 (커밋 대상)
git diff --cached --stat

# 상세 diff (커밋 대상)
git diff --cached

# 최근 커밋 메시지 스타일 확인
git log --oneline -10
```

### 2. 커밋 타입 자동 분류

변경 파일과 내용을 분석하여 타입 결정:

| Type | 조건 | 예시 |
|------|------|------|
| `feat` | 새 기능, 새 파일, 새 함수 추가 | 새 플러그인, 새 도구 |
| `fix` | 버그 수정, 예외 처리 추가 | 오류 수정, None 체크 |
| `refactor` | 구조 변경 (기능 동일) | 함수 분리, 변수명 변경 |
| `docs` | 문서 파일만 변경 | README, CLAUDE.md |
| `test` | 테스트 파일만 변경 | test_*.py |
| `chore` | 설정, 의존성, 빌드 | pyproject.toml, requirements.txt |
| `style` | 포맷팅, 공백, 임포트 정리 | ruff format 결과 |
| `perf` | 성능 개선 | 캐싱, 최적화 |
| `ci` | CI/CD 설정 | .github/workflows |

### 3. Scope 결정

변경 파일 경로에서 scope 추출:

| 경로 패턴 | Scope |
|-----------|-------|
| `cli/*` | `cli` |
| `core/*` | `core` |
| `plugins/{service}/*` | `{service}` |
| `tests/*` | `tests` |
| `pyproject.toml`, `requirements*.txt` | `deps` |
| 여러 영역 | 가장 주요한 영역 또는 생략 |

### 4. 커밋 메시지 생성

```
<type>(<scope>): <description>

[optional body]

Co-Authored-By: Claude <claude-code@anthropic.com>
```

#### 메시지 작성 규칙

- **description**: 영문 소문자 시작, 50자 이내, 명령형
- **body**: 무엇을/왜 변경했는지 설명 (필요 시)
- **Co-Authored-By**: 항상 포함

### 5. 커밋 실행

```bash
git commit -m "$(cat <<'EOF'
type(scope): description

body (optional)

Co-Authored-By: Claude <claude-code@anthropic.com>
EOF
)"
```

### 6. 버전 업데이트 안내

커밋 타입에 따라 버전 변경 필요 여부 안내:

| Commit Type | 버전 변경 | 안내 메시지 |
|-------------|----------|-------------|
| `feat` | MINOR ↑ | "버전 업데이트 권장: MINOR (예: 0.1.1 → 0.2.0)" |
| `fix`, `refactor` | PATCH ↑ | "버전 업데이트 권장: PATCH (예: 0.1.1 → 0.1.2)" |
| `feat!`, `BREAKING CHANGE` | MAJOR ↑ | "버전 업데이트 필수: MAJOR (예: 0.1.1 → 1.0.0)" |
| `docs`, `test`, `chore` | 없음 | 버전 업데이트 불필요 |

## 예시

### 새 플러그인 추가

```
/commit

분석 결과:
  - 변경 파일: plugins/elasticache/__init__.py, plugins/elasticache/unused.py
  - 타입: feat (새 파일 추가)
  - Scope: elasticache

커밋 메시지:
  feat(elasticache): add unused cluster detection

  - Add CATEGORY and TOOLS definition
  - Implement unused cluster analysis with CloudWatch metrics
  - Support Redis and Memcached clusters

  Co-Authored-By: Claude <claude-code@anthropic.com>

버전 업데이트 권장: MINOR (0.2.3 → 0.3.0)
```

### 버그 수정

```
/commit

분석 결과:
  - 변경 파일: core/parallel/executor.py
  - 타입: fix (예외 처리 추가)
  - Scope: core

커밋 메시지:
  fix(core): handle SSO token expiration gracefully

  Co-Authored-By: Claude <claude-code@anthropic.com>

버전 업데이트 권장: PATCH (0.2.3 → 0.2.4)
```

### 문서 수정

```
/commit

분석 결과:
  - 변경 파일: CLAUDE.md, README.md
  - 타입: docs
  - Scope: (생략)

커밋 메시지:
  docs: update plugin development guide

  Co-Authored-By: Claude <claude-code@anthropic.com>

버전 업데이트 불필요
```

## Breaking Change 처리

Breaking Change가 감지되면:

```
feat(cli)!: change run command arguments

BREAKING CHANGE: -p flag now requires profile name instead of index

Co-Authored-By: Claude <claude-code@anthropic.com>
```

## 주의사항

1. **스테이지된 파일만 커밋**: `git add`로 스테이지한 파일만 분석
2. **민감 정보 확인**: .env, credentials 파일이 포함되어 있으면 경고
3. **Pre-commit 훅 실패 시**: 새 커밋 생성 (--amend 사용 금지)
4. **대용량 변경**: 50개 이상 파일 변경 시 확인 요청
5. **master 브랜치 직접 push 금지**:
   - master 브랜치에서 작업 중이면 feature 브랜치 생성 권장
   - 커밋 후 push 시 `gh pr create`로 PR 생성

## 참조 파일

- `.claude/skills/commit-conventional.md` - Conventional Commits 가이드
- `version.txt` - 현재 버전
- `CHANGELOG.md` - 변경 이력
