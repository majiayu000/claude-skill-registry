---
name: unit-test-caching
description: Provides patterns for unit testing caching behavior using Spring Cache annotations (@Cacheable, @CachePut, @CacheEvict). Use when validating cache configuration and cache hit/miss scenarios.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Unit Testing Spring Caching

## Overview

This skill provides patterns for unit testing Spring caching annotations (@Cacheable, @CacheEvict, @CachePut) without full Spring context. It covers testing cache behavior, hits/misses, invalidation strategies, cache key generation, and conditional caching using in-memory cache managers.

## When to Use

Use this skill when:
- Testing @Cacheable method caching
- Testing @CacheEvict cache invalidation
- Testing @CachePut cache updates
- Verifying cache key generation
- Testing conditional caching
- Want fast caching tests without Redis or cache infrastructure

## Instructions

1. **Use in-memory CacheManager**: Use ConcurrentMapCacheManager for tests instead of Redis or other external caches
2. **Verify repository call counts**: Use `times(n)` to verify cache hits/misses by counting repository invocations
3. **Test both cache and eviction scenarios**: Verify data is cached on first call and evicted when appropriate
4. **Test cache key generation**: Ensure SpEL expressions in `@Cacheable(key = "...")` produce correct keys
5. **Test conditional caching**: Verify `unless` and `condition` parameters work correctly
6. **Clear cache between tests**: Reset cache state in @BeforeEach or use @DirtiesContext
7. **Mock service dependencies**: Use mocks for repositories and other services the caching layer uses
8. **Verify cache behavior explicitly**: Don't rely on timing; verify actual cache hit/miss behavior

## Examples

## Setup: Caching Testing

### Maven
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.mockito</groupId>
  <artifactId>mockito-core</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.assertj</groupId>
  <artifactId>assertj-core</artifactId>
  <scope>test</scope>
</dependency>
```

### Gradle
```kotlin
dependencies {
  implementation("org.springframework.boot:spring-boot-starter-cache")
  testImplementation("org.springframework.boot:spring-boot-starter-test")
  testImplementation("org.mockito:mockito-core")
  testImplementation("org.assertj:assertj-core")
}
```

## Basic Pattern: Testing @Cacheable

### Cache Hit and Miss Behavior

```java
// Service with caching
@Service
public class UserService {

  private final UserRepository userRepository;

  public UserService(UserRepository userRepository) {
    this.userRepository = userRepository;
  }

  @Cacheable("users")
  public User getUserById(Long id) {
    return userRepository.findById(id).orElse(null);
  }
}

// Test caching behavior
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.concurrent.ConcurrentMapCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.*;

@Configuration
@EnableCaching
class CacheTestConfig {
  @Bean
  public CacheManager cacheManager() {
    return new ConcurrentMapCacheManager("users");
  }
}

class UserServiceCachingTest {

  private UserRepository userRepository;
  private UserService userService;
  private CacheManager cacheManager;

  @BeforeEach
  void setUp() {
    userRepository = mock(UserRepository.class);
    cacheManager = new ConcurrentMapCacheManager("users");
    userService = new UserService(userRepository);
  }

  @Test
  void shouldCacheUserAfterFirstCall() {
    User user = new User(1L, "Alice");
    when(userRepository.findById(1L)).thenReturn(Optional.of(user));

    User firstCall = userService.getUserById(1L);
    User secondCall = userService.getUserById(1L);

    assertThat(firstCall).isEqualTo(secondCall);
    verify(userRepository, times(1)).findById(1L); // Called only once due to cache
  }

  @Test
  void shouldReturnCachedValueOnSecondCall() {
    User user = new User(1L, "Alice");
    when(userRepository.findById(1L)).thenReturn(Optional.of(user));

    userService.getUserById(1L); // First call - hits database
    User cachedResult = userService.getUserById(1L); // Second call - hits cache

    assertThat(cachedResult).isEqualTo(user);
    verify(userRepository, times(1)).findById(1L);
  }
}
```

## Testing @CacheEvict

### Cache Invalidation

```java
@Service
public class ProductService {

  private final ProductRepository productRepository;

  public ProductService(ProductRepository productRepository) {
    this.productRepository = productRepository;
  }

  @Cacheable("products")
  public Product getProductById(Long id) {
    return productRepository.findById(id).orElse(null);
  }

  @CacheEvict("products")
  public void deleteProduct(Long id) {
    productRepository.deleteById(id);
  }

  @CacheEvict(value = "products", allEntries = true)
  public void clearAllProducts() {
    // Clear entire cache
  }
}

class ProductCacheEvictTest {

  private ProductRepository productRepository;
  private ProductService productService;
  private CacheManager cacheManager;

  @BeforeEach
  void setUp() {
    productRepository = mock(ProductRepository.class);
    cacheManager = new ConcurrentMapCacheManager("products");
    productService = new ProductService(productRepository);
  }

  @Test
  void shouldEvictProductFromCacheWhenDeleted() {
    Product product = new Product(1L, "Laptop", 999.99);
    when(productRepository.findById(1L)).thenReturn(Optional.of(product));

    productService.getProductById(1L); // Cache the product

    productService.deleteProduct(1L); // Evict from cache

    User cachedAfterEvict = userService.getUserById(1L);
    
    // After eviction, repository should be called again
    verify(productRepository, times(2)).findById(1L);
  }

  @Test
  void shouldClearAllEntriesFromCache() {
    Product product1 = new Product(1L, "Laptop", 999.99);
    Product product2 = new Product(2L, "Mouse", 29.99);
    when(productRepository.findById(1L)).thenReturn(Optional.of(product1));
    when(productRepository.findById(2L)).thenReturn(Optional.of(product2));

    productService.getProductById(1L);
    productService.getProductById(2L);

    productService.clearAllProducts(); // Clear all cache entries

    productService.getProductById(1L);
    productService.getProductById(2L);

    // Repository called twice for each product
    verify(productRepository, times(2)).findById(1L);
    verify(productRepository, times(2)).findById(2L);
  }
}
```

## Testing @CachePut

### Cache Update

```java
@Service
public class OrderService {

  private final OrderRepository orderRepository;

  public OrderService(OrderRepository orderRepository) {
    this.orderRepository = orderRepository;
  }

  @Cacheable("orders")
  public Order getOrder(Long id) {
    return orderRepository.findById(id).orElse(null);
  }

  @CachePut(value = "orders", key = "#order.id")
  public Order updateOrder(Order order) {
    return orderRepository.save(order);
  }
}

class OrderCachePutTest {

  private OrderRepository orderRepository;
  private OrderService orderService;

  @BeforeEach
  void setUp() {
    orderRepository = mock(OrderRepository.class);
    orderService = new OrderService(orderRepository);
  }

  @Test
  void shouldUpdateCacheWhenOrderIsUpdated() {
    Order originalOrder = new Order(1L, "Pending", 100.0);
    Order updatedOrder = new Order(1L, "Shipped", 100.0);

    when(orderRepository.findById(1L)).thenReturn(Optional.of(originalOrder));
    when(orderRepository.save(updatedOrder)).thenReturn(updatedOrder);

    orderService.getOrder(1L);
    Order result = orderService.updateOrder(updatedOrder);

    assertThat(result.getStatus()).isEqualTo("Shipped");
    
    // Next call should return updated version from cache
    Order cachedOrder = orderService.getOrder(1L);
    assertThat(cachedOrder.getStatus()).isEqualTo("Shipped");
  }
}
```

## Testing Conditional Caching

### Cache with Conditions

```java
@Service
public class DataService {

  private final DataRepository dataRepository;

  public DataService(DataRepository dataRepository) {
    this.dataRepository = dataRepository;
  }

  @Cacheable(value = "data", unless = "#result == null")
  public Data getData(Long id) {
    return dataRepository.findById(id).orElse(null);
  }

  @Cacheable(value = "users", condition = "#id > 0")
  public User getUser(Long id) {
    return userRepository.findById(id).orElse(null);
  }
}

class ConditionalCachingTest {

  @Test
  void shouldNotCacheNullResults() {
    DataRepository dataRepository = mock(DataRepository.class);
    when(dataRepository.findById(999L)).thenReturn(Optional.empty());

    DataService service = new DataService(dataRepository);

    service.getData(999L);
    service.getData(999L);

    // Should call repository twice because null results are not cached
    verify(dataRepository, times(2)).findById(999L);
  }

  @Test
  void shouldNotCacheWhenConditionIsFalse() {
    UserRepository userRepository = mock(UserRepository.class);
    User user = new User(1L, "Alice");
    when(userRepository.findById(-1L)).thenReturn(Optional.of(user));

    DataService service = new DataService(null);

    service.getUser(-1L);
    service.getUser(-1L);

    // Should call repository twice because id <= 0 doesn't match condition
    verify(userRepository, times(2)).findById(-1L);
  }
}
```

## Testing Cache Keys

### Verify Cache Key Generation

```java
@Service
public class InventoryService {

  private final InventoryRepository inventoryRepository;

  public InventoryService(InventoryRepository inventoryRepository) {
    this.inventoryRepository = inventoryRepository;
  }

  @Cacheable(value = "inventory", key = "#productId + '-' + #warehouseId")
  public InventoryItem getInventory(Long productId, Long warehouseId) {
    return inventoryRepository.findByProductAndWarehouse(productId, warehouseId);
  }
}

class CacheKeyTest {

  @Test
  void shouldGenerateCorrectCacheKey() {
    InventoryRepository repository = mock(InventoryRepository.class);
    InventoryItem item = new InventoryItem(1L, 1L, 100);
    when(repository.findByProductAndWarehouse(1L, 1L)).thenReturn(item);

    InventoryService service = new InventoryService(repository);

    service.getInventory(1L, 1L); // Cache: "1-1"
    service.getInventory(1L, 1L); // Hit cache: "1-1"
    service.getInventory(2L, 1L); // Miss cache: "2-1"

    verify(repository, times(2)).findByProductAndWarehouse(any(), any());
  }
}
```

## Best Practices

- **Use in-memory CacheManager** for unit tests
- **Verify repository calls** to confirm cache hits/misses
- **Test both positive and negative** cache scenarios
- **Test cache invalidation** thoroughly
- **Test conditional caching** with various conditions
- **Keep cache configuration simple** in tests
- **Mock dependencies** that services use

## Common Pitfalls

- Testing actual cache infrastructure instead of caching logic
- Not verifying repository call counts
- Forgetting to test cache eviction
- Not testing conditional caching
- Not resetting cache between tests

## Constraints and Warnings

- **@Cacheable requires a proxy**: Spring's caching works via proxies; direct method calls bypass caching
- **Cache key collisions**: Be aware that different parameters can produce the same cache key if key generation is not specific
- **Serialization requirements**: Cached objects must be serializable when using distributed caches
- **Memory usage**: In-memory caches can consume significant memory; consider TTL and max-size settings
- **@CachePut vs @Cacheable**: @CachePut always executes the method, while @Cacheable skips execution on cache hit
- **Null caching**: By default, null results are cached unless `unless = "#result == null"` is specified
- **Thread safety**: Cache operations should be thread-safe; verify behavior under concurrent access

## Troubleshooting

**Cache not working in tests**: Ensure `@EnableCaching` is in test configuration.

**Wrong cache key generated**: Use `SpEL` syntax correctly in `@Cacheable(key = "...")`.

**Cache not evicting**: Verify `@CacheEvict` key matches stored key exactly.

## References

- [Spring Caching Documentation](https://docs.spring.io/spring-framework/docs/current/reference/html/integration.html#cache)
- [Spring Cache Abstractions](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/cache/annotation/Cacheable.html)
- [SpEL in Caching](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions)
