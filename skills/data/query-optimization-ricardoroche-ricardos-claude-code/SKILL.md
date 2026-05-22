---
name: query-optimization
description: Automatically applies when optimizing database queries. Ensures EXPLAIN analysis, proper indexing, N+1 prevention, query performance monitoring, and efficient SQL patterns.
category: python
---

# Query Optimization Patterns

When optimizing database queries, follow these patterns for efficient, scalable data access.

**Trigger Keywords**: query optimization, EXPLAIN, index, N+1, query performance, slow query, database performance, SELECT, JOIN, query plan

**Agent Integration**: Used by `backend-architect`, `database-engineer`, `performance-engineer`

## ✅ Correct Pattern: EXPLAIN Analysis

```python
from sqlalchemy import create_engine, text
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class QueryAnalyzer:
    """Analyze query performance with EXPLAIN."""

    def __init__(self, engine):
        self.engine = engine

    def explain(self, query: str, params: Dict = None) -> List[Dict]:
        """
        Run EXPLAIN on query.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            EXPLAIN output
        """
        with self.engine.connect() as conn:
            explain_query = f"EXPLAIN ANALYZE {query}"
            result = conn.execute(text(explain_query), params or {})
            return [dict(row._mapping) for row in result]

    def find_slow_queries(
        self,
        threshold_ms: float = 1000.0
    ) -> List[Dict]:
        """
        Find queries slower than threshold.

        Args:
            threshold_ms: Threshold in milliseconds

        Returns:
            List of slow queries
        """
        # PostgreSQL pg_stat_statements
        query = text("""
            SELECT
                query,
                calls,
                total_exec_time / 1000.0 as total_seconds,
                mean_exec_time as avg_ms,
                max_exec_time as max_ms
            FROM pg_stat_statements
            WHERE mean_exec_time > :threshold
            ORDER BY total_exec_time DESC
            LIMIT 50
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"threshold": threshold_ms})
            return [dict(row._mapping) for row in result]


# Usage
analyzer = QueryAnalyzer(engine)

# Analyze specific query
explain_output = analyzer.explain(
    "SELECT * FROM users WHERE email = :email",
    {"email": "user@example.com"}
)

for row in explain_output:
    logger.info(f"Query plan: {row}")

# Find slow queries
slow_queries = analyzer.find_slow_queries(threshold_ms=500)
```

## Index Creation

```python
from sqlalchemy import Index, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """User model with proper indexes."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)

    # Single column indexes
    __table_args__ = (
        Index('ix_users_email', 'email', unique=True),  # Unique constraint
        Index('ix_users_username', 'username'),
        Index('ix_users_status', 'status'),

        # Composite indexes (order matters!)
        Index('ix_users_status_created', 'status', 'created_at'),

        # Partial index (PostgreSQL)
        Index(
            'ix_users_active_email',
            'email',
            postgresql_where=(status == 'active')
        ),

        # Expression index
        Index(
            'ix_users_email_lower',
            func.lower(email),
            postgresql_using='btree'
        ),
    )


# When to create indexes:
# ✅ Columns in WHERE clauses
# ✅ Columns in JOIN conditions
# ✅ Columns in ORDER BY
# ✅ Foreign key columns
# ✅ Columns in GROUP BY
```

## N+1 Query Prevention

```python
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload, relationship


class Order(Base):
    """Order model."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total = Column(Numeric)

    # Relationship
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


# ❌ N+1 Query Problem
def get_orders_with_users_bad(session: Session) -> List[Order]:
    """
    BAD: Causes N+1 queries.

    1 query for orders + N queries for users.
    """
    orders = session.execute(select(Order)).scalars().all()

    for order in orders:
        print(f"Order {order.id} by {order.user.email}")  # N queries!

    return orders


# ✅ Solution 1: Eager Loading with joinedload
def get_orders_with_users_joined(session: Session) -> List[Order]:
    """
    GOOD: Single query with JOIN.

    Use for one-to-one or many-to-one relationships.
    """
    stmt = select(Order).options(
        joinedload(Order.user)
    )

    orders = session.execute(stmt).unique().scalars().all()

    for order in orders:
        print(f"Order {order.id} by {order.user.email}")  # No extra queries!

    return orders


# ✅ Solution 2: Eager Loading with selectinload
def get_orders_with_items(session: Session) -> List[Order]:
    """
    GOOD: Separate query with WHERE IN.

    Use for one-to-many or many-to-many relationships.
    """
    stmt = select(Order).options(
        selectinload(Order.items)
    )

    orders = session.execute(stmt).scalars().all()

    for order in orders:
        print(f"Order {order.id} has {len(order.items)} items")  # No N+1!

    return orders


# ✅ Solution 3: Load multiple relationships
def get_orders_complete(session: Session) -> List[Order]:
    """Load orders with users and items."""
    stmt = select(Order).options(
        joinedload(Order.user),      # JOIN for user
        selectinload(Order.items)    # Separate query for items
    )

    return session.execute(stmt).unique().scalars().all()
```

## Batch Loading

```python
from typing import List, Dict


async def get_users_by_ids_batch(
    session: Session,
    user_ids: List[int]
) -> Dict[int, User]:
    """
    Load multiple users in single query.

    Args:
        session: Database session
        user_ids: List of user IDs

    Returns:
        Dict mapping user_id to User
    """
    if not user_ids:
        return {}

    # Single query with WHERE IN
    stmt = select(User).where(User.id.in_(user_ids))
    users = session.execute(stmt).scalars().all()

    # Return as dict for O(1) lookup
    return {user.id: user for user in users}


# Usage with DataLoader pattern
class UserDataLoader:
    """Batch load users to prevent N+1."""

    def __init__(self, session: Session):
        self.session = session
        self._batch: List[int] = []
        self._cache: Dict[int, User] = {}

    async def load(self, user_id: int) -> User:
        """
        Load user by ID with batching.

        Collects IDs and loads in batch.
        """
        if user_id in self._cache:
            return self._cache[user_id]

        self._batch.append(user_id)
        return await self._load_batch()

    async def _load_batch(self):
        """Execute batch load."""
        if not self._batch:
            return None

        users = await get_users_by_ids_batch(self.session, self._batch)
        self._cache.update(users)
        self._batch.clear()

        return users
```

## Query Optimization Patterns

```python
from sqlalchemy import func, and_, or_


# ✅ Use specific columns, not SELECT *
def get_user_emails_good(session: Session) -> List[str]:
    """Select only needed columns."""
    stmt = select(User.email)
    return session.execute(stmt).scalars().all()


# ✅ Use pagination for large result sets
def get_users_paginated(
    session: Session,
    page: int = 1,
    page_size: int = 50
) -> List[User]:
    """Paginate results."""
    offset = (page - 1) * page_size

    stmt = (
        select(User)
        .order_by(User.id)
        .limit(page_size)
        .offset(offset)
    )

    return session.execute(stmt).scalars().all()


# ✅ Use EXISTS for checking existence
def user_has_orders_exists(session: Session, user_id: int) -> bool:
    """Check if user has orders efficiently."""
    stmt = select(
        exists(select(Order.id).where(Order.user_id == user_id))
    )
    return session.execute(stmt).scalar()


# ✅ Use COUNT efficiently
def get_active_user_count(session: Session) -> int:
    """Count without loading rows."""
    stmt = select(func.count()).select_from(User).where(User.status == 'active')
    return session.execute(stmt).scalar()


# ✅ Use bulk operations
def bulk_update_status(
    session: Session,
    user_ids: List[int],
    new_status: str
):
    """Bulk update in single query."""
    stmt = (
        update(User)
        .where(User.id.in_(user_ids))
        .values(status=new_status)
    )
    session.execute(stmt)
    session.commit()


# ✅ Use window functions for rankings
def get_top_users_by_orders(session: Session) -> List[Dict]:
    """Get users ranked by order count."""
    stmt = text("""
        SELECT
            u.id,
            u.email,
            COUNT(o.id) as order_count,
            RANK() OVER (ORDER BY COUNT(o.id) DESC) as rank
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        GROUP BY u.id, u.email
        ORDER BY order_count DESC
        LIMIT 100
    """)

    with session.connection() as conn:
        result = conn.execute(stmt)
        return [dict(row._mapping) for row in result]
```

## Query Performance Monitoring

```python
import time
from functools import wraps
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def monitor_query_performance(threshold_ms: float = 100.0):
    """
    Decorator to monitor query performance.

    Args:
        threshold_ms: Log warning if query exceeds threshold
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()

            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start) * 1000

                if duration_ms > threshold_ms:
                    logger.warning(
                        f"Slow query detected",
                        extra={
                            "function": func.__name__,
                            "duration_ms": duration_ms,
                            "threshold_ms": threshold_ms
                        }
                    )
                else:
                    logger.debug(
                        f"Query completed",
                        extra={
                            "function": func.__name__,
                            "duration_ms": duration_ms
                        }
                    )

                return result

            except Exception as e:
                duration_ms = (time.time() - start) * 1000
                logger.error(
                    f"Query failed",
                    extra={
                        "function": func.__name__,
                        "duration_ms": duration_ms,
                        "error": str(e)
                    }
                )
                raise

        return wrapper
    return decorator


# Usage
@monitor_query_performance(threshold_ms=500.0)
async def get_user_orders(session: Session, user_id: int) -> List[Order]:
    """Get user orders with performance monitoring."""
    stmt = select(Order).where(Order.user_id == user_id)
    return session.execute(stmt).scalars().all()
```

## ❌ Anti-Patterns

```python
# ❌ SELECT *
stmt = select(User)  # Loads all columns!

# ✅ Better: Select specific columns
stmt = select(User.id, User.email)


# ❌ N+1 queries
orders = session.query(Order).all()
for order in orders:
    print(order.user.email)  # N queries!

# ✅ Better: Eager load
orders = session.query(Order).options(joinedload(Order.user)).all()


# ❌ No pagination
users = session.query(User).all()  # Could be millions!

# ✅ Better: Paginate
users = session.query(User).limit(100).offset(0).all()


# ❌ Loading full objects for COUNT
count = len(session.query(User).all())  # Loads all rows!

# ✅ Better: Use COUNT
count = session.query(func.count(User.id)).scalar()


# ❌ No indexes on WHERE columns
# Query: SELECT * FROM users WHERE email = ?
# No index on email column!

# ✅ Better: Create index
Index('ix_users_email', 'email')


# ❌ Using OR instead of IN
stmt = select(User).where(
    or_(User.id == 1, User.id == 2, User.id == 3)
)

# ✅ Better: Use IN
stmt = select(User).where(User.id.in_([1, 2, 3]))
```

## Best Practices Checklist

- ✅ Run EXPLAIN on complex queries
- ✅ Create indexes on foreign keys
- ✅ Create indexes on WHERE/JOIN columns
- ✅ Use eager loading to prevent N+1
- ✅ Select only needed columns
- ✅ Paginate large result sets
- ✅ Use EXISTS for existence checks
- ✅ Use COUNT without loading rows
- ✅ Use bulk operations for updates
- ✅ Monitor slow queries
- ✅ Use connection pooling
- ✅ Cache frequent queries

## Auto-Apply

When writing database queries:
1. Use EXPLAIN to analyze query plans
2. Create indexes on filtered/joined columns
3. Use joinedload/selectinload to prevent N+1
4. Select specific columns, not SELECT *
5. Implement pagination for large results
6. Monitor query performance
7. Use bulk operations when possible

## Related Skills

- `database-migrations` - For index creation
- `type-safety` - For type hints
- `monitoring-alerting` - For query monitoring
- `performance-profiling` - For optimization
- `async-await-checker` - For async queries
