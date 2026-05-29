---
name: public
description: Generates public/ directory with static assets including favicons, app icons, and site.webmanifest for Progressive Web App (PWA) support.
---

# Public Folder Skill

## Purpose
Generate the `public/` directory with static assets including favicons, app icons, and web manifest for Progressive Web App (PWA) support.

## Input Parameters
- No user input required - uses standard favicon and icon files

## Output
Create the following files in the `public/` directory:
- `favicon.ico` - Main favicon
- `favicon-16x16.png` - 16x16 favicon
- `favicon-32x32.png` - 32x32 favicon
- `apple-touch-icon.png` - Apple touch icon (180x180)
- `android-chrome-192x192.png` - Android icon (192x192)
- `android-chrome-512x512.png` - Android icon (512x512)
- `site.webmanifest` - Web app manifest file

## Implementation
See: `examples.md` in this directory for implementation details and file examples.

## Notes
- The public folder contains static assets that are served directly without processing
- Favicons are referenced in `index.html` via link tags
- The site.webmanifest enables PWA features and Android app icon support
- These files should be customized for each application with brand-specific icons
- Icons support various device sizes and platforms (iOS, Android, web browsers)
- All files are served from the root path in production builds
