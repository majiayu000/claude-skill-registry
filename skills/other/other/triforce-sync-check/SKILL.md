---
name: triforce-sync-check
description: Verify 3-Mirror skill sync consistency across .public/skills, .codex/skills, and .claude/skills. Use after skill changes, before commits, or for CI validation.
allowed-tools: Read, Glob, Grep, Bash
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Triforce Sync Check

3-Mirror 스킬 동기화 일관성을 검증하는 스킬입니다.

## Architecture

```
.public/skills/     (SSOT - Single Source of Truth)
       │
       ├──► .codex/skills/   (Mirror - Antigravity/Codex)
       │
       └──► .claude/skills/  (Mirror - Claude Code)
```

## When to Use

- 스킬 추가/수정/삭제 후
- 커밋 전 검증
- CI/CD 파이프라인
- 배포 전 확인

## Quick Check

```bash
# 1. 스킬 수 확인
ls -1d .public/skills/*/ | wc -l
ls -1d .codex/skills/*/ | wc -l
ls -1d .claude/skills/*/ | wc -l

# 2. 콘텐츠 해시 비교
find .public/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5
find .codex/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5
find .claude/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5
```

## Full Verification Checklist

### 1. Count Verification

```bash
public_count=$(ls -1d .public/skills/*/ | wc -l)
codex_count=$(ls -1d .codex/skills/*/ | wc -l)
claude_count=$(ls -1d .claude/skills/*/ | wc -l)

echo "SSOT:   $public_count"
echo "Codex:  $codex_count"
echo "Claude: $claude_count"
```

**Pass Criteria**: 3개 값이 모두 동일

### 2. Structure Verification

```bash
# 디렉토리 목록 비교
diff <(ls -1 .public/skills | sort) <(ls -1 .codex/skills | sort)
diff <(ls -1 .public/skills | sort) <(ls -1 .claude/skills | sort)
```

**Pass Criteria**: diff 출력 없음 (빈 결과)

### 3. Content Verification

```bash
# SKILL.md 파일 해시 비교
public_hash=$(find .public/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5)
codex_hash=$(find .codex/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5)
claude_hash=$(find .claude/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5)

[ "$public_hash" = "$codex_hash" ] && [ "$public_hash" = "$claude_hash" ]
```

**Pass Criteria**: 3개 해시가 모두 동일

### 4. YAML Validation

```bash
# 각 SKILL.md의 frontmatter 유효성
for skill in .public/skills/*/SKILL.md; do
  name=$(grep "^name:" "$skill" | head -1)
  desc=$(grep "^description:" "$skill" | head -1)
  if [ -z "$name" ] || [ -z "$desc" ]; then
    echo "INVALID: $skill"
  fi
done
```

**Pass Criteria**: INVALID 출력 없음

### 5. Duplicate Check

```bash
# name 필드 중복 확인
grep -h "^name:" .public/skills/*/SKILL.md | sort | uniq -c | grep -v "^ *1 "
```

**Pass Criteria**: 출력 없음 (중복 없음)

## Sync Command

불일치 발견 시 재동기화:

```bash
node scripts/sync-skills.js
```

## CI Integration

```yaml
# .github/workflows/skills-check.yml
- name: Triforce Sync Check
  run: |
    public=$(ls -1d .public/skills/*/ | wc -l)
    codex=$(ls -1d .codex/skills/*/ | wc -l)
    claude=$(ls -1d .claude/skills/*/ | wc -l)

    if [ "$public" != "$codex" ] || [ "$public" != "$claude" ]; then
      echo "❌ Mirror count mismatch"
      exit 1
    fi

    pub=$(find .public/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5)
    cx=$(find .codex/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5)
    cl=$(find .claude/skills -name "SKILL.md" -exec md5 -q {} \; | sort | md5)

    if [ "$pub" != "$cx" ] || [ "$pub" != "$cl" ]; then
      echo "❌ Content hash mismatch"
      exit 1
    fi

    echo "✅ Triforce sync verified"
```

## Troubleshooting

| 증상 | 원인 | 해결 |
|------|------|------|
| 수 불일치 | sync 미실행 | `node scripts/sync-skills.js` |
| 해시 불일치 | 직접 미러 수정 | SSOT 수정 후 sync |
| YAML 오류 | frontmatter 형식 | name/description 확인 |
| 중복 name | 복사 붙여넣기 실수 | 고유한 name으로 수정 |

## Pass/Fail Summary

```
✅ PASS 조건:
- Count: github = codex = claude
- Structure: 동일한 디렉토리 목록
- Content: 동일한 해시값
- YAML: 모든 스킬에 name + description
- Unique: 중복 name 없음

❌ FAIL 시:
1. 오류 유형 식별
2. SSOT (.public/skills) 수정
3. sync-skills.js 실행
4. 재검증
```
