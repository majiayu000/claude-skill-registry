---
name: hapi-fhir-server
description: Expert guidance for implementing FHIR servers using HAPI FHIR Plain Server framework. Use this skill when creating RESTful FHIR server implementations, implementing resource providers, adding FHIR operations (read, create, update, delete, search, $operations), implementing server interceptors for logging, security, and validation, setting up authentication and authorisation, or configuring FHIR server behaviour. Trigger keywords include "HAPI", "FHIR server", "RestfulServer", "resource provider", "IResourceProvider", "FHIR interceptor", "AuthorizationInterceptor", "FhirContext", "FHIR validation", "FHIR search", "FHIR operation".
---

# HAPI FHIR Plain Server Implementation

## Quick Start

### Basic Server Setup

```java
public class MyFhirServer extends RestfulServer {
    @Override
    protected void initialize() throws ServletException {
        setFhirContext(FhirContext.forR4());
        setResourceProviders(List.of(
            new PatientResourceProvider(),
            new ObservationResourceProvider()
        ));
        registerInterceptor(new ResponseHighlighterInterceptor());
    }
}
```

### Minimal Resource Provider

```java
public class PatientResourceProvider implements IResourceProvider {
    @Override
    public Class<Patient> getResourceType() { return Patient.class; }

    @Read
    public Patient read(@IdParam IdType id) {
        return loadPatient(id.getIdPart());
    }

    @Search
    public List<Patient> search(
            @OptionalParam(name = Patient.SP_FAMILY) StringParam family) {
        return searchPatients(family);
    }
}
```

## Server Architecture

### Component Hierarchy

```
RestfulServer (Servlet)
├── FhirContext (version-specific, expensive to create - reuse)
├── Resource Providers (IResourceProvider per resource type)
├── Plain Providers (cross-resource operations)
├── Interceptors (request/response hooks)
└── Configuration (paging, address strategy, encoding)
```

### Server vs Storage Distinction

- **SERVER_xxx pointcuts**: Request/response lifecycle hooks
- **STORAGE_xxx pointcuts**: Data persistence hooks (must be triggered manually in Plain Server)

## Core Patterns

### CRUD Operations

| Operation | Annotation            | Key Parameters                                       |
| --------- | --------------------- | ---------------------------------------------------- |
| Read      | `@Read`               | `@IdParam IdType`                                    |
| VRead     | `@Read(version=true)` | `@IdParam IdType` (with version)                     |
| Create    | `@Create`             | `@ResourceParam Patient`                             |
| Update    | `@Update`             | `@IdParam`, `@ResourceParam`                         |
| Delete    | `@Delete`             | `@IdParam IdType`                                    |
| Patch     | `@Patch`              | `@IdParam`, `PatchTypeEnum`, `@ResourceParam String` |

### Conditional Operations

Add `@ConditionalUrlParam String` to support conditional create/update/delete:

```java
@Update
public MethodOutcome update(
        @ResourceParam Patient patient,
        @IdParam IdType id,
        @ConditionalUrlParam String conditional) {
    if (conditional != null) {
        // Find by search criteria in conditional URL
    }
    // Perform update
}
```

### MethodOutcome Return

```java
MethodOutcome outcome = new MethodOutcome();
outcome.setId(new IdType("Patient", "123", "1"));
outcome.setCreated(true);  // For create operations
return outcome;
```

## Search Implementation

### Parameter Types

| Type      | Class                        | Example URL                 |
| --------- | ---------------------------- | --------------------------- |
| String    | `StringParam`                | `?family=Smith`             |
| Token     | `TokenParam`                 | `?identifier=mrn\|123`      |
| Date      | `DateParam`/`DateRangeParam` | `?date=ge2020-01-01`        |
| Reference | `ReferenceParam`             | `?subject=Patient/123`      |
| Quantity  | `QuantityParam`              | `?value-quantity=gt5\|\|kg` |

### Multi-Value Logic

```java
// OR logic (comma-separated): ?family=Smith,Jones
@OptionalParam(name = "family") StringOrListParam families

// AND logic (repeated param): ?family=Smith&family=Jones
@OptionalParam(name = "family") StringAndListParam families
```

### Paging with IBundleProvider

For large results, return `IBundleProvider` instead of `List<IBaseResource>`:

```java
@Search
public IBundleProvider search(...) {
    List<String> ids = findMatchingIds();
    return new SimpleBundleProvider(ids) {
        @Override
        public List<IBaseResource> getResources(int from, int to) {
            return loadResources(ids.subList(from, Math.min(to, ids.size())));
        }
    };
}
```

Configure paging provider on server:

```java
FifoMemoryPagingProvider paging = new FifoMemoryPagingProvider(10);
paging.setDefaultPageSize(20);
paging.setMaximumPageSize(100);
setPagingProvider(paging);
```

## Extended Operations ($operations)

```java
@Operation(name = "$everything", idempotent = true)
public Bundle everything(
        @IdParam IdType patientId,
        @OperationParam(name = "start") DateType start,
        @OperationParam(name = "end") DateType end) {
    // Return bundle with patient and related resources
}
```

- **Instance-level**: Include `@IdParam`
- **Type-level**: No `@IdParam`, register on resource provider
- **Server-level**: Register on plain provider (no `IResourceProvider`)
- `idempotent = true`: Allows HTTP GET (only for primitive params)

## Interceptors

### Registration

```java
registerInterceptor(new LoggingInterceptor());
registerInterceptor(new ResponseHighlighterInterceptor());
```

### Custom Interceptor

```java
@Interceptor
public class MyInterceptor {
    @Hook(Pointcut.SERVER_INCOMING_REQUEST_PRE_HANDLED)
    public void preHandle(RequestDetails details, HttpServletRequest request) {
        // Before request processing
    }

    @Hook(Pointcut.SERVER_OUTGOING_RESPONSE)
    public void postHandle(RequestDetails details, IBaseResource resource) {
        // After response generated
    }
}
```

### Key Pointcuts

- `SERVER_INCOMING_REQUEST_PRE_PROCESSED`: Earliest hook
- `SERVER_INCOMING_REQUEST_PRE_HANDLED`: After handler selected
- `SERVER_OUTGOING_RESPONSE`: Before response sent
- `SERVER_HANDLE_EXCEPTION`: On any exception

### Essential Built-in Interceptors

| Interceptor                      | Purpose                     |
| -------------------------------- | --------------------------- |
| `LoggingInterceptor`             | Request/response logging    |
| `ResponseHighlighterInterceptor` | HTML view for browsers      |
| `RequestValidatingInterceptor`   | Validate incoming resources |
| `ResponseValidatingInterceptor`  | Validate outgoing resources |
| `CorsInterceptor`                | CORS support                |
| `ExceptionHandlingInterceptor`   | Custom error responses      |

## Security

### Authentication Pattern

```java
@Interceptor
public class AuthInterceptor {
    @Hook(Pointcut.SERVER_INCOMING_REQUEST_PRE_HANDLED)
    public void authenticate(RequestDetails details, HttpServletRequest request) {
        String auth = request.getHeader("Authorization");
        if (!validateToken(auth)) {
            throw new AuthenticationException("Invalid credentials");
        }
        details.getUserData().put("user", extractUser(auth));
    }
}
```

### Authorisation with AuthorizationInterceptor

```java
public class MyAuthInterceptor extends AuthorizationInterceptor {
    @Override
    public List<IAuthRule> buildRuleList(RequestDetails details) {
        String userId = (String) details.getUserData().get("user");
        return new RuleBuilder()
            .allow().read().allResources()
                .inCompartment("Patient", new IdType("Patient", userId))
            .andThen()
            .allow().write().allResources()
                .inCompartment("Patient", new IdType("Patient", userId))
            .andThen()
            .denyAll()
            .build();
    }
}
```

## Validation

### Setup

```java
ValidationSupportChain chain = new ValidationSupportChain(
    new DefaultProfileValidationSupport(ctx),
    new InMemoryTerminologyServerValidationSupport(ctx),
    new CommonCodeSystemsTerminologyService(ctx)
);
FhirInstanceValidator validator = new FhirInstanceValidator(chain);
RequestValidatingInterceptor interceptor = new RequestValidatingInterceptor();
interceptor.addValidatorModule(validator);
interceptor.setFailOnSeverity(ResultSeverityEnum.ERROR);
registerInterceptor(interceptor);
```

### Profile Validation

Add `NpmPackageValidationSupport` for implementation guide validation:

```java
NpmPackageValidationSupport npm = new NpmPackageValidationSupport(ctx);
npm.loadPackageFromClasspath("classpath:package/us.core.tgz");
```

## Exception Handling

| Exception                          | HTTP Status | Use Case               |
| ---------------------------------- | ----------- | ---------------------- |
| `ResourceNotFoundException`        | 404         | Resource not found     |
| `InvalidRequestException`          | 400         | Bad request parameters |
| `UnprocessableEntityException`     | 422         | Validation failure     |
| `AuthenticationException`          | 401         | Auth required          |
| `ForbiddenOperationException`      | 403         | Access denied          |
| `ResourceVersionConflictException` | 409         | Version mismatch       |
| `InternalErrorException`           | 500         | Server error           |

## Configuration

### Server Address Strategy

```java
// For reverse proxy
setServerAddressStrategy(new HardcodedServerAddressStrategy("https://api.example.com/fhir"));

// For Apache mod_proxy
setServerAddressStrategy(new ApacheProxyAddressStrategy(true));
```

### Response Defaults

```java
setDefaultResponseEncoding(EncodingEnum.JSON);
setDefaultPrettyPrint(true);
```

### Multitenancy

```java
setTenantIdentificationStrategy(new UrlBaseTenantIdentificationStrategy());
// Access via: details.getTenantId()
```

## Detailed References

- **Resource Providers**: See [references/resource-providers.md](references/resource-providers.md)
- **Search Operations**: See [references/search.md](references/search.md)
- **Interceptors**: See [references/interceptors.md](references/interceptors.md)
- **Security**: See [references/security.md](references/security.md)
- **Extended Operations**: See [references/operations.md](references/operations.md)
