---
name: add-project
description: 새 프로젝트를 STAR+I로 추가할 때
---

# 새 프로젝트 추가

## 개요

새로운 프로젝트 경험을 `my_career_data.md`에 STAR+I 형식으로 추가하고, 10개 파일에 동기화합니다.

## 실행 단계

### Step 1: 프로젝트 정보 수집

사용자에게 아래 정보 요청:

```markdown
## 프로젝트 기본 정보
- 프로젝트명:
- 기간: YYYY.MM - YYYY.MM
- 소속 회사/팀:

## STAR+I 상세

### Situation (상황/배경)
- 당시 문제점이나 제약사항은?
- 비즈니스적 배경은?

### Task (과제/목표)
- 해결해야 할 목표는? (가능하면 수치로)

### Action (실행/기술적 의사결정)
- 어떤 기술을 왜 선택했는가?
- 어떻게 설계/구현했는가?

### Result (결과/성과)
- 정량적 성과는? (%, 배, 건수 등)

### Impact (비즈니스 효과)
- 조직/비즈니스에 미친 영향은?

## 사용 기술
- 기술 스택 나열
```

### Step 2: STAR+I 형식으로 정리

```markdown
#### 프로젝트: [프로젝트명]

**Situation (배경):**
- [배경/문제점 설명]

**Task (과제/목표):**
- [해결 목표 - 수치 포함]

**Action (해결 방법):**
- **[핵심 액션 1]**: [상세 설명]
- **[핵심 액션 2]**: [상세 설명]

**Result (성과):**
- **[성과 1]**: [정량적 수치]
- **[성과 2]**: [정량적 수치]

**Impact (비즈니스 효과):**
- [비즈니스/조직적 효과]

**Tech Decision:**
> "[기술 A] 선택 - [선택 이유]"

**사용 기술:**
- [기술 스택 나열]
```

### Step 3: my_career_data.md에 추가

- 해당 회사 섹션에 프로젝트 추가
- 프로젝트 번호 순서 유지
- STAR+I 형식 정확히 적용

### Step 4: work-logs에 상세 작업 로그 작성

**파일 위치:** `docs/career/work-logs/{company}/project-{번호}-{slug}.md`

프로젝트의 상세 내용을 work-logs에 기록:
- 아키텍처 다이어그램
- 기술 스택 상세
- 구현 내용 상세
- 기술적 의사결정 배경
- 향후 개선점

**README.md 업데이트:** `docs/career/work-logs/README.md`에 인덱스 추가

### Step 5: 10개 파일 동기화

`/update-resume` 스킬 로직 활용:
1. resume.md 업데이트
2. career_portfolio.md 업데이트
3. templates/resume/*.html (4개) 업데이트
4. templates/career/*.html (4개) 업데이트

### Step 6: git add

```bash
git add docs/career/my_career_data.md
git add docs/career/resume.md
git add docs/career/career_portfolio.md
git add docs/career/work-logs/
git add templates/resume/*.html
git add templates/career/*.html
```

## STAR+I 작성 가이드

> **상세 가이드**: `/write-guide` 스킬 참조

### 핵심 요약

| 요소 | 작성 포인트 |
|------|------------|
| **Situation** | 비즈니스/기술적 제약 명시 |
| **Task** | 구체적 목표 수치 포함 |
| **Action** | **Why(선택 이유)** + How(구현 방법) |
| **Result** | Before → After 정량적 수치 |
| **Impact** | 비즈니스/팀 영향 |

### 8년차 핵심
- Action에 **"왜 그 기술을 선택했는지"** 의사결정 근거 필수
- "담당했습니다" 대신 **"달성/개선했습니다"** 표현 사용

## 체크리스트

- [ ] 프로젝트 정보 수집 완료
- [ ] STAR+I 형식 적용
- [ ] my_career_data.md에 추가
- [ ] work-logs에 상세 작업 로그 작성
- [ ] work-logs/README.md 인덱스 업데이트
- [ ] 10개 파일 동기화
- [ ] git add 완료
