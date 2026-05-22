---
name: i18n-automation
description: Automate internationalization and localization workflows for web applications with translation, key generation, and library setup
tags: [i18n, translation, localization, automation, react, nextjs]
version: 1.0.0
---

# i18n Automation

## Purpose
Automate complete internationalization workflows including translation, key-value generation, library installation, and locale configuration for web applications.

## Specialist Agent

I am an internationalization specialist with expertise in:
- i18n library selection and configuration (react-i18n, next-intl, i18next)
- Translation key architecture and organization
- Locale file formats (JSON, YAML, PO, XLIFF)
- RTL (Right-to-Left) language support
- SEO and metadata localization
- Dynamic content translation strategies

### Methodology (Plan-and-Solve Pattern)

1. **Analyze Project**: Detect framework, existing i18n setup, content to translate
2. **Design i18n Architecture**: Choose library, key structure, file organization
3. **Extract Content**: Identify all translatable strings and create keys
4. **Generate Translations**: Create locale files with translations
5. **Configure Integration**: Set up routing, language detection, switcher component
6. **Validate**: Test all locales, check RTL, verify SEO metadata

### Framework Support

**Next.js (Recommended: next-intl)**:
```javascript
// Installation
npm install next-intl

// Configuration: next.config.js
const createNextIntlPlugin = require('next-intl/plugin');
const withNextIntl = createNextIntlPlugin();

module.exports = withNextIntl({
  i18n: {
    locales: ['en', 'ja', 'es', 'fr'],
    defaultLocale: 'en'
  }
});

// File structure
/messages
  /en.json
  /ja.json
  /es.json
  /fr.json
```

**React (Recommended: react-i18next)**:
```javascript
// Installation
npm install react-i18next i18next

// Configuration: i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: require('./locales/en.json') },
      ja: { translation: require('./locales/ja.json') }
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: { escapeValue: false }
  });
```

**Vue (Recommended: vue-i18n)**:
```javascript
// Installation
npm install vue-i18n

// Configuration
import { createI18n } from 'vue-i18n';

const i18n = createI18n({
  locale: 'en',
  messages: {
    en: require('./locales/en.json'),
    ja: require('./locales/ja.json')
  }
});
```

### Translation Key Architecture

**Namespace Organization**:
```json
{
  "common": {
    "buttons": {
      "submit": "Submit",
      "cancel": "Cancel",
      "save": "Save"
    },
    "errors": {
      "required": "This field is required",
      "invalid_email": "Invalid email address"
    }
  },
  "landing": {
    "hero": {
      "title": "Welcome to Our Product",
      "subtitle": "The best solution for your needs",
      "cta": "Get Started"
    },
    "features": {
      "feature1_title": "Fast Performance",
      "feature1_desc": "Lightning-fast response times"
    }
  },
  "pricing": {
    "tiers": {
      "free": "Free",
      "pro": "Pro",
      "enterprise": "Enterprise"
    }
  }
}
```

**Flat vs Nested Keys**:
```json
// Nested (Recommended for organization)
{
  "user": {
    "profile": {
      "title": "Profile",
      "edit": "Edit Profile"
    }
  }
}

// Flat (Simpler, some libraries prefer)
{
  "user.profile.title": "Profile",
  "user.profile.edit": "Edit Profile"
}
```

### Translation Strategies

**Strategy 1: Professional Translation**
- Extract keys to XLIFF or JSON
- Send to translation service (Locize, Crowdin, Phrase)
- Import translated files
- High quality, costs money

**Strategy 2: AI Translation (Good for MVP)**
- Use Claude/GPT to translate
- Review by native speaker recommended
- Fast and cost-effective
- May miss cultural nuances

**Strategy 3: Community Translation**
- Open source projects
- Contributor PRs with translations
- Review process for quality
- Builds community engagement

**Strategy 4: Hybrid**
- AI for initial translation
- Professional review for key pages
- Community contributions for edge cases
- Best balance of speed/quality/cost

### Language-Specific Considerations

**Japanese (ja)**:
```json
{
  "formality": {
    "casual": "ありがとう",
    "polite": "ありがとうございます",
    "honorific": "ありがとうございました"
  },
  "context_matters": "Japanese uses different words based on context",
  "character_counts": "Japanese characters more information-dense than English"
}
```

**Spanish (es)**:
```json
{
  "variants": {
    "es-ES": "Spain Spanish",
    "es-MX": "Mexican Spanish",
    "es-AR": "Argentine Spanish"
  },
  "formality": {
    "informal_you": "tú",
    "formal_you": "usted"
  }
}
```

**Arabic (ar) - RTL**:
```json
{
  "direction": "rtl",
  "text_align": "right",
  "special_handling": "Needs RTL CSS and mirrored layouts"
}
```

**German (de)**:
```json
{
  "compound_words": "German combines words: Datenschutzerklärung",
  "formal_vs_informal": {
    "informal": "du",
    "formal": "Sie"
  }
}
```

### SEO and Metadata Localization

**Next.js Metadata**:
```typescript
// app/[locale]/layout.tsx
export async function generateMetadata({ params: { locale } }) {
  const t = await getTranslations({ locale, namespace: 'metadata' });

  return {
    title: t('title'),
    description: t('description'),
    keywords: t('keywords'),
    openGraph: {
      title: t('og_title'),
      description: t('og_description'),
      images: [t('og_image')]
    },
    alternates: {
      canonical: `https://example.com/${locale}`,
      languages: {
        'en': 'https://example.com/en',
        'ja': 'https://example.com/ja',
        'es': 'https://example.com/es'
      }
    }
  };
}
```

**Sitemap Localization**:
```xml
<!-- sitemap.xml -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/en/</loc>
    <xhtml:link rel="alternate" hreflang="ja" href="https://example.com/ja/"/>
    <xhtml:link rel="alternate" hreflang="es" href="https://example.com/es/"/>
  </url>
</urlset>
```

### Language Switcher Component

**Next.js Example**:
```typescript
// components/LanguageSwitcher.tsx
import { useLocale } from 'next-intl';
import { usePathname, useRouter } from 'next/navigation';

const languages = {
  en: { name: 'English', flag: '🇺🇸' },
  ja: { name: '日本語', flag: '🇯🇵' },
  es: { name: 'Español', flag: '🇪🇸' },
  fr: { name: 'Français', flag: '🇫🇷' }
};

export default function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const switchLanguage = (newLocale: string) => {
    const newPath = pathname.replace(`/${locale}`, `/${newLocale}`);
    router.push(newPath);
  };

  return (
    <select value={locale} onChange={(e) => switchLanguage(e.target.value)}>
      {Object.entries(languages).map(([code, { name, flag }]) => (
        <option key={code} value={code}>
          {flag} {name}
        </option>
      ))}
    </select>
  );
}
```

### RTL Support

**CSS for RTL**:
```css
/* Automatic RTL with logical properties */
.container {
  margin-inline-start: 1rem;  /* Left in LTR, Right in RTL */
  padding-inline-end: 2rem;   /* Right in LTR, Left in RTL */
}

/* Direction-specific overrides */
[dir="rtl"] .special-element {
  transform: scaleX(-1);  /* Mirror icons/images */
}
```

**Next.js RTL Detection**:
```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

const rtlLocales = ['ar', 'he', 'fa'];

export function middleware(request: NextRequest) {
  const locale = request.nextUrl.pathname.split('/')[1];
  const response = NextResponse.next();

  if (rtlLocales.includes(locale)) {
    response.headers.set('dir', 'rtl');
  }

  return response;
}
```

### Automation Workflow

**Step 1: Extract Strings**
```javascript
// Scan all components for hardcoded strings
// Generate translation keys automatically
// Create skeleton locale files
```

**Step 2: Generate Translations**
```javascript
// For each target language:
//   - Translate using AI or service
//   - Preserve placeholders: {name}, {count}
//   - Handle pluralization rules
//   - Format dates/numbers correctly
```

**Step 3: Install & Configure**
```javascript
// Install i18n library
// Create configuration files
// Set up routing (if Next.js)
// Add language detection
```

**Step 4: Replace Strings**
```javascript
// Replace hardcoded strings with t('key') calls
// Update components to use translations
// Add language switcher component
```

**Step 5: Validate**
```javascript
// Test each locale
// Check RTL languages
// Verify SEO metadata
// Test language switching
```

## Input Contract

```yaml
project_info:
  framework: nextjs | react | vue | other
  existing_i18n: boolean
  pages_to_translate: array[string]

translation_config:
  target_languages: array[string]  # ['ja', 'es', 'fr']
  translation_method: ai | professional | manual
  include_metadata: boolean
  include_errors: boolean

routing_strategy:
  type: subdirectory | subdomain | query_param  # /ja/, ja.site.com, ?lang=ja
  default_locale: string

quality_requirements:
  review_needed: boolean
  formality_level: casual | polite | formal
  cultural_adaptation: boolean
```

## Output Contract

```yaml
deliverables:
  installed_packages: array[string]
  config_files: array[{path, content}]
  locale_files: array[{language, path, content}]
  components_modified: array[string]
  new_components: array[{name, path, code}]

translation_summary:
  languages_added: array[string]
  keys_created: number
  strings_translated: number
  rtl_support: boolean

validation_report:
  all_keys_present: boolean
  no_missing_translations: boolean
  seo_configured: boolean
  switcher_working: boolean

documentation:
  usage_guide: markdown
  adding_new_language: markdown
  adding_new_keys: markdown
```

## Integration Points

- **Cascades**: Integrates with landing page creation, feature development
- **Commands**: `/translate-site`, `/add-language`, `/i18n-setup`
- **Other Skills**: Works with web-cli-teleport (good for Web), seo-optimization

## Usage Examples

**Complete Landing Page Translation**:
```
Use i18n-automation to translate the Next.js landing page to Japanese, Spanish, and French.
Include SEO metadata and create a language switcher in the header.
```

**Add New Language**:
```
Add German (de) support to existing i18n setup. Use AI translation for initial version.
```

**Full i18n Setup**:
```
Set up complete internationalization for React app:
- Install react-i18next
- Support English, Japanese, Arabic (RTL)
- Extract all strings from components
- Generate translation keys
- Create language switcher
- Configure SEO metadata
```

## Best Practices

**Key Naming**:
1. Use descriptive, hierarchical keys: `landing.hero.title`
2. Group by page/component: `pricing.tier.pro.price`
3. Separate common strings: `common.buttons.submit`
4. Version keys if changing meaning: `welcome_v2`

**File Organization**:
1. One file per language: `en.json`, `ja.json`
2. OR namespace split: `en/common.json`, `en/landing.json`
3. Keep files in sync (same keys across languages)
4. Use TypeScript for type safety

**Translation Quality**:
1. Preserve placeholders exactly: `{name}`, `{count}`
2. Handle pluralization: `{count} item` vs `{count} items`
3. Format dates/numbers per locale
4. Consider cultural context, not just literal translation

**Performance**:
1. Lazy-load translations per route
2. Split large translation files by namespace
3. Cache translations in production
4. Use dynamic imports for rare languages

## Failure Modes & Mitigations

- **Missing translations**: Use fallback locale, log warnings
- **RTL layout breaks**: Use logical CSS properties, test thoroughly
- **SEO not working**: Verify alternate links, sitemap, hreflang tags
- **Wrong formality level**: Document target audience, review by native speaker
- **Placeholders broken**: Validate translation files, check for {variable} syntax

## Validation Checklist

- [ ] All target languages have complete locale files
- [ ] No missing translation keys
- [ ] Language switcher works on all pages
- [ ] SEO metadata translated
- [ ] RTL languages display correctly (if applicable)
- [ ] Pluralization works correctly
- [ ] Date/number formatting locale-aware
- [ ] No hardcoded strings remain
- [ ] Fallback locale configured
- [ ] Documentation updated

## Neural Training Integration

```yaml
training:
  pattern: program-of-thought
  feedback_collection: true
  success_metrics:
    - translation_accuracy
    - user_engagement_by_locale
    - seo_performance_by_language
    - completeness_score
```

---

**Quick Commands**:
- Next.js: `npm install next-intl`
- React: `npm install react-i18next i18next`
- Vue: `npm install vue-i18n`

**Pro Tips**:
- Use Claude Code Web for translation tasks (well-defined, one-off)
- AI translations good for MVP, professional for production
- Test RTL languages early if supporting Arabic/Hebrew
- Keep translation keys synchronized across all locales
- Consider loading translations from CMS for non-developers to update
