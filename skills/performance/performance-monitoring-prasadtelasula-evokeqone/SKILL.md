---
name: performance-monitoring
description: Set up application monitoring, logging, error tracking, and performance metrics tracking. Use when implementing monitoring or debugging production issues.
allowed-tools: Read, Write, Edit, Bash, Glob
---

You implement performance monitoring and logging for the QA Team Portal.

## Requirements from PROJECT_PLAN.md

- Application logging and error tracking
- Performance metrics monitoring
- API response time tracking
- Page load time monitoring
- Error logging and alerting
- Success metrics tracking (usage, downloads, page views)

## Implementation

### 1. Backend Logging Setup

**Location:** `backend/app/core/logging_config.py`

```python
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

def setup_logging():
    """Configure application logging."""

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # File handler for all logs (rotating by size)
    file_handler = RotatingFileHandler(
        filename=LOGS_DIR / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)

    # Error log handler (rotating daily)
    error_handler = TimedRotatingFileHandler(
        filename=LOGS_DIR / "error.log",
        when='midnight',
        interval=1,
        backupCount=30,  # Keep 30 days
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)

    # Access log handler
    access_handler = TimedRotatingFileHandler(
        filename=LOGS_DIR / "access.log",
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    access_handler.setLevel(logging.INFO)
    access_handler.setFormatter(simple_formatter)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    # Access logger
    access_logger = logging.getLogger("access")
    access_logger.setLevel(logging.INFO)
    access_logger.addHandler(access_handler)
    access_logger.propagate = False

    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)

    return root_logger

logger = setup_logging()
```

**Initialize in main app:**

```python
# backend/app/main.py
from fastapi import FastAPI
from app.core.logging_config import logger

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")
```

### 2. Performance Middleware

**Location:** `backend/app/middleware/monitoring_middleware.py`

```python
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

logger = logging.getLogger(__name__)
access_logger = logging.getLogger("access")

class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Monitor API performance and log slow requests."""

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        # Get request details
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"

        try:
            response = await call_next(request)

            # Calculate response time
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = f"{process_time:.3f}"

            # Log access
            access_logger.info(
                f"{client_ip} - {method} {path} - "
                f"Status: {response.status_code} - "
                f"Time: {process_time:.3f}s"
            )

            # Log slow requests (> 200ms)
            if process_time > 0.2:
                logger.warning(
                    f"SLOW REQUEST: {method} {path} took {process_time:.3f}s - "
                    f"Client: {client_ip}"
                )

            # Log very slow requests (> 1s)
            if process_time > 1.0:
                logger.error(
                    f"VERY SLOW REQUEST: {method} {path} took {process_time:.3f}s - "
                    f"Client: {client_ip}"
                )

            return response

        except Exception as e:
            process_time = time.time() - start_time

            # Log exception
            logger.error(
                f"REQUEST FAILED: {method} {path} - "
                f"Error: {str(e)} - "
                f"Time: {process_time:.3f}s - "
                f"Client: {client_ip}",
                exc_info=True
            )

            raise

# Add to app
from app.middleware.monitoring_middleware import PerformanceMonitoringMiddleware
app.add_middleware(PerformanceMonitoringMiddleware)
```

### 3. Error Tracking with Sentry (Optional)

```bash
cd backend
uv pip install sentry-sdk[fastapi]
```

```python
# backend/app/core/config.py
class Settings(BaseSettings):
    SENTRY_DSN: Optional[str] = None
    ENVIRONMENT: str = "development"

# backend/app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from app.core.config import settings

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration()],
        environment=settings.ENVIRONMENT,
        traces_sample_rate=0.1,  # 10% of transactions
        profiles_sample_rate=0.1,  # 10% of profiles
        send_default_pii=False  # Don't send personally identifiable info
    )
    logger.info("Sentry error tracking initialized")
```

### 4. Metrics Tracking

**Location:** `backend/app/services/metrics_service.py`

```python
import time
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.metric import Metric

class MetricsService:
    """Track and retrieve application metrics."""

    @staticmethod
    async def record_metric(
        db: Session,
        metric_name: str,
        value: float,
        tags: Dict[str, str] = None
    ):
        """Record a metric value."""
        metric = Metric(
            name=metric_name,
            value=value,
            tags=tags or {},
            timestamp=datetime.utcnow()
        )
        db.add(metric)
        db.commit()

    @staticmethod
    async def record_page_view(
        db: Session,
        page_path: str,
        user_id: str = None
    ):
        """Record a page view."""
        await MetricsService.record_metric(
            db,
            metric_name="page_view",
            value=1,
            tags={
                "page": page_path,
                "user_id": user_id or "anonymous"
            }
        )

    @staticmethod
    async def record_tool_download(
        db: Session,
        tool_id: str,
        tool_name: str,
        user_id: str = None
    ):
        """Record a tool download."""
        await MetricsService.record_metric(
            db,
            metric_name="tool_download",
            value=1,
            tags={
                "tool_id": tool_id,
                "tool_name": tool_name,
                "user_id": user_id or "anonymous"
            }
        )

    @staticmethod
    async def get_page_views(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get page views grouped by page."""
        metrics = db.query(Metric).filter(
            Metric.name == "page_view",
            Metric.timestamp >= start_date,
            Metric.timestamp <= end_date
        ).all()

        # Group by page
        page_views = {}
        for metric in metrics:
            page = metric.tags.get("page", "unknown")
            page_views[page] = page_views.get(page, 0) + 1

        return [
            {"page": page, "views": count}
            for page, count in page_views.items()
        ]

    @staticmethod
    async def get_api_performance(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """Get API performance metrics."""
        metrics = db.query(Metric).filter(
            Metric.name == "api_response_time",
            Metric.timestamp >= start_date,
            Metric.timestamp <= end_date
        ).all()

        if not metrics:
            return {"average": 0, "min": 0, "max": 0, "count": 0}

        values = [m.value for m in metrics]
        return {
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }
```

**Metric Model:**

```python
# backend/app/models/metric.py
from sqlalchemy import Column, String, Float, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.base_class import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    tags = Column(JSON, nullable=False, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
```

### 5. Health Check Endpoints

**Location:** `backend/app/api/v1/endpoints/health.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.deps import get_db
from app.core.config import settings
import psutil
import time

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "qa-portal-api",
        "version": "1.0.0",
        "timestamp": time.time()
    }

@router.get("/health/db")
async def database_health(db: Session = Depends(get_db)):
    """Database connectivity check."""
    try:
        # Execute simple query
        result = db.execute(text("SELECT 1"))
        result.scalar()

        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "timestamp": time.time()
            }
        )

@router.get("/health/system")
async def system_health():
    """System resources check."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent
            },
            "disk": {
                "total": disk.total,
                "free": disk.free,
                "percent": disk.percent
            },
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }
        )

@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check for load balancer."""
    try:
        # Check database
        db.execute(text("SELECT 1"))

        # Check if essential services are running
        # Add more checks as needed

        return {"status": "ready"}
    except:
        raise HTTPException(503, {"status": "not ready"})
```

### 6. Frontend Performance Monitoring

**Location:** `frontend/src/utils/analytics.ts`

```typescript
interface PageViewEvent {
  page: string
  timestamp: number
  loadTime?: number
}

interface MetricEvent {
  name: string
  value: number
  tags?: Record<string, string>
}

class Analytics {
  private static instance: Analytics
  private apiUrl: string

  private constructor() {
    this.apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  }

  static getInstance(): Analytics {
    if (!Analytics.instance) {
      Analytics.instance = new Analytics()
    }
    return Analytics.instance
  }

  /**
   * Track page view
   */
  trackPageView(page: string) {
    const loadTime = this.getPageLoadTime()

    const event: PageViewEvent = {
      page,
      timestamp: Date.now(),
      loadTime
    }

    // Send to backend
    this.sendEvent('page_view', event)

    // Log to console in dev
    if (import.meta.env.DEV) {
      console.log('📊 Page View:', event)
    }
  }

  /**
   * Track custom event
   */
  trackEvent(name: string, data: Record<string, any>) {
    this.sendEvent(name, {
      ...data,
      timestamp: Date.now()
    })

    if (import.meta.env.DEV) {
      console.log(`📊 Event: ${name}`, data)
    }
  }

  /**
   * Track tool download
   */
  trackToolDownload(toolId: string, toolName: string) {
    this.trackEvent('tool_download', {
      tool_id: toolId,
      tool_name: toolName
    })
  }

  /**
   * Track error
   */
  trackError(error: Error, context?: Record<string, any>) {
    const errorData = {
      message: error.message,
      stack: error.stack,
      context,
      timestamp: Date.now(),
      url: window.location.href,
      userAgent: navigator.userAgent
    }

    this.sendEvent('error', errorData)

    console.error('❌ Error tracked:', errorData)
  }

  /**
   * Get page load time
   */
  private getPageLoadTime(): number | undefined {
    if (typeof window !== 'undefined' && window.performance) {
      const perfData = window.performance.timing
      const loadTime = perfData.loadEventEnd - perfData.navigationStart
      return loadTime > 0 ? loadTime : undefined
    }
    return undefined
  }

  /**
   * Send event to backend
   */
  private async sendEvent(name: string, data: any) {
    try {
      await fetch(`${this.apiUrl}/api/v1/metrics`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name,
          data
        })
      })
    } catch (error) {
      // Silently fail - don't break app if analytics fail
      console.warn('Failed to send analytics event:', error)
    }
  }
}

export const analytics = Analytics.getInstance()

// Track page views on route changes
export const useAnalytics = () => {
  const location = useLocation()

  useEffect(() => {
    analytics.trackPageView(location.pathname)
  }, [location])
}
```

**Usage in App:**

```typescript
// frontend/src/App.tsx
import { useAnalytics } from './utils/analytics'

function App() {
  // Track page views
  useAnalytics()

  return <Routes>...</Routes>
}

// Track button clicks
<Button onClick={() => {
  analytics.trackEvent('button_click', { button: 'download_tool' })
  handleDownload()
}}>
  Download
</Button>

// Track errors
try {
  await someAsyncOperation()
} catch (error) {
  analytics.trackError(error as Error, { operation: 'someAsyncOperation' })
}
```

### 7. Web Vitals Monitoring

```bash
cd frontend
npm install web-vitals
```

```typescript
// frontend/src/utils/webVitals.ts
import { onCLS, onFID, onFCP, onLCP, onTTFB } from 'web-vitals'
import { analytics } from './analytics'

export const reportWebVitals = () => {
  onCLS((metric) => {
    analytics.trackEvent('web_vital', {
      name: 'CLS',
      value: metric.value,
      rating: metric.rating
    })
  })

  onFID((metric) => {
    analytics.trackEvent('web_vital', {
      name: 'FID',
      value: metric.value,
      rating: metric.rating
    })
  })

  onFCP((metric) => {
    analytics.trackEvent('web_vital', {
      name: 'FCP',
      value: metric.value,
      rating: metric.rating
    })
  })

  onLCP((metric) => {
    analytics.trackEvent('web_vital', {
      name: 'LCP',
      value: metric.value,
      rating: metric.rating
    })
  })

  onTTFB((metric) => {
    analytics.trackEvent('web_vital', {
      name: 'TTFB',
      value: metric.value,
      rating: metric.rating
    })
  })
}

// Initialize in main.tsx
reportWebVitals()
```

### 8. Metrics Dashboard API

**Location:** `backend/app/api/v1/endpoints/metrics.py`

```python
@router.get("/admin/metrics/overview")
async def get_metrics_overview(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get metrics overview for the last N days."""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Page views
    page_views = await MetricsService.get_page_views(db, start_date, end_date)

    # API performance
    api_performance = await MetricsService.get_api_performance(db, start_date, end_date)

    # Tool downloads
    tool_downloads = db.query(Metric).filter(
        Metric.name == "tool_download",
        Metric.timestamp >= start_date
    ).count()

    # Active users
    active_users = db.query(User).filter(
        User.last_login >= start_date
    ).count()

    return {
        "period_days": days,
        "page_views": page_views,
        "api_performance": api_performance,
        "tool_downloads": tool_downloads,
        "active_users": active_users
    }
```

## Monitoring Best Practices

1. **Log Levels:**
   - DEBUG: Detailed diagnostic information
   - INFO: General informational messages
   - WARNING: Warning messages, but application continues
   - ERROR: Error messages, but application recovers
   - CRITICAL: Critical errors, application may crash

2. **What to Log:**
   - All API requests (access logs)
   - Errors and exceptions (with stack traces)
   - Slow operations (> 200ms)
   - Authentication events (login, logout, failures)
   - Admin actions (audit logs)
   - Database operations (migrations, backups)

3. **What NOT to Log:**
   - Passwords or sensitive credentials
   - Personal identifiable information (PII)
   - Credit card numbers
   - API keys or tokens

4. **Log Rotation:**
   - Rotate by size (10MB per file)
   - Rotate by time (daily for access logs)
   - Keep historical logs (30 days minimum)
   - Compress old logs to save space

5. **Alerting:**
   - Set up alerts for error rate spikes
   - Alert on slow response times (> 1s)
   - Alert on high resource usage (CPU > 80%, Memory > 90%)
   - Alert on failed health checks

## Troubleshooting

**No logs appearing:**
- Check logs directory permissions
- Verify logging configuration loaded
- Check log level settings
- Ensure handlers are attached to logger

**Logs filling disk:**
- Implement log rotation
- Reduce log level (INFO instead of DEBUG)
- Compress old logs
- Set up automated cleanup (delete logs > 30 days)

**Performance impact:**
- Use async logging if available
- Log to separate disk/partition
- Reduce log verbosity in production
- Use log sampling for high-volume events

## Report

✅ Application logging configured (rotating files)
✅ Performance monitoring middleware added
✅ Error tracking configured (Sentry optional)
✅ Metrics service implemented
✅ Health check endpoints created
✅ Frontend analytics tracking added
✅ Web Vitals monitoring configured
✅ Metrics dashboard API implemented
✅ Log rotation configured (30-day retention)
✅ Access logs separated from error logs
✅ Slow query logging enabled
