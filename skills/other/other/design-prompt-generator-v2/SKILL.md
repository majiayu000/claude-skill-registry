---
name: design-prompt-generator-v2
description: Advanced 7-step hierarchical design prompt generator for AI web development tools (Lovable, Cursor, Bolt). Generates domain-aware, user-journey-based design prompts with emotional design considerations. Triggers on "디자인 프롬프트", "웹 디자인", "Lovable 프롬프트", "랜딩페이지 만들어줘", or any AI web builder prompt requests.
---

# Design Prompt Generator v2

AI 웹 개발 도구(Lovable, Cursor, Bolt)를 위한 7단계 계층적 디자인 프롬프트 생성기입니다.

## 7-Step Framework

```
Step 1: Domain Research      → 업종 UX 패턴, 경쟁사 인사이트
Step 2: User Journey         → 핵심 사용자 흐름, 전환 포인트
Step 3: Emotional Design     → 감성 키워드, 무드 컨셉
Step 4: Identity & Goal      → 브랜드 정체성, 목표
Step 5: Design System        → 컬러, 타이포, 컴포넌트
Step 6: Component Specs      → 핵심 컴포넌트 상세 정의
Step 7: Micro-interactions   → 애니메이션, 인터랙션 패턴
```

---

## Step 1: Domain Research

업종별 UX 패턴과 경쟁사를 분석합니다.

**탐색 질문:**
- 이 도메인의 Top 3 앱/사이트는?
- 사용자가 기대하는 UX 패턴은? (예: 데이팅앱의 스와이프, 배달앱의 카드)
- 중요한 신뢰 신호는? (리뷰, 뱃지, 보증)
- 경쟁사가 해결하지 못한 페인포인트는?

**도메인별 패턴:**

| 도메인 | 예상 패턴 | 신뢰 신호 | 핵심 액션 |
|--------|-----------|-----------|-----------|
| Pet Services | 프로필 카드, 예약 캘린더, 펫 타입 필터 | 인증 뱃지, 리뷰, 보험 | 검색 → 조회 → 예약 → 결제 |
| SaaS | 기능 비교, 요금제, 데모 CTA | 로고, 후기, 보안 뱃지 | 학습 → 체험 → 구독 |
| E-commerce | 그리드 갤러리, 필터, 장바구니 | 리뷰, 반품정책, 보안결제 | 탐색 → 담기 → 결제 |
| Education | 강의 카드, 진도 추적, 강사 프로필 | 인증서, 수강생 수, 평점 | 탐색 → 등록 → 학습 |
| Healthcare | 의료진 검색, 예약 슬롯, 증상 체커 | 면허, 병원 소속 | 찾기 → 예약 → 상담 |
| Fintech | 대시보드, 거래 내역, 빠른 액션 | 암호화 뱃지, 규제 준수 | 연결 → 모니터링 → 실행 |
| Food Delivery | 레스토랑 카드, 실시간 추적, 재주문 | 평점, 배달 시간 예측 | 탐색 → 주문 → 추적 |
| Marketplace | 판매자 프로필, 리스팅 그리드, 메시징 | 인증, 거래 내역 | 검색 → 연락 → 거래 |

---

## Step 2: User Journey

핵심 사용자 흐름과 전환 포인트를 매핑합니다.

**프레임워크:**
```
[진입] → [발견] → [평가] → [결정] → [행동] → [유지]
```

**각 단계별 정의:**
```
Journey Stage: [단계명]
├── User Goal: 달성하고자 하는 것
├── Key Info: 필요한 정보
├── Friction: 이탈 요인
└── Solution: 디자인 해결책
```

---

## Step 3: Emotional Design

디자인이 불러일으킬 감정을 정의합니다.

**감정 키워드 매트릭스:**

| 감정 | 시각적 표현 | 컬러 방향 | 타이포 | 이미지 |
|------|-------------|-----------|--------|--------|
| Trust | 깔끔, 정돈, 일관성 | 블루, 그린 | 안정적 세리프/클린 산스 | 실제 사진, 뱃지 |
| Warmth | 부드러운 모서리, 유기적 형태 | 웜 옐로우, 오렌지 | 둥글고 친근함 | 일러스트, 미소 |
| Energy | 강한 대비, 다이나믹 앵글 | 비비드 레드, 오렌지 | 강렬, 임팩트 | 액션샷, 모션 |
| Calm | 여백, 미니멀 | 소프트 블루, 그린, 뉴트럴 | 가벼운 웨이트 | 자연, 미니멀 |
| Luxury | 다크 배경, 골드 액센트 | 블랙, 골드, 딥 퍼플 | 우아한 세리프 | 하이엔드 포토 |
| Playful | 비대칭, 애니메이션 | 밝고 다양한 팔레트 | 퀴키, 커스텀 | 일러스트, 아이콘 |
| Professional | 그리드 기반, 구조적 | 네이비, 그레이, 화이트 | 클래식 산스세리프 | 기업적, 클린 |

**감정 비율 정의 예시:** 60% Trust, 30% Warmth, 10% Energy

---

## Step 4: Identity & Goal

브랜드 포지셔닝을 명확히 정의합니다.

**템플릿:**
```
Service Name: [이름]
One-liner: [10단어 이내 설명]
Category: [도메인 카테고리]
Positioning: [경쟁사와의 차별점]
Primary Goal: [주요 전환 액션]
Secondary Goal: [보조 액션]
Brand Personality: [형용사 3개]
```

---

## Step 5: Design System

종합적인 비주얼 시스템을 정의합니다.

**컬러 시스템:**
```
Primary:      #[hex] - CTAs, 핵심 액션
Secondary:    #[hex] - 보조 요소
Accent:       #[hex] - 하이라이트, 뱃지
Background:   #[hex] - 기본 캔버스
Surface:      #[hex] - 카드, 상승 요소
Text Primary: #[hex] - 헤딩, 본문
Text Muted:   #[hex] - 캡션, 힌트
Success:      #[hex] - 확인
Warning:      #[hex] - 경고
Error:        #[hex] - 에러
```

**타이포그래피:**
```
Headings: [폰트] - [웨이트] - [특성]
Body: [폰트] - [웨이트] - [행간]
Scale: [base]px, ratio [비율]
```

**스페이싱 & 레이아웃:**
```
Base unit: [4/8]px
Border radius: [size]px
Shadow: subtle/medium/strong
Grid: [columns]columns, [gap]px gap
Container: max-width [width]px
```

**컴포넌트 스타일:**
```
Buttons: [shape], [padding], [hover]
Cards: [radius], [shadow], [padding]
Inputs: [border], [focus state]
```

---

## Step 6: Component Specs

도메인별 핵심 컴포넌트를 정의합니다.

**컴포넌트 템플릿:**
```
[Component Name]
├── Purpose: 존재 이유
├── Contents: 표시 정보
├── States: Default, Hover, Active, Disabled, Loading
├── Variants: 필요한 버전들
└── Responsive: 모바일 적응 방식
```

**공통 도메인 컴포넌트:**
- **Profile/Card**: 사용자 또는 아이템 표시
- **Search/Filter**: 탐색 메커니즘
- **Booking/Action**: 주요 전환
- **Review/Trust**: 소셜 프루프
- **Status/Progress**: 피드백 및 추적

---

## Step 7: Micro-interactions

애니메이션과 인터랙션 피드백을 정의합니다.

**카테고리:**

| 타입 | 목적 | 예시 |
|------|------|------|
| Entrance | 새 콘텐츠 주목 | Fade in, Slide up, Scale in |
| Feedback | 사용자 액션 확인 | 버튼 누름, 성공 체크마크 |
| State Change | 전환 표시 | 로딩 스피너, 스켈레톤 |
| Navigation | 뷰 간 가이드 | 페이지 전환, 드로어 슬라이드 |
| Delight | 기억에 남는 순간 | 컨페티, 바운스 |

**스펙 포맷:**
```
Trigger: [트리거]
Animation: [동작]
Duration: [시간 ms]
Easing: [커브]
Purpose: [목적]
```

**권장 기본값:**
- Micro-feedback: 150-200ms, ease-out
- Transitions: 250-350ms, ease-in-out
- Entrances: 400-600ms, ease-out + stagger

---

## Output Format

최종 프롬프트 구조:

```markdown
# [Service Name] Design Prompt

## Domain Context
[업계 인사이트, 사용자 기대, 경쟁 환경]

## User Journey
[단계별 흐름과 디자인 시사점]

## Emotional Direction
[주요 감정, 시각적 해석]

## Design Specifications

### Identity
[이름, 포지셔닝, 개성]

### Design System
[컬러, 타이포, 스페이싱 전체 스펙]

### Key Components
[도메인 특화 컴포넌트 정의]

### Interactions
[애니메이션, 마이크로 인터랙션 스펙]

## Implementation Prompt
[AI 도구용 복사-붙여넣기 프롬프트]

## Iterative Refinement Prompts
[단계별 개선 프롬프트]
```

---

## User Input

**필수:**
1. 서비스 주제/업종
2. 서비스 이름 (없으면 제안)

**선택 (더 좋은 결과):**
3. 타겟 사용자
4. 경쟁사 또는 참고 서비스
5. 원하는 분위기/감성
6. 필수 기능
7. 페이지 종류 (랜딩/앱UI/대시보드)

*최소 입력 시 도메인 기본값을 사용하고 가정을 명시합니다.*

---

## Quality Checklist

- [ ] 도메인 특화 UX 패턴 반영
- [ ] 사용자 여정 단계가 구조에 반영
- [ ] 감정 키워드가 시각 스펙으로 변환
- [ ] 컬러 시스템 완성 (용도 포함)
- [ ] 핵심 컴포넌트 상태 정의
- [ ] 마이크로 인터랙션 명시
- [ ] 모바일 반응형 고려
- [ ] 구현 프롬프트 복사-붙여넣기 가능
