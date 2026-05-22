---
name: nestjs-typescript-starter
description: Official NestJS starter with modular architecture and Jest testing.
---

# NestJS TypeScript Starter

The official NestJS starter with modular architecture and testing.

## Tech Stack

- **Framework**: NestJS
- **Language**: TypeScript
- **Testing**: Jest
- **Package Manager**: npm

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/nestjs/typescript-starter.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/nestjs/typescript-starter.git _temp_template
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
npm install
```

## Build

```bash
npm run build
```

## Development

```bash
npm run start:dev
```
