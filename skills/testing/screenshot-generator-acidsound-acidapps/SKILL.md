---
name: screenshot-generator
description: Generate screenshots for web audio apps (desktop, mobile landscape, mobile portrait) using Playwright. Also captures component-level screenshots for documentation.
---

# 📸 Screenshot Generator Skill

웹 앱의 스크린샷을 자동으로 생성합니다.

## 🎯 용도

- README.md 및 문서용 스크린샷 생성
- Desktop, Mobile Landscape, Mobile Portrait 뷰 캡처
- 개별 컴포넌트(헤더, 패드, 노브 등) 스크린샷

## 📁 파일 구조

```
screenshot-generator/
├── SKILL.md              # 이 파일
└── scripts/
    └── generate_screenshots.js  # 메인 스크립트
```

## ⚙️ 요구사항

```bash
# Playwright 설치
npm install playwright
npx playwright install chromium
```

## 🚀 사용법

### 기본 실행

```bash
# 프로젝트 루트에서
node scripts/generate_screenshots.js
```

### 스크립트 동작

1. **로컬 서버 시작**: `http-server`로 앱 서빙 (포트 8080)
2. **브라우저 실행**: Playwright Chromium
3. **스크린샷 캡처**:
   - `screenshot-desktop.png` (1280x800)
   - `screenshot-mobile-landscape.png` (844x390)
   - `screenshot-mobile-portrait.png` (iPhone 13 Pro)
4. **컴포넌트 캡처**: 개별 UI 요소
5. **서버 종료**

### 출력 위치

스크린샷은 `assets/` 폴더에 저장됩니다.

## 🔧 프로젝트별 커스터마이징

각 프로젝트에서 스크립트를 복사하고 필요에 맞게 수정하세요:

### 필수 수정 사항

```javascript
// 1. 서버 포트 (필요시)
const server = spawn('npx', ['-y', 'http-server', '-p', '8080', '-a', '127.0.0.1']);

// 2. 대기할 UI 요소 (프로젝트별로 다름)
await page.waitForSelector('.your-main-element', { timeout: 10000 });

// 3. 컴포넌트 셀렉터 (프로젝트별로 다름)
const header = page.locator('.your-header-class');
await header.screenshot({ path: path.join(assetsDir, 'header.png') });
```

### 새 스크린샷 추가

```javascript
// 스크립트 하단에 추가
console.log('Taking New Feature Screenshot...');
const newFeature = page.locator('.your-selector');
await newFeature.screenshot({ path: path.join(assetsDir, 'new-feature.png') });
```

## 📋 프로젝트별 설정 예시

### acidBros
```javascript
// 대기할 요소
await page.waitForSelector('.step-303', { timeout: 10000 });
await page.waitForSelector('.step-909', { timeout: 10000 });
await page.waitForSelector('.rotary-knob', { timeout: 10000 });

// 컴포넌트
const transport = page.locator('.top-bar');
const tb303 = page.locator('.machine.tb-303').first();
const tr909 = page.locator('.machine.tr-909');
```

### ddxx7
```javascript
// 대기할 요소
await page.waitForSelector('.operator-panel', { timeout: 10000 });
await page.waitForSelector('.algorithm-matrix', { timeout: 10000 });

// 컴포넌트
const header = page.locator('header');
const operatorPanel = page.locator('.operator-panel');
const libraryView = page.locator('.library-view');
```

### uss44
```javascript
// 대기할 요소
await page.waitForSelector('.pad-grid', { timeout: 10000 });
await page.waitForSelector('.waveform-editor', { timeout: 10000 });

// 컴포넌트
const header = page.locator('header');
const padGrid = page.locator('.pad-grid');
const paramsPanel = page.locator('.params-panel');
```

## ⚠️ 주의사항

1. **서버 충돌**: 이미 8080 포트가 사용 중이면 실패
2. **타임아웃**: 네트워크 느리면 waitForSelector 타임아웃 증가 필요
3. **헤드리스**: 기본적으로 headless 모드 (화면 표시 없음)

## 🔗 관련 문서

- [Playwright 문서](https://playwright.dev/docs/intro)
- [Device descriptors](https://playwright.dev/docs/emulation#devices)
