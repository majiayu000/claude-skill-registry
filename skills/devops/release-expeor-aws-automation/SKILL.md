---
name: release
description: Semantic Versioning 기반 릴리스 관리. version.txt, CHANGELOG.md 자동 업데이트.
disable-model-invocation: true
---

# /release - 릴리스 관리 자동화

Semantic Versioning 기반 릴리스 프로세스를 자동화합니다.

## 사용법

```
/release <type>
```

타입:
- `patch` - 패치 버전 증가 (0.1.1 → 0.1.2)
- `minor` - 마이너 버전 증가 (0.1.1 → 0.2.0)
- `major` - 메이저 버전 증가 (0.1.1 → 1.0.0)
- `auto` - 최근 커밋 분석 기반 자동 결정

예시:
```
/release patch
/release minor
/release auto
```

## 실행 순서

### 1. 현재 버전 확인

`version.txt` 파일에서 현재 버전 읽기:
```bash
cat version.txt
```

### 2. 버전 타입 결정

#### `auto` 모드
최근 커밋 메시지 분석:
```bash
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD
```

커밋 타입별 버전 영향:
| Commit Type | 버전 변경 |
|-------------|----------|
| `feat!` 또는 `BREAKING CHANGE` | MAJOR |
| `feat` | MINOR |
| `fix`, `refactor`, `perf` | PATCH |
| `docs`, `test`, `chore`, `style`, `ci` | 변경 없음 |

우선순위: MAJOR > MINOR > PATCH

#### 명시적 지정
`$ARGUMENTS`가 `patch`, `minor`, `major` 중 하나인 경우 해당 타입 사용.

### 3. 새 버전 계산

```
현재: {MAJOR}.{MINOR}.{PATCH}

patch: {MAJOR}.{MINOR}.{PATCH+1}
minor: {MAJOR}.{MINOR+1}.0
major: {MAJOR+1}.0.0
```

### 4. 커밋 분류

최근 커밋을 CHANGELOG 섹션별로 분류:

```bash
git log --pretty=format:"%s" $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD
```

분류 기준:
- **Added**: `feat:` 커밋
- **Changed**: `refactor:`, `perf:` 커밋
- **Fixed**: `fix:` 커밋
- **Deprecated**: `deprecate:` 또는 메시지에 "deprecate" 포함
- **Removed**: 메시지에 "remove" 또는 "delete" 포함
- **Security**: `security:` 또는 메시지에 "security", "vulnerability" 포함

### 5. version.txt 업데이트

```bash
echo "{새_버전}" > version.txt
```

### 6. CHANGELOG.md 업데이트

CHANGELOG.md 파일 상단에 새 섹션 추가 (기존 `## [Unreleased]` 아래):

```markdown
## [{새_버전}] - {YYYY-MM-DD}

### Added
- feat(scope): 새 기능 설명
- feat: 다른 기능

### Changed
- refactor(scope): 변경 사항
- perf: 성능 개선

### Fixed
- fix(scope): 버그 수정 설명
- fix: 다른 수정

### Removed
- 제거된 기능 (해당되는 경우)
```

빈 섹션은 제외.

### 7. 검증

#### Git 상태 확인
```bash
git status
```
- 수정된 파일: `version.txt`, `CHANGELOG.md`

#### 태그 중복 확인
```bash
git tag -l "v{새_버전}"
```
- 이미 존재하면 경고 후 확인 요청

### 8. 커밋 생성 (선택)

사용자 확인 후 릴리스 커밋 생성:
```bash
git add version.txt CHANGELOG.md
git commit -m "chore: bump version to {새_버전}"
```

## 출력 예시

```
/release auto 실행 중...

[현재 버전] 0.1.1

[커밋 분석] 마지막 태그 이후 12개 커밋
  - feat: 3개 (새 기능)
  - fix: 5개 (버그 수정)
  - refactor: 2개 (리팩토링)
  - docs: 1개 (문서)
  - chore: 1개 (기타)

[버전 결정] MINOR (feat 커밋 존재)
  0.1.1 → 0.2.0

[CHANGELOG 미리보기]
────────────────────────────────────
## [0.2.0] - 2026-01-23

### Added
- feat(plugins): add elasticache unused cluster detection
- feat(ec2): add snapshot age analysis
- feat(cli): add headless mode support

### Changed
- refactor(core): improve parallel execution performance
- refactor(cli): simplify menu navigation

### Fixed
- fix(vpc): handle empty security group rules
- fix(iam): correct policy document parsing
- fix(core): resolve SSO token refresh issue
- fix(s3): handle bucket in different region
- fix(elb): fix target group health check
────────────────────────────────────

[파일 업데이트]
  ✓ version.txt: 0.1.1 → 0.2.0
  ✓ CHANGELOG.md: 새 섹션 추가

릴리스 커밋을 생성하시겠습니까? [Y/n]
```

## 커밋 타입 매핑

### Conventional Commits → Semantic Versioning

| Commit Prefix | 버전 영향 | CHANGELOG 섹션 |
|---------------|----------|----------------|
| `feat!:` | MAJOR | Breaking Changes |
| `BREAKING CHANGE:` | MAJOR | Breaking Changes |
| `feat:` | MINOR | Added |
| `fix:` | PATCH | Fixed |
| `refactor:` | PATCH | Changed |
| `perf:` | PATCH | Changed |
| `docs:` | - | - |
| `test:` | - | - |
| `chore:` | - | - |
| `style:` | - | - |
| `ci:` | - | - |

### Scope 처리

커밋 메시지의 scope는 CHANGELOG에 포함:
```
feat(plugins): add new tool  →  feat(plugins): add new tool
fix(core): resolve issue     →  fix(core): resolve issue
```

## 참조 파일

- `version.txt` - 현재 버전
- `CHANGELOG.md` - 변경 이력
- `.claude/skills/versioning.md` - 버전 관리 가이드
- `.claude/skills/commit-conventional.md` - 커밋 컨벤션

## 주의사항

1. **Dry-run 우선**: 파일 변경 전 미리보기 제공
2. **기존 형식 유지**: CHANGELOG.md의 기존 형식 준수
3. **태그 생성 안함**: 커밋만 생성, 태그는 별도 생성 필요
4. **푸시 안함**: 로컬 커밋만 생성, 푸시는 사용자 판단
5. **Breaking Change 주의**: MAJOR 버전 증가 시 명시적 확인

---

## GitHub Release Notes 생성 (선택)

`--github` 옵션 사용 시 GitHub Release Notes 초안 생성:

### 명령어

```bash
/release auto --github
```

### Release Notes 형식

```markdown
## What's Changed

### New Features
- feat(plugins): add elasticache unused cluster detection (#45)
- feat(ec2): add snapshot age analysis (#42)
- feat(cli): add headless mode support (#40)

### Bug Fixes
- fix(vpc): handle empty security group rules (#44)
- fix(iam): correct policy document parsing (#43)

### Other Changes
- refactor(core): improve parallel execution performance (#41)
- docs: update README with new examples (#39)

**Full Changelog**: https://github.com/org/repo/compare/v0.1.1...v0.2.0
```

### 커밋 링크 포함 CHANGELOG

```markdown
## [0.2.0] - 2026-01-24

### Added
- feat(plugins): add elasticache unused cluster detection ([#45](https://github.com/org/repo/pull/45))
- feat(ec2): add snapshot age analysis ([#42](https://github.com/org/repo/pull/42))

### Fixed
- fix(vpc): handle empty security group rules ([#44](https://github.com/org/repo/pull/44))
```

### gh CLI 연동

```bash
# Release 생성 (태그 필요)
git tag v0.2.0
git push origin v0.2.0

# GitHub Release 생성
gh release create v0.2.0 --title "v0.2.0" --notes-file release-notes.md

# 또는 자동 생성
gh release create v0.2.0 --generate-notes
```

## 에러 처리

### version.txt 없음
```
오류: version.txt 파일이 없습니다.
현재 버전을 설정하려면:
  echo "0.1.0" > version.txt
```

### CHANGELOG.md 없음
```
오류: CHANGELOG.md 파일이 없습니다.
파일을 생성하시겠습니까? [Y/n]
```

### 커밋 없음 (auto 모드)
```
알림: 마지막 릴리스 이후 버전에 영향을 주는 커밋이 없습니다.
  - docs: 2개
  - chore: 1개

버전을 유지하거나 수동으로 타입을 지정하세요:
  /release patch
```

### 이미 존재하는 태그
```
경고: 태그 v0.2.0이 이미 존재합니다.
다른 버전을 지정하거나 기존 태그를 삭제하세요.
```
