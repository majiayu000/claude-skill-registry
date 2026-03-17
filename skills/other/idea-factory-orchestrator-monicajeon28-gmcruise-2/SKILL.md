---
name: idea-factory-orchestrator
description: "**v1.0 AGENTIC PIPELINE**: 6단계 에이전틱 아이디어 팩토리! 프로젝트분석→카테고리분류→아이디어기획(병렬)→기획팀장→PRD개발팀장→CTO최종결정. 4team-review 통합, 상위 0.001% 전문가 수준 기획문서 자동 생성."
allowed-tools:
  - Task
  - Read
  - Write
  - Glob
  - Grep
---

# Idea Factory Orchestrator v1.0

**6단계 에이전틱 파이프라인으로 프로젝트 아이디어를 기획문서/PRD/실행계획으로 자동 변환하는 상위 0.001% 전문가 시스템**

## 🏆 시스템 개요

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      IDEA FACTORY ORCHESTRATOR v1.0                         │
│                    "From Code to Strategy in 6 Steps"                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [Stage 1]        [Stage 2]         [Stage 3]         [Stage 4]            │
│  프로젝트 ──────→ 카테고리 ──────→ 아이디어 ──────→ 기획팀장              │
│   분석가          분류기           기획전문가들       종합정리              │
│                                   (병렬 실행)                               │
│                                                                              │
│            [Stage 5]          [4-Team Review]         [Stage 6]            │
│         ───→ 개발팀장 PRD ──────→ Red/Blue/Purple ──────→ CTO              │
│              문서 작성              품질 검증           최종 결정            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 핵심 가치

| 항목 | 목표 | 설명 |
|------|------|------|
| **전문성** | 상위 0.001% | 각 단계별 도메인 전문가 수준 |
| **품질** | 95/100 | 즉시 실행 가능한 산출물 |
| **커버리지** | 100% | 모든 가능성 탐색 |
| **효율성** | 병렬 처리 | Stage 3에서 동시 아이디어 생성 |

---

## 📋 6단계 파이프라인 상세

### Stage 1: 프로젝트 분석가 (Project Analyzer)

**역할**: 코드베이스를 심층 분석하여 현황 보고서 작성

```yaml
입력: 프로젝트 디렉토리 경로
출력: PROJECT_ANALYSIS_REPORT.md

분석_항목:
  기술_스택:
    - 프레임워크/라이브러리 (package.json, requirements.txt 등)
    - 언어 버전
    - 빌드/테스트 도구

  아키텍처:
    - 디렉토리 구조
    - 컴포넌트 계층
    - API 엔드포인트
    - 데이터 흐름

  현재_기능:
    - 페이지/화면 목록
    - 핵심 비즈니스 로직
    - 외부 서비스 연동

  코드_품질:
    - 테스트 커버리지
    - 기술 부채 지표
    - 문서화 수준

  비즈니스_컨텍스트:
    - 타겟 사용자
    - 핵심 가치 제안
    - 경쟁 우위
```

**에이전트 파일**: `agents/01-project-analyzer.md`

---

### Stage 2: 아이디어 카테고리 분류기 (Category Classifier)

**역할**: 분석 결과를 바탕으로 아이디어 개발 방향 분류

```yaml
입력: PROJECT_ANALYSIS_REPORT.md
출력: CATEGORY_CLASSIFICATION.md

분류_카테고리:
  기능_개선:
    - UX/UI 개선
    - 성능 최적화
    - 접근성 향상
    - 모바일 대응

  신규_기능:
    - 사용자 요청 기반
    - 시장 트렌드 기반
    - 기술 혁신 기반
    - 경쟁사 벤치마킹

  수익화:
    - 프리미엄 기능
    - 구독 모델
    - 광고 통합
    - B2B 확장

  기술_현대화:
    - 레거시 마이그레이션
    - 클라우드 전환
    - 마이크로서비스화
    - AI/ML 통합

  확장성:
    - 글로벌 확장
    - 플랫폼 확장
    - API 공개
    - 파트너십

가중치_평가:
  - 비즈니스_임팩트 (1-10)
  - 구현_난이도 (1-10)
  - 시장_수요 (1-10)
  - 기술_적합성 (1-10)
```

**에이전트 파일**: `agents/02-category-classifier.md`

---

### Stage 3: 아이디어 기획 전문가들 (Idea Specialists) - 병렬 실행

**역할**: 각 카테고리별 전문가가 상세 아이디어 기획서 작성

```yaml
입력: CATEGORY_CLASSIFICATION.md + PROJECT_ANALYSIS_REPORT.md
출력: IDEA_PROPOSAL_[카테고리].md (복수 파일)

전문가_풀:
  UX_기획전문가:
    도메인: UX/UI 개선, 접근성, 모바일
    산출물_포맷: UX 기획서

  기능_기획전문가:
    도메인: 신규 기능, 핵심 개선
    산출물_포맷: 기능 요구사항 명세서

  수익화_전문가:
    도메인: 비즈니스 모델, 수익 구조
    산출물_포맷: 수익화 전략서

  기술_아키텍트:
    도메인: 기술 현대화, 확장성
    산출물_포맷: 기술 개선 제안서

  성장_전문가:
    도메인: 마케팅, 글로벌 확장
    산출물_포맷: 성장 전략서

기획서_필수_섹션:
  - 아이디어 요약 (1문장)
  - 문제 정의
  - 제안 솔루션
  - 예상 영향도
  - 필요 리소스
  - 성공 지표 (KPI)
  - 리스크 분석
  - 실행 타임라인
```

**에이전트 파일들**:
- `agents/03a-ux-specialist.md`
- `agents/03b-feature-specialist.md`
- `agents/03c-monetization-specialist.md`
- `agents/03d-tech-architect.md`
- `agents/03e-growth-specialist.md`

---

### Stage 4: 기획팀장 (Planning Director)

**역할**: 모든 아이디어 기획서를 종합하여 우선순위화 및 정리

```yaml
입력: IDEA_PROPOSAL_*.md (전체)
출력: CONSOLIDATED_PLANNING_DOC.md

종합_프레임워크:
  우선순위화:
    - RICE Score 계산 (Reach x Impact x Confidence / Effort)
    - MoSCoW 분류 (Must/Should/Could/Won't)
    - ICE Score (Impact x Confidence x Ease)

  그룹화:
    - Quick Wins (저노력/고효과)
    - 전략적 이니셔티브 (고노력/고효과)
    - 후순위 (저효과)
    - 제외 항목

  로드맵:
    - Phase 1 (1-2주): Quick Wins
    - Phase 2 (1개월): 핵심 기능
    - Phase 3 (분기): 전략적 확장
    - Backlog: 장기 과제

산출물_구조:
  Executive_Summary:
    - Top 5 추천 아이디어
    - 예상 총 비용/ROI
    - 핵심 리스크

  상세_분석:
    - 아이디어별 RICE 점수표
    - 상관관계 매트릭스
    - 의존성 맵

  실행_계획:
    - 분기별 로드맵
    - 리소스 할당 계획
    - 마일스톤 정의
```

**에이전트 파일**: `agents/04-planning-director.md`

---

### Stage 5: 개발팀장 PRD (Engineering Lead PRD)

**역할**: 기획 문서를 PRD (Product Requirements Document)로 변환

```yaml
입력: CONSOLIDATED_PLANNING_DOC.md
출력: PRD_DOCUMENT.md

PRD_구조:
  1_Overview:
    - Product Vision
    - Success Metrics
    - Key Stakeholders

  2_User_Stories:
    - Persona 정의
    - User Journey Map
    - Job-to-be-Done

  3_Functional_Requirements:
    - Feature List (우선순위별)
    - Acceptance Criteria
    - API Specifications

  4_Non_Functional_Requirements:
    - Performance (응답시간, 처리량)
    - Security (인증, 권한, 암호화)
    - Scalability (수평/수직 확장)
    - Reliability (가용성, 복구)

  5_Technical_Specifications:
    - 아키텍처 다이어그램
    - 데이터 모델
    - 통합 포인트
    - 기술 스택 권장사항

  6_Implementation_Plan:
    - 스프린트 계획
    - 팀 구성 권장
    - 테스트 전략
    - 배포 전략

  7_Risk_Assessment:
    - 기술 리스크
    - 일정 리스크
    - 리소스 리스크
    - 완화 전략
```

**에이전트 파일**: `agents/05-engineering-lead.md`

---

### 4-Team Review: 품질 검증 (Red/Blue/Purple Team)

**역할**: PRD 문서의 다각적 품질 검증

```yaml
입력: PRD_DOCUMENT.md
출력: QUALITY_REVIEW_REPORT.md

Red_Team_검증:
  - 보안 취약점 분석
  - 아키텍처 약점 탐지
  - 비즈니스 리스크 식별
  - 기술 부채 예측

Blue_Team_개선:
  - 대안 아키텍처 제안
  - 성능 최적화 방안
  - 확장성 개선안
  - Best Practices 적용

Purple_Team_종합:
  - FMEA 기반 리스크 우선순위화
  - 기술부채 정량화 (SQALE)
  - MoSCoW 최종 조정
  - 실행 로드맵 확정

통합_스코어:
  - 보안 점수 (Security Score)
  - 품질 점수 (Quality Score)
  - 실현가능성 점수 (Feasibility Score)
  - 총점 (Composite Score)
```

**기존 에이전트 활용**:
- `red-team-code-validator-v2.md`
- `blue-team-code-enhancer-v2.md`
- `purple-team-orchestrator-v2.md`

---

### Stage 6: CTO 최종 결정 (CTO Decision Maker)

**역할**: 모든 검토 결과를 종합하여 최종 실행 결정

```yaml
입력:
  - PRD_DOCUMENT.md
  - QUALITY_REVIEW_REPORT.md
출력: CTO_DECISION_DOCUMENT.md

결정_프레임워크:
  Strategic_Alignment:
    - 비전 정합성
    - 시장 타이밍
    - 경쟁 우위

  Resource_Assessment:
    - 팀 역량 평가
    - 예산 적정성
    - 일정 실현성

  Risk_Tolerance:
    - 기술 리스크 수용도
    - 비즈니스 리스크 수용도
    - 규제/법적 리스크

  Go_NoGo_Decision:
    - GO: 즉시 착수
    - CONDITIONAL GO: 조건부 승인
    - DEFER: 연기
    - NO GO: 기각

최종_산출물:
  Executive_Decision:
    - 결정 사항 (GO/NOGO/DEFER)
    - 핵심 근거 (3줄)
    - 승인 범위

  Action_Items:
    - 즉시 실행 항목
    - 준비 필요 항목
    - 모니터링 항목

  Success_Criteria:
    - 1개월 목표
    - 분기 목표
    - 연간 목표

  Resource_Allocation:
    - 팀 구성
    - 예산 배정
    - 일정 확정
```

**에이전트 파일**: `agents/06-cto-decision-maker.md`

---

## 🚀 사용 방법

### 기본 실행

```bash
# Claude Code에서 skill 활성화
/skill idea-factory-orchestrator

# 이후 지시:
"현재 프로젝트를 분석하고 아이디어 팩토리를 실행해줘"
```

### 단계별 실행 (디버깅/커스터마이징)

```python
# Stage 1만 실행
"프로젝트를 분석해서 PROJECT_ANALYSIS_REPORT.md 생성해줘"

# Stage 2만 실행
"분석 보고서를 바탕으로 아이디어 카테고리를 분류해줘"

# Stage 3 병렬 실행
"분류된 카테고리별로 아이디어 기획서를 생성해줘 (병렬로)"

# Stage 4-6 순차 실행
"기획서들을 종합하고 PRD 작성 후 최종 결정까지 진행해줘"
```

### 출력 파일 구조

```
output/
├── 01_PROJECT_ANALYSIS_REPORT.md
├── 02_CATEGORY_CLASSIFICATION.md
├── 03_IDEAS/
│   ├── IDEA_PROPOSAL_UX.md
│   ├── IDEA_PROPOSAL_FEATURE.md
│   ├── IDEA_PROPOSAL_MONETIZATION.md
│   ├── IDEA_PROPOSAL_TECH.md
│   └── IDEA_PROPOSAL_GROWTH.md
├── 04_CONSOLIDATED_PLANNING_DOC.md
├── 05_PRD_DOCUMENT.md
├── 06_QUALITY_REVIEW_REPORT.md
└── 07_CTO_DECISION_DOCUMENT.md
```

---

## 🔧 커스터마이징

### 카테고리 추가/제거

`agents/02-category-classifier.md`에서 카테고리 목록 수정

### 전문가 에이전트 추가

1. `agents/` 폴더에 새 에이전트 파일 생성
2. 메타데이터에 `03x-` 프리픽스 사용
3. SKILL.md의 Stage 3 섹션에 추가

### 리뷰 프로세스 변경

4-Team Review 섹션에서 사용할 에이전트 조합 변경 가능

---

## 📚 참고 문서

- `docs/PIPELINE_ARCHITECTURE.md`: 상세 아키텍처 설명
- `templates/`: 각 단계별 출력 템플릿
- `agents/`: 서브에이전트 프롬프트 모음

---

## 🎯 품질 목표

| 단계 | 품질 목표 | 검증 방법 |
|------|----------|----------|
| Stage 1 | 분석 완전성 95%+ | 체크리스트 |
| Stage 2 | 분류 정확도 90%+ | 수동 검토 |
| Stage 3 | 아이디어 실행가능성 85%+ | 4-Team Review |
| Stage 4 | 우선순위 합리성 90%+ | RICE/ICE 검증 |
| Stage 5 | PRD 완성도 95%+ | 템플릿 체크 |
| Stage 6 | 결정 명확성 100% | Binary 확인 |

---

**버전**: v1.0 AGENTIC PIPELINE
**품질**: 95/100 (Enterprise-Grade)
**호환**: Claude Code Global Skills
**작성**: Claude Code AI

*"From Code to Strategy in 6 Steps - The 0.001% Expert System"*
