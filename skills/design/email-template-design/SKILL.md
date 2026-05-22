---
name: email-template-design
description: Design and build professional HTML email templates with inline CSS for broad email client compatibility. Use this skill when the user asks to create, design, or build email templates, newsletters, transactional emails (order confirmations, receipts, shipping notifications, password resets), marketing emails, welcome series, onboarding emails, abandoned cart emails, drip campaigns, or any HTML email layout. Covers responsive design, dark mode support, and compatibility with Gmail, Outlook (desktop + web), Apple Mail, Yahoo, and mobile clients.
---

# Email Template Design

Design production-ready HTML email templates using table-based layouts and inline CSS for maximum email client compatibility.

## Workflow

1. **Clarify purpose** - Determine the email type (marketing, transactional, lifecycle) and brand context
2. **Select base template** - Start from an asset template in `assets/` or build from scratch using the patterns below
3. **Build structure** - Use table-based layout with the boilerplate from `assets/base.html`
4. **Style inline** - Apply all CSS as inline styles; use `<style>` block only as progressive enhancement
5. **Test compatibility** - Review against the client quirks in `references/client-compatibility.md`
6. **Optimize** - Compress images, add alt text, verify dark mode, ensure accessibility

## Email Type Selection

| Type | Key characteristics | Template asset |
|------|-------------------|----------------|
| Marketing / Newsletter | Hero image, CTA buttons, multi-section content | `assets/marketing.html` |
| Transactional | Data-driven, minimal design, clear information hierarchy | `assets/transactional.html` |
| Lifecycle / Drip | Personal tone, single CTA, storytelling flow | `assets/lifecycle.html` |

## Core Architecture

Every email template follows this skeleton:

```html
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="format-detection" content="telephone=no,address=no,email=no,date=no,url=no">
  <title>{{email_title}}</title>
  <!--[if mso]>
  <noscript><xml>
    <o:OfficeDocumentSettings>
      <o:AllowPNG/>
      <o:PixelPerInch>96</o:PixelPerInch>
    </o:OfficeDocumentSettings>
  </xml></noscript>
  <![endif]-->
  <style>
    /* Reset — progressive enhancement only */
    table, td { mso-table-lspace:0pt; mso-table-rspace:0pt; }
    img { -ms-interpolation-mode:bicubic; border:0; height:auto; line-height:100%; outline:none; text-decoration:none; }
    body { margin:0; padding:0; width:100%!important; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }

    /* Dark mode */
    @media (prefers-color-scheme: dark) {
      .dark-bg { background-color: #1a1a2e !important; }
      .dark-text { color: #e0e0e0 !important; }
    }

    /* Responsive */
    @media only screen and (max-width: 600px) {
      .stack-column { display: block !important; width: 100% !important; max-width: 100% !important; }
      .mobile-padding { padding-left: 16px !important; padding-right: 16px !important; }
      .mobile-full-width { width: 100% !important; }
      .mobile-hide { display: none !important; }
      .mobile-center { text-align: center !important; }
    }
  </style>
</head>
<body style="margin:0; padding:0; background-color:#f4f4f4;">
  <!-- Preview text (hidden preheader) -->
  <div style="display:none; max-height:0; overflow:hidden;">
    {{preview_text}}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;
  </div>

  <!-- Outer wrapper -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f4f4;">
    <tr>
      <td align="center" style="padding: 20px 0;">
        <!-- Inner container (600px max) -->
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" class="mobile-full-width" style="background-color:#ffffff; border-radius:8px; overflow:hidden;">
          <!-- CONTENT ROWS GO HERE -->
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

## Essential Patterns

### CTA Buttons (Outlook-safe)

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
  <tr>
    <td align="center" style="border-radius:6px; background-color:#2563eb;">
      <!--[if mso]>
      <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="{{url}}" style="height:44px; width:200px; v-text-anchor:middle;" arcsize="14%" fill="true" stroke="false">
        <v:fill type="tile" color="#2563eb"/>
        <v:textbox inset="0,0,0,0"><center style="color:#ffffff; font-family:Arial,sans-serif; font-size:16px; font-weight:bold;">Button Text</center></v:textbox>
      </v:roundrect>
      <![endif]-->
      <!--[if !mso]><!-->
      <a href="{{url}}" style="display:inline-block; padding:12px 32px; font-family:Arial,Helvetica,sans-serif; font-size:16px; font-weight:bold; color:#ffffff; text-decoration:none; border-radius:6px; background-color:#2563eb;">Button Text</a>
      <!--<![endif]-->
    </td>
  </tr>
</table>
```

### Two-Column Layout (responsive)

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="padding: 20px;">
      <!--[if mso]><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td width="280" valign="top"><![endif]-->
      <div class="stack-column" style="display:inline-block; width:280px; vertical-align:top;">
        <!-- Left column content -->
      </div>
      <!--[if mso]></td><td width="20"></td><td width="280" valign="top"><![endif]-->
      <div class="stack-column" style="display:inline-block; width:280px; vertical-align:top;">
        <!-- Right column content -->
      </div>
      <!--[if mso]></td></tr></table><![endif]-->
    </td>
  </tr>
</table>
```

### Hero Image

```html
<tr>
  <td style="padding:0; line-height:0;">
    <img src="{{hero_image_url}}" alt="{{hero_alt}}" width="600" style="display:block; width:100%; max-width:600px; height:auto;" class="mobile-full-width">
  </td>
</tr>
```

## Design Rules

1. **600px max width** for the content container
2. **All critical styles inline** — `<style>` blocks are for progressive enhancement only (resets, dark mode, responsive)
3. **Tables for layout** — use `role="presentation"` on every layout table
4. **System-safe font stacks** — `font-family: Arial, Helvetica, sans-serif;` or `Georgia, 'Times New Roman', serif;`. Web fonts via `@import` work in Apple Mail, iOS Mail, and some Android clients only
5. **Images**: always set explicit `width`, `height:auto`, `display:block`, `border:0`, and meaningful `alt` text
6. **Backgrounds**: use inline `background-color`; background images require VML fallback for Outlook — see `references/client-compatibility.md`
7. **Spacing**: use `padding` on `<td>` cells, never `margin` on tables
8. **Links**: always use absolute URLs with `https://`
9. **Preheader text**: hidden preview text improves open rates; pad with `&#847;&zwnj;&nbsp;` to prevent email clients from pulling body content

## Accessibility

- Use semantic `lang` attribute on `<html>`
- Add `role="presentation"` to all layout tables
- Provide descriptive `alt` text for all images
- Maintain minimum **4.5:1** contrast ratio for text
- Use at least **14px** font size for body text
- Structure content in logical reading order (not reliant on visual layout)
- Include a plain-text version or web-view link

## Dark Mode

Support three strategies (apply all):
1. **`@media (prefers-color-scheme: dark)`** in `<style>` — works in Apple Mail, Outlook.com
2. **`color-scheme: light dark`** meta tag and CSS property — opts into native dark mode handling
3. **Transparent images** — use PNGs with transparency so logos adapt to dark backgrounds; provide light/dark logo variants when possible

For full dark mode quirks per client, see `references/client-compatibility.md`.

## Pre-Send Checklist

- [ ] All CSS is inline (use a CSS inliner tool if needed)
- [ ] Preview text is set and padded
- [ ] All images have `alt`, `width`, `display:block`
- [ ] CTA buttons use VML fallback for Outlook
- [ ] Links are absolute `https://` URLs
- [ ] Responsive breakpoint at 600px tested
- [ ] Dark mode classes applied to key elements
- [ ] Unsubscribe link present (required for marketing emails by CAN-SPAM / GDPR)
- [ ] Plain-text fallback available
- [ ] Total email size under 102KB (Gmail clipping threshold)
