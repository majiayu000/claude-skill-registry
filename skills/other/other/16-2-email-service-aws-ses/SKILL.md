---
name: email-service-aws-ses
description: "Implements email service using AWS SES for .NET APIs. Designed for applications with HTML template support, placeholder replacement, and Result pattern error handling."
version: 1.0.0
language: C#
framework: .NET 9+
dependencies: AWSSDK.SimpleEmailV2
---

# AWS SES Email Service

## Overview

This skill implements email delivery via AWS SES for APIs:

- **AWS SES Integration** - Production-ready email delivery
- **HTML Templates** - File-based templates with placeholder replacement
- **Result Pattern** - No exceptions, returns `Result<T>` for error handling
- **Enable/Disable Toggle** - Development mode without actual sending

---

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| `IEmailService` | Email abstraction interface | Application/Abstractions/Email |
| `AwsSesEmailService` | AWS SES implementation | Infrastructure/Email |
| `EmailOptions` | AWS SES configuration | Infrastructure/Email |
| `EmailErrors` | Error definitions | Application/Abstractions/Email |

---

## Email Structure

```
/Application/Abstractions/
├── Email/
│   ├── IEmailService.cs
│   └── EmailErrors.cs

/Infrastructure/
├── Email/
│   ├── EmailOptions.cs
│   └── AwsSesEmailService.cs

/Api/
├── EmailTemplates/
│   ├── appointment-reminder.html
│   ├── appointment-reminder-es.html
│   ├── test-results-ready.html
│   ├── prescription-ready.html
│   ├── welcome.html
│   └── password-reset.html
```

---

## Template: Email Service Interface

```csharp
// src/{name}.application/Abstractions/Email/IEmailService.cs
using {name}.domain.abstractions;

namespace {name}.application.Abstractions.Email;

/// <summary>
/// Service for sending emails via AWS SES
/// Returns Result pattern for error handling (no exceptions)
/// </summary>
public interface IEmailService
{
    /// <summary>
    /// Send an email using a template file with placeholder replacements
    /// </summary>
    /// <param name="toEmail">Recipient email address</param>
    /// <param name="subject">Email subject</param>
    /// <param name="templateName">Name of the template file (without extension)</param>
    /// <param name="placeholders">Dictionary of placeholder keys and replacement values</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Result indicating success or failure</returns>
    Task<r> SendTemplatedEmailAsync(
        string toEmail,
        string subject,
        string templateName,
        Dictionary<string, string> placeholders,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Send an email with raw HTML content
    /// </summary>
    /// <param name="toEmail">Recipient email address</param>
    /// <param name="subject">Email subject</param>
    /// <param name="htmlBody">HTML content of the email</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Result indicating success or failure</returns>
    Task<r> SendHtmlEmailAsync(
        string toEmail,
        string subject,
        string htmlBody,
        CancellationToken cancellationToken = default);
}
```

---

## Template: Email Errors

```csharp
// src/{name}.application/Abstractions/Email/EmailErrors.cs
using {name}.domain.abstractions;

namespace {name}.application.Abstractions.Email;

public static class EmailErrors
{
    public static readonly Error SendFailed = new(
        "Email.SendFailed",
        "Failed to send email. Please try again later.");

    public static readonly Error TemplateNotFound = new(
        "Email.TemplateNotFound",
        "Email template not found.");

    public static readonly Error InvalidRecipient = new(
        "Email.InvalidRecipient",
        "Invalid recipient email address.");

    public static readonly Error EmailDisabled = new(
        "Email.Disabled",
        "Email sending is currently disabled.");
}
```

---

## Template: Email Options

```csharp
// src/{name}.infrastructure/Email/EmailOptions.cs
namespace {name}.infrastructure.Email;

public sealed class EmailOptions
{
    public const string SectionName = "Email";

    /// <summary>
    /// AWS region for SES (e.g., "us-east-1")
    /// </summary>
    public string AwsRegion { get; init; } = "us-east-1";

    /// <summary>
    /// AWS access key ID (optional - use IAM role in production)
    /// </summary>
    public string? AwsAccessKeyId { get; init; }

    /// <summary>
    /// AWS secret access key (optional - use IAM role in production)
    /// </summary>
    public string? AwsSecretAccessKey { get; init; }

    /// <summary>
    /// Email address to send from
    /// </summary>
    public string FromAddress { get; init; } = string.Empty;

    /// <summary>
    /// Display name for the sender (e.g., "Support Team")
    /// </summary>
    public string FromName { get; init; } = string.Empty;

    /// <summary>
    /// Whether email sending is enabled (disable for development)
    /// </summary>
    public bool Enabled { get; init; } = false;

    /// <summary>
    /// Path to email templates directory (relative to app base)
    /// </summary>
    public string TemplatesPath { get; init; } = "EmailTemplates";
}
```

### appsettings.json

```json
{
  "Email": {
    "AwsRegion": "us-east-1",
    "AwsAccessKeyId": "",
    "AwsSecretAccessKey": "",
    "FromAddress": "noreply@healthcare.example.com",
    "FromName": "Supoort Team",
    "Enabled": true,
    "TemplatesPath": "EmailTemplates"
  }
}
```

---

## Template: AWS SES Email Service Implementation

```csharp
// src/{name}.infrastructure/Email/AwsSesEmailService.cs
using Amazon;
using Amazon.SimpleEmailV2;
using Amazon.SimpleEmailV2.Model;
using {name}.application.Abstractions.Email;
using {name}.domain.abstractions;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace {name}.infrastructure.Email;

internal sealed class AwsSesEmailService : IEmailService
{
    private readonly EmailOptions _options;
    private readonly ILogger<AwsSesEmailService> _logger;
    private readonly IAmazonSimpleEmailServiceV2 _sesClient;
    private readonly string _templatesPath;

    public AwsSesEmailService(
        IOptions<EmailOptions> options,
        ILogger<AwsSesEmailService> logger)
    {
        _options = options.Value;
        _logger = logger;

        // Initialize SES v2 client
        var region = RegionEndpoint.GetBySystemName(_options.AwsRegion);

        if (!string.IsNullOrEmpty(_options.AwsAccessKeyId) &&
            !string.IsNullOrEmpty(_options.AwsSecretAccessKey))
        {
            // Use explicit credentials (dev/staging)
            _sesClient = new AmazonSimpleEmailServiceV2Client(
                _options.AwsAccessKeyId,
                _options.AwsSecretAccessKey,
                region);
        }
        else
        {
            // Use IAM role or environment credentials (production)
            _sesClient = new AmazonSimpleEmailServiceV2Client(region);
        }

        // Set templates path relative to application base directory
        _templatesPath = Path.Combine(
            AppDomain.CurrentDomain.BaseDirectory, 
            _options.TemplatesPath);
    }

    public async Task<r> SendTemplatedEmailAsync(
        string toEmail,
        string subject,
        string templateName,
        Dictionary<string, string> placeholders,
        CancellationToken cancellationToken = default)
    {
        // Load template file
        var templatePath = Path.Combine(_templatesPath, $"{templateName}.html");

        if (!File.Exists(templatePath))
        {
            _logger.LogError("Email template not found: {TemplatePath}", templatePath);
            return Result.Failure(EmailErrors.TemplateNotFound);
        }

        var htmlBody = await File.ReadAllTextAsync(templatePath, cancellationToken);

        // Replace placeholders using {{key}} syntax
        foreach (var (key, value) in placeholders)
        {
            htmlBody = htmlBody.Replace($"{{{{{key}}}}}", value);
        }

        return await SendHtmlEmailAsync(toEmail, subject, htmlBody, cancellationToken);
    }

    public async Task<r> SendHtmlEmailAsync(
        string toEmail,
        string subject,
        string htmlBody,
        CancellationToken cancellationToken = default)
    {
        // Development mode - log but don't send
        if (!_options.Enabled)
        {
            _logger.LogWarning(
                "Email disabled. Would send to {Email}: {Subject}",
                toEmail, subject);
            return Result.Success();
        }

        // Validate recipient
        if (string.IsNullOrWhiteSpace(toEmail))
        {
            _logger.LogWarning("Cannot send email: recipient address is empty");
            return Result.Failure(EmailErrors.InvalidRecipient);
        }

        try
        {
            // Format sender address
            var fromAddress = string.IsNullOrEmpty(_options.FromName)
                ? _options.FromAddress
                : $"{_options.FromName} <{_options.FromAddress}>";

            var request = new SendEmailRequest
            {
                FromEmailAddress = fromAddress,
                Destination = new Destination
                {
                    ToAddresses = new List<string> { toEmail }
                },
                Content = new EmailContent
                {
                    Simple = new Message
                    {
                        Subject = new Content { Data = subject, Charset = "UTF-8" },
                        Body = new Body
                        {
                            Html = new Content { Data = htmlBody, Charset = "UTF-8" }
                        }
                    }
                }
            };

            var response = await _sesClient.SendEmailAsync(request, cancellationToken);

            _logger.LogInformation(
                "Email sent to {Email}. MessageId: {MessageId}",
                toEmail, response.MessageId);

            return Result.Success();
        }
        catch (MessageRejectedException ex)
        {
            _logger.LogError(ex, "Email rejected for {Email}", toEmail);
            return Result.Failure(EmailErrors.SendFailed);
        }
        catch (MailFromDomainNotVerifiedException ex)
        {
            _logger.LogError(ex, "From domain not verified: {FromAddress}", _options.FromAddress);
            return Result.Failure(EmailErrors.SendFailed);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to send email to {Email}", toEmail);
            return Result.Failure(EmailErrors.SendFailed);
        }
    }
}
```

---

## Template: Dependency Injection Registration

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
private static void AddEmail(IServiceCollection services, IConfiguration configuration)
{
    // Configure email options
    services.Configure<EmailOptions>(configuration.GetSection(EmailOptions.SectionName));

    // Register email service
    services.AddScoped<IEmailService, AwsSesEmailService>();
}
```

---

## Email Templates

### Template: Appointment Reminder

```html
<!-- EmailTemplates/appointment-reminder.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Reminder</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2c5aa0;">Appointment Reminder</h1>
        
        <p>Dear {{patient_name}},</p>
        
        <p>This is a reminder of your upcoming appointment:</p>
        
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Date:</strong> {{appointment_date}}</p>
            <p><strong>Time:</strong> {{appointment_time}}</p>
            <p><strong>Provider:</strong> {{provider_name}}</p>
            <p><strong>Location:</strong> {{clinic_address}}</p>
            <p><strong>Appointment Type:</strong> {{appointment_type}}</p>
        </div>
        
        <h3>Before Your Visit</h3>
        <ul>
            <li>Please arrive 15 minutes early</li>
            <li>Bring your insurance card and photo ID</li>
            <li>Bring a list of current medications</li>
        </ul>
        
        <p>If you need to reschedule or cancel, please contact us at least 24 hours in advance.</p>
        
        <p>
            <a href="{{cancel_url}}" style="color: #2c5aa0;">Cancel Appointment</a> | 
            <a href="{{reschedule_url}}" style="color: #2c5aa0;">Reschedule</a>
        </p>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        
        <p style="font-size: 12px; color: #666;">
            {{clinic_name}}<br>
            {{clinic_phone}}<br>
            <em>This is an automated message. Please do not reply directly to this email.</em>
        </p>
    </div>
</body>
</html>
```

### Template: Test Results Ready

```html
<!-- EmailTemplates/test-results-ready.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Results Available</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2c5aa0;">Your Test Results Are Ready</h1>
        
        <p>Dear {{patient_name}},</p>
        
        <p>Your test results from <strong>{{test_date}}</strong> are now available for review.</p>
        
        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Test Type:</strong> {{test_type}}</p>
            <p><strong>Ordered By:</strong> {{ordering_provider}}</p>
        </div>
        
        <p>
            <a href="{{portal_url}}" style="display: inline-block; background-color: #2c5aa0; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                View Results in Patient Portal
            </a>
        </p>
        
        <p style="margin-top: 20px;">
            <strong>Note:</strong> For questions about your results, please contact your healthcare 
            provider directly or send a message through the patient portal.
        </p>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        
        <p style="font-size: 12px; color: #666;">
            <strong>HIPAA Notice:</strong> This email contains protected health information (PHI). 
            It is intended only for the individual named above. If you received this in error, 
            please delete it and notify us immediately.
        </p>
    </div>
</body>
</html>
```

### Template: Welcome Email

```html
<!-- EmailTemplates/welcome.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Welcome to {{clinic_name}}</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2c5aa0;">Welcome to {{clinic_name}}</h1>
        
        <p>Dear {{patient_name}},</p>
        
        <p>Thank you for registering with us. Your patient portal account has been created.</p>
        
        <h3>Getting Started</h3>
        <ul>
            <li>Complete your health history</li>
            <li>Add your insurance information</li>
            <li>Review your upcoming appointments</li>
            <li>Set up prescription refill reminders</li>
        </ul>
        
        <p>
            <a href="{{portal_url}}" style="display: inline-block; background-color: #2c5aa0; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                Access Patient Portal
            </a>
        </p>
        
        <h3>Contact Us</h3>
        <p>
            Phone: {{clinic_phone}}<br>
            Email: {{clinic_email}}<br>
            Address: {{clinic_address}}
        </p>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        
        <p style="font-size: 12px; color: #666;">
            Questions? Contact our support team at {{support_email}}
        </p>
    </div>
</body>
</html>
```

---

## Usage Examples

### Sending Appointment Reminder

```csharp
public class SendAppointmentReminderHandler
{
    private readonly IEmailService _emailService;

    public async Task<Result> Handle(SendReminderCommand command, CancellationToken ct)
    {
        var placeholders = new Dictionary<string, string>
        {
            ["patient_name"] = command.PatientName,
            ["appointment_date"] = command.AppointmentDate.ToString("MMMM d, yyyy"),
            ["appointment_time"] = command.AppointmentTime.ToString("h:mm tt"),
            ["provider_name"] = command.ProviderName,
            ["clinic_address"] = command.ClinicAddress,
            ["appointment_type"] = command.AppointmentType,
            ["cancel_url"] = $"https://portal.example.com/cancel/{command.AppointmentId}",
            ["reschedule_url"] = $"https://portal.example.com/reschedule/{command.AppointmentId}",
            ["clinic_name"] = "HealthCare Medical Center",
            ["clinic_phone"] = "(555) 123-4567"
        };

        var result = await _emailService.SendTemplatedEmailAsync(
            toEmail: command.PatientEmail,
            subject: $"Appointment Reminder - {command.AppointmentDate:MMM d}",
            templateName: "appointment-reminder",
            placeholders: placeholders,
            cancellationToken: ct);

        if (result.IsFailure)
        {
            // Log failure but don't throw
            _logger.LogWarning("Failed to send reminder to {Email}", command.PatientEmail);
        }

        return result;
    }
}
```

### Sending Test Results Notification

```csharp
public class NotifyTestResultsReadyHandler
{
    private readonly IEmailService _emailService;
    private readonly ISecurityAuditService _auditService;

    public async Task<Result> Handle(NotifyResultsCommand command, CancellationToken ct)
    {
        var placeholders = new Dictionary<string, string>
        {
            ["patient_name"] = command.PatientName,
            ["test_date"] = command.TestDate.ToString("MMMM d, yyyy"),
            ["test_type"] = command.TestType,
            ["ordering_provider"] = command.OrderingProvider,
            ["portal_url"] = $"https://portal.example.com/results/{command.ResultId}"
        };

        var result = await _emailService.SendTemplatedEmailAsync(
            toEmail: command.PatientEmail,
            subject: "Your Test Results Are Ready",
            templateName: "test-results-ready",
            placeholders: placeholders,
            cancellationToken: ct);

        // HIPAA: Audit the notification
        await _auditService.LogAsync(
            eventType: "PHI_ACCESS_NOTIFICATION",
            severity: "INFO",
            eventDescription: $"Test results notification sent for {command.TestType}",
            userId: command.PatientId,
            metadata: new { TestId = command.ResultId });

        return result;
    }
}
```

### Localized Templates

```csharp
// Use template naming convention for localization
public async Task<Result> SendAppointmentReminderAsync(
    string email,
    string patientName,
    DateTime appointmentDate,
    string language,
    CancellationToken ct)
{
    // Template names: appointment-reminder.html, appointment-reminder-es.html
    var templateName = language.ToLower() switch
    {
        "es" => "appointment-reminder-es",
        "fr" => "appointment-reminder-fr",
        _ => "appointment-reminder"
    };

    var subject = language.ToLower() switch
    {
        "es" => "Recordatorio de Cita",
        "fr" => "Rappel de Rendez-vous",
        _ => "Appointment Reminder"
    };

    return await _emailService.SendTemplatedEmailAsync(
        toEmail: email,
        subject: subject,
        templateName: templateName,
        placeholders: new Dictionary<string, string>
        {
            ["patient_name"] = patientName,
            ["appointment_date"] = appointmentDate.ToString("MMMM d, yyyy")
        },
        cancellationToken: ct);
}
```
---

## Anti-Patterns to Avoid

// ❌ WRONG: Throwing exceptions on failure
if (!File.Exists(templatePath))
    throw new EmailTemplateNotFoundException(templateName);

// ✅ CORRECT: Return Result for graceful handling
if (!File.Exists(templatePath))
    return Result.Failure(EmailErrors.TemplateNotFound);

// ❌ WRONG: Logging email content
_logger.LogInformation("Sending email: {Body}", htmlBody);

// ✅ CORRECT: Log only metadata
_logger.LogInformation("Sending email to {Email}: {Subject}", toEmail, subject);

// ❌ WRONG: Hardcoding template paths
var path = "/app/templates/email.html";

// ✅ CORRECT: Use configuration
var path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, _options.TemplatesPath);
```

---

## Related Skills

- `domain-events-generator` - Trigger emails from events
- `quartz-background-jobs` - Scheduled email jobs
- `outbox-pattern` - Reliable email delivery