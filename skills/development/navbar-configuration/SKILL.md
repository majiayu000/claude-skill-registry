---
name: navbar-configuration
description: Configure navbar menu items, logo, buttons, and styling. Sets up navigation from sitemap.md, ensures dropdown z-index is above content, configures buttons, and updates i18n. Dynamically finds navbar*.tsx component.
---

# Navbar Configuration

Configure the navbar component with proper navigation, z-index, and button visibility.

## Workflow

1. **Find Navbar Component** - Glob for `website/components/navbar*.tsx`
2. **Read Sitemap** - Get all pages from `docs/sitemap.md`
3. **Update Menu Items** - Configure links from sitemap using Next.js `<Link>`
4. **Fix Z-Index** - Ensure dropdowns appear above all content (z-50)
5. **Configure Buttons** - Set visibility and styles for primary/outline buttons
6. **Set Logo** - Text or image logo configuration
7. **Set Background** - Apply background color setting
8. **Update i18n** - Add/update keys in de.json and en.json

## Menu Configuration

### Standard Menu Items

Based on `docs/sitemap.md`, configure menu items:

```tsx
import Link from "next/link";

const menu: MenuItem[] = [
  { title: t("home"), url: "/" },
  {
    title: t("services"),
    url: "/dienstleistungen",
    items: [
      // Submenu items if needed
    ],
  },
  { title: t("about"), url: "/ueber-uns" },
  { title: t("contact"), url: "/kontakt" },
];
```

### Using Next.js Link

Replace ALL `<a>` tags with Next.js `<Link>` for internal navigation:

```tsx
import Link from "next/link";

// Internal links
<Link href={item.url}>{item.title}</Link>

// External links (social media, etc.) keep <a> with security attributes
<a href={item.url} target="_blank" rel="noopener noreferrer">
  {item.title}
</a>
```

## Link Styling

Navigation links should be simple text without button-like effects.

**IMPORTANT:** The shadcn `NavigationMenuLink` component has built-in `hover:bg-accent` styling. You MUST override this on the wrapper AND style the inner Link:

```tsx
<NavigationMenuLink asChild className="bg-transparent hover:bg-transparent focus:bg-transparent rounded-none p-0">
  <Link
    href={item.url}
    className="text-sm font-medium text-foreground hover:text-foreground/70 transition-colors px-3 py-2"
  >
    {item.title}
  </Link>
</NavigationMenuLink>
```

**On NavigationMenuLink (wrapper):**
- `bg-transparent` - removes default background
- `hover:bg-transparent` - removes hover background
- `focus:bg-transparent` - removes focus background
- `rounded-none` - removes rounded corners
- `p-0` - removes padding (apply to Link instead)

**On Link (inner):**
- `text-foreground` - default text color (NOT `text-primary`)
- `hover:text-foreground/70` - subtle opacity on hover
- `px-3 py-2` - spacing for click area

**Do NOT use on nav links:**
- `text-primary` (use `text-foreground` instead)
- `hover:bg-muted` or `hover:bg-accent` (no background on hover)
- `hover:underline` (no underline)
- `rounded-md` (no rounded corners)

## Z-Index Fix

### Dropdown Content

Add z-50 to NavigationMenuContent:

```tsx
<NavigationMenuContent className="z-50 ...other classes...">
```

### Mobile Sheet

Ensure Sheet has proper z-index:

```tsx
<SheetContent className="z-50 overflow-y-auto">
```

### Z-Index Hierarchy

| Element | Z-Index | Purpose |
|---------|---------|---------|
| Page content | z-0 | Regular content |
| Section overlays | z-10 | Overlay elements |
| Fixed elements | z-30 | Sticky headers |
| Dropdown menus | z-50 | Navigation dropdowns |
| Mobile sheet | z-50 | Mobile navigation |
| Modals | z-[100] | Dialog overlays |

## Button Configuration

### Button Visibility Options

Configure which buttons appear:

```tsx
const buttons = {
  showOutline: true,  // Contact button (outline variant)
  showPrimary: true,  // CTA button (primary variant)
};

// Render conditionally
{buttons.showOutline && (
  <Button asChild variant="outline" size="sm">
    <Link href="/kontakt">{t("contact")}</Link>
  </Button>
)}
{buttons.showPrimary && (
  <Button asChild size="sm">
    <Link href="/kontakt">{t("bookNow")}</Link>
  </Button>
)}
```

## Logo Configuration

### Text Logo

```tsx
const logo = {
  type: "text",
  url: "/",
  title: t("logo"),
};

<Link href={logo.url} className="flex items-center gap-2">
  <span className="font-serif text-xl">{logo.title}</span>
</Link>
```

### Image Logo

```tsx
import Image from "next/image";

const logo = {
  type: "image",
  url: "/",
  src: "/logo.svg",
  alt: t("logoAlt"),
  width: 120,
  height: 40,
};

<Link href={logo.url} className="flex items-center gap-2">
  <Image src={logo.src} alt={logo.alt} width={logo.width} height={logo.height} />
</Link>
```

## Background Configuration

### Static Positioning (Default)

Navbar scrolls with page:

```tsx
<section className="py-4 bg-background">
```

### Background Options

```tsx
// Solid background
<section className="py-4 bg-background">

// Muted background
<section className="py-4 bg-muted">

// Transparent
<section className="py-4 bg-transparent">
```

## i18n Keys

### Required Keys in de.json/en.json

```json
{
  "navbar": {
    "logo": "Salon Elegance",
    "logoAlt": "Salon Elegance Logo",
    "home": "Startseite",
    "services": "Dienstleistungen",
    "servicesDescription": "Alle unsere Dienstleistungen",
    "about": "Über uns",
    "contact": "Kontakt",
    "bookNow": "Termin buchen"
  }
}
```

## Checklist

- [ ] Found navbar component (navbar*.tsx)
- [ ] Menu items match docs/sitemap.md pages
- [ ] All internal links use Next.js `<Link>` component
- [ ] NavigationMenuContent has z-50 class
- [ ] SheetContent has z-50 class
- [ ] Button visibility configured as needed
- [ ] Logo renders correctly (text or image)
- [ ] Background color applied
- [ ] All navbar keys in de.json
- [ ] All navbar keys in en.json
- [ ] Mobile menu tested and working
