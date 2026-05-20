---
name: report-writing
description: 작업 완료 후 상세 리포트 문서를 작성. 변경 이력, 영향도 분석, 검증 결과를 문서화할 때 사용. 파일명 규칙 YYYY-MM-DD-<제목>-report.md
allowed-tools: Read, Glob, Grep, Write
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Report Writing

작업 완료 후 상세 리포트를 작성하는 스킬입니다.

## Core Principle

> **"작업의 '무엇'과 '왜'를 기록하여 6개월 후에도 추적 가능하게"**

## 파일명 규칙 (필수)

```
docs/reports/YYYY-MM-DD-<제목>-report.md
```

예시:
- `2024-12-24-path-renaming-report.md`
- `2024-12-20-security-audit-report.md`
- `2024-12-15-migration-complete-report.md`

## 리포트 구조

### 필수 섹션

```markdown
# 🔄 [작업 제목] 리포트

**작성일**: YYYY-MM-DD
**작업자**: [작업자명]
**스킬 사용**: [사용한 스킬 목록]

---

## 📋 변경 개요

| 항목 | 내용 |
|------|------|
| **변경 사유** | [왜 이 작업이 필요했는지] |
| **변경 내용** | [무엇을 변경했는지] |
| **영향 범위** | [어디에 영향을 미치는지] |
| **상태** | ✅ 완료 / 🔄 진행중 / ❌ 실패 |

---

## 🔧 변경된 파일 목록

### 📝 수정된 파일

| # | 파일 | 변경 내용 | 변경 유형 |
|---|------|----------|----------|
| 1 | `파일경로` | 변경 설명 | 🔧 Refactor |

---

## 🔍 상세 변경 내역

### 파일명

\`\`\`diff
- 이전 내용
+ 변경된 내용
\`\`\`

---

## ✅ 검증 완료

\`\`\`bash
# 검증 명령어 및 결과
\`\`\`

---

## 📌 후속 작업

- [ ] 후속 작업 1
- [ ] 후속 작업 2
```

## 변경 유형 분류

| Prefix | 이모지 | 설명 |
|--------|--------|------|
| Feature | ✨ | 새로운 기능 추가 |
| Fix | 🐛 | 버그 수정 |
| Refactor | 🔧 | 코드 리팩토링 |
| Docs | 📚 | 문서 변경 |
| Performance | ⚡ | 성능 개선 |
| Security | 🔒 | 보안 관련 |
| Breaking | 💥 | 호환성 깨짐 |
| Delete | 🗑️ | 파일/기능 삭제 |

## Before/After 패턴

복잡한 변경에는 Before/After 비교 포함:

```markdown
### Before/After 구조

\`\`\`
Before                          After
──────────────────              ──────────────────
.old-folder/                    .new-folder/
├── files/                      ├── files/ ✏️
└── config/                     └── config/
\`\`\`
```

## 영향도 분석 섹션

```markdown
## 📊 영향도 분석

### 직접 영향
- 영향 1
- 영향 2

### 간접 영향
- 의존성 변경
- 설정 파일 업데이트 필요

### 유지된 항목
| 항목 | 사유 |
|------|------|
| 항목1 | 변경하지 않은 이유 |
```

## 다이어그램 (선택)

Mermaid로 아키텍처 변경 시각화:

```markdown
\`\`\`mermaid
graph LR
    A[Before] --> B[Change]
    B --> C[After]
\`\`\`
```

## Workflow

### 1. 정보 수집

```bash
# 변경된 파일 확인
git status --porcelain

# 변경 내용 확인
git diff --name-only HEAD
```

### 2. 리포트 초안 작성

필수 섹션 구조에 맞춰 작성

### 3. 검증 결과 추가

실제 검증 명령어와 결과 포함

### 4. 후속 작업 정리

남은 작업 체크리스트로 정리

## 관련 스킬

리포트 작성 시 함께 활용:

| 스킬 | 활용 |
|------|------|
| `changelog-generator` | 변경 분류, 이모지 체계 |
| `adr-log` | 결정 기록, 대안 분석 |
| `writing-plans` | 태스크 구조화 |

## Checklist

리포트 작성 완료 전 확인:

- [ ] 파일명이 `YYYY-MM-DD-<제목>-report.md` 형식
- [ ] 변경 개요 테이블 작성
- [ ] 모든 변경 파일 목록화
- [ ] diff 형식 상세 내역 포함
- [ ] 검증 명령어/결과 포함
- [ ] 후속 작업 체크리스트 작성
