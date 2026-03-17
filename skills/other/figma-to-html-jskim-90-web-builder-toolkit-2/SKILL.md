---
name: figma-to-html
description: Figma 디자인을 정적 HTML/CSS로 변환합니다. Figma 링크나 node-id가 제공되면 MCP를 통해 디자인 정보를 가져와 정확한 코드를 생성합니다. Use when converting Figma designs to HTML/CSS, or when user mentions Figma links, design conversion, or static HTML implementation.
---

# Figma to HTML/CSS 변환

Figma 디자인을 **정적 HTML/CSS**로 변환하는 Skill입니다.
스크립트 작업은 하지 않습니다 (순수 퍼블리싱).

> 공통 규칙: [SHARED_INSTRUCTIONS.md](/.claude/skills/SHARED_INSTRUCTIONS.md) 참조

---

## ⚠️ 작업 전 필수 확인

**코드 작성 전 반드시 다음 파일들을 Read 도구로 읽으세요.**
**이전에 읽었더라도 매번 다시 읽어야 합니다 - 캐싱하거나 생략하지 마세요.**

1. [/.claude/skills/SHARED_INSTRUCTIONS.md](/.claude/skills/SHARED_INSTRUCTIONS.md) - 공통 규칙
2. [/Figma_Conversion/README.md](/Figma_Conversion/README.md) - 프로젝트 구조 및 시작 방법
3. [/Figma_Conversion/CLAUDE.md](/Figma_Conversion/CLAUDE.md) - 워크플로우와 규칙
4. [/.claude/guides/CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) - 코딩 스타일

---

## 사전 조건

- Figma Desktop 앱 실행 중
- 대상 Figma 파일이 열려 있음
- Figma MCP 서버 등록됨

```bash
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
```

---

## 워크플로우

```
1. Figma 링크에서 node-id 추출
   - URL의 node-id 파라미터: 25-1393 → 25:1393 (하이픈을 콜론으로)

2. MCP 도구 호출 (병렬 실행)
   ├─ get_design_context (dirForAssetWrites 필수!)
   │  └─ 에셋 자동 다운로드 + Tailwind 코드 반환
   └─ get_screenshot
      └─ Figma 원본 스크린샷 (비교 기준)

3. Tailwind → 순수 CSS 변환
   - MCP가 제공한 값 그대로 사용 (추측 금지!)

4. HTML/CSS 파일 생성
   - 에셋 경로: ./assets/파일명.svg

5. Playwright 스크린샷 캡처
   - viewport를 Figma 프레임 크기와 동일하게 설정

6. 시각적 비교
   ├─ get_screenshot 결과 (원본)
   └─ Playwright 스크린샷 (구현물)

7. 차이점 발견 시
   ├─ MCP 데이터 다시 확인
   ├─ CSS 수정 (추측 금지, 데이터 기반)
   └─ 5-6 반복

8. 완료 판단
   └─ 원본과 구현물이 시각적으로 일치할 때만 완료
```

---

## MCP 도구 사용

### 디자인 정보 + 에셋 다운로드

```javascript
mcp__figma-desktop__get_design_context({
  nodeId: "781:47496",
  clientLanguages: "html,css",
  clientFrameworks: "vanilla",
  dirForAssetWrites: "./Figma_Conversion/Static_Components/[프로젝트명]/[컴포넌트명]/assets"
})
```

**필수**: `dirForAssetWrites` 파라미터로 에셋 자동 저장

### 원본 스크린샷 (비교 기준)

```javascript
mcp__figma-desktop__get_screenshot({ nodeId: "781:47496" })
```

---

## 출력 폴더 구조

```
Figma_Conversion/Static_Components/
└── [프로젝트명]/
    └── [컴포넌트명]/
        ├── assets/              # SVG, 이미지 에셋 (자동 다운로드)
        ├── screenshots/         # 구현물 스크린샷
        │   └── impl.png
        ├── [컴포넌트명].html
        └── [컴포넌트명].css
```

---

## 핵심 규칙

### 1. CSS 원칙

**[CODING_STYLE.md](/.claude/guides/CODING_STYLE.md)의 CSS 원칙 섹션 참조**

핵심 요약:
- **px 단위 사용** (rem/em 금지) - RNBT 런타임 호환성 보장
- **Flexbox 우선** (Grid는 2D 카드 레이아웃 등 명확한 경우만 허용, absolute 지양)

---

### 2. 추측 금지 원칙

```
❌ 잘못된 접근:
- "이 정도면 비슷해 보이니까 완료"
- "대충 이 값이면 맞겠지"
- CSS 값을 "추측"해서 조정

✅ 올바른 접근:
- get_screenshot → 유일한 원본
- get_design_context → 정확한 구조와 수치
- Tailwind 클래스를 CSS로 변환할 때 값 그대로 사용
- 시각적 차이가 있으면 MCP 데이터 다시 확인
```

### 3. 에셋 규칙

| 규칙 | 설명 |
|------|------|
| 에셋 자동 다운로드 | `dirForAssetWrites` 파라미터 필수 |
| 로컬 경로 사용 | `./assets/파일명.svg` 형식 |
| localhost URL 금지 | `http://127.0.0.1:3845/...` 직접 사용 금지 |
| 외부 아이콘 금지 | 새로운 아이콘 패키지 가져오기 금지 |
| Figma 페이로드만 | Figma에서 제공된 에셋만 사용 |
| 임의 생성 금지 | Figma에 없는 에셋 만들지 않음 |

### 4. 컨테이너 구조 패턴

```html
<!-- Figma 선택 요소 = 컨테이너 -->
<div id="component-container">
  <!-- Figma 내부 구조 그대로 -->
</div>
```

**규칙:**
- 컨테이너 크기 = Figma 선택 요소 크기 (metadata에서 확인)
- Figma 스타일 그대로 유지 (임의로 100%로 변경 금지)

### 5. overflow 적용 규칙

**핵심 원칙:** 동적 데이터가 렌더링되는 영역을 파악하여 적절한 위치에 overflow 적용

**동적 데이터 영역 식별:**
- 테이블의 목록 (list, tbody)
- 카드 목록 (card-list, grid)
- 반복 렌더링되는 아이템 컨테이너

```css
/* 케이스 1: 내부 목록만 스크롤 */
.component-container {
  overflow: hidden;
}
.component__list {
  overflow-y: auto;
}

/* 케이스 2: 전체 컨테이너 스크롤 (컨테이너 자체가 동적 영역일 때) */
.component-container {
  overflow: auto;
}
```

**판단 기준:**
- 컨테이너 내에 고정 헤더/푸터가 있고 목록만 스크롤 → 목록에 overflow
- 컨테이너 전체가 스크롤 대상 → 컨테이너에 overflow

### 6. box-sizing 주의사항

```css
/* ❌ height 없으면 border가 별도 추가됨 */
.button {
    box-sizing: border-box;
    border: 1px solid #000;
    padding: 6px 15px;
}

/* ✅ height 명시하면 border가 높이에 포함됨 */
.button {
    box-sizing: border-box;
    height: 24px;  /* Figma에서 측정한 높이 명시 */
    border: 1px solid #000;
    padding: 6px 15px;
}
```

---

## Playwright 스크린샷

```javascript
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 524, height: 350 }  // Figma 프레임 크기와 동일
  });
  await page.goto('file:///path/to/component.html');
  await page.screenshot({ path: './screenshots/impl.png' });
  await browser.close();
})();
"
```

**주의**: viewport 크기를 Figma metadata의 프레임 크기와 정확히 일치시킬 것

---

## 금지 사항

```
❌ 추측하지 않는다
- "비슷해 보인다" ≠ "일치한다"
- 확인하지 않고 완료라고 말하지 않음

❌ 임의로 추가하지 않는다
- 외부 아이콘 패키지
- Figma에 없는 에셋
- 임의의 스타일

❌ 로컬호스트 URL 직접 사용
- http://127.0.0.1:3845/... URL을 HTML에 직접 사용

❌ 고정 사이즈 임의 변경
- Figma metadata에 명시된 크기 그대로 구현

❌ 스크린샷 비교 생략
- 매번 get_screenshot과 Playwright 결과 비교 필수
```

---

## 완료 체크리스트

```
- [ ] Figma 원본 스크린샷 확보 (get_screenshot)
- [ ] 에셋 자동 다운로드 완료 (dirForAssetWrites)
- [ ] 전체 컨테이너 크기가 Figma와 일치
- [ ] gap 값 정확 (row-gap ≠ column-gap 체크)
- [ ] 헤더-컨텐츠 간격 일치
- [ ] 상단/하단 여백 일치
- [ ] border 있는 요소에 height 명시
- [ ] 에셋 로컬 경로로 변환 완료
- [ ] Playwright 스크린샷 캡처 완료
- [ ] Figma 원본과 구현물 시각적 비교 완료
- [ ] 차이점 없음 확인
```

---

## 다음 단계

변환이 완료되면 **create-standard-component** Skill을 사용하여
정적 HTML/CSS를 RNBT 동적 컴포넌트로 변환할 수 있습니다.
