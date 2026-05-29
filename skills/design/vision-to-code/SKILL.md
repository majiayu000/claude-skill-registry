---
name: vision-to-code
description: Convert UI screenshots and designs to working code. Use when translating visual designs, mockups, or screenshots into HTML/CSS/React components.
---

# 👁️ Vision to Code Skill

## Workflow

### Step 1: Analyze Image
1. Identify layout structure (grid, flex, columns)
2. List all UI components
3. Note colors, fonts, spacing
4. Identify interactive elements

### Step 2: Plan Component Structure
```
Page
├── Header (nav, logo, menu)
├── Hero (title, subtitle, CTA)
├── Features (grid of cards)
├── Testimonials (carousel)
└── Footer (links, social)
```

### Step 3: Generate Code

---

## Common Patterns

### Card Component
```jsx
<div className="card">
  <img src={image} alt={title} className="card-image" />
  <div className="card-content">
    <h3 className="card-title">{title}</h3>
    <p className="card-description">{description}</p>
    <button className="card-button">Learn More</button>
  </div>
</div>
```

```css
.card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s;
}
.card:hover {
  transform: translateY(-4px);
}
```

### Navigation
```jsx
<nav className="navbar">
  <div className="logo">Brand</div>
  <ul className="nav-links">
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
    <li><a href="#">Services</a></li>
  </ul>
  <button className="cta-button">Get Started</button>
</nav>
```

---

## Design Token Extraction

| Visual Element | CSS Property | Example |
|----------------|--------------|---------|
| Primary Color | `--primary` | `#6366f1` |
| Background | `--bg` | `#f8fafc` |
| Text | `--text` | `#1e293b` |
| Border Radius | `--radius` | `12px` |
| Shadow | `--shadow` | `0 4px 6px rgba(0,0,0,0.1)` |
| Font | `--font` | `'Inter', sans-serif` |

---

## Responsive Approach

```css
/* Mobile First */
.container {
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

---

## Checklist

- [ ] วิเคราะห์ layout โครงสร้าง
- [ ] ระบุ components ทั้งหมด
- [ ] Extract design tokens (colors, fonts)
- [ ] สร้าง HTML structure
- [ ] เพิ่ม CSS styling
- [ ] ทำให้ responsive
- [ ] เพิ่ม interactivity (hover, click)
- [ ] Test บน multiple screen sizes
