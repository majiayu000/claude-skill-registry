---
name: algorithmic-art
description: Create generative art using p5.js with seeded randomness. Use this when creating procedural art, interactive visualizations, or algorithmic designs.
allowed-tools: Read, Glob, Grep, Edit, Write
license: MIT
metadata:
  author: anthropics
  version: "1.0"
---

# Algorithmic Art

p5.js를 사용한 제너러티브 아트 생성 가이드입니다.

## Two-Phase Process

### Phase 1: Algorithmic Philosophy

```
1. 제너러티브 무브먼트 명명 (예: "Organic Turbulence")
2. 4-6 문단의 계산적 미학 선언문 작성
3. 수학적 프로세스, 노이즈 필드, 창발적 행동 강조
4. "meticulously crafted algorithm" 강조
```

### Phase 2: P5.js Implementation

```
1. viewer.html 템플릿 기반
2. 자체 포함 HTML artifact 생성
3. Seeded randomness로 재현성 확보
4. 사이드바 컨트롤 구현
```

## HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
  <style>
    /* Anthropic 브랜딩 스타일 */
    body { font-family: 'Poppins', sans-serif; }
    .sidebar { /* 사이드바 스타일 */ }
    .canvas-container { /* 캔버스 컨테이너 */ }
  </style>
</head>
<body>
  <div class="sidebar">
    <!-- 시드 컨트롤 -->
    <!-- 파라미터 슬라이더 -->
    <!-- 액션 버튼 -->
  </div>
  <div class="canvas-container"></div>
  <script>
    // p5.js 스케치
  </script>
</body>
</html>
```

## Fixed Elements (변경 금지)

| 요소 | 설명 |
|------|------|
| Anthropic 브랜딩 | Poppins/Lora 폰트, 라이트 테마 |
| 사이드바 구조 | 레이아웃 유지 |
| 시드 컨트롤 | Previous/Next/Random/Jump |
| 액션 버튼 | Regenerate/Reset/Download |

## Variable Elements (커스터마이즈)

| 요소 | 설명 |
|------|------|
| p5.js 알고리즘 | 완전히 새로 작성 |
| 파라미터 정의 | 철학에서 도출 |
| UI 컨트롤 | 슬라이더, 체크박스 등 |
| 컬러 섹션 | 선택적 |

## Core Patterns

### Seeded Randomness

```javascript
let seed = 12345;

function setup() {
  createCanvas(800, 600);
  randomSeed(seed);
  noiseSeed(seed);
}

function regenerate() {
  randomSeed(seed);
  noiseSeed(seed);
  redraw();
}

function nextSeed() {
  seed++;
  regenerate();
}
```

### Noise Field

```javascript
function draw() {
  for (let x = 0; x < width; x += 10) {
    for (let y = 0; y < height; y += 10) {
      let n = noise(x * 0.01, y * 0.01);
      let angle = n * TWO_PI * 2;

      push();
      translate(x, y);
      rotate(angle);
      line(0, 0, 10, 0);
      pop();
    }
  }
}
```

### Particle System

```javascript
class Particle {
  constructor(x, y) {
    this.pos = createVector(x, y);
    this.vel = createVector(0, 0);
    this.acc = createVector(0, 0);
  }

  update() {
    this.vel.add(this.acc);
    this.pos.add(this.vel);
    this.acc.mult(0);
  }

  follow(flowfield) {
    let x = floor(this.pos.x / scale);
    let y = floor(this.pos.y / scale);
    let force = flowfield[x + y * cols];
    this.applyForce(force);
  }
}
```

## Parameter Controls

```javascript
// 사이드바 파라미터
let params = {
  complexity: 5,
  speed: 0.5,
  colorMode: 'gradient'
};

// 슬라이더 생성
function createControls() {
  createSlider(1, 10, params.complexity)
    .input(v => { params.complexity = v; regenerate(); });
}
```

## Download Functionality

```javascript
function downloadArt() {
  saveCanvas('artwork-' + seed, 'png');
}

function downloadSVG() {
  // SVG 내보내기 로직
}
```

## Philosophy Examples

### Organic Turbulence
> 유기적 난류는 자연의 혼돈 속에서 질서를 찾는다.
> Perlin 노이즈 필드가 입자들을 흐름에 따라 안내하며,
> 각 시드는 독특한 리버베드를 생성한다.

### Geometric Meditation
> 기하학적 명상은 반복되는 패턴 속 고요함을 탐구한다.
> 황금비와 피보나치 수열이 시각적 조화를 이끈다.

## Best Practices

1. **재현성**: 모든 랜덤은 시드 기반
2. **성능**: requestAnimationFrame 활용
3. **반응형**: windowResized() 구현
4. **접근성**: 키보드 네비게이션 지원
5. **내보내기**: PNG/SVG 다운로드 제공
