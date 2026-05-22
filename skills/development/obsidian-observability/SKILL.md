---
name: obsidian-observability
description: |
  Set up comprehensive logging and monitoring for Obsidian plugins.
  Use when implementing debug logging, tracking plugin performance,
  or setting up error reporting for your Obsidian plugin.
  Trigger with phrases like "obsidian logging", "obsidian monitoring",
  "obsidian debug", "track obsidian plugin".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Obsidian Observability

## Overview
Implement comprehensive logging, monitoring, and debugging capabilities for Obsidian plugins.

## Prerequisites
- Working Obsidian plugin
- Understanding of Developer Tools
- Basic TypeScript knowledge

## Observability Components

### Key Metrics
| Metric | Type | Purpose |
|--------|------|---------|
| Command execution time | Timer | Performance |
| File operations count | Counter | Usage patterns |
| Error rate | Counter | Reliability |
| Cache hit ratio | Gauge | Efficiency |
| Memory usage | Gauge | Resource health |

## Instructions

### Step 1: Structured Logger
```typescript
// src/utils/logger.ts
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context?: Record<string, any>;
  duration?: number;
}

export class Logger {
  private pluginId: string;
  private level: LogLevel;
  private history: LogEntry[] = [];
  private maxHistory: number = 100;

  private readonly levelPriority: Record<LogLevel, number> = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3,
  };

  constructor(pluginId: string, level: LogLevel = 'info') {
    this.pluginId = pluginId;
    this.level = level;
  }

  setLevel(level: LogLevel): void {
    this.level = level;
  }

  private shouldLog(level: LogLevel): boolean {
    return this.levelPriority[level] >= this.levelPriority[this.level];
  }

  private formatMessage(entry: LogEntry): string {
    const prefix = `[${this.pluginId}]`;
    const time = entry.timestamp.split('T')[1].split('.')[0];
    const level = entry.level.toUpperCase().padEnd(5);

    let message = `${prefix} ${time} ${level} ${entry.message}`;

    if (entry.duration !== undefined) {
      message += ` (${entry.duration.toFixed(2)}ms)`;
    }

    return message;
  }

  private log(level: LogLevel, message: string, context?: Record<string, any>): void {
    if (!this.shouldLog(level)) return;

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context,
    };

    // Store in history
    this.history.push(entry);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }

    // Console output
    const formatted = this.formatMessage(entry);
    const consoleMethod = level === 'debug' ? 'log' : level;

    if (context) {
      console[consoleMethod](formatted, context);
    } else {
      console[consoleMethod](formatted);
    }
  }

  debug(message: string, context?: Record<string, any>): void {
    this.log('debug', message, context);
  }

  info(message: string, context?: Record<string, any>): void {
    this.log('info', message, context);
  }

  warn(message: string, context?: Record<string, any>): void {
    this.log('warn', message, context);
  }

  error(message: string, error?: Error, context?: Record<string, any>): void {
    const errorContext = error ? {
      ...context,
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack,
      },
    } : context;

    this.log('error', message, errorContext);
  }

  // Timing helper
  time(label: string): () => void {
    const start = performance.now();
    return () => {
      const duration = performance.now() - start;
      const entry: LogEntry = {
        timestamp: new Date().toISOString(),
        level: 'debug',
        message: label,
        duration,
      };

      if (this.shouldLog('debug')) {
        console.log(this.formatMessage(entry));
      }

      this.history.push(entry);
    };
  }

  // Get log history for debugging
  getHistory(): LogEntry[] {
    return [...this.history];
  }

  // Export logs for support
  exportLogs(): string {
    return this.history.map(entry => {
      let line = `${entry.timestamp} [${entry.level}] ${entry.message}`;
      if (entry.duration) line += ` (${entry.duration}ms)`;
      if (entry.context) line += `\n  ${JSON.stringify(entry.context)}`;
      return line;
    }).join('\n');
  }
}
```

### Step 2: Metrics Collector
```typescript
// src/utils/metrics.ts
interface MetricValue {
  value: number;
  timestamp: number;
}

export class MetricsCollector {
  private counters = new Map<string, number>();
  private gauges = new Map<string, number>();
  private timers = new Map<string, MetricValue[]>();
  private maxTimerHistory = 100;

  // Counter operations
  increment(name: string, value: number = 1): void {
    const current = this.counters.get(name) || 0;
    this.counters.set(name, current + value);
  }

  getCounter(name: string): number {
    return this.counters.get(name) || 0;
  }

  // Gauge operations
  setGauge(name: string, value: number): void {
    this.gauges.set(name, value);
  }

  getGauge(name: string): number {
    return this.gauges.get(name) || 0;
  }

  // Timer operations
  recordTiming(name: string, durationMs: number): void {
    const timings = this.timers.get(name) || [];
    timings.push({ value: durationMs, timestamp: Date.now() });

    // Keep only recent timings
    while (timings.length > this.maxTimerHistory) {
      timings.shift();
    }

    this.timers.set(name, timings);
  }

  getTimerStats(name: string): {
    count: number;
    avg: number;
    min: number;
    max: number;
    p95: number;
  } | null {
    const timings = this.timers.get(name);
    if (!timings || timings.length === 0) return null;

    const values = timings.map(t => t.value).sort((a, b) => a - b);
    const sum = values.reduce((a, b) => a + b, 0);

    return {
      count: values.length,
      avg: sum / values.length,
      min: values[0],
      max: values[values.length - 1],
      p95: values[Math.floor(values.length * 0.95)],
    };
  }

  // Time a function
  async timeAsync<T>(name: string, fn: () => Promise<T>): Promise<T> {
    const start = performance.now();
    try {
      return await fn();
    } finally {
      this.recordTiming(name, performance.now() - start);
    }
  }

  timeSync<T>(name: string, fn: () => T): T {
    const start = performance.now();
    try {
      return fn();
    } finally {
      this.recordTiming(name, performance.now() - start);
    }
  }

  // Get all metrics
  getAllMetrics(): {
    counters: Record<string, number>;
    gauges: Record<string, number>;
    timers: Record<string, ReturnType<typeof this.getTimerStats>>;
  } {
    const timerStats: Record<string, ReturnType<typeof this.getTimerStats>> = {};
    for (const name of this.timers.keys()) {
      timerStats[name] = this.getTimerStats(name);
    }

    return {
      counters: Object.fromEntries(this.counters),
      gauges: Object.fromEntries(this.gauges),
      timers: timerStats,
    };
  }

  // Reset all metrics
  reset(): void {
    this.counters.clear();
    this.gauges.clear();
    this.timers.clear();
  }
}
```

### Step 3: Error Tracking
```typescript
// src/utils/error-tracker.ts
interface TrackedError {
  timestamp: string;
  error: {
    name: string;
    message: string;
    stack?: string;
  };
  context: Record<string, any>;
  count: number;
}

export class ErrorTracker {
  private errors = new Map<string, TrackedError>();
  private maxErrors = 50;

  track(error: Error, context: Record<string, any> = {}): void {
    const key = `${error.name}:${error.message}`;
    const existing = this.errors.get(key);

    if (existing) {
      existing.count++;
      existing.timestamp = new Date().toISOString();
      existing.context = { ...existing.context, ...context };
    } else {
      // Enforce max errors limit
      if (this.errors.size >= this.maxErrors) {
        const oldestKey = this.errors.keys().next().value;
        this.errors.delete(oldestKey);
      }

      this.errors.set(key, {
        timestamp: new Date().toISOString(),
        error: {
          name: error.name,
          message: error.message,
          stack: error.stack,
        },
        context,
        count: 1,
      });
    }
  }

  getErrors(): TrackedError[] {
    return Array.from(this.errors.values())
      .sort((a, b) => b.count - a.count);
  }

  getMostCommon(limit: number = 5): TrackedError[] {
    return this.getErrors().slice(0, limit);
  }

  clear(): void {
    this.errors.clear();
  }

  // Safe wrapper for async functions
  wrapAsync<T>(
    fn: () => Promise<T>,
    context: Record<string, any> = {}
  ): Promise<T> {
    return fn().catch((error: Error) => {
      this.track(error, context);
      throw error;
    });
  }

  // Export for debugging
  export(): string {
    return JSON.stringify(this.getErrors(), null, 2);
  }
}
```

### Step 4: Debug Panel View
```typescript
// src/ui/views/debug-view.ts
import { ItemView, WorkspaceLeaf } from 'obsidian';
import type MyPlugin from '../../main';

export const DEBUG_VIEW_TYPE = 'plugin-debug-view';

export class DebugView extends ItemView {
  private plugin: MyPlugin;
  private refreshInterval: number;

  constructor(leaf: WorkspaceLeaf, plugin: MyPlugin) {
    super(leaf);
    this.plugin = plugin;
  }

  getViewType(): string {
    return DEBUG_VIEW_TYPE;
  }

  getDisplayText(): string {
    return 'Plugin Debug';
  }

  getIcon(): string {
    return 'bug';
  }

  async onOpen() {
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass('plugin-debug-view');

    this.render(container);

    // Auto-refresh every 5 seconds
    this.refreshInterval = window.setInterval(() => {
      this.render(container);
    }, 5000);

    this.registerInterval(this.refreshInterval);
  }

  private render(container: Element) {
    container.empty();

    // Metrics section
    container.createEl('h3', { text: 'Metrics' });
    const metricsDiv = container.createDiv({ cls: 'debug-section' });
    this.renderMetrics(metricsDiv);

    // Errors section
    container.createEl('h3', { text: 'Recent Errors' });
    const errorsDiv = container.createDiv({ cls: 'debug-section' });
    this.renderErrors(errorsDiv);

    // Logs section
    container.createEl('h3', { text: 'Recent Logs' });
    const logsDiv = container.createDiv({ cls: 'debug-section' });
    this.renderLogs(logsDiv);

    // Actions
    const actionsDiv = container.createDiv({ cls: 'debug-actions' });
    this.renderActions(actionsDiv);
  }

  private renderMetrics(container: Element) {
    const metrics = this.plugin.metrics.getAllMetrics();

    // Counters
    container.createEl('h4', { text: 'Counters' });
    const countersList = container.createEl('ul');
    for (const [name, value] of Object.entries(metrics.counters)) {
      countersList.createEl('li', { text: `${name}: ${value}` });
    }

    // Timers
    container.createEl('h4', { text: 'Timers' });
    const timersList = container.createEl('ul');
    for (const [name, stats] of Object.entries(metrics.timers)) {
      if (stats) {
        timersList.createEl('li', {
          text: `${name}: avg=${stats.avg.toFixed(2)}ms, p95=${stats.p95.toFixed(2)}ms (n=${stats.count})`,
        });
      }
    }
  }

  private renderErrors(container: Element) {
    const errors = this.plugin.errorTracker.getMostCommon(5);

    if (errors.length === 0) {
      container.createEl('p', { text: 'No errors recorded', cls: 'muted' });
      return;
    }

    const list = container.createEl('ul');
    for (const error of errors) {
      const item = list.createEl('li');
      item.createEl('strong', { text: `${error.error.name}: ` });
      item.createSpan({ text: error.error.message });
      item.createEl('span', {
        text: ` (${error.count}x)`,
        cls: 'error-count',
      });
    }
  }

  private renderLogs(container: Element) {
    const logs = this.plugin.logger.getHistory().slice(-10).reverse();

    const pre = container.createEl('pre', { cls: 'log-output' });
    for (const log of logs) {
      const line = pre.createEl('div', { cls: `log-${log.level}` });
      line.textContent = `[${log.level}] ${log.message}`;
    }
  }

  private renderActions(container: Element) {
    const exportBtn = container.createEl('button', { text: 'Export Debug Data' });
    exportBtn.addEventListener('click', () => this.exportDebugData());

    const clearBtn = container.createEl('button', { text: 'Clear Data' });
    clearBtn.addEventListener('click', () => {
      this.plugin.metrics.reset();
      this.plugin.errorTracker.clear();
      this.render(this.containerEl.children[1]);
    });
  }

  private exportDebugData() {
    const data = {
      timestamp: new Date().toISOString(),
      plugin: this.plugin.manifest.id,
      version: this.plugin.manifest.version,
      metrics: this.plugin.metrics.getAllMetrics(),
      errors: this.plugin.errorTracker.getErrors(),
      logs: this.plugin.logger.exportLogs(),
    };

    // Create download
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${this.plugin.manifest.id}-debug-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async onClose() {
    if (this.refreshInterval) {
      window.clearInterval(this.refreshInterval);
    }
  }
}
```

### Step 5: Integration in Main Plugin
```typescript
// src/main.ts
import { Plugin } from 'obsidian';
import { Logger } from './utils/logger';
import { MetricsCollector } from './utils/metrics';
import { ErrorTracker } from './utils/error-tracker';
import { DebugView, DEBUG_VIEW_TYPE } from './ui/views/debug-view';

export default class MyPlugin extends Plugin {
  logger: Logger;
  metrics: MetricsCollector;
  errorTracker: ErrorTracker;

  async onload() {
    // Initialize observability
    this.logger = new Logger(this.manifest.id, 'debug');
    this.metrics = new MetricsCollector();
    this.errorTracker = new ErrorTracker();

    this.logger.info('Plugin loading');
    const endLoadTime = this.logger.time('plugin-load');

    // Register debug view (dev mode only)
    if (process.env.NODE_ENV !== 'production') {
      this.registerView(
        DEBUG_VIEW_TYPE,
        (leaf) => new DebugView(leaf, this)
      );

      this.addCommand({
        id: 'open-debug-view',
        name: 'Open Debug View',
        callback: () => this.openDebugView(),
      });
    }

    // Track command usage
    this.addCommand({
      id: 'my-command',
      name: 'My Command',
      callback: async () => {
        this.metrics.increment('command.my-command');
        await this.metrics.timeAsync('command.my-command.duration', async () => {
          // Command implementation
        });
      },
    });

    endLoadTime();
    this.logger.info('Plugin loaded');
  }

  private async openDebugView() {
    const leaf = this.app.workspace.getRightLeaf(false);
    await leaf.setViewState({ type: DEBUG_VIEW_TYPE, active: true });
    this.app.workspace.revealLeaf(leaf);
  }
}
```

## Output
- Structured logger with levels and history
- Metrics collection (counters, gauges, timers)
- Error tracking with deduplication
- Debug panel view for runtime inspection
- Export capability for support

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Too much logging | Debug level in prod | Set level to 'error' |
| Memory growth | Unbounded history | Limit history size |
| Performance impact | Sync logging | Use async logging |
| Missing context | No error tracking | Wrap async calls |

## Examples

### Styles for Debug View
```css
/* styles.css */
.plugin-debug-view {
  padding: 16px;
}

.debug-section {
  margin-bottom: 24px;
  padding: 12px;
  background: var(--background-secondary);
  border-radius: 4px;
}

.log-output {
  font-family: monospace;
  font-size: 12px;
  max-height: 200px;
  overflow-y: auto;
}

.log-debug { color: var(--text-muted); }
.log-info { color: var(--text-normal); }
.log-warn { color: var(--text-warning); }
.log-error { color: var(--text-error); }

.error-count {
  color: var(--text-error);
  font-weight: bold;
}

.debug-actions button {
  margin-right: 8px;
}
```

## Resources
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Obsidian Developer Tools](https://docs.obsidian.md/Plugins/Guides/Developer+tools)

## Next Steps
For incident response, see `obsidian-incident-runbook`.
