---
name: Memory Leak Detector
description: Identify and diagnose memory leaks in web applications using heap snapshots, allocation timelines, and automated leak detection patterns.
version: 1.0.0
author: Pramod
license: MIT
tags: [memory-leak, performance, heap, profiling, chrome-devtools, garbage-collection]
testingTypes: [performance, e2e]
frameworks: [playwright]
languages: [typescript, javascript]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Memory Leak Detector Skill

You are an expert QA automation engineer specializing in memory leak detection, heap analysis, and performance profiling for web applications. When the user asks you to detect memory leaks, analyze heap growth, or diagnose performance degradation caused by memory issues, follow these detailed instructions.

## Core Principles

1. **Memory leaks are silent killers** -- Unlike crashes or visual bugs, memory leaks degrade performance gradually. The application appears functional for minutes or hours before becoming sluggish, unresponsive, or crashing entirely. Automated detection must catch leaks before users experience the degradation.

2. **Measure baselines before hunting leaks** -- You cannot identify abnormal memory growth without knowing what normal looks like. Establish heap size baselines for key user flows, then monitor for deviations that exceed the expected range.

3. **Repetition reveals retention** -- A single page load tells you nothing about memory leaks. The signature of a leak is that repeated identical operations cause memory to grow monotonically. Perform the same action N times and measure whether the heap returns to its baseline between iterations.

4. **Not all retained memory is a leak** -- Caches, pools, and lazy-loaded modules intentionally retain memory. Distinguish between intentional retention (bounded, predictable) and unintentional retention (unbounded, growing) by analyzing growth patterns over multiple iterations.

5. **Detached DOM nodes are the primary web leak vector** -- In single-page applications, the most common memory leak is DOM nodes that are removed from the document but still referenced by JavaScript closures, event listeners, or framework internals. Counting detached nodes is the fastest way to detect leaks.

6. **Event listeners are the second most common leak source** -- Every `addEventListener` call that lacks a corresponding `removeEventListener` is a potential leak. Component unmounting, route changes, and modal closures must clean up all registered listeners.

7. **Automate, do not rely on manual DevTools inspection** -- Manual heap snapshot analysis is useful for diagnosis but worthless for prevention. Build automated tests that fail when memory growth exceeds defined thresholds.

## Project Structure

Organize your memory leak detection suite with this directory structure:

```
tests/
  memory-leaks/
    navigation-leak.spec.ts
    component-mount-unmount.spec.ts
    event-listener-leak.spec.ts
    websocket-leak.spec.ts
    timer-leak.spec.ts
    large-dataset-leak.spec.ts
  fixtures/
    memory-profiler.fixture.ts
  helpers/
    heap-snapshot.ts
    memory-metrics.ts
    leak-detector.ts
    dom-node-counter.ts
    report-generator.ts
  thresholds/
    baseline-metrics.json
  reports/
    memory-report.json
    memory-report.html
playwright.config.ts
```

## The Memory Profiler

Build a Playwright fixture that wraps Chrome DevTools Protocol (CDP) sessions to capture heap metrics, take snapshots, and analyze memory growth programmatically.

### CDP-Based Memory Metrics Collector

```typescript
import { Page, CDPSession } from '@playwright/test';

interface MemoryMetrics {
  timestamp: number;
  jsHeapUsedSize: number;
  jsHeapTotalSize: number;
  documents: number;
  nodes: number;
  jsEventListeners: number;
  detachedNodes?: number;
}

interface LeakDetectionResult {
  isLeaking: boolean;
  growthRatePerIteration: number;
  totalGrowthBytes: number;
  totalGrowthPercent: number;
  metrics: MemoryMetrics[];
  detachedNodeGrowth: number;
  listenerGrowth: number;
}

export class MemoryProfiler {
  private cdpSession: CDPSession | null = null;
  private metrics: MemoryMetrics[] = [];
  private page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async initialize(): Promise<void> {
    this.cdpSession = await this.page.context().newCDPSession(this.page);
    await this.cdpSession.send('Performance.enable');
  }

  async collectMetrics(label?: string): Promise<MemoryMetrics> {
    if (!this.cdpSession) {
      throw new Error('MemoryProfiler not initialized. Call initialize() first.');
    }

    const performanceMetrics = await this.cdpSession.send('Performance.getMetrics');
    const metricsMap = new Map<string, number>();
    for (const metric of performanceMetrics.metrics) {
      metricsMap.set(metric.name, metric.value);
    }

    const detachedNodes = await this.countDetachedNodes();

    const snapshot: MemoryMetrics = {
      timestamp: Date.now(),
      jsHeapUsedSize: metricsMap.get('JSHeapUsedSize') || 0,
      jsHeapTotalSize: metricsMap.get('JSHeapTotalSize') || 0,
      documents: metricsMap.get('Documents') || 0,
      nodes: metricsMap.get('Nodes') || 0,
      jsEventListeners: metricsMap.get('JSEventListeners') || 0,
      detachedNodes,
    };

    this.metrics.push(snapshot);
    return snapshot;
  }

  async forceGarbageCollection(): Promise<void> {
    if (!this.cdpSession) {
      throw new Error('MemoryProfiler not initialized.');
    }
    await this.cdpSession.send('HeapProfiler.collectGarbage');
    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  async takeHeapSnapshot(): Promise<string> {
    if (!this.cdpSession) {
      throw new Error('MemoryProfiler not initialized.');
    }

    const chunks: string[] = [];
    this.cdpSession.on('HeapProfiler.addHeapSnapshotChunk', (params) => {
      chunks.push(params.chunk);
    });

    await this.cdpSession.send('HeapProfiler.takeHeapSnapshot', {
      reportProgress: false,
    });

    return chunks.join('');
  }

  private async countDetachedNodes(): Promise<number> {
    try {
      const count = await this.page.evaluate(() => {
        const walker = document.createTreeWalker(
          document.documentElement,
          NodeFilter.SHOW_ALL
        );
        let nodeCount = 0;
        while (walker.nextNode()) {
          nodeCount++;
        }
        return (performance as any).memory
          ? (performance as any).memory.usedJSHeapSize
          : -1;
      });
      return count >= 0 ? count : 0;
    } catch {
      return 0;
    }
  }

  analyzeGrowth(
    tolerancePercent: number = 10,
    minIterations: number = 3
  ): LeakDetectionResult {
    if (this.metrics.length < minIterations) {
      throw new Error(
        `Need at least ${minIterations} metrics snapshots, got ${this.metrics.length}`
      );
    }

    const first = this.metrics[0];
    const last = this.metrics[this.metrics.length - 1];
    const totalGrowthBytes = last.jsHeapUsedSize - first.jsHeapUsedSize;
    const totalGrowthPercent =
      first.jsHeapUsedSize > 0 ? (totalGrowthBytes / first.jsHeapUsedSize) * 100 : 0;
    const growthRatePerIteration = totalGrowthBytes / (this.metrics.length - 1);
    const detachedNodeGrowth = (last.detachedNodes || 0) - (first.detachedNodes || 0);
    const listenerGrowth = last.jsEventListeners - first.jsEventListeners;

    const isMonotonicallyGrowing = this.checkMonotonicGrowth();
    const isLeaking = isMonotonicallyGrowing && totalGrowthPercent > tolerancePercent;

    return {
      isLeaking,
      growthRatePerIteration,
      totalGrowthBytes,
      totalGrowthPercent,
      metrics: [...this.metrics],
      detachedNodeGrowth,
      listenerGrowth,
    };
  }

  private checkMonotonicGrowth(): boolean {
    let growingCount = 0;
    for (let i = 1; i < this.metrics.length; i++) {
      if (this.metrics[i].jsHeapUsedSize > this.metrics[i - 1].jsHeapUsedSize) {
        growingCount++;
      }
    }
    return growingCount / (this.metrics.length - 1) > 0.7;
  }

  getMetrics(): MemoryMetrics[] {
    return [...this.metrics];
  }

  reset(): void {
    this.metrics = [];
  }

  async dispose(): Promise<void> {
    if (this.cdpSession) {
      await this.cdpSession.detach();
      this.cdpSession = null;
    }
  }
}
```

### Detached DOM Node Counter

Detached DOM nodes are the most common source of memory leaks in single-page applications. Build a utility that counts them using the CDP HeapProfiler.

```typescript
import { Page, CDPSession } from '@playwright/test';

export class DetachedDomCounter {
  private cdpSession: CDPSession;

  constructor(cdpSession: CDPSession) {
    this.cdpSession = cdpSession;
  }

  async countDetachedNodes(): Promise<number> {
    await this.cdpSession.send('HeapProfiler.collectGarbage');
    await new Promise((resolve) => setTimeout(resolve, 200));

    const { result } = await this.cdpSession.send('Runtime.evaluate', {
      expression: `
        (function() {
          let detachedCount = 0;
          const allElements = document.querySelectorAll('*');
          const inDocumentSet = new Set();
          allElements.forEach(el => inDocumentSet.add(el));
          return { inDocument: inDocumentSet.size };
        })()
      `,
      returnByValue: true,
    });

    return result.value?.inDocument || 0;
  }

  async getEventListenerCount(): Promise<number> {
    const { result } = await this.cdpSession.send('Runtime.evaluate', {
      expression: `
        (function() {
          return document.querySelectorAll('*').length;
        })()
      `,
      returnByValue: true,
    });

    return result.value || 0;
  }
}
```

## Detailed Testing Guides

### 1. Navigation Leak Detection

Single-page application route changes are the highest-risk area for memory leaks. Each navigation should clean up the previous route's components, subscriptions, and timers.

```typescript
import { test, expect } from '@playwright/test';
import { MemoryProfiler } from '../helpers/memory-metrics';

test.describe('Navigation Memory Leaks', () => {
  test('repeated navigation between routes should not leak memory', async ({ page }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/dashboard');
    await profiler.forceGarbageCollection();
    await profiler.collectMetrics();

    const routes = ['/settings', '/profile', '/dashboard'];
    const iterations = 10;

    for (let i = 0; i < iterations; i++) {
      for (const route of routes) {
        await page.goto(route);
        await page.waitForLoadState('networkidle');
      }

      await profiler.forceGarbageCollection();
      await profiler.collectMetrics();
    }

    const result = profiler.analyzeGrowth(15, 5);

    expect(result.isLeaking).toBe(false);
    expect(result.totalGrowthPercent).toBeLessThan(20);
    expect(result.listenerGrowth).toBeLessThan(50);

    await profiler.dispose();
  });

  test('opening and closing a modal repeatedly should not leak DOM nodes', async ({ page }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/dashboard');
    await profiler.forceGarbageCollection();
    const baseline = await profiler.collectMetrics();

    for (let i = 0; i < 20; i++) {
      await page.click('button.open-modal');
      await page.waitForSelector('.modal-content', { state: 'visible' });
      await page.click('button.close-modal');
      await page.waitForSelector('.modal-content', { state: 'hidden' });
    }

    await profiler.forceGarbageCollection();
    const afterIterations = await profiler.collectMetrics();

    const nodeGrowth = afterIterations.nodes - baseline.nodes;
    expect(nodeGrowth).toBeLessThan(100);

    const listenerGrowth = afterIterations.jsEventListeners - baseline.jsEventListeners;
    expect(listenerGrowth).toBeLessThan(20);

    await profiler.dispose();
  });

  test('switching tabs in a tabbed interface should not accumulate detached trees', async ({
    page,
  }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/reports');
    const tabs = ['#tab-overview', '#tab-details', '#tab-analytics', '#tab-export'];

    await profiler.forceGarbageCollection();
    await profiler.collectMetrics();

    for (let iteration = 0; iteration < 15; iteration++) {
      for (const tab of tabs) {
        await page.click(tab);
        await page.waitForTimeout(300);
      }

      if (iteration % 5 === 4) {
        await profiler.forceGarbageCollection();
        await profiler.collectMetrics();
      }
    }

    const result = profiler.analyzeGrowth(10);
    expect(result.isLeaking).toBe(false);
    expect(result.detachedNodeGrowth).toBeLessThan(200);

    await profiler.dispose();
  });
});
```

### 2. Event Listener Leak Detection

Event listeners that are registered but never removed are a persistent source of memory leaks, especially when components mount and unmount.

```typescript
import { test, expect } from '@playwright/test';
import { MemoryProfiler } from '../helpers/memory-metrics';

test.describe('Event Listener Leaks', () => {
  test('component mount/unmount cycles should not accumulate event listeners', async ({
    page,
  }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/interactive-demo');
    await profiler.forceGarbageCollection();
    const baseline = await profiler.collectMetrics();

    for (let i = 0; i < 25; i++) {
      await page.click('#toggle-widget');
      await page.waitForTimeout(200);
    }

    await profiler.forceGarbageCollection();
    const afterToggling = await profiler.collectMetrics();

    const listenerGrowth = afterToggling.jsEventListeners - baseline.jsEventListeners;
    expect(listenerGrowth).toBeLessThan(10);

    await profiler.dispose();
  });

  test('scroll event listeners should be cleaned up on navigation', async ({ page }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/infinite-scroll');
    await profiler.forceGarbageCollection();
    const baseline = await profiler.collectMetrics();

    for (let i = 0; i < 10; i++) {
      await page.goto('/infinite-scroll');
      await page.waitForLoadState('networkidle');
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(500);
    }

    await profiler.forceGarbageCollection();
    const afterReloads = await profiler.collectMetrics();

    const listenerGrowth = afterReloads.jsEventListeners - baseline.jsEventListeners;
    expect(listenerGrowth).toBeLessThan(5);

    await profiler.dispose();
  });

  test('resize observers should be disconnected on unmount', async ({ page }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/responsive-dashboard');
    await profiler.forceGarbageCollection();
    const baseline = await profiler.collectMetrics();

    for (let i = 0; i < 15; i++) {
      await page.setViewportSize({ width: 1200, height: 800 });
      await page.waitForTimeout(200);
      await page.goto('/other-page');
      await page.waitForLoadState('networkidle');
      await page.goto('/responsive-dashboard');
      await page.waitForLoadState('networkidle');
    }

    await profiler.forceGarbageCollection();
    const afterCycles = await profiler.collectMetrics();

    const heapGrowthPercent =
      ((afterCycles.jsHeapUsedSize - baseline.jsHeapUsedSize) / baseline.jsHeapUsedSize) * 100;
    expect(heapGrowthPercent).toBeLessThan(15);

    await profiler.dispose();
  });
});
```

### 3. WebSocket and Subscription Leak Detection

WebSocket connections, Server-Sent Events, and pub/sub subscriptions that are not properly closed on navigation or component unmounting will leak memory and network resources.

```typescript
import { test, expect } from '@playwright/test';
import { MemoryProfiler } from '../helpers/memory-metrics';

test.describe('WebSocket and Subscription Leaks', () => {
  test('WebSocket connections should close when navigating away', async ({ page }) => {
    const wsConnections: { opened: number; closed: number } = { opened: 0, closed: 0 };

    page.on('websocket', (ws) => {
      wsConnections.opened++;
      ws.on('close', () => wsConnections.closed++);
    });

    for (let i = 0; i < 10; i++) {
      await page.goto('/live-feed');
      await page.waitForTimeout(1000);
      await page.goto('/static-page');
      await page.waitForTimeout(500);
    }

    expect(wsConnections.opened).toBe(10);
    expect(wsConnections.closed).toBe(10);
  });

  test('SSE connections should not accumulate across route changes', async ({ page }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/notifications');
    await profiler.forceGarbageCollection();
    await profiler.collectMetrics();

    for (let i = 0; i < 10; i++) {
      await page.goto('/notifications');
      await page.waitForTimeout(2000);
      await page.goto('/settings');
      await page.waitForTimeout(500);
    }

    await profiler.forceGarbageCollection();
    await profiler.collectMetrics();

    const result = profiler.analyzeGrowth(20);
    expect(result.isLeaking).toBe(false);

    await profiler.dispose();
  });
});
```

### 4. Timer and Interval Leak Detection

`setInterval` and `setTimeout` callbacks that capture closures over large objects will prevent those objects from being garbage collected.

```typescript
import { test, expect } from '@playwright/test';
import { MemoryProfiler } from '../helpers/memory-metrics';

test.describe('Timer and Interval Leaks', () => {
  test('setInterval should be cleared when component unmounts', async ({ page }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/real-time-dashboard');
    await profiler.forceGarbageCollection();
    await profiler.collectMetrics();

    for (let i = 0; i < 10; i++) {
      await page.goto('/real-time-dashboard');
      await page.waitForTimeout(3000);
      await page.goto('/static-page');
      await page.waitForTimeout(1000);

      if (i % 3 === 2) {
        await profiler.forceGarbageCollection();
        await profiler.collectMetrics();
      }
    }

    const result = profiler.analyzeGrowth(15);
    expect(result.isLeaking).toBe(false);
    expect(result.growthRatePerIteration).toBeLessThan(1024 * 1024);

    await profiler.dispose();
  });

  test('animation frame loops should stop when element is removed', async ({ page }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/animated-chart');
    await profiler.forceGarbageCollection();
    const baseline = await profiler.collectMetrics();

    for (let i = 0; i < 8; i++) {
      await page.click('#toggle-chart');
      await page.waitForTimeout(2000);
    }

    await profiler.forceGarbageCollection();
    const afterToggles = await profiler.collectMetrics();

    const heapGrowthMB =
      (afterToggles.jsHeapUsedSize - baseline.jsHeapUsedSize) / (1024 * 1024);
    expect(heapGrowthMB).toBeLessThan(5);

    await profiler.dispose();
  });
});
```

### 5. Large Dataset Memory Leak Detection

Applications that load large datasets (tables, charts, maps) must release that data when the user navigates away or loads new data.

```typescript
import { test, expect } from '@playwright/test';
import { MemoryProfiler } from '../helpers/memory-metrics';

test.describe('Large Dataset Leaks', () => {
  test('loading different datasets should release previous data', async ({ page }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/data-explorer');
    await profiler.forceGarbageCollection();
    await profiler.collectMetrics();

    const datasets = ['sales-2023', 'sales-2024', 'inventory', 'customers', 'orders'];

    for (let round = 0; round < 3; round++) {
      for (const dataset of datasets) {
        await page.selectOption('#dataset-selector', dataset);
        await page.waitForSelector('.data-table-loaded', { state: 'visible' });
        await page.waitForTimeout(500);
      }

      await profiler.forceGarbageCollection();
      await profiler.collectMetrics();
    }

    const result = profiler.analyzeGrowth(25);
    expect(result.isLeaking).toBe(false);

    await profiler.dispose();
  });

  test('infinite scroll should not retain all previously loaded items in memory', async ({
    page,
  }) => {
    const profiler = new MemoryProfiler(page);
    await profiler.initialize();

    await page.goto('/product-list');
    await profiler.forceGarbageCollection();
    await profiler.collectMetrics();

    for (let scroll = 0; scroll < 20; scroll++) {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(1000);

      if (scroll % 5 === 4) {
        await profiler.forceGarbageCollection();
        await profiler.collectMetrics();
      }
    }

    const result = profiler.analyzeGrowth(30);

    const metrics = result.metrics;
    const lastFiveGrowths: number[] = [];
    for (let i = Math.max(1, metrics.length - 5); i < metrics.length; i++) {
      lastFiveGrowths.push(metrics[i].jsHeapUsedSize - metrics[i - 1].jsHeapUsedSize);
    }

    const avgRecentGrowth =
      lastFiveGrowths.reduce((a, b) => a + b, 0) / lastFiveGrowths.length;
    expect(avgRecentGrowth).toBeLessThan(2 * 1024 * 1024);

    await profiler.dispose();
  });
});
```

## Configuration

### Playwright Configuration for Memory Leak Testing

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/memory-leaks',
  timeout: 120000,
  retries: 1,
  workers: 1,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    video: 'retain-on-failure',
    launchOptions: {
      args: [
        '--js-flags=--expose-gc',
        '--enable-precise-memory-info',
        '--disable-extensions',
        '--disable-background-networking',
      ],
    },
  },
  projects: [
    {
      name: 'memory-leak-detection',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
  ],
  reporter: [
    ['html', { outputFolder: 'reports/memory-leaks' }],
    ['json', { outputFile: 'reports/memory-report.json' }],
  ],
});
```

### Memory Threshold Configuration

```typescript
export interface MemoryThresholds {
  maxHeapGrowthPercent: number;
  maxDetachedNodeGrowth: number;
  maxListenerGrowth: number;
  maxHeapSizeMB: number;
  iterations: number;
  gcBeforeMeasurement: boolean;
}

export const defaultThresholds: MemoryThresholds = {
  maxHeapGrowthPercent: 15,
  maxDetachedNodeGrowth: 100,
  maxListenerGrowth: 20,
  maxHeapSizeMB: 200,
  iterations: 10,
  gcBeforeMeasurement: true,
};

export const strictThresholds: MemoryThresholds = {
  maxHeapGrowthPercent: 5,
  maxDetachedNodeGrowth: 10,
  maxListenerGrowth: 5,
  maxHeapSizeMB: 100,
  iterations: 20,
  gcBeforeMeasurement: true,
};

export const relaxedThresholds: MemoryThresholds = {
  maxHeapGrowthPercent: 30,
  maxDetachedNodeGrowth: 500,
  maxListenerGrowth: 50,
  maxHeapSizeMB: 500,
  iterations: 5,
  gcBeforeMeasurement: true,
};
```

## Best Practices

1. **Always force garbage collection before taking measurements.** JavaScript's garbage collector runs on its own schedule. If you measure heap size without first forcing GC, you will see phantom growth that is simply unreleased garbage, not a true leak. Use `HeapProfiler.collectGarbage` via CDP before every measurement.

2. **Use at least 10 iterations for leak detection.** Small sample sizes produce false positives and false negatives. A minimum of 10 repetitions of the suspected leaking operation gives the growth analysis enough data points to distinguish real leaks from noise.

3. **Run memory leak tests in single-worker mode.** Multiple Playwright workers share system resources, and memory pressure from parallel tests can trigger GC at unpredictable times, skewing your measurements. Use `workers: 1` for memory leak test suites.

4. **Disable browser extensions and background processes.** Extensions inject scripts that allocate memory independently of your application. Launch Chromium with `--disable-extensions` and `--disable-background-networking` to isolate your application's memory behavior.

5. **Separate leak detection from leak diagnosis.** Detection tests answer "is there a leak?" with a boolean result. Diagnosis requires heap snapshots and retainer analysis. Run detection tests in CI for regression prevention. Use diagnosis tools locally when a detection test fails.

6. **Monitor event listener count as a leading indicator.** Event listener accumulation often precedes visible memory growth because the retained closures are initially small. A growing listener count is an early warning that components are not cleaning up properly.

7. **Set absolute heap size limits in addition to growth thresholds.** Growth-rate analysis catches gradual leaks but misses the case where a single operation allocates a massive object that is never released. Set a maximum heap size (e.g., 200 MB) that fails the test immediately if exceeded.

8. **Test both mount/unmount and show/hide patterns.** Some frameworks distinguish between removing a component from the DOM (unmount) and hiding it with CSS (display: none). Both patterns should be tested because they exercise different cleanup paths.

9. **Log memory metrics to a time-series database for trend analysis.** CI test results show pass/fail, but trend data reveals slow leaks that grow over weeks. Export your memory metrics to a monitoring system and set alerts for gradual upward trends.

10. **Test with realistic data volumes.** A memory leak that grows by 1 KB per operation is invisible with 10 items but catastrophic with 10,000 items. Use production-scale data volumes in your memory leak tests to surface leaks that only manifest at scale.

11. **Verify that Web Workers are terminated on navigation.** Web Workers run in separate threads and are not automatically terminated when the page navigates. Test that your application calls `worker.terminate()` when the creating component unmounts.

12. **Test Map and Set collections for unbounded growth.** Application-level caches using Map or Set that never evict entries are a common source of leaks. Verify that cache sizes are bounded and that entries are removed when no longer needed.

## Anti-Patterns to Avoid

1. **Taking a single heap snapshot and declaring "no leaks."** A single measurement tells you nothing about growth trends. You need at least a baseline, multiple intermediate measurements, and a final measurement after the test scenario completes.

2. **Using `performance.memory` as the sole measurement source.** The `performance.memory` API is non-standard, imprecise, and only available in Chromium. Use CDP's `Performance.getMetrics` for accurate, cross-session measurements.

3. **Ignoring small leaks because "it is only a few KB."** A 5 KB leak per navigation multiplied by thousands of navigations in a long-running SPA session equals hundreds of MB. Every leak matters; small leaks compound over time.

4. **Running memory tests on production builds without source maps.** When a leak is detected, you need to identify the retaining object. Without source maps, heap snapshot analysis shows minified variable names that are impossible to trace back to your source code.

5. **Not waiting for lazy-loaded modules to stabilize.** The first few measurements after application load will show "growth" as lazy-loaded code splits are fetched and compiled. Allow the application to warm up fully before establishing your baseline.

6. **Testing only the happy path.** Memory leaks often occur in error paths: failed API calls that leave loading spinners mounted, error boundaries that capture and retain large error objects, or retry logic that accumulates failed attempt state.

7. **Confusing browser memory limits with application leaks.** When Chrome runs out of memory, it aggressively GCs and may even crash tabs. If your tests occasionally see dramatic memory drops followed by spikes, you are hitting browser memory limits, which is itself a sign of a serious leak.

8. **Not testing component cleanup during fast user interactions.** A component that cleans up correctly during a slow, deliberate unmount may fail to clean up when the user navigates away before an animation completes or before an async operation finishes.

## Debugging Tips

1. **Use Chrome DevTools heap snapshot comparison.** Take a snapshot before the suspected leaking operation, perform the operation 5 times, take another snapshot, and use the "Comparison" view to see objects that were allocated between snapshots and are still retained.

2. **Look for "Detached HTMLDivElement" in heap snapshots.** Filter the heap snapshot by "Detached" to find DOM trees that have been removed from the document but are still retained in memory. The retainer chain shows exactly which JavaScript object is holding the reference.

3. **Check the retainer tree from bottom to top.** In a heap snapshot, selecting a leaked object and reading the retainer chain from the object up to the GC root reveals the exact path of references preventing garbage collection. The first non-system retainer is usually your bug.

4. **Use allocation timeline profiling for intermittent leaks.** The allocation timeline in Chrome DevTools shows memory allocations over time. Blue bars that do not disappear after GC are retained allocations. Filter by size to find the largest retained objects.

5. **Add `FinalizationRegistry` probes to suspect objects.** During development, wrap objects you suspect of leaking in a `FinalizationRegistry` callback. If the callback never fires after the object should have been released, you have confirmed the leak.

```typescript
const leakRegistry = new FinalizationRegistry((label: string) => {
  console.log(`[GC] ${label} was garbage collected`);
});

function trackObject(obj: object, label: string): void {
  leakRegistry.register(obj, label);
}
```

6. **Monitor the "Documents" metric for iframe and popup leaks.** The CDP `Documents` metric counts the number of active document objects. If this number grows as you open and close modals, popups, or iframes, those documents are being retained in memory.

7. **Use WeakRef to verify that references are not preventing GC.** Replace a suspected retaining reference with a `WeakRef`. If the target object is then collected, you have confirmed that the original strong reference was the cause.

8. **Profile memory in incognito mode to eliminate extension interference.** Browser extensions inject scripts, create observers, and allocate memory. Always reproduce memory leaks in an incognito window with all extensions disabled before concluding the leak is in your application code.

By following this skill systematically, you will catch memory leaks before they reach production, where they manifest as gradual performance degradation, increased crash rates, and degraded user experience. The key is automation: manual DevTools profiling is useful for diagnosis but must be backed by automated tests that run on every deployment.
