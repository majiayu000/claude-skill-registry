---
name: skill-management
description: Create, update, test, and manage Agent Skills. Use when creating new skills, debugging existing ones, or organizing skill libraries. Based on official Claude Code documentation.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: claude-docs
  version: "1.0"
---

# Skill Management

스킬 생성, 업데이트, 테스트, 관리를 위한 공식 가이드입니다.

## Skill 저장 위치

| 유형 | 경로 | 용도 |
|------|------|------|
| Personal | `~/.claude/skills/` | 개인 워크플로우, 실험적 스킬 |
| Project | `.claude/skills/` | 팀 워크플로우, Git 공유 |
| Plugin | 플러그인 번들 | 외부 플러그인과 함께 배포 |

---

## Skill 생성

### 1. 디렉토리 생성

```bash
# Personal Skill
mkdir -p ~/.claude/skills/my-skill-name

# Project Skill
mkdir -p .claude/skills/my-skill-name
```

### 2. SKILL.md 작성

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
allowed-tools: Read, Grep, Glob  # 선택사항
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

### Frontmatter 규칙

| 필드 | 필수 | 규칙 |
|------|------|------|
| `name` | ✅ | 소문자, 숫자, 하이픈만 (최대 64자) |
| `description` | ✅ | 수행 작업 + 사용 시기 (최대 1024자) |
| `allowed-tools` | ❌ | 사용 가능 도구 제한 |

---

## Skill 구조

### 단일 파일

```
my-skill/
└── SKILL.md
```

### 다중 파일

```
my-skill/
├── SKILL.md (필수)
├── references/
│   └── REFERENCE.md (선택)
├── scripts/
│   └── helper.py (선택)
└── templates/
    └── template.txt (선택)
```

### 참조 링크

```markdown
상세 내용은 [references/REFERENCE.md](references/REFERENCE.md) 참조.

스크립트 실행:
```bash
python scripts/helper.py input.txt
```
```

---

## allowed-tools

도구 사용을 제한하여 안전한 스킬 생성:

```yaml
---
name: safe-file-reader
description: Read files without making changes.
allowed-tools: Read, Grep, Glob
---
```

**사용 사례**:
- 읽기 전용 스킬
- 보안에 민감한 워크플로우
- 기능 범위 제한

---

## Skill 관리

### 목록 확인

```bash
# Personal Skills
ls ~/.claude/skills/

# Project Skills
ls .claude/skills/

# 특정 스킬 내용 확인
cat ~/.claude/skills/my-skill/SKILL.md
```

### 업데이트

```bash
# Personal Skill 편집
code ~/.claude/skills/my-skill/SKILL.md

# Project Skill 편집
code .claude/skills/my-skill/SKILL.md
```

### 제거

```bash
# Personal
rm -rf ~/.claude/skills/my-skill

# Project
rm -rf .claude/skills/my-skill
git commit -m "Remove unused Skill"
```

---

## 팀 공유

### 1단계: 프로젝트에 추가

```bash
mkdir -p .claude/skills/my-skill
# SKILL.md 작성
```

### 2단계: Git 커밋

```bash
git add .claude/skills/
git commit -m "feat(skills): add my-skill"
git push
```

### 3단계: 팀 멤버 자동 적용

팀 멤버가 pull 시 자동으로 스킬 사용 가능.

---

## 모범 사례

### 1. 집중적 유지

```
✅ GOOD: "Git commit messages"
✅ GOOD: "PDF form filling"
❌ BAD: "Document processing" (분할 필요)
```

### 2. 명확한 description

```yaml
# ✅ GOOD
description: Analyze Excel spreadsheets and create pivot tables. 
             Use when working with .xlsx files or tabular data.

# ❌ BAD
description: For files
```

### 3. 버전 문서화

```markdown
## Version History
- v2.0.0 (2025-10-01): Breaking changes
- v1.0.0 (2025-09-01): Initial release
```

### 4. 권장 라인 수

| 대상 | 권장 | 최대 |
|------|------|------|
| SKILL.md | 200줄 | 500줄 |
| REFERENCE.md | - | 제한 없음 |

---

## 문제 해결

### Claude가 스킬을 사용하지 않음

1. `description`이 트리거 키워드 포함하는지 확인
2. 파일 경로 확인 (`SKILL.md` 대소문자)
3. YAML 구문 오류 확인

### 스킬 오류 발생

```bash
# YAML 구문 검증
cat SKILL.md | head -10
```

### 여러 스킬 충돌

- `description`으로 트리거 조건 명확화
- 스킬 범위 좁히기

---

## 예제

### 간단한 스킬

```yaml
---
name: commit-helper
description: Generates clear commit messages from git diffs.
---

# Commit Helper

1. Run `git diff --staged` to see changes
2. Suggest commit message with:
   - Summary under 50 characters
   - Detailed description
```

### 읽기 전용 스킬

```yaml
---
name: code-reviewer
description: Review code for best practices.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Review checklist
1. Code organization
2. Error handling
3. Security concerns
```

---

## Checklist

스킬 생성 시:

- [ ] name: 소문자+숫자+하이픈, 64자 이내
- [ ] description: 작업 내용 + 사용 시기
- [ ] 단일 책임 원칙 (한 가지 역할)
- [ ] 예시 포함
- [ ] 500줄 이내 (초과 시 REFERENCE 분리)
