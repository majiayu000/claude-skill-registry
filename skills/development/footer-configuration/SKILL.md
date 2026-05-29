---
name: footer-configuration
description: Configure footer navigation links for SEO completeness. Sets up all pages (Homepage, Services, About, Contact, Impressum, Datenschutz) in organized groups. Dynamically finds footer*.tsx component. Updates i18n with all footer keys.
---

# Footer Configuration

Configure footer links to include ALL pages for complete SEO coverage.

## Workflow

1. **Find Footer Component** - Glob for `website/components/footer*.tsx`
2. **Read Sitemap** - Get all pages from `docs/sitemap.md`
3. **Organize Links** - Group into Navigation, Services, Legal, Social
4. **Update Component** - Apply link structure to footer component
5. **Add Contact Info** - Phone, email, address
6. **Configure Branding** - Logo/name and copyright
7. **Update i18n** - Add all keys to de.json and en.json

## Link Groups

### Navigation Group

Main pages that should always be linked:

```tsx
const navigation = [
  { name: t("navigation.home"), href: "/" },
  { name: t("navigation.services"), href: "/dienstleistungen" },
  { name: t("navigation.about"), href: "/ueber-uns" },
  { name: t("navigation.contact"), href: "/kontakt" },
];
```

### Services Group (Optional)

If services page has subsections:

```tsx
const services = [
  { name: t("services.hair"), href: "/dienstleistungen#haare" },
  { name: t("services.nails"), href: "/dienstleistungen#naegel" },
  { name: t("services.facials"), href: "/dienstleistungen#gesicht" },
];
```

### Legal Group

Required legal pages for Swiss/German compliance:

```tsx
const legal = [
  { name: t("legal.privacy"), href: "/datenschutz" },
  { name: t("legal.imprint"), href: "/impressum" },
];
```

### Social Group

External social media links:

```tsx
const social = [
  { name: t("social.instagram"), href: "https://instagram.com/salonname", icon: Instagram },
  { name: t("social.facebook"), href: "https://facebook.com/salonname", icon: Facebook },
];
```

## Contact Information

Add contact details section:

```tsx
const contact = {
  phone: "+41 44 XXX XX XX",
  email: "info@salon-elegance.ch",
  address: {
    street: "Musterstrasse 123",
    city: "8001 Zürich",
    country: "Schweiz",
  },
};
```

## Using Next.js Link

Replace `<a>` with Next.js `<Link>` for internal navigation:

```tsx
import Link from "next/link";

// Internal links
<Link href={item.href}>{item.name}</Link>

// External links (social media)
<a
  href={item.href}
  target="_blank"
  rel="noopener noreferrer"
>
  {item.name}
</a>
```

## List Styling

Footer lists must NOT have bullet points. Always add `list-none p-0`:

```tsx
<ul className="list-none space-y-3 p-0">
  {links.map((link) => (
    <li key={link.text}>
      <Link href={link.url} className="text-sm text-foreground/70 hover:text-foreground transition-colors">
        {link.text}
      </Link>
    </li>
  ))}
</ul>
```

## Link Colors

Use `text-foreground` or opacity variants, NOT `text-primary`:

- `text-foreground/70` - muted links
- `hover:text-foreground` - hover state (full opacity)
- `text-foreground/60` - subtle text like copyright

**Do NOT use:**
- `text-primary` (reserved for CTA buttons, not navigation)
- `hover:underline` (no underlines)

## SEO Importance

All pages MUST be linked in footer for:

1. **Crawlability** - Search engines find all pages
2. **Internal Linking** - Distributes page authority
3. **User Navigation** - Users expect footer navigation
4. **Accessibility** - Alternative to main navigation

### Required Pages

| Page | Route | Group |
|------|-------|-------|
| Homepage | `/` | Navigation |
| Services | `/dienstleistungen` | Navigation |
| About | `/ueber-uns` | Navigation |
| Contact | `/kontakt` | Navigation |
| Privacy Policy | `/datenschutz` | Legal |
| Imprint | `/impressum` | Legal |

## Branding Section

### Business Name

```tsx
<p className="font-serif text-4xl md:text-6xl">
  {t("brand")}
</p>
```

### Copyright

```tsx
<p className="text-sm text-muted-foreground">
  {t("copyright")}
</p>
```

## i18n Keys

### Required Keys in de.json

```json
{
  "footer": {
    "brand": "Salon Elegance",
    "tagline": "Ihr Salon in Zürich",
    "navigation": {
      "title": "Navigation",
      "home": "Startseite",
      "services": "Dienstleistungen",
      "about": "Über uns",
      "contact": "Kontakt"
    },
    "services": {
      "title": "Dienstleistungen",
      "hair": "Haare",
      "nails": "Nägel",
      "facials": "Gesicht"
    },
    "legal": {
      "title": "Rechtliches",
      "privacy": "Datenschutz",
      "imprint": "Impressum"
    },
    "social": {
      "title": "Social Media",
      "instagram": "Instagram",
      "facebook": "Facebook"
    },
    "contact": {
      "title": "Kontakt",
      "phone": "Telefon",
      "email": "E-Mail",
      "address": "Adresse"
    },
    "copyright": "© 2024 Salon Elegance Zürich. Alle Rechte vorbehalten."
  }
}
```

### Required Keys in en.json

```json
{
  "footer": {
    "brand": "Salon Elegance",
    "tagline": "Your salon in Zurich",
    "navigation": {
      "title": "Navigation",
      "home": "Home",
      "services": "Services",
      "about": "About Us",
      "contact": "Contact"
    },
    "services": {
      "title": "Services",
      "hair": "Hair",
      "nails": "Nails",
      "facials": "Facials"
    },
    "legal": {
      "title": "Legal",
      "privacy": "Privacy Policy",
      "imprint": "Legal Notice"
    },
    "social": {
      "title": "Social Media",
      "instagram": "Instagram",
      "facebook": "Facebook"
    },
    "contact": {
      "title": "Contact",
      "phone": "Phone",
      "email": "Email",
      "address": "Address"
    },
    "copyright": "© 2024 Salon Elegance Zurich. All rights reserved."
  }
}
```

## Checklist

- [ ] Found footer component (footer*.tsx)
- [ ] Homepage linked in navigation group
- [ ] Services page linked in navigation group
- [ ] About page linked in navigation group
- [ ] Contact page linked in navigation group
- [ ] Datenschutz (Privacy) in legal group
- [ ] Impressum (Imprint) in legal group
- [ ] Social media links with external attributes
- [ ] All internal links use Next.js `<Link>`
- [ ] Contact information displayed (phone, email, address)
- [ ] Brand name displayed
- [ ] Copyright with current year
- [ ] All footer keys in de.json
- [ ] All footer keys in en.json
