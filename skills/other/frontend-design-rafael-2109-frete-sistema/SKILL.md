---
name: frontend-design
description: Cria interfaces frontend de alta qualidade com Flask/Jinja2. Gera componentes web, paginas, dashboards e aplicacoes com design profissional, suporte obrigatorio light/dark mode e estetica nao-generica. Usar quando precisar construir telas, artefatos visuais ou posters.
---

Create distinctive frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details.

## Quick Reference

**CSS Variables Reference**: See [references/css-variables.md](references/css-variables.md) for complete list of all CSS variables (`--bs-*`, `--fin-*`, `--agent-*`).

**Premium Effects Reference**: See [references/premium-effects.md](references/premium-effects.md) for aurora background, scroll reveal, and other premium visual effects.

## Decision Tree

```
Does the screen belong to an EXISTING module?
│
├─ YES → Use existing CSS/JS files
│        Use existing class prefix (fin-*, cart-*, exp-*, etc.)
│        EXTEND, don't recreate
│
└─ NO  → Create NEW design system
         Choose unique class prefix
         Follow creation guidelines below
```

## Known Design Systems

| Module | Prefix | CSS File | Reference |
|--------|--------|----------|-----------|
| **Sistema (Bootstrap)** | `--bs-*` | `css/bootstrap-overrides.css` | [css-variables.md#1](references/css-variables.md#1-bootstrap-overrides---bs-) |
| **Financeiro** | `--fin-*` | `css/financeiro/extrato.css` | [css-variables.md#2](references/css-variables.md#2-financeiro---fin-) |
| **Agente** | `--agent-*` | `agente/css/agent-theme.css` | [css-variables.md#3](references/css-variables.md#3-agente---agent-) |

## Using Existing Systems

### Template Structure (with Premium Effects)

```jinja2
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/[module]/[module].css') }}">
{% endblock %}

{% block content %}
<div class="container-fluid premium-page">
    <header class="page-header reveal">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3 mb-0">
                    <i class="fas fa-icon text-primary me-2"></i>
                    Título
                </h1>
                <small class="text-muted">Subtítulo</small>
            </div>
        </div>
    </header>
    <!-- Content -->
</div>
{% endblock %}
```

**Key classes:**
- `premium-page` → Auto-injects aurora background (centralized in base.html)
- `reveal` → Scroll reveal animation for headers/sections

For complete premium effects guide: [references/premium-effects.md](references/premium-effects.md)

### Essential Patterns

**Card:**
```css
.my-card {
    background: var(--bs-secondary-bg);
    border: 1px solid var(--bs-border-color);
    border-radius: 12px;
}
```

**Table:**
```css
.table-container thead th {
    background: var(--bs-tertiary-bg);
    color: var(--bs-secondary-color);
}
```

**For complete patterns**: See [css-variables.md#6](references/css-variables.md#6-padrões-de-componentes)

## Creating New Systems

### Step 1: Define Identity

| Decision | Options |
|----------|---------|
| **Module Name** | `inventory`, `reports`, `customers` |
| **Class Prefix** | `inv-*`, `rpt-*`, `cust-*` |
| **Aesthetic** | Industrial, Clean, Warm, Data-dense, Bold |

### Step 2: CSS Variables Template

```css
/* === [MODULE] DESIGN SYSTEM === */
:root {
    /* Backgrounds */
    --[prefix]-bg-primary: #0a1628;
    --[prefix]-bg-secondary: #111d2e;
    --[prefix]-bg-tertiary: #1a2942;

    /* Texto */
    --[prefix]-text-primary: #f0f6fc;
    --[prefix]-text-secondary: #8b949e;

    /* Acentos */
    --[prefix]-accent-primary: #00d4aa;
    --[prefix]-accent-success: #10b981;
    --[prefix]-accent-warning: #f59e0b;
    --[prefix]-accent-danger: #ef4444;
}

[data-theme="light"] {
    --[prefix]-bg-primary: #ffffff;
    /* ... light mode overrides */
}
```

### Step 3: Signature Visual Moments (pick 2+)

**A. Atmospheric Background:**
```css
.[prefix]-container::before {
    content: '';
    position: fixed;
    background: radial-gradient(
        ellipse at 70% 30%,
        rgba(var(--bs-primary-rgb), 0.08) 0%,
        transparent 60%
    );
    pointer-events: none;
}
```

**B. Entry Animation:**
```css
@keyframes [prefix]-fadeIn {
    from { opacity: 0; transform: translateY(20px); filter: blur(4px); }
    to { opacity: 1; transform: translateY(0); filter: blur(0); }
}
```

**C. Progressive Glow Line:**
```css
.[prefix]-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 0; height: 3px;
    background: linear-gradient(90deg, var(--bs-primary), var(--bs-info));
    transition: width 0.4s ease;
}
.[prefix]-card:hover::after { width: 100%; }
```

## Quality Checklist

- [ ] Uses CSS variables (NOT hex colors)
- [ ] Dark mode complete
- [ ] Light mode complete (NOT just inverted)
- [ ] Theme toggle functional
- [ ] `premium-page` class on main container
- [ ] `reveal` class on header/sections
- [ ] At least 2 signature visual moments
- [ ] Reduced motion respected (`@media (prefers-reduced-motion)`)
- [ ] WCAG AA contrast (4.5:1)

## FORBIDDEN

```css
/* ❌ NEVER USE */
background: #343541;     /* Fixed hex */
background: #0d1117;     /* GitHub Dark */
--accent: #58a6ff;       /* GitHub Blue */
font-family: Arial;      /* Generic font */
```

**Always use**: `var(--bs-*)`, `var(--fin-*)`, or `var(--agent-*)` depending on module.


**If you need to check the availables variables**: See [references/css-variables.md](references/css-variables.md)
