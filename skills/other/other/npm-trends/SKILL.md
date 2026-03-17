---
name: npm-trends
description: Fetch and compare npm package download statistics with trend analysis. Use when the user asks about npm trends, package popularity, download counts, growth rates, or wants to compare npm packages over time.
---

# npm Trends

Fetch and compare download statistics for npm packages using the official npm registry API.

## Usage

```bash
<your-skill-directory>/npm-trends/scripts/npm_trends.ts <package1> [package2] ... [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--period` | Time period: `last-day`, `last-week`, `last-month`, `last-year`. Default: `last-month` |
| `--range` | Custom date range: `YYYY-MM-DD:YYYY-MM-DD` (overrides `--period`) |
| `--daily` | Show daily breakdown (with `--range`) |
| `--trends` | Show weekly trends with growth analysis and ASCII chart |
| `--weeks` | Number of weeks for trend analysis (default: 12, max: 52) |

## Examples

**Compare packages (last month totals):**
```bash
<your-skill-directory>/npm-trends/scripts/npm_trends.ts skills add-skill
```

**Weekly trend analysis (recommended for comparison):**
```bash
<your-skill-directory>/npm-trends/scripts/npm_trends.ts skills add-skill --trends
```

**Extended trend analysis (6 months):**
```bash
<your-skill-directory>/npm-trends/scripts/npm_trends.ts react vue --trends --weeks 26
```

**Custom date range:**
```bash
<your-skill-directory>/npm-trends/scripts/npm_trends.ts express fastify --range 2025-01-01:2025-01-25
```

## Output

### Basic mode
- Total downloads and daily average
- Comparison ranking with bar chart

### Trends mode (`--trends`)
- Weekly download totals
- Growth rate (overall and recent 4 weeks)
- Momentum indicator (📈 accelerating, ➡️ steady, 📉 decelerating)
- ASCII chart showing weekly downloads
- Crossover analysis (when comparing 2 packages)
- Gap analysis showing which package is gaining ground

## API Reference

Uses the official npm downloads API:
- Point: `https://api.npmjs.org/downloads/point/{period}/{package}`
- Range: `https://api.npmjs.org/downloads/range/{start:end}/{package}`
