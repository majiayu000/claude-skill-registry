---
name: lighthouse-ci-integrator
description: Integrates Lighthouse CI for automated performance testing, Core Web Vitals tracking, and regression detection in CI/CD pipelines. Use when user asks to "setup Lighthouse CI", "add performance testing", "monitor Core Web Vitals", or "prevent performance regressions".
allowed-tools: [Write, Read, Bash, Glob]
---

# Lighthouse CI Integrator

Sets up Lighthouse CI to automatically test performance, accessibility, SEO, and best practices in your CI/CD pipeline with budget enforcement and trend tracking.

## When to Use

- "Setup Lighthouse CI"
- "Add performance testing to CI/CD"
- "Monitor Core Web Vitals"
- "Prevent performance regressions"
- "Track Lighthouse scores"
- "Setup performance budgets"

## Instructions

### 1. Install Lighthouse CI

```bash
npm install --save-dev @lhci/cli
# or
yarn add --dev @lhci/cli
```

### 2. Create Configuration File

**lighthouserc.js:**
```javascript
module.exports = {
  ci: {
    collect: {
      // URLs to test
      url: [
        'http://test-frontend:3000/',
        'http://test-frontend:3000/about',
        'http://test-frontend:3000/products',
      ],
      // Number of runs per URL
      numberOfRuns: 3,
      // Start server before collecting
      startServerCommand: 'npm run serve',
      startServerReadyPattern: 'Server listening',
      // Or use static directory
      staticDistDir: './dist',
      // Settings
      settings: {
        preset: 'desktop', // or 'mobile'
        // Throttling
        throttling: {
          rttMs: 40,
          throughputKbps: 10240,
          cpuSlowdownMultiplier: 1,
        },
        // Screen emulation
        screenEmulation: {
          mobile: false,
          width: 1350,
          height: 940,
          deviceScaleFactor: 1,
          disabled: false,
        },
      },
    },
    upload: {
      target: 'temporary-public-storage',
      // Or use LHCI server
      // target: 'lhci',
      // serverBaseUrl: 'https://your-lhci-server.com',
      // token: process.env.LHCI_TOKEN,
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        // Performance
        'categories:performance': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['warn', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['warn', { maxNumericValue: 300 }],
        'speed-index': ['warn', { maxNumericValue: 3000 }],
        'interactive': ['warn', { maxNumericValue: 3500 }],

        // Accessibility
        'categories:accessibility': ['error', { minScore: 0.95 }],

        // Best Practices
        'categories:best-practices': ['error', { minScore: 0.9 }],

        // SEO
        'categories:seo': ['warn', { minScore: 0.9 }],

        // Resource budgets
        'resource-summary:script:size': ['error', { maxNumericValue: 500000 }],
        'resource-summary:stylesheet:size': ['warn', { maxNumericValue: 100000 }],
        'resource-summary:image:size': ['warn', { maxNumericValue: 1000000 }],
        'resource-summary:font:size': ['warn', { maxNumericValue: 100000 }],
        'total-byte-weight': ['warn', { maxNumericValue: 2000000 }],

        // Other metrics
        'uses-http2': 'error',
        'uses-webp-images': 'warn',
        'offscreen-images': 'warn',
        'unused-css-rules': 'warn',
        'unused-javascript': 'warn',
        'modern-image-formats': 'warn',
        'uses-optimized-images': 'warn',
        'uses-text-compression': 'error',
        'uses-responsive-images': 'warn',
      },
    },
  },
};
```

**Mobile Configuration:**
```javascript
// lighthouserc.mobile.js
module.exports = {
  ci: {
    collect: {
      url: ['http://test-frontend:3000/'],
      numberOfRuns: 3,
      settings: {
        preset: 'mobile',
        throttling: {
          rttMs: 150,
          throughputKbps: 1638,
          cpuSlowdownMultiplier: 4,
        },
        screenEmulation: {
          mobile: true,
          width: 412,
          height: 823,
          deviceScaleFactor: 2.625,
          disabled: false,
        },
        formFactor: 'mobile',
      },
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.85 }],
        'first-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 4000 }],
      },
    },
  },
};
```

### 3. Add npm Scripts

**package.json:**
```json
{
  "scripts": {
    "build": "next build",
    "serve": "next start",
    "lhci:collect": "lhci collect",
    "lhci:assert": "lhci assert",
    "lhci:upload": "lhci upload",
    "lhci:autorun": "lhci autorun",
    "lhci:mobile": "lhci autorun --config=lighthouserc.mobile.js",
    "lhci:desktop": "lhci autorun --config=lighthouserc.js"
  }
}
```

### 4. GitHub Actions Integration

**.github/workflows/lighthouse-ci.yml:**
```yaml
name: Lighthouse CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.sha }}

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Run Lighthouse CI (Desktop)
        run: npm run lhci:desktop
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}

      - name: Run Lighthouse CI (Mobile)
        run: npm run lhci:mobile
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}

      - name: Upload Lighthouse results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: lighthouse-results
          path: .lighthouseci
```

**With deployment preview (Vercel/Netlify):**
```yaml
name: Lighthouse CI with Preview

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Wait for Vercel Preview
        uses: patrickedqvist/wait-for-vercel-preview@v1.2.0
        id: wait-for-vercel
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          max_timeout: 300

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Lighthouse CI
        run: npm install -g @lhci/cli

      - name: Run Lighthouse CI
        run: |
          lhci autorun --url=${{ steps.wait-for-vercel.outputs.url }}
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

### 5. GitLab CI Integration

**.gitlab-ci.yml:**
```yaml
lighthouse:
  stage: test
  image: node:18
  before_script:
    - npm ci
  script:
    - npm run build
    - npm run lhci:autorun
  artifacts:
    paths:
      - .lighthouseci
    expire_in: 1 week
  only:
    - merge_requests
    - main
```

### 6. Setup LHCI Server (Optional)

**Docker Compose for LHCI Server:**
```yaml
# docker-compose.lhci.yml
version: '3.8'

services:
  lhci-server:
    image: patrickhulce/lhci-server:latest
    ports:
      - '9001:9001'
    environment:
      LHCI_STORAGE_METHOD: sql
      LHCI_STORAGE_SQL_DIALECT: postgres
      LHCI_STORAGE_SQL_DATABASE: lighthouse
      LHCI_STORAGE_SQL_USERNAME: postgres
      LHCI_STORAGE_SQL_PASSWORD: postgres
      LHCI_STORAGE_SQL_HOST: postgres
    depends_on:
      - postgres

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: lighthouse
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - lhci-postgres-data:/var/lib/postgresql/data

volumes:
  lhci-postgres-data:
```

**Start server:**
```bash
docker-compose -f docker-compose.lhci.yml up -d
```

**Create project:**
```bash
lhci wizard
# Follow prompts to create project and get token
```

### 7. Budget.json (Alternative Format)

**budget.json:**
```json
[
  {
    "path": "/*",
    "timings": [
      {
        "metric": "interactive",
        "budget": 3500
      },
      {
        "metric": "first-meaningful-paint",
        "budget": 2000
      }
    ],
    "resourceSizes": [
      {
        "resourceType": "script",
        "budget": 300
      },
      {
        "resourceType": "image",
        "budget": 500
      },
      {
        "resourceType": "stylesheet",
        "budget": 100
      },
      {
        "resourceType": "font",
        "budget": 100
      },
      {
        "resourceType": "total",
        "budget": 1000
      }
    ],
    "resourceCounts": [
      {
        "resourceType": "third-party",
        "budget": 10
      }
    ]
  }
]
```

### 8. Custom Audits

**custom-audit.js:**
```javascript
// custom-audit.js
class CustomAudit extends Lighthouse.Audit {
  static get meta() {
    return {
      id: 'custom-performance-check',
      title: 'Custom Performance Check',
      failureTitle: 'Custom performance check failed',
      description: 'Validates custom performance requirements',
      requiredArtifacts: ['devtoolsLogs', 'traces'],
    };
  }

  static audit(artifacts, context) {
    // Custom audit logic
    const score = 1; // 0-1
    return {
      score,
      numericValue: 100,
      displayValue: '100ms',
    };
  }
}

module.exports = CustomAudit;
```

**Use in lighthouserc.js:**
```javascript
module.exports = {
  ci: {
    collect: {
      settings: {
        plugins: ['./custom-audit.js'],
      },
    },
  },
};
```

### 9. PR Comments Integration

**Comment on PR with results:**
```yaml
# .github/workflows/lighthouse-ci.yml
- name: Comment PR with results
  uses: treosh/lighthouse-ci-action@v9
  with:
    urls: |
      https://example.com
      https://example.com/about
    uploadArtifacts: true
    temporaryPublicStorage: true
```

### 10. Monitoring and Alerts

**Slack notifications:**
```yaml
# .github/workflows/lighthouse-ci.yml
- name: Notify Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Lighthouse CI failed! Performance regression detected.'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

**Email notifications:**
```yaml
- name: Send email notification
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Lighthouse CI Failed
    body: Performance regression detected in ${{ github.repository }}
    to: team@example.com
```

### 11. Generate Reports

**HTML Report:**
```bash
# Generate HTML report locally
lhci collect
lhci upload --target=filesystem --outputDir=./lighthouse-reports

# Open report
open ./lighthouse-reports/index.html
```

**JSON Report:**
```javascript
// parse-lighthouse-results.js
const fs = require('fs');

const results = JSON.parse(fs.readFileSync('.lighthouseci/manifest.json'));

results.forEach(result => {
  const report = JSON.parse(fs.readFileSync(result.jsonPath));

  console.log('URL:', report.finalUrl);
  console.log('Performance:', report.categories.performance.score * 100);
  console.log('Accessibility:', report.categories.accessibility.score * 100);
  console.log('Best Practices:', report.categories['best-practices'].score * 100);
  console.log('SEO:', report.categories.seo.score * 100);
  console.log('---');
});
```

### 12. Performance Budgets

**Strict budgets:**
```javascript
assertions: {
  // Core Web Vitals (strict)
  'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
  'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
  'first-input-delay': ['error', { maxNumericValue: 100 }],

  // Page weight
  'total-byte-weight': ['error', { maxNumericValue: 1500000 }], // 1.5MB
  'dom-size': ['warn', { maxNumericValue: 800 }],

  // JavaScript
  'bootup-time': ['warn', { maxNumericValue: 3500 }],
  'mainthread-work-breakdown': ['warn', { maxNumericValue: 4000 }],
}
```

### Best Practices

**DO:**
- Run Lighthouse CI on every PR
- Set realistic performance budgets
- Test both mobile and desktop
- Monitor trends over time
- Use temporary storage for PRs
- Setup LHCI server for history
- Test multiple pages
- Include authentication flows

**DON'T:**
- Set budgets too strict initially
- Only test homepage
- Ignore accessibility scores
- Skip mobile testing
- Test only in production
- Forget to warm up the server
- Ignore flaky metrics

## Checklist

- [ ] Lighthouse CI installed
- [ ] Configuration file created
- [ ] Performance budgets set
- [ ] CI/CD integration added
- [ ] Multiple URLs configured
- [ ] Mobile + Desktop testing
- [ ] Assertions configured
- [ ] PR comments enabled
- [ ] Monitoring setup
- [ ] Team notified of new checks
