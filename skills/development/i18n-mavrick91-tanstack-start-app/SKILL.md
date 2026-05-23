---
name: i18n
description: Internationalization with i18next for UI translations and JSONB for database content. Use when adding translations, working with localized content, or implementing multi-language features.
---

# i18n Helper

Complete internationalization guide for this application.

## Supported Languages

| Code | Language          | URL Pattern    |
| ---- | ----------------- | -------------- |
| `en` | English (default) | `/en/products` |
| `fr` | French            | `/fr/products` |
| `id` | Indonesian        | `/id/products` |

## Two Types of i18n

### 1. UI Translations (i18next)

Static strings in the interface: buttons, labels, messages.

```typescript
import { useTranslation } from 'react-i18next'

function MyComponent() {
  const { t } = useTranslation()

  return (
    <div>
      <h1>{t('Welcome')}</h1>
      <button>{t('Add to Cart')}</button>
    </div>
  )
}
```

### 2. Database Content (JSONB)

Dynamic content stored in the database: product names, descriptions.

```typescript
type LocalizedString = { en: string; fr?: string; id?: string }

// In database schema
name: jsonb('name').$type<LocalizedString>().notNull()

// Usage
const productName = product.name[currentLang] || product.name.en
```

## Adding UI Translations

### 1. Add Keys to Locale Files

```json
// src/i18n/locales/en.json
{
  "Welcome": "Welcome",
  "Add to Cart": "Add to Cart",
  "{{count}} items": "{{count}} items",
  "{{count}} items_one": "1 item",
  "{{count}} items_other": "{{count}} items"
}

// src/i18n/locales/fr.json
{
  "Welcome": "Bienvenue",
  "Add to Cart": "Ajouter au panier",
  "{{count}} items_one": "1 article",
  "{{count}} items_other": "{{count}} articles"
}

// src/i18n/locales/id.json
{
  "Welcome": "Selamat datang",
  "Add to Cart": "Tambah ke Keranjang",
  "{{count}} items": "{{count}} barang"
}
```

### 2. Use in Components

```typescript
import { useTranslation } from 'react-i18next'

function CartSummary({ itemCount }: { itemCount: number }) {
  const { t } = useTranslation()

  return (
    <div>
      <h2>{t('Cart')}</h2>
      <p>{t('{{count}} items', { count: itemCount })}</p>
    </div>
  )
}
```

### 3. Scan for Missing Keys

```bash
yarn locales:scan
```

## Translation Patterns

### Basic Translation

```typescript
t('Hello') // "Hello" or localized version
```

### With Interpolation

```typescript
t('Hello {{name}}', { name: 'John' }) // "Hello John"
t('Price: {{price}}', { price: '$99.99' }) // "Price: $99.99"
```

### Pluralization

```json
// en.json
{
  "{{count}} selected_one": "1 selected",
  "{{count}} selected_other": "{{count}} selected",
  "{{count}} selected_zero": "None selected"
}
```

```typescript
t('{{count}} selected', { count: 0 }) // "None selected"
t('{{count}} selected', { count: 1 }) // "1 selected"
t('{{count}} selected', { count: 5 }) // "5 selected"
```

### Nested Keys

```json
{
  "errors": {
    "required": "This field is required",
    "email": "Please enter a valid email"
  }
}
```

```typescript
t('errors.required') // "This field is required"
```

## Database Localized Content

### Schema Definition

```typescript
// src/db/schema.ts
type LocalizedString = { en: string; fr?: string; id?: string }

export const products = pgTable('products', {
  id: uuid('id').defaultRandom().primaryKey(),
  name: jsonb('name').$type<LocalizedString>().notNull(),
  description: jsonb('description').$type<LocalizedString>(),
  metaTitle: jsonb('meta_title').$type<LocalizedString>(),
  metaDescription: jsonb('meta_description').$type<LocalizedString>(),
})
```

### Creating Localized Content

```typescript
// API endpoint
const body = await request.json()
const { name, description } = body

// Validate English is present
if (!name?.en?.trim()) {
  return simpleErrorResponse('Name (English) is required')
}

await db.insert(products).values({
  name: {
    en: name.en,
    fr: name.fr || undefined,
    id: name.id || undefined,
  },
  description: description || undefined,
})
```

### Displaying Localized Content

```typescript
import { useParams } from '@tanstack/react-router'

function ProductName({ product }: { product: Product }) {
  const { lang } = useParams({ from: '/$lang' })

  // Fallback to English if translation missing
  const name = product.name[lang as keyof typeof product.name] || product.name.en

  return <h1>{name}</h1>
}
```

### Helper Function

```typescript
// src/lib/i18n.ts
export function getLocalizedValue<T extends Record<string, unknown>>(
  obj: T | null | undefined,
  lang: string,
  fallback: string = '',
): string {
  if (!obj) return fallback

  const value = obj[lang as keyof T] || obj['en' as keyof T]
  return typeof value === 'string' ? value : fallback
}

// Usage
const name = getLocalizedValue(product.name, lang)
const description = getLocalizedValue(
  product.description,
  lang,
  'No description',
)
```

## Multi-Language Admin Forms

### Tab-Based Locale Editor

```typescript
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const LOCALES = ['en', 'fr', 'id'] as const

function LocalizedInput({
  value,
  onChange,
  label,
}: {
  value: LocalizedString
  onChange: (value: LocalizedString) => void
  label: string
}) {
  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <Tabs defaultValue="en">
        <TabsList>
          {LOCALES.map((locale) => (
            <TabsTrigger key={locale} value={locale}>
              {locale.toUpperCase()}
              {locale === 'en' && <span className="text-red-500 ml-1">*</span>}
            </TabsTrigger>
          ))}
        </TabsList>
        {LOCALES.map((locale) => (
          <TabsContent key={locale} value={locale}>
            <Input
              value={value[locale] || ''}
              onChange={(e) =>
                onChange({ ...value, [locale]: e.target.value })
              }
              placeholder={`${label} (${locale.toUpperCase()})`}
            />
          </TabsContent>
        ))}
      </Tabs>
    </div>
  )
}
```

### Usage in Product Form

```typescript
function ProductForm() {
  const [name, setName] = useState<LocalizedString>({ en: '' })
  const [description, setDescription] = useState<LocalizedString>({ en: '' })

  return (
    <form>
      <LocalizedInput
        value={name}
        onChange={setName}
        label="Product Name"
      />
      <LocalizedInput
        value={description}
        onChange={setDescription}
        label="Description"
      />
    </form>
  )
}
```

## URL-Based Language Switching

### Route Structure

```
src/routes/
├── $lang/                    # Language prefix
│   ├── index.tsx             # /$lang/
│   ├── products/
│   │   ├── index.tsx         # /$lang/products
│   │   └── $handle.tsx       # /$lang/products/:handle
│   └── cart.tsx              # /$lang/cart
```

### Language Switcher Component

```typescript
import { Link, useParams, useLocation } from '@tanstack/react-router'

const languages = [
  { code: 'en', label: 'English' },
  { code: 'fr', label: 'Français' },
  { code: 'id', label: 'Indonesia' },
]

function LanguageSwitcher() {
  const { lang } = useParams({ from: '/$lang' })
  const location = useLocation()

  // Replace language in current path
  const switchPath = (newLang: string) => {
    return location.pathname.replace(`/${lang}`, `/${newLang}`)
  }

  return (
    <div className="flex gap-2">
      {languages.map((language) => (
        <Link
          key={language.code}
          to={switchPath(language.code)}
          className={lang === language.code ? 'font-bold' : ''}
        >
          {language.label}
        </Link>
      ))}
    </div>
  )
}
```

### Sync i18next with URL

```typescript
// In layout component
import { useEffect } from 'react'
import { useParams } from '@tanstack/react-router'
import { changeLanguage } from '@/lib/i18n'

function Layout() {
  const { lang } = useParams({ from: '/$lang' })

  useEffect(() => {
    changeLanguage(lang)
  }, [lang])

  return <Outlet />
}
```

## SEO with Localized Content

```typescript
function ProductPage({ product }: { product: Product }) {
  const { lang } = useParams({ from: '/$lang' })

  const title = getLocalizedValue(product.metaTitle, lang)
    || getLocalizedValue(product.name, lang)
  const description = getLocalizedValue(product.metaDescription, lang)
    || getLocalizedValue(product.description, lang)

  return (
    <>
      <head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <link rel="alternate" hreflang="en" href={`/en/products/${product.handle}`} />
        <link rel="alternate" hreflang="fr" href={`/fr/products/${product.handle}`} />
        <link rel="alternate" hreflang="id" href={`/id/products/${product.handle}`} />
      </head>
      {/* ... */}
    </>
  )
}
```

## Common Translation Keys

```json
{
  "common": {
    "Save": "Save",
    "Cancel": "Cancel",
    "Delete": "Delete",
    "Edit": "Edit",
    "Loading": "Loading...",
    "Error": "Error",
    "Success": "Success"
  },
  "validation": {
    "Required": "This field is required",
    "Invalid email": "Please enter a valid email",
    "Too short": "Must be at least {{min}} characters"
  },
  "cart": {
    "Add to Cart": "Add to Cart",
    "Remove": "Remove",
    "Empty cart": "Your cart is empty",
    "Checkout": "Checkout"
  }
}
```

## See Also

- `src/lib/i18n.ts` - i18next setup
- `src/i18n/locales/` - Translation files
- `src/routes/$lang/` - Localized routes
- `forms` skill - Localized form inputs
