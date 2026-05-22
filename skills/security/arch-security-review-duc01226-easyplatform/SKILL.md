---
name: arch-security-review
description: Use when reviewing code for security vulnerabilities, implementing authorization, or ensuring data protection.
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# Security Review Workflow

## When to Use This Skill

- Security audit of code changes
- Implementing authentication/authorization
- Data protection review
- Vulnerability assessment

## Pre-Flight Checklist

- [ ] Identify security-sensitive areas
- [ ] Review OWASP Top 10 relevance
- [ ] Check for existing security patterns
- [ ] Plan remediation approach

## OWASP Top 10 Checklist

### 1. Broken Access Control

```csharp
// :x: VULNERABLE - No authorization check
[HttpGet("{id}")]
public async Task<Employee> Get(string id)
    => await repo.GetByIdAsync(id);

// :white_check_mark: SECURE - Authorization enforced
[HttpGet("{id}")]
[PlatformAuthorize(Roles.Manager, Roles.Admin)]
public async Task<Employee> Get(string id)
{
    var employee = await repo.GetByIdAsync(id);

    // Verify access to this specific resource
    if (employee.CompanyId != RequestContext.CurrentCompanyId())
        throw new UnauthorizedAccessException();

    return employee;
}
```

### 2. Cryptographic Failures

```csharp
// :x: VULNERABLE - Storing plain text secrets
var apiKey = config["ApiKey"];
await SaveToDatabase(apiKey);

// :white_check_mark: SECURE - Encrypt sensitive data
var encryptedKey = encryptionService.Encrypt(apiKey);
await SaveToDatabase(encryptedKey);

// Use secure configuration
var apiKey = config.GetValue<string>("ApiKey");  // From Azure Key Vault
```

### 3. Injection

```csharp
// :x: VULNERABLE - SQL Injection
var sql = $"SELECT * FROM Users WHERE Name = '{name}'";
await context.Database.ExecuteSqlRawAsync(sql);

// :white_check_mark: SECURE - Parameterized query
await context.Users.Where(u => u.Name == name).ToListAsync();

// Or if raw SQL needed:
await context.Database.ExecuteSqlRawAsync(
    "SELECT * FROM Users WHERE Name = @p0", name);
```

### 4. Insecure Design

```csharp
// :x: VULNERABLE - No rate limiting
[HttpPost("login")]
public async Task<IActionResult> Login(LoginRequest request)
    => await authService.Login(request);

// :white_check_mark: SECURE - Rate limiting applied
[HttpPost("login")]
[RateLimit(MaxRequests = 5, WindowSeconds = 60)]
public async Task<IActionResult> Login(LoginRequest request)
    => await authService.Login(request);
```

### 5. Security Misconfiguration

```csharp
// :x: VULNERABLE - Detailed errors in production
app.UseDeveloperExceptionPage();  // Exposes stack traces

// :white_check_mark: SECURE - Generic errors in production
if (env.IsDevelopment())
    app.UseDeveloperExceptionPage();
else
    app.UseExceptionHandler("/Error");
```

### 6. Vulnerable Components

```bash
# Check for vulnerable packages
dotnet list package --vulnerable

# Update vulnerable packages
dotnet outdated
```

### 7. Authentication Failures

```csharp
// :x: VULNERABLE - Weak password policy
if (password.Length >= 4) { }

// :white_check_mark: SECURE - Strong password policy
public class PasswordPolicy
{
    public bool Validate(string password)
    {
        return password.Length >= 12
            && password.Any(char.IsUpper)
            && password.Any(char.IsLower)
            && password.Any(char.IsDigit)
            && password.Any(c => !char.IsLetterOrDigit(c));
    }
}
```

### 8. Data Integrity Failures

```csharp
// :x: VULNERABLE - No validation of external data
var userData = await externalApi.GetUserAsync(id);
await SaveToDatabase(userData);

// :white_check_mark: SECURE - Validate external data
var userData = await externalApi.GetUserAsync(id);
var validation = userData.Validate();
if (!validation.IsValid)
    throw new ValidationException(validation.Errors);
await SaveToDatabase(userData);
```

### 9. Logging Failures

```csharp
// :x: VULNERABLE - Logging sensitive data
Logger.LogInformation("User login: {Email} {Password}", email, password);

// :white_check_mark: SECURE - Redact sensitive data
Logger.LogInformation("User login: {Email}", email);
// Never log passwords, tokens, or PII
```

### 10. SSRF (Server-Side Request Forgery)

```csharp
// :x: VULNERABLE - User-controlled URL
var url = request.WebhookUrl;
await httpClient.GetAsync(url);  // Could access internal services

// :white_check_mark: SECURE - Validate and restrict URLs
if (!IsAllowedUrl(request.WebhookUrl))
    throw new SecurityException("Invalid webhook URL");

private bool IsAllowedUrl(string url)
{
    var uri = new Uri(url);
    return AllowedDomains.Contains(uri.Host)
        && uri.Scheme == "https";
}
```

## Authorization Patterns

### Controller Level

```csharp
[ApiController]
[Route("api/[controller]")]
[PlatformAuthorize]  // Require authentication
public class EmployeeController : PlatformBaseController
{
    [HttpPost]
    [PlatformAuthorize(Roles.Admin, Roles.Manager)]  // Role-based
    public async Task<IActionResult> Create(...)
}
```

### Handler Level

```csharp
protected override async Task<PlatformValidationResult<T>> ValidateRequestAsync(
    PlatformValidationResult<T> validation, CancellationToken ct)
{
    return await validation
        // Check role
        .And(_ => RequestContext.HasRole(Roles.Admin), "Admin role required")
        // Check company access
        .And(_ => entity.CompanyId == RequestContext.CurrentCompanyId(),
            "Access denied: different company")
        // Check ownership
        .And(_ => entity.OwnerId == RequestContext.UserId() ||
            RequestContext.HasRole(Roles.Admin),
            "Access denied: not owner");
}
```

### Query Level

```csharp
// Always filter by company/user context
var employees = await repo.GetAllAsync(
    e => e.CompanyId == RequestContext.CurrentCompanyId()
        && (e.IsPublic || e.OwnerId == RequestContext.UserId()));
```

## Data Protection

### Sensitive Data Handling

```csharp
public class SensitiveDataHandler
{
    // Encrypt at rest
    public string EncryptForStorage(string plainText)
        => encryptionService.Encrypt(plainText);

    // Mask for display
    public string MaskEmail(string email)
    {
        var parts = email.Split('@');
        return $"{parts[0][0]}***@{parts[1]}";
    }

    // Never log sensitive data
    public void LogUserAction(User user)
    {
        Logger.LogInformation("User action: {UserId}", user.Id);
        // NOT: Logger.Log("User: {Email} {Phone}", user.Email, user.Phone);
    }
}
```

### File Upload Security

```csharp
public async Task<IActionResult> Upload(IFormFile file)
{
    // Validate file type
    var allowedTypes = new[] { ".pdf", ".docx", ".xlsx" };
    var extension = Path.GetExtension(file.FileName).ToLowerInvariant();
    if (!allowedTypes.Contains(extension))
        return BadRequest("Invalid file type");

    // Validate file size
    if (file.Length > 10 * 1024 * 1024)  // 10MB
        return BadRequest("File too large");

    // Scan for malware (if available)
    if (!await antivirusService.ScanAsync(file))
        return BadRequest("File rejected by security scan");

    // Generate safe filename
    var safeFileName = $"{Guid.NewGuid()}{extension}";

    // Save to isolated storage
    await fileService.SaveAsync(file, safeFileName);

    return Ok();
}
```

## Security Scanning Commands

```bash
# .NET vulnerability scan
dotnet list package --vulnerable

# Outdated packages
dotnet outdated

# Secret scanning
grep -r "password\|secret\|apikey" --include="*.cs" --include="*.json"

# Hardcoded credentials
grep -r "Password=\"" --include="*.cs"
grep -r "connectionString.*password" --include="*.json"
```

## Security Review Checklist

### Authentication

- [ ] Strong password policy enforced
- [ ] Account lockout after failed attempts
- [ ] Secure session management
- [ ] JWT tokens properly validated
- [ ] Refresh token rotation

### Authorization

- [ ] All endpoints require authentication
- [ ] Role-based access control implemented
- [ ] Resource-level permissions checked
- [ ] No privilege escalation possible

### Input Validation

- [ ] All inputs validated
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (output encoding)
- [ ] File uploads validated
- [ ] URL validation for redirects

### Data Protection

- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced
- [ ] No sensitive data in logs
- [ ] Proper error handling (no stack traces)

### Dependencies

- [ ] No known vulnerable packages
- [ ] Dependencies regularly updated
- [ ] Third-party code reviewed

## Anti-Patterns to AVOID

:x: **Trusting client input**

```csharp
var isAdmin = request.IsAdmin;  // User-supplied!
```

:x: **Exposing internal errors**

```csharp
catch (Exception ex) { return BadRequest(ex.ToString()); }
```

:x: **Hardcoded secrets**

```csharp
var apiKey = "sk_live_xxxxx";
```

:x: **Insufficient logging**

```csharp
// No audit trail for sensitive operations
await DeleteAllUsers();
```

## Verification Checklist

- [ ] OWASP Top 10 reviewed
- [ ] Authentication/authorization verified
- [ ] Input validation complete
- [ ] Sensitive data protected
- [ ] No hardcoded secrets
- [ ] Logging appropriate (no PII)
- [ ] Dependencies scanned

## See Also

See `/security` command for structured security review workflow.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
