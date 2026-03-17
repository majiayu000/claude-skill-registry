---
name: update-resume
description: 원본 변경 후 전체 파일 동기화가 필요할 때
---

# 이력서/경력기술서 업데이트

## 개요

`my_career_data.md` (Single Source of Truth)의 변경사항을 감지하고, 아래 파일들에 STAR+I 형식으로 동기화합니다.

## 대상 파일

### 1. 핵심 Markdown 파일 (2개)
1. `docs/career/resume.md` - 간결 이력서
2. `docs/career/career_portfolio.md` - 상세 경력기술서

### 2. 맞춤형 이력서 (formats/) (6개)
3. `docs/career/formats/TEMPLATE.md` - 템플릿 기본
4. `private/by-company/startup.md` - 스타트업용
5. `private/by-company/enterprise.md` - 대기업용
6. `docs/career/formats/by-domain/fintech.md` - 핀테크용
7. `docs/career/formats/by-domain/commerce.md` - 커머스용
8. `docs/career/formats/by-jd/backend_sample.md` - JD 샘플

### 3. 면접 스크립트 (1개)
9. `docs/career/interview_script.md` - 면접 답변 스크립트

### 4. Resume HTML 템플릿 (4개)
10. `templates/resume/default.html`
11. `templates/resume/minimal.html`
12. `templates/resume/modern.html`
13. `templates/resume/corporate.html`

### 5. Career HTML 템플릿 (4개)
14. `templates/career/default.html`
15. `templates/career/minimal.html`
16. `templates/career/modern.html`
17. `templates/career/corporate.html`

### 6. Work Logs
18. `docs/career/work-logs/{company}/*.md` - 해당 프로젝트 작업 로그 업데이트
19. `docs/career/work-logs/README.md` - 인덱스 업데이트

## 실행 단계

### Step 1: 변경사항 확인
```bash
git diff docs/career/my_career_data.md
```
- 변경된 프로젝트/섹션 식별
- 변경 범위 결정

### Step 2: 가이드 참조
- `/write-guide` 스킬 참조 (STAR+I, 시니어 톤, 정량화)
- STAR+I 형식 준수 확인

### Step 3: 핵심 파일 업데이트
- `resume.md`, `career_portfolio.md` 변경된 섹션만 정확히 반영
- 변경되지 않은 부분은 절대 수정 금지

### Step 4: formats/ 폴더 업데이트
- 맞춤형 이력서 6개 파일 동기화
- 각 파일의 특성(스타트업/대기업/핀테크/커머스)에 맞게 내용 반영

### Step 5: interview_script.md 업데이트
- 면접 스크립트의 해당 프로젝트 설명 동기화

### Step 6: HTML 템플릿 업데이트
- 8개 HTML 템플릿 구조 유지하며 내용만 교체

### Step 7: work-logs 업데이트
- 변경된 프로젝트의 work-logs 파일도 함께 업데이트
- work-logs 파일이 없으면 새로 생성
- README.md 인덱스 확인 및 업데이트

### Step 8: 검증
- STAR+I 형식 유지 확인
- 정량적 성과(숫자) 포함 확인
- 기술 선택 이유(Why) 포함 확인

### Step 9: git add
- 전체 대상 파일 staging
- commit은 하지 않음 (사용자 요청 시에만)

```bash
# 핵심 파일
git add docs/career/my_career_data.md
git add docs/career/resume.md
git add docs/career/career_portfolio.md

# formats 폴더
git add docs/career/formats/

# 면접 스크립트
git add docs/career/interview_script.md

# HTML 템플릿
git add templates/resume/*.html
git add templates/career/*.html

# work-logs
git add docs/career/work-logs/
```

## 주의사항

- 변경된 프로젝트/섹션만 업데이트
- 전체 내용 재작성 금지
- 사용하지 않은 기술 추가 금지
- "담당했습니다" 대신 "달성/개선했습니다" 표현 사용

## 체크리스트

### 변경 전 확인
- [ ] `git diff docs/career/my_career_data.md` 실행
- [ ] 변경된 프로젝트/섹션 확인
- [ ] 기술 선택 이유(Why)가 포함되었는가?

### 변경 적용
- [ ] 핵심 파일 업데이트 (resume.md, career_portfolio.md)
- [ ] formats/ 폴더 6개 파일 업데이트
- [ ] interview_script.md 업데이트
- [ ] HTML 템플릿 8개 파일 업데이트 (필요시)
- [ ] work-logs 해당 프로젝트 파일 업데이트
- [ ] work-logs/README.md 인덱스 업데이트 (필요시)
- [ ] STAR+I 형식 그대로 반영 (Impact 포함)
- [ ] **변경된 섹션만** 교체

### 검증
- [ ] 변경된 프로젝트만 업데이트되었는가?
- [ ] 전체 대상 파일 모두 업데이트되었는가?
- [ ] STAR+I 형식이 유지되었는가?
- [ ] 정량적 성과(숫자)가 포함되었는가?
- [ ] 기술 선택 이유(Why)가 드러나는가?
- [ ] 비즈니스 임팩트와 연결되는가?
- [ ] 사용하지 않은 기술이 제거되었는가?
- [ ] "담당했습니다" 대신 "달성/개선/설계했습니다" 표현 사용?

### git 작업
- [ ] git add 완료
- [ ] git status로 staging 확인
