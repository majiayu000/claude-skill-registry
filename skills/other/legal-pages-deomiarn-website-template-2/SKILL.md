---
name: legal-pages
description: Create Impressum and Datenschutz pages with legally required content for German/Swiss websites. Provides templates with all mandatory sections for DSG/DSGVO compliance. Use when creating legal pages, checking compliance, or user asks for "impressum", "datenschutz", "legal pages", "privacy policy", "imprint".
---

# Legal Pages

Create compliant Impressum (Legal Notice) and Datenschutz (Privacy Policy) pages.

## Workflow

1. User provides company details (name, address, contact, UID, etc.)
2. Create page files at `app/[locale]/impressum/` and `app/[locale]/datenschutz/`
3. Add translations to messages/de.json and messages/en.json
4. Simple text-based layout with Navbar2 and Footer16

## Required Input

Ask user for:
- Company name and legal form
- Address (street, city, postal code, country)
- Contact (phone, email)
- UID/MwSt-Nummer (Switzerland) or USt-IdNr (Germany)
- Responsible person name
- Hosting provider name
- Analytics tools used (if any)

## Page Structure

```tsx
// app/[locale]/impressum/page.tsx
"use client";

import { useTranslations } from "next-intl";
import { Navbar2 } from "@/components/navbar2";
import { Footer16 } from "@/components/footer16";

export default function ImpressumPage() {
  const t = useTranslations("impressum");

  return (
    <main>
      <Navbar2 />
      <section className="container py-24 max-w-3xl">
        <h1 className="mb-8">{t("title")}</h1>

        <h2>{t("companyInfo.title")}</h2>
        <p>{t("companyInfo.content")}</p>

        <h2>{t("contact.title")}</h2>
        <p>{t("contact.content")}</p>

        {/* More sections... */}
      </section>
      <Footer16 />
    </main>
  );
}
```

## Templates

See references/impressum-template.md for required Impressum sections.
See references/datenschutz-template.md for DSGVO/DSG privacy policy sections.

## Legal Compliance

**Swiss (DSG):**
- UID-Nummer required
- DSG (Datenschutzgesetz) compliance

**German/EU (DSGVO):**
- § 5 TMG requirements
- DSGVO Art. 13/14 information duties
- User rights (Art. 15-22)

## Styling

- Use `container max-w-3xl` for readable text width
- No inline typography classes on headings
- Simple paragraph text, no complex components
