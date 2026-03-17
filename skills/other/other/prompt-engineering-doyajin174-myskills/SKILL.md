---
name: prompt-engineering
description: Advanced prompt engineering techniques for optimal AI responses. Use this when crafting prompts, optimizing AI interactions, or designing system prompts for applications.
allowed-tools: Read, Glob, Grep, Edit, Write
license: MIT
metadata:
  author: NeoLabHQ
  version: "1.0"
---

# Prompt Engineering

효과적인 프롬프트 작성을 위한 고급 기법 가이드입니다.

## Core Principles

### 1. Clarity (명확성)

```
❌ "코드 좀 고쳐줘"
✅ "auth.js의 validateToken 함수에서 만료된 토큰 처리 시
    발생하는 TypeError를 수정해주세요"
```

### 2. Context (맥락)

```
❌ "이 에러 해결해줘: TypeError"
✅ "Node.js 18, Express 4 환경에서 JWT 검증 시
    다음 에러 발생: TypeError: Cannot read property 'exp' of undefined
    관련 코드: [코드 첨부]"
```

### 3. Specificity (구체성)

```
❌ "좋은 API 만들어줘"
✅ "다음 요구사항의 REST API 설계:
    - 리소스: 사용자, 게시물
    - 인증: JWT Bearer
    - 페이지네이션: cursor 기반
    - 응답 형식: JSON:API 스펙"
```

## Prompting Techniques

### Zero-Shot Prompting

```
직접 지시만으로 결과 도출

예: "다음 텍스트의 감정을 분석하세요: [텍스트]"
```

### Few-Shot Prompting

```
예시를 통한 패턴 학습

예시 1: 입력 → 출력
예시 2: 입력 → 출력
---
실제 입력 → ?
```

### Chain-of-Thought (CoT)

```
단계별 추론 유도

"단계별로 생각해보세요:
1. 먼저 문제를 분석합니다
2. 가능한 해결책을 나열합니다
3. 각 해결책의 장단점을 평가합니다
4. 최적의 해결책을 선택합니다"
```

### Role Prompting

```
특정 역할 부여

"당신은 10년 경력의 시니어 백엔드 개발자입니다.
코드 리뷰 관점에서 다음 코드를 평가해주세요..."
```

## Prompt Structure

### 기본 구조

```markdown
## Role (역할)
[AI가 수행할 역할 정의]

## Context (맥락)
[배경 정보, 제약 조건]

## Task (작업)
[구체적인 요청 사항]

## Format (형식)
[원하는 출력 형식]

## Examples (예시) - 선택적
[입출력 예시]
```

### 코드 관련 프롬프트

```markdown
## 환경
- 언어/프레임워크: [명시]
- 버전: [명시]
- 관련 의존성: [명시]

## 현재 상태
[현재 코드 또는 상황]

## 목표
[달성하려는 결과]

## 제약 조건
- [제약 1]
- [제약 2]
```

## Anti-Patterns

### 피해야 할 패턴

| 안티패턴 | 문제점 | 개선 |
|----------|--------|------|
| 모호한 요청 | 해석의 여지가 많음 | 구체적 조건 명시 |
| 과도한 정보 | 핵심이 묻힘 | 관련 정보만 포함 |
| 부정형 지시 | "~하지 마세요" | "~해주세요" 로 변경 |
| 열린 결말 | 범위가 무한함 | 범위와 제약 명시 |

### 예시

```
❌ "이상한 코드 패턴 사용하지 마세요"
✅ "ESLint 규칙을 따르고, 함수는 20줄 이내로 작성해주세요"

❌ "좋은 성능으로 만들어주세요"
✅ "응답 시간 100ms 이내, 메모리 사용 512MB 이하로 최적화해주세요"
```

## System Prompt Design

### 구조

```markdown
# Identity
[AI의 정체성과 목적]

# Capabilities
[할 수 있는 것]

# Constraints
[제한 사항]

# Response Format
[응답 형식 규칙]

# Examples
[대표적인 상호작용 예시]
```

### 예시: 코드 리뷰 봇

```markdown
# Identity
당신은 코드 품질 향상을 돕는 시니어 개발자입니다.

# Capabilities
- 코드 스타일 검토
- 버그 탐지
- 성능 개선 제안
- 보안 취약점 식별

# Constraints
- 개인적 스타일 강요 금지
- 프로젝트 컨벤션 우선
- 건설적 피드백만 제공

# Response Format
## 요약
[한 줄 요약]

## 주요 발견
- [이슈 1]: [설명] → [제안]

## 긍정적 측면
- [잘한 점]
```

## Iteration Strategies

```
1. 초기 프롬프트 작성
2. 결과 평가
3. 문제점 식별:
   - 불완전한 응답 → 더 구체적인 지시 추가
   - 잘못된 방향 → 제약 조건 강화
   - 형식 불일치 → 예시 추가
4. 프롬프트 수정
5. 반복
```
