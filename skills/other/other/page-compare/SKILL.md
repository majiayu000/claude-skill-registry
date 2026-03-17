---
name: page-compare
description: 여러 웹 페이지의 스크린샷을 찍어 시각적으로 동일한지 비교. 페이지 비교, 디자인 비교, 시각적 차이 확인 시 사용.
allowed-tools:
  - Bash(playwright-cli:*)
  - Read
---

# page-compare Skill

웹 페이지들의 스크린샷을 찍고 시각적으로 비교하여 차이점을 분석합니다.

## 사용법

```
/page-compare <URL1> <URL2> [URL3] ...
```

**예시:**
```
/page-compare https://playground-playwright-cli.vercel.app/page-a.html https://playground-playwright-cli.vercel.app/page-b.html https://playground-playwright-cli.vercel.app/page-c.html
```

## 동작 방식

1. **브라우저 실행**: `playwright-cli open` 명령으로 브라우저를 엽니다.

2. **각 페이지 스크린샷 캡처**:
   - 각 URL에 대해:
     - `playwright-cli goto <URL>` 로 페이지 이동
     - `playwright-cli screenshot --full-page --filename=page-N.png` 로 전체 페이지 스크린샷 저장
     - N은 1부터 시작하는 순번

3. **브라우저 종료**: `playwright-cli close` 로 브라우저를 닫습니다.

4. **이미지 비교 분석**:
   - `Read` 도구로 각 스크린샷 이미지 파일을 읽습니다.
   - Claude의 멀티모달 능력을 활용하여 시각적 차이를 분석합니다.

5. **결과 리포트 제공**:
   - 페이지들이 시각적으로 동일한지 또는 다른지 판단
   - 차이점이 있다면 구체적으로 설명 (레이아웃, 색상, 텍스트, 이미지 등)
   - 각 페이지의 주요 특징 요약

## 지시사항

사용자가 이 skill을 호출하면:

1. 제공된 URL 목록을 파싱합니다.
2. playwright-cli로 브라우저를 열고 각 URL의 스크린샷을 캡처합니다.
3. 모든 스크린샷 이미지를 읽어서 시각적으로 비교합니다.
4. 다음 형식으로 결과를 보고합니다:

```
## 페이지 비교 결과

### 캡처된 페이지
- 페이지 1: <URL1>
- 페이지 2: <URL2>
- 페이지 3: <URL3> (있는 경우)

### 시각적 비교 분석
[각 페이지의 주요 시각적 특징 설명]

### 동일성 판단
- **결과**: 동일함 / 차이 있음
- **차이점** (있는 경우):
  - 레이아웃: [설명]
  - 색상/스타일: [설명]
  - 콘텐츠: [설명]
  - 기타: [설명]

### 요약
[전체 비교 결과 요약]
```

## 참고사항

- 스크린샷은 현재 작업 디렉토리에 저장됩니다.
- `--full-page` 옵션을 사용하여 페이지 전체를 캡처합니다 (viewport만이 아닌).
- 페이지 로딩 시간을 고려하여 스크린샷 전에 충분한 대기 시간을 둘 수 있습니다.
- 동적 콘텐츠(애니메이션, 타임스탬프 등)로 인한 사소한 차이는 무시하고 주요 시각적 차이에 집중합니다.
