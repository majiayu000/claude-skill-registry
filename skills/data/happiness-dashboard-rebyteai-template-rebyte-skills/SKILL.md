---
name: happiness-dashboard
description: Evidence framework data dashboard with DuckDB. Write SQL in markdown to create visualizations.
---

# Happiness Dashboard

An interactive data dashboard using Evidence framework - write SQL queries in markdown to create visualizations.

## Tech Stack

- **Framework**: Evidence
- **Database**: DuckDB (embedded)
- **Frontend**: Svelte
- **Package Manager**: pnpm
- **Output**: `build` directory
- **Dev Port**: 3000

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/happiness-dashboard-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/happiness-dashboard-template.git _temp_template
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

### 4. Process Data Sources

```bash
pnpm run sources
```

## Build

```bash
pnpm run build
```

Generates static site in `build/` directory.

## Deploy

### Vercel (Recommended)

```bash
vercel pull --yes -t $VERCEL_TOKEN
vercel build --prod -t $VERCEL_TOKEN
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

**Important:** Deploy from project root, not `build/` directory.

### Netlify

```bash
netlify deploy --prod --dir=build
```

## Data Sources

CSV files in `sources/happiness_score/`:
- `hs2024.csv` - Current year happiness data
- `hsArchive.csv` - Historical happiness data

## Notes

- **Use pnpm** (not npm) - `.npmrc` has `shamefully-hoist=true` for Evidence compatibility
- **Build locally** - Vercel/Netlify build can timeout due to DuckDB compilation (40+ min)
- Uses CSV files, no database setup needed
- Never run `pnpm run dev` in VM environment
