---
name: RTL (Right-to-Left) Support
description: Supporting right-to-left writing and layout direction for languages like Arabic, Hebrew, Persian, and Urdu using CSS direction, logical properties, and RTL-aware components.
---

# RTL (Right-to-Left) Support

> **Current Level:** Intermediate  
> **Domain:** Internationalization / Frontend

---

## Overview

RTL (Right-to-Left) is the writing and layout direction used by languages such as Arabic, Hebrew, Persian, Urdu, and others. Effective RTL support includes CSS direction properties, logical properties, mirrored layouts, and RTL-aware components.

## What is RTL

### RTL Languages

| Language | Script | Direction |
|----------|-------|-----------|
| **Arabic** | Arabic | RTL |
| **Hebrew** | Hebrew | RTL |
| **Persian** | Persian | RTL |
| **Urdu** | Arabic | RTL |
| **Yiddish** | Hebrew | RTL |
| **Aramaic** | Arabic | RTL |
| **Kurdish** | Arabic | RTL |

### LTR Languages

| Language | Script | Direction |
|----------|-------|-----------|
| **English** | Latin | LTR |
| **Spanish** | Latin | LTR |
| **French** | Latin | LTR |
| **German** | Latin | LTR |
| **Thai** | Thai | LTR |
| **Japanese** | Chinese, Kana | LTR |
| **Korean** | Hangul | LTR |

## HTML dir Attribute

### Setting Direction

```html
<!-- LTR (default) -->
<html dir="ltr">
<head>
    <title>LTR Page</title>
</head>
<body>
    <p>This is left-to-right content.</p>
</body>
</html>

<!-- RTL -->
<html dir="rtl">
<head>
    <title>RTL Page</title>
</head>
<body>
    <p>هذا هو المحتوى من اليمين إلى اليمين.</p>
</body>
</html>

<!-- Dynamic direction -->
<html dir="" id="html-element">
<head>
    <script>
        function setDirection(direction) {
            document.getElementById('html-element').setAttribute('dir', direction);
        }
    </script>
</head>
<body>
    <button onclick="setDirection('ltr')">LTR</button>
    <button onclick="setDirection('rtl')">RTL</button>
</body>
</html>
```

### Auto-Detection

```javascript
// Detect RTL languages
const RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur', 'yi', 'ckb'];

function isRTL(language) {
    return RTL_LANGUAGES.includes(language.split('-')[0]);
}

// Detect browser language
const userLang = navigator.language || 'en-US';
const isUserRTL = isRTL(userLang);

// Set direction
document.documentElement.dir = isUserRTL ? 'rtl' : 'ltr';
```

## CSS for RTL

### Logical Properties

```css
/* Logical properties instead of physical properties */
.container {
    /* Physical (LTR only) */
    margin-left: 20px;
    padding-left: 10px;
    text-align: left;
    float: left;
    
    /* Logical (works for both LTR and RTL) */
    margin-inline-start: 20px;
    padding-inline-start: 10px;
    text-align: start;
    float: inline-start;
}

/* Flexbox */
.flex-container {
    /* Physical */
    flex-direction: row;
    justify-content: flex-start;
    margin-left: 20px;
    
    /* Logical */
    flex-direction: row;
    justify-content: flex-start;
    margin-inline-start: 20px;
}

/* Grid */
.grid-container {
    /* Physical */
    grid-template-columns: 1fr 2fr 3fr;
    gap: 20px 0 0 0 0;
    
    /* Logical */
    grid-template-columns: 1fr 2fr 3fr;
    gap-inline-start: 20px 0 0 0 0;
}

/* Positioning */
.element {
    /* Physical */
    left: 0;
    transform: translateX(100px);
    
    /* Logical */
    inset-inline-start: 0;
    right: 0;
    transform: translateX(100px);
}
```

### Margin and Padding

```css
/* LTR */
.ltr-container {
    margin-left: 20px;
    padding-left: 10px;
}

/* RTL */
.rtl-container {
    margin-right: 20px;
    padding-right: 10px;
}

/* Logical (both) */
.container {
    margin-inline-start: 20px;
    padding-inline-start: 10px;
}
```

### Text Alignment

```css
/* Physical (LTR) */
.ltr-text {
    text-align: left;
    text-indent: 20px;
}

/* Physical (RTL) */
.rtl-text {
    text-align: right;
    text-indent: 20px;
}

/* Logical (both) */
.text {
    text-align: start;
    text-indent: 20px;
}
```

### Flexbox Layout

```css
/* LTR flexbox */
.ltr-flex {
    flex-direction: row;
    justify-content: flex-start;
    margin-left: 20px;
}

/* RTL flexbox */
.rtl-flex {
    flex-direction: row;
    justify-content: flex-end;
    margin-right: 20px;
}

/* Logical flexbox */
.flex {
    flex-direction: row;
    justify-content: flex-start;
    margin-inline-start: 20px;
}
```

### Grid Layout

```css
/* LTR grid */
.ltr-grid {
    grid-template-columns: 1fr 2fr 3fr;
    gap: 20px 0 0 0 0;
    margin-left: 20px;
}

/* RTL grid */
.rtl-grid {
    grid-template-columns: 3fr 2fr 1fr;
    gap: 20px 0 0 0 0;
    margin-right: 20px;
}

/* Logical grid */
.grid {
    grid-template-columns: 1fr 2fr 3fr;
    gap-inline-start: 20px 0 0 0 0;
}
```

## Layout Flipping

### Navigation

```html
<!-- LTR navigation -->
<nav class="ltr-nav">
    <a href="/home">Home</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
</nav>

<!-- RTL navigation -->
<nav class="rtl-nav">
    <a href="/home">الرئيسية</a>
    <a href="/about">عن</a>
    <a href="/contact">اتصل</a>
</nav>
```

```css
/* LTR navigation */
.ltr-nav a {
    margin-right: 20px;
    padding-right: 10px;
}

/* RTL navigation */
.rtl-nav a {
    margin-left: 20px;
    padding-left: 10px;
}

/* Logical navigation */
.nav a {
    margin-inline-end: 20px;
    padding-inline-end: 10px;
}
```

### Cards and Lists

```html
<!-- LTR card -->
<div class="ltr-card">
    <h3>Card Title</h3>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</div>

<!-- RTL card -->
<div class="rtl-card">
    <h3>عنوان البطاقة</h3>
    <ul>
        <li>البند 1</li>
        <li>البند 2</li>
    </ul>
</div>
```

```css
/* LTR card */
.ltr-card ul {
    list-style-position: inside;
    padding-left: 20px;
}

/* RTL card */
.rtl-card ul {
    list-style-position: inside;
    padding-right: 20px;
}

/* Logical card */
.card ul {
    list-style-position: inside;
    padding-inline-start: 20px;
}
```

## Icon and Image Flipping

### Icons

```css
/* Flip icons for RTL */
[dir="rtl"] .icon-arrow {
    transform: scaleX(-1);
}

/* Logical flip */
.icon-arrow {
    transform: scaleX(-1);
}

[dir="ltr"] .icon-arrow {
    transform: scaleX(1);
}
```

### Images

```html
<!-- LTR image -->
<img src="arrow-left.png" alt="Arrow" class="ltr-arrow">

<!-- RTL image -->
<img src="arrow-right.png" alt="Arrow" class="rtl-arrow">
```

```css
/* Flip images for RTL */
[dir="rtl"] .directional-image {
    transform: scaleX(-1);
}

/* Logical flip */
.directional-image {
    transform: scaleX(-1);
}

[dir="ltr"] .directional-image {
    framework: scaleX(1);
}
```

## Not Flipping

### Latin Text and Numbers

```css
/* Don't flip Latin text or numbers */
.latin-text,
.latin-numbers {
    direction: ltr;
    unicode-bidi: embed;
}
```

### URLs and Paths

```css
/* URLs stay LTR */
.url,
.path {
    direction: ltr;
    unicode-bidi: embed;
}
```

## CSS-in-JS with RTL

### Tailwind CSS

```javascript
// tailwind.config.js
module.exports = {
    content: [
        './src/**/*.{js,jsx,ts,tsx}',
    './public/**/*.{png,jpg,jpeg,gif,svg}',
    ],
    theme: {
        extend: {
            screens: {
                lg: {
                    spacing: {
                        'margin-left': '1.5rem',
                        'margin-right': '1.5rem',
                    },
                    'padding-left': '1rem',
                    'padding-right': '1rem',
                    'text-align': 'left',
                    'flex-direction': 'row',
                    'gap': '1rem',
                },
            },
        },
    },
    plugins: [
        require('tailwindcss-rtl')({ default: 'ltr' }),
    ],
}
```

### Styled Components

```jsx
// RTL-aware components
function Card({ children, className = '' }) {
    return (
        <div className={`card ${className}`}>
            {children}
        </div>
    );
}

function Navigation({ links }) {
    return (
        <nav className="nav">
            {links.map(link => (
                <a key={link.href} href={link.href} className="nav-link">
                    {link.text}
                </a>
            ))}
        </nav>
    );
}
```

## React with RTL

### React i18next with RTL

```javascript
import { useTranslation } from 'react-i18next';

function App() {
    const { i18n } = useTranslation();
    const [direction, setDirection] = useState('ltr');
    
    const isRTL = direction === 'rtl';
    
    return (
        <html lang={i18n.language} dir={direction}>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <style>{`
                    body {
                        font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
                        direction: ${direction};
                    }
                    .container {
                        margin-inline-start: 20px;
                        padding: 20px;
                    }
                    .nav {
                        display: flex;
                        gap: 20px;
                        margin-bottom: 20px;
                    }
                    .nav-link {
                        padding: 10px 20px;
                        border-radius: 4px;
                    }
                `}</style>
            </head>
            <body>
                <Navigation links={[
                    { href: '/home', text: i18n.t('nav.home') },
                    { href: '/about', text: i18n.t('nav.about') },
                    { href: '/contact', text: i18n('nav.contact') }
                ]} />
                
                <button onClick={() => setDirection(direction === 'ltr' ? 'rtl' : 'ltr')}>
                    {direction === 'ltr' ? '🔄 RTL' : '🔄 LTR'}
                </button>
                
                <div className="container">
                    <h1>{i18n.t('welcome')}</h1>
                    <p>{i18n.t('description')}</p>
                </div>
            </body>
        </html>
    );
}
```

### Direction Hook

```javascript
import { useState, useEffect } from 'react';

function useDirection() {
    const [direction, setDirection] = useState('ltr');
    
    useEffect(() => {
        // Detect RTL language
        const userLang = navigator.language || 'en-US';
        const isRTL = ['ar', 'he', 'fa', 'ur'].includes(userLang.split('-')[0]);
        
        if (isRTL && direction === 'ltr') {
            setDirection('rtl');
        }
    }, []);
    
    return [direction, setDirection];
}
```

## Vue.js with RTL

### Vue i18n with RTL

```vue
<template>
    <div :dir="direction">
        <button @click="toggleDirection">
            {{ direction === 'ltr' ? '🔄 RTL' : '🔄 LTR' }}
        </button>
        
        <nav>
            <a v-for="link in links" :key="link.href" :href="link.href">
                {{ link.text }}
            </a>
        </nav>
        <div class="content">
            <h1>{{ $t('welcome') }}</h1>
            <p>{{ $t('description') }}</p>
        </div>
    </div>
</template>

<script>
import { useI18n } from 'vue-i18n';

export default {
    data() {
        return {
            direction: 'ltr',
            links: [
                { href: '/home', text: this.$t('nav.home') },
                { href: '/about', this.$t('nav.about') },
                { href: /contact', text: this.$t('nav.contact') }
            ]
        };
    },
    methods: {
        toggleDirection() {
            this.direction = this.direction === 'ltr' ? 'rtl' : 'ltr';
        }
    },
    computed: {
        isRTL() {
            return this.direction === 'rtl';
        }
    }
};
</script>

<style>
.container {
    margin-inline-start: 20px;
    padding: 20px;
}

.nav {
    display: flex;
    gap: 20px;
}

.nav-link {
    padding: 10px 20px;
    border-radius: 4px;
}
</style>
```

## Angular with RTL

### Angular with RTL

```typescript
import { Component, OnInit } from '@angular/core';
import { I18n } from '@ngx-translate/core';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
    direction = 'ltr';
    
    constructor(private translate: I18n) {}
    
    ngOnInit() {
        // Detect RTL language
        const userLang = this.translate.currentLang;
        const isRTL = ['ar', 'he', 'fa', 'ur'].includes(userLang.split('-')[0]);
        
        if (isRTL && this.direction === 'ltr') {
            this.direction = 'rtl';
        }
    }
    
    toggleDirection() {
        this.direction = this.direction === 'ltr' ? 'rtl' : 'ltr';
    }
}
```

```html
<div [dir]="direction">
    <button (click)="toggleDirection()">
        {{ direction === 'ltr' ? '🔄 RTL' : '🔄 LTR' }}
    </button>
    
    <nav>
        <a *ngFor="let link of links" [routerLink]="link.href">
            {{ 'nav.' + link.key | translate }}
        </a>
    </nav>
    
    <div class="content">
        <h1>{{ 'welcome' | translate }}</h1>
        <p>{{ 'description' | translate }}</p>
    </div>
</div>
```

```scss
.container {
    margin-inline-start: 20px;
    padding: 20px;
}

.nav {
    display: flex;
    gap: 20px;
}

.nav-link {
    padding: 10px 20px;
    border-radius: 4px;
}

[dir="rtl"] {
    .container {
        margin-inline-start: 20px;
    }
    
    .nav {
        gap: 20px;
    margin-inline-end: 20px;
    }
}
```

## Testing RTL

### Visual Testing

| Test | Description |
|------|-------------|
| **Layout** | Check alignment in both directions |
| **Text** | Verify text displays correctly |
| **Forms** | Test form input and validation |
| **Navigation** | Check menu and links work |
| **Responsiveness** | Test on mobile devices |

### Automated Testing

```javascript
// RTL test suite
describe('RTL Support', () => {
    const rtlLanguages = ['ar', 'he', 'fa', 'ur', 'yi', 'ckb'];
    
    rtlLanguages.forEach(lang => {
        describe(`Language: ${lang}`, () => {
            // Test direction detection
            expect(isRTL(lang)).toBe(true);
            
            // Test CSS logical properties
            const element = document.createElement('div');
            document.body.appendChild(element);
            element.style.marginInlineStart = '20px';
            const computedStyle = window.getComputedStyle(element);
            expect(computedStyle.marginInlineStart).toBe('20px');
            document.body.removeChild(element);
        });
    });
});
```

## Common Issues and Solutions

### Issue: Misaligned Content

**Problem**: Content doesn't align in RTL

**Solution**: Use logical properties

```css
/* Bad: Physical properties */
.bad-alignment {
    margin-left: 20px;  /* Wrong for RTL */
}

/* Good: Logical properties */
.good-alignment {
    margin-inline-start: 20px;  /* Works for both */
}
```

### Issue: Broken Layout

**Problem**: Layout breaks in RTL

**Solution**: Test with both directions

```css
/* Test both directions */
.container {
    /* Test with LTR */
    margin-inline-start: 20px;
}

[dir="rtl"] .container {
    /* Override for RTL */
    margin-inline-start: 20px;
}
```

### Issue: Icons Not Flipped

**Problem**: Icons point wrong direction

**Solution**: Flip icons for RTL

```css
/* Flip icons for RTL */
[dir="rtl"] .icon {
    transform: scaleX(-1);
}
```

### Issue: URLs Broken

**Problem**: URLs become unclickable

**Solution**: Keep URLs LTR

```css
/* Keep URLs LTR */
.url {
    direction: ltr;
    unicode-bidi: embed;
}
```

## Tools

### RTL Testing Tools

| Tool | Description |
|------|-------------|
| **Browsers** | Chrome DevTools, Firefox DevTools |
| **Extensions** | RTL tester extensions |
| **Online** | RTL preview tools |

### Browser DevTools

```
1. Open DevTools (F12)
2. Toggle device toolbar
3. Select device (iPhone, iPad, etc.)
4. Test RTL layout
```

### Browser Extensions

| Extension | Description |
|-----------|-------------|
| **RTL Tester** | Test RTL layouts |
| **Direction** | Switch between LTR/RTL |
| **Bidi Checker** | Check bidirectional text |

## Real Examples

### RTL E-commerce

```html
<div dir="rtl">
    <nav class="navbar">
        <a href="/products">المنتجات</a>
        <a href="/cart">السلة</a>
        <a href="/checkout">إتمام الطلب</a>
    </nav>
    
    <div class="product">
        <img src="product.jpg" alt="منتج" />
        <h1>منتج جديد</h1>
        <p>منتج جديد مع خصم 10%</p>
        <button>أضف للسلة</button>
    </div>
    
    <div class="price">
        <span class="original-price">100 ر.س</span>
        <span class="discount-price">90 ر.س</span>
    </div>
</div>
```

```css
.navbar {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
}

.navbar a {
    padding: 10px 20px;
    border-radius: 4px;
}

.price {
    text-align: center;
    margin: 20px 0;
}

.original-price {
    text-decoration: line-through;
    color: #999;
}

.discount-price {
    color: #e74c3c;
    font-weight: bold;
}
```

### RTL Dashboard

```html
<div dir="rtl">
    <header class="dashboard-header">
        <h1>لوحة التحليلات</h1>
        <p>آخر تحديث: 15 يناير 2024</p>
    </header>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h2>المستخدمين النشط</h2>
            <p class="stat-value">12,3456</p>
            <p class="stat-change">+5.2%</p>
        </div>
        <div class="stat-card">
            <h2>الإيرادات</h2>
            <p class="stat-value">1,234</p>
            <p class="stat-change">+8.7%</p>
        </div>
        <div class="stat-card">
            <h2>الدخل</h2>
            <p class="stat-value">456</p>
            <p class="stat-change">-2.3%</p>
        </div>
    </div>
</div>
```

```css
.dashboard-header {
    margin-bottom: 30px;
    padding: 20px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}

.stat-value {
    font-size: 2rem;
    font-weight: bold;
    margin: 10px 0;
}

.stat-change {
    color: #28a745;
    font-weight: bold;
}
```

### RTL Form

```html
<div dir="rtl">
    <form class="rtl-form">
        <div class="form-group">
            <label for="email">البريد الإلكتروني</label>
            <input type="email" id="email" placeholder="example@email.com" />
        </div>
        
        <div class="form-group">
            <label for="password">كلمة المرور</label>
            <input type="password" id="password" />
        </div>
        
        <div class="form-group">
            <label for="name">الاسم الكامل</label>
            <input type="text" id="name" />
        </div>
        
        <button type="submit">تسجيل</button>
    </form>
</div>
```

```css
.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
}

.form-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.form-group button {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
}
```

## Summary Checklist

### Planning

- [ ] RTL languages identified
- [ ] RTL requirements documented
- [ ] Design system supports RTL
- [ ] Translation includes RTL languages

### Implementation

- [ ] HTML dir attribute used
- [ ] Logical CSS properties
- [ ] Icons and images mirrored
- [ ] Text alignment handled
```

---

## Quick Start

### HTML Direction

```html
<!-- Set direction -->
<html dir="rtl" lang="ar">
  <head>
    <title>My App</title>
  </head>
  <body>
    <!-- Content automatically flows RTL -->
  </body>
</html>
```

### CSS Logical Properties

```css
/* ❌ Bad - Physical properties */
.element {
  margin-left: 10px;
  padding-right: 20px;
  border-left: 1px solid black;
}

/* ✅ Good - Logical properties */
.element {
  margin-inline-start: 10px;  /* Left in LTR, Right in RTL */
  padding-inline-end: 20px;
  border-inline-start: 1px solid black;
}
```

---

## Production Checklist

- [ ] **Direction Detection**: Auto-detect RTL languages
- [ ] **HTML dir**: Set dir attribute correctly
- [ ] **CSS Logical Properties**: Use logical properties
- [ ] **Icons**: Mirror icons appropriately
- [ ] **Images**: Handle image direction
- [ ] **Text Alignment**: Proper text alignment
- [ ] **Layout**: RTL-aware layouts
- [ ] **Testing**: Test with RTL languages
- [ ] **Documentation**: Document RTL support
- [ ] **Design System**: RTL-aware design system
- [ ] **Components**: RTL-aware components
- [ ] **Accessibility**: Maintain accessibility in RTL

---

## Anti-patterns

### ❌ Don't: Physical Properties Only

```css
/* ❌ Bad - Physical properties */
.element {
  margin-left: 10px;  /* Wrong in RTL! */
  padding-right: 20px;
}
```

```css
/* ✅ Good - Logical properties */
.element {
  margin-inline-start: 10px;  /* Adapts to direction */
  padding-inline-end: 20px;
}
```

### ❌ Don't: Hardcoded Directions

```css
/* ❌ Bad - Hardcoded */
.text {
  text-align: left;  /* Wrong in RTL! */
}
```

```css
/* ✅ Good - Direction-aware */
.text {
  text-align: start;  /* Adapts to direction */
}
```

---

## Integration Points

- **i18n Setup** (`25-internationalization/i18n-setup/`) - Internationalization
- **Localization** (`25-internationalization/localization/`) - Content translation
- **Multi-language** (`25-internationalization/multi-language/`) - Multi-language support

---

## Further Reading

- [CSS Logical Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties)
- [RTL Best Practices](https://rtlstyling.com/)
- [ ] Icons flip for RTL
- [ ] URLs remain LTR
- [ ] Numbers stay LTR

### Testing

- [ ] Test all RTL languages
- [ ] Visual testing completed
- [ ] Form testing completed
- [ ] Navigation testing completed
- [ ] Responsiveness verified

### Maintenance

- [ ] New content checked for RTL
- [ ] Translations reviewed
- [ ] User feedback collected
- [ ] RTL bugs prioritized
