---
name: aws-sdk-java-v2-dynamodb
description: Provides Amazon DynamoDB patterns using AWS SDK for Java 2.x. Use when creating, querying, scanning, or performing CRUD operations on DynamoDB tables, working with indexes, batch operations, transactions, or integrating with Spring Boot applications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java 2.x - Amazon DynamoDB

## Overview

Provides DynamoDB patterns using AWS SDK for Java 2.x with Enhanced Client for type-safe CRUD, queries, batch operations, transactions, and Spring Boot integration.

## When to Use

- CRUD operations on DynamoDB items
- Querying tables with sort keys or GSI
- Batch operations for multiple items
- Atomic transactions across tables
- Spring Boot integration with DynamoDB

## Instructions

1. Add AWS SDK DynamoDB dependencies to `pom.xml`
2. Configure client setup (low-level or Enhanced Client)
3. Define entity classes with `@DynamoDbBean` annotations
4. Perform operations using `DynamoDbTable` (CRUD, query, scan, batch, transactions)
5. Handle partial failures with retry logic and exponential backoff
6. Use repository pattern for Spring Boot integration

## Dependencies

Add to `pom.xml`:
```xml
<!-- Low-level DynamoDB client -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>dynamodb</artifactId>
</dependency>

<!-- Enhanced client (recommended) -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>dynamodb-enhanced</artifactId>
</dependency>
```
## Client Setup

### Low-Level Client
```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;

DynamoDbClient dynamoDb = DynamoDbClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

### Enhanced Client (Recommended)
```java
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;

DynamoDbEnhancedClient enhancedClient = DynamoDbEnhancedClient.builder()
    .dynamoDbClient(dynamoDb)
    .build();
```

## Entity Mapping

```java
@DynamoDbBean
public class Customer {

    @DynamoDbPartitionKey
    private String customerId;

    @DynamoDbAttribute("customer_name")
    private String name;

    private String email;

    @DynamoDbSortKey
    private String orderId;

    // Getters and setters
}
```

For complex entity mapping with GSIs and custom converters, see [Entity Mapping Reference](references/entity-mapping.md).

## CRUD Operations

### Basic Operations
```java
// Create or update item
DynamoDbTable<Customer> table = enhancedClient.table("Customers", TableSchema.fromBean(Customer.class));
table.putItem(customer);

// Get item
Customer result = table.getItem(Key.builder().partitionValue(customerId).build());

// Update item
return table.updateItem(customer);

// Delete item
table.deleteItem(Key.builder().partitionValue(customerId).build());
```

### Composite Key Operations
```java
// Get item with composite key
Order order = table.getItem(Key.builder()
    .partitionValue(customerId)
    .sortValue(orderId)
    .build());
```

## Query Operations

### Basic Query
```java
import software.amazon.awssdk.enhanced.dynamodb.model.QueryConditional;

QueryConditional queryConditional = QueryConditional
    .keyEqualTo(Key.builder()
        .partitionValue(customerId)
        .build());

List<Order> orders = table.query(queryConditional).items().stream()
    .collect(Collectors.toList());
```

### Advanced Query with Filters
```java
import software.amazon.awssdk.enhanced.dynamodb.Expression;

Expression filter = Expression.builder()
    .expression("status = :pending")
    .putExpressionValue(":pending", AttributeValue.builder().s("PENDING").build())
    .build();

List<Order> pendingOrders = table.query(r -> r
    .queryConditional(queryConditional)
    .filterExpression(filter))
    .items().stream()
    .collect(Collectors.toList());
```

For detailed query patterns, see [Advanced Operations Reference](references/advanced-operations.md).

## Scan Operations

> **Warning**: Scan reads entire table and consumes read capacity for all items. Prefer Query operations with partition keys or GSIs whenever possible.

**Validation before scan**:
- Confirm query with partition key is not feasible for your access pattern
- Verify table has sufficient provisioned read capacity or use on-demand mode
- Consider using pagination with `limit()` to control capacity consumption

```java
// Scan all items
List<Customer> allCustomers = table.scan().items().stream()
    .collect(Collectors.toList());

// Scan with filter
Expression filter = Expression.builder()
    .expression("points >= :minPoints")
    .putExpressionValue(":minPoints", AttributeValue.builder().n("1000").build())
    .build();

List<Customer> vipCustomers = table.scan(r -> r.filterExpression(filter))
    .items().stream()
    .collect(Collectors.toList());
```

## Batch Operations

### Batch Get
```java
import software.amazon.awssdk.enhanced.dynamodb.model.*;

List<Key> keys = customerIds.stream()
    .map(id -> Key.builder().partitionValue(id).build())
    .collect(Collectors.toList());

ReadBatch.Builder<Customer> batchBuilder = ReadBatch.builder(Customer.class)
    .mappedTableResource(table);

keys.forEach(batchBuilder::addGetItem);

BatchGetResultPageIterable result = enhancedClient.batchGetItem(r ->
    r.addReadBatch(batchBuilder.build()));

List<Customer> customers = result.resultsForTable(table).stream()
    .collect(Collectors.toList());
```

### Batch Write with Error Handling
```java
WriteBatch.Builder<Customer> batchBuilder = WriteBatch.builder(Customer.class)
    .mappedTableResource(table);

customers.forEach(batchBuilder::addPutItem);

BatchWriteItemEnhancedRequest request = BatchWriteItemEnhancedRequest.builder()
    .addWriteBatch(batchBuilder.build())
    .build();

BatchWriteResult result = enhancedClient.batchWriteItem(request);

// Validate: check for unprocessed items
if (!result.writeResponsesForTable(table).isEmpty()) {
    // Retry unprocessed items with exponential backoff
    Map<String, AttributeValue> unprocessed = result.writeResponsesForTable(table).get(0)
        .unprocessedAttributes();
    if (unprocessed != null && !unprocessed.isEmpty()) {
        enhancedClient.batchWriteItem(r -> r
            .addWriteBatch(WriteBatch.builder(Customer.class)
                .mappedTableResource(table)
                .addPutItemFromItem(unprocessed)
                .build()));
    }
}
```

## Transactions

### Transactional Write with Retry
```java
public void placeOrderWithRetry(Order order, Customer customer, int maxRetries) {
    int attempt = 0;
    while (attempt < maxRetries) {
        try {
            enhancedClient.transactWriteItems(r -> r
                .addPutItem(customerTable, customer)
                .addPutItem(orderTable, order));
            return;
        } catch (TransactionCanceledException e) {
            if (e.cancellationReasons().stream()
                .anyMatch(r -> r.code().equals("TransactionCanceledException")
                    && r.message().contains("throughput"))) {
                attempt++;
                if (attempt < maxRetries) {
                    try { Thread.sleep((long) Math.pow(2, attempt) * 100); }
                    catch (InterruptedException ie) { Thread.currentThread().interrupt(); }
                }
            } else {
                throw e; // Non-retryable error
            }
        }
    }
}
```

### Transactional Read
```java
TransactGetItemsEnhancedRequest request = TransactGetItemsEnhancedRequest.builder()
    .addGetItem(customerTable, customerKey)
    .addGetItem(orderTable, orderKey)
    .build();

List<Document> results = enhancedClient.transactGetItems(request);
```

## Spring Boot Integration

### Configuration
```java
@Configuration
public class DynamoDbConfiguration {

    @Bean
    public DynamoDbClient dynamoDbClient() {
        return DynamoDbClient.builder()
            .region(Region.US_EAST_1)
            .build();
    }

    @Bean
    public DynamoDbEnhancedClient dynamoDbEnhancedClient(DynamoDbClient dynamoDbClient) {
        return DynamoDbEnhancedClient.builder()
            .dynamoDbClient(dynamoDbClient)
            .build();
    }
}
```

### Repository Pattern
```java
@Repository
public class CustomerRepository {

    private final DynamoDbTable<Customer> customerTable;

    public CustomerRepository(DynamoDbEnhancedClient enhancedClient) {
        this.customerTable = enhancedClient.table("Customers", TableSchema.fromBean(Customer.class));
    }

    public void save(Customer customer) {
        customerTable.putItem(customer);
    }

    public Optional<Customer> findById(String customerId) {
        Key key = Key.builder().partitionValue(customerId).build();
        return Optional.ofNullable(customerTable.getItem(key));
    }
}
```

For comprehensive Spring Boot integration patterns, see [Spring Boot Integration Reference](references/spring-boot-integration.md).

## Testing

### Unit Testing with Mocks
```java
@ExtendWith(MockitoExtension.class)
class CustomerServiceTest {

    @Mock
    private DynamoDbClient dynamoDbClient;

    @Mock
    private DynamoDbEnhancedClient enhancedClient;

    @Mock
    private DynamoDbTable<Customer> customerTable;

    @InjectMocks
    private CustomerService customerService;

    @Test
    void saveCustomer_ShouldReturnSavedCustomer() {
        // Arrange
        when(enhancedClient.table(anyString(), any(TableSchema.class)))
            .thenReturn(customerTable);

        Customer customer = new Customer("123", "John Doe", "john@example.com");

        // Act
        Customer result = customerService.saveCustomer(customer);

        // Assert
        assertNotNull(result);
        verify(customerTable).putItem(customer);
    }
}
```

### Integration Testing with LocalStack
```java
@Testcontainers
@SpringBootTest
class DynamoDbIntegrationTest {

    @Container
    static LocalStackContainer localstack = new LocalStackContainer(
        DockerImageName.parse("localstack/localstack:3.0"))
        .withServices(LocalStackContainer.Service.DYNAMODB);

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("aws.endpoint",
            () -> localstack.getEndpointOverride(LocalStackContainer.Service.DYNAMODB).toString());
    }

    @Autowired
    private DynamoDbEnhancedClient enhancedClient;

    @Test
    void testCustomerCRUDOperations() {
        // Test implementation
    }
}
```

For detailed testing strategies, see [Testing Strategies](references/testing-strategies.md).

## Best Practices

- **Use Enhanced Client**: Type-safe operations with less boilerplate
- **Design partition keys for even distribution**: Avoid hot partitions
- **Prefer queries over scans**: Use GSIs for access patterns
- **Batch in chunks of 25/100**: BatchGetItem limits to 100, BatchWriteItem to 25 per table
- **Handle partial failures**: Implement retry with exponential backoff for `ProvisionedThroughputExceeded`
- **Use conditional writes**: Prevent race conditions with `attribute_not_exists(pk)`

## Examples

### Complete CRUD Repository
```java
@Repository
public class UserRepository {

    private final DynamoDbTable<User> userTable;

    public UserRepository(DynamoDbEnhancedClient enhancedClient) {
        this.userTable = enhancedClient.table("Users", TableSchema.fromBean(User.class));
    }

    public User save(User user) {
        userTable.putItem(user);
        return user;
    }

    public Optional<User> findById(String userId) {
        Key key = Key.builder().partitionValue(userId).build();
        return Optional.ofNullable(userTable.getItem(key));
    }

    public void deleteById(String userId) {
        userTable.deleteItem(Key.builder().partitionValue(userId).build());
    }
}
```

### Conditional Write with Retry
```java
public boolean createIfNotExists(User user) {
    PutItemEnhancedRequest<User> request = PutItemEnhancedRequest.builder(User.class)
        .item(user)
        .conditionExpression("attribute_not_exists(userId)")
        .build();

    try {
        userTable.putItemWithRequest(request);
        return true;
    } catch (ConditionalCheckFailedException e) {
        return false; // Item already exists
    }
}
```

## Constraints and Warnings

- **Item Size Limit**: DynamoDB items limited to 400KB
- **Partition Key Design**: Poor design causes hot partitions
- **Batch Limits**: BatchGetItem max 100, BatchWriteItem max 25 items per table
- **Transaction Costs**: Transactions cost 2x read/write capacity units
- **Scan Operations**: Scans consume large amounts of read capacity; use only when necessary

## References

- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [AWS SDK for Java Documentation](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/)
- [DynamoDB Examples](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2/example_code/dynamodb)
- [LocalStack for Testing](https://docs.localstack.cloud/user-guide/aws/)

For detailed implementations, see the references folder:
- [Entity Mapping Reference](references/entity-mapping.md)
- [Advanced Operations Reference](references/advanced-operations.md)
- [Spring Boot Integration Reference](references/spring-boot-integration.md)
- [Testing Strategies](references/testing-strategies.md)
