---
name: kratos-events
description: Implements event-driven architecture with Watermill pub/sub (RabbitMQ/AMQP/message queue) for go-kratos microservices. Creates publisher/subscriber wrappers, event handlers, worker services with context propagation (request_id, correlation_id), and RabbitMQ/AMQP integration. Use when implementing pub/sub patterns, creating message queues, adding event handlers, building worker services for async processing, or setting up background jobs.
---

<essential_principles>
## How Event-Driven Architecture Works in Kratos

### Three-Layer Architecture

**1. Platform Layer** (`platform/events/`)
- Broker-agnostic interfaces (Publisher, Subscriber)
- Allows swapping brokers (AMQP, Redis, Kafka) without changing code

**2. Data Layer** (`services/{service}/internal/data/mq/`)
- Publisher/Subscriber wrappers
- Context propagation and metadata enrichment
- Structured logging with request_id and correlation_id

**3. Application Layer** (`services/{service}/internal/handlers/`)
- Event handlers with business logic
- Delegate to use cases (biz layer)
- Extract context and metadata from messages

### Worker Services

Each service can have a companion **worker** binary:
```
services/{service}/
  ├── cmd/
  │   ├── {service}/        # Main HTTP/gRPC service
  │   └── {service}-worker/ # Event processing worker
  ├── internal/
  │   ├── handlers/         # Event handlers
  │   ├── worker/           # Watermill router setup
  │   └── ...
```

### Context Propagation Flow

```
HTTP Request → Middleware (request_id) → Use Case → Publisher
    ↓ (message with context + metadata)
Subscriber → Handler → Use Case (same request_id in logs)
```

**Best Practice**: Always use `logger.WithContext(ctx)` for distributed tracing.
</essential_principles>

<intake>
What would you like to do?

1. Create publisher/subscriber wrappers for a new service
2. Add event handler for existing service
3. Set up worker service for async processing
4. Publish events from business layer
5. View examples and patterns

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "create wrappers", "new service" | `workflows/create-pubsub-wrappers.md` |
| 2, "add handler", "handler" | `workflows/add-event-handler.md` |
| 3, "worker", "async", "background" | `workflows/setup-worker.md` |
| 4, "publish", "emit event" | `workflows/publish-events.md` |
| 5, "examples", "patterns", "help" | `workflows/view-examples.md` |

**After reading the workflow, follow it exactly.**
</routing>

<quick_start>
## 1. Create Publisher/Subscriber Wrappers

**File**: `services/{service}/internal/data/mq/publisher.go`

```go
package mq

import (
	"context"
	"fmt"
	"platform/events"
	middleware2 "platform/middleware"

	"github.com/ThreeDotsLabs/watermill"
	"github.com/ThreeDotsLabs/watermill/message"
	"github.com/ThreeDotsLabs/watermill/message/router/middleware"
	"github.com/go-kratos/kratos/v2/log"
)

const RoutingKey = "routing_key"

func NewEventPublisher(pub message.Publisher, logger log.Logger) events.Publisher {
	return &eventPublisher{
		pub:    pub,
		logger: log.NewHelper(logger),
	}
}

type eventPublisher struct {
	pub    message.Publisher
	logger *log.Helper
}

func (ep *eventPublisher) Unwrap() message.Publisher {
	return ep.pub
}

func (ep *eventPublisher) Publish(ctx context.Context, topic string, payload []byte) error {
	msg := message.NewMessage(watermill.NewUUID(), payload)

	// Propagate context to subscriber
	msg.SetContext(ctx)

	// Set correlation ID if not already set
	correlationId := middleware.MessageCorrelationID(msg)
	if correlationId == "" {
		correlationId = watermill.NewUUID()
		middleware.SetCorrelationID(correlationId, msg)
	}

	// Set routing key
	SetMessageRoutingKey(topic, msg)

	// Extract request ID from HTTP context
	if requestID := extractRequestID(ctx); requestID != "" {
		msg.Metadata.Set(middleware2.RequestIdKey, requestID)
	}

	ep.logger.WithContext(ctx).Infof("Publishing message %s to topic %s, correlation_id: %s", msg.UUID, topic, correlationId)

	if err := ep.pub.Publish(topic, msg); err != nil {
		ep.logger.WithContext(ctx).Errorf("Failed to publish message %s to topic %s: %v", msg.UUID, topic, err)
		return fmt.Errorf("failed to publish message to topic %s: %w", topic, err)
	}

	return nil
}

func SetMessageRoutingKey(key string, msg *message.Message) {
	if MessageRoutingKey(msg) != "" {
		return
	}
	msg.Metadata.Set(RoutingKey, key)
}

func MessageRoutingKey(message *message.Message) string {
	return message.Metadata.Get(RoutingKey)
}

func extractRequestID(ctx context.Context) string {
	val := middleware2.RequestID()(ctx)
	if requestID, ok := val.(string); ok {
		return requestID
	}
	return ""
}
```

**File**: `services/{service}/internal/data/mq/subscriber.go`

```go
package mq

import (
	"context"
	"platform/events"

	"github.com/ThreeDotsLabs/watermill/message"
	"github.com/go-kratos/kratos/v2/log"
)

func NewEventSubscriber(sub message.Subscriber, logger log.Logger) events.Subscriber {
	return &eventSubscriber{
		sub:    sub,
		logger: log.NewHelper(logger),
	}
}

type eventSubscriber struct {
	sub    message.Subscriber
	logger *log.Helper
}

func (es *eventSubscriber) Subscribe(ctx context.Context, topic string) (<-chan *message.Message, error) {
	es.logger.WithContext(ctx).Infof("Subscribing to topic: %s", topic)

	messages, err := es.sub.Subscribe(ctx, topic)
	if err != nil {
		es.logger.WithContext(ctx).Errorf("Failed to subscribe to topic %s: %v", topic, err)
		return nil, err
	}

	es.logger.WithContext(ctx).Infof("Successfully subscribed to topic: %s", topic)
	return messages, nil
}

func (es *eventSubscriber) Close() error {
	es.logger.Info("Closing event subscriber")

	if err := es.sub.Close(); err != nil {
		es.logger.Errorf("Failed to close subscriber: %v", err)
		return err
	}

	es.logger.Info("Event subscriber closed successfully")
	return nil
}

func (es *eventSubscriber) Unwrap() message.Subscriber {
	return es.sub
}
```

## 2. Create Event Handler

**File**: `services/{service}/internal/handlers/{event}_handler.go`

```go
package handlers

import (
	"{service}/internal/biz"

	"github.com/ThreeDotsLabs/watermill/message"
	"github.com/go-kratos/kratos/v2/log"
)

func NewLifecycleEventHandler(symbolUC biz.SymbolUseCase, logger log.Logger) *LifecycleEventHandler {
	return &LifecycleEventHandler{
		logger:   log.NewHelper(logger),
		symbolUC: symbolUC,
	}
}

type LifecycleEventHandler struct {
	logger   *log.Helper
	symbolUC biz.SymbolUseCase
}

func (h *LifecycleEventHandler) Handle(msg *message.Message) error {
	// CRITICAL: Extract context from message
	ctx := msg.Context()

	// Extract correlation ID for tracing
	correlationID := msg.Metadata.Get("correlation_id")
	requestID := msg.Metadata.Get("request_id")

	h.logger.WithContext(ctx).Infof(
		"Processing lifecycle event - msgID: %s, correlationID: %s, requestID: %s",
		msg.UUID,
		correlationID,
		requestID,
	)

	// Unmarshal payload
	var payload EventPayload
	if err := json.Unmarshal(msg.Payload, &payload); err != nil {
		h.logger.WithContext(ctx).Errorf("Failed to unmarshal payload: %v", err)
		return err
	}

	// Delegate to business layer
	if err := h.symbolUC.ProcessLifecycleEvent(ctx, &payload); err != nil {
		h.logger.WithContext(ctx).Errorf("Failed to process event: %v", err)
		return err
	}

	return nil
}
```

**File**: `services/{service}/internal/handlers/provider.go`

```go
package handlers

import "github.com/google/wire"

// ProviderSet is handlers providers.
var ProviderSet = wire.NewSet(
	NewLifecycleEventHandler,
)
```

## 3. Create Worker Service

**File**: `services/{service}/internal/worker/worker.go`

```go
package worker

import (
	"context"
	"fmt"
	"platform/events"
	platform_logger "platform/logger"
	conf "symbols/internal/conf/gen"
	"symbols/internal/handlers"
	"sync"
	"time"

	"github.com/ThreeDotsLabs/watermill/message"
	"github.com/ThreeDotsLabs/watermill/message/router/middleware"
	"github.com/ThreeDotsLabs/watermill/message/router/plugin"
	"github.com/go-kratos/kratos/v2/log"
)

type HookFunc func(ctx context.Context) error

type Worker interface {
	Start() HookFunc
	Stop() HookFunc
}

func NewWorker(router *message.Router, logger log.Logger) Worker {
	return &worker{
		logger:       log.NewHelper(logger),
		name:         "watermill-router",
		router:       router,
		closeTimeout: 15 * time.Second,
		done:         make(chan struct{}),
	}
}

type worker struct {
	logger       *log.Helper
	name         string
	router       *message.Router
	closeTimeout time.Duration

	startOnce sync.Once
	stopOnce  sync.Once

	done chan struct{}
	err  error
}

func (w *worker) Start() HookFunc {
	return func(ctx context.Context) error {
		w.startOnce.Do(func() {
			go func() {
				defer close(w.done)
				w.logger.WithContext(ctx).Infof("Starting router %s", w.name)
				if err := w.router.Run(ctx); err != nil {
					w.err = fmt.Errorf("%s: router run: %w", w.name, err)
					w.logger.WithContext(ctx).Errorf("%v", w.err)
				}
			}()
		})

		return nil
	}
}

func (w *worker) Stop() HookFunc {
	return func(ctx context.Context) error {
		var closeErr error
		w.stopOnce.Do(func() {
			stopCtx, cancel := context.WithTimeout(ctx, w.closeTimeout)
			defer cancel()

			w.logger.WithContext(ctx).Infof("Closing router %s", w.name)

			errCh := make(chan error, 1)
			go func() { errCh <- w.router.Close() }()

			select {
			case <-stopCtx.Done():
				w.logger.WithContext(ctx).Errorf("Shutting down %s (timeout: %v)", w.name, w.closeTimeout)
				closeErr = fmt.Errorf("%s: router close timeout: %w", w.name, stopCtx.Err())
			case err := <-errCh:
				if err != nil {
					w.logger.WithContext(ctx).Errorf("%s: router failed to gracefully close: %v", w.name, err)
					closeErr = fmt.Errorf("%s: router close: %w", w.name, err)
				}
			}
		})

		<-w.done
		if closeErr != nil && w.err == nil {
			w.err = closeErr
		}

		return w.err
	}
}

func NewRouter(cfg *conf.Data, lifecycleHandler *handlers.LifecycleEventHandler, eventPub events.Publisher, eventSub events.Subscriber, logger *platform_logger.WatermillLogger) *message.Router {

	router, err := message.NewRouter(message.RouterConfig{}, logger)

	if err != nil {
		panic(err)
	}

	// SignalsHandler will gracefully shut down Router when SIGTERM is received
	router.AddPlugin(plugin.SignalsHandler)

	// Router level middleware is executed for every message sent to the router
	router.AddMiddleware(
		// CorrelationID will copy the correlation id from the incoming message's metadata to the produced messages
		middleware.CorrelationID,

		// The handler function is retried if it returns an error
		middleware.Retry{
			MaxRetries:      3,
			InitialInterval: time.Millisecond * 100,
			Logger:          logger,
		}.Middleware,

		// Recoverer handles panics from handlers
		middleware.Recoverer,
	)

	// Add handlers for specific topics
	router.AddConsumerHandler("events", cfg.Mq.Exchange.Name, eventSub.Unwrap(), lifecycleHandler.Handle)

	return router
}
```

**File**: `services/{service}/cmd/{service}-worker/main.go`

```go
package main

import (
	"flag"
	"os"
	p "platform/logger"
	"{service}/internal/conf/gen"
	"{service}/internal/worker"

	"github.com/go-kratos/kratos/v2"
	"github.com/go-kratos/kratos/v2/config"
	"github.com/go-kratos/kratos/v2/config/env"
	"github.com/go-kratos/kratos/v2/config/file"
	"github.com/go-kratos/kratos/v2/log"
	_ "go.uber.org/automaxprocs"
)

var (
	Name       string = "{service}-worker"
	Version    string = "1.0"
	configFile string
	id, _             = os.Hostname()
)

func init() {
	flag.StringVar(&configFile, "conf", "configs/config.yaml", "config path, eg: --conf config.yaml")
}

func newApp(worker worker.Worker, logger log.Logger) *kratos.App {
	return kratos.New(
		kratos.ID(id),
		kratos.Name(Name),
		kratos.Version(Version),
		kratos.Metadata(map[string]string{}),
		kratos.Logger(logger),
		kratos.BeforeStart(worker.Start()),
		kratos.AfterStop(worker.Stop()),
	)
}

func main() {
	flag.Parse()

	c := config.New(
		config.WithSource(
			env.NewSource(),
			file.NewSource(configFile),
		),
	)
	defer c.Close()

	if err := c.Load(); err != nil {
		panic(err)
	}

	var bc conf.Bootstrap
	if err := c.Scan(&bc); err != nil {
		panic(err)
	}

	if err := bc.Validate(); err != nil {
		panic(err)
	}

	logger := p.NewLogger(bc.Log.Level, id, Name, Version)

	app, cleanup, err := wireApp(bc.Server, bc.Data, bc.Log, logger)
	if err != nil {
		panic(err)
	}
	defer cleanup()

	if err := app.Run(); err != nil {
		panic(err)
	}
}
```

## 4. Publish Events from Business Layer

**File**: `services/{service}/internal/biz/{entity}.go`

```go
func (uc *symbolUseCase) CreateSymbol(ctx context.Context, symbol *Symbol) (*Symbol, error) {
	// Validate
	if err := uc.validator.Struct(symbol); err != nil {
		return nil, err
	}

	// Create in database
	result, err := uc.repo.Create(ctx, symbol)
	if err != nil {
		return nil, err
	}

	// Publish event (if publisher configured)
	if uc.pub != nil {
		payload, _ := json.Marshal(map[string]interface{}{
			"symbol_id": result.Id,
			"action":    "created",
		})

		// Context is automatically propagated with request_id
		if err := uc.pub.Publish(ctx, "symbols.created", payload); err != nil {
			uc.log.WithContext(ctx).Errorf("Failed to publish event: %v", err)
			// Don't fail the operation if event publishing fails
		}
	}

	return result, nil
}
```
</quick_start>

<critical_patterns>
## Context Propagation

**ALWAYS extract context from message**:
```go
func (h *Handler) Handle(msg *message.Message) error {
	ctx := msg.Context()  // CRITICAL - preserves request_id chain
	h.logger.WithContext(ctx).Infof("Processing...")
}
```

**ALWAYS use WithContext for logging**:
```go
h.logger.WithContext(ctx).Infof("...")  // ✅ Includes request_id
h.logger.Infof("...")                    // ❌ No request_id
```

## Metadata Extraction

```go
correlationID := msg.Metadata.Get("correlation_id")
requestID := msg.Metadata.Get("request_id")
```

## Error Handling in Handlers

```go
func (h *Handler) Handle(msg *message.Message) error {
	// Return error to trigger retry (configured in middleware)
	if err := h.process(msg); err != nil {
		h.logger.WithContext(ctx).Errorf("Processing failed: %v", err)
		return err  // Watermill will retry based on middleware config
	}

	// Return nil to ACK message
	return nil
}
```

## Unwrap Pattern

Use `Unwrap()` to access underlying Watermill publisher/subscriber for router:
```go
router.AddConsumerHandler("name", topic, eventSub.Unwrap(), handler.Handle)
```
</critical_patterns>

<file_structure>
```
services/{service}/
├── cmd/
│   ├── {service}/           # Main service
│   └── {service}-worker/    # Worker service
│       ├── main.go
│       ├── wire.go
│       └── wire_gen.go
├── internal/
│   ├── data/
│   │   └── mq/
│   │       ├── publisher.go
│   │       └── subscriber.go
│   ├── handlers/            # Event handlers
│   │   ├── provider.go
│   │   └── lifecycle.go
│   └── worker/              # Worker setup
│       └── worker.go
```
</file_structure>

<wire_integration>
## Adding to Wire

**File**: `services/{service}/internal/data/data.go`
```go
var ProviderSet = wire.NewSet(
	NewData,
	repo.NewSymbolRepo,
	mq.NewEventPublisher,     // Add publisher
	mq.NewEventSubscriber,    // Add subscriber
)
```

**File**: `services/{service}/internal/handlers/provider.go`
```go
var ProviderSet = wire.NewSet(
	NewLifecycleEventHandler,
)
```

**File**: `services/{service}/internal/worker/provider.go`
```go
var ProviderSet = wire.NewSet(
	NewWorker,
	NewRouter,
)
```

**File**: `services/{service}/cmd/{service}-worker/wire.go`
```go
//go:build wireinject

func wireApp(
	*conf.Server,
	*conf.Data,
	*conf.Log,
	log.Logger,
) (*kratos.App, func(), error) {
	wire.Build(
		worker.ProviderSet,
		handlers.ProviderSet,
		biz.ProviderSet,
		data.ProviderSet,
		newApp,
	)
	return &kratos.App{}, nil, nil
}
```

After adding providers, run:
```bash
cd services/{service}
make generate
```
</wire_integration>

<validation_checklist>
- [ ] Publisher wrapper enriches messages with context, correlation_id, request_id
- [ ] Subscriber wrapper provides lifecycle management
- [ ] Event handlers extract `ctx := msg.Context()`
- [ ] Event handlers use `logger.WithContext(ctx)`
- [ ] Event handlers delegate to biz layer (not data layer)
- [ ] Worker service uses graceful shutdown with timeout
- [ ] Router configured with middleware (CorrelationID, Retry, Recoverer)
- [ ] Unwrap() used for router integration
- [ ] Wire ProviderSets updated and regenerated
- [ ] Worker binary created in cmd/{service}-worker/
</validation_checklist>

<anti_patterns>
❌ **DON'T:**
- Log without context: `h.logger.Infof("...")`
- Ignore message context: process payload without extracting ctx
- Put business logic in handlers (delegate to use cases)
- Fail operations if event publishing fails
- Skip correlation ID propagation
- Use blocking operations in publisher without timeout

✅ **DO:**
- Always extract context: `ctx := msg.Context()`
- Always log with context: `h.logger.WithContext(ctx)`
- Delegate to use cases from handlers
- Make event publishing non-blocking (don't fail if publish fails)
- Use middleware.CorrelationID in router
- Set reasonable timeouts for worker shutdown
</anti_patterns>

<success_criteria>
Event-driven architecture is correctly implemented when:
1. Publisher/subscriber wrappers created in `internal/data/mq/`
2. Event handlers created in `internal/handlers/`
3. Worker service created in `cmd/{service}-worker/`
4. Context propagation works end-to-end (request_id visible in all logs)
5. Correlation IDs tracked across service boundaries
6. Handlers delegate to business layer (biz)
7. Router configured with retry and recovery middleware
8. Wire dependencies configured and regenerated
9. Worker gracefully shuts down on SIGTERM
10. All logging uses `WithContext(ctx)` for distributed tracing

**Verification**:
- Publish event from HTTP request, verify request_id appears in worker logs
- Check correlation_id is consistent across publisher and subscriber
- Test graceful shutdown with SIGTERM
- Verify retry middleware works on handler errors
</success_criteria>

<reference_docs>
For detailed architecture documentation, see:
- `docs/pubsub-architecture.md` - Complete pub/sub implementation guide
- `platform/events/events.go` - Platform interfaces
- CLAUDE.md - Event-driven architecture overview
</reference_docs>