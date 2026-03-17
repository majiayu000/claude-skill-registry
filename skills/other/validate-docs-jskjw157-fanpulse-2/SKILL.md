---
name: validate-docs
description: "기획 문서 정합성 검증 스킬. 화면 정의서, DB 정의서, 프로젝트 기획서, API 계약서 간의 일관성을 검사합니다. 사용 시기: (1) 문서 수정 후 정합성 확인 (2) 새 화면/기능 추가 후 누락 확인 (3) 전체 문서 리뷰 시 (4) /validate-docs 호출 시"
---

# 기획 문서 정합성 검증

## 개요

FanPulse 기획 문서들(화면 정의서, DB 정의서, 프로젝트 기획서, API 계약서) 간의 정합성을 검증합니다.

## 검증 워크플로우

```
1. 문서 로드 → 2. 검증 수행 → 3. 불일치 리포트 생성
```

## 검증 항목

### 1. 화면 ↔ DB 정합성

화면에서 필요한 데이터가 DB에 정의되어 있는지 확인

| 검증 항목 | 설명 |
|-----------|------|
| 화면별 필수 테이블 | 화면 기능에 필요한 DB 테이블 존재 여부 |
| 필드 매핑 | 화면 표시 항목이 DB 컬럼으로 지원되는지 |
| 활용 화면 주석 | DB 테이블의 "활용 화면" 주석과 실제 화면 ID 일치 |

**검증 방법:**
1. `doc/화면_정의서.md` 또는 `doc/mvp/mvp_화면_정의서.md`에서 화면 ID, 기능 목록 추출
2. `doc/데이터베이스_정의서.md` 또는 `doc/mvp/mvp_데이터베이스_정의서.md`에서 테이블별 활용 화면 주석 추출
3. 화면 기능 키워드 → 필요 테이블 매핑 확인

### 2. 기획서 ↔ 화면 정합성

프로젝트 기획서의 핵심 기능이 화면으로 구현되었는지 확인

| 검증 항목 | 설명 |
|-----------|------|
| 기능 커버리지 | 기획서 핵심 기능별 담당 화면 존재 |
| 플로우 일치 | 기획서 사용자 플로우와 화면 연결 흐름 일치 |
| PRD 요구사항 | PRD의 기능 요구사항이 화면에 반영되었는지 |
| User Journey | 사용자 여정이 화면 흐름과 일치하는지 |

**검증 방법:**
1. `doc/프로젝트_기획서.md` 또는 `doc/mvp/mvp_기획서.md`에서 핵심 기능 목록 추출
2. `doc/mvp/mvp_PRD.md`에서 기능 요구사항 추출
3. `doc/mvp/mvp_user_journey.md`에서 사용자 여정 추출
4. `doc/화면_정의서.md`에서 화면별 주요 기능 추출
5. 기능 ↔ 화면 매핑 확인

### 3. API ↔ 화면/DB 정합성

API가 화면 기능을 지원하고 DB와 일관성 있는지 확인

| 검증 항목 | 설명 |
|-----------|------|
| 화면별 필요 API | 화면 기능 수행에 필요한 API 엔드포인트 존재 |
| API-DB 일관성 | API 응답 필드가 DB 스키마와 일치 |

**검증 방법:**
1. `doc/mvp/mvp_API_명세서.md`에서 API 엔드포인트 추출
2. 화면 기능 → 필요 API 매핑 확인

### 4. DDD ↔ 구현 문서 정합성

DDD 설계와 구현 문서 간 일관성 확인

| 검증 항목 | 설명 |
|-----------|------|
| Bounded Context | Context별 화면/API가 올바르게 분리되었는지 |
| Ubiquitous Language | DDD 용어와 화면/DB 용어 일치 |
| Domain Model | 도메인 모델이 DB 스키마에 반영되었는지 |
| Context Map | 컨텍스트 간 통합 방식이 API에 반영되었는지 |

**검증 방법:**
1. `doc/ddd/bounded-contexts/`에서 컨텍스트별 책임 추출
2. `doc/ddd/ubiquitous-language.md`에서 용어 정의 추출
3. `doc/ddd/domain-model.md`와 DB 스키마 비교
4. `doc/ddd/context-map.md`와 API 통합 방식 비교

### 5. IA ↔ 화면 정합성

정보 구조(IA)와 실제 화면 구조 일치 확인

| 검증 항목 | 설명 |
|-----------|------|
| 네비게이션 구조 | IA의 메뉴 구조가 화면에 반영되었는지 |
| 화면 계층 | IA 계층과 화면 ID 체계 일치 |

**검증 방법:**
1. `doc/mvp/mvp_IA.md`에서 정보 구조 추출
2. 화면 정의서와 구조 비교

### 6. 용어 일관성

문서 간 동일 개념에 대한 용어 통일 확인

| 검증 항목 | 설명 |
|-----------|------|
| 화면 ID | 모든 문서에서 동일한 화면 ID 사용 |
| 테이블/필드명 | API와 DB 간 네이밍 일관성 |
| 기능 명칭 | 동일 기능의 명칭 통일 |
| DDD 용어 | Ubiquitous Language와 일치 |

## 실행 방법

```
/validate-docs
```

또는 특정 검증만 수행:
```
/validate-docs --check screen-db
/validate-docs --check plan-screen
/validate-docs --check api
/validate-docs --check ddd
/validate-docs --check ia
/validate-docs --check terminology
```

## 리포트 형식

```markdown
# 문서 정합성 검증 리포트

## 요약
- 총 검증 항목: N개
- 통과: N개
- 불일치: N개
- 경고: N개

## 불일치 상세

### [심각도] 카테고리
- 문서1: 내용
- 문서2: 내용
- 권장 조치: ...
```

## 주요 매핑 규칙

화면-DB 매핑 규칙은 `references/validation_rules.md` 참조

## 문서 위치

### 전체 프로젝트 문서

| 문서 | 경로 |
|------|------|
| 화면 정의서 | `doc/화면_정의서.md` |
| DB 정의서 | `doc/데이터베이스_정의서.md` |
| 프로젝트 기획서 | `doc/프로젝트_기획서.md` |
| 크롤링 정의서 | `doc/크롤링.md` |
| 디자인 가이드 | `doc/디자인.md` |

### MVP 문서

| 문서 | 경로 |
|------|------|
| MVP 화면 정의서 | `doc/mvp/mvp_화면_정의서.md` |
| MVP DB 정의서 | `doc/mvp/mvp_데이터베이스_정의서.md` |
| MVP API 명세서 | `doc/mvp/mvp_API_명세서.md` |
| MVP 기획서 | `doc/mvp/mvp_기획서.md` |
| MVP PRD | `doc/mvp/mvp_PRD.md` |
| MVP IA | `doc/mvp/mvp_IA.md` |
| MVP User Journey | `doc/mvp/mvp_user_journey.md` |
| MVP 백로그 | `doc/mvp/mvp_백로그.md` |
| MVP 크롤링 | `doc/mvp/mvp_크롤링.md` |

### DDD 문서

| 문서 | 경로 |
|------|------|
| Bounded Contexts | `doc/ddd/bounded-contexts/` |
| Context Map | `doc/ddd/context-map.md` |
| Domain Model | `doc/ddd/domain-model.md` |
| Event Storming | `doc/ddd/event-storming.md` |
| Ubiquitous Language | `doc/ddd/ubiquitous-language.md` |
