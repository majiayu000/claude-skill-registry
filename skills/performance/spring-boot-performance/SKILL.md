---
name: spring-boot-performance
description: Guide for optimizing Spring Boot application performance including caching, pagination, async processing, and JPA optimization. Use this when addressing performance issues or implementing high-traffic features.
---

# Spring Boot Performance Optimization

Follow these practices to optimize application performance.

## Pagination for Large Datasets

**NEVER load entire tables into memory:**

```java
// ❌ WRONG - Can cause OutOfMemoryError
List<User> allUsers = userRepository.findAll();

// ✅ CORRECT - Use pagination
@GetMapping("/users")
public Page<UserDTO> getUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(defaultValue = "id") String sortBy) {

    Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
    return userRepository.findAll(pageable)
        .map(userMapper::toDto);
}
```

## Projections for Partial Data

**Use projections when you don't need full entities:**

```java
// Interface projection
public interface UserSummary {
    Long getId();
    String getName();
    String getEmail();
}

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<UserSummary> findAllProjectedBy();
    
    @Query("SELECT u.id as id, u.name as name FROM User u")
    List<UserSummary> findUserSummaries();
}
```

## Avoiding N+1 Query Problem

```java
// ❌ WRONG - N+1 queries
List<Order> orders = orderRepository.findAll();
for (Order order : orders) {
    // This causes N additional queries
    List<OrderItem> items = order.getItems();
}

// ✅ CORRECT - Use JOIN FETCH
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    @Query("SELECT o FROM Order o LEFT JOIN FETCH o.items")
    List<Order> findAllWithItems();
    
    @EntityGraph(attributePaths = {"items", "customer"})
    List<Order> findAll();
}
```

## Caching Configuration

```java
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        cacheManager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(1000)
            .expireAfterWrite(Duration.ofMinutes(10))
            .recordStats());
        return cacheManager;
    }
}

@Service
public class ServiceTypeService {

    @Cacheable(value = "serviceTypes", key = "#id")
    public ServiceType getServiceType(Long id) {
        return serviceTypeRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Service type not found"));
    }

    @CacheEvict(value = "serviceTypes", key = "#serviceType.id")
    public ServiceType updateServiceType(ServiceType serviceType) {
        return serviceTypeRepository.save(serviceType);
    }

    @CacheEvict(value = "serviceTypes", allEntries = true)
    public void clearCache() {
        // Clears entire cache
    }
}
```

## Async Processing

```java
@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(25);
        executor.setThreadNamePrefix("Async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}

@Service
public class NotificationService {

    @Async("taskExecutor")
    public CompletableFuture<Void> sendEmailNotification(String email, String message) {
        // Long-running email sending operation
        // This runs in a separate thread
        return CompletableFuture.completedFuture(null);
    }
}

// Usage in controller
@PostMapping("/appointments")
public AppointmentDTO createAppointment(@RequestBody AppointmentRequest request) {
    AppointmentDTO appointment = appointmentService.create(request);
    
    // Fire and forget - doesn't block response
    notificationService.sendEmailNotification(
        appointment.getCustomerEmail(),
        "Your appointment is confirmed"
    );
    
    return appointment;
}
```

## Connection Pool Configuration

```yaml
# application.yml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      idle-timeout: 30000
      connection-timeout: 20000
      max-lifetime: 1800000
      pool-name: SalonHubPool
```

## JPA Optimization

```yaml
# application.yml
spring:
  jpa:
    properties:
      hibernate:
        # Batch processing
        jdbc:
          batch_size: 50
        order_inserts: true
        order_updates: true
        
        # Second-level cache (optional)
        cache:
          use_second_level_cache: true
          region:
            factory_class: org.hibernate.cache.jcache.JCacheRegionFactory
        
        # Query hints
        default_batch_fetch_size: 25
```

## Batch Processing

```java
@Service
@Transactional
public class BulkImportService {

    @PersistenceContext
    private EntityManager entityManager;

    public void bulkInsert(List<Customer> customers) {
        int batchSize = 50;
        for (int i = 0; i < customers.size(); i++) {
            entityManager.persist(customers.get(i));
            if (i > 0 && i % batchSize == 0) {
                entityManager.flush();
                entityManager.clear();
            }
        }
        entityManager.flush();
        entityManager.clear();
    }
}
```

## Lazy Loading Best Practices

```java
@Entity
public class Order {
    @Id
    private Long id;
    
    // Lazy by default for collections
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderItem> items;
    
    // Consider lazy for large objects
    @Basic(fetch = FetchType.LAZY)
    @Lob
    private String description;
}

// Initialize lazy collections when needed
@Transactional(readOnly = true)
public Order getOrderWithItems(Long id) {
    Order order = orderRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("Order not found"));
    // Force initialization within transaction
    Hibernate.initialize(order.getItems());
    return order;
}
```

## Response Compression

```yaml
# application.yml
server:
  compression:
    enabled: true
    mime-types: application/json,application/xml,text/html,text/xml,text/plain
    min-response-size: 1024
```

## Index Optimization

```sql
-- Create indexes for frequently queried columns
CREATE INDEX idx_appointments_customer_id ON appointments(customer_id);
CREATE INDEX idx_appointments_employee_id ON appointments(employee_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_time);

-- Composite index for common query patterns
CREATE INDEX idx_appointments_status_date ON appointments(status, appointment_time);
```

## Performance Monitoring

```java
@Aspect
@Component
public class PerformanceLoggingAspect {

    private static final Logger logger = LoggerFactory.getLogger(PerformanceLoggingAspect.class);

    @Around("@annotation(LogExecutionTime)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long duration = System.currentTimeMillis() - start;
        
        logger.info("{} executed in {} ms", joinPoint.getSignature(), duration);
        return result;
    }
}

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LogExecutionTime {}
```

## Performance Checklist

- [ ] Use pagination for all list endpoints
- [ ] Implement caching for frequently accessed, rarely changed data
- [ ] Check for N+1 queries using logging or profiler
- [ ] Use projections when full entities aren't needed
- [ ] Add database indexes for frequently queried columns
- [ ] Configure connection pooling appropriately
- [ ] Use async processing for non-critical operations
- [ ] Enable response compression
- [ ] Monitor slow queries and optimize
