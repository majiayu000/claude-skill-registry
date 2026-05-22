---
name: continuous-testing
description: Integrate automated testing into CI/CD pipelines for continuous quality feedback. Use for continuous testing, CI testing, automated testing pipelines, test orchestration, and DevOps quality practices.
---

# Continuous Testing

## Overview

Continuous testing integrates automated testing throughout the software development lifecycle, providing rapid feedback on quality at every stage. It shifts testing left in the development process and ensures that code changes are validated automatically before reaching production.

## When to Use

- Setting up CI/CD pipelines
- Automating test execution on commits
- Implementing shift-left testing
- Running tests in parallel
- Creating test gates for deployments
- Monitoring test health
- Optimizing test execution time
- Establishing quality gates

## Key Concepts

- **Shift Left**: Testing early in development cycle
- **Test Pyramid**: Unit > Integration > E2E tests
- **Parallel Execution**: Running tests concurrently
- **Test Gates**: Quality requirements before promotion
- **Flaky Tests**: Unreliable tests that need fixing
- **Test Reporting**: Dashboards and metrics
- **Test Selection**: Running only affected tests

## Instructions

### 1. **GitHub Actions CI Pipeline**

```yaml
# .github/workflows/ci.yml
name: Continuous Testing

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  NODE_VERSION: '18'

jobs:
  # Unit tests - Fast feedback
  unit-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unit

      - name: Comment PR with coverage
        if: github.event_name == 'pull_request'
        uses: romeovs/lcov-reporter-action@v0.3.1
        with:
          lcov-file: ./coverage/lcov.info
          github-token: ${{ secrets.GITHUB_TOKEN }}

  # Integration tests
  integration-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379

  # E2E tests - Run in parallel
  e2e-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Build application
        run: npm run build

      - name: Run E2E tests (shard ${{ matrix.shardIndex }}/${{ matrix.shardTotal }})
        run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report-${{ matrix.shardIndex }}
          path: playwright-report/
          retention-days: 7

  # Visual regression tests
  visual-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Required for Percy

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build Storybook
        run: npm run build-storybook

      - name: Run visual tests
        run: npx percy storybook ./storybook-static
        env:
          PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}

  # Security scanning
  security-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v3

      - name: Run npm audit
        run: npm audit --audit-level=high
        continue-on-error: true

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run SAST with Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten

  # Performance tests
  performance-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Install k6
        run: |
          sudo gpg -k
          sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6

      - name: Run performance tests
        run: k6 run tests/performance/load-test.js

  # Quality gate - All tests must pass
  quality-gate:
    runs-on: ubuntu-latest
    needs:
      - unit-tests
      - integration-tests
      - e2e-tests
      - security-tests

    steps:
      - name: Check test results
        run: echo "All quality gates passed!"

      - name: Can deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: echo "Ready for staging deployment"

      - name: Can deploy to production
        if: github.ref == 'refs/heads/main'
        run: echo "Ready for production deployment"
```

### 2. **GitLab CI Pipeline**

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security
  - deploy

variables:
  POSTGRES_DB: test
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres

# Test template
.test_template:
  image: node:18
  cache:
    paths:
      - node_modules/
  before_script:
    - npm ci

# Unit tests - Runs on every commit
unit-tests:
  extends: .test_template
  stage: test
  script:
    - npm run test:unit -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/

# Integration tests
integration-tests:
  extends: .test_template
  stage: test
  services:
    - postgres:14
    - redis:7
  variables:
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test
  script:
    - npm run db:migrate
    - npm run test:integration

# E2E tests - Parallel execution
e2e-tests:
  extends: .test_template
  stage: test
  parallel: 4
  script:
    - npx playwright install --with-deps chromium
    - npm run build
    - npx playwright test --shard=$CI_NODE_INDEX/$CI_NODE_TOTAL
  artifacts:
    when: always
    paths:
      - playwright-report/
    expire_in: 7 days

# Security scanning
security-scan:
  stage: security
  image: node:18
  script:
    - npm audit --audit-level=moderate
    - npx snyk test --severity-threshold=high
  allow_failure: true

# Contract tests
contract-tests:
  extends: .test_template
  stage: test
  script:
    - npm run test:pact
    - npx pact-broker publish ./pacts \
        --consumer-app-version=$CI_COMMIT_SHA \
        --broker-base-url=$PACT_BROKER_URL \
        --broker-token=$PACT_BROKER_TOKEN
  only:
    - merge_requests
    - main
```

### 3. **Jenkins Pipeline**

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        NODE_VERSION = '18'
        DATABASE_URL = credentials('test-database-url')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Parallel Tests') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit -- --coverage'
                    }
                    post {
                        always {
                            junit 'test-results/junit.xml'
                            publishCoverage adapters: [
                                coberturaAdapter('coverage/cobertura-coverage.xml')
                            ]
                        }
                    }
                }

                stage('Integration Tests') {
                    steps {
                        sh 'npm run test:integration'
                    }
                }

                stage('Lint & Type Check') {
                    steps {
                        sh 'npm run lint'
                        sh 'npm run type-check'
                    }
                }
            }
        }

        stage('E2E Tests') {
            steps {
                sh 'npx playwright install --with-deps'
                sh 'npm run build'
                sh 'npx playwright test'
            }
            post {
                always {
                    publishHTML([
                        reportDir: 'playwright-report',
                        reportFiles: 'index.html',
                        reportName: 'Playwright Report'
                    ])
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh 'npm audit --audit-level=high'
                sh 'npx snyk test --severity-threshold=high'
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def coverage = readFile('coverage/coverage-summary.json')
                    def coverageData = new groovy.json.JsonSlurper().parseText(coverage)
                    def lineCoverage = coverageData.total.lines.pct

                    if (lineCoverage < 80) {
                        error "Coverage ${lineCoverage}% is below threshold 80%"
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Deploying to staging...'
                // Deployment steps
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                echo 'Deploying to production...'
                // Deployment steps
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
            )
        }
        success {
            slackSend(
                color: 'good',
                message: "Build succeeded: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
            )
        }
    }
}
```

### 4. **Test Selection Strategy**

```typescript
// scripts/run-affected-tests.ts
import { execSync } from 'child_process';
import * as fs from 'fs';

class AffectedTestRunner {
  getAffectedFiles(): string[] {
    // Get changed files from git
    const output = execSync('git diff --name-only HEAD~1', {
      encoding: 'utf-8',
    });
    return output.split('\n').filter(Boolean);
  }

  getTestsForFiles(files: string[]): Set<string> {
    const tests = new Set<string>();

    for (const file of files) {
      if (file.endsWith('.test.ts') || file.endsWith('.spec.ts')) {
        // File is already a test
        tests.add(file);
      } else if (file.endsWith('.ts')) {
        // Find associated test file
        const testFile = file.replace('.ts', '.test.ts');
        if (fs.existsSync(testFile)) {
          tests.add(testFile);
        }

        // Check for integration tests that import this file
        const integrationTests = execSync(
          `grep -r "from.*${file}" tests/integration/*.test.ts`,
          { encoding: 'utf-8' }
        ).split('\n');

        integrationTests.forEach(line => {
          const match = line.match(/^([^:]+):/);
          if (match) tests.add(match[1]);
        });
      }
    }

    return tests;
  }

  run() {
    const affectedFiles = this.getAffectedFiles();
    console.log('Affected files:', affectedFiles);

    const testsToRun = this.getTestsForFiles(affectedFiles);
    console.log('Tests to run:', testsToRun);

    if (testsToRun.size === 0) {
      console.log('No tests affected');
      return;
    }

    // Run only affected tests
    const testPattern = Array.from(testsToRun).join('|');
    execSync(`npm test -- --testPathPattern="${testPattern}"`, {
      stdio: 'inherit',
    });
  }
}

new AffectedTestRunner().run();
```

### 5. **Flaky Test Detection**

```yaml
# .github/workflows/flaky-test-detection.yml
name: Flaky Test Detection

on:
  schedule:
    - cron: '0 2 * * *'  # Run nightly

jobs:
  detect-flaky-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests 10 times
        run: |
          for i in {1..10}; do
            echo "Run $i"
            npm test -- --json --outputFile=results-$i.json || true
          done

      - name: Analyze flaky tests
        run: node scripts/analyze-flaky-tests.js
```

```javascript
// scripts/analyze-flaky-tests.js
const fs = require('fs');

const runs = Array.from({ length: 10 }, (_, i) =>
  JSON.parse(fs.readFileSync(`results-${i + 1}.json`, 'utf-8'))
);

const testResults = new Map();

// Aggregate results
runs.forEach(run => {
  run.testResults.forEach(suite => {
    suite.assertionResults.forEach(test => {
      const key = `${suite.name}::${test.title}`;
      if (!testResults.has(key)) {
        testResults.set(key, { passed: 0, failed: 0 });
      }
      const stats = testResults.get(key);
      if (test.status === 'passed') {
        stats.passed++;
      } else {
        stats.failed++;
      }
    });
  });
});

// Identify flaky tests
const flakyTests = [];
testResults.forEach((stats, test) => {
  if (stats.passed > 0 && stats.failed > 0) {
    flakyTests.push({
      test,
      passRate: (stats.passed / 10) * 100,
      ...stats,
    });
  }
});

if (flakyTests.length > 0) {
  console.log('\nFlaky Tests Detected:');
  flakyTests.forEach(({ test, passRate, passed, failed }) => {
    console.log(`  ${test}`);
    console.log(`    Pass rate: ${passRate}% (${passed}/10 runs)`);
  });

  // Fail if too many flaky tests
  if (flakyTests.length > 5) {
    process.exit(1);
  }
}
```

### 6. **Test Metrics Dashboard**

```typescript
// scripts/generate-test-metrics.ts
import * as fs from 'fs';

interface TestMetrics {
  totalTests: number;
  passedTests: number;
  failedTests: number;
  skippedTests: number;
  duration: number;
  coverage: number;
  timestamp: string;
}

class MetricsCollector {
  collectMetrics(): TestMetrics {
    const testResults = JSON.parse(
      fs.readFileSync('test-results.json', 'utf-8')
    );
    const coverage = JSON.parse(
      fs.readFileSync('coverage/coverage-summary.json', 'utf-8')
    );

    return {
      totalTests: testResults.numTotalTests,
      passedTests: testResults.numPassedTests,
      failedTests: testResults.numFailedTests,
      skippedTests: testResults.numPendingTests,
      duration: testResults.testResults.reduce(
        (sum, r) => sum + r.perfStats.runtime,
        0
      ),
      coverage: coverage.total.lines.pct,
      timestamp: new Date().toISOString(),
    };
  }

  saveMetrics(metrics: TestMetrics) {
    const history = this.loadHistory();
    history.push(metrics);

    // Keep last 30 days
    const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000;
    const filtered = history.filter(
      m => new Date(m.timestamp).getTime() > cutoff
    );

    fs.writeFileSync(
      'metrics-history.json',
      JSON.stringify(filtered, null, 2)
    );
  }

  loadHistory(): TestMetrics[] {
    try {
      return JSON.parse(fs.readFileSync('metrics-history.json', 'utf-8'));
    } catch {
      return [];
    }
  }

  generateReport() {
    const history = this.loadHistory();

    console.log('\nTest Metrics (Last 7 days):');
    console.log('─'.repeat(60));

    const recent = history.slice(-7);
    const avgCoverage =
      recent.reduce((sum, m) => sum + m.coverage, 0) / recent.length;
    const avgDuration =
      recent.reduce((sum, m) => sum + m.duration, 0) / recent.length;

    console.log(`Average Coverage: ${avgCoverage.toFixed(2)}%`);
    console.log(`Average Duration: ${(avgDuration / 1000).toFixed(2)}s`);
    console.log(`Total Tests: ${recent[recent.length - 1].totalTests}`);
  }
}

const collector = new MetricsCollector();
const metrics = collector.collectMetrics();
collector.saveMetrics(metrics);
collector.generateReport();
```

## Best Practices

### ✅ DO
- Run fast tests first (unit → integration → E2E)
- Parallelize test execution
- Cache dependencies
- Set appropriate timeouts
- Monitor test health and flakiness
- Implement quality gates
- Use test selection strategies
- Generate comprehensive reports

### ❌ DON'T
- Run all tests sequentially
- Ignore flaky tests
- Skip test maintenance
- Allow tests to depend on each other
- Run slow tests on every commit
- Deploy with failing tests
- Ignore test execution time
- Skip security scanning

## Metrics to Track

- **Test Coverage**: Line, branch, function coverage
- **Test Duration**: Execution time trends
- **Pass Rate**: Percentage of passing tests
- **Flakiness**: Tests with inconsistent results
- **Test Count**: Growth over time
- **Build Success Rate**: Pipeline reliability

## Tools

- **CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI
- **Test Orchestration**: Nx, Bazel, Lerna
- **Reporting**: Allure, ReportPortal, TestRail
- **Monitoring**: Datadog, New Relic, Grafana

## Examples

See also: test-automation-framework, integration-testing, cicd-pipeline-setup for comprehensive CI/CD implementation.
