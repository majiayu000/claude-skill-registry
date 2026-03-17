---
name: graceful-shutdown
description: Implement graceful shutdown procedures to handle SIGTERM signals, drain connections, complete in-flight requests, and clean up resources properly. Use when deploying containerized applications, handling server restarts, or ensuring zero-downtime deployments.
---

# Graceful Shutdown

## Overview

Implement proper shutdown procedures to ensure all requests are completed, connections are closed, and resources are released before process termination.

## When to Use

- Kubernetes/Docker deployments
- Rolling updates and deployments
- Server restarts
- Load balancer drain periods
- Zero-downtime deployments
- Process managers (PM2, systemd)
- Long-running background jobs
- Database connection cleanup

## Shutdown Phases

```
1. Receive SIGTERM signal
2. Stop accepting new requests
3. Drain active connections
4. Complete in-flight requests
5. Close database connections
6. Flush logs and metrics
7. Exit process
```

## Implementation Examples

### 1. **Express.js Graceful Shutdown**

```typescript
import express from 'express';
import http from 'http';

class GracefulShutdownServer {
  private app: express.Application;
  private server: http.Server;
  private isShuttingDown = false;
  private activeConnections = new Set<any>();
  private shutdownTimeout = 30000; // 30 seconds

  constructor() {
    this.app = express();
    this.server = http.createServer(this.app);
    this.setupMiddleware();
    this.setupRoutes();
    this.setupShutdownHandlers();
  }

  private setupMiddleware(): void {
    // Track active connections
    this.app.use((req, res, next) => {
      if (this.isShuttingDown) {
        res.set('Connection', 'close');
        return res.status(503).json({
          error: 'Server is shutting down'
        });
      }

      this.activeConnections.add(res);

      res.on('finish', () => {
        this.activeConnections.delete(res);
      });

      res.on('close', () => {
        this.activeConnections.delete(res);
      });

      next();
    });
  }

  private setupRoutes(): void {
    this.app.get('/health', (req, res) => {
      if (this.isShuttingDown) {
        return res.status(503).json({ status: 'shutting_down' });
      }
      res.json({ status: 'ok' });
    });

    this.app.get('/api/data', async (req, res) => {
      // Simulate long-running request
      await new Promise(resolve => setTimeout(resolve, 5000));
      res.json({ data: 'response' });
    });
  }

  private setupShutdownHandlers(): void {
    const signals: NodeJS.Signals[] = ['SIGTERM', 'SIGINT'];

    signals.forEach(signal => {
      process.on(signal, () => {
        console.log(`Received ${signal}, starting graceful shutdown...`);
        this.gracefulShutdown(signal);
      });
    });

    // Handle uncaught exceptions
    process.on('uncaughtException', (error) => {
      console.error('Uncaught exception:', error);
      this.gracefulShutdown('UNCAUGHT_EXCEPTION');
    });

    process.on('unhandledRejection', (reason, promise) => {
      console.error('Unhandled rejection:', reason);
      this.gracefulShutdown('UNHANDLED_REJECTION');
    });
  }

  private async gracefulShutdown(signal: string): Promise<void> {
    if (this.isShuttingDown) {
      console.log('Shutdown already in progress');
      return;
    }

    this.isShuttingDown = true;
    console.log(`Starting graceful shutdown (${signal})`);

    // Set shutdown timeout
    const shutdownTimer = setTimeout(() => {
      console.error('Shutdown timeout reached, forcing exit');
      process.exit(1);
    }, this.shutdownTimeout);

    try {
      // 1. Stop accepting new connections
      await this.stopAcceptingConnections();

      // 2. Wait for active requests to complete
      await this.waitForActiveConnections();

      // 3. Close server
      await this.closeServer();

      // 4. Cleanup resources
      await this.cleanupResources();

      console.log('Graceful shutdown completed');
      clearTimeout(shutdownTimer);
      process.exit(0);
    } catch (error) {
      console.error('Error during shutdown:', error);
      clearTimeout(shutdownTimer);
      process.exit(1);
    }
  }

  private async stopAcceptingConnections(): Promise<void> {
    console.log('Stopping new connections...');
    return new Promise((resolve) => {
      this.server.close(() => {
        console.log('Server stopped accepting new connections');
        resolve();
      });
    });
  }

  private async waitForActiveConnections(): Promise<void> {
    console.log(`Waiting for ${this.activeConnections.size} active connections...`);

    const checkInterval = 100;
    const maxWait = this.shutdownTimeout - 5000;
    let waited = 0;

    while (this.activeConnections.size > 0 && waited < maxWait) {
      await new Promise(resolve => setTimeout(resolve, checkInterval));
      waited += checkInterval;

      if (waited % 1000 === 0) {
        console.log(`Still waiting for ${this.activeConnections.size} connections...`);
      }
    }

    if (this.activeConnections.size > 0) {
      console.warn(`Force closing ${this.activeConnections.size} remaining connections`);
      this.activeConnections.forEach((res: any) => {
        res.destroy();
      });
    }

    console.log('All connections closed');
  }

  private async closeServer(): Promise<void> {
    // Server already closed in stopAcceptingConnections
    console.log('Server closed');
  }

  private async cleanupResources(): Promise<void> {
    console.log('Cleaning up resources...');

    // Close database connections
    await this.closeDatabaseConnections();

    // Flush logs
    await this.flushLogs();

    // Close any other resources
    await this.closeOtherResources();

    console.log('Resources cleaned up');
  }

  private async closeDatabaseConnections(): Promise<void> {
    // Close database connections
    console.log('Closing database connections...');
    // await db.close();
  }

  private async flushLogs(): Promise<void> {
    // Flush any pending logs
    console.log('Flushing logs...');
  }

  private async closeOtherResources(): Promise<void> {
    // Close Redis, message queues, etc.
    console.log('Closing other resources...');
  }

  start(port: number): void {
    this.server.listen(port, () => {
      console.log(`Server listening on port ${port}`);
    });
  }
}

// Usage
const server = new GracefulShutdownServer();
server.start(3000);
```

### 2. **Kubernetes-Aware Shutdown**

```typescript
class KubernetesGracefulShutdown {
  private isReady = true;
  private isLive = true;
  private shutdownDelay = 5000; // K8s propagation delay

  setupProbes(app: express.Application): void {
    // Readiness probe
    app.get('/health/ready', (req, res) => {
      if (this.isReady) {
        res.status(200).json({ status: 'ready' });
      } else {
        res.status(503).json({ status: 'not_ready' });
      }
    });

    // Liveness probe
    app.get('/health/live', (req, res) => {
      if (this.isLive) {
        res.status(200).json({ status: 'alive' });
      } else {
        res.status(503).json({ status: 'not_alive' });
      }
    });
  }

  async shutdown(): Promise<void> {
    console.log('Kubernetes graceful shutdown initiated');

    // 1. Mark as not ready (fail readiness probe)
    this.isReady = false;
    console.log('Marked as not ready');

    // 2. Wait for K8s to remove pod from service endpoints
    console.log(`Waiting ${this.shutdownDelay}ms for endpoint propagation...`);
    await new Promise(resolve => setTimeout(resolve, this.shutdownDelay));

    // 3. Continue with normal graceful shutdown
    // ... rest of shutdown logic
  }
}
```

### 3. **Worker Process Shutdown**

```typescript
import Queue from 'bull';

class WorkerShutdown {
  private queue: Queue.Queue;
  private isProcessing = new Map<string, boolean>();

  constructor(queue: Queue.Queue) {
    this.queue = queue;
    this.setupWorker();
    this.setupShutdownHandlers();
  }

  private setupWorker(): void {
    this.queue.process('task', 5, async (job) => {
      const jobId = job.id!.toString();
      this.isProcessing.set(jobId, true);

      try {
        console.log(`Processing job ${jobId}`);
        await this.processJob(job);
        console.log(`Completed job ${jobId}`);
      } finally {
        this.isProcessing.delete(jobId);
      }
    });
  }

  private async processJob(job: Queue.Job): Promise<void> {
    // Job processing logic
    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  private setupShutdownHandlers(): void {
    process.on('SIGTERM', () => {
      console.log('SIGTERM received, shutting down worker...');
      this.shutdownWorker();
    });
  }

  private async shutdownWorker(): Promise<void> {
    console.log('Pausing queue...');
    await this.queue.pause(true, true);

    console.log(`Waiting for ${this.isProcessing.size} jobs to complete...`);

    // Wait for current jobs to finish
    const checkInterval = 500;
    const maxWait = 30000;
    let waited = 0;

    while (this.isProcessing.size > 0 && waited < maxWait) {
      await new Promise(resolve => setTimeout(resolve, checkInterval));
      waited += checkInterval;

      if (waited % 5000 === 0) {
        console.log(`Still processing ${this.isProcessing.size} jobs...`);
      }
    }

    if (this.isProcessing.size > 0) {
      console.warn(`Forcing shutdown with ${this.isProcessing.size} jobs remaining`);
    }

    console.log('Closing queue...');
    await this.queue.close();

    console.log('Worker shutdown complete');
    process.exit(0);
  }
}
```

### 4. **Database Connection Pool Shutdown**

```typescript
import { Pool } from 'pg';

class DatabaseShutdown {
  private pool: Pool;
  private activeQueries = new Set<Promise<any>>();

  constructor(pool: Pool) {
    this.pool = pool;
    this.setupQueryTracking();
  }

  private setupQueryTracking(): void {
    const originalQuery = this.pool.query.bind(this.pool);

    this.pool.query = (...args: any[]) => {
      const queryPromise = originalQuery(...args);

      this.activeQueries.add(queryPromise);

      queryPromise.finally(() => {
        this.activeQueries.delete(queryPromise);
      });

      return queryPromise;
    };
  }

  async shutdown(): Promise<void> {
    console.log('Shutting down database connections...');

    // Wait for active queries
    if (this.activeQueries.size > 0) {
      console.log(`Waiting for ${this.activeQueries.size} active queries...`);

      await Promise.race([
        Promise.all(Array.from(this.activeQueries)),
        new Promise(resolve => setTimeout(resolve, 5000))
      ]);
    }

    // Close pool
    console.log('Ending pool...');
    await this.pool.end();

    console.log('Database connections closed');
  }
}
```

### 5. **PM2 Graceful Shutdown**

```typescript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'api-server',
    script: './dist/server.js',
    instances: 4,
    exec_mode: 'cluster',
    kill_timeout: 30000, // Wait 30s for graceful shutdown
    wait_ready: true,
    listen_timeout: 10000,
    shutdown_with_message: true
  }]
};

// server.ts
import express from 'express';

const app = express();
const port = process.env.PORT || 3000;

// ... setup routes ...

const server = app.listen(port, () => {
  console.log(`Server started on port ${port}`);

  // Signal to PM2 that app is ready
  if (process.send) {
    process.send('ready');
  }
});

// Handle shutdown message from PM2
process.on('message', (msg) => {
  if (msg === 'shutdown') {
    console.log('Received shutdown message from PM2');
    gracefulShutdown();
  }
});

async function gracefulShutdown() {
  console.log('Starting graceful shutdown...');

  // Stop accepting new connections
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });

  // Force shutdown after timeout
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, 28000); // Less than PM2's kill_timeout
}
```

### 6. **Python/Flask Graceful Shutdown**

```python
import signal
import sys
import time
from flask import Flask, request, g
from threading import Lock

app = Flask(__name__)

class GracefulShutdown:
    def __init__(self):
        self.is_shutting_down = False
        self.active_requests = 0
        self.lock = Lock()

    def before_request(self):
        """Track active requests."""
        if self.is_shutting_down:
            return {'error': 'Server is shutting down'}, 503

        with self.lock:
            self.active_requests += 1

    def after_request(self, response):
        """Decrement active requests."""
        with self.lock:
            self.active_requests -= 1
        return response

    def shutdown(self, signum, frame):
        """Handle shutdown signal."""
        print(f"Received signal {signum}, starting graceful shutdown...")
        self.is_shutting_down = True

        # Wait for active requests
        max_wait = 30
        waited = 0

        while self.active_requests > 0 and waited < max_wait:
            print(f"Waiting for {self.active_requests} active requests...")
            time.sleep(1)
            waited += 1

        if self.active_requests > 0:
            print(f"Force closing with {self.active_requests} requests remaining")

        print("Graceful shutdown complete")
        sys.exit(0)

# Setup graceful shutdown
shutdown_handler = GracefulShutdown()
app.before_request(shutdown_handler.before_request)
app.after_request(shutdown_handler.after_request)

signal.signal(signal.SIGTERM, shutdown_handler.shutdown)
signal.signal(signal.SIGINT, shutdown_handler.shutdown)

@app.route('/health')
def health():
    if shutdown_handler.is_shutting_down:
        return {'status': 'shutting_down'}, 503
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Best Practices

### ✅ DO
- Handle SIGTERM and SIGINT signals
- Stop accepting new requests immediately
- Wait for in-flight requests to complete
- Set reasonable shutdown timeouts
- Close database connections properly
- Flush logs and metrics
- Fail health checks during shutdown
- Test shutdown procedures
- Log shutdown progress
- Use graceful shutdown in containers

### ❌ DON'T
- Ignore shutdown signals
- Force kill processes without cleanup
- Set unreasonably long timeouts
- Skip resource cleanup
- Forget to close connections
- Block shutdown indefinitely

## Kubernetes Configuration

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: api-server:latest
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 5"]
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
          initialDelaySeconds: 15
          periodSeconds: 10
      terminationGracePeriodSeconds: 30
```

## Resources

- [Kubernetes Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Node.js Signal Events](https://nodejs.org/api/process.html#process_signal_events)
