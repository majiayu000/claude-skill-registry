---
name: spring-boot-jpa-repository
description: Guide for implementing Spring Data JPA repositories with best practices for queries, transactions, and data access patterns. Use this when creating or modifying data access layer code.
---

# Spring Data JPA Repository Best Practices

Follow these practices for efficient and maintainable data access.

## Repository Interface

```java
@Repository
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    
    // Query derivation - Spring generates the query
    Optional<Customer> findByEmail(String email);
    
    List<Customer> findByGuestFalse();
    
    List<Customer> findByNameContainingIgnoreCase(String name);
    
    boolean existsByEmail(String email);
    
    // Pagination support
    Page<Customer> findByGuestFalse(Pageable pageable);
}
```

## Custom Queries with @Query

```java
@Repository
public interface AppointmentRepository extends JpaRepository<Appointment, Long> {
    
    // JPQL query
    @Query("SELECT a FROM Appointment a WHERE a.customer.id = :customerId AND a.status = :status")
    List<Appointment> findByCustomerAndStatus(
        @Param("customerId") Long customerId, 
        @Param("status") String status
    );
    
    // Native query (use sparingly)
    @Query(value = "SELECT * FROM appointments WHERE appointment_time BETWEEN ?1 AND ?2", 
           nativeQuery = true)
    List<Appointment> findByDateRange(LocalDateTime start, LocalDateTime end);
    
    // Join fetch to avoid N+1
    @Query("SELECT a FROM Appointment a " +
           "LEFT JOIN FETCH a.customer " +
           "LEFT JOIN FETCH a.employee " +
           "WHERE a.id = :id")
    Optional<Appointment> findByIdWithDetails(@Param("id") Long id);
    
    // Aggregate queries
    @Query("SELECT COUNT(a) FROM Appointment a WHERE a.employee.id = :employeeId AND a.status = 'COMPLETED'")
    long countCompletedByEmployee(@Param("employeeId") Long employeeId);
}
```

## Modifying Queries

```java
@Repository
public interface AppointmentRepository extends JpaRepository<Appointment, Long> {
    
    @Modifying
    @Query("UPDATE Appointment a SET a.status = :status WHERE a.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") String status);
    
    @Modifying
    @Query("DELETE FROM Appointment a WHERE a.status = 'CANCELLED' AND a.appointmentTime < :before")
    int deleteCancelledBefore(@Param("before") LocalDateTime before);
}
```

## Projections

```java
// Interface projection - only selected fields
public interface CustomerSummary {
    Long getId();
    String getName();
    String getEmail();
}

// DTO projection - full control
public record CustomerDTO(Long id, String name, String email) {}

@Repository
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    
    // Interface projection
    List<CustomerSummary> findAllProjectedBy();
    
    // DTO projection with JPQL
    @Query("SELECT new com.salonhub.api.customer.dto.CustomerDTO(c.id, c.name, c.email) FROM Customer c")
    List<CustomerDTO> findAllAsDTO();
    
    // Dynamic projection
    <T> List<T> findByGuestFalse(Class<T> type);
}
```

## Entity Graphs

```java
@Entity
@NamedEntityGraph(
    name = "Appointment.withDetails",
    attributeNodes = {
        @NamedAttributeNode("customer"),
        @NamedAttributeNode("employee"),
        @NamedAttributeNode("serviceType")
    }
)
public class Appointment {
    // fields
}

@Repository
public interface AppointmentRepository extends JpaRepository<Appointment, Long> {
    
    @EntityGraph("Appointment.withDetails")
    Optional<Appointment> findById(Long id);
    
    @EntityGraph(attributePaths = {"customer", "employee"})
    List<Appointment> findByStatus(String status);
}
```

## Specifications for Dynamic Queries

```java
public class AppointmentSpecifications {
    
    public static Specification<Appointment> hasStatus(String status) {
        return (root, query, cb) -> 
            status == null ? null : cb.equal(root.get("status"), status);
    }
    
    public static Specification<Appointment> hasCustomer(Long customerId) {
        return (root, query, cb) -> 
            customerId == null ? null : cb.equal(root.get("customer").get("id"), customerId);
    }
    
    public static Specification<Appointment> hasDateBetween(LocalDateTime start, LocalDateTime end) {
        return (root, query, cb) -> {
            if (start == null && end == null) return null;
            if (start == null) return cb.lessThanOrEqualTo(root.get("appointmentTime"), end);
            if (end == null) return cb.greaterThanOrEqualTo(root.get("appointmentTime"), start);
            return cb.between(root.get("appointmentTime"), start, end);
        };
    }
}

// Usage
@Service
public class AppointmentService {
    
    public List<Appointment> search(String status, Long customerId, LocalDateTime start, LocalDateTime end) {
        Specification<Appointment> spec = Specification
            .where(AppointmentSpecifications.hasStatus(status))
            .and(AppointmentSpecifications.hasCustomer(customerId))
            .and(AppointmentSpecifications.hasDateBetween(start, end));
        
        return appointmentRepository.findAll(spec);
    }
}
```

## Transaction Management

```java
@Service
@Transactional(readOnly = true)  // Default read-only
public class AppointmentService {
    
    private final AppointmentRepository appointmentRepository;
    private final QueueService queueService;
    
    // Read operation - uses class-level readOnly=true
    public AppointmentResponseDTO findById(Long id) {
        return appointmentRepository.findById(id)
            .map(appointmentMapper::toResponseDTO)
            .orElseThrow(() -> new ResourceNotFoundException("Appointment not found"));
    }
    
    // Write operation - override to allow writes
    @Transactional
    public AppointmentResponseDTO create(AppointmentRequestDTO request) {
        Appointment appointment = appointmentMapper.toEntity(request);
        appointment = appointmentRepository.save(appointment);
        return appointmentMapper.toResponseDTO(appointment);
    }
    
    // Complex transaction spanning multiple services
    @Transactional(rollbackFor = Exception.class)
    public void completeAppointment(Long id) {
        Appointment appointment = appointmentRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Appointment not found"));
        
        appointment.setStatus("COMPLETED");
        appointmentRepository.save(appointment);
        
        // If this fails, entire transaction rolls back
        queueService.removeFromQueue(appointment.getCustomer().getId());
    }
}
```

## Optimistic Locking

```java
@Entity
public class Appointment {
    @Id
    private Long id;
    
    @Version
    private Long version;
    
    // Other fields
}

// Handling optimistic lock exception
@Service
public class AppointmentService {
    
    @Transactional
    @Retryable(value = OptimisticLockException.class, maxAttempts = 3)
    public void updateAppointment(Long id, AppointmentUpdateDTO dto) {
        Appointment appointment = appointmentRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Appointment not found"));
        
        // Update fields
        appointmentMapper.updateEntity(dto, appointment);
        
        // Save will throw OptimisticLockException if version mismatch
        appointmentRepository.save(appointment);
    }
}
```

## Auditing

```java
@Configuration
@EnableJpaAuditing
public class JpaConfig {
    
    @Bean
    public AuditorAware<String> auditorProvider() {
        return () -> Optional.ofNullable(SecurityContextHolder.getContext())
            .map(SecurityContext::getAuthentication)
            .map(Authentication::getName);
    }
}

@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {
    
    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    private LocalDateTime updatedAt;
    
    @CreatedBy
    @Column(updatable = false)
    private String createdBy;
    
    @LastModifiedBy
    private String updatedBy;
}

@Entity
public class Appointment extends BaseEntity {
    // Entity-specific fields
}
```

## Query Hints for Performance

```java
@Repository
public interface AppointmentRepository extends JpaRepository<Appointment, Long> {
    
    @QueryHints(value = {
        @QueryHint(name = "org.hibernate.fetchSize", value = "50"),
        @QueryHint(name = "org.hibernate.readOnly", value = "true"),
        @QueryHint(name = "org.hibernate.cacheable", value = "true")
    })
    @Query("SELECT a FROM Appointment a WHERE a.status = :status")
    List<Appointment> findByStatusOptimized(@Param("status") String status);
}
```

## Repository Checklist

- [ ] Extend JpaRepository for full CRUD support
- [ ] Use query derivation for simple queries
- [ ] Use @Query for complex JPQL queries
- [ ] Add JOIN FETCH or @EntityGraph to prevent N+1
- [ ] Use projections when full entities aren't needed
- [ ] Implement Specification for dynamic queries
- [ ] Configure transactions appropriately
- [ ] Add @Version for optimistic locking where needed
- [ ] Enable auditing for tracking changes
