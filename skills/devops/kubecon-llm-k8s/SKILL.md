---
name: kubecon-llm-k8s
description: Slidev presentation about taming dependency chaos for LLM in Kubernetes.
---

# KubeCon LLM K8s Slides

A Slidev presentation about taming dependency chaos for LLM in Kubernetes.

## Tech Stack

- **Framework**: Slidev (Vue-based)
- **Icons**: Carbon, Logos, Simple Icons, DevIcon, Fluent, Twemoji
- **Package Manager**: pnpm
- **Output**: `dist` directory

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/kubecon-llm-k8s-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/kubecon-llm-k8s-template.git _temp_template
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

Use `npm run build` (not `build-base`) for standard deployment without custom base path.

## Deploy

### Vercel (Recommended)

```bash
vercel pull --yes -t $VERCEL_TOKEN
vercel build --prod -t $VERCEL_TOKEN
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

### Netlify

```bash
netlify deploy --prod --dir=dist
```

## Development

```bash
pnpm dev
```

Starts the Slidev server and opens the presentation in your browser. Edit slides in `slides.md`.
