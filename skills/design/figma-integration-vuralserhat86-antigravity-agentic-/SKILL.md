---
name: figma-integration
description: '> Figma design-to-code workflow rehberi.'
---

---
name: figma_integration
router_kit: FullStackKit
description: Figma design-to-code, design system extraction ve component generation rehberi.
metadata:
  skillport:
    category: design
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, figma integration, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - design-system
---

# 🎨 Figma Integration

> Figma design-to-code workflow rehberi.

---

## 📋 Design Token Extraction

### Figma Variables → CSS
```css
:root {
  /* Colors from Figma */
  --color-primary: #3b82f6;
  --color-secondary: #10b981;

  /* Spacing from Figma */
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;

  /* Typography */
  --font-size-sm: 14px;
  --font-size-base: 16px;
}
```

---

## 🔧 Component Mapping

| Figma | React Component |
|-------|-----------------|
| Frame | `<div>` |
| Auto Layout | Flexbox |
| Component | React Component |
| Instance | Component usage |
| Text | `<p>`, `<h1>`, etc. |

---

## 📐 Layout Translation

### Figma Auto Layout → CSS Flexbox
```css
/* Horizontal, space-between, gap 16 */
.container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
}

/* Vertical, start, gap 8 */
.stack {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}
```

---

## 🎯 Best Practices

1. **Naming**: Figma layer names = component names
2. **Variants**: Figma variants = component props
3. **Tokens**: Export design tokens as JSON
4. **Components**: Start from atoms → molecules → organisms

---

*Figma Integration v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Figma for Developers](https://www.figma.com/best-practices/developer-handoff-guide/)

### Aşama 1: Inspection
- [ ] **Dev Mode**: Figma Dev Mode'u aç ve CSS/iOS/Android kodunu incele.
- [ ] **Assets**: Görselleri SVG veya 2x/3x PNG olarak export et.
- [ ] **Variables**: Renk/Spacing token'larını `theme.ts` veya `tailwind.config`'e ekle.

### Aşama 2: component Build
- [ ] **Structure**: Frame yapısını `Flex` veya `Grid` olarak koda dök.
- [ ] **Props**: Varyantları (Primary/Secondary) component prop'u yap.
- [ ] **Responsive**: Auto Layout constraint'lerine göre responsive davranışı kodla.

### Aşama 3: Verification
- [ ] **Pixel Perfect**: Overlay ile tasarım ve kodu üst üste kontrol et.
- [ ] **States**: Hover, Focus, Active, Disabled durumlarını atlama.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Tüm renkler hardcoded hex yerine variable mı? |
| 2 | Component Figma'daki gibi esniyor (resize) mu? |
| 3 | Yazı tipleri ve satır aralıkları birebir aynı mı? |
