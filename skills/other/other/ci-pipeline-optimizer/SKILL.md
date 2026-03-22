---
name: CI Pipeline Optimizer
description: Optimize CI test pipelines through intelligent test splitting, parallelization, caching strategies, and selective test execution based on code changes.
version: 1.0.0
author: Pramod
license: MIT
tags: [ci-cd, pipeline, optimization, parallelization, test-splitting, caching, github-actions]
testingTypes: [code-quality]
frameworks: [jest, vitest, playwright]
languages: [typescript, javascript, python, java]
domains: [devops]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# CI Pipeline Optimizer

Slow CI pipelines are one of the most common productivity killers in software teams. A test suite that takes 30 minutes to run means developers context-switch away from their work, batch multiple changes into fewer PRs to avoid waiting, and eventually start skipping CI altogether. This skill addresses CI pipeline performance through four complementary strategies: intelligent test splitting across parallel workers, selective test execution based on code changes, aggressive caching of dependencies and build artifacts, and pipeline architecture that minimizes total wall-clock time. The techniques apply to any CI system but use GitHub Actions as the primary example, with patterns that transfer to GitLab CI, CircleCI, Jenkins, and other platforms.

## Core Principles

### 1. Wall-Clock Time Is the Only Metric That Matters

CPU time, billable minutes, and total test count are secondary metrics. The developer waits for wall-clock time. A pipeline that uses 60 CPU-minutes across 10 parallel workers in 6 minutes is vastly preferable to a pipeline that uses 20 CPU-minutes sequentially in 20 minutes. Optimize for the duration the developer experiences.

### 2. Never Run Tests You Do Not Need

If a PR changes only documentation files, running the full test suite is waste. If a PR modifies only the frontend, running backend integration tests is waste. Selective test execution identifies the minimum set of tests needed to validate a specific change, with a safety net that defaults to running everything when the analysis is uncertain.

### 3. Cache Everything That Does Not Change

Dependencies, build artifacts, Docker layers, and browser binaries are the same across most CI runs. Downloading and building them from scratch on every run is unnecessary. Aggressive caching can eliminate minutes from every pipeline execution.

### 4. Split Tests by Duration, Not by File Count

Naive test splitting distributes files evenly across workers. But if one file contains a 5-minute test and another contains a 5-second test, the distribution is severely unbalanced. Intelligent splitting uses historical duration data to distribute tests so that all workers finish at approximately the same time.

### 5. Fail Fast, Report Completely

Run the fastest tests first. If unit tests catch a bug in 30 seconds, there is no reason to wait 10 minutes for e2e tests to also catch it. Structure the pipeline so the cheapest checks (lint, type-check) run first to provide the fastest possible feedback, but still collect complete results from all shards for thorough reporting.

## Project Structure

```
ci-config/
  scripts/
    split-tests.ts
    detect-changes.ts
    cache-manager.ts
    timing-collector.ts
    pipeline-analyzer.ts
  config/
    test-groups.json
    change-map.json
    cache-config.json
  .github/
    workflows/
      ci-optimized.yml
      ci-selective.yml
      cache-warmup.yml
  package.json
  tsconfig.json
```

The `scripts/` directory contains automation tools for test splitting, change detection, cache management, and pipeline analysis. The `config/` directory holds the mapping from file changes to test groups, cache key definitions, and test group specifications.

## Test Splitting Strategies

### Duration-Based Test Splitting

Split tests across parallel workers based on historical execution times so that each worker runs for approximately the same duration:

```typescript
// scripts/split-tests.ts

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';

interface TestTiming {
  file: string;
  duration: number;
  lastRun: string;
}

interface SplitResult {
  shardIndex: number;
  files: string[];
  estimatedDuration: number;
}

export function splitTestsByDuration(
  testFiles: string[],
  shardCount: number,
  timingsFile: string = 'test-timings.json'
): SplitResult[] {
  // Load historical timings
  const timings = loadTimings(timingsFile);

  // Create a list of files with their estimated duration
  const fileTimings: Array<{ file: string; duration: number }> = testFiles.map((file) => ({
    file,
    duration: timings.get(file) || estimateDefaultDuration(file),
  }));

  // Sort by duration descending (greedy algorithm: assign largest jobs first)
  fileTimings.sort((a, b) => b.duration - a.duration);

  // Initialize shards
  const shards: SplitResult[] = Array.from({ length: shardCount }, (_, i) => ({
    shardIndex: i,
    files: [],
    estimatedDuration: 0,
  }));

  // Greedy assignment: always assign to the shard with the least total duration
  for (const fileTiming of fileTimings) {
    const lightest = shards.reduce((min, shard) =>
      shard.estimatedDuration < min.estimatedDuration ? shard : min
    );
    lightest.files.push(fileTiming.file);
    lightest.estimatedDuration += fileTiming.duration;
  }

  return shards;
}

function loadTimings(timingsFile: string): Map<string, number> {
  const timings = new Map<string, number>();

  if (!existsSync(timingsFile)) {
    return timings;
  }

  try {
    const data: TestTiming[] = JSON.parse(readFileSync(timingsFile, 'utf-8'));
    for (const entry of data) {
      timings.set(entry.file, entry.duration);
    }
  } catch {
    console.warn(`Failed to parse timings file: ${timingsFile}`);
  }

  return timings;
}

function estimateDefaultDuration(file: string): number {
  // Heuristic estimates based on test type when no historical data exists
  if (file.includes('.e2e.') || file.includes('e2e/')) return 30000;
  if (file.includes('.integration.') || file.includes('integration/')) return 10000;
  if (file.includes('.spec.')) return 5000;
  return 3000; // Default estimate for unit tests
}

// CLI entry point for use in GitHub Actions
function main(): void {
  const shardIndex = parseInt(process.env.SHARD_INDEX || '0', 10);
  const shardCount = parseInt(process.env.SHARD_COUNT || '1', 10);

  // Discover all test files
  const testFilesOutput = execSync(
    'find . -name "*.test.ts" -o -name "*.spec.ts" | grep -v node_modules',
    { encoding: 'utf-8' }
  );
  const testFiles = testFilesOutput.trim().split('\n').filter(Boolean);

  const shards = splitTestsByDuration(testFiles, shardCount);
  const myShard = shards[shardIndex];

  if (!myShard) {
    console.error(`Invalid shard index ${shardIndex} for ${shardCount} shards`);
    process.exit(1);
  }

  console.log(
    `Shard ${shardIndex + 1}/${shardCount}: ${myShard.files.length} files, ~${(myShard.estimatedDuration / 1000).toFixed(1)}s`
  );

  // Write shard files list for the test runner to consume
  writeFileSync('shard-files.txt', myShard.files.join('\n'), 'utf-8');
}

main();
```

### Collecting Test Timings

After each CI run, collect and store test execution timings for future split optimization:

```typescript
// scripts/timing-collector.ts

import { readFileSync, writeFileSync, existsSync } from 'fs';

interface JestResult {
  testResults: Array<{
    testFilePath: string;
    perfStats: {
      runtime: number;
    };
  }>;
}

interface PlaywrightResult {
  suites: Array<{
    file: string;
    specs: Array<{
      tests: Array<{
        results: Array<{
          duration: number;
        }>;
      }>;
    }>;
  }>;
}

interface TestTiming {
  file: string;
  duration: number;
  lastRun: string;
}

export function collectJestTimings(resultsFile: string): TestTiming[] {
  const results: JestResult = JSON.parse(readFileSync(resultsFile, 'utf-8'));

  return results.testResults.map((test) => ({
    file: test.testFilePath.replace(process.cwd() + '/', ''),
    duration: test.perfStats.runtime,
    lastRun: new Date().toISOString(),
  }));
}

export function collectPlaywrightTimings(resultsFile: string): TestTiming[] {
  const results: PlaywrightResult = JSON.parse(readFileSync(resultsFile, 'utf-8'));
  const timings: TestTiming[] = [];

  for (const suite of results.suites) {
    let totalDuration = 0;
    for (const spec of suite.specs) {
      for (const test of spec.tests) {
        for (const result of test.results) {
          totalDuration += result.duration;
        }
      }
    }

    timings.push({
      file: suite.file,
      duration: totalDuration,
      lastRun: new Date().toISOString(),
    });
  }

  return timings;
}

export function mergeTimings(
  existing: TestTiming[],
  latest: TestTiming[]
): TestTiming[] {
  const map = new Map<string, TestTiming>();

  for (const timing of existing) {
    map.set(timing.file, timing);
  }

  // Merge with exponential moving average to smooth out outliers
  for (const timing of latest) {
    const prev = map.get(timing.file);
    if (prev) {
      // EMA with alpha = 0.3 gives 70% weight to history, 30% to new data
      const smoothedDuration = prev.duration * 0.7 + timing.duration * 0.3;
      map.set(timing.file, {
        file: timing.file,
        duration: Math.round(smoothedDuration),
        lastRun: timing.lastRun,
      });
    } else {
      map.set(timing.file, timing);
    }
  }

  return Array.from(map.values());
}

function main(): void {
  const timingsFile = 'test-timings.json';
  const existing: TestTiming[] = existsSync(timingsFile)
    ? JSON.parse(readFileSync(timingsFile, 'utf-8'))
    : [];

  let latest: TestTiming[] = [];

  if (existsSync('jest-results.json')) {
    latest = collectJestTimings('jest-results.json');
  } else if (existsSync('playwright-results.json')) {
    latest = collectPlaywrightTimings('playwright-results.json');
  }

  if (latest.length > 0) {
    const merged = mergeTimings(existing, latest);
    writeFileSync(timingsFile, JSON.stringify(merged, null, 2), 'utf-8');
    console.log(`Updated timings for ${latest.length} test files (${merged.length} total)`);
  } else {
    console.warn('No test results found to collect timings from');
  }
}

main();
```

## Selective Test Execution

### Change Detection Engine

Detect which files changed and determine which test groups need to run:

```typescript
// scripts/detect-changes.ts

import { execSync } from 'child_process';
import { readFileSync, existsSync } from 'fs';

interface ChangeMap {
  patterns: Array<{
    glob: string;
    testGroups: string[];
    description: string;
  }>;
  testGroups: Record<
    string,
    {
      command: string;
      files?: string[];
      description: string;
    }
  >;
}

interface DetectedChanges {
  changedFiles: string[];
  testGroupsToRun: Set<string>;
  skipReason?: string;
}

export function detectChanges(baseBranch: string = 'main'): DetectedChanges {
  let changedFiles: string[];

  try {
    const diffOutput = execSync(
      `git diff --name-only origin/${baseBranch}...HEAD`,
      { encoding: 'utf-8' }
    );
    changedFiles = diffOutput.trim().split('\n').filter(Boolean);
  } catch {
    const diffOutput = execSync('git diff --name-only HEAD~1', {
      encoding: 'utf-8',
    });
    changedFiles = diffOutput.trim().split('\n').filter(Boolean);
  }

  if (changedFiles.length === 0) {
    return {
      changedFiles: [],
      testGroupsToRun: new Set(),
      skipReason: 'No files changed',
    };
  }

  const changeMap = loadChangeMap();
  const testGroups = new Set<string>();

  for (const file of changedFiles) {
    for (const pattern of changeMap.patterns) {
      if (matchGlob(file, pattern.glob)) {
        for (const group of pattern.testGroups) {
          testGroups.add(group);
        }
      }
    }
  }

  // Safety net: if no patterns matched, run all tests
  if (testGroups.size === 0) {
    testGroups.add('all');
  }

  return {
    changedFiles,
    testGroupsToRun: testGroups,
  };
}

function loadChangeMap(): ChangeMap {
  const configPath = 'ci-config/config/change-map.json';
  if (!existsSync(configPath)) {
    return getDefaultChangeMap();
  }
  return JSON.parse(readFileSync(configPath, 'utf-8'));
}

function getDefaultChangeMap(): ChangeMap {
  return {
    patterns: [
      {
        glob: 'src/api/**',
        testGroups: ['unit', 'api-integration'],
        description: 'API source changes trigger unit and integration tests',
      },
      {
        glob: 'src/components/**',
        testGroups: ['unit', 'component'],
        description: 'UI component changes trigger unit and component tests',
      },
      {
        glob: 'src/pages/**',
        testGroups: ['unit', 'e2e'],
        description: 'Page-level changes trigger unit and E2E tests',
      },
      {
        glob: 'src/lib/**',
        testGroups: ['unit'],
        description: 'Library changes trigger unit tests',
      },
      {
        glob: 'src/db/**',
        testGroups: ['unit', 'api-integration', 'e2e'],
        description: 'Database changes trigger all test types',
      },
      {
        glob: 'package.json',
        testGroups: ['all'],
        description: 'Dependency changes require full test run',
      },
      {
        glob: '*.config.*',
        testGroups: ['all'],
        description: 'Config changes require full test run',
      },
      {
        glob: '**/*.md',
        testGroups: ['docs-only'],
        description: 'Documentation-only changes skip tests',
      },
      {
        glob: '.github/**',
        testGroups: ['ci-only'],
        description: 'CI configuration changes need validation',
      },
    ],
    testGroups: {
      all: { command: 'npm test', description: 'Full test suite' },
      unit: { command: 'npm run test:unit', description: 'Unit tests only' },
      'api-integration': {
        command: 'npm run test:integration',
        description: 'API integration tests',
      },
      component: { command: 'npm run test:components', description: 'Component tests' },
      e2e: { command: 'npx playwright test', description: 'End-to-end tests' },
      'docs-only': {
        command: 'echo "No tests needed for docs-only changes"',
        description: 'Skip tests',
      },
      'ci-only': {
        command: 'echo "CI config changed - validate workflow syntax only"',
        description: 'Validate CI config',
      },
    },
  };
}

function matchGlob(filePath: string, pattern: string): boolean {
  const regexPattern = pattern
    .replace(/\*\*/g, '<<<GLOBSTAR>>>')
    .replace(/\*/g, '[^/]*')
    .replace(/<<<GLOBSTAR>>>/g, '.*')
    .replace(/\?/g, '.');
  return new RegExp(`^${regexPattern}$`).test(filePath);
}

function main(): void {
  const baseBranch = process.env.BASE_BRANCH || 'main';
  const result = detectChanges(baseBranch);

  console.log(`Changed files: ${result.changedFiles.length}`);
  console.log(`Test groups to run: ${Array.from(result.testGroupsToRun).join(', ')}`);

  if (result.skipReason) {
    console.log(`Skip reason: ${result.skipReason}`);
  }

  // Output for GitHub Actions
  const groups = Array.from(result.testGroupsToRun);
  const shouldRun = groups.length > 0 && !groups.includes('docs-only');
  console.log(`::set-output name=test-groups::${JSON.stringify(groups)}`);
  console.log(`::set-output name=should-run-tests::${shouldRun}`);
}

main();
```

## Caching Strategies

### Multi-Layer Cache Configuration

```typescript
// scripts/cache-manager.ts

import { readFileSync, existsSync } from 'fs';
import { createHash } from 'crypto';

interface CacheLayer {
  name: string;
  paths: string[];
  keyFiles: string[];
  fallbackKeys: string[];
  maxAge: number;
}

interface CacheConfig {
  layers: CacheLayer[];
}

export function generateCacheKeys(config: CacheConfig): Array<{
  name: string;
  key: string;
  restoreKeys: string[];
  paths: string[];
}> {
  const platform = process.env.RUNNER_OS || process.platform;

  return config.layers.map((layer) => {
    const fileHashes = layer.keyFiles
      .filter((f) => existsSync(f))
      .map((f) => hashFile(f))
      .join('-');

    const key = `${platform}-${layer.name}-${fileHashes}`;

    const restoreKeys = layer.fallbackKeys.map(
      (fallback) => `${platform}-${layer.name}-${fallback}`
    );

    return {
      name: layer.name,
      key,
      restoreKeys,
      paths: layer.paths,
    };
  });
}

function hashFile(filePath: string): string {
  const content = readFileSync(filePath);
  return createHash('sha256').update(content).digest('hex').substring(0, 16);
}

export const DEFAULT_CACHE_CONFIG: CacheConfig = {
  layers: [
    {
      name: 'node-modules',
      paths: ['node_modules', '~/.pnpm-store'],
      keyFiles: ['pnpm-lock.yaml', 'package.json'],
      fallbackKeys: [''],
      maxAge: 604800000, // 7 days
    },
    {
      name: 'playwright-browsers',
      paths: ['~/.cache/ms-playwright'],
      keyFiles: ['package.json'],
      fallbackKeys: [''],
      maxAge: 2592000000, // 30 days
    },
    {
      name: 'build-cache',
      paths: ['.next/cache', 'dist', '.turbo'],
      keyFiles: ['tsconfig.json', 'next.config.js'],
      fallbackKeys: [''],
      maxAge: 86400000, // 1 day
    },
    {
      name: 'test-timings',
      paths: ['test-timings.json'],
      keyFiles: [],
      fallbackKeys: [''],
      maxAge: 2592000000, // 30 days
    },
  ],
};
```

## GitHub Actions Optimized Pipeline

### Full Optimized CI Workflow

```yaml
# .github/workflows/ci-optimized.yml
name: Optimized CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # Step 1: Detect changes and determine what to test
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.changes.outputs.backend }}
      frontend: ${{ steps.changes.outputs.frontend }}
      config: ${{ steps.changes.outputs.config }}
      docs-only: ${{ steps.changes.outputs.docs }}
      shard-count: ${{ steps.shards.outputs.count }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect changed file categories
        id: changes
        uses: dorny/paths-filter@v3
        with:
          filters: |
            backend:
              - 'src/api/**'
              - 'src/db/**'
              - 'src/lib/**'
            frontend:
              - 'src/components/**'
              - 'src/pages/**'
              - 'src/styles/**'
            config:
              - 'package.json'
              - 'pnpm-lock.yaml'
              - '*.config.*'
            docs:
              - '**/*.md'
              - 'docs/**'

      - name: Determine optimal shard count
        id: shards
        run: |
          if [[ "${{ steps.changes.outputs.config }}" == "true" ]]; then
            echo "count=4" >> $GITHUB_OUTPUT
          elif [[ "${{ steps.changes.outputs.backend }}" == "true" && "${{ steps.changes.outputs.frontend }}" == "true" ]]; then
            echo "count=4" >> $GITHUB_OUTPUT
          elif [[ "${{ steps.changes.outputs.backend }}" == "true" || "${{ steps.changes.outputs.frontend }}" == "true" ]]; then
            echo "count=2" >> $GITHUB_OUTPUT
          else
            echo "count=1" >> $GITHUB_OUTPUT
          fi

  # Step 2: Lint and type-check (fastest feedback)
  lint:
    runs-on: ubuntu-latest
    needs: detect-changes
    if: needs.detect-changes.outputs.docs-only != 'true'
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Run lint
        run: pnpm lint

      - name: Run type check
        run: pnpm tsc --noEmit

  # Step 3: Unit tests (fast, parallel shards)
  unit-tests:
    runs-on: ubuntu-latest
    needs: [detect-changes, lint]
    if: needs.detect-changes.outputs.docs-only != 'true'
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2]
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Restore test timings
        uses: actions/cache@v4
        with:
          path: test-timings.json
          key: test-timings-${{ github.ref }}
          restore-keys: |
            test-timings-refs/heads/main
            test-timings-

      - name: Run unit tests (shard ${{ matrix.shard }}/2)
        run: |
          pnpm vitest run \
            --reporter=json \
            --outputFile=vitest-results.json \
            --shard=${{ matrix.shard }}/2

      - name: Collect test timings
        if: always()
        run: npx tsx ci-config/scripts/timing-collector.ts

      - name: Save test timings
        if: always()
        uses: actions/cache/save@v4
        with:
          path: test-timings.json
          key: test-timings-${{ github.ref }}-${{ github.run_id }}-shard-${{ matrix.shard }}

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: unit-results-shard-${{ matrix.shard }}
          path: vitest-results.json
          retention-days: 7

  # Step 4: Integration tests (medium speed, conditional)
  integration-tests:
    runs-on: ubuntu-latest
    needs: [detect-changes, lint]
    if: |
      needs.detect-changes.outputs.backend == 'true' ||
      needs.detect-changes.outputs.config == 'true'
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Run integration tests
        run: pnpm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

  # Step 5: E2E tests (slowest, most shards, conditional)
  e2e-tests:
    runs-on: ubuntu-latest
    needs: [detect-changes, lint]
    if: |
      needs.detect-changes.outputs.frontend == 'true' ||
      needs.detect-changes.outputs.config == 'true'
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Cache Playwright browsers
        uses: actions/cache@v4
        with:
          path: ~/.cache/ms-playwright
          key: playwright-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Build application
        run: pnpm build

      - name: Run E2E tests (shard ${{ matrix.shard }}/4)
        run: npx playwright test --shard=${{ matrix.shard }}/4

      - name: Upload failure artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-results-shard-${{ matrix.shard }}
          path: test-results/
          retention-days: 7
```

### Cache Warmup Workflow

Pre-populate caches on a schedule so the first PR of the day gets warm caches:

```yaml
# .github/workflows/cache-warmup.yml
name: Cache Warmup

on:
  schedule:
    - cron: '0 6 * * 1-5'  # Weekdays at 6 AM UTC
  workflow_dispatch:

jobs:
  warmup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Cache node_modules
        uses: actions/cache/save@v4
        with:
          path: |
            node_modules
            ~/.pnpm-store
          key: pnpm-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Cache Playwright
        uses: actions/cache/save@v4
        with:
          path: ~/.cache/ms-playwright
          key: playwright-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}

      - name: Build application
        run: pnpm build

      - name: Cache build artifacts
        uses: actions/cache/save@v4
        with:
          path: |
            .next/cache
            dist
            .turbo
          key: build-${{ runner.os }}-${{ hashFiles('tsconfig.json') }}-${{ github.sha }}
```

## Pipeline Analysis and Monitoring

### Pipeline Duration Analyzer

Track and analyze pipeline performance over time to identify regressions and optimization opportunities:

```typescript
// scripts/pipeline-analyzer.ts

interface PipelineRun {
  runId: string;
  branch: string;
  timestamp: string;
  totalDuration: number;
  jobs: Array<{
    name: string;
    duration: number;
    status: 'success' | 'failure' | 'cancelled';
    steps: Array<{
      name: string;
      duration: number;
    }>;
  }>;
}

interface PipelineAnalysis {
  averageDuration: number;
  medianDuration: number;
  p95Duration: number;
  slowestJobs: Array<{ name: string; avgDuration: number }>;
  slowestSteps: Array<{ jobName: string; stepName: string; avgDuration: number }>;
  cacheSavings: number;
  recommendations: string[];
}

export function analyzePipeline(runs: PipelineRun[]): PipelineAnalysis {
  if (runs.length === 0) {
    return {
      averageDuration: 0,
      medianDuration: 0,
      p95Duration: 0,
      slowestJobs: [],
      slowestSteps: [],
      cacheSavings: 0,
      recommendations: [],
    };
  }

  const durations = runs.map((r) => r.totalDuration).sort((a, b) => a - b);
  const average = durations.reduce((a, b) => a + b, 0) / durations.length;
  const median = durations[Math.floor(durations.length / 2)];
  const p95 = durations[Math.floor(durations.length * 0.95)];

  // Aggregate job durations across runs
  const jobDurations = new Map<string, number[]>();
  const stepDurations = new Map<string, number[]>();

  for (const run of runs) {
    for (const job of run.jobs) {
      if (!jobDurations.has(job.name)) {
        jobDurations.set(job.name, []);
      }
      jobDurations.get(job.name)!.push(job.duration);

      for (const step of job.steps) {
        const key = `${job.name}::${step.name}`;
        if (!stepDurations.has(key)) {
          stepDurations.set(key, []);
        }
        stepDurations.get(key)!.push(step.duration);
      }
    }
  }

  const slowestJobs = Array.from(jobDurations.entries())
    .map(([name, times]) => ({
      name,
      avgDuration: times.reduce((a, b) => a + b, 0) / times.length,
    }))
    .sort((a, b) => b.avgDuration - a.avgDuration)
    .slice(0, 5);

  const slowestSteps = Array.from(stepDurations.entries())
    .map(([key, times]) => {
      const [jobName, stepName] = key.split('::');
      return {
        jobName,
        stepName,
        avgDuration: times.reduce((a, b) => a + b, 0) / times.length,
      };
    })
    .sort((a, b) => b.avgDuration - a.avgDuration)
    .slice(0, 10);

  const recommendations = generateOptimizationRecommendations(
    average,
    slowestJobs,
    slowestSteps
  );

  return {
    averageDuration: Math.round(average),
    medianDuration: Math.round(median),
    p95Duration: Math.round(p95),
    slowestJobs,
    slowestSteps,
    cacheSavings: estimateCacheSavings(stepDurations),
    recommendations,
  };
}

function generateOptimizationRecommendations(
  avgDuration: number,
  slowestJobs: Array<{ name: string; avgDuration: number }>,
  slowestSteps: Array<{ jobName: string; stepName: string; avgDuration: number }>
): string[] {
  const recommendations: string[] = [];

  if (avgDuration > 600000) {
    recommendations.push(
      'Pipeline average exceeds 10 minutes. Consider increasing parallelization or enabling selective test execution.'
    );
  }

  for (const job of slowestJobs) {
    if (job.avgDuration > 300000) {
      recommendations.push(
        `Job "${job.name}" averages ${(job.avgDuration / 60000).toFixed(1)}min. Consider splitting into shards.`
      );
    }
  }

  for (const step of slowestSteps) {
    if (step.stepName.toLowerCase().includes('install') && step.avgDuration > 60000) {
      recommendations.push(
        `Step "${step.stepName}" in "${step.jobName}" takes ${(step.avgDuration / 1000).toFixed(0)}s. Verify dependency caching is working correctly.`
      );
    }
    if (step.stepName.toLowerCase().includes('build') && step.avgDuration > 120000) {
      recommendations.push(
        `Build step in "${step.jobName}" takes ${(step.avgDuration / 1000).toFixed(0)}s. Consider incremental builds or build caching with Turborepo.`
      );
    }
  }

  return recommendations;
}

function estimateCacheSavings(stepDurations: Map<string, number[]>): number {
  let savings = 0;

  for (const [key, times] of stepDurations) {
    if (key.toLowerCase().includes('install') || key.toLowerCase().includes('cache')) {
      if (times.length > 1) {
        const first = times[0];
        const subsequent = times.slice(1);
        const avgSubsequent =
          subsequent.reduce((a, b) => a + b, 0) / subsequent.length;
        if (first > avgSubsequent * 2) {
          savings += (first - avgSubsequent) * subsequent.length;
        }
      }
    }
  }

  return Math.round(savings);
}
```

## Critical Path Optimization

### Understanding the Pipeline Dependency Graph

The critical path is the longest sequential chain of jobs in your pipeline. Parallelizing jobs off the critical path does not reduce total duration. Focus optimization on the critical path:

```typescript
// scripts/critical-path.ts

interface JobNode {
  name: string;
  estimatedDuration: number;
  dependencies: string[];
  canParallelize: boolean;
  shardable: boolean;
}

export function findCriticalPath(jobs: JobNode[]): {
  path: JobNode[];
  duration: number;
  parallelizableSavings: number;
} {
  const jobMap = new Map(jobs.map((j) => [j.name, j]));
  const memo = new Map<string, number>();

  function longestPath(jobName: string): number {
    if (memo.has(jobName)) return memo.get(jobName)!;

    const job = jobMap.get(jobName);
    if (!job) return 0;

    let maxDepDuration = 0;
    for (const dep of job.dependencies) {
      maxDepDuration = Math.max(maxDepDuration, longestPath(dep));
    }

    const total = maxDepDuration + job.estimatedDuration;
    memo.set(jobName, total);
    return total;
  }

  // Find the endpoint of the critical path
  let maxDuration = 0;
  let criticalEndJob = '';

  for (const job of jobs) {
    const duration = longestPath(job.name);
    if (duration > maxDuration) {
      maxDuration = duration;
      criticalEndJob = job.name;
    }
  }

  // Reconstruct the critical path by walking backwards
  const path: JobNode[] = [];
  let current = criticalEndJob;

  while (current) {
    const job = jobMap.get(current);
    if (!job) break;
    path.unshift(job);

    let nextJob = '';
    let nextDuration = 0;
    for (const dep of job.dependencies) {
      const depDuration = memo.get(dep) || 0;
      if (depDuration > nextDuration) {
        nextDuration = depDuration;
        nextJob = dep;
      }
    }
    current = nextJob;
  }

  const totalSequentialDuration = jobs.reduce(
    (sum, job) => sum + job.estimatedDuration,
    0
  );
  const criticalPathDuration = path.reduce(
    (sum, job) => sum + job.estimatedDuration,
    0
  );

  return {
    path,
    duration: criticalPathDuration,
    parallelizableSavings: totalSequentialDuration - criticalPathDuration,
  };
}
```

## Best Practices

1. **Measure before optimizing.** Profile your current pipeline to identify actual bottlenecks. The slowest step may not be what you expect. Use pipeline analytics to find the real performance killers before implementing any optimizations.

2. **Use concurrency controls to cancel redundant runs.** When a developer pushes multiple commits in quick succession, cancel the in-progress run for the previous commit. The GitHub Actions `concurrency` key with `cancel-in-progress: true` handles this automatically.

3. **Cache aggressively but validate cache correctness.** Cache node_modules, build artifacts, Playwright browsers, and Docker layers. But always verify that stale caches do not cause false-positive test results. Include lock file hashes in cache keys to invalidate on dependency changes.

4. **Split E2E tests across more shards than unit tests.** E2E tests are typically 10-50x slower than unit tests. A suite that benefits from 2 unit test shards may need 4-8 E2E test shards for balanced execution times.

5. **Run lint and type-check before tests.** These checks are fast (typically under 60 seconds) and catch a large class of issues. Running them before expensive test suites provides faster initial feedback when they fail.

6. **Use fail-fast: false for sharded jobs.** When tests are split across shards, a failure in shard 1 should not cancel shard 3. You want complete results from all shards to see the full scope of failures.

7. **Collect and store test timing data persistently.** Duration-based test splitting requires historical data to be effective. Collect timings after every CI run and cache them for future runs. Use exponential moving averages to smooth outliers.

8. **Implement selective test execution with a safety net.** When change detection cannot determine which tests to run (e.g., for config file changes), default to running all tests. A false positive (running unnecessary tests) is always safer than a false negative (missing a regression).

9. **Pre-warm caches on a schedule.** Run a scheduled workflow that installs dependencies and populates caches before the workday begins. This ensures the first PR of the day gets a cache hit instead of a cold start.

10. **Monitor pipeline duration trends over time.** Track P50 and P95 pipeline durations weekly. A gradual increase of 30 seconds per week adds up to 25 minutes over a year. Catch regressions early with automated alerting on duration spikes.

11. **Use service containers for integration test dependencies.** Instead of installing PostgreSQL or Redis in your workflow steps, use GitHub Actions service containers. They start in parallel with job setup and are ready when your tests need them.

12. **Keep Docker images minimal for CI runners.** If your CI uses custom Docker images, minimize their size. Every megabyte of image that needs to be pulled adds to every pipeline run. Use multi-stage builds and slim base images.

## Anti-Patterns to Avoid

**Running all tests on every PR regardless of changes.** A documentation-only PR does not need E2E tests. A frontend-only change does not need backend integration tests. Implement change detection to skip unnecessary work and save both time and compute resources.

**Using sequential job execution when parallelism is possible.** If unit tests and E2E tests have no dependency on each other, run them in parallel. Restructure your pipeline so that only actual data dependencies create sequential chains.

**Caching too broadly or too narrowly.** Caching `node_modules` without including the lock file hash in the cache key means stale dependencies persist. Caching only `node_modules` but not Playwright browsers means downloading 100+ MB of browser binaries on every run.

**Splitting tests by file count instead of duration.** Ten test files may take 10 seconds or 10 minutes depending on their content. Always use duration-based splitting when timing data is available to ensure balanced shard execution times.

**Ignoring the critical path.** Parallelizing jobs that are already off the critical path does not reduce total pipeline duration. Identify and focus optimization on the jobs that form the longest sequential chain.

**Not canceling redundant pipeline runs.** Without concurrency controls, every push creates a new pipeline run. Three pushes in 5 minutes create three full runs, wasting resources and delaying results for other developers waiting in the queue.

**Hard-coding shard counts.** A static 4-shard configuration may be wasteful for small PRs and insufficient for full test runs on main. Dynamically determine shard counts based on the scope of changes detected.

**Skipping tests to speed up the pipeline.** Disabling tests is not optimization; it is risk accumulation. Optimize the tests themselves (reduce flakiness, parallelize, cache) rather than removing them from the pipeline.

## Debugging Tips

**Cache misses on every run.** Verify that the cache key includes only deterministic inputs. Environment variables, timestamps, and random values in cache keys cause every run to miss. Use `hashFiles()` on lock files and configuration files for consistent keys.

**Sharded tests produce inconsistent results.** Test isolation issues become visible under sharding because tests run in different orders and different processes. Identify tests that depend on shared state (global variables, database records, file system artifacts) and fix them to be truly independent.

**Selective test execution misses a regression.** Review your change-to-test mapping configuration. Common gaps include: shared utility files that are not mapped to all their consumers, configuration changes that should trigger full runs, and transitive dependencies that are not tracked in the change map.

**Pipeline duration increases after adding caching.** This can happen when cache save and restore steps take longer than the operation they are caching. Very small caches (under 10 MB) may not be worth the overhead. Profile the cache steps themselves to verify they provide net savings.

**Test timings file grows unbounded.** Prune entries for test files that no longer exist. When files are renamed or deleted, their timing entries remain in the file indefinitely. Add a cleanup step that removes entries for files not present in the current codebase.

**GitHub Actions job matrix generates too many combinations.** Matrix strategies with multiple dimensions (OS x Node version x shard) can produce dozens of jobs. Use `include` and `exclude` to limit combinations to only those that provide unique value.

**Jobs fail with "No space left on device."** CI runners have limited disk space. Large caches, Docker images, and build artifacts can exhaust the available storage. Add cleanup steps between resource-intensive operations, use slimmer base images, and prune unnecessary artifacts before running tests.
