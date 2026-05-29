---
name: email-service
description: "Implements email service abstraction with SendGrid provider. Includes template support, localization, async sending, and domain event integration for transactional emails."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: SendGrid
---

# Email Service Integration

## Overview

Abstracted email service with template support:

- **Interface in Application** - `IEmailService`
- **SendGrid implementation** - Production-ready provider
- **Template support** - Dynamic content with placeholders
- **Localization** - Multiple language templates
- **Domain event integration** - Send on user actions

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `IEmailService` | Email abstraction interface |
| `SendGridEmailService` | SendGrid implementation |
| `EmailOptions` | Configuration settings |
| `EmailTemplate` | Template definitions |

---

## Template: Email Service Interface

```csharp
// src/{name}.application/Abstractions/Email/IEmailService.cs
namespace {name}.application.abstractions.email;

public interface IEmailService
{
    Task SendAsync(
        string to,
        string subject,
        string htmlBody,
        CancellationToken cancellationToken = default);

    Task SendTemplateAsync(
        string to,
        string templateId,
        object templateData,
        CancellationToken cancellationToken = default);

    Task SendWelcomeEmailAsync(
        string to,
        string userName,
        string language = "en",
        CancellationToken cancellationToken = default);

    Task SendPasswordResetEmailAsync(
        string to,
        string resetCode,
        string language = "en",
        CancellationToken cancellationToken = default);

    Task SendAssessmentReadyEmailAsync(
        string to,
        string userName,
        string assessmentName,
        string language = "en",
        CancellationToken cancellationToken = default);
}
```

---

## Template: Email Options

```csharp
// src/{name}.infrastructure/Email/EmailOptions.cs
namespace {name}.infrastructure.email;

public sealed class EmailOptions
{
    public const string SectionName = "Email";

    public string ApiKey { get; init; } = string.Empty;
    public string FromEmail { get; init; } = string.Empty;
    public string FromName { get; init; } = string.Empty;
    public bool EnableSending { get; init; } = true;

    // SendGrid template IDs
    public EmailTemplateIds Templates { get; init; } = new();
}

public sealed class EmailTemplateIds
{
    public string WelcomeEn { get; init; } = string.Empty;
    public string WelcomeEs { get; init; } = string.Empty;
    public string PasswordResetEn { get; init; } = string.Empty;
    public string PasswordResetEs { get; init; } = string.Empty;
    public string AssessmentReadyEn { get; init; } = string.Empty;
    public string AssessmentReadyEs { get; init; } = string.Empty;
}
```

---

## Template: SendGrid Implementation

```csharp
// src/{name}.infrastructure/Email/SendGridEmailService.cs
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using SendGrid;
using SendGrid.Helpers.Mail;
using {name}.application.abstractions.email;

namespace {name}.infrastructure.email;

internal sealed class SendGridEmailService : IEmailService
{
    private readonly ISendGridClient _client;
    private readonly EmailOptions _options;
    private readonly ILogger<SendGridEmailService> _logger;

    public SendGridEmailService(
        IOptions<EmailOptions> options,
        ILogger<SendGridEmailService> logger)
    {
        _options = options.Value;
        _client = new SendGridClient(_options.ApiKey);
        _logger = logger;
    }

    public async Task SendAsync(
        string to,
        string subject,
        string htmlBody,
        CancellationToken cancellationToken = default)
    {
        if (!_options.EnableSending)
        {
            _logger.LogInformation(
                "Email sending disabled. Would send to {To}: {Subject}",
                to, subject);
            return;
        }

        var message = new SendGridMessage
        {
            From = new EmailAddress(_options.FromEmail, _options.FromName),
            Subject = subject,
            HtmlContent = htmlBody
        };
        message.AddTo(new EmailAddress(to));

        var response = await _client.SendEmailAsync(message, cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            var body = await response.Body.ReadAsStringAsync(cancellationToken);
            _logger.LogError(
                "Failed to send email to {To}. Status: {Status}, Body: {Body}",
                to, response.StatusCode, body);
            throw new EmailSendException($"Failed to send email: {response.StatusCode}");
        }

        _logger.LogInformation("Email sent to {To}: {Subject}", to, subject);
    }

    public async Task SendTemplateAsync(
        string to,
        string templateId,
        object templateData,
        CancellationToken cancellationToken = default)
    {
        if (!_options.EnableSending)
        {
            _logger.LogInformation(
                "Email sending disabled. Would send template {TemplateId} to {To}",
                templateId, to);
            return;
        }

        var message = new SendGridMessage
        {
            From = new EmailAddress(_options.FromEmail, _options.FromName),
            TemplateId = templateId
        };
        message.AddTo(new EmailAddress(to));
        message.SetTemplateData(templateData);

        var response = await _client.SendEmailAsync(message, cancellationToken);

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogError(
                "Failed to send template email to {To}. Template: {TemplateId}",
                to, templateId);
            throw new EmailSendException($"Failed to send email: {response.StatusCode}");
        }

        _logger.LogInformation(
            "Template email sent to {To}. Template: {TemplateId}",
            to, templateId);
    }

    public async Task SendWelcomeEmailAsync(
        string to,
        string userName,
        string language = "en",
        CancellationToken cancellationToken = default)
    {
        var templateId = language.ToLower() switch
        {
            "es" => _options.Templates.WelcomeEs,
            _ => _options.Templates.WelcomeEn
        };

        await SendTemplateAsync(to, templateId, new
        {
            user_name = userName,
            login_url = "https://app.example.com/login"
        }, cancellationToken);
    }

    public async Task SendPasswordResetEmailAsync(
        string to,
        string resetCode,
        string language = "en",
        CancellationToken cancellationToken = default)
    {
        var templateId = language.ToLower() switch
        {
            "es" => _options.Templates.PasswordResetEs,
            _ => _options.Templates.PasswordResetEn
        };

        await SendTemplateAsync(to, templateId, new
        {
            reset_code = resetCode,
            reset_url = $"https://app.example.com/reset-password?code={resetCode}",
            expiration_hours = 24
        }, cancellationToken);
    }

    public async Task SendAssessmentReadyEmailAsync(
        string to,
        string userName,
        string assessmentName,
        string language = "en",
        CancellationToken cancellationToken = default)
    {
        var templateId = language.ToLower() switch
        {
            "es" => _options.Templates.AssessmentReadyEs,
            _ => _options.Templates.AssessmentReadyEn
        };

        await SendTemplateAsync(to, templateId, new
        {
            user_name = userName,
            assessment_name = assessmentName,
            assessment_url = "https://app.example.com/assessments"
        }, cancellationToken);
    }
}

public class EmailSendException : Exception
{
    public EmailSendException(string message) : base(message) { }
}
```

---

## Template: Domain Event Handler

```csharp
// src/{name}.application/Users/EventHandlers/UserCreatedSendWelcomeEmailHandler.cs
using MediatR;
using Microsoft.Extensions.Logging;
using {name}.application.abstractions.email;
using {name}.domain.users.events;

namespace {name}.application.users.eventhandlers;

internal sealed class UserCreatedSendWelcomeEmailHandler
    : INotificationHandler<UserCreatedDomainEvent>
{
    private readonly IEmailService _emailService;
    private readonly IUserRepository _userRepository;
    private readonly ILogger<UserCreatedSendWelcomeEmailHandler> _logger;

    public UserCreatedSendWelcomeEmailHandler(
        IEmailService emailService,
        IUserRepository userRepository,
        ILogger<UserCreatedSendWelcomeEmailHandler> logger)
    {
        _emailService = emailService;
        _userRepository = userRepository;
        _logger = logger;
    }

    public async Task Handle(
        UserCreatedDomainEvent notification,
        CancellationToken cancellationToken)
    {
        var user = await _userRepository.GetByIdAsync(
            notification.UserId,
            cancellationToken);

        if (user is null)
        {
            _logger.LogWarning(
                "User {UserId} not found for welcome email",
                notification.UserId);
            return;
        }

        await _emailService.SendWelcomeEmailAsync(
            user.Email.Value,
            user.Name,
            user.PreferredLanguage,
            cancellationToken);
    }
}
```

---

## Template: Registration

```csharp
// appsettings.json
{
  "Email": {
    "ApiKey": "SG.your-sendgrid-api-key",
    "FromEmail": "noreply@example.com",
    "FromName": "My Application",
    "EnableSending": true,
    "Templates": {
      "WelcomeEn": "d-xxxxxxxxxxxxx",
      "WelcomeEs": "d-xxxxxxxxxxxxx",
      "PasswordResetEn": "d-xxxxxxxxxxxxx",
      "PasswordResetEs": "d-xxxxxxxxxxxxx"
    }
  }
}

// DependencyInjection.cs
services.Configure<EmailOptions>(configuration.GetSection(EmailOptions.SectionName));
services.AddScoped<IEmailService, SendGridEmailService>();
```

---

## Related Skills

- `domain-events-generator` - Trigger emails from events
- `quartz-background-jobs` - Scheduled email jobs
- `outbox-pattern` - Reliable email delivery
