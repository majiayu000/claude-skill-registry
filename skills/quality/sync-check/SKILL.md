---
name: sync-check
description: 원본과 생성 파일의 동기화 검증이 필요할 때
---

# 동기화 상태 검증

## 개요

원본 데이터(`my_career_data.md`)와 생성된 파일들 간의 일관성을 검증합니다.

## 검증 대상 파일 (10개)

### Markdown (2개)
1. `docs/career/resume.md`
2. `docs/career/career_portfolio.md`

### Resume HTML (4개)
3. `templates/resume/default.html`
4. `templates/resume/minimal.html`
5. `templates/resume/modern.html`
6. `templates/resume/corporate.html`

### Career HTML (4개)
7. `templates/career/default.html`
8. `templates/career/minimal.html`
9. `templates/career/modern.html`
10. `templates/career/corporate.html`

## 검증 항목

### 1. 프로젝트 정보
- 프로젝트명, 기간, 역할

### 2. 성과 수치
- 정량적 수치 (%, 배, 건수)
- Before/After 값

### 3. 기술 스택
- 사용 기술 목록
- 프로젝트별 기술 스택

### 4. STAR+I 형식
> 상세 기준: `/write-guide` 스킬 참조

### 5. 표현 스타일
- "담당했습니다" 사용 금지
- "달성/개선했습니다" 사용

## 실행 단계

### Step 1: 원본 데이터 확인
```bash
cat docs/career/my_career_data.md
```

### Step 2: 각 파일 비교
```bash
cat docs/career/resume.md
cat docs/career/career_portfolio.md
cat templates/resume/default.html
# ... (모든 템플릿)
```

### Step 3: 불일치 리포트

```markdown
## 불일치 항목

### 파일: [파일명]
| 항목 | 원본 | 현재값 |
|------|------|--------|
| [항목명] | [원본값] | [현재값] |
```

### Step 4: 결과 요약

```markdown
## 동기화 상태
- 총 검증: 10개
- 정상: N개
- 불일치: N개
```

## 체크리스트

- [ ] 프로젝트별 수치 일치
- [ ] 기술 스택 일치
- [ ] STAR+I 형식 준수
- [ ] 시니어 톤 표현 사용

## 불일치 발견 시

`/update-resume` 스킬 실행 권장
