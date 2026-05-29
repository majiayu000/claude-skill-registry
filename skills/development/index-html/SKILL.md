---
name: index-html
description: Generates index.html as the application entry point. Includes meta tags, favicon links, and root div for Vue app mounting.
---

# Index HTML Skill

## Purpose
Generate the `index.html` file as the entry point for the application.

## Input Parameters
- `application_title`: The application title for the page title (e.g., "Inventory Manager")

## Output
Create the file: `index.html`


## Template
See: `examples.md` in this directory for complete template and detailed examples.

## Notes
- HTML entry point for the Vue application
- Includes multiple favicon sizes for different devices
- Progressive Web App (PWA) ready with manifest link
- IE compatibility meta tag for edge cases
- Responsive viewport meta tag for mobile devices
- Noscript message for users without JavaScript
- The #app div is where Vue mounts the application
- Vite automatically injects built files during development and production
