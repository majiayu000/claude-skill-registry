---
name: seo-analytics
description: Generate visual SEO analysis reports using Google PageSpeed Insights API. Use when user asks to analyze website performance, SEO scores, Core Web Vitals, or page speed. Outputs an interactive HTML report with charts and actionable recommendations.
---

# SEO Analytics Skill

Generate comprehensive SEO and performance analysis reports for any website using Google PageSpeed Insights API.

## When to Use

- "Analyze the SEO of https://example.com"
- "Check the performance of my website"
- "Generate a Core Web Vitals report for..."
- "What's the page speed score of..."
- "SEO audit for..."

## API Key Requirement

**IMPORTANT**: This skill requires a Google PageSpeed Insights API key. If the user has not provided an API key, you MUST ask for one before proceeding.

### When No API Key is Provided

If the user requests SEO analysis without providing an API key, respond with:

---

**To run SEO analysis, I need a Google PageSpeed Insights API key.**

**How to get your API key (takes ~2 minutes):**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** > **Library**
4. Search for "**PageSpeed Insights API**" and click **Enable**
5. Go to **APIs & Services** > **Credentials**
6. Click **Create Credentials** > **API Key**
7. Copy your new API key

Once you have the key, provide it and I'll run the analysis.

---

### API Key Usage

The API key can be provided in two ways:
1. As a command line argument: `npx ts-node analyze.ts <URL> <API_KEY>`
2. As an environment variable: `PAGESPEED_API_KEY`

## Quick Start

```
User: "Analyze https://eng0.ai"

# If no API key provided, ask user for one first

# With API key:
Output:
- ./seo-report.html (interactive report with charts)
- Console summary with key metrics
```

## How to Execute

### Step 1: Run the Analysis Script

```bash
npx ts-node analyze.ts https://example.com YOUR_API_KEY
```

Or with environment variable:
```bash
PAGESPEED_API_KEY=your_key npx ts-node analyze.ts https://example.com
```

### Step 2: Inline Execution (Alternative)

Create and run `analyze.ts` in the current directory:

```typescript
// analyze.ts - SEO Analysis Script
const url = process.argv[2];
const apiKey = process.argv[3] || process.env.PAGESPEED_API_KEY;

if (!url) {
  console.error('Usage: npx ts-node analyze.ts <URL> [API_KEY]');
  console.error('Or set PAGESPEED_API_KEY environment variable');
  process.exit(1);
}

interface AuditResult {
  title?: string;
  description?: string;
  score?: number | null;
  displayValue?: string;
  numericValue?: number;
}

interface PageSpeedResult {
  lighthouseResult: {
    categories: {
      performance: { score: number };
      accessibility: { score: number };
      'best-practices': { score: number };
      seo: { score: number };
    };
    audits: {
      [key: string]: AuditResult;
    };
  };
}

async function analyzeUrl(targetUrl: string, strategy: 'mobile' | 'desktop'): Promise<PageSpeedResult> {
  let apiUrl = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${encodeURIComponent(targetUrl)}&strategy=${strategy}&category=performance&category=accessibility&category=best-practices&category=seo`;

  if (apiKey) {
    apiUrl += `&key=${apiKey}`;
  }

  console.log(`Analyzing ${strategy}...`);
  const response = await fetch(apiUrl);
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<PageSpeedResult>;
}

function getScoreColor(score: number): string {
  if (score >= 90) return '#0cce6b';
  if (score >= 50) return '#ffa400';
  return '#ff4e42';
}

function generateReport(mobile: PageSpeedResult, desktop: PageSpeedResult, targetUrl: string): string {
  const m = mobile.lighthouseResult;
  const d = desktop.lighthouseResult;

  const mobileScores = {
    performance: Math.round(m.categories.performance.score * 100),
    accessibility: Math.round(m.categories.accessibility.score * 100),
    bestPractices: Math.round(m.categories['best-practices'].score * 100),
    seo: Math.round(m.categories.seo.score * 100),
  };

  const desktopScores = {
    performance: Math.round(d.categories.performance.score * 100),
    accessibility: Math.round(d.categories.accessibility.score * 100),
    bestPractices: Math.round(d.categories['best-practices'].score * 100),
    seo: Math.round(d.categories.seo.score * 100),
  };

  const webVitals = {
    mobile: {
      lcp: m.audits['largest-contentful-paint'],
      tbt: m.audits['total-blocking-time'],
      cls: m.audits['cumulative-layout-shift'],
      fcp: m.audits['first-contentful-paint'],
      si: m.audits['speed-index'],
      tti: m.audits['interactive'],
    },
    desktop: {
      lcp: d.audits['largest-contentful-paint'],
      tbt: d.audits['total-blocking-time'],
      cls: d.audits['cumulative-layout-shift'],
      fcp: d.audits['first-contentful-paint'],
      si: d.audits['speed-index'],
      tti: d.audits['interactive'],
    },
  };

  // Extract top opportunities
  const opportunities: string[] = [];
  for (const [key, audit] of Object.entries(m.audits)) {
    if (audit.score !== undefined && audit.score < 0.9 && audit.title && audit.description) {
      opportunities.push(`<li><strong>${audit.title}</strong>: ${audit.description.split('.')[0]}.</li>`);
    }
  }

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SEO Report - ${targetUrl}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }
    .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
    h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .url { color: #666; font-size: 0.9rem; margin-bottom: 2rem; word-break: break-all; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
    .card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .card h2 { font-size: 1.1rem; margin-bottom: 1rem; color: #444; }
    .scores { display: flex; justify-content: space-around; text-align: center; }
    .score-item { display: flex; flex-direction: column; align-items: center; }
    .score-circle { width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: bold; color: white; margin-bottom: 0.5rem; }
    .score-label { font-size: 0.75rem; color: #666; }
    .vitals-table { width: 100%; border-collapse: collapse; }
    .vitals-table th, .vitals-table td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #eee; }
    .vitals-table th { font-weight: 500; color: #666; font-size: 0.85rem; }
    .good { color: #0cce6b; }
    .needs-improvement { color: #ffa400; }
    .poor { color: #ff4e42; }
    .chart-container { position: relative; height: 300px; }
    .opportunities { list-style: none; }
    .opportunities li { padding: 0.75rem 0; border-bottom: 1px solid #eee; font-size: 0.9rem; }
    .opportunities li:last-child { border-bottom: none; }
    .timestamp { text-align: center; color: #999; font-size: 0.8rem; margin-top: 2rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1>SEO Analysis Report</h1>
    <p class="url">${targetUrl}</p>

    <div class="grid">
      <div class="card">
        <h2>Mobile Scores</h2>
        <div class="scores">
          <div class="score-item">
            <div class="score-circle" style="background: ${getScoreColor(mobileScores.performance)}">${mobileScores.performance}</div>
            <span class="score-label">Performance</span>
          </div>
          <div class="score-item">
            <div class="score-circle" style="background: ${getScoreColor(mobileScores.accessibility)}">${mobileScores.accessibility}</div>
            <span class="score-label">Accessibility</span>
          </div>
          <div class="score-item">
            <div class="score-circle" style="background: ${getScoreColor(mobileScores.bestPractices)}">${mobileScores.bestPractices}</div>
            <span class="score-label">Best Practices</span>
          </div>
          <div class="score-item">
            <div class="score-circle" style="background: ${getScoreColor(mobileScores.seo)}">${mobileScores.seo}</div>
            <span class="score-label">SEO</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>Desktop Scores</h2>
        <div class="scores">
          <div class="score-item">
            <div class="score-circle" style="background: ${getScoreColor(desktopScores.performance)}">${desktopScores.performance}</div>
            <span class="score-label">Performance</span>
          </div>
          <div class="score-item">
            <div class="score-circle" style="background: ${getScoreColor(desktopScores.accessibility)}">${desktopScores.accessibility}</div>
            <span class="score-label">Accessibility</span>
          </div>
          <div class="score-item">
            <div class="score-circle" style="background: ${getScoreColor(desktopScores.bestPractices)}">${desktopScores.bestPractices}</div>
            <span class="score-label">Best Practices</span>
          </div>
          <div class="score-item">
            <div class="score-circle" style="background: ${getScoreColor(desktopScores.seo)}">${desktopScores.seo}</div>
            <span class="score-label">SEO</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <h2>Core Web Vitals - Mobile</h2>
        <table class="vitals-table">
          <tr><th>Metric</th><th>Value</th><th>Status</th></tr>
          <tr>
            <td>Largest Contentful Paint (LCP)</td>
            <td>${webVitals.mobile.lcp?.displayValue || 'N/A'}</td>
            <td class="${(webVitals.mobile.lcp?.numericValue || 0) <= 2500 ? 'good' : (webVitals.mobile.lcp?.numericValue || 0) <= 4000 ? 'needs-improvement' : 'poor'}">${(webVitals.mobile.lcp?.numericValue || 0) <= 2500 ? 'Good' : (webVitals.mobile.lcp?.numericValue || 0) <= 4000 ? 'Needs Work' : 'Poor'}</td>
          </tr>
          <tr>
            <td>Total Blocking Time (TBT)</td>
            <td>${webVitals.mobile.tbt?.displayValue || 'N/A'}</td>
            <td class="${(webVitals.mobile.tbt?.numericValue || 0) <= 200 ? 'good' : (webVitals.mobile.tbt?.numericValue || 0) <= 600 ? 'needs-improvement' : 'poor'}">${(webVitals.mobile.tbt?.numericValue || 0) <= 200 ? 'Good' : (webVitals.mobile.tbt?.numericValue || 0) <= 600 ? 'Needs Work' : 'Poor'}</td>
          </tr>
          <tr>
            <td>Cumulative Layout Shift (CLS)</td>
            <td>${webVitals.mobile.cls?.displayValue || 'N/A'}</td>
            <td class="${(webVitals.mobile.cls?.numericValue || 0) <= 0.1 ? 'good' : (webVitals.mobile.cls?.numericValue || 0) <= 0.25 ? 'needs-improvement' : 'poor'}">${(webVitals.mobile.cls?.numericValue || 0) <= 0.1 ? 'Good' : (webVitals.mobile.cls?.numericValue || 0) <= 0.25 ? 'Needs Work' : 'Poor'}</td>
          </tr>
          <tr>
            <td>First Contentful Paint (FCP)</td>
            <td>${webVitals.mobile.fcp?.displayValue || 'N/A'}</td>
            <td class="${(webVitals.mobile.fcp?.numericValue || 0) <= 1800 ? 'good' : (webVitals.mobile.fcp?.numericValue || 0) <= 3000 ? 'needs-improvement' : 'poor'}">${(webVitals.mobile.fcp?.numericValue || 0) <= 1800 ? 'Good' : (webVitals.mobile.fcp?.numericValue || 0) <= 3000 ? 'Needs Work' : 'Poor'}</td>
          </tr>
          <tr>
            <td>Speed Index</td>
            <td>${webVitals.mobile.si?.displayValue || 'N/A'}</td>
            <td class="${(webVitals.mobile.si?.numericValue || 0) <= 3400 ? 'good' : (webVitals.mobile.si?.numericValue || 0) <= 5800 ? 'needs-improvement' : 'poor'}">${(webVitals.mobile.si?.numericValue || 0) <= 3400 ? 'Good' : (webVitals.mobile.si?.numericValue || 0) <= 5800 ? 'Needs Work' : 'Poor'}</td>
          </tr>
          <tr>
            <td>Time to Interactive (TTI)</td>
            <td>${webVitals.mobile.tti?.displayValue || 'N/A'}</td>
            <td class="${(webVitals.mobile.tti?.numericValue || 0) <= 3800 ? 'good' : (webVitals.mobile.tti?.numericValue || 0) <= 7300 ? 'needs-improvement' : 'poor'}">${(webVitals.mobile.tti?.numericValue || 0) <= 3800 ? 'Good' : (webVitals.mobile.tti?.numericValue || 0) <= 7300 ? 'Needs Work' : 'Poor'}</td>
          </tr>
        </table>
      </div>

      <div class="card">
        <h2>Score Comparison</h2>
        <div class="chart-container">
          <canvas id="comparisonChart"></canvas>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Optimization Opportunities</h2>
      <ul class="opportunities">
        ${opportunities.slice(0, 10).join('\n        ') || '<li>No significant issues found. Great job!</li>'}
      </ul>
    </div>

    <p class="timestamp">Generated on ${new Date().toLocaleString()}</p>
  </div>

  <script>
    new Chart(document.getElementById('comparisonChart'), {
      type: 'radar',
      data: {
        labels: ['Performance', 'Accessibility', 'Best Practices', 'SEO'],
        datasets: [
          {
            label: 'Mobile',
            data: [${mobileScores.performance}, ${mobileScores.accessibility}, ${mobileScores.bestPractices}, ${mobileScores.seo}],
            borderColor: '#4285f4',
            backgroundColor: 'rgba(66, 133, 244, 0.2)',
          },
          {
            label: 'Desktop',
            data: [${desktopScores.performance}, ${desktopScores.accessibility}, ${desktopScores.bestPractices}, ${desktopScores.seo}],
            borderColor: '#34a853',
            backgroundColor: 'rgba(52, 168, 83, 0.2)',
          }
        ]
      },
      options: {
        scales: { r: { beginAtZero: true, max: 100 } },
        plugins: { legend: { position: 'bottom' } }
      }
    });
  </script>
</body>
</html>`;
}

async function main() {
  try {
    console.log('Starting SEO analysis for:', url);
    console.log('');

    // Sequential requests to avoid rate limiting
    const mobile = await analyzeUrl(url, 'mobile');
    const desktop = await analyzeUrl(url, 'desktop');

    const report = generateReport(mobile, desktop, url);

    const fs = await import('fs');
    const outputPath = './seo-report.html';
    fs.writeFileSync(outputPath, report);

    // Print summary
    const m = mobile.lighthouseResult;
    const d = desktop.lighthouseResult;

    console.log('');
    console.log('=== SEO Analysis Complete ===');
    console.log('');
    console.log('Mobile Scores:');
    console.log(`  Performance:    ${Math.round(m.categories.performance.score * 100)}/100`);
    console.log(`  Accessibility:  ${Math.round(m.categories.accessibility.score * 100)}/100`);
    console.log(`  Best Practices: ${Math.round(m.categories['best-practices'].score * 100)}/100`);
    console.log(`  SEO:            ${Math.round(m.categories.seo.score * 100)}/100`);
    console.log('');
    console.log('Desktop Scores:');
    console.log(`  Performance:    ${Math.round(d.categories.performance.score * 100)}/100`);
    console.log(`  Accessibility:  ${Math.round(d.categories.accessibility.score * 100)}/100`);
    console.log(`  Best Practices: ${Math.round(d.categories['best-practices'].score * 100)}/100`);
    console.log(`  SEO:            ${Math.round(d.categories.seo.score * 100)}/100`);
    console.log('');
    console.log('Core Web Vitals (Mobile):');
    console.log(`  LCP: ${m.audits['largest-contentful-paint']?.displayValue || 'N/A'}`);
    console.log(`  TBT: ${m.audits['total-blocking-time']?.displayValue || 'N/A'}`);
    console.log(`  CLS: ${m.audits['cumulative-layout-shift']?.displayValue || 'N/A'}`);
    console.log('');
    console.log(`Report saved to: ${outputPath}`);
    console.log('Open the HTML file in a browser to view the interactive report.');

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
```

Run with:
```bash
npx ts-node analyze.ts https://eng0.ai YOUR_API_KEY
```

## Output

The skill generates:
1. **Console Summary** - Quick overview of all scores
2. **seo-report.html** - Interactive HTML report with:
   - Mobile & Desktop score cards
   - Core Web Vitals table with status indicators
   - Radar chart comparing mobile vs desktop
   - Top optimization opportunities

## Metrics Explained

### Lighthouse Scores (0-100)
- **Performance**: Page load speed and interactivity
- **Accessibility**: How accessible the page is to users with disabilities
- **Best Practices**: Modern web development standards
- **SEO**: Search engine optimization basics

### Core Web Vitals
| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| TBT (Total Blocking Time) | < 200ms | 200-600ms | > 600ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |

## API Details

Uses Google PageSpeed Insights API v5:
- **Free**: No API key required for basic usage
- **Rate Limit**: ~25 requests per 100 seconds
- **Data**: Real Lighthouse audit results

## Example Output

```
=== SEO Analysis Complete ===

Mobile Scores:
  Performance:    89/100
  Accessibility:  95/100
  Best Practices: 100/100
  SEO:            91/100

Core Web Vitals (Mobile):
  LCP: 1.8 s
  TBT: 150 ms
  CLS: 0.02

Report saved to: ./seo-report.html
```
