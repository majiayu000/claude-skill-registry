---
name: apscheduler
description: Advanced Python Scheduler - Task scheduling and job queue system
when_to_use: "Background task execution, periodic jobs, cron scheduling, distributed task processing"
tags: [scheduling, background-jobs, cron, async, task-queue]
---

# APScheduler

APScheduler is a flexible task scheduling and job queue system for Python applications. It supports both synchronous and asynchronous execution with multiple scheduling mechanisms including cron-style, interval-based, and one-off scheduling.

## Quick Start

### Basic Synchronous Scheduler

```python
from datetime import datetime
from apscheduler import Scheduler
from apscheduler.triggers.interval import IntervalTrigger

def tick():
    print(f"Tick: {datetime.now()}")

# Create and start scheduler with memory datastore
with Scheduler() as scheduler:
    scheduler.add_schedule(tick, IntervalTrigger(seconds=1))
    scheduler.run_until_stopped()
```

### Async Scheduler with FastAPI

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger

def cleanup_task():
    print("Running cleanup task...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncScheduler()
    async with scheduler:
        await scheduler.add_schedule(
            cleanup_task,
            IntervalTrigger(hours=1),
            id="cleanup"
        )
        await scheduler.start_in_background()
        yield

app = FastAPI(lifespan=lifespan)
```

## Common Patterns

### Schedulers

**In-memory scheduler (development):**

```python
from apscheduler import AsyncScheduler

async def main():
    async with AsyncScheduler() as scheduler:
        # Jobs lost on restart
        await scheduler.add_schedule(my_task, trigger)
        await scheduler.run_until_stopped()
```

**Persistent scheduler (production):**

```python
from sqlalchemy.ext.asyncio import create_async_engine
from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore

async def main():
    engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
    data_store = SQLAlchemyDataStore(engine)

    async with AsyncScheduler(data_store) as scheduler:
        # Jobs survive restarts
        await scheduler.add_schedule(my_task, trigger)
        await scheduler.run_until_stopped()
```

**Distributed scheduler:**

```python
from apscheduler import AsyncScheduler, SchedulerRole
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from apscheduler.eventbrokers.asyncpg import AsyncpgEventBroker

# Scheduler node - creates jobs from schedules
async def scheduler_node():
    async with AsyncScheduler(
        data_store,
        event_broker,
        role=SchedulerRole.scheduler
    ) as scheduler:
        await scheduler.add_schedule(task, trigger)
        await scheduler.run_until_stopped()

# Worker node - executes jobs only
async def worker_node():
    async with AsyncScheduler(
        data_store,
        event_broker,
        role=SchedulerRole.worker
    ) as scheduler:
        await scheduler.run_until_stopped()
```

### Jobs

**Simple function jobs:**

```python
def send_daily_report():
    generate_report()
    email_report("admin@example.com")

scheduler.add_schedule(
    send_daily_report,
    CronTrigger(hour=9, minute=0)  # 9 AM daily
)
```

**Jobs with arguments:**

```python
def process_data(source: str, destination: str, batch_size: int):
    # Data processing logic
    pass

scheduler.add_schedule(
    process_data,
    IntervalTrigger(hours=1),
    kwargs={
        'source': 's3://incoming',
        'destination': 's3://processed',
        'batch_size': 1000
    }
)
```

**Async jobs:**

```python
async def fetch_external_api():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com/data') as resp:
            data = await resp.json()
            await save_to_database(data)

scheduler.add_schedule(
    fetch_external_api,
    IntervalTrigger(minutes=5)
)
```

### Triggers

**Interval trigger:**

```python
from apscheduler.triggers.interval import IntervalTrigger

# Every 30 seconds
IntervalTrigger(seconds=30)

# Every 2 hours and 15 minutes
IntervalTrigger(hours=2, minutes=15)

# Every 3 days
IntervalTrigger(days=3)
```

**Cron trigger:**

```python
from apscheduler.triggers.cron import CronTrigger

# 9:00 AM Monday-Friday
CronTrigger(hour=9, minute=0, day_of_week='mon-fri')

# Every 15 minutes
CronTrigger(minute='*/15')

# Last day of month at midnight
CronTrigger(day='last', hour=0, minute=0)

# Using crontab syntax
CronTrigger.from_crontab('0 9 * * 1-5')  # 9 AM weekdays
```

**Date trigger (one-time):**

```python
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger

# 5 minutes from now
run_time = datetime.now() + timedelta(minutes=5)
DateTrigger(run_time=run_time)

# Specific datetime
DateTrigger(run_time=datetime(2024, 12, 31, 23, 59, 59))
```

**Calendar interval:**

```python
from apscheduler.triggers.calendarinterval import CalendarIntervalTrigger

# First day of every month at 9 AM
CalendarIntervalTrigger(months=1, hour=9, minute=0)

# Every Monday at 10 AM
CalendarIntervalTrigger(weeks=1, day_of_week='mon', hour=10, minute=0)
```

### Persistence

**SQLite:**

```python
engine = create_async_engine("sqlite+aiosqlite:///scheduler.db")
data_store = SQLAlchemyDataStore(engine)
```

**PostgreSQL:**

```python
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
data_store = SQLAlchemyDataStore(engine)
event_broker = AsyncpgEventBroker.from_async_sqla_engine(engine)
```

**Redis (event broker):**

```python
from apscheduler.eventbrokers.redis import RedisEventBroker

event_broker = RedisEventBroker.from_url("redis://localhost:6379")
```

### Job Management

**Get job results:**

```python
async def main():
    async with AsyncScheduler() as scheduler:
        await scheduler.start_in_background()

        # Add job with result retention
        job_id = await scheduler.add_job(
            calculate_result,
            args=(10, 20),
            result_expiration_time=timedelta(hours=1)
        )

        # Wait for result
        result = await scheduler.get_job_result(job_id, wait=True)
        print(f"Result: {result.return_value}")
```

**Schedule management:**

```python
# Pause schedule
await scheduler.pause_schedule("my_schedule")

# Resume schedule
await scheduler.unpause_schedule("my_schedule")

# Remove schedule
await scheduler.remove_schedule("my_schedule")

# Get schedule info
schedule = await scheduler.get_schedule("my_schedule")
print(f"Next run: {schedule.next_fire_time}")
```

**Event handling:**

```python
from apscheduler import JobAdded, JobReleased

def on_job_completed(event: JobReleased):
    if event.outcome == Outcome.success:
        print(f"Job {event.job_id} completed successfully")
    else:
        print(f"Job {event.job_id} failed: {event.exception}")

scheduler.subscribe(on_job_completed, JobReleased)
```

## Configuration

**Task defaults:**

```python
from apscheduler import TaskDefaults

task_defaults = TaskDefaults(
    job_executor='threadpool',
    max_running_jobs=3,
    misfire_grace_time=timedelta(minutes=5)
)

scheduler = AsyncScheduler(task_defaults=task_defaults)
```

**Job execution options:**

```python
# Configure task behavior
await scheduler.configure_task(
    my_function,
    job_executor='processpool',
    max_running_jobs=5,
    misfire_grace_time=timedelta(minutes=10)
)

# Override per schedule
await scheduler.add_schedule(
    my_function,
    trigger,
    job_executor='threadpool',  # Override default
    coalesce=CoalescePolicy.latest
)
```

## Requirements

```bash
# Core package
pip install apscheduler

# Database backends
pip install "apscheduler[postgresql]"  # PostgreSQL
pip install "apscheduler[mongodb]"     # MongoDB
pip install "apscheduler[sqlite]"      # SQLite

# Event brokers
pip install "apscheduler[redis]"       # Redis
pip install "apscheduler[mqtt]"        # MQTT
```

**Dependencies by use case:**

- **Basic scheduling**: `apscheduler`
- **PostgreSQL persistence**: `asyncpg`, `sqlalchemy`
- **Redis distributed**: `redis`
- **MongoDB**: `motor`
- **SQLite**: `aiosqlite`

## Best Practices

1. **Use persistent storage** for production to survive restarts
2. **Set appropriate misfire_grace_time** to handle system delays
3. **Use conflict policies** when updating schedules
4. **Subscribe to events** for monitoring and debugging
5. **Choose appropriate executors** (threadpool for I/O, processpool for CPU)
6. **Implement error handling** in job functions
7. **Use unique schedule IDs** for management operations
8. **Set result expiration** to prevent memory leaks
