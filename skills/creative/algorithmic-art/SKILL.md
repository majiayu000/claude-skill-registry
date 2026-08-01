---
name: algorithmic-art
description: '> p5.js ile generative art rehberi.'
---

---
name: algorithmic_art
router_kit: FullStackKit
description: p5.js ile generative art, flow fields ve interactive visuals oluşturma rehberi.
metadata:
  skillport:
    category: design
    tags: [algorithmic art, architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - creative
---

# 🎨 Algorithmic Art

> p5.js ile generative art rehberi.

---

## 📋 Temel Yapı

```javascript
function setup() {
  createCanvas(800, 600);
  background(20);
}

function draw() {
  // Animation loop
}
```

---

## 🔧 Temel Şekiller

```javascript
// Çizgi
line(x1, y1, x2, y2);

// Dikdörtgen
rect(x, y, width, height);

// Elips
ellipse(x, y, width, height);

// Nokta
point(x, y);

// Renkler
fill(r, g, b, alpha);
stroke(r, g, b);
noFill();
noStroke();
```

---

## 🌀 Flow Fields

```javascript
let flowField = [];
let cols, rows;
let scale = 20;

function setup() {
  createCanvas(800, 600);
  cols = floor(width / scale);
  rows = floor(height / scale);

  // Create flow field
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      let angle = noise(x * 0.1, y * 0.1) * TWO_PI;
      flowField.push(p5.Vector.fromAngle(angle));
    }
  }
}
```

---

## ✨ Particle Systems

```javascript
class Particle {
  constructor() {
    this.pos = createVector(random(width), random(height));
    this.vel = createVector(0, 0);
    this.acc = createVector(0, 0);
  }

  update() {
    this.vel.add(this.acc);
    this.vel.limit(4);
    this.pos.add(this.vel);
    this.acc.mult(0);
  }

  show() {
    point(this.pos.x, this.pos.y);
  }
}
```

---

## 🎲 Seeded Randomness

```javascript
// Reproducible randomness
randomSeed(42);
noiseSeed(42);

// Perlin noise
let n = noise(x, y);

// Random range
let r = random(0, 100);
```

---

## 🖱️ Interactivity

```javascript
function mouseMoved() {
  // Mouse position: mouseX, mouseY
}

function mousePressed() {
  // Click handler
}

function keyPressed() {
  if (key === 's') {
    saveCanvas('artwork', 'png');
  }
}
```

---

### 💾 High-Res Export (Print-Ready)
```javascript
// Press 'S' to save high-res
function keyPressed() {
  if (key === 's') {
    pixelDensity(4); // 4x resolution for print
    saveCanvas('artwork_' + frameCount, 'png');
    pixelDensity(1); // Reset for performance
  }
}
```

### 🚀 Performance (Shaders)
For pixel-level manipulation, use GLSL shaders in WEBGL mode instead of `pixels[]` array for 100x speedup.

---

*Algorithmic Art v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Generative Design Process](https://www.illustration.app/blog/the-generative-design-process-from-ai-output-to-polished-visual)

### Aşama 1: Concept & Rules
- [ ] **Define Theme**: e.g., "Organic Decay", "Geometric Order".
- [ ] **Set Constraints**: Color palette (max 3 colors), Aspect ratio.
- [ ] **Choose Algorithm**: Flow fields, Cellular Automata, Recursion.

### Aşama 2: Implementation (Sketching)
- [ ] **Setup**: Configure canvas and basic loop.
- [ ] **Primitives**: Draw static shapes to test composition.
- [ ] **Dynamics**: Add movement/change (using `draw()` loop).

### Aşama 3: Generative Logic
- [ ] **Introduce Randomness**: Use `random()` inside controlled bounds.
- [ ] **Apply Noise**: Replace random with `noise()` for natural flow.
- [ ] **Interaction**: Couple variables with mouse/keyboard inputs.

### Aşama 4: Tuning & Curation
- [ ] **Parameterize**: Create variables for `scale`, `speed`, `density`.
- [ ] **Seed Testing**: Test different `randomSeed()` values.
- [ ] **Selection**: Curate the best outputs.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Konsept ve kısıtlamalar net |
| 2 | Temel döngü hatasız çalışıyor |
| 3 | Çıktı her çalıştırıldığında varyasyon gösteriyor |
| 4 | Performans stabil (>30 FPS) |
