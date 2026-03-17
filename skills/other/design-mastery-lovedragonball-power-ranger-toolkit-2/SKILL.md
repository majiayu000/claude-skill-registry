# 🎨 Design Mastery Skill

---
name: design-mastery
description: Advanced UI/UX design patterns, premium aesthetics, and modern design system implementation
---

## 🎯 Purpose

Master advanced design patterns to create stunning, premium-quality user interfaces that wow users at first glance.

## 📋 When to Use

- Creating premium UI components
- Designing landing pages
- Building design systems
- Reviewing UI for improvements
- Implementing micro-interactions

## 🔧 Design Principles

### 1. Visual Hierarchy
```css
/* Typography Scale */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

### 2. Color Systems
```css
/* Premium Color Palette */
--primary-50: #eff6ff;
--primary-500: #3b82f6;
--primary-900: #1e3a8a;

/* Semantic Colors */
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;
```

### 3. Spacing System
```css
/* 4px Base Grid */
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
```

## ✨ Premium Design Patterns

### Glassmorphism
```css
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

### Neumorphism
```css
.neu-button {
  background: #e0e5ec;
  box-shadow: 
    5px 5px 10px #a3b1c6,
    -5px -5px 10px #ffffff;
  border-radius: 12px;
}
```

### Gradient Backgrounds
```css
.gradient-bg {
  background: linear-gradient(
    135deg, 
    #667eea 0%, 
    #764ba2 100%
  );
}
```

## 🎬 Micro-Interactions

### Hover Effects
```css
.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}
```

### Loading States
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.skeleton {
  animation: pulse 2s infinite;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
}
```

## 📐 Layout Patterns

| Pattern | Use Case |
|---------|----------|
| **Bento Grid** | Dashboard, Portfolio |
| **Split Screen** | Landing pages |
| **Card Grid** | E-commerce, Blog |
| **Masonry** | Gallery, Pinterest-style |
| **Sticky Sidebar** | Documentation |

## 🎯 Design Checklist

- [ ] Consistent spacing (8px grid)
- [ ] Clear visual hierarchy
- [ ] Proper contrast ratios (WCAG AA)
- [ ] Hover/focus states for all interactive elements
- [ ] Loading and empty states
- [ ] Error states with helpful messages
- [ ] Responsive breakpoints
- [ ] Dark mode support

## 🔗 Related Skills

- `accessibility-audit` - Ensure designs are accessible
- `vision-to-code` - Convert designs to code
- `code-review` - Review design implementation
