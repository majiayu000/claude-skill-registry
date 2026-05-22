---
name: changelog-generator
description: Generate user-friendly release notes from git commits. Use this when preparing releases, writing changelogs, or summarizing development progress.
allowed-tools: Read, Glob, Grep, Bash, Write
license: MIT
metadata:
  author: ComposioHQ
  version: "1.0"
---

# Changelog Generator

Git 커밋을 사용자 친화적인 릴리즈 노트로 변환하는 스킬입니다.

## Workflow

### Step 1: 커밋 히스토리 수집

```bash
# 최근 릴리즈 이후 커밋
git log --oneline $(git describe --tags --abbrev=0)..HEAD

# 특정 기간 커밋
git log --oneline --since="2024-01-01"

# 상세 정보 포함
git log --pretty=format:"%h - %s (%an, %ar)" --since="1 week ago"
```

### Step 2: 커밋 분류

| Prefix | 카테고리 | 설명 |
|--------|----------|------|
| `feat:` | ✨ New Features | 새로운 기능 |
| `fix:` | 🐛 Bug Fixes | 버그 수정 |
| `perf:` | ⚡ Performance | 성능 개선 |
| `docs:` | 📚 Documentation | 문서 변경 |
| `refactor:` | 🔧 Refactoring | 리팩토링 |
| `test:` | 🧪 Tests | 테스트 추가/수정 |
| `chore:` | 🔨 Chores | 빌드/설정 변경 |
| `BREAKING:` | 💥 Breaking Changes | 호환성 깨짐 |

### Step 3: 사용자 관점으로 변환

**개발자 커밋:**
```
feat: implement JWT token refresh mechanism
fix: resolve race condition in order processing
```

**사용자 릴리즈 노트:**
```
✨ 새로운 기능
- 자동 로그인 갱신으로 더 오래 로그인 상태 유지

🐛 버그 수정
- 주문 처리 중 간헐적 오류 수정
```

## Output Format

### Standard CHANGELOG.md

```markdown
# Changelog

## [1.2.0] - 2024-12-22

### ✨ New Features
- Feature A description
- Feature B description

### 🐛 Bug Fixes
- Fixed issue X
- Resolved problem Y

### ⚡ Performance
- Improved loading speed

### 💥 Breaking Changes
- Changed API endpoint structure
```

### GitHub Release Notes

```markdown
## What's New

### Highlights
🎉 **Feature A** - Brief exciting description

### All Changes
- feat: detailed change 1
- fix: detailed change 2

### Contributors
@user1, @user2
```

## Examples

### Example 1: 버전 릴리즈
```
User: v1.2.0 릴리즈 노트 만들어줘

Claude:
1. git log로 이전 태그 이후 커밋 수집
2. Conventional Commits 기준 분류
3. 사용자 관점으로 변환
4. CHANGELOG.md 업데이트
```

### Example 2: 주간 업데이트
```
User: 이번 주 개발 내용 정리해줘

Claude:
1. git log --since="1 week ago" 실행
2. 주요 변경사항 요약
3. 팀 공유용 문서 생성
```

## Automation

### Pre-release Hook

```bash
#!/bin/bash
# .git/hooks/pre-tag

# 현재 버전과 이전 버전 사이 변경사항 추출
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null)..HEAD > /tmp/changes.txt

echo "Changes since last release:"
cat /tmp/changes.txt
```

### CI Integration

```yaml
# .github/workflows/release.yml
- name: Generate Changelog
  run: |
    git log --oneline ${{ github.event.before }}..${{ github.sha }} > changes.txt
    # Claude API로 릴리즈 노트 생성
```

## Best Practices

1. **Conventional Commits 사용**: `type(scope): message`
2. **사용자 관점**: 기술 용어 → 사용자 이점
3. **Breaking Changes 강조**: 마이그레이션 가이드 포함
4. **감사 표시**: 기여자 멘션
