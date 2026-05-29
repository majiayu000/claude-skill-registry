---
name: work-logs-sync
description: work-log 템플릿 변경 후 동기화가 필요할 때
---

# Work Logs 형식 동기화

## 개요

`/work-log` 스킬의 가이드(템플릿 형식)가 변경되었을 때, `docs/career/work-logs/` 디렉토리의 **모든 기존 작업 로그 파일**을 새 형식에 맞게 일괄 업데이트합니다.

## 동기화 흐름

```
.claude/skills/data/work-log/SKILL.md (가이드 변경)
    ↓
변경된 템플릿 형식 분석
    ↓
docs/career/work-logs/**/*.md (기존 파일들)
    ↓
새 형식에 맞게 일괄 변환
    ↓
git add
```

## 실행 단계

### Step 1: 가이드 변경사항 확인

```bash
git diff .claude/skills/data/work-log/SKILL.md
```

**확인 항목:**
- 템플릿 구조 변경 (섹션 추가/삭제/이름 변경)
- 필수 항목 변경
- 메타데이터 형식 변경
- 테이블/리스트 형식 변경

### Step 2: 현재 템플릿 형식 파악

`.claude/skills/data/work-log/SKILL.md`에서 템플릿 섹션 확인:

```markdown
## 현재 템플릿 구조
- 메타정보 (작성일, 소속, 기간)
- 개요
- 배경 및 문제점
- 상세 구현
- 결과 및 성과
- 팀 영향 및 공유
- 이력서 반영 여부
- 향후 개선점
```

### Step 3: 기존 work-logs 파일 목록 조회

```bash
find docs/career/work-logs -name "*.md" -not -name "README.md"
```

**대상 디렉토리:**
- `docs/career/work-logs/guhada/*.md`
- `docs/career/work-logs/interpark/*.md`
- `docs/career/work-logs/korealit/*.md`
- `docs/career/work-logs/personal/*.md`

### Step 4: 각 파일 형식 변환

**변환 규칙:**

| 변경 유형 | 처리 방법 |
|----------|----------|
| 섹션 추가 | 새 섹션을 적절한 위치에 추가 (기본값 또는 빈 내용) |
| 섹션 삭제 | 해당 섹션 제거 |
| 섹션 이름 변경 | 헤더 텍스트만 변경, 내용 유지 |
| 구조 변경 | 기존 내용을 새 구조에 맞게 재배치 |
| 테이블 형식 변경 | 기존 데이터를 새 테이블 형식으로 변환 |

**변환 시 주의사항:**
- 기존 내용(데이터)은 **절대 삭제하지 않음**
- 형식만 변경, 실제 작성된 내용은 보존
- 새 필수 섹션이 추가된 경우 빈 템플릿으로 추가

### Step 5: 파일별 변환 실행

각 파일에 대해:

1. 파일 읽기
2. 현재 구조 파악
3. 새 템플릿 구조와 비교
4. 차이점 변환 적용
5. 파일 저장

### Step 6: README.md 인덱스 확인

`docs/career/work-logs/README.md` 형식도 변경되었다면 함께 업데이트

### Step 7: git add

```bash
git add docs/career/work-logs/
git add .claude/skills/data/work-log/SKILL.md
```

## 체크리스트

### 변경 분석
- [ ] `/work-log` 스킬 가이드 변경사항 확인
- [ ] 변경된 템플릿 구조 파악
- [ ] 영향받는 섹션 목록 작성

### 파일 변환
- [ ] 대상 work-logs 파일 목록 확인
- [ ] 각 파일 형식 변환 실행
- [ ] 기존 내용 보존 확인
- [ ] 새 섹션 추가 (필요시)

### 검증
- [ ] 모든 파일 새 형식 준수
- [ ] 기존 데이터 손실 없음
- [ ] README.md 인덱스 정상

### git 작업
- [ ] git add 완료
- [ ] git status로 변경 파일 확인

## 주의사항

- **내용 보존 최우선**: 형식만 변경, 데이터 손실 금지
- **백업 권장**: 대량 변경 전 현재 상태 확인
- **점진적 적용**: 한 파일씩 변환 후 검증
- 새 필수 항목은 빈 값 또는 "(작성 필요)"로 표시
