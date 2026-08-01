---
name: screenshot-to-code
description: แปลง screenshots หรือ design mockups เป็น working code (HTML/CSS/React)
---

# 📸 Screenshot to Code Skill

---
name: screenshot-to-code
description: Convert UI screenshots or design mockups into working code
---

## 🎯 Purpose

แปลง screenshots หรือ design mockups เป็น working code (HTML/CSS/React)

## 📋 When to Use

- Implement designs from Figma/Sketch
- Clone existing UI
- Rapid prototyping
- Design handoff

## 🔧 Process

```
1. ANALYZE screenshot
   - Layout structure
   - Components
   - Colors, fonts
   - Spacing

2. IDENTIFY patterns
   - Grid/Flexbox
   - Component library matches
   - Responsive behavior

3. GENERATE code
   - HTML structure
   - CSS/Tailwind styles
   - React components

4. REFINE
   - Pixel perfect adjustments
   - Responsive tweaks
   - Interactions
```

## 📝 Example Workflow

### Input: Card Component Screenshot

### Output:
```jsx
function ProductCard({ product }) {
  return (
    <div className="card">
      <img
        src={product.image}
        alt={product.name}
        className="card-image"
      />
      <div className="card-content">
        <h3 className="card-title">{product.name}</h3>
        <p className="card-price">฿{product.price}</p>
        <button className="card-button">
          Add to Cart
        </button>
      </div>
    </div>
  );
}
```

```css
.card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  background: white;
}

.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.card-price {
  color: #10b981;
  font-weight: 700;
  margin-bottom: 12px;
}

.card-button {
  width: 100%;
  padding: 12px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
```

## 📊 Analysis Checklist

| Element | Extract |
|---------|---------|
| Layout | Grid, Flex, positioning |
| Colors | Primary, secondary, text |
| Typography | Fonts, sizes, weights |
| Spacing | Margins, padding, gaps |
| Borders | Radius, width, color |
| Shadows | Box-shadow values |
| Images | Aspect ratios, fit |

## ✅ Quality Checklist

- [ ] Matches original visually
- [ ] Responsive behavior
- [ ] Semantic HTML
- [ ] Accessible
- [ ] Clean code structure
- [ ] Reusable components

## 🔗 Related Skills

- `vision-to-code` - Similar, image input
- `design-mastery` - Premium designs
- `ui-first-builder` - UI development
