# High Availability Patterns

Production-ready HA patterns for cryptocurrency trading systems with 99.99% uptime.

## Active-Passive Architecture with Redis Leader Election

```python
import redis
import asyncio
import time
import uuid
from typing import Optional

class LeaderElection:
    """Redis-based leader election for active-passive HA"""

    def __init__(
        self,
        redis_client: redis.Redis,
        service_name: str,
        ttl_seconds: int = 10,
        instance_id: Optional[str] = None
    ):
        self.redis = redis_client
        self.service_name = service_name
        self.ttl = ttl_seconds
        self.instance_id = instance_id or str(uuid.uuid4())
        self.is_leader = False
        self.lock_key = f"leader:{service_name}"

    async def run_leader_election(self):
        """Continuous leader election loop"""
        while True:
            try:
                # Try to acquire leadership
                acquired = self.redis.set(
                    self.lock_key,
                    self.instance_id,
                    nx=True,  # Only set if not exists
                    ex=self.ttl  # Expire after TTL
                )

                if acquired:
                    if not self.is_leader:
                        logger.info(f"Instance {self.instance_id} became LEADER")
                        self.is_leader = True
                        await self._on_become_leader()

                    # Renew leadership
                    await self._renew_leadership()

                else:
                    # Check if we were leader before
                    if self.is_leader:
                        logger.warning(f"Instance {self.instance_id} lost leadership")
                        self.is_leader = False
                        await self._on_lose_leadership()

                # Sleep for half the TTL before renewing
                await asyncio.sleep(self.ttl / 2)

            except redis.RedisError as e:
                logger.error(f"Leader election error: {e}")
                self.is_leader = False
                await asyncio.sleep(1)

    async def _renew_leadership(self):
        """Renew leadership lock"""
        try:
            # Only renew if we still hold the lock
            current_leader = self.redis.get(self.lock_key)
            if current_leader and current_leader.decode() == self.instance_id:
                self.redis.expire(self.lock_key, self.ttl)
            else:
                self.is_leader = False
                logger.warning("Lost leadership during renewal")

        except redis.RedisError as e:
            logger.error(f"Leadership renewal failed: {e}")
            self.is_leader = False

    async def _on_become_leader(self):
        """Hook called when instance becomes leader"""
        # Perform state reconciliation
        await self._reconcile_state()

        # Start active trading
        await self._start_trading_engine()

        # Send notification
        logger.info("Transitioned to ACTIVE state")

    async def _on_lose_leadership(self):
        """Hook called when instance loses leadership"""
        # Stop trading immediately
        await self._stop_trading_engine()

        # Flush pending orders
        await self._flush_pending_orders()

        logger.info("Transitioned to PASSIVE state")
```

## State Reconciliation on Failover

```python
from dataclasses import dataclass
from typing import Dict, List
import asyncio

@dataclass
class ReconciliationReport:
    open_orders_found: int
    orders_cancelled: int
    positions_synced: int
    balance_drift: Decimal
    discrepancies: List[str]

class StateReconciliation:
    """Reconcile state on failover to prevent duplicate orders"""

    def __init__(self, exchange_connector, database, cache):
        self.exchange = exchange_connector
        self.db = database
        self.cache = cache

    async def reconcile_on_startup(self) -> ReconciliationReport:
        """
        Full state reconciliation when becoming active leader
        CRITICAL: Run this BEFORE starting trading engine
        """
        logger.info("Starting state reconciliation...")

        # Step 1: Fetch ground truth from exchanges
        exchange_orders = await self._fetch_all_open_orders()
        exchange_positions = await self._fetch_all_positions()
        exchange_balances = await self._fetch_all_balances()

        # Step 2: Compare with local state
        db_orders = await self.db.get_open_orders()
        db_positions = await self.db.get_positions()
        db_balances = await self.db.get_balances()

        # Step 3: Reconcile orders
        orders_cancelled = await self._reconcile_orders(exchange_orders, db_orders)

        # Step 4: Reconcile positions
        positions_synced = await self._reconcile_positions(exchange_positions, db_positions)

        # Step 5: Reconcile balances
        balance_drift = await self._reconcile_balances(exchange_balances, db_balances)

        # Step 6: Check for discrepancies
        discrepancies = await self._detect_discrepancies()

        report = ReconciliationReport(
            open_orders_found=len(exchange_orders),
            orders_cancelled=orders_cancelled,
            positions_synced=positions_synced,
            balance_drift=balance_drift,
            discrepancies=discrepancies
        )

        logger.info(f"State reconciliation complete: {report}")

        return report

    async def _reconcile_orders(
        self,
        exchange_orders: List[Dict],
        db_orders: List[Dict]
    ) -> int:
        """
        Reconcile orders between exchange and database
        Cancel any orphaned orders
        """
        cancelled_count = 0

        # Build lookup of DB orders
        db_order_ids = {o['order_id'] for o in db_orders}

        # Find orders on exchange not in DB (orphans)
        for exchange_order in exchange_orders:
            order_id = exchange_order['id']

            if order_id not in db_order_ids:
                # Orphaned order - cancel it
                logger.warning(f"Found orphaned order {order_id} - cancelling")
                try:
                    await self.exchange.cancel_order(order_id)
                    cancelled_count += 1
                except Exception as e:
                    logger.error(f"Failed to cancel orphaned order {order_id}: {e}")

        # Update DB orders with exchange status
        for db_order in db_orders:
            exchange_status = next(
                (o for o in exchange_orders if o['id'] == db_order['order_id']),
                None
            )

            if exchange_status:
                # Update status if different
                if exchange_status['status'] != db_order['status']:
                    await self.db.update_order_status(
                        db_order['order_id'],
                        exchange_status['status']
                    )
            else:
                # Order not on exchange - mark as cancelled
                await self.db.update_order_status(
                    db_order['order_id'],
                    'cancelled'
                )

        return cancelled_count
```

## Health Check and Monitoring

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional

@dataclass
class HealthStatus:
    healthy: bool
    timestamp: datetime
    checks: Dict[str, bool]
    latency_ms: Optional[float]
    message: str

class HealthChecker:
    """Comprehensive health checking for active/passive instances"""

    def __init__(self, exchange, database, redis_client):
        self.exchange = exchange
        self.db = database
        self.redis = redis_client
        self.last_trade_time = None
        self.health_history = []

    async def check_health(self) -> HealthStatus:
        """Run all health checks"""
        start_time = time.time()

        checks = {
            'exchange_connection': await self._check_exchange_connection(),
            'database_connection': await self._check_database_connection(),
            'redis_connection': await self._check_redis_connection(),
            'data_freshness': await self._check_data_freshness(),
            'order_execution': await self._check_order_execution(),
            'websocket_alive': await self._check_websocket_connection(),
        }

        latency_ms = (time.time() - start_time) * 1000
        all_healthy = all(checks.values())

        status = HealthStatus(
            healthy=all_healthy,
            timestamp=datetime.utcnow(),
            checks=checks,
            latency_ms=latency_ms,
            message="All systems operational" if all_healthy else "System degraded"
        )

        self.health_history.append(status)

        # Keep only last 100 health checks
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]

        return status

    async def _check_exchange_connection(self) -> bool:
        """Check if exchange API is responsive"""
        try:
            # Simple ping to exchange
            await asyncio.wait_for(
                self.exchange.fetch_time(),
                timeout=5.0
            )
            return True
        except asyncio.TimeoutError:
            logger.error("Exchange connection check timed out")
            return False
        except Exception as e:
            logger.error(f"Exchange connection check failed: {e}")
            return False

    async def _check_data_freshness(self) -> bool:
        """Check if market data is fresh (< 5 seconds old)"""
        try:
            last_update = await self.redis.get('last_ticker_update')
            if not last_update:
                return False

            last_update_time = datetime.fromisoformat(last_update.decode())
            age = datetime.utcnow() - last_update_time

            return age < timedelta(seconds=5)

        except Exception as e:
            logger.error(f"Data freshness check failed: {e}")
            return False
```

## Graceful Shutdown Pattern

```python
import signal
import asyncio

class GracefulShutdown:
    """Handle graceful shutdown on SIGTERM/SIGINT"""

    def __init__(self, trading_engine):
        self.trading_engine = trading_engine
        self.shutdown_event = asyncio.Event()
        self.shutdown_complete = asyncio.Event()

        # Register signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum} - initiating graceful shutdown")
        self.shutdown_event.set()

    async def shutdown_sequence(self):
        """Execute graceful shutdown sequence"""
        logger.info("Starting graceful shutdown sequence...")

        # Step 1: Stop accepting new orders (30 seconds timeout)
        logger.info("Step 1/5: Stopping new order acceptance")
        await asyncio.wait_for(
            self.trading_engine.stop_new_orders(),
            timeout=30
        )

        # Step 2: Cancel all open orders (60 seconds timeout)
        logger.info("Step 2/5: Cancelling all open orders")
        await asyncio.wait_for(
            self.trading_engine.cancel_all_orders(),
            timeout=60
        )

        # Step 3: Close all positions (optional, 120 seconds timeout)
        logger.info("Step 3/5: Closing positions (if configured)")
        if self.trading_engine.config.get('close_positions_on_shutdown'):
            await asyncio.wait_for(
                self.trading_engine.close_all_positions(),
                timeout=120
            )

        # Step 4: Flush all pending database writes (30 seconds timeout)
        logger.info("Step 4/5: Flushing pending writes")
        await asyncio.wait_for(
            self.trading_engine.flush_pending_writes(),
            timeout=30
        )

        # Step 5: Close connections
        logger.info("Step 5/5: Closing connections")
        await self.trading_engine.close_connections()

        logger.info("Graceful shutdown complete")
        self.shutdown_complete.set()
```

## Failover Time Monitoring

```python
class FailoverMonitor:
    """Monitor and alert on failover times"""

    def __init__(self, target_failover_seconds: int = 30):
        self.target_failover_time = target_failover_seconds
        self.failover_history = []

    def record_failover(
        self,
        old_leader: str,
        new_leader: str,
        failover_time_seconds: float
    ):
        """Record failover event"""
        event = {
            'timestamp': datetime.utcnow(),
            'old_leader': old_leader,
            'new_leader': new_leader,
            'failover_time': failover_time_seconds,
            'met_target': failover_time_seconds <= self.target_failover_time
        }

        self.failover_history.append(event)

        # Alert if target not met
        if not event['met_target']:
            logger.critical(
                f"Failover took {failover_time_seconds:.1f}s - "
                f"exceeds target of {self.target_failover_time}s"
            )

        # Calculate statistics
        if len(self.failover_history) >= 5:
            recent_times = [e['failover_time'] for e in self.failover_history[-5:]]
            avg_time = sum(recent_times) / len(recent_times)

            logger.info(
                f"Failover stats - Current: {failover_time_seconds:.1f}s, "
                f"Avg (last 5): {avg_time:.1f}s, "
                f"Target: {self.target_failover_time}s"
            )
```

---
**Critical for production**: Always implement leader election, state reconciliation, and graceful shutdown for 99.99% uptime.
