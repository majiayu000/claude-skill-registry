---
name: internationalization
description: i18n/l10n implementation for multi-language support. Use for translation setup, RTL support, and locale-aware formatting.
---

# 🌍 Internationalization (i18n) Skill

## Setup

### Next.js (next-intl)
```bash
npm install next-intl
```

```typescript
// messages/en.json
{
  "home": {
    "title": "Welcome",
    "greeting": "Hello, {name}!"
  }
}

// messages/th.json
{
  "home": {
    "title": "ยินดีต้อนรับ",
    "greeting": "สวัสดี, {name}!"
  }
}
```

### React (react-i18next)
```bash
npm install react-i18next i18next
```

```typescript
import { useTranslation } from 'react-i18next';

function Welcome() {
  const { t } = useTranslation();
  return <h1>{t('home.title')}</h1>;
}
```

---

## Translation Best Practices

### Do's ✅
```json
{
  "items_count": "{count, plural, one {# item} other {# items}}",
  "greeting": "Hello, {name}!",
  "date_format": "{date, date, medium}"
}
```

### Don'ts ❌
```javascript
// Don't concatenate strings
const message = t('hello') + ' ' + name;  // ❌

// Do use interpolation
const message = t('greeting', { name }); // ✅
```

---

## Number & Date Formatting

```javascript
// Numbers
new Intl.NumberFormat('th-TH', {
  style: 'currency',
  currency: 'THB'
}).format(1234.56);
// "฿1,234.56"

// Dates
new Intl.DateTimeFormat('th-TH', {
  dateStyle: 'long'
}).format(new Date());
// "15 มกราคม 2569"

// Relative time
new Intl.RelativeTimeFormat('th', { numeric: 'auto' })
  .format(-1, 'day');
// "เมื่อวาน"
```

---

## RTL Support

```css
/* Use logical properties */
.container {
  /* Instead of margin-left/right */
  margin-inline-start: 1rem;
  margin-inline-end: 2rem;
  
  /* Instead of padding-left/right */
  padding-inline: 1rem;
  
  /* Instead of text-align: left */
  text-align: start;
}

/* RTL-specific styles */
[dir="rtl"] .icon-arrow {
  transform: scaleX(-1);
}
```

```html
<html lang="ar" dir="rtl">
```

---

## Locale Detection

```typescript
// Browser detection
const locale = navigator.language; // "th-TH"

// Accept-Language header
app.use((req, res, next) => {
  const locale = req.acceptsLanguages('th', 'en') || 'en';
  req.locale = locale;
  next();
});
```

---

## Translation Workflow

```
1. Extract strings → i18n keys
2. Create base locale (en.json)
3. Send to translators
4. Import translations
5. Test all locales
6. Handle missing translations
```

## Checklist

- [ ] Set up i18n library
- [ ] Create translation files
- [ ] Handle pluralization
- [ ] Format dates/numbers
- [ ] Support RTL if needed
- [ ] Add language switcher
- [ ] Test all locales
- [ ] Handle missing keys
