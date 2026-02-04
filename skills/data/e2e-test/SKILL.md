---
name: e2e-test
description: Run E2E test scenarios against running services. Use for happy path testing, unhappy flows, debugging, or when user says "otestuj", "proved test", "zkus flow".
allowed-tools: Bash, Read, Glob, Grep, WebFetch, AskUserQuestion
---

# E2E Test Runner

Execute end-to-end test scenarios against running microservices with automatic debugging and reporting.

## Usage

```
/e2e-test                    # Interactive - asks what to test
/e2e-test happy              # Happy path: create order flow
/e2e-test unhappy            # Unhappy path: out of stock, invalid data
/e2e-test cancel             # Cancel order flow
/e2e-test debug              # Just show service status and debug info
/e2e-test trace <corr-id>    # Trace request across services by CorrelationId
/e2e-test <custom scenario>  # Describe what you want to test
```

## Input

- `$ARGUMENTS` - Test scenario to run or empty for interactive mode

## Architecture Reference

### Services

| Service | Purpose | API Base | gRPC |
|---------|---------|----------|------|
| Gateway | Reverse proxy (YARP) | `/api/*` | - |
| Product API | Product catalog & stock | `/api/products` | `ProductService` |
| Order API | Order management | `/api/orders` | - |
| Notification | Email notifications | - (consumer only) | - |
| Analytics | Order tracking | - (consumer only) | - |

### Databases (PostgreSQL)

| Database | Tables | Purpose |
|----------|--------|---------|
| `productdb` | `Product`, `Stock`, `StockReservation`, `OutboxMessage`, `InboxState` | Product catalog & stock |
| `orderdb` | `Order`, `OrderItem`, `OutboxMessage`, `OutboxState`, `InboxState` | Orders + outbox |
| `notificationdb` | `ProcessedMessages` | Inbox pattern (note: plural "Messages") |

### Stock Behavior (IMPORTANT)

**Stock quantity is NOT decreased** when orders are created. Instead:
- A `StockReservation` record is created with `Status=0` (Active)
- When order is cancelled, reservation changes to `Status=1` (Released)
- The `Stock.Quantity` field represents total inventory, not available inventory

### Message Flow

```
Order API → [gRPC] → Product API (ReserveStock)
    ↓
OrderConfirmedEvent → [RabbitMQ] → Notification + Analytics
```

## CRITICAL: Gateway-First Rule

**ALL API calls in E2E tests MUST go through the Gateway.** This is non-negotiable.

```
✓ CORRECT:  curl http://localhost:$GATEWAY_PORT/api/products
✗ WRONG:    curl http://localhost:$PRODUCT_PORT/api/products
```

**Why:**
- Gateway is the only entry point in production
- E2E tests must simulate real-world usage
- Tests the full stack: YARP proxy, correlation ID propagation, routing
- Catches Gateway-specific issues (routing, headers, timeouts)

**When direct service access is allowed:**
- `debug` scenario only - to compare Gateway vs direct response
- Troubleshooting when Gateway returns error but you need to verify backend works
- Never in `happy`, `unhappy`, `cancel` scenarios

## Process

### Phase 0: Service Mode Selection

**ALWAYS start here.** Use `AskUserQuestion` to ask the user how they want to manage services:

**Question:** "How should I manage services for this E2E test?"

**Options:**
1. **Manual (Recommended)** - "I'll run the services myself or they're already running"
   - User controls AppHost in their own terminal
   - Skill only discovers existing services
   - User responsible for starting/stopping

2. **Automatic** - "Start AppHost as a background process"
   - Skill starts `dotnet run --project src/AppHost` in background using `run_in_background: true`
   - Skill waits for services to be healthy
   - Skill offers to stop AppHost at the end using `TaskStop`

**Based on selection:**

- **Manual mode:** Proceed to Phase 1 (Environment Discovery)
- **Automatic mode:**
  1. Start AppHost in background:
     ```bash
     dotnet run --project src/AppHost
     ```
     Use `run_in_background: true` parameter
  2. Wait 15-30 seconds for services to start
  3. Run discovery to verify services are healthy
  4. If services not healthy after 60s, show logs and ask user what to do
  5. **Remember the task_id** - you'll need it for cleanup at the end

### Phase 1: Environment Discovery

Run `./tools/e2e-test/discover.sh` to get:

1. **Running services** - ports dynamically assigned by Aspire
2. **Database connection** - PostgreSQL container and credentials
3. **Message broker** - RabbitMQ management URL
4. **Health status** - all service health endpoints

If services are not running:
- **Manual mode:** Inform user: `Services not detected. Start with: dotnet run --project src/AppHost`
- **Automatic mode:** Check AppHost logs for errors, report to user

### Phase 2: Scenario Planning

Based on `$ARGUMENTS`, plan the test scenario:

#### `happy` - Order Happy Path
All API calls via Gateway (`$GATEWAY_PORT`):
1. GET `/api/products` via Gateway → pick one with stock > 0
2. POST `/api/orders` via Gateway → create order (see API Contract below)
3. Verify: Order status = Confirmed (via Gateway GET `/api/orders/{id}`)
4. Verify: StockReservation created (Status=0) - DB query
5. Verify: Notification inbox has record (`ProcessedMessages` table) - DB query
6. Check logs for complete flow

**API Contract - Create Order:**
```json
{
  "customerId": "guid",
  "customerEmail": "email@example.com",
  "items": [{
    "productId": "guid",
    "quantity": 2
  }]
}
```

#### `unhappy` - Failure Scenarios
All API calls via Gateway (`$GATEWAY_PORT`):
1. **Out of stock**: POST `/api/orders` via Gateway with quantity > available
2. **Invalid product**: POST `/api/orders` via Gateway with non-existent productId
3. **Invalid data**: POST `/api/orders` via Gateway with missing required fields
4. Verify: Appropriate error responses from Gateway
5. Verify: No side effects (stock unchanged, no events) - DB queries

#### `cancel` - Order Cancellation
All API calls via Gateway (`$GATEWAY_PORT`):
1. Create order first via Gateway (happy path steps 1-2)
2. POST `/api/orders/{orderId}/cancel` via Gateway (see API Contract below)
3. Verify: Order status = Cancelled (via Gateway GET `/api/orders/{id}`)
4. Verify: StockReservation status changed to 1 (Released) - DB query
5. Verify: Cancellation notification processed (`OrderCancelledConsumer`) - DB query

**API Contract - Cancel Order:**
```bash
POST /api/orders/{orderId}/cancel
Content-Type: application/json

{"reason": "Customer requested cancellation"}  # Body is REQUIRED!
```

#### `debug` - Service Debug Info
**This is the only scenario where direct service access is allowed** (for comparison/troubleshooting).

1. Show all service ports and URLs (Gateway + backend services)
2. Show database connection info
3. Show recent logs (last 20 lines per service)
4. Show message queue status (RabbitMQ)
5. Show gRPC connectivity status
6. Check service discovery configuration
7. (Optional) Compare Gateway response vs direct service response

#### `trace <correlation-id>` - Distributed Request Tracing
1. Run `./tools/e2e-test/trace-correlation.sh <correlation-id>`
2. Display chronologically sorted logs from all services
3. Highlight errors and warnings
4. Show service flow visualization

**Options:**
- `--all-logs` - Search all log files, not just latest
- `--json` - Output as JSON for further processing

**Example:**
```bash
/e2e-test trace 228617a4-175a-4384-a8e2-ade916a78c3f
```

**Output shows:**
- Service-colored log entries (gateway=cyan, order=green, product=yellow, etc.)
- Chronological order across all services
- Error highlighting in red, warnings in yellow

### Phase 3: Execution

Execute scenario step by step. **After each step:**

1. Log the action taken
2. Verify expected outcome
3. If failure detected → **STOP and consult user**

**REMEMBER: All API calls go through Gateway!** (see Gateway-First Rule above)

Use these helpers:

```bash
# Service discovery - saves ports to .env file
./tools/e2e-test/discover.sh
source ./tools/e2e-test/.env

# API calls - ALWAYS use Gateway port!
curl -s "http://localhost:$GATEWAY_PORT/api/products" | jq '.'
curl -s "http://localhost:$GATEWAY_PORT/api/orders" | jq '.'
curl -s -X POST "http://localhost:$GATEWAY_PORT/api/orders" -H "Content-Type: application/json" -d '...'

# WRONG - never call services directly in E2E tests:
# curl -s "http://localhost:$PRODUCT_PORT/api/products"  # ✗ DON'T DO THIS
# curl -s "http://localhost:$ORDER_PORT/api/orders"      # ✗ DON'T DO THIS

# Database queries - get password first, then query
PG_PASS=$(docker exec <container> printenv POSTGRES_PASSWORD)
docker exec -e PGPASSWORD="$PG_PASS" <container> psql -U postgres -d <db> -c '<SQL>'

# Example:
PG_PASS=$(docker exec postgres-4cdf07e3 printenv POSTGRES_PASSWORD)
docker exec -e PGPASSWORD="$PG_PASS" postgres-4cdf07e3 psql -U postgres -d productdb -c 'SELECT * FROM "StockReservation";'

# Log inspection
./tools/e2e-test/logs.sh <service> [lines]

# Trace correlation ID
./tools/e2e-test/trace-correlation.sh <correlation-id>
```

### Finding Service Ports Manually

If `discover.sh` fails to find services, use this:

```bash
# List all dotnet processes with ports
lsof -i -P -n | grep -E "EShop\.(Ord|Pro|Gat)" | grep LISTEN

# Typical output:
# EShop.Ord 45956  ... TCP 127.0.0.1:49814 (LISTEN)  <- Order API HTTP
# EShop.Pro 45955  ... TCP 127.0.0.1:49815 (LISTEN)  <- Product API HTTP
# EShop.Gat 45954  ... TCP 127.0.0.1:49818 (LISTEN)  <- Gateway HTTP
```

### Phase 4: Reporting

Generate structured report:

```
═══════════════════════════════════════════════════════
  E2E TEST REPORT: <scenario name>
═══════════════════════════════════════════════════════

ENVIRONMENT
  Gateway:      http://localhost:XXXXX ✓  ← All API calls go here
  PostgreSQL:   localhost:XXXXX ✓
  RabbitMQ:     localhost:XXXXX ✓

  Backend services (for reference only):
    Order API:    http://localhost:XXXXX ✓
    Product API:  http://localhost:XXXXX ✓

SCENARIO: <description>

STEPS EXECUTED
  [✓] Step 1: Get products
      → Found 10 products, selected "Cable Management Kit" (stock: 100)

  [✓] Step 2: Create order
      → POST /api/orders → 201 Created
      → OrderId: abc-123-def

  [✓] Step 3: Verify order status
      → DB: Order.Status = 1 (Confirmed)

  [✗] Step 4: Verify stock decreased
      → Expected: 98, Actual: 100
      → FAILURE: Stock not reserved

LOGS (relevant entries)
  [Order.API 21:00:10] Creating order for customer X
  [Order.API 21:00:10] ERROR: gRPC call failed - No address resolver

DIAGNOSIS
  Problem: gRPC service discovery not configured
  Location: src/Common/EShop.ServiceClients/Extensions/ServiceCollectionExtensions.cs
  Fix: Add .AddServiceDiscovery() to gRPC client registration

RESULT: FAILED (Step 4)
═══════════════════════════════════════════════════════
```

## Error Handling

When an error blocks the scenario:

1. **STOP execution immediately**
2. **Gather diagnostic info:**
   - Recent logs from affected service
   - Database state
   - Error response details
3. **Present to user with options:**

```
⚠️  Test blocked by error at Step X

Error: <description>
Service: <service name>
Log excerpt:
  <relevant log lines>

Options:
1. Attempt to fix the issue (I'll suggest a fix)
2. Skip this step and continue
3. Abort test and show partial report
4. Debug mode - show all diagnostic info
```

Wait for user decision before proceeding.

## Key Validation Points

**Note:** All API calls in these validation points go through Gateway.

### Order Creation (Happy Path)

| Check | Query/Command | Expected |
|-------|---------------|----------|
| API Response | `POST $GATEWAY_PORT/api/orders` | 200, `status: "Confirmed"` |
| Get Order | `GET $GATEWAY_PORT/api/orders/{id}` | `status: "Confirmed"` |
| Order in DB | `SELECT * FROM "Order" WHERE "Id"='X'` | `Status = 1` (Confirmed) |
| Reservation created | `SELECT * FROM "StockReservation" WHERE "OrderId"='X'` | 1 row, `Status=0` |
| Stock unchanged | `SELECT "Quantity" FROM "Stock"` | Same as before (stock is NOT decreased) |
| Outbox processed | `SELECT * FROM "OutboxMessage"` | 0 pending (processed) |
| Notification inbox | `SELECT * FROM "ProcessedMessages"` | `OrderConfirmedConsumer` row |

### Order Cancellation

| Check | Query/Command | Expected |
|-------|---------------|----------|
| API Response | `POST $GATEWAY_PORT/api/orders/{id}/cancel` | 200, `status: "Cancelled"` |
| Get Order | `GET $GATEWAY_PORT/api/orders/{id}` | `status: "Cancelled"` |
| Order in DB | `SELECT * FROM "Order" WHERE "Id"='X'` | `Status = 3` (Cancelled) |
| Reservation released | `SELECT * FROM "StockReservation" WHERE "OrderId"='X'` | `Status=1` (Released) |
| Notification inbox | `SELECT * FROM "ProcessedMessages"` | `OrderCancelledConsumer` row |

### Stock Low Alert

| Check | Query/Command | Expected |
|-------|---------------|----------|
| Triggered when | Reservation makes available < threshold | `StockLowEvent` published |
| Notification inbox | `SELECT * FROM "ProcessedMessages"` | `StockLowConsumer` row |

### Log Patterns to Verify

| Service | Pattern | Meaning |
|---------|---------|---------|
| Order.API | `Creating order for customer` | Command received |
| Order.API | `Publishing OrderConfirmedEvent` | Event dispatched |
| Product.API | `ReserveStock request received` | gRPC call arrived |
| Product.API | `Stock reserved successfully` | Reservation complete |
| Notification | `Consuming OrderConfirmedEvent` | Event received |
| Notification | `Sending email to` | Email triggered |

## RabbitMQ Diagnostics

Use `./tools/e2e-test/rabbitmq.sh` for message broker debugging:

```bash
./tools/e2e-test/rabbitmq.sh status      # Overview
./tools/e2e-test/rabbitmq.sh queues      # Queue status with message counts
./tools/e2e-test/rabbitmq.sh connections # Active service connections
./tools/e2e-test/rabbitmq.sh consumers   # Consumer registrations
./tools/e2e-test/rabbitmq.sh messages    # Pending message analysis
```

### RabbitMQ Validation Points

| Check | What to look for | Issue if... |
|-------|------------------|-------------|
| **Messages Ready** | Should be 0 after processing | > 0 = stuck messages, consumer issue |
| **Messages Unacked** | Should be 0 or low | High = slow consumer or stuck processing |
| **Connections** | Order, Notification, Analytics | Missing = service not connected |
| **Consumers** | At least 2 per event type | 0 = no one listening |
| **Dead Letter** | Should be empty | Messages = repeated failures |

### Expected Queues (after first message)

```
order-confirmed     - OrderConfirmedEvent consumers
order-rejected      - OrderRejectedEvent consumers
order-cancelled     - OrderCancelledEvent consumers
stock-low           - StockLowEvent consumers
```

## gRPC Diagnostics

Use `./tools/e2e-test/grpc.sh` for inter-service communication debugging:

```bash
./tools/e2e-test/grpc.sh status      # Port and connectivity check
./tools/e2e-test/grpc.sh list        # List services (requires grpcurl)
./tools/e2e-test/grpc.sh test        # Test gRPC calls
./tools/e2e-test/grpc.sh discovery   # Service discovery configuration
```

### gRPC Services

| Service | Proto | Methods |
|---------|-------|---------|
| `ProductService` | `product.proto` | `GetProducts`, `ReserveStock`, `ReleaseStock` |

### gRPC Validation Points

| Check | How | Expected |
|-------|-----|----------|
| Product service reachable | `grpc.sh status` | HTTP 200 on health, gRPC port open |
| Service discovery | `grpc.sh discovery` | `AddServiceDiscovery()` configured |
| Proto matches | Compare proto file | Same version client/server |

## Cleanup After Testing

After completing tests, offer cleanup options based on the mode selected in Phase 0:

### Ask User About Cleanup

**Manual mode:**
```
Test completed. Cleanup options:

1. Keep everything running (for further testing)
2. Reset test data (purge queues, clear orders)

Note: Stop services manually with Ctrl+C in your AppHost terminal.
What would you like to do?
```

**Automatic mode (AppHost started by skill):**
```
Test completed. Cleanup options:

1. Keep AppHost running (for further testing)
2. Stop AppHost (terminate background process)
3. Reset test data only (keep services running)
4. Full cleanup (stop AppHost + reset data)

What would you like to do?
```

Use `TaskStop` with the saved `task_id` to stop the background AppHost process.

### Cleanup Commands

Use `./tools/e2e-test/cleanup.sh` for easy cleanup:

```bash
./tools/e2e-test/cleanup.sh status    # See what needs cleaning
./tools/e2e-test/cleanup.sh data      # Clear test orders, reservations
./tools/e2e-test/cleanup.sh queues    # Purge RabbitMQ queues
./tools/e2e-test/cleanup.sh logs      # Remove logs older than 7 days
./tools/e2e-test/cleanup.sh env       # Remove generated .env
./tools/e2e-test/cleanup.sh services  # Kill all running EShop services
./tools/e2e-test/cleanup.sh all       # Full cleanup (except services)
```

### Kill Services

Use `./tools/e2e-test/kill-services.sh` to kill all running EShop services:

```bash
./tools/e2e-test/kill-services.sh           # Show running services
./tools/e2e-test/kill-services.sh kill      # Kill with confirmation
./tools/e2e-test/kill-services.sh --force   # Kill without confirmation
```

This script finds and terminates all processes matching:
- `EShop.*` (AppHost, common libs)
- `Order.API`, `Products.API`, `Gateway.API`
- `Notification.API`, `Analytics.API`
- `DatabaseMigration`

Or manually:

```bash
# Stop Aspire (if started by this session)
# Note: AppHost runs in foreground, Ctrl+C stops it

# Reset databases (clear test orders, keep products)
./tools/reset-db.sh

# Purge RabbitMQ queues (remove stuck messages)
./tools/e2e-test/rabbitmq.sh purge <queue-name>
```

### Test Data Cleanup SQL

```sql
-- Clear orders (orderdb)
DELETE FROM "OrderItem";
DELETE FROM "Order";
DELETE FROM "OutboxMessage";
DELETE FROM "OutboxState";
DELETE FROM "InboxState";

-- Clear stock reservations (productdb)
DELETE FROM "StockReservation";

-- Note: Stock.Quantity doesn't need reset - it's not modified by orders

-- Clear processed messages (notificationdb) - note plural "Messages"
DELETE FROM "ProcessedMessages";
```

### When to Clean Up

| Scenario | Recommended Cleanup |
|----------|---------------------|
| Single test run | Option 1 (keep running) |
| End of testing session | Option 2 (stop services) |
| Tests created bad data | Option 3 (reset data) |
| Fresh start needed | Option 4 (full cleanup) |

### Important Notes

- **Never auto-cleanup** without asking user
- **Preserve logs** - useful for debugging issues found during tests
- **Database reset** uses `./tools/reset-db.sh` which re-seeds products
- **RabbitMQ queues** auto-recreate when services restart
- **Automatic mode cleanup** - if you started AppHost in background, ALWAYS offer to stop it at the end using `TaskStop` with the saved `task_id`
- **Manual mode** - user manages services, don't attempt to stop them

## Files Reference

| File | Purpose |
|------|---------|
| `./tools/e2e-test/discover.sh` | Service discovery (ports, credentials) |
| `./tools/e2e-test/db-query.sh` | Database queries |
| `./tools/e2e-test/logs.sh` | Log inspection |
| `./tools/e2e-test/api.sh` | API call helper |
| `./tools/e2e-test/rabbitmq.sh` | RabbitMQ diagnostics |
| `./tools/e2e-test/grpc.sh` | gRPC diagnostics |
| `./tools/e2e-test/trace-correlation.sh` | Distributed tracing by CorrelationId |
| `./tools/e2e-test/cleanup.sh` | Test cleanup (default: all) |
| `./tools/e2e-test/kill-services.sh` | Kill all running EShop services |
| `./tools/reset-db.sh` | Database reset script |
| `src/Services/*/logs/*.log` | Service log files |
| `http://localhost:PORT/swagger` | API documentation |

## Technical Notes

### StockReservation Table Schema
- `ReservedAt` - timestamp when reservation was made
- `ExpiresAt` - when reservation expires
- `Status`: 0 = Active, 1 = Released

### Process Names in lsof
Aspire services use truncated names:
- `EShop.Ord` / `Order.API`
- `EShop.Pro` / `Products.`
- `EShop.Gat` / `Gateway.A`

The `discover.sh` script searches for both naming patterns.
