---
name: spring-boot-coding-standards
description: Guide for Spring Boot coding best practices including dependency injection, error handling, and API design. Use this when writing or reviewing Spring Boot code.
---

# Spring Boot Coding Standards

Follow these coding standards when developing Spring Boot applications.

## Constructor Injection (Required)

**ALWAYS use constructor injection instead of field injection:**

```java
// ✅ CORRECT: Constructor injection
@Service
public class AppointmentService {
    private final AppointmentRepository appointmentRepository;
    private final CustomerService customerService;

    public AppointmentService(AppointmentRepository appointmentRepository, 
                              CustomerService customerService) {
        this.appointmentRepository = appointmentRepository;
        this.customerService = customerService;
    }
}

// ❌ WRONG: Field injection
@Service
public class AppointmentService {
    @Autowired
    private AppointmentRepository appointmentRepository;
    
    @Autowired
    private CustomerService customerService;
}
```

## DTOs and Value Objects

**Create immutable DTOs when possible:**

```java
// Request DTO with validation
public class AppointmentRequestDTO {
    @NotNull(message = "Customer ID is required")
    private Long customerId;
    
    @NotNull(message = "Employee ID is required")
    private Long employeeId;
    
    @NotNull(message = "Service type is required")
    private Long serviceTypeId;
    
    @FutureOrPresent(message = "Appointment time must be in the future")
    private LocalDateTime appointmentTime;
    
    // Getters and setters
}

// Response DTO (immutable pattern)
public final class AppointmentResponseDTO {
    private final Long id;
    private final String customerName;
    private final String employeeName;
    private final String serviceType;
    private final LocalDateTime appointmentTime;
    private final String status;
    
    // Constructor and getters only
}
```

## Error Handling

**Implement global exception handling:**

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(ResourceNotFoundException ex) {
        logger.error("Resource not found: {}", ex.getMessage());
        return new ResponseEntity<>(
            new ErrorResponse("NOT_FOUND", ex.getMessage()), 
            HttpStatus.NOT_FOUND
        );
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getFieldErrors().stream()
            .map(FieldError::getDefaultMessage)
            .collect(Collectors.joining(", "));
        return new ResponseEntity<>(
            new ErrorResponse("VALIDATION_ERROR", message), 
            HttpStatus.BAD_REQUEST
        );
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex) {
        logger.error("Unexpected error", ex);
        return new ResponseEntity<>(
            new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"), 
            HttpStatus.INTERNAL_SERVER_ERROR
        );
    }
}
```

## Optional Handling

**Never use `.get()` without checking:**

```java
// ✅ CORRECT
public User getUser(Long id) {
    return userRepository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("User not found: " + id));
}

// ❌ WRONG - Can throw NoSuchElementException
public User getUser(Long id) {
    return userRepository.findById(id).get();
}
```

## RESTful API Design

**Follow REST conventions:**

```java
@RestController
@RequestMapping("/api/appointments")
public class AppointmentController {

    @GetMapping                              // GET all
    public List<AppointmentDTO> getAll() { }
    
    @GetMapping("/{id}")                     // GET by ID
    public AppointmentDTO getById(@PathVariable Long id) { }
    
    @PostMapping                             // CREATE
    public ResponseEntity<AppointmentDTO> create(@Valid @RequestBody AppointmentRequestDTO dto) {
        AppointmentDTO created = service.create(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    @PutMapping("/{id}")                     // UPDATE
    public AppointmentDTO update(@PathVariable Long id, @Valid @RequestBody AppointmentRequestDTO dto) { }
    
    @DeleteMapping("/{id}")                  // DELETE
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

## Lombok Usage

**Use Lombok judiciously:**

```java
@Data                   // For entities with caution (equals/hashCode issues)
@NoArgsConstructor      // Required for JPA
@AllArgsConstructor     // Useful for testing
@Builder               // For complex object construction
public class Appointment {
    // fields
}

// For DTOs, prefer explicit immutable pattern or:
@Getter
@AllArgsConstructor
public class AppointmentResponseDTO {
    private final Long id;
    private final String name;
}
```

## Input Validation

**Always validate user input:**

```java
@PostMapping
public ResponseEntity<CustomerDTO> createCustomer(
        @Valid @RequestBody CustomerRequest request) {
    // Process validated input
}

public class CustomerRequest {
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be 2-100 characters")
    private String name;

    @Email(message = "Invalid email format")
    private String email;

    @Pattern(regexp = "^\\+?[1-9]\\d{1,14}$", message = "Invalid phone number")
    private String phone;
}
```

## Transaction Management

```java
@Service
@Transactional(readOnly = true)  // Default read-only for safety
public class OrderService {

    @Transactional  // Override for write operations
    public Order placeOrder(OrderRequest request) {
        Order order = new Order();
        // ... set order details
        return orderRepository.save(order);
    }
    
    // Read operation uses class-level readOnly = true
    public Order getOrder(Long id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Order not found"));
    }
}
```
