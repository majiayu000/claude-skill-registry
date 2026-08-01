---
name: quality-gates
description: '> Skill Purpose: Automated quality thresholds and enforcement patterns'
---

# Quality Gates

> **Skill Purpose:** Automated quality thresholds and enforcement patterns

---

## Core Skill Pattern

**Objective:** Establish automated quality gates that prevent low-quality code from progressing through the development pipeline.

**Universal Pattern:**
1. Define quality metrics and thresholds
2. Create automated quality check pipelines
3. Set up gate enforcement and failure handling
4. Establish quality reporting and trend analysis
5. Create quality improvement and remediation procedures

**Key Decisions (Project-Specific):**
- Quality metrics and threshold values
- Gate enforcement strictness and exceptions
- Reporting frequency and audience
- Integration with CI/CD pipeline
- Team accountability and improvement processes

---

## Project-Specific Implementation Notes

**Customize per project:**
- Quality thresholds based on project maturity
- Metrics based on team and stakeholder needs
- Enforcement based on release cadence and risk tolerance
- Reporting based on team size and management needs
- Integration with existing development and deployment workflows

---

## Example Implementation (Next.js Quality Gates Pattern)

> **Note:** This is an example pattern. Adapt quality metrics and thresholds based on your specific project requirements and quality standards.

### Prerequisites (Example)
- Project initialized
- Quality measurement tools available
- Development pipeline established

---

## Example: Next.js Quality Gates Implementation

> **Framework-Specific Example:** This demonstrates the pattern using Next.js quality metrics. Adapt for your tech stack and quality standards.

### 1. Install Quality Gate Dependencies

```bash
# Install quality gate tools
npm install -D @codecov/codecov-node bundlephobia-cli size-limit

# Install additional analysis tools
npm install -D webpack-bundle-analyzer @next/bundle-analyzer
npm install -D lighthouse-ci

# Install performance monitoring
npm install -D @vercel/ncc
npm install -D npm-check-updates
```

### 2. Create Quality Gate Configuration

Create `quality-gates.config.js`:

```javascript
// Quality gates configuration for Zeus framework
module.exports = {
  // Code quality thresholds
  codeQuality: {
    // ESLint thresholds
    eslint: {
      maxErrors: 0,
      maxWarnings: 0,
      rules: {
        // Critical rules that must pass
        'no-unused-vars': 'error',
        'no-undef': 'error',
        'no-unreachable': 'error',
        'no-console': 'warn', // Allow in development, warn in production
      },
    },

    // Prettier compliance
    prettier: {
      check: true,
      enforce: true,
    },

    // TypeScript strictness
    typescript: {
      strict: true,
      noImplicitAny: true,
      noImplicitReturns: true,
    },
  },

  // Test coverage thresholds
  coverage: {
    global: {
      statements: 80,
      branches: 80,
      functions: 80,
      lines: 80,
    },
    // Per-file thresholds
    files: {
      '**/*.ts': {
        statements: 85,
        branches: 85,
        functions: 85,
        lines: 85,
      },
      '**/*.tsx': {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80,
      },
    },
    // Exclude certain files from coverage
    exclude: [
      '**/*.d.ts',
      '**/*.config.js',
      '**/*.config.ts',
      '**/stories/**',
      '**/__tests__/**',
      '**/test/**',
      '**/spec/**',
    ],
  },

  // Performance thresholds
  performance: {
    // Bundle size limits (in bytes)
    bundleSize: {
      'main.js': 250000,      // 250KB
      'vendor.js': 300000,    // 300KB
      'framework.js': 50000,  // 50KB
    },

    // Build performance
    buildTime: {
      maxDuration: 300000, // 5 minutes in milliseconds
    },

    // Lighthouse scores
    lighthouse: {
      performance: 90,
      accessibility: 95,
      'best-practices': 90,
      seo: 90,
    },
  },

  // Security thresholds
  security: {
    // Vulnerability thresholds
    vulnerabilities: {
      high: 0,
      moderate: 0,
      low: 5,
    },

    // Dependency audit
    audit: {
      failOn: ['moderate', 'high', 'critical'],
    },
  },

  // Documentation requirements
  documentation: {
    // JSDoc coverage
    jsdocCoverage: {
      functions: 80,
      classes: 90,
      variables: 60,
    },

    // README requirements
    readme: {
      required: true,
      sections: [
        'Installation',
        'Usage',
        'API',
        'Contributing',
        'License',
      ],
    },
  },

  // Code complexity metrics
  complexity: {
    // Cyclomatic complexity
    cyclomaticComplexity: {
      max: 10,
      warn: 7,
    },

    // Cognitive complexity
    cognitiveComplexity: {
      max: 15,
      warn: 10,
    },

    // Function length
    functionLength: {
      max: 50,
      warn: 30,
    },

    // File length
    fileLength: {
      max: 300,
      warn: 200,
    },
  },

  // Integration requirements
  integration: {
    // API compatibility
    apiCompatibility: {
      version: '1.0.0',
      breakingChanges: false,
    },

    // Database migrations
    migrations: {
      reversible: true,
      tested: true,
    },
  },

  // Deployment requirements
  deployment: {
    // Environment parity
    environmentParity: {
      dev: 'staging',
      staging: 'production',
    },

    // Health checks
    healthChecks: {
      endpoints: ['/health', '/api/health'],
      responseTime: 1000, // 1 second
    },
  },
};
```

### 3. Create Quality Gate Runner

Create `scripts/quality-gates.js`:

```javascript
#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const config = require('../quality-gates.config');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m',
};

function colorLog(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

class QualityGateRunner {
  constructor() {
    this.results = [];
    this.startTime = Date.now();
  }

  runCommand(command, description, options = {}) {
    const startTime = Date.now();

    try {
      colorLog(`🔍 Running: ${description}`, 'blue');

      const output = execSync(command, {
        encoding: 'utf8',
        stdio: options.quiet ? 'pipe' : 'inherit',
        maxBuffer: 1024 * 1024 * 10, // 10MB buffer
      });

      const duration = Date.now() - startTime;

      this.results.push({
        name: description,
        status: 'passed',
        duration,
        output: options.quiet ? output : undefined,
      });

      colorLog(`✅ ${description} - PASSED (${duration}ms)`, 'green');
      return { success: true, output, duration };
    } catch (error) {
      const duration = Date.now() - startTime;

      this.results.push({
        name: description,
        status: 'failed',
        duration,
        error: error.message,
        output: options.quiet ? error.stdout : undefined,
      });

      colorLog(`❌ ${description} - FAILED (${duration}ms)`, 'red');
      if (!options.quiet) {
        colorLog(`Error: ${error.message}`, 'red');
      }

      return { success: false, error: error.message, duration };
    }
  }

  async checkCodeQuality() {
    colorLog('\n📝 Checking Code Quality', 'magenta');
    colorLog('========================', 'magenta');

    // TypeScript compilation
    this.runCommand('npm run type-check', 'TypeScript compilation');

    // ESLint
    this.runCommand('npm run lint', 'ESLint linting');

    // Prettier formatting
    this.runCommand('npm run format:check', 'Prettier formatting');

    // Code complexity (if tools available)
    try {
      this.runCommand('npx complexity-report src/', 'Code complexity analysis');
    } catch (error) {
      colorLog('⚠️  Code complexity analysis not available', 'yellow');
    }
  }

  async checkTestCoverage() {
    colorLog('\n🧪 Checking Test Coverage', 'magenta');
    colorLog('=======================', 'magenta');

    const result = this.runCommand('npm run test:coverage', 'Test coverage', { quiet: true });

    if (result.success) {
      // Parse coverage report
      try {
        const coveragePath = 'coverage/coverage-summary.json';
        if (fs.existsSync(coveragePath)) {
          const coverage = JSON.parse(fs.readFileSync(coveragePath, 'utf8'));

          colorLog('\n📊 Coverage Summary:', 'cyan');
          const thresholds = config.coverage.global;

          Object.entries(thresholds).forEach(([metric, threshold]) => {
            const coveragePercent = coverage.total[metric]?.pct || 0;
            const status = coveragePercent >= threshold ? '✅' : '❌';
            const color = coveragePercent >= threshold ? 'green' : 'red';

            colorLog(`   ${status} ${metric}: ${coveragePercent}% (required: ${threshold}%)`, color);

            if (coveragePercent < threshold) {
              this.results.push({
                name: `Coverage threshold: ${metric}`,
                status: 'failed',
                error: `${coveragePercent}% < ${threshold}%`,
              });
            }
          });
        }
      } catch (error) {
        colorLog('⚠️  Could not parse coverage report', 'yellow');
      }
    }
  }

  async checkPerformance() {
    colorLog('\n⚡ Checking Performance', 'magenta');
    colorLog('=====================', 'magenta');

    // Build performance
    const buildStart = Date.now();
    const buildResult = this.runCommand('npm run build', 'Build performance');
    const buildDuration = Date.now() - buildStart;

    if (buildDuration > config.performance.buildTime.maxDuration) {
      this.results.push({
        name: 'Build time',
        status: 'failed',
        error: `${buildDuration}ms > ${config.performance.buildTime.maxDuration}ms`,
      });
    }

    // Bundle size analysis
    if (fs.existsSync('.next')) {
      try {
        const bundleStats = this.analyzeBundleSize();
        Object.entries(config.performance.bundleSize).forEach(([file, maxSize]) => {
          const actualSize = bundleStats[file] || 0;
          const status = actualSize <= maxSize ? '✅' : '❌';
          const color = actualSize <= maxSize ? 'green' : 'red';

          colorLog(`   ${status} ${file}: ${this.formatBytes(actualSize)} (max: ${this.formatBytes(maxSize)})`, color);

          if (actualSize > maxSize) {
            this.results.push({
              name: `Bundle size: ${file}`,
              status: 'failed',
              error: `${this.formatBytes(actualSize)} > ${this.formatBytes(maxSize)}`,
            });
          }
        });
      } catch (error) {
        colorLog('⚠️  Bundle size analysis failed', 'yellow');
      }
    }
  }

  async checkSecurity() {
    colorLog('\n🔒 Checking Security', 'magenta');
    colorLog('==================', 'magenta');

    // Security audit
    const auditResult = this.runCommand('npm audit --json', 'Security audit', { quiet: true });

    if (auditResult.success) {
      try {
        const audit = JSON.parse(auditResult.output);
        const vulnerabilities = audit.vulnerabilities || {};

        const thresholds = config.security.vulnerabilities;
        let failed = false;

        Object.entries(thresholds).forEach(([level, maxAllowed]) => {
          const count = vulnerabilities[level] || 0;
          const status = count <= maxAllowed ? '✅' : '❌';
          const color = count <= maxAllowed ? 'green' : 'red';

          colorLog(`   ${status} ${level}: ${count} (max: ${maxAllowed})`, color);

          if (count > maxAllowed) {
            failed = true;
          }
        });

        if (failed) {
          this.results.push({
            name: 'Security audit',
            status: 'failed',
            error: 'Vulnerability thresholds exceeded',
          });
        }
      } catch (error) {
        colorLog('⚠️  Could not parse security audit', 'yellow');
      }
    }
  }

  analyzeBundleSize() {
    const stats = {};

    try {
      // Analyze .next build output
      const buildDir = '.next';
      if (fs.existsSync(buildDir)) {
        const files = this.getAllFiles(buildDir, '.js');

        files.forEach(file => {
          const size = fs.statSync(file).size;
          const name = path.basename(file);
          stats[name] = (stats[name] || 0) + size;
        });
      }
    } catch (error) {
      colorLog('Bundle size analysis failed', 'red');
    }

    return stats;
  }

  getAllFiles(dir, extension) {
    const files = [];

    function traverse(currentDir) {
      const items = fs.readdirSync(currentDir);

      for (const item of items) {
        const fullPath = path.join(currentDir, item);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
          traverse(fullPath);
        } else if (item.endsWith(extension)) {
          files.push(fullPath);
        }
      }
    }

    traverse(dir);
    return files;
  }

  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  generateReport() {
    const totalDuration = Date.now() - this.startTime;
    const passed = this.results.filter(r => r.status === 'passed').length;
    const failed = this.results.filter(r => r.status === 'failed').length;

    colorLog('\n📊 Quality Gates Report', 'magenta');
    colorLog('======================', 'magenta');

    colorLog(`Total Duration: ${totalDuration}ms`, 'cyan');
    colorLog(`Passed: ${passed}`, 'green');
    colorLog(`Failed: ${failed}`, failed > 0 ? 'red' : 'green');

    if (failed > 0) {
      colorLog('\n❌ Failed Checks:', 'red');
      this.results
        .filter(r => r.status === 'failed')
        .forEach(result => {
          colorLog(`   • ${result.name}: ${result.error}`, 'red');
        });
    }

    // Save detailed report
    const report = {
      timestamp: new Date().toISOString(),
      duration: totalDuration,
      results: this.results,
      summary: {
        passed,
        failed,
        total: this.results.length,
      },
    };

    try {
      fs.writeFileSync('quality-gates-report.json', JSON.stringify(report, null, 2));
      colorLog('\n📄 Detailed report saved to: quality-gates-report.json', 'cyan');
    } catch (error) {
      colorLog('⚠️  Could not save detailed report', 'yellow');
    }

    return failed === 0;
  }

  async run() {
    colorLog('🚀 Running Zeus Framework Quality Gates', 'magenta');
    colorLog('=====================================', 'magenta');

    try {
      await this.checkCodeQuality();
      await this.checkTestCoverage();
      await this.checkPerformance();
      await this.checkSecurity();

      const success = this.generateReport();

      if (success) {
        colorLog('\n✅ All quality gates passed!', 'green');
        process.exit(0);
      } else {
        colorLog('\n❌ Quality gates failed!', 'red');
        process.exit(1);
      }
    } catch (error) {
      colorLog(`\n💥 Quality gates execution failed: ${error.message}`, 'red');
      process.exit(1);
    }
  }
}

// Main execution
if (require.main === module) {
  const runner = new QualityGateRunner();
  runner.run();
}

module.exports = QualityGateRunner;
```

### 4. Create CI Quality Gates Script

Create `scripts/ci-quality-gates.js`:

```javascript
#!/usr/bin/env node

const QualityGateRunner = require('./quality-gates');

class CIQualityGateRunner extends QualityGateRunner {
  async run() {
    colorLog('🚀 Running CI Quality Gates', 'magenta');
    colorLog('========================', 'magenta');

    // CI-specific checks
    await this.checkCodeQuality();
    await this.checkTestCoverage();
    await this.checkPerformance();
    await this.checkSecurity();

    // Additional CI checks
    await this.checkDependencies();
    await this.checkDocumentation();
    await this.checkIntegration();

    const success = this.generateReport();

    if (success) {
      colorLog('\n✅ CI quality gates passed!', 'green');
      process.exit(0);
    } else {
      colorLog('\n❌ CI quality gates failed!', 'red');
      process.exit(1);
    }
  }

  async checkDependencies() {
    colorLog('\n📦 Checking Dependencies', 'magenta');
    colorLog('=====================', 'magenta');

    // Check for outdated dependencies
    this.runCommand('npm-check-updates --dep', 'Outdated dependencies check', { quiet: true });

    // Check for security updates
    this.runCommand('npm audit --audit-level moderate', 'Security updates check');
  }

  async checkDocumentation() {
    colorLog('\n📚 Checking Documentation', 'magenta');
    colorLog('========================', 'magenta');

    // Check README exists
    if (fs.existsSync('README.md')) {
      colorLog('✅ README.md exists', 'green');
    } else {
      this.results.push({
        name: 'README.md',
        status: 'failed',
        error: 'README.md not found',
      });
    }

    // Check API documentation
    if (fs.existsSync('docs/api.md')) {
      colorLog('✅ API documentation exists', 'green');
    } else {
      colorLog('⚠️  API documentation not found', 'yellow');
    }
  }

  async checkIntegration() {
    colorLog('\n🔗 Checking Integration', 'magenta');
    colorLog('=====================', 'magenta');

    // Check environment variables
    const requiredEnvVars = [
      'NEXT_PUBLIC_SUPABASE_URL',
      'NEXTAUTH_SECRET',
      'NEXT_PUBLIC_APP_URL',
    ];

    const missingVars = requiredEnvVars.filter(varName => !process.env[varName]);

    if (missingVars.length === 0) {
      colorLog('✅ Required environment variables present', 'green');
    } else {
      this.results.push({
        name: 'Environment variables',
        status: 'failed',
        error: `Missing: ${missingVars.join(', ')}`,
      });
    }
  }
}

if (require.main === module) {
  const runner = new CIQualityGateRunner();
  runner.run();
}

module.exports = CIQualityGateRunner;
```

### 5. Create Pre-Deployment Quality Gates

Create `scripts/pre-deployment-gates.js`:

```javascript
#!/usr/bin/env node

const QualityGateRunner = require('./quality-gates');

class PreDeploymentGateRunner extends QualityGateRunner {
  async run() {
    colorLog('🚀 Running Pre-Deployment Quality Gates', 'magenta');
    colorLog('=====================================', 'magenta');

    // Pre-deployment specific checks
    await this.checkCodeQuality();
    await this.checkTestCoverage();
    await this.checkPerformance();
    await this.checkSecurity();
    await this.checkDeploymentReadiness();

    const success = this.generateReport();

    if (success) {
      colorLog('\n✅ Pre-deployment quality gates passed!', 'green');
      process.exit(0);
    } else {
      colorLog('\n❌ Pre-deployment quality gates failed!', 'red');
      process.exit(1);
    }
  }

  async checkDeploymentReadiness() {
    colorLog('\n🚀 Checking Deployment Readiness', 'magenta');
    colorLog('=============================', 'magenta');

    // Check build artifacts
    if (fs.existsSync('.next')) {
      colorLog('✅ Build artifacts exist', 'green');
    } else {
      this.results.push({
        name: 'Build artifacts',
        status: 'failed',
        error: 'Build artifacts not found',
      });
    }

    // Check environment-specific files
    const envFiles = ['.env.production', '.env.production.local'];
    const hasEnvFiles = envFiles.some(file => fs.existsSync(file));

    if (hasEnvFiles) {
      colorLog('✅ Production environment files exist', 'green');
    } else {
      colorLog('⚠️  Production environment files not found', 'yellow');
    }

    // Check deployment configuration
    if (fs.existsSync('vercel.json') || fs.existsSync('next.config.js')) {
      colorLog('✅ Deployment configuration exists', 'green');
    } else {
      this.results.push({
        name: 'Deployment configuration',
        status: 'failed',
        error: 'Deployment configuration not found',
      });
    }
  }
}

if (require.main === module) {
  const runner = new PreDeploymentGateRunner();
  runner.run();
}

module.exports = PreDeploymentGateRunner;
```

### 6. Create Quality Gates Monitoring

Create `scripts/quality-monitor.js`:

```javascript
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

class QualityMonitor {
  constructor() {
    this.reportPath = 'quality-gates-report.json';
    this.historyPath = 'quality-history.json';
  }

  loadCurrentReport() {
    try {
      if (fs.existsSync(this.reportPath)) {
        return JSON.parse(fs.readFileSync(this.reportPath, 'utf8'));
      }
    } catch (error) {
      console.error('Could not load current report:', error.message);
    }
    return null;
  }

  loadHistory() {
    try {
      if (fs.existsSync(this.historyPath)) {
        return JSON.parse(fs.readFileSync(this.historyPath, 'utf8'));
      }
    } catch (error) {
      console.error('Could not load history:', error.message);
    }
    return [];
  }

  saveHistory(history) {
    try {
      fs.writeFileSync(this.historyPath, JSON.stringify(history, null, 2));
    } catch (error) {
      console.error('Could not save history:', error.message);
    }
  }

  addToHistory(report) {
    const history = this.loadHistory();

    history.push({
      timestamp: report.timestamp,
      duration: report.duration,
      summary: report.summary,
    });

    // Keep only last 100 entries
    if (history.length > 100) {
      history.splice(0, history.length - 100);
    }

    this.saveHistory(history);
  }

  generateTrends() {
    const history = this.loadHistory();

    if (history.length < 2) {
      console.log('Not enough data for trend analysis');
      return;
    }

    const latest = history[history.length - 1];
    const previous = history[history.length - 2];

    console.log('\n📈 Quality Trends', 'cyan');
    console.log('================', 'cyan');

    // Duration trend
    const durationChange = latest.duration - previous.duration;
    const durationTrend = durationChange > 0 ? '📈' : '📉';
    console.log(`${durationTrend} Duration: ${durationChange > 0 ? '+' : ''}${durationChange}ms`);

    // Success rate trend
    const latestRate = (latest.summary.passed / latest.summary.total) * 100;
    const previousRate = (previous.summary.passed / previous.summary.total) * 100;
    const rateChange = latestRate - previousRate;
    const rateTrend = rateChange >= 0 ? '📈' : '📉';
    console.log(`${rateTrend} Success Rate: ${rateChange >= 0 ? '+' : ''}${rateChange.toFixed(1)}%`);

    // Recent performance
    const recent = history.slice(-10);
    const avgDuration = recent.reduce((sum, entry) => sum + entry.duration, 0) / recent.length;
    const avgSuccessRate = recent.reduce((sum, entry) => sum + (entry.summary.passed / entry.summary.total) * 100, 0) / recent.length;

    console.log('\n📊 Recent Averages (last 10 runs):', 'cyan');
    console.log(`   Duration: ${avgDuration.toFixed(0)}ms`);
    console.log(`   Success Rate: ${avgSuccessRate.toFixed(1)}%`);
  }

  run() {
    const currentReport = this.loadCurrentReport();

    if (!currentReport) {
      console.log('❌ No current quality gates report found');
      console.log('   Run "npm run quality-gates" first');
      process.exit(1);
    }

    this.addToHistory(currentReport);
    this.generateTrends();
  }
}

if (require.main === module) {
  const monitor = new QualityMonitor();
  monitor.run();
}

module.exports = QualityMonitor;
```

### 7. Update Package.json Scripts

Update `package.json` scripts:

```json
{
  "scripts": {
    "quality-gates": "node scripts/quality-gates.js",
    "quality-gates:ci": "node scripts/ci-quality-gates.js",
    "quality-gates:pre-deploy": "node scripts/pre-deployment-gates.js",
    "quality-monitor": "node scripts/quality-monitor.js",
    "quality-report": "node -e \"console.log(JSON.stringify(require('./quality-gates-report.json'), null, 2))\"",
    "quality-check": "npm run quality-gates && npm run quality-monitor"
  }
}
```

### 8. Create GitHub Actions Workflow

Create `.github/workflows/quality-gates.yml`:

```yaml
name: Quality Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality-gates:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run quality gates
        run: npm run quality-gates:ci

      - name: Upload quality report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-gates-report.json

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
```

---

## Code Examples

### Running Quality Gates

```bash
# Standard quality gates
npm run quality-gates

# CI quality gates (includes additional checks)
npm run quality-gates:ci

# Pre-deployment quality gates
npm run quality-gates:pre-deploy

# Monitor quality trends
npm run quality-monitor

# Generate quality report
npm run quality-report
```

### Custom Quality Gate Configuration

```javascript
// quality-gates.config.js - Custom thresholds
module.exports = {
  coverage: {
    global: {
      statements: 90,  // Higher threshold
      branches: 85,
      functions: 90,
      lines: 90,
    },
  },
  performance: {
    bundleSize: {
      'main.js': 200000,  // Stricter bundle size
      'vendor.js': 250000,
    },
  },
  security: {
    vulnerabilities: {
      high: 0,
      moderate: 0,  // No moderate vulnerabilities allowed
      low: 2,
    },
  },
};
```

### Quality Gates in CI/CD Pipeline

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run quality gates
        run: npm run quality-gates:ci

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('quality-gates-report.json', 'utf8'));

            const comment = `
            ## Quality Gates Report

            **Duration:** ${report.duration}ms
            **Passed:** ${report.summary.passed}/${report.summary.total}
            **Status:** ${report.summary.failed === 0 ? '✅ PASSED' : '❌ FAILED'}

            ${report.summary.failed > 0 ? '### Failed Checks:\n' + report.results.filter(r => r.status === 'failed').map(r => `- ${r.name}: ${r.error}`).join('\n') : ''}
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

## Configuration Templates

### Complete quality-gates.config.js

```javascript
module.exports = {
  codeQuality: {
    eslint: {
      maxErrors: 0,
      maxWarnings: 0,
    },
    prettier: {
      check: true,
      enforce: true,
    },
    typescript: {
      strict: true,
      noImplicitAny: true,
    },
  },
  coverage: {
    global: {
      statements: 80,
      branches: 80,
      functions: 80,
      lines: 80,
    },
  },
  performance: {
    bundleSize: {
      'main.js': 250000,
      'vendor.js': 300000,
    },
    buildTime: {
      maxDuration: 300000,
    },
  },
  security: {
    vulnerabilities: {
      high: 0,
      moderate: 0,
      low: 5,
    },
  },
};
```

---

## Best Practices

1. **Set appropriate thresholds** - Balance quality and development speed
2. **Monitor trends over time** - Track quality improvements
3. **Use different gate levels** - Development, CI, pre-deployment
4. **Automate quality enforcement** - Prevent quality degradation
5. **Generate detailed reports** - Team visibility and accountability
6. **Integrate with CI/CD** - Automated quality checks
7. **Review failed gates** - Continuous improvement
8. **Update configuration regularly** - Adapt to project needs

---

## Stop Conditions

**STOP and report if:**
- Quality gate execution fails
- Configuration errors occur
- Report generation fails
- Threshold validation errors

**Expected Outcomes:**
- All quality gates functional
- Reports generated correctly
- Thresholds enforced properly
- CI/CD integration working
- Monitoring system active

---

## Verification Checklist

- [ ] Quality gate configuration created
- [ ] Quality gate runner functional
- [ ] CI quality gates working
- [ ] Pre-deployment gates functional
- [ ] Quality monitoring system active
- [ ] GitHub Actions workflow configured
- [ ] Package.json scripts updated
- [ ] Report generation working
- [ ] Threshold enforcement active
- [ ] Trend analysis functional

---

*Version: 1.0.0*
*Last Updated: 2026-01-31*
*Skill Category: Architecture - CI*
