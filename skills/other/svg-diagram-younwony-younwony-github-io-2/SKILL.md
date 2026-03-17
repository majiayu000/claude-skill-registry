---
name: svg-diagram
description: 정교한 SVG 아키텍처 다이어그램이 필요할 때
---

# SVG 직접 생성 스킬

> 직접 SVG 코드를 작성하여 정교한 다이어그램을 생성합니다.
> 포트폴리오의 **아키텍처 다이어그램** 작성에 적합합니다.

---

## 언제 이 방식을 사용하는가?

| 상황 | SVG 직접 생성 적합 |
|------|-------------------|
| **Before/After 비교** | 시스템 개선 전후 비교 (포트폴리오 핵심) |
| **아키텍처 구조도** | 데이터 파이프라인, MSA 구성, 시스템 구성 |
| **계층 구조** | 레이어 구조, 컴포넌트 스택 |
| **데이터 흐름** | 배치 프로세스, ETL 파이프라인 |
| **상태 다이어그램** | 서킷브레이커, 상태 머신 |
| **정교한 레이아웃** | 정확한 위치, 크기, 정렬이 필요한 경우 |

## 장점

- 정확한 레이아웃 제어
- 그라디언트, 그림자 등 시각 효과
- 일관된 색상 팔레트 적용
- 한글 텍스트 완벽 지원
- 추가 도구 설치 불필요

## 파일 구조

```
docs/career/portfolio/
├── portfolio.md                     # 포트폴리오 문서
└── images/
    ├── data-pipeline-before.svg     # Before 아키텍처
    ├── data-pipeline-after.svg      # After 아키텍처
    └── search-system.svg            # 검색 시스템 구성도
```

### 파일명 규칙

| 유형 | 파일명 예시 |
|------|------------|
| Before/After | `{project}-before.svg`, `{project}-after.svg` |
| 시스템 구성도 | `{system}-architecture.svg` |
| 데이터 흐름 | `{process}-flow.svg` |
| 상태 다이어그램 | `{feature}-state.svg` |

---

## SVG 생성 규칙

### 1. 기본 구조

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
  <defs>
    <!-- 그라디언트, 마커 정의 -->
  </defs>
  <!-- 다이어그램 요소 -->
</svg>
```

### 2. 색상 팔레트 (필수)

#### 기본 노드 색상

| 용도 | 그라디언트 시작색 | 그라디언트 끝색 | 텍스트색 |
|------|------------------|----------------|---------|
| **파랑 (기본)** | #3498DB | #2980B9 | white |
| **초록 (성공)** | #2ECC71 | #27AE60 | white |
| **빨강 (경고)** | #E74C3C | #C0392B | white |
| **주황** | #E67E22 | #D35400 | white |
| **노랑** | #F1C40F | #F39C12 | white |
| **보라** | #9B59B6 | #8E44AD | white |
| **청록** | #1ABC9C | #16A085 | white |

#### 배경/보조 색상

| 용도 | 색상 | 사용처 |
|------|------|--------|
| 제목 텍스트 | #2C3E50 | 헤더, 타이틀 |
| 보조 텍스트 | #7F8C8D | 부제, 레이블 |
| 선/테두리 | #7F8C8D | 간선, 구분선 |
| 연한 배경 | #ECF0F1 | 컨테이너 |

### 3. 그라디언트 정의 템플릿

```xml
<defs>
  <linearGradient id="nodeBlue" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#3498DB"/>
    <stop offset="100%" style="stop-color:#2980B9"/>
  </linearGradient>
  <linearGradient id="nodeGreen" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#2ECC71"/>
    <stop offset="100%" style="stop-color:#27AE60"/>
  </linearGradient>
  <linearGradient id="nodeRed" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#E74C3C"/>
    <stop offset="100%" style="stop-color:#C0392B"/>
  </linearGradient>
  <linearGradient id="nodePurple" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#9B59B6"/>
    <stop offset="100%" style="stop-color:#8E44AD"/>
  </linearGradient>
  <linearGradient id="nodeOrange" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#E67E22"/>
    <stop offset="100%" style="stop-color:#D35400"/>
  </linearGradient>
</defs>
```

### 4. 화살표 마커 정의

```xml
<defs>
  <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#7F8C8D"/>
  </marker>
  <marker id="arrowRed" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#E74C3C"/>
  </marker>
  <marker id="arrowGreen" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#27AE60"/>
  </marker>
</defs>
```

### 5. 요소 스타일 규칙

#### 원형 노드 (트리, 그래프)

```xml
<circle cx="150" cy="50" r="18" fill="url(#nodeBlue)"/>
<text x="150" y="55" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">1</text>
```

#### 사각형 박스 (프레임, 블록)

```xml
<rect x="20" y="30" width="120" height="35" rx="5" fill="url(#nodeBlue)"/>
<text x="80" y="53" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">텍스트</text>
```

#### 연결선

```xml
<!-- 일반 선 -->
<line x1="50" y1="50" x2="150" y2="50" stroke="#7F8C8D" stroke-width="2"/>

<!-- 화살표 선 -->
<line x1="50" y1="50" x2="150" y2="50" stroke="#7F8C8D" stroke-width="2" marker-end="url(#arrowhead)"/>

<!-- 점선 -->
<line x1="50" y1="50" x2="150" y2="50" stroke="#BDC3C7" stroke-width="2" stroke-dasharray="5,5"/>
```

#### 텍스트

```xml
<!-- 타이틀 -->
<text x="200" y="25" text-anchor="middle" fill="#2C3E50" font-family="Arial, sans-serif" font-size="14" font-weight="bold">제목</text>

<!-- 부제 -->
<text x="200" y="40" text-anchor="middle" fill="#7F8C8D" font-family="Arial, sans-serif" font-size="10">부제목</text>

<!-- 레이블 -->
<text x="100" y="80" fill="#7F8C8D" font-family="Arial, sans-serif" font-size="9">레이블</text>
```

---

## 다이어그램 유형별 템플릿

### 1. 트리 다이어그램

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200">
  <defs>
    <linearGradient id="nodeBlue" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3498DB"/>
      <stop offset="100%" style="stop-color:#2980B9"/>
    </linearGradient>
  </defs>

  <!-- 간선 먼저 그리기 -->
  <line x1="150" y1="35" x2="80" y2="85" stroke="#7F8C8D" stroke-width="2"/>
  <line x1="150" y1="35" x2="220" y2="85" stroke="#7F8C8D" stroke-width="2"/>

  <!-- 노드 그리기 -->
  <circle cx="150" cy="25" r="18" fill="url(#nodeBlue)"/>
  <text x="150" y="30" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">1</text>
</svg>
```

### 2. 계층 테이블 (OSI 스타일)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 200">
  <defs>
    <linearGradient id="layer1" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#E74C3C"/>
      <stop offset="100%" style="stop-color:#C0392B"/>
    </linearGradient>
  </defs>

  <!-- 타이틀 -->
  <text x="250" y="20" text-anchor="middle" fill="#2C3E50" font-family="Arial, sans-serif" font-size="14" font-weight="bold">계층 구조</text>

  <!-- 행 -->
  <rect x="20" y="35" width="40" height="25" fill="url(#layer1)" rx="3"/>
  <text x="40" y="52" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="11" font-weight="bold">1</text>
</svg>
```

### 3. 시퀀스/핸드셰이크 다이어그램

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300">
  <defs>
    <linearGradient id="clientGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3498DB"/>
      <stop offset="100%" style="stop-color:#2980B9"/>
    </linearGradient>
    <marker id="arrowR" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#E74C3C"/>
    </marker>
  </defs>

  <!-- 엔티티 -->
  <rect x="80" y="40" width="80" height="30" fill="url(#clientGrad)" rx="5"/>
  <text x="120" y="60" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Client</text>

  <!-- 세로선 -->
  <line x1="120" y1="70" x2="120" y2="280" stroke="#3498DB" stroke-width="3"/>

  <!-- 메시지 화살표 -->
  <line x1="120" y1="100" x2="370" y2="100" stroke="#E74C3C" stroke-width="2" marker-end="url(#arrowR)"/>
  <rect x="200" y="85" width="100" height="22" fill="#E74C3C" rx="3"/>
  <text x="250" y="100" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="10" font-weight="bold">SYN</text>
</svg>
```

### 4. 아키텍처/시스템 구성도

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="lbGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#E74C3C"/>
      <stop offset="100%" style="stop-color:#C0392B"/>
    </linearGradient>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#7F8C8D"/>
    </marker>
  </defs>

  <!-- Load Balancer -->
  <rect x="200" y="50" width="200" height="40" fill="url(#lbGrad)" rx="5"/>
  <text x="300" y="75" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Load Balancer</text>

  <!-- 화살표 -->
  <line x1="300" y1="90" x2="300" y2="130" stroke="#7F8C8D" stroke-width="2" marker-end="url(#arrow)"/>
</svg>
```

### 5. 상태 다이어그램 (서킷브레이커 스타일)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 280">
  <defs>
    <linearGradient id="closedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#2ECC71"/>
      <stop offset="100%" style="stop-color:#27AE60"/>
    </linearGradient>
    <linearGradient id="openGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#E74C3C"/>
      <stop offset="100%" style="stop-color:#C0392B"/>
    </linearGradient>
  </defs>

  <!-- 상태 원 -->
  <circle cx="100" cy="100" r="45" fill="url(#closedGrad)"/>
  <text x="100" y="105" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="11" font-weight="bold">Closed</text>

  <!-- 전이 화살표 (곡선) -->
  <path d="M 145 85 Q 225 40 305 85" fill="none" stroke="#E74C3C" stroke-width="2"/>
</svg>
```

---

## 작성 절차

1. **다이어그램 유형 결정**: 표현하려는 내용에 맞는 템플릿 선택
2. **SVG 파일 생성**: `docs/career/portfolio/images/{diagram-name}.svg`
3. **마크다운에서 참조**: `![설명](./images/{diagram-name}.svg)`
4. **git add 실행**

## 주의사항

1. **파일명**: kebab-case 사용 (예: `data-pipeline-after.svg`)
2. **위치**: `docs/career/portfolio/images/` 폴더에 저장
3. **폰트**: Arial, sans-serif 사용 (크로스 플랫폼 호환)
4. **viewBox**: 컨텐츠 크기에 맞게 조정
5. **그라디언트**: 계층/중요도에 따라 색상 구분
6. **간선**: 노드보다 먼저 그리기 (노드 아래에 위치)
7. **텍스트 크기**: 타이틀 14px, 본문 11-12px, 레이블 9-10px

---

## 체크리스트

- [ ] 다이어그램 유형이 목적에 적합한가?
- [ ] 파일명이 kebab-case인가?
- [ ] 색상 팔레트를 일관되게 사용했는가?
- [ ] 그라디언트가 올바르게 정의되었는가?
- [ ] 텍스트가 가독성 있는 크기인가?
- [ ] viewBox가 컨텐츠에 맞게 설정되었는가?
- [ ] SVG 파일이 `images/` 폴더에 있는가?
- [ ] 마크다운에서 올바르게 참조했는가?
- [ ] git add 실행했는가?

---

## 관련 스킬

- `/write-portfolio`: 포트폴리오 작성 (아키텍처 다이어그램 포함)
- `/mermaid-diagram`: Mermaid 기반 다이어그램 (플로우차트, 시퀀스)
- `/export`: PDF 내보내기
