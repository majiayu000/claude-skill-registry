---
name: create-component-with-popup
description: Shadow DOM 팝업을 가진 컴포넌트를 생성합니다. 컴포넌트가 직접 데이터를 fetch하고 팝업으로 표시합니다. 3D 씬, 독립 위젯 등에 사용합니다.
---

# 팝업 컴포넌트 생성

컴포넌트가 직접 데이터를 fetch하고 Shadow DOM 팝업으로 표시합니다.

> 기본 원칙은 [create-standard-component](/.claude/skills/2-component/create-standard-component/SKILL.md) 참조

---

## ⚠️ 작업 전 필수 확인

**코드 작성 전 반드시 다음 파일들을 Read 도구로 읽으세요.**
**이전에 읽었더라도 매번 다시 읽어야 합니다 - 캐싱하거나 생략하지 마세요.**

1. [/RNBT_architecture/README.md](/RNBT_architecture/README.md) - 아키텍처 이해
2. [/.claude/guides/CODING_STYLE.md](/.claude/guides/CODING_STYLE.md) - 코딩 스타일
3. [/RNBT_architecture/Utils/PopupMixin.js](/RNBT_architecture/Utils/PopupMixin.js) - PopupMixin API

---

## 일반 vs 팝업 컴포넌트

| 구분 | 일반 컴포넌트 | 팝업 컴포넌트 |
|------|--------------|--------------|
| 데이터 | GlobalDataPublisher | Wkit.fetchData |
| 구독 | `subscriptions` | `datasetInfo` |
| 팝업 | 선택적 | **필수** |

---

## 핵심 원칙

### 데이터 흐름

```
페이지 → @assetClicked 이벤트 수신 → source.showDetail() 호출
컴포넌트 → showPopup() → fetchData() → render functions
```

- **팝업이 있을 때만** 컴포넌트의 직접 fetch 허용

---

## 필수 구성

| 구성 | 설명 |
|------|------|
| `applyShadowPopupMixin` | Shadow DOM 팝업 |
| `datasetInfo` | fetch할 데이터 정의 |
| `applyEChartsMixin` | 차트 시 (옵션) |
| `applyTabulatorMixin` | 테이블 시 (옵션) |

---

## 출력 구조

```
components/[ComponentName]/
├── views/component.html       # 팝업 템플릿 (<template id="popup-xxx">)
├── styles/component.css
├── scripts/
│   ├── register.js
│   └── beforeDestroy.js       # destroyPopup() 호출
├── preview.html
└── README.md
```

---

## 관련 자료

> beforeDestroy에서 `destroyPopup()` 필수

| 참조 | 위치 |
|------|------|
| UPS (기본) | [/RNBT_architecture/Projects/ECO/page/components/UPS/](/RNBT_architecture/Projects/ECO/page/components/UPS/) |
| PDU (탭 UI + 테이블) | [/RNBT_architecture/Projects/ECO/page/components/PDU/](/RNBT_architecture/Projects/ECO/page/components/PDU/) |
| CRAC (듀얼 Y축 차트) | [/RNBT_architecture/Projects/ECO/page/components/CRAC/](/RNBT_architecture/Projects/ECO/page/components/CRAC/) |
