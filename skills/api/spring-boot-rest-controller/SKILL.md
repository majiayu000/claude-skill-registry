---
name: spring-boot-rest-controller
description: Guide for creating RESTful controllers with proper request/response handling, validation, and documentation. Use this when implementing new API endpoints or refactoring existing controllers.
---

# Spring Boot REST Controller Best Practices

Follow these practices for implementing RESTful APIs.

## Controller Structure

```java
@RestController
@RequestMapping("/api/appointments")
@Tag(name = "Appointments", description = "Appointment management endpoints")
public class AppointmentController {

    private final AppointmentService appointmentService;

    // Constructor injection
    public AppointmentController(AppointmentService appointmentService) {
        this.appointmentService = appointmentService;
    }

    // Endpoints follow CRUD order: Create, Read, Update, Delete
}
```

## HTTP Methods and Status Codes

```java
@RestController
@RequestMapping("/api/appointments")
public class AppointmentController {

    // GET all - Returns 200 OK
    @GetMapping
    public List<AppointmentResponseDTO> getAll() {
        return appointmentService.findAll();
    }

    // GET by ID - Returns 200 OK or 404 Not Found
    @GetMapping("/{id}")
    public AppointmentResponseDTO getById(@PathVariable Long id) {
        return appointmentService.findById(id);
    }

    // POST create - Returns 201 Created
    @PostMapping
    public ResponseEntity<AppointmentResponseDTO> create(
            @Valid @RequestBody AppointmentRequestDTO request) {
        AppointmentResponseDTO created = appointmentService.create(request);
        URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(created.getId())
            .toUri();
        return ResponseEntity.created(location).body(created);
    }

    // PUT update - Returns 200 OK or 404 Not Found
    @PutMapping("/{id}")
    public AppointmentResponseDTO update(
            @PathVariable Long id,
            @Valid @RequestBody AppointmentRequestDTO request) {
        return appointmentService.update(id, request);
    }

    // PATCH partial update - Returns 200 OK or 404 Not Found
    @PatchMapping("/{id}/status")
    public AppointmentResponseDTO updateStatus(
            @PathVariable Long id,
            @RequestParam String status) {
        return appointmentService.updateStatus(id, status);
    }

    // DELETE - Returns 204 No Content
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        appointmentService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

## Request Validation

```java
// Request DTO with validation
public class AppointmentRequestDTO {

    @NotNull(message = "Customer ID is required")
    private Long customerId;

    @NotNull(message = "Employee ID is required")
    private Long employeeId;

    @NotNull(message = "Service type ID is required")
    private Long serviceTypeId;

    @NotNull(message = "Appointment time is required")
    @FutureOrPresent(message = "Appointment time must be in the future")
    private LocalDateTime appointmentTime;

    @Size(max = 500, message = "Notes cannot exceed 500 characters")
    private String notes;

    // Getters and setters
}

// Controller with validation
@PostMapping
public ResponseEntity<AppointmentResponseDTO> create(
        @Valid @RequestBody AppointmentRequestDTO request) {
    // Request is automatically validated
    return ResponseEntity.status(HttpStatus.CREATED)
        .body(appointmentService.create(request));
}
```

## Pagination and Sorting

```java
@GetMapping
public Page<AppointmentResponseDTO> getAll(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(defaultValue = "appointmentTime") String sortBy,
        @RequestParam(defaultValue = "asc") String sortDir) {
    
    Sort sort = sortDir.equalsIgnoreCase("desc") 
        ? Sort.by(sortBy).descending() 
        : Sort.by(sortBy).ascending();
    
    Pageable pageable = PageRequest.of(page, size, sort);
    return appointmentService.findAll(pageable);
}
```

## Filtering and Search

```java
@GetMapping("/search")
public List<AppointmentResponseDTO> search(
        @RequestParam(required = false) Long customerId,
        @RequestParam(required = false) Long employeeId,
        @RequestParam(required = false) String status,
        @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date) {
    
    return appointmentService.search(customerId, employeeId, status, date);
}
```

## Response DTOs

```java
// Response DTO - what API returns
public class AppointmentResponseDTO {
    private Long id;
    private CustomerSummaryDTO customer;
    private EmployeeSummaryDTO employee;
    private ServiceTypeSummaryDTO serviceType;
    private LocalDateTime appointmentTime;
    private String status;
    private String notes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // Getters and setters
}

// Nested summary DTO - avoid circular references
public class CustomerSummaryDTO {
    private Long id;
    private String name;
    private String phone;
    
    // Getters and setters
}
```

## OpenAPI Documentation

```java
@RestController
@RequestMapping("/api/appointments")
@Tag(name = "Appointments", description = "Appointment management endpoints")
public class AppointmentController {

    @Operation(summary = "Get appointment by ID", description = "Returns a single appointment")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Found the appointment",
            content = @Content(schema = @Schema(implementation = AppointmentResponseDTO.class))),
        @ApiResponse(responseCode = "404", description = "Appointment not found",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @GetMapping("/{id}")
    public AppointmentResponseDTO getById(
            @Parameter(description = "ID of appointment to return") @PathVariable Long id) {
        return appointmentService.findById(id);
    }

    @Operation(summary = "Create new appointment")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Appointment created"),
        @ApiResponse(responseCode = "400", description = "Invalid input"),
        @ApiResponse(responseCode = "404", description = "Referenced entity not found")
    })
    @PostMapping
    public ResponseEntity<AppointmentResponseDTO> create(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                description = "Appointment to create",
                required = true,
                content = @Content(schema = @Schema(implementation = AppointmentRequestDTO.class)))
            @Valid @RequestBody AppointmentRequestDTO request) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(appointmentService.create(request));
    }
}
```

## Security Annotations

```java
@RestController
@RequestMapping("/api/appointments")
public class AppointmentController {

    // Admin only
    @PreAuthorize("hasRole('ADMIN')")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        appointmentService.delete(id);
        return ResponseEntity.noContent().build();
    }

    // Front desk and above
    @PreAuthorize("hasRole('FRONT_DESK')")
    @PostMapping
    public ResponseEntity<AppointmentResponseDTO> create(@Valid @RequestBody AppointmentRequestDTO request) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(appointmentService.create(request));
    }

    // Self-access or higher role
    @PreAuthorize("hasRole('MANAGER') or #customerId == authentication.principal.customerId")
    @GetMapping("/customer/{customerId}")
    public List<AppointmentResponseDTO> getByCustomer(@PathVariable Long customerId) {
        return appointmentService.findByCustomerId(customerId);
    }
}
```

## Error Handling

```java
// Let GlobalExceptionHandler handle exceptions
@GetMapping("/{id}")
public AppointmentResponseDTO getById(@PathVariable Long id) {
    return appointmentService.findById(id);
    // Service throws ResourceNotFoundException if not found
    // GlobalExceptionHandler converts to 404 response
}

// Custom error response format
public class ErrorResponse {
    private String code;
    private String message;
    private LocalDateTime timestamp;
    private Map<String, String> details;
    
    // Constructor, getters
}
```

## Response Headers

```java
@GetMapping("/{id}")
public ResponseEntity<AppointmentResponseDTO> getById(@PathVariable Long id) {
    AppointmentResponseDTO appointment = appointmentService.findById(id);
    
    return ResponseEntity.ok()
        .header("X-Request-Id", UUID.randomUUID().toString())
        .header("Cache-Control", "max-age=3600")
        .body(appointment);
}
```

## Controller Checklist

- [ ] Use meaningful URL paths (`/api/appointments`, not `/api/getAppointments`)
- [ ] Use correct HTTP methods (GET, POST, PUT, PATCH, DELETE)
- [ ] Return appropriate status codes (200, 201, 204, 400, 404, etc.)
- [ ] Validate all input with `@Valid`
- [ ] Add security annotations (`@PreAuthorize`)
- [ ] Document with OpenAPI annotations
- [ ] Keep controllers thin - delegate to services
- [ ] Use DTOs for requests and responses
- [ ] Support pagination for list endpoints
- [ ] Add proper error handling
