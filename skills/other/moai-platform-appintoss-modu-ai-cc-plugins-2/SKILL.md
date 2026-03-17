---
name: moai-platform-appintoss
description: "앱인토스(Apps in Toss) 미니앱 개발 전문가. WebView/React Native SDK, 토스 로그인/결제, 푸시 알림, 광고 통합을 다룹니다. 토스 앱 내 미니앱 개발, Granite 프레임워크 사용, 토스페이 결제 연동 시 사용하세요."
version: 2.2.0
category: platform
modularized: true
user-invocable: false
tags: ["appintoss", "앱인토스", "toss", "토스", "miniapp", "미니앱", "granite", "webview", "react-native", "토스페이", "unity", "cocos", "game", "게임"]
related-skills: moai-lang-typescript, moai-domain-frontend, moai-domain-backend, moai-domain-uiux
updated: 2026-01-19
status: active
allowed-tools: Read, Write, Bash, Grep, Glob
triggers:
  keywords: ["appintoss", "앱인토스", "toss", "토스", "미니앱", "miniapp", "granite", "webview", "react-native", "토스페이", "toss pay", "intoss", "unity webgl", "cocos creator", "토스게임"]
modules:
  - modules/getting-started.md
  - modules/development.md
  - modules/authentication.md
  - modules/payment.md
  - modules/marketing.md
  - modules/launch.md
  - modules/monetization.md
  - modules/unity-guide.md
  - modules/cocos-guide.md
  - modules/tds-mobile.md
  - modules/tds-react-native.md
  - modules/examples-index.md
  - design-guide.md
  - reference.md
---

# moai-platform-appintoss: 앱인토스 미니앱 개발 전문가

앱인토스(Apps in Toss)는 파트너사가 개발한 서비스를 토스 앱 내부에서 App-in-App 형태로 제공하는 플랫폼입니다. 3,000만 토스 사용자에게 서비스를 노출할 수 있습니다.

---

## Quick Reference

### 플랫폼 개요

- **지원 OS:** Android 7+, iOS 16+
- **사용자:** 만 19세 이상
- **개발 방식:** WebView (Vite+React+TS) 또는 React Native (Granite)

### 핵심 기능

| 기능 | 설명 |
|------|------|
| 토스 로그인 | OAuth2 기반 사용자 인증 |
| 토스페이 | mTLS 인증 기반 결제 시스템 |
| 인앱 결제 | App Store / Google Play IAP |
| 푸시 알림 | 프로모션/기능성 메시지 |
| 광고 | 전면 광고, 보상형 광고 |
| 프로모션 | 토스 포인트 리워드 |

### 빠른 시작

**WebView 프로젝트:**

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @apps-in-toss/web-framework @toss/tds-mobile
npx ait init
```

**React Native (Granite) 프로젝트:**

```bash
npm create granite-app
cd my-granite-app
npm install @apps-in-toss/framework @toss/tds-react-native
npx ait init
```

### API Base URLs

| 서비스 | URL |
|--------|-----|
| 로그인/메시징 | https://apps-in-toss-api.toss.im |
| 결제 | https://pay-apps-in-toss-api.toss.im |
| 인증 | https://cert.toss.im |

---

## Module Index

이 스킬은 모듈화된 구조로 구성되어 있습니다. 상세 내용은 각 모듈을 참조하세요.

### 시작하기
- [modules/getting-started.md](modules/getting-started.md) - 플랫폼 개요, 온보딩, 요구사항, 주의사항

### 개발
- [modules/development.md](modules/development.md) - WebView/React Native 설정, 디버깅, 클라이언트 설정, 테스트

### 인증
- [modules/authentication.md](modules/authentication.md) - 토스 로그인, 게임 로그인, 토스 인증 (OAuth2, API)

### 결제
- [modules/payment.md](modules/payment.md) - 토스페이, 인앱 결제, mTLS 인증서

### 마케팅
- [modules/marketing.md](modules/marketing.md) - 푸시 알림, 광고, 프로모션, 게임센터, 애널리틱스

### 출시
- [modules/launch.md](modules/launch.md) - 검수 프로세스, 체크리스트, 다크패턴 방지

### 수익화
- [modules/monetization.md](modules/monetization.md) - 수익 구조, 정산, Biz Wallet

### 게임 개발
- [modules/unity-guide.md](modules/unity-guide.md) - Unity WebGL 미니앱 개발 가이드
- [modules/cocos-guide.md](modules/cocos-guide.md) - Cocos Creator 미니앱 개발 가이드

### TDS (Toss Design System)
- [modules/tds-mobile.md](modules/tds-mobile.md) - TDS Mobile (WebView용) 컴포넌트 가이드
- [modules/tds-react-native.md](modules/tds-react-native.md) - TDS React Native (Granite용) 컴포넌트 가이드

### 예제 코드
- [modules/examples-index.md](modules/examples-index.md) - 공식 예제 코드 인덱스 (24+ 예제)

### 디자인
- [design-guide.md](design-guide.md) - 브랜딩, 다크패턴 방지, UX 라이팅, TDS

### API Reference
- [reference.md](reference.md) - 상세 API 문서, SDK 레퍼런스, 에러 코드

---

## 주요 SDK 버전 요구사항

| 기능 | SDK 버전 | 토스 앱 버전 |
|------|----------|-------------|
| 기본 기능 | 1.0.0+ | - |
| 인앱 광고 | 1.0.3+ | - |
| 인앱 결제 | 1.1.3+ | 5.231.0+ |
| 토스 인증 | 1.2.1+ | 5.233.0+ |
| 게임 로그인 | 1.4.0+ | 5.232.0+ |

---

## 개발 흐름

```
1. 콘솔에서 미니앱 생성
       ↓
2. 개발 환경 선택 (WebView / RN)
       ↓
3. SDK 설치 및 초기화
       ↓
4. 로컬 개발 및 테스트
       ↓
5. 샌드박스 앱에서 테스트
       ↓
6. 토스 앱에서 QR 테스트
       ↓
7. 번들 빌드 및 업로드
       ↓
8. 검수 (운영/디자인/기능/보안)
       ↓
9. 출시
```

---

## 핵심 정책

### 필수 사항

- TDS(Toss Design System) 컴포넌트 사용 필수
- 라이트 모드 전용 (다크 모드 미지원)
- 토스 로그인만 사용 (서드파티 로그인 금지)
- 토스페이/인앱결제만 사용 (다른 결제 수단 금지)
- 번들 크기 100MB 이하

### 다크패턴 금지

- 진입 시 바텀시트 즉시 표시 금지
- 뒤로가기 가로채기 금지
- 종료 옵션 없는 UI 금지
- 예상치 못한 광고 노출 금지
- 모호한 CTA 버튼 금지

---

## Works Well With

- moai-lang-typescript: TypeScript 개발 패턴
- moai-domain-frontend: React 컴포넌트 개발
- moai-domain-backend: API 서버 개발
- moai-domain-uiux: UI/UX 디자인 시스템
- moai-workflow-testing: 테스트 전략

---

## Resources

### 공식 문서
- 개발자센터: https://developers-apps-in-toss.toss.im
- SDK 레퍼런스: https://developers-apps-in-toss.toss.im/bedrock/reference
- Unity 가이드: https://developers-apps-in-toss.toss.im/unity/intro/overview.html
- TDS Mobile: https://tossmini-docs.toss.im/tds-mobile/
- TDS React Native: https://tossmini-docs.toss.im/tds-react-native/

### GitHub 예제
- 공식 예제: https://github.com/toss/apps-in-toss-examples
- Cocos 예제: https://github.com/toss/apps-in-toss-cocos-examples

### 스킬 내부 참조
- 상세 API 문서: [reference.md](reference.md)
- 디자인 가이드: [design-guide.md](design-guide.md)
- 예제 인덱스: [modules/examples-index.md](modules/examples-index.md)

---

Status: Production Ready
Version: 2.2.0
Last Updated: 2026-01-19
Platform: Apps in Toss (앱인토스)
Game Engines: Unity WebGL, Cocos Creator 3.8.7
