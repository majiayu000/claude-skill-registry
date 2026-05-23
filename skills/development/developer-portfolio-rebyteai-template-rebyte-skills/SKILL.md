---
name: developer-portfolio
description: Next.js 16 portfolio with Lottie animations, contact form (Email/Telegram), dev.to integration.
---

# Developer Portfolio Pro

A modern, responsive portfolio with Next.js, Lottie animations, contact form with Email/Telegram, and dev.to blog integration.

## Tech Stack

- **Framework**: Next.js 16 with App Router
- **React**: React 19
- **Styling**: Tailwind CSS 4
- **Animation**: Lottie
- **Package Manager**: pnpm
- **Output**: `.next` directory
- **Dev Port**: 3000

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/developer-portfolio-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/developer-portfolio-template.git _temp_template
mv _temp_template/* _temp_template/.* . 2>/dev/null || true
rm -rf _temp_template
```

### 2. Remove Git History (Optional)

```bash
rm -rf .git
git init
```

### 3. Install Dependencies

```bash
pnpm install
```

## Build

```bash
pnpm build
```

## Deploy

### Vercel (Recommended)

```bash
vercel pull --yes -t $VERCEL_TOKEN
vercel build --prod -t $VERCEL_TOKEN
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

### Netlify

```bash
netlify deploy --prod
```

## Customization

Edit content in `utils/data/`:
- `personal-data.js` - Name, bio, social links
- `experience.js` - Work history
- `projects-data.js` - Portfolio projects
- `skills.js` - Technical skills
- `educations.js` - Education background

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_GTM` | No | Google Tag Manager ID |
| `NEXT_PUBLIC_APP_URL` | Yes | Your portfolio's public URL |
| `TELEGRAM_BOT_TOKEN` | No | Telegram bot token for contact form |
| `TELEGRAM_CHAT_ID` | No | Telegram chat ID |
| `GMAIL_PASSKEY` | No | Gmail app password |
| `EMAIL_ADDRESS` | No | Gmail address for contact form |

## Development

```bash
pnpm dev
```

Opens at http://localhost:3000

Requires Node.js 18.17+ (Node.js 20+ recommended)
