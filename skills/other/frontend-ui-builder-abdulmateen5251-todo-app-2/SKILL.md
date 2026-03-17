---
name: frontend-ui-builder
description: Build responsive frontend pages and reusable UI components with clean layouts and modern styling.
---

# Frontend UI Builder

## Instructions

### 1. Page & Layout Structure

- Use semantic HTML (`header`, `main`, `section`, `footer`)
- Full-width or container-based layouts
- Clear visual hierarchy
- Grid or Flexbox-based positioning

### 2. Components

- Build reusable UI components (buttons, cards, navbars)
- Consistent spacing and typography
- Component-first mindset
- Easy to scale and modify

### 3. Styling

- Mobile-first CSS approach
- Use Flexbox and CSS Grid
- CSS variables for colors, spacing, and fonts
- Clean hover, focus, and active states

### 4. Responsiveness

- Works across mobile, tablet, and desktop
- Breakpoints for layout changes
- Fluid typography and spacing

## Best Practices

- Keep components reusable and isolated
- Follow mobile-first design principles
- Maintain a consistent spacing system
- Ensure accessible color contrast
- Avoid inline styles
- Use clear and predictable class names

## Example Structure

```html
<header class="navbar">
  <div class="container">
    <h1 class="logo">Brand</h1>
    <nav class="nav-links">
      <a href="#">Home</a>
      <a href="#">Features</a>
      <a href="#">Contact</a>
    </nav>
  </div>
</header>

<main class="container">
  <section class="card-grid">
    <div class="card">
      <h2>Card Title</h2>
      <p>Reusable component content.</p>
      <button class="btn-primary">Action</button>
    </div>
  </section>
</main>
```