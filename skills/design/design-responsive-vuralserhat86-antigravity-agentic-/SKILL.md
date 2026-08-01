---
name: design-responsive
description: '> Responsive tasarım ve modern CSS özellikleri.'
---

---
name: design_responsive
router_kit: FullStackKit
description: Breakpoints, fluid typography, container queries ve modern CSS features.
metadata:
  skillport:
    category: design
    tags: [accessibility, api integration, backend, browser apis, client-side, components, css3, debugging, deployment, design responsive, frameworks, frontend, fullstack, html5, javascript, libraries, node.js, npm, performance optimization, responsive design, seo, state management, testing, typescript, ui/ux, web development]      - design-components
---

# 📱 Design Responsive

> Responsive tasarım ve modern CSS özellikleri.

---

## 📐 1. Breakpoints

### Standard
```
Mobile:       0 - 639px
Tablet SM:    640 - 767px
Tablet:       768 - 1023px
Desktop:      1024 - 1439px
Wide:         1440px+
```

### Tailwind Mapping
```
sm:  640px
md:  768px
lg:  1024px
xl:  1280px
2xl: 1536px
```

---

## 🔤 2. Fluid Typography

```css
:root {
  --fluid-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --fluid-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --fluid-lg: clamp(1.25rem, 1rem + 1vw, 1.5rem);
  --fluid-xl: clamp(1.5rem, 1.2rem + 1.5vw, 2rem);
  --fluid-2xl: clamp(2rem, 1.5rem + 2.5vw, 3rem);
}
```

---

## 📦 3. Container System

| Device | Max-Width | Padding |
|--------|-----------|---------|
| Mobile | 100% | 16px |
| Tablet | 768px | 24px |
| Desktop | 1200px | 32px |
| Wide | 1440px | 48px |

---

## 🎯 4. Container Queries

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card-content {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}
```

---

## ⚙️ 5. User Preferences

```css
/* Dark mode */
@media (prefers-color-scheme: dark) { }

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}

/* High contrast */
@media (prefers-contrast: high) { }
```

---

## 📋 6. Grid Columns

| Device | Columns | Gutter |
|--------|---------|--------|
| Mobile | 4 | 16px |
| Tablet | 8 | 16px |
| Desktop | 12 | 24px |

---

## 🔄 Workflow

> **Kaynak:** [MDN - Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Containment/Container_Queries) & [Utopia - Fluid Responsive Design](https://utopia.fyi/)

### Aşama 1: Viewport & Layout Strategy
- [ ] **Mobile First**: Tasarımı en küçük ekran boyutundan başlayarak kurgula.
- [ ] **Breakpoints Selection**: Cihaz bazlı değil, içerik bazlı (Content-driven) kırılma noktaları belirle.
- [ ] **Fluid Scaling**: Typography ve spacing için `clamp()` fonksiyonlarını hesapla ve entegre et.

### Aşama 2: Modern CSS Implementation
- [ ] **Container Queries**: Komponentlerin içindeki bulundukları alana göre (Viewport değil) şekil almasını sağla.
- [ ] **Grid/Flex Optimization**: Kompleks layout'lar için `CSS Grid` (Area naming) ve `Flexbox` (Gap) kullan.
- [ ] **Image Optimization**: `srcset` ve `aspect-ratio` kullanarak görsel yüklemelerini ve düzenini optimize et.

### Aşama 3: Performance & Accessibility Audit
- [ ] **Lighthouse Check**: Core Web Vitals (LCP/CLS) metriklerini mobil için optimize et.
- [ ] **Interaction Check**: Dokunmatik (Touch) alanların yeterli boyutta (min 44x44px) olduğunu doğrula.
- [ ] **User Preferences**: `prefers-color-scheme` ve `prefers-reduced-motion` desteğini test et.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Tasarım 320px (iPhone SE) ve 2560px (Ultra-wide) arasında sorunsuz mu? |
| 2 | Horizontal scroll oluşuyor mu? (Overflow kontrolü) |
| 3 | Font boyutları her viewport'ta okunabilir mi? |

---
*Design Responsive v1.5 - With Workflow*
