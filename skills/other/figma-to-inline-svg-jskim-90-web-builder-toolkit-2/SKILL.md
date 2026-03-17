---
name: figma-to-inline-svg
description: Figma 디자인을 인라인 SVG가 포함된 정적 HTML/CSS로 변환합니다. 런타임에서 색상 제어가 필요한 심볼/아이콘용입니다. Use when converting Figma SVG designs to inline SVG HTML for runtime color control, symbol state components, or icon theming.
---

# Figma to Inline SVG 변환

Figma 디자인을 **인라인 SVG가 포함된 정적 HTML/CSS**로 변환하는 Skill입니다.
런타임에서 색상 제어가 필요한 심볼, 아이콘, 상태 표시 컴포넌트용입니다.
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

## figma-to-html과의 차이점

| 구분 | figma-to-html | figma-to-inline-svg |
|------|---------------|---------------------|
| **SVG 처리** | `<img src="./assets/...">` | `<svg>...</svg>` 인라인 |
| **용도** | 일반 이미지/아이콘 | 런타임 색상 제어 필요 |
| **후속 작업** | create-standard-component | create-symbol-state-component |
| **색상** | 원본 유지 | 원본 유지 (CSS 변수 변환은 다음 단계) |

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
   │  └─ 에셋 자동 다운로드 + 코드 반환
   └─ get_screenshot
      └─ Figma 원본 스크린샷 (비교 기준)

3. 에셋 폴더에서 SVG 파일 읽기
   └─ 다운로드된 SVG 파일 내용 확인

4. HTML에 인라인 SVG 삽입
   └─ <img> 대신 <svg> 태그로 직접 삽입

5. CSS 작성
   └─ 컨테이너 스타일, SVG 크기 조정

6. Playwright 스크린샷 캡처
   - viewport를 Figma 프레임 크기와 동일하게 설정

7. 시각적 비교
   ├─ get_screenshot 결과 (원본)
   └─ Playwright 스크린샷 (구현물)

8. 완료 판단
   └─ 원본과 구현물이 시각적으로 일치할 때만 완료
```

---

## MCP 도구 사용

### 디자인 정보 + 에셋 다운로드

```javascript
mcp__figma-desktop__get_design_context({
  nodeId: "1:140",
  clientLanguages: "html,css",
  clientFrameworks: "vanilla",
  dirForAssetWrites: "./Figma_Conversion/Static_Components/[프로젝트명]/[컴포넌트명]/assets"
})
```

**필수**: `dirForAssetWrites` 파라미터로 에셋 자동 저장

### 원본 스크린샷 (비교 기준)

```javascript
mcp__figma-desktop__get_screenshot({ nodeId: "1:140" })
```

---

## 출력 폴더 구조

```
Figma_Conversion/Static_Components/
└── [프로젝트명]/
    └── [컴포넌트명]/
        ├── assets/              # SVG 에셋 (자동 다운로드)
        │   └── xxxxxxxx.svg     # 해시 파일명
        ├── screenshots/         # 구현물 스크린샷
        │   └── impl.png
        ├── [컴포넌트명].html    # 인라인 SVG 포함
        └── [컴포넌트명].css
```

---

## 핵심 규칙

### 1. SVG 인라인 삽입 방법

```html
<!-- ❌ figma-to-html 방식 (img 태그) -->
<div id="component-container">
    <img src="./assets/abc123.svg" alt="symbol">
</div>

<!-- ✅ figma-to-inline-svg 방식 (인라인 SVG) -->
<div id="component-container">
    <svg class="symbol-svg" viewBox="0 0 73 54" preserveAspectRatio="none">
        <!-- SVG 파일 내용 그대로 삽입 -->
        <path d="..." fill="#4ADE80"/>
        <path d="..." stroke="#16A34A"/>
    </svg>
</div>
```

### 2. SVG 파일 읽기 후 삽입

```
1. get_design_context로 에셋 다운로드
2. assets/ 폴더의 SVG 파일 읽기 (Read 도구)
3. SVG 내용에서 불필요한 부분 제거:
   - <?xml ...?> 선언
   - <!DOCTYPE ...> 선언
   - xmlns 속성은 유지
4. <svg> 태그에 class 추가
5. HTML에 인라인으로 삽입
```

### 3. CSS 원칙

**[CODING_STYLE.md](/.claude/guides/CODING_STYLE.md)의 CSS 원칙 섹션 참조**

핵심 요약:
- **px 단위 사용** (rem/em 금지) - RNBT 런타임 호환성 보장
- **Flexbox 우선** (Grid는 2D 카드 레이아웃 등 명확한 경우만 허용, absolute 지양)

### 4. 인라인 SVG CSS 스타일

```css
#component-container {
    width: 73px;   /* Figma 프레임 크기 */
    height: 54px;
    position: relative;
}

.symbol-svg {
    display: block;
    width: 100%;
    height: 100%;
}
```

### 5. 색상 유지 원칙

**이 단계에서는 색상을 원본 그대로 유지합니다.**

```html
<!-- ✅ 원본 색상 그대로 (하드코딩) -->
<path d="..." fill="#4ADE80"/>
<path d="..." stroke="#16A34A"/>

<!-- ❌ CSS 변수 변환은 이 단계에서 하지 않음 -->
<path d="..." fill="var(--fill-primary)"/>
```

**이유**: 정적/동적 작업 분리 원칙
- figma-to-inline-svg: 정적 퍼블리싱 (색상 원본 유지)
- create-symbol-state-component: 동적 변환 (CSS 변수화)

### 6. 추측 금지 원칙

```
❌ 잘못된 접근:
- "이 정도면 비슷해 보이니까 완료"
- "대충 이 값이면 맞겠지"
- CSS 값을 "추측"해서 조정

✅ 올바른 접근:
- get_screenshot → 유일한 원본
- get_design_context → 정확한 구조와 수치
- SVG 파일 내용 그대로 사용
- 시각적 차이가 있으면 MCP 데이터 다시 확인
```

---

## Playwright 스크린샷

```javascript
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 73, height: 54 }  // Figma 프레임 크기와 동일
  });
  await page.goto('file:///path/to/component.html');
  await page.screenshot({ path: './screenshots/impl.png' });
  await browser.close();
})();
"
```

**주의**: viewport 크기를 Figma metadata의 프레임 크기와 정확히 일치시킬 것

---

## 여러 상태의 색상 추출

심볼이 여러 상태(green, yellow, red 등)를 가질 때:

```
1. 각 상태의 Figma node-id 확인
   - green: 1:102
   - yellow: 1:178
   - red: 1:140

2. 각 node-id에서 get_design_context 호출
   └─ 색상 정보 추출

3. 색상 정보 문서화 (README.md 또는 주석)
   - 어떤 색상이 어떤 상태인지 기록
   - 다음 단계(create-symbol-state-component)에서 사용
```

**예시: 색상 정보 기록**

```javascript
/*
 * 상태별 색상 (Figma에서 추출)
 *
 * green (1:102):
 *   - fillPrimary: #4ADE80
 *   - strokeColor: #16A34A
 *
 * yellow (1:178):
 *   - fillPrimary: #FACC15
 *   - strokeColor: #CA8A04
 *
 * red (1:140):
 *   - fillPrimary: #EF4444
 *   - strokeColor: #DC2626
 */
```

---

## 금지 사항

```
❌ 추측하지 않는다
- "비슷해 보인다" ≠ "일치한다"
- 확인하지 않고 완료라고 말하지 않음

❌ CSS 변수로 변환하지 않는다
- 이 단계에서는 원본 색상 유지
- CSS 변수 변환은 create-symbol-state-component에서

❌ 스크립트 작성하지 않는다
- 이 단계는 순수 퍼블리싱
- JavaScript는 다음 단계에서

❌ 로컬호스트 URL 직접 사용
- http://127.0.0.1:3845/... URL을 HTML에 직접 사용

❌ SVG 내용 임의 수정
- Figma에서 제공된 path, fill, stroke 그대로 사용
- viewBox 등 필수 속성만 조정

❌ 스크린샷 비교 생략
- 매번 get_screenshot과 Playwright 결과 비교 필수
```

---

## 완료 체크리스트

```
- [ ] Figma 원본 스크린샷 확보 (get_screenshot)
- [ ] 에셋 자동 다운로드 완료 (dirForAssetWrites)
- [ ] SVG 파일 읽기 완료
- [ ] SVG를 인라인으로 HTML에 삽입
- [ ] 컨테이너 크기가 Figma와 일치
- [ ] SVG 색상 원본 유지 (하드코딩)
- [ ] Playwright 스크린샷 캡처 완료
- [ ] Figma 원본과 구현물 시각적 비교 완료
- [ ] 차이점 없음 확인
- [ ] (여러 상태일 경우) 색상 정보 문서화
```

---

## 다음 단계

변환이 완료되면 **create-symbol-state-component** Skill을 사용하여
인라인 SVG HTML을 상태 기반 동적 컴포넌트로 변환할 수 있습니다.

```
figma-to-inline-svg (정적)
    │
    │  인라인 SVG HTML/CSS
    │  + 색상 정보 문서화
    │
    ▼
create-symbol-state-component (동적)
    - 하드코딩 색상 → CSS 변수
    - 상태별 색상 클래스
    - 런타임 API (setStatus 등)
```

---

## 참고 문서

| 문서 | 참고 시점 | 내용 |
|------|----------|------|
| [CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) | 코드 작성 시 | CSS 원칙 |
| [figma-to-html/SKILL.md](/.claude/skills/1-figma/figma-to-html/SKILL.md) | MCP 사용법 참고 시 | 기본 워크플로우 |

## 참고 예제

| 예제 | 참고 시점 | 특징 |
|------|----------|------|
| [/Figma_Conversion/Static_Components/Symbol_Test/symbol-1-198/](/Figma_Conversion/Static_Components/Symbol_Test/symbol-1-198/) | 인라인 SVG 예제 | 3D 큐브 심볼 |
