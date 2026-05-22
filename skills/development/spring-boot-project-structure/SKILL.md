---
name: spring-boot-project-structure
description: Guide for creating proper Spring Boot project structure following domain-driven design. Use this when creating new features, modules, or refactoring existing code.
---

# Spring Boot Project Structure Best Practices

When creating new features or modules in a Spring Boot application, follow this domain-driven structure:

## Package Organization

```
com.salonhub.api/
├── Application.java              # Main application class
├── config/                       # Global configuration
├── common/                       # Shared utilities and components
│   ├── exception/               # Custom exceptions
│   ├── util/                    # Utility classes
│   └── dto/                     # Shared DTOs
├── auth/                        # Authentication/Authorization
│   ├── config/
│   ├── controller/
│   ├── service/
│   └── model/
└── [domain]/                    # Feature-specific packages
    ├── controller/              # REST controllers
    ├── service/                 # Business logic
    ├── repository/              # Data access
    ├── model/                   # JPA entities
    ├── dto/                     # Request/Response DTOs
    └── mapper/                  # Entity-DTO mappers
```

## Creating a New Domain/Feature

1. **Create the package structure**:
   ```
   src/main/java/com/salonhub/api/[feature]/
   ├── controller/
   │   └── [Feature]Controller.java
   ├── service/
   │   └── [Feature]Service.java
   ├── repository/
   │   └── [Feature]Repository.java
   ├── model/
   │   └── [Feature].java
   ├── dto/
   │   ├── [Feature]RequestDTO.java
   │   └── [Feature]ResponseDTO.java
   └── mapper/
       └── [Feature]Mapper.java
   ```

2. **Follow proper layering**:
   - **Controller Layer**: Only handles HTTP requests/responses, validation
   - **Service Layer**: Contains ALL business logic
   - **Repository Layer**: Only data access operations
   - **Model Layer**: Defines JPA entities

## Key Principles

1. **Single Responsibility**: Each class has one reason to change
2. **One-way Dependencies**: Controller → Service → Repository (never reverse)
3. **No Circular Dependencies**: If detected, refactor immediately
4. **Use Interfaces**: For services that may have multiple implementations
5. **Keep Controllers Thin**: Delegate all logic to services

## Example Structure

```java
@RestController
@RequestMapping("/api/appointments")
public class AppointmentController {
    private final AppointmentService appointmentService;
    
    public AppointmentController(AppointmentService appointmentService) {
        this.appointmentService = appointmentService;
    }
    
    @GetMapping("/{id}")
    public AppointmentResponseDTO getAppointment(@PathVariable Long id) {
        return appointmentService.findById(id);
    }
}
```

## Checklist for New Features

- [ ] Create proper package structure under `src/main/java/com/salonhub/api/[feature]/`
- [ ] Create Entity in `model/` package
- [ ] Create Repository interface extending `JpaRepository`
- [ ] Create Service class with constructor injection
- [ ] Create Request/Response DTOs in `dto/` package
- [ ] Create Mapper class for entity-DTO conversion
- [ ] Create Controller with proper REST endpoints
- [ ] Add corresponding test packages mirroring main structure
