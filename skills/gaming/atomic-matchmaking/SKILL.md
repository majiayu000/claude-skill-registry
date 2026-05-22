---
name: atomic-matchmaking
description: Two-phase commit matchmaking that verifies both player connections before creating a match. Handles disconnections gracefully with automatic re-queue of healthy players.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: api
  time: 6h
  source: drift-masterguide
---

# Atomic Matchmaking with Two-Phase Commit

Two-phase commit semantics for match creation that handles player disconnections gracefully.

## When to Use This Skill

- Building real-time multiplayer matchmaking
- Need to handle player disconnections during match creation
- Want to avoid orphaned lobbies and stuck players
- Require reliable match notifications

## Core Concepts

Matching two players is deceptively hard. Either player can disconnect between being matched and joining. The solution uses two-phase commit:

1. **Phase 1**: Verify both connections are healthy via ping/pong
2. **Phase 2**: Create lobby, send notifications, confirm delivery
3. **Rollback**: On any failure, clean up lobby and re-queue the healthy player

## Implementation

### Python

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Tuple
from enum import Enum
import asyncio


class MatchStatus(str, Enum):
    SUCCESS = "success"
    PLAYER1_DISCONNECTED = "player1_disconnected"
    PLAYER2_DISCONNECTED = "player2_disconnected"
    BOTH_DISCONNECTED = "both_disconnected"
    NOTIFICATION_FAILED = "notification_failed"


@dataclass
class MatchTicket:
    player_id: str
    category: str
    queued_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MatchResult:
    status: MatchStatus
    lobby_id: Optional[str] = None
    lobby_code: Optional[str] = None
    player1_healthy: bool = True
    player2_healthy: bool = True
    requeued_player: Optional[str] = None


class ConnectionHealthChecker:
    """Verifies player connections are healthy before matching."""
    
    PING_TIMEOUT = 2.0
    MAX_ACCEPTABLE_LATENCY = 500  # ms
    
    def __init__(self, connection_manager):
        self._manager = connection_manager
    
    async def check_health(self, player_id: str) -> Tuple[bool, Optional[float]]:
        if not self._manager.is_user_connected(player_id):
            return False, None
        
        success, latency = await self._manager.ping_user(
            player_id, timeout=self.PING_TIMEOUT
        )
        
        if not success:
            return False, None
        
        if latency and latency > self.MAX_ACCEPTABLE_LATENCY:
            return False, latency
        
        return True, latency
    
    async def verify_both_healthy(
        self, player1_id: str, player2_id: str
    ) -> Tuple[bool, bool, bool]:
        results = await asyncio.gather(
            self.check_health(player1_id),
            self.check_health(player2_id),
        )
        
        health1, _ = results[0]
        health2, _ = results[1]
        
        return (health1 and health2), health1, health2


class AtomicMatchCreator:
    """Creates matches with two-phase commit semantics."""
    
    NOTIFICATION_TIMEOUT = 2.0
    NOTIFICATION_RETRIES = 3
    
    def __init__(
        self,
        health_checker: ConnectionHealthChecker,
        lobby_service,
        queue_manager,
        notification_service,
    ):
        self._health_checker = health_checker
        self._lobby_service = lobby_service
        self._queue_manager = queue_manager
        self._notifications = notification_service
    
    async def create_match(
        self, player1: MatchTicket, player2: MatchTicket
    ) -> MatchResult:
        # Phase 1: Health Check
        both_healthy, health1, health2 = await self._health_checker.verify_both_healthy(
            player1.player_id, player2.player_id
        )
        
        if not both_healthy:
            return await self._handle_health_failure(player1, player2, health1, health2)
        
        # Phase 2: Create Lobby & Notify
        lobby = None
        try:
            lobby = await self._lobby_service.create_lobby(
                host_id=player1.player_id,
                category=player1.category,
            )
            
            await self._lobby_service.add_player(lobby["id"], player2.player_id)
            
            # Notify both players in parallel
            notify_results = await asyncio.gather(
                self._notify_with_retry(player1.player_id, lobby["code"], player2.player_id),
                self._notify_with_retry(player2.player_id, lobby["code"], player1.player_id),
                return_exceptions=True,
            )
            
            if not all(r is True for r in notify_results):
                raise Exception("Notification failed")
            
            return MatchResult(
                status=MatchStatus.SUCCESS,
                lobby_id=lobby["id"],
                lobby_code=lobby["code"],
            )
            
        except Exception as e:
            # Rollback: delete lobby if created
            if lobby:
                await self._lobby_service.delete_lobby(lobby["id"])
            
            return await self._handle_phase2_failure(player1, player2, str(e))
    
    async def _handle_health_failure(
        self, player1: MatchTicket, player2: MatchTicket,
        health1: bool, health2: bool
    ) -> MatchResult:
        if not health1 and not health2:
            return MatchResult(
                status=MatchStatus.BOTH_DISCONNECTED,
                player1_healthy=False,
                player2_healthy=False,
            )
        
        # Re-queue the healthy player with priority
        if health1 and not health2:
            await self._queue_manager.requeue_player(player1, priority=True)
            return MatchResult(
                status=MatchStatus.PLAYER2_DISCONNECTED,
                player1_healthy=True,
                player2_healthy=False,
                requeued_player=player1.player_id,
            )
        
        if health2 and not health1:
            await self._queue_manager.requeue_player(player2, priority=True)
            return MatchResult(
                status=MatchStatus.PLAYER1_DISCONNECTED,
                player1_healthy=False,
                player2_healthy=True,
                requeued_player=player2.player_id,
            )
        
        return MatchResult(status=MatchStatus.BOTH_DISCONNECTED)
    
    async def _notify_with_retry(
        self, player_id: str, lobby_code: str, opponent_id: str
    ) -> bool:
        for attempt in range(self.NOTIFICATION_RETRIES):
            try:
                success = await asyncio.wait_for(
                    self._notifications.notify_match_found(player_id, lobby_code, opponent_id),
                    timeout=self.NOTIFICATION_TIMEOUT,
                )
                if success:
                    return True
            except asyncio.TimeoutError:
                pass
            
            if attempt < self.NOTIFICATION_RETRIES - 1:
                await asyncio.sleep(0.1)
        
        return False
```

### Queue Manager with Priority Re-queue

```python
from collections import deque
from typing import Dict, Optional, Set
import asyncio


class MatchmakingQueue:
    """FIFO queue with priority re-queue support."""
    
    def __init__(self):
        self._queues: Dict[str, deque] = {}
        self._player_tickets: Dict[str, MatchTicket] = {}
        self._lock = asyncio.Lock()
    
    async def enqueue(self, ticket: MatchTicket, priority: bool = False) -> bool:
        async with self._lock:
            if ticket.player_id in self._player_tickets:
                return False
            
            if ticket.category not in self._queues:
                self._queues[ticket.category] = deque()
            
            queue = self._queues[ticket.category]
            
            if priority:
                queue.appendleft(ticket)
            else:
                queue.append(ticket)
            
            self._player_tickets[ticket.player_id] = ticket
            return True
    
    async def dequeue_pair(self, category: str) -> Optional[tuple]:
        async with self._lock:
            queue = self._queues.get(category)
            if not queue or len(queue) < 2:
                return None
            
            ticket1 = queue.popleft()
            ticket2 = queue.popleft()
            
            self._player_tickets.pop(ticket1.player_id, None)
            self._player_tickets.pop(ticket2.player_id, None)
            
            return ticket1, ticket2
    
    async def requeue_player(self, ticket: MatchTicket, priority: bool = True) -> None:
        await self.remove_player(ticket.player_id)
        await self.enqueue(ticket, priority=priority)
```

## Usage Examples

### Match Creation Flow

```python
health_checker = ConnectionHealthChecker(connection_manager)
match_creator = AtomicMatchCreator(
    health_checker, lobby_service, queue_manager, notification_service
)

# When two players are matched
result = await match_creator.create_match(ticket1, ticket2)

if result.status == MatchStatus.SUCCESS:
    print(f"Match created: {result.lobby_code}")
elif result.requeued_player:
    print(f"Re-queued {result.requeued_player}")
```

## Best Practices

1. Always verify connections before creating lobby - prevents orphaned lobbies
2. Re-queue healthy players with priority - they've already waited
3. Use notification retries - network can be flaky
4. Rollback on any failure - clean up partial state
5. Log correlation IDs - essential for debugging match failures

## Common Mistakes

- Creating lobby before verifying connections (orphaned lobbies)
- Not re-queuing healthy players (stuck in limbo)
- No notification retries (lost matches on network blips)
- Missing rollback logic (resource leaks)
- Not using priority re-queue (unfair to healthy players)

## Related Patterns

- websocket-management - Connection health verification
- distributed-lock - Prevent race conditions in matching
- graceful-shutdown - Drain queue on shutdown
