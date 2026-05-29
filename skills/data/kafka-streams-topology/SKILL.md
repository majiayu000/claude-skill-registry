---
description: Kafka Streams topology design expert. Covers KStream vs KTable vs GlobalKTable, topology patterns, stream operations (filter, map, flatMap, branch), joins, windowing strategies, and exactly-once semantics. Activates for kafka streams topology, kstream, ktable, globalkTable, stream operations, stream joins, windowing, exactly-once, topology design.
---

# Kafka Streams Topology Skill

Expert knowledge of Kafka Streams library for building stream processing topologies in Java/Kotlin.

## What I Know

### Core Abstractions

**KStream** (Event Stream - Unbounded, Append-Only):
- Represents immutable event sequences
- Each record is an independent event
- Use for: Clickstreams, transactions, sensor readings

**KTable** (Changelog Stream - Latest State by Key):
- Represents mutable state (compacted topic)
- Updates override previous values (by key)
- Use for: User profiles, product catalog, account balances

**GlobalKTable** (Replicated Table - Available on All Instances):
- Full table replicated to every stream instance
- No partitioning (broadcast)
- Use for: Reference data (countries, products), lookups

**Key Differences**:
```java
// KStream: Every event is independent
KStream<Long, Click> clicks = builder.stream("clicks");
clicks.foreach((key, value) -> {
    System.out.println(value); // Prints every click event
});

// KTable: Latest value wins (by key)
KTable<Long, User> users = builder.table("users");
users.toStream().foreach((key, value) -> {
    System.out.println(value); // Prints only current user state
});

// GlobalKTable: Replicated to all instances (no partitioning)
GlobalKTable<Long, Product> products = builder.globalTable("products");
// Available for lookups on any instance (no repartitioning needed)
```

## When to Use This Skill

Activate me when you need help with:
- Topology design ("How to design Kafka Streams topology?")
- KStream vs KTable ("When to use KStream vs KTable?")
- Stream operations ("Filter and transform events")
- Joins ("Join KStream with KTable")
- Windowing ("Tumbling vs hopping vs session windows")
- Exactly-once semantics ("Enable EOS")
- Topology optimization ("Optimize stream processing")

## Common Patterns

### Pattern 1: Filter and Transform

**Use Case**: Clean and enrich events

```java
StreamsBuilder builder = new StreamsBuilder();

// Input stream
KStream<Long, ClickEvent> clicks = builder.stream("clicks");

// Filter out bot clicks
KStream<Long, ClickEvent> humanClicks = clicks
    .filter((key, value) -> !value.isBot());

// Transform: Extract page from URL
KStream<Long, String> pages = humanClicks
    .mapValues(click -> extractPage(click.getUrl()));

// Write to output topic
pages.to("pages");
```

### Pattern 2: Branch by Condition

**Use Case**: Route events to different paths

```java
Map<String, KStream<Long, Order>> branches = orders
    .split(Named.as("order-"))
    .branch((key, order) -> order.getTotal() > 1000, Branched.as("high-value"))
    .branch((key, order) -> order.getTotal() > 100, Branched.as("medium-value"))
    .defaultBranch(Branched.as("low-value"));

// High-value orders → priority processing
branches.get("order-high-value").to("priority-orders");

// Low-value orders → standard processing
branches.get("order-low-value").to("standard-orders");
```

### Pattern 3: Enrich Stream with Table (Stream-Table Join)

**Use Case**: Add user details to click events

```java
// Users table (current state)
KTable<Long, User> users = builder.table("users");

// Clicks stream
KStream<Long, ClickEvent> clicks = builder.stream("clicks");

// Enrich clicks with user data (left join)
KStream<Long, EnrichedClick> enriched = clicks.leftJoin(
    users,
    (click, user) -> new EnrichedClick(
        click.getPage(),
        user != null ? user.getName() : "unknown",
        user != null ? user.getEmail() : "unknown"
    ),
    Joined.with(Serdes.Long(), clickSerde, userSerde)
);

enriched.to("enriched-clicks");
```

### Pattern 4: Aggregate with Windowing

**Use Case**: Count clicks per user, per 5-minute window

```java
KTable<Windowed<Long>, Long> clickCounts = clicks
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
    .count(Materialized.as("click-counts-store"));

// Convert to stream for output
clickCounts.toStream()
    .map((windowedKey, count) -> {
        Long userId = windowedKey.key();
        Instant start = windowedKey.window().startTime();
        Instant end = windowedKey.window().endTime();
        return KeyValue.pair(userId, new WindowedCount(userId, start, end, count));
    })
    .to("click-counts");
```

### Pattern 5: Stateful Processing with State Store

**Use Case**: Detect duplicate events within 10 minutes

```java
// Define state store
StoreBuilder<KeyValueStore<Long, Long>> storeBuilder =
    Stores.keyValueStoreBuilder(
        Stores.persistentKeyValueStore("dedup-store"),
        Serdes.Long(),
        Serdes.Long()
    );

builder.addStateStore(storeBuilder);

// Deduplicate events
KStream<Long, Event> deduplicated = events.transformValues(
    () -> new ValueTransformerWithKey<Long, Event, Event>() {
        private KeyValueStore<Long, Long> store;

        @Override
        public void init(ProcessorContext context) {
            this.store = context.getStateStore("dedup-store");
        }

        @Override
        public Event transform(Long key, Event value) {
            Long lastSeen = store.get(key);
            long now = System.currentTimeMillis();

            // Duplicate detected (within 10 minutes)
            if (lastSeen != null && (now - lastSeen) < 600_000) {
                return null; // Drop duplicate
            }

            // Not duplicate, store timestamp
            store.put(key, now);
            return value;
        }
    },
    "dedup-store"
).filter((key, value) -> value != null); // Remove nulls

deduplicated.to("unique-events");
```

## Join Types

### 1. Stream-Stream Join (Inner)

**Use Case**: Correlate related events within time window

```java
// Page views and clicks within 10 minutes
KStream<Long, PageView> views = builder.stream("page-views");
KStream<Long, Click> clicks = builder.stream("clicks");

KStream<Long, ClickWithView> joined = clicks.join(
    views,
    (click, view) -> new ClickWithView(click, view),
    JoinWindows.of(Duration.ofMinutes(10)),
    StreamJoined.with(Serdes.Long(), clickSerde, viewSerde)
);
```

### 2. Stream-Table Join (Left)

**Use Case**: Enrich events with current state

```java
// Add product details to order items
KTable<Long, Product> products = builder.table("products");
KStream<Long, OrderItem> items = builder.stream("order-items");

KStream<Long, EnrichedOrderItem> enriched = items.leftJoin(
    products,
    (item, product) -> new EnrichedOrderItem(
        item,
        product != null ? product.getName() : "Unknown",
        product != null ? product.getPrice() : 0.0
    )
);
```

### 3. Table-Table Join (Inner)

**Use Case**: Combine two tables (latest state)

```java
// Join users with their current shopping cart
KTable<Long, User> users = builder.table("users");
KTable<Long, Cart> carts = builder.table("shopping-carts");

KTable<Long, UserWithCart> joined = users.join(
    carts,
    (user, cart) -> new UserWithCart(user.getName(), cart.getTotal())
);
```

### 4. Stream-GlobalKTable Join

**Use Case**: Enrich with reference data (no repartitioning)

```java
// Add country details to user registrations
GlobalKTable<String, Country> countries = builder.globalTable("countries");
KStream<Long, UserRegistration> registrations = builder.stream("registrations");

KStream<Long, EnrichedRegistration> enriched = registrations.leftJoin(
    countries,
    (userId, registration) -> registration.getCountryCode(), // Key extractor
    (registration, country) -> new EnrichedRegistration(
        registration,
        country != null ? country.getName() : "Unknown"
    )
);
```

## Windowing Strategies

### Tumbling Windows (Non-Overlapping)

**Use Case**: Aggregate per fixed time period

```java
// Count events every 5 minutes
KTable<Windowed<Long>, Long> counts = events
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
    .count();

// Windows: [0:00-0:05), [0:05-0:10), [0:10-0:15)
```

### Hopping Windows (Overlapping)

**Use Case**: Moving average or overlapping aggregates

```java
// Count events in 10-minute windows, advancing every 5 minutes
KTable<Windowed<Long>, Long> counts = events
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeAndGrace(
        Duration.ofMinutes(10),
        Duration.ofMinutes(5)
    ).advanceBy(Duration.ofMinutes(5)))
    .count();

// Windows: [0:00-0:10), [0:05-0:15), [0:10-0:20)
```

### Session Windows (Event-Based)

**Use Case**: User sessions with inactivity gap

```java
// Session ends after 30 minutes of inactivity
KTable<Windowed<Long>, Long> sessionCounts = events
    .groupByKey()
    .windowedBy(SessionWindows.ofInactivityGapWithNoGrace(Duration.ofMinutes(30)))
    .count();
```

### Sliding Windows (Continuous)

**Use Case**: Anomaly detection over sliding time window

```java
// Detect >100 events in any 1-minute period
KTable<Windowed<Long>, Long> slidingCounts = events
    .groupByKey()
    .windowedBy(SlidingWindows.ofTimeDifferenceWithNoGrace(Duration.ofMinutes(1)))
    .count();
```

## Best Practices

### 1. Partition Keys Correctly

✅ **DO**:
```java
// Repartition by user_id before aggregation
KStream<Long, Event> byUser = events
    .selectKey((key, value) -> value.getUserId());

// Now aggregation is efficient
KTable<Long, Long> userCounts = byUser
    .groupByKey()
    .count();
```

❌ **DON'T**:
```java
// WRONG: groupBy with different key (triggers repartitioning!)
KTable<Long, Long> userCounts = events
    .groupBy((key, value) -> KeyValue.pair(value.getUserId(), value))
    .count();
```

### 2. Use Appropriate Serdes

✅ **DO**:
```java
// Define custom serde for complex types
Serde<User> userSerde = new JsonSerde<>(User.class);

KStream<Long, User> users = builder.stream(
    "users",
    Consumed.with(Serdes.Long(), userSerde)
);
```

❌ **DON'T**:
```java
// WRONG: No serde specified (uses default String serde!)
KStream<Long, User> users = builder.stream("users");
```

### 3. Enable Exactly-Once Semantics

✅ **DO**:
```java
Properties props = new Properties();
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
    StreamsConfig.EXACTLY_ONCE_V2); // EOS v2 (recommended)
props.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, 100); // Commit frequently
```

### 4. Use Materialized Stores for Queries

✅ **DO**:
```java
// Named store for interactive queries
KTable<Long, Long> counts = events
    .groupByKey()
    .count(Materialized.<Long, Long, KeyValueStore<Bytes, byte[]>>as("user-counts")
        .withKeySerde(Serdes.Long())
        .withValueSerde(Serdes.Long()));

// Query store from REST API
ReadOnlyKeyValueStore<Long, Long> store =
    streams.store(StoreQueryParameters.fromNameAndType(
        "user-counts",
        QueryableStoreTypes.keyValueStore()
    ));

Long count = store.get(userId);
```

## Topology Optimization

### 1. Combine Operations

**GOOD** (Single pass):
```java
KStream<Long, String> result = events
    .filter((key, value) -> value.isValid())
    .mapValues(value -> value.toUpperCase())
    .filterNot((key, value) -> value.contains("test"));
```

**BAD** (Multiple intermediate topics):
```java
KStream<Long, Event> valid = events.filter((key, value) -> value.isValid());
valid.to("valid-events"); // Unnecessary write

KStream<Long, Event> fromValid = builder.stream("valid-events");
KStream<Long, String> upper = fromValid.mapValues(v -> v.toUpperCase());
```

### 2. Reuse KTables

**GOOD** (Shared table):
```java
KTable<Long, User> users = builder.table("users");

KStream<Long, EnrichedClick> enrichedClicks = clicks.leftJoin(users, ...);
KStream<Long, EnrichedOrder> enrichedOrders = orders.leftJoin(users, ...);
```

**BAD** (Duplicate tables):
```java
KTable<Long, User> users1 = builder.table("users");
KTable<Long, User> users2 = builder.table("users"); // Duplicate!
```

## Testing Topologies

### Topology Test Driver

```java
@Test
public void testClickFilter() {
    // Setup topology
    StreamsBuilder builder = new StreamsBuilder();
    KStream<Long, Click> clicks = builder.stream("clicks");
    clicks.filter((key, value) -> !value.isBot())
          .to("human-clicks");

    Topology topology = builder.build();

    // Create test driver
    TopologyTestDriver testDriver = new TopologyTestDriver(topology);

    // Input topic
    TestInputTopic<Long, Click> inputTopic = testDriver.createInputTopic(
        "clicks",
        Serdes.Long().serializer(),
        clickSerde.serializer()
    );

    // Output topic
    TestOutputTopic<Long, Click> outputTopic = testDriver.createOutputTopic(
        "human-clicks",
        Serdes.Long().deserializer(),
        clickSerde.deserializer()
    );

    // Send test data
    inputTopic.pipeInput(1L, new Click(1L, "page1", false)); // Human
    inputTopic.pipeInput(2L, new Click(2L, "page2", true));  // Bot

    // Assert output
    List<Click> output = outputTopic.readValuesToList();
    assertEquals(1, output.size()); // Only human click
    assertFalse(output.get(0).isBot());

    testDriver.close();
}
```

## Common Issues & Solutions

### Issue 1: StreamsException - Not Co-Partitioned

**Error**: Topics not co-partitioned for join

**Root Cause**: Joined streams/tables have different partition counts

**Solution**: Repartition to match:
```java
// Ensure same partition count
KStream<Long, Event> repartitioned = events
    .through("events-repartitioned",
        Produced.with(Serdes.Long(), eventSerde)
            .withStreamPartitioner((topic, key, value, numPartitions) ->
                (int) (key % 12) // Match target partition count
            )
    );
```

### Issue 2: Out of Memory (Large State Store)

**Error**: Java heap space

**Root Cause**: State store too large, windowing not used

**Solution**: Add time-based cleanup:
```java
// Use windowing to limit state size
KTable<Windowed<Long>, Long> counts = events
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeAndGrace(
        Duration.ofHours(24),     // Window size
        Duration.ofHours(1)       // Grace period
    ))
    .count();
```

### Issue 3: High Lag, Slow Processing

**Root Cause**: Blocking operations, inefficient transformations

**Solution**: Use async processing:
```java
// BAD: Blocking HTTP call
events.mapValues(value -> {
    return httpClient.get(value.getUrl()); // BLOCKS!
});

// GOOD: Async processing with state store
events.transformValues(() -> new AsyncEnricher());
```

## References

- Kafka Streams Documentation: https://kafka.apache.org/documentation/streams/
- Kafka Streams Tutorial: https://kafka.apache.org/documentation/streams/tutorial
- Testing Guide: https://kafka.apache.org/documentation/streams/developer-guide/testing.html

---

**Invoke me when you need topology design, joins, windowing, or exactly-once semantics expertise!**
