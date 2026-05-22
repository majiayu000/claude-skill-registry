---
name: i18n (Internationalization) Setup
description: Designing software applications to adapt to different languages and regions without requiring engineering changes, using translation keys, pluralization, and locale-aware formatting.
---

# i18n (Internationalization) Setup

> **Current Level:** Intermediate  
> **Domain:** Internationalization / Frontend

---

## Overview

Internationalization (i18n) is the process of designing software applications to adapt to different languages and regions without requiring engineering changes. Effective i18n uses translation keys, pluralization rules, date/number formatting, and RTL support to create applications that work globally.

## What is i18n

### i18n vs l10n

| Aspect | i18n | l10n |
|--------|-------|-------|
| **Full Name** | Internationalization | Localization |
| **Focus** | Making app translatable | Translating to specific language |
| **When** | During development | After i18n is complete |
| **Who** | Developers | Translators |
| **Output** | Code with translation keys | Translated content |

### i18n Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      i18n Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │   Source    │───▶│ Translation │───▶│   Display   │   │
│  │    Code     │    │    Files    │    │   Layer     │   │
│  │             │    │             │    │             │   │
│  │ t('key')    │    │ { "key":    │    │ Hello World │   │
│  │             │    │   "value"  │    │             │   │
│  │             │    │ }           │    │             │   │
│  └─────────────┘    └─────────────┘    └─────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Locale

### Locale Format

`language-COUNTRY`

| Locale | Language | Country |
|--------|----------|---------|
| `en-US` | English | United States |
| `en-GB` | English | United Kingdom |
| `th-TH` | Thai | Thailand |
| `pt-BR` | Portuguese | Brazil |
| `ja-JP` | Japanese | Japan |

### Supported Locales

```javascript
const SUPPORTED_LOCALES = [
    'en-US',
    'th-TH',
    'ja-JP',
    'pt-BR',
    'de-DE',
    'fr-FR',
    'es-ES',
    'zh-CN'
];
```

## Translation File Structure

### JSON Format

```json
{
  "common": {
    "welcome": "Welcome",
    "login": "Login",
    "logout": "Logout"
  },
  "auth": {
    "email": "Email",
    "password": "Password",
    "forgotPassword": "Forgot Password?",
    "signup": "Sign Up"
  },
  "errors": {
    "required": "This field is required",
    "invalidEmail": "Invalid email address",
    "wrongPassword": "Incorrect password"
  }
}
```

### Nested Keys

```json
{
  "user": {
    "profile": {
      "title": "Profile",
      "name": "Name",
      "email": "Email"
    },
    "settings": {
      "title": "Settings",
      "language": "Language",
      "theme": "Theme"
    }
  }
}
```

### Pluralization

```json
{
  "items": {
    "zero": "No items",
    "one": "One item",
    "other": "{{count}} items"
  }
}
```

## i18n Libraries

### React

| Library | Description |
|---------|-------------|
| **react-i18next** | Most popular, feature-rich |
| **react-intl** | Format.js-based, good for complex formatting |
| **react-intl-universal** | Lightweight, simple |

### Vue.js

| Library | Description |
|---------|-------------|
| **vue-i18n** | Official Vue plugin |
| **vue-intl** | Alternative plugin |

### Angular

| Library | Description |
|---------|-------------|
| **@angular/localize** | Official Angular i18n |
| **ngx-translate** | Community favorite |

### Node.js

| Library | Description |
|---------|-------------|
| **i18next** | Framework-agnostic |
| **i18n-node** | Simple Node.js i18n |

### Python

| Library | Description |
|---------|-------------|
| **Babel** | Python i18n library |
| **gettext** | GNU gettext for Python |

### Java

| Library | Description |
|---------|-------------|
| **ResourceBundle** | Built-in Java i18n |
| **MessageFormat** | ICU MessageFormat |

## react-i18next Setup

### Installation

```bash
npm install i18next react-i18next
```

### Configuration

```javascript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            welcome: 'Welcome',
            login: 'Login'
        }
    },
    th: {
        translation: {
            welcome: 'ยินดีต้อนรับ',
            login: 'เข้าสู่ระบบ'
        }
    }
};

i18n.use(initReactI18next({
    resources,
    lng: 'en', // Default language
    fallbackLng: 'en',
    interpolation: { escapeValue: false },
    react: {
        useSuspense: false
    }
}));

export default i18n;
```

### Using Translations

```javascript
import { useTranslation } from 'react-i18next';

function Welcome() {
    const { t } = useTranslation();
    
    return (
        <div>
            <h1>{t('welcome')}</h1>
            <button>{t('login')}</button>
        </div>
    );
}
```

### Dynamic Content

```javascript
const { t } = useTranslation();

function Greeting({ name }) {
    return <p>{t('greeting', { name })}</p>;
}

// Translation: "greeting": "Hello, {{name}}"
```

### Pluralization

```javascript
const { t } = useTranslation();

function ItemCount({ count }) {
    return <p>{t('items', { count })}</p>;
}

// Translation:
// "items_zero": "No items",
// "items_one": "One item",
// "items_other": "{{count}} items"
```

## Translation Keys

### Naming Conventions

| Convention | Example | Why |
|-----------|----------|-----|
| **Descriptive** | `user.profile.title` | Self-documenting |
| **Hierarchical** | `auth.login.email` | Organized |
| **Consistent** | `button.submit` | Predictable |
| **Avoid** | `btn1`, `txt2` | Unclear |

### Namespace Organization

```json
{
  "common": {
    "actions": {
      "save": "Save",
      "cancel": "Cancel",
      "delete": "Delete"
    }
  },
  "auth": {
    "login": {
      "title": "Login",
      "email": "Email",
      "password": "Password",
      "button": "Login"
    },
    "signup": {
      "title": "Sign Up",
      "name": "Name",
      "email": "Email",
      "password": "Password",
      "button": "Sign Up"
    }
  },
  "dashboard": {
    "title": "Dashboard",
    "overview": "Overview",
    "analytics": "Analytics",
    "settings": "Settings"
  }
}
```

### Default Values

```javascript
const { t } = useTranslation();

function Welcome() {
    return (
        <div>
            <h1>{t('welcome', { defaultValue: 'Welcome' })}</h1>
        </div>
    );
}
```

## Language Detection

### Browser Language

```javascript
function detectBrowserLanguage() {
    return navigator.language || navigator.userLanguage;
}

// Returns: "en-US", "th-TH", etc.
```

### User Preference

```javascript
// Get from localStorage
function getUserLanguage() {
    return localStorage.getItem('userLanguage') || 'en-US';
}

// Set user preference
function setUserLanguage(language) {
    localStorage.setItem('userLanguage', language);
    i18n.changeLanguage(language);
}
```

### URL Parameter

```javascript
function getLanguageFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('lang') || getUserLanguage();
}

// Usage: ?lang=th-TH
```

### Subdomain

```javascript
function getLanguageFromSubdomain() {
    const subdomain = window.location.hostname.split('.')[0];
    const languageMap = {
        'en': 'en-US',
        'th': 'th-TH',
        'ja': 'ja-JP'
    };
    return languageMap[subdomain] || 'en-US';
}

// Usage: en.example.com, th.example.com
```

### Detection Priority

```
URL Parameter → User Preference → Browser Language → Default
```

```javascript
function getLanguage() {
    // 1. Check URL parameter
    const urlLang = getLanguageFromURL();
    if (urlLang && SUPPORTED_LOCALES.includes(urlLang)) {
        return urlLang;
    }
    
    // 2. Check user preference
    const userLang = getUserLanguage();
    if (userLang && SUPPORTED_LOCALES.includes(userLang)) {
        return userLang;
    }
    
    // 3. Check browser language
    const browserLang = detectBrowserLanguage();
    if (browserLang && SUPPORTED_LOCALES.includes(browserLang)) {
        return browserLang;
    }
    
    // 4. Default
    return 'en-US';
}
```

## Language Switching

### Language Switcher Component

```javascript
import { useTranslation } from 'react-i18next';

function LanguageSwitcher() {
    const { i18n } = useTranslation();
    const { changeLanguage } = i18n;
    
    const handleLanguageChange = (language) => {
        changeLanguage(language);
        setUserLanguage(language);
    };
    
    return (
        <select value={i18n.language} onChange={(e) => handleLanguageChange(e.target.value)}>
            <option value="en-US">English</option>
            <option value="th-TH">ไทย</option>
            <option value="ja-JP">日本語</option>
            <option value="pt-BR">Português</option>
        </select>
    );
}
```

### Persist Preference

```javascript
function setUserLanguage(language) {
    localStorage.setItem('userLanguage', language);
    
    // Also send to server if user is logged in
    if (isLoggedIn()) {
        fetch('/api/user/language', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language })
        });
    }
}
```

### Reload Content

```javascript
function changeLanguage(language) {
    i18n.changeLanguage(language);
    setUserLanguage(language);
    
    // Optional: Reload page to apply new language
    // window.location.reload();
}
```

## RTL (Right-to-Left) Support

### RTL Languages

| Language | Direction |
|----------|-----------|
| Arabic | RTL |
| Hebrew | RTL |
| Persian | RTL |
| Urdu | RTL |

### Setting Direction

```javascript
import { useTranslation } from 'react-i18next';

function App() {
    const { i18n } = useTranslation();
    const isRTL = ['ar', 'he', 'fa', 'ur'].includes(i18n.language.split('-')[0]);
    
    return (
        <html lang={i18n.language} dir={isRTL ? 'rtl' : 'ltr'}>
            {/* App content */}
        </html>
    );
}
```

### CSS Logical Properties

```css
/* Logical properties instead of physical properties */
.container {
    margin-inline-start: 20px;  /* margin-left for LTR, margin-right for RTL */
    padding-inline-end: 20px;   /* padding-right for LTR, padding-left for RTL */
    text-align: start;            /* text-align-left for LTR, text-align-right for RTL */
}

/* Flexbox */
.flex-container {
    flex-direction: row;  /* Works with logical properties */
    gap: 20px;
}
```

### Flipping Icons

```css
/* Flip icons for RTL */
[dir="rtl"] .icon-arrow {
    transform: scaleX(-1);
}
```

## Date and Number Formatting

### Intl.DateTimeFormat

```javascript
function formatDate(date, locale) {
    return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(date);
}

// Usage
const date = new Date('2024-01-15');
console.log(formatDate(date, 'en-US')); // January 15, 2024
console.log(formatDate(date, 'th-TH')); // 15 มกราคม 2567
```

### Intl.NumberFormat

```javascript
function formatNumber(number, locale) {
    return new Intl.NumberFormat(locale).format(number);
}

// Usage
console.log(formatNumber(1234.56, 'en-US')); // 1,234.56
console.log(formatNumber(1234.56, 'th-TH')); // 1,234.56
console.log(formatNumber(1234.56, 'de-DE')); // 1.234,56
```

### Currency Formatting

```javascript
function formatCurrency(amount, currency, locale) {
    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Usage
console.log(formatCurrency(99.99, 'USD', 'en-US')); // $99.99
console.log(formatCurrency(99.99, 'THB', 'th-TH')); // ฿99.99
console.log(formatCurrency(99.99, 'EUR', 'de-DE')); // 99,99 €
```

## Translation Workflow

### Export for Translation

```javascript
// Extract translation keys
const translations = {
    en: require('./locales/en.json'),
    th: require('./locales/th.json')
};

// Export to CSV
function exportToCSV(translations, language) {
    const keys = Object.keys(translations[language].translation);
    const values = keys.map(key => translations[language].translation[key]);
    
    const csv = [
        keys.join(','),
        values.join(',')
    ].join('\n');
    
    // Download CSV
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${language}.csv`;
    a.click();
}
```

### Translation Management Platforms

| Platform | Features | Pricing |
|----------|-----------|---------|
| **Lokalise** | Crowdsourced, version control | $$ |
| **Crowdin** | Crowdsourced, integrations | $$ |
| **Phrase** | In-context editor, integrations | $$$ |
| **POEditor** | Simple, affordable | $ |

### Git-Based Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  Git-Based Translation Workflow                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Developer ──▶ 2. Export Keys ──▶ 3. Upload to  │
│     Extracts       to CSV        Platform      │
│     Keys                                       │
│                                                  │
│  4. Translator ──▶ 5. Download       │
│     Translates      Translations    │
│                                                  │
│  6. Developer ──▶ 7. Import to     │
│     Imports         Project        │
│                                                  │
│  8. Commit ──▶ 9. Deploy        │
│     Changes        Translations   │
└─────────────────────────────────────────────────────────────────┘
```

## Missing Translations

### Show Key (Development)

```javascript
const { t } = useTranslation();

function Welcome() {
    return (
        <div>
            <h1>{t('welcome', { defaultValue: 'Welcome' })}</h1>
            {/* Shows 'welcome' if translation missing */}
        </div>
    );
}
```

### Show Default Language (Production)

```javascript
const { t } = useTranslation();

function Welcome() {
    return (
        <div>
            <h1>{t('welcome', { defaultValue: 'Welcome' })}</h1>
            {/* Shows 'welcome' if translation missing */}
        </div>
    );
}

// Configure fallback language
i18n.use(initReactI18next({
    fallbackLng: 'en', // Fallback to English
    // ... other config
}));
```

### Log Missing Keys

```javascript
function missingKeyHandler(lng, ns, key) {
    console.warn(`Missing translation: ${lng}.${ns}.${key}`);
    
    // Send to analytics
    if (window.analytics) {
        window.analytics.track('missing_translation', {
            language: lng,
            namespace: ns,
            key: key
        });
    }
    
    return key; // Return key as fallback
}

i18n.use(initReactI18next({
    missingKeyHandler,
    // ... other config
}));
```

## SEO Considerations

### Separate URLs per Language

```
/en/         (English)
/th/          (Thai)
/ja/          (Japanese)
/pt-BR/       (Portuguese)
```

### Hreflang Tags

```html
<link rel="alternate" hreflang="en" href="https://example.com/en/" />
<link rel="alternate" hreflang="th" href="https://example.com/th/" />
<link rel="alternate" hreflang="ja" href="https://example.com/ja/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/en/" />
```

### Language Selector

```javascript
function LanguageSelector() {
    const languages = [
        { code: 'en', name: 'English', url: '/en/' },
        { code: 'th', name: 'ไทย', url: '/th/' },
        { code: 'ja', name: '日本語', url: '/ja/' }
    ];
    
    return (
        <nav aria-label="Language">
            {languages.map(lang => (
                <a key={lang.code} href={lang.url}>
                    {lang.name}
                </a>
            ))}
        </nav>
    );
}
```

### Translated Meta Tags

```javascript
import { useTranslation } from 'react-i18next';

function MetaTags() {
    const { t } = useTranslation();
    
    return (
        <Helmet>
            <title>{t('meta.title')}</title>
            <meta name="description" content={t('meta.description')} />
            <meta name="keywords" content={t('meta.keywords')} />
        </Helmet>
    );
}
```

## Performance

### Lazy Load Translations

```javascript
import { useTranslation } from 'react-i18next';

function LazyComponent() {
    const { t, ready } = useTranslation('common', { useSuspense: false });
    
    if (!ready) {
        return <div>Loading...</div>;
    }
    
    return <div>{t('welcome')}</div>;
}
```

### Bundle Only Needed Languages

```javascript
// webpack.config.js
module.exports = {
    // ...
    plugins: [
        new i18nextWebpackPlugin({
            languages: ['en', 'th', 'ja'], // Only bundle needed languages
            defaultLanguage: 'en'
        })
    ]
};
```

### Cache Translations

```javascript
// Simple in-memory cache
const translationCache = new Map();

function getTranslation(language, key) {
    const cacheKey = `${language}:${key}`;
    
    if (translationCache.has(cacheKey)) {
        return translationCache.get(cacheKey);
    }
    
    const translation = loadTranslation(language, key);
    translationCache.set(cacheKey, translation);
    return translation;
}
```

## Testing

### Test All Languages

```javascript
describe('i18n', () => {
    const languages = ['en', 'th', 'ja'];
    
    languages.forEach(language => {
        i18n.changeLanguage(language);
        
        test('welcome message', () => {
            const { t } = renderHook();
            expect(t('welcome')).toBeDefined();
        });
        
        test('pluralization', () => {
            const { t } = renderHook();
            expect(t('items', { count: 1 })).toBeDefined();
            expect(t('items', { count: 5 })).toBeDefined();
        });
    });
});
```

### Screenshot Testing

```bash
# Take screenshots in different languages
npm run test:visual --locale=en
npm run test:visual --locale=th
npm run test:visual --locale=ja
```

### Pseudo-Localization

```javascript
// Test string expansion
function pseudoLocalize(text) {
    return text.split('').join(' ');
}

// "Hello" → "H e l l o "
```

## Common Mistakes

### Hardcoded Strings

```javascript
// Bad: Hardcoded string
<h1>Welcome</h1>

// Good: Translated string
<h1>{t('welcome')}</h1>
```

### Concatenating Translations

```javascript
// Bad: Concatenation
<p>{t('hello')} {name}!</p>

// Good: Use interpolation
<p>{t('greeting', { name })}</p>
```

### Not Handling Pluralization

```javascript
// Bad: No pluralization
<p>You have {count} items</p>

// Good: With pluralization
<p>{t('items', { count })}</p>
```

### Not Supporting RTL

```javascript
// Bad: No RTL support
<div className="container">

// Good: RTL support
<div className="container" dir={isRTL ? 'rtl' : 'ltr'}>
```

## Implementation Examples

### React i18next Setup

```javascript
// i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import HttpApi from 'i18next-http-backend';

const resources = {
    en: {
        translation: {
            welcome: 'Welcome',
            login: 'Login',
            logout: 'Logout'
        }
    },
    th: {
        translation: {
            welcome: 'ยินดีต้อนรับ',
            login: 'เข้าสู่ระบบ',
            logout: 'ออกจากระบบ'
        }
    }
};

i18n
    .use(HttpApi) // Load translations from API
    .use(LanguageDetector) // Detect user language
    .use(initReactI18next({
        resources,
        fallbackLng: 'en',
        interpolation: { escapeValue: false },
        react: {
            useSuspense: false
        }
    }))
    .init();

export default i18n;
```

### Translation File Example

```json
// locales/en.json
{
  "common": {
    "welcome": "Welcome",
    "login": "Login",
    "logout": "Logout",
    "save": "Save",
    "cancel": "Cancel"
  },
  "auth": {
    "login": {
      "title": "Login to Your Account",
      "email": "Email Address",
      "password": "Password",
      "button": "Login",
      "forgot": "Forgot Password?",
      "signup": "Don't have an account? Sign up"
    },
    "signup": {
      "title": "Create Your Account",
      "name": "Full Name",
      "email": "Email Address",
      "password": "Password",
      "confirmPassword": "Confirm Password",
      "button": "Sign Up",
      "login": "Already have an account? Login"
    }
  },
  "dashboard": {
    "title": "Dashboard",
    "overview": "Overview",
    "analytics": "Analytics",
    "settings": "Settings",
    "logout": "Logout"
  }
}
```

```json
// locales/th.json
{
  "common": {
    "welcome": "ยินดีต้อนรับ",
    "login": "เข้าสู่ระบบ",
    "logout": "ออกจากระบบ",
    "save": "บันทึก",
    "cancel": "ยกเลิก"
  },
  "auth": {
    "login": {
      "title": "เข้าสู่ระบบของคุณ",
      "email": "อีเมล",
      "password": "รหัสผ่าน",
      "button": "เข้าสู่ระบบ",
      "forgot": "ลืมรหัสผ่าน?",
      "signup": "ยังไม่มีบัญชี? ลงทะเบียน"
    },
    "signup": {
      "title": "สร้างบัญชีของคุณ",
      "name": "ชื่อเต็ม",
      "email": "อีเมล",
      "password": "รหัสผ่าน",
      "confirmPassword": "ยืนยันรหัสผ่าน",
      "button": "ลงทะเบียน",
      "login": "มีบัญชีอยู่? เข้าสู่ระบบ"
    }
  },
  "dashboard": {
    "title": "แดชบอร์ด",
    "overview": "ภาพระกับ",
    "analytics": "การวิเคราะห์",
    "settings": "การตั้งค่า",
    "logout": "ออกจากระบบ"
  }
}
```

### Language Switcher Component

```javascript
import { useTranslation } from 'react-i18next';

function LanguageSwitcher() {
    const { i18n } = useTranslation();
    const { changeLanguage } = i18n;
    
    const languages = [
        { code: 'en-US', name: 'English', flag: '🇺🇸' },
        { code: 'th-TH', name: 'ไทย', flag: '🇹🇭' },
        { code: 'ja-JP', name: '日本語', flag: '🇯🇵' },
        { code: 'pt-BR', name: 'Português', flag: '🇧🇷' }
    ];
    
    const handleLanguageChange = (language) => {
        changeLanguage(language);
        localStorage.setItem('userLanguage', language);
    };
    
    return (
        <div className="language-switcher">
            {languages.map(lang => (
                <button
                    key={lang.code}
                    onClick={() => handleLanguageChange(lang.code)}
                    className={i18n.language === lang.code ? 'active' : ''}
                >
                    <span className="flag">{lang.flag}</span>
                    <span className="name">{lang.name}</span>
                </button>
            ))}
        </div>
    );
}
```

## Summary Checklist

### Setup

- [ ] i18n library installed
- [ ] Translation file structure defined
- [ ] Default language configured
- [ ] Language detection implemented
- [ ] Language switcher created

### Content

- [ ] All strings extracted to translation files
- [ ] Translation keys are descriptive
- [ ] Namespaces organized
- [ ] Pluralization handled
- [ ] Variables supported

### Features

- [ ] RTL support implemented
- [ ] Date/time formatting
- [ ] Number/currency formatting
- [ ] Testing completed
```

---

## Quick Start

### React i18next Setup

```bash
npm install i18next react-i18next i18next-browser-languagedetector
```

```javascript
// i18n.js
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          welcome: 'Welcome',
          goodbye: 'Goodbye'
        }
      },
      th: {
        translation: {
          welcome: 'ยินดีต้อนรับ',
          goodbye: 'ลาก่อน'
        }
      }
    },
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  })
```

### Usage in Components

```jsx
import { useTranslation } from 'react-i18next'

function App() {
  const { t, i18n } = useTranslation()
  
  return (
    <div>
      <h1>{t('welcome')}</h1>
      <button onClick={() => i18n.changeLanguage('th')}>
        Switch to Thai
      </button>
    </div>
  )
}
```

---

## Production Checklist

- [ ] **i18n Library**: Choose and configure i18n library
- [ ] **Translation Files**: Organize translation files by namespace
- [ ] **Translation Keys**: Use descriptive, hierarchical keys
- [ ] **Pluralization**: Handle plural forms correctly
- [ ] **Variables**: Support variables in translations
- [ ] **Date/Time**: Format dates and times per locale
- [ ] **Numbers**: Format numbers and currency per locale
- [ ] **RTL Support**: Support right-to-left languages
- [ ] **Language Detection**: Auto-detect user language
- [ ] **Language Switcher**: UI for language selection
- [ ] **Testing**: Test all languages and locales
- [ ] **Fallback**: Fallback language configured

---

## Anti-patterns

### ❌ Don't: Hardcoded Strings

```jsx
// ❌ Bad - Hardcoded
<h1>Welcome</h1>
<p>Hello, user!</p>
```

```jsx
// ✅ Good - Translation keys
<h1>{t('welcome')}</h1>
<p>{t('greeting', { name: user.name })}</p>
```

### ❌ Don't: No Pluralization

```jsx
// ❌ Bad - No pluralization
{t('item', { count: items.length })}  // Always "item"
```

```jsx
// ✅ Good - Pluralization
{t('item', { count: items.length })}  // "item" or "items"
```

### ❌ Don't: Ignore RTL

```css
/* ❌ Bad - Left-aligned only */
.text {
  text-align: left;
}
```

```css
/* ✅ Good - RTL-aware */
.text {
  text-align: start;  /* Adapts to direction */
}
```

---

## Integration Points

- **Localization** (`25-internationalization/localization/`) - Content translation
- **Multi-language** (`25-internationalization/multi-language/`) - Multi-language support
- **RTL Support** (`25-internationalization/rtl-support/`) - Right-to-left languages

---

## Further Reading

- [i18next Documentation](https://www.i18next.com/)
- [React Intl](https://formatjs.io/docs/react-intl/)
- [i18n Best Practices](https://www.w3.org/International/techniques/developing-specs)
- [ ] Missing translation fallback
- [ ] Translation logging

### Testing

- [ ] All languages tested
- [ ] Screenshot testing completed
- [ ] Pseudo-localization tested
- [ ] RTL layouts tested
- [ ] SEO tags tested
