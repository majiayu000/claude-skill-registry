---
name: dzen
description: Publish articles and posts to Dzen.ru (Yandex Zen). Supports text, images, and videos. Requires session cookies and a CSRF token from a logged-in browser session.
---

# Dzen Publisher

This skill allows you to programmatically publish content to Dzen.ru using a browser-mimic approach.

## Setup

Dzen does not provide a public API for posting. This skill uses your active browser session.

### 1. Get Authentication Data

1.  Log in to [dzen.ru](https://dzen.ru) in your browser.
2.  Open the **Network** tab in Developer Tools (F12).
3.  Go to [dzen.ru/profile/editor](https://dzen.ru/profile/editor).
4.  Find any request to `dzen.ru` (e.g., `entry`, `list`, or even the main page).
5.  In the **Headers** tab:
    *   Find the `Cookie` header. Copy its value.
    *   Find the `x-csrf-token` header. Copy its value.

### 2. Create Config File

Create a file named `dzen_config.json` in the workspace with the following structure:

```json
{
  "cookies": {
    "SESSION_ID": "your_session_id_from_cookies",
    "zen_sso_checked": "...",
    "...": "..."
  },
  "csrf_token": "your_csrf_token"
}
```

## Usage

### Publishing a Post

Use the `publish.py` script to create a post.

```bash
python3 scripts/publish.py --title "My Title" --text "My Content" --media image.jpg video.mp4 --config dzen_config.json
```

### Supported Media

- **Images**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`.
- **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`.

Media files are uploaded automatically before the final publication.

## Tips

- **Session Expiry**: If the publication fails with a 403 error, your cookies or CSRF token may have expired. Refresh them from the browser.
- **CSRF Token**: Ensure the `X-Csrf-Token` matches the one in your config. It is mandatory for all POST requests.
