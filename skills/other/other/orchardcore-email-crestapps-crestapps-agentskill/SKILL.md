---
name: orchardcore-email
description: Guidance for configuring and sending emails in Orchard Core using the OrchardCore.Email module, including SMTP setup, programmatic sending via ISmtpService, Liquid-based email templates, recipe-driven configuration, workflow email activities, and the Azure Communication Services email provider.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# OrchardCore.Email Module

The `OrchardCore.Email` module provides email functionality for Orchard Core applications. It supports multiple email providers, Liquid-based templates for dynamic content, workflow integration, and both admin UI and recipe-based configuration.

## Email Providers

Orchard Core ships with built-in support for the following email providers:

- **SMTP (MailKit)** — Uses `MailKitSmtpService` to deliver messages through any standard SMTP server.
- **Azure Communication Services** — Sends email through the Azure Communication Services Email API using the `OrchardCore.Email.Azure` module.

Enable the relevant feature depending on your provider:

- `OrchardCore.Email` — Core email abstractions and admin settings.
- `OrchardCore.Email.Smtp` — SMTP delivery via MailKit.
- `OrchardCore.Email.Azure` — Azure Communication Services delivery.

## Configuring SMTP Settings

### Via Admin UI

Navigate to **Configuration → Settings → Email** in the admin dashboard. The SMTP settings section allows you to specify:

| Setting | Description |
|---|---|
| Default Sender | The default "From" address for outgoing messages. |
| Host | The SMTP server hostname (e.g., `smtp.example.com`). |
| Port | The SMTP port (typically 25, 465, or 587). |
| Encryption Method | `None`, `SSLTLS`, or `STARTTLS`. |
| Username | Credentials for SMTP authentication. |
| Password | Password for SMTP authentication. |
| Proxy Host / Port | Optional SOCKS proxy settings for environments that route through a proxy. |

### Via Recipe

Configure SMTP settings declaratively using a `Settings` recipe step targeting `SmtpSettings`:

```json
{
  "steps": [
    {
      "name": "Settings",
      "SmtpSettings": {
        "DefaultSender": "noreply@example.com",
        "Host": "smtp.example.com",
        "Port": 587,
        "EncryptionMethod": "STARTTLS",
        "AutoSelectEncryption": false,
        "RequireCredentials": true,
        "UserName": "smtp-user",
        "Password": "smtp-password",
        "ProxyHost": null,
        "ProxyPort": 0
      }
    }
  ]
}
```

### Via Configuration Provider

SMTP settings can also be supplied through `appsettings.json` or environment variables using the `OrchardCore_Email_Smtp` configuration section:

```json
{
  "OrchardCore_Email_Smtp": {
    "DefaultSender": "noreply@example.com",
    "Host": "smtp.example.com",
    "Port": 587,
    "EncryptionMethod": "STARTTLS",
    "RequireCredentials": true,
    "UserName": "smtp-user",
    "Password": "smtp-password"
  }
}
```

## Configuring Azure Communication Services Email

Enable the `OrchardCore.Email.Azure` feature, then configure settings in the admin under **Configuration → Settings → Email → Azure Communication Services**, or via configuration:

```json
{
  "OrchardCore_Email_Azure": {
    "DefaultSender": "DoNotReply@your-azure-domain.azurecomm.net",
    "ConnectionString": "endpoint=https://your-resource.communication.azure.com/;accesskey=YOUR_ACCESS_KEY"
  }
}
```

Or supply the connection string as a recipe step:

```json
{
  "steps": [
    {
      "name": "Settings",
      "AzureEmailSettings": {
        "DefaultSender": "DoNotReply@your-azure-domain.azurecomm.net",
        "ConnectionString": "endpoint=https://your-resource.communication.azure.com/;accesskey=YOUR_ACCESS_KEY"
      }
    }
  ]
}
```

## Sending Emails Programmatically

### Using ISmtpService

Inject `ISmtpService` to send emails from custom code. Build a `MailMessage` and call `SendAsync`:

```csharp
using Microsoft.Extensions.Localization;
using OrchardCore.Email;

public sealed class OrderConfirmationService
{
    private readonly ISmtpService _smtpService;
    private readonly IStringLocalizer S;

    public OrderConfirmationService(
        ISmtpService smtpService,
        IStringLocalizer<OrderConfirmationService> stringLocalizer)
    {
        _smtpService = smtpService;
        S = stringLocalizer;
    }

    public async Task<SmtpResult> SendOrderConfirmationAsync(
        string recipientEmail,
        string orderId)
    {
        var message = new MailMessage
        {
            To = recipientEmail,
            Subject = S["Order Confirmation - {0}", orderId].Value,
            Body = $"<p>Your order <strong>{orderId}</strong> has been confirmed.</p>",
            IsHtmlBody = true
        };

        return await _smtpService.SendAsync(message);
    }
}
```

Register the service in your module's `Startup`:

```csharp
using Microsoft.Extensions.DependencyInjection;
using OrchardCore.Modules;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<OrderConfirmationService>();
    }
}
```

### Checking the Result

`SmtpResult` indicates whether the send operation succeeded:

```csharp
var result = await _smtpService.SendAsync(message);

if (!result.Succeeded)
{
    foreach (var error in result.Errors)
    {
        logger.LogError("Email send failed: {Error}", error.Value);
    }
}
```

### MailMessage Properties

The `MailMessage` class exposes these key properties:

| Property | Type | Description |
|---|---|---|
| `From` | `string` | Sender address. Falls back to `DefaultSender` if empty. |
| `To` | `string` | Comma-separated list of recipient addresses. |
| `Cc` | `string` | Comma-separated list of CC addresses. |
| `Bcc` | `string` | Comma-separated list of BCC addresses. |
| `ReplyTo` | `string` | Reply-to address. |
| `Subject` | `string` | Message subject line. |
| `Body` | `string` | Message body (plain text or HTML). |
| `IsHtmlBody` | `bool` | When `true`, the body is treated as HTML. |
| `Attachments` | `List<MailMessageAttachment>` | File attachments. |

### Sending with Attachments

```csharp
public sealed class ReportEmailService
{
    private readonly ISmtpService _smtpService;

    public ReportEmailService(ISmtpService smtpService)
    {
        _smtpService = smtpService;
    }

    public async Task<SmtpResult> SendReportAsync(
        string recipientEmail,
        string reportName,
        Stream reportStream)
    {
        var message = new MailMessage
        {
            To = recipientEmail,
            Subject = $"Report: {reportName}",
            Body = "<p>Please find the attached report.</p>",
            IsHtmlBody = true
        };

        message.Attachments.Add(new MailMessageAttachment
        {
            Filename = $"{reportName}.pdf",
            Stream = reportStream
        });

        return await _smtpService.SendAsync(message);
    }
}
```

## Liquid Email Templates

Orchard Core's Liquid integration allows you to build dynamic email bodies. Use `ILiquidTemplateManager` to render templates before sending:

```csharp
using OrchardCore.Liquid;
using OrchardCore.Email;

public sealed class TemplatedEmailService
{
    private readonly ISmtpService _smtpService;
    private readonly ILiquidTemplateManager _liquidTemplateManager;

    public TemplatedEmailService(
        ISmtpService smtpService,
        ILiquidTemplateManager liquidTemplateManager)
    {
        _smtpService = smtpService;
        _liquidTemplateManager = liquidTemplateManager;
    }

    public async Task<SmtpResult> SendWelcomeEmailAsync(
        string recipientEmail,
        string userName)
    {
        var template = @"
<h1>Welcome, {{ UserName }}!</h1>
<p>Thank you for registering on our site.</p>
<p>Your account is now active and ready to use.</p>
";

        var model = new { UserName = userName };
        var body = await _liquidTemplateManager.RenderStringAsync(
            template,
            System.Text.Encodings.Web.HtmlEncoder.Default,
            model);

        var message = new MailMessage
        {
            To = recipientEmail,
            Subject = $"Welcome, {userName}!",
            Body = body,
            IsHtmlBody = true
        };

        return await _smtpService.SendAsync(message);
    }
}
```

### Liquid Syntax in Email Templates

Common Liquid constructs for email templates:

- **Variable output**: `{{ Model.PropertyName }}`
- **Conditionals**: `{% if Model.IsVip %} ... {% endif %}`
- **Loops**: `{% for item in Model.Items %} ... {% endfor %}`
- **Filters**: `{{ Model.Date | date: "%B %d, %Y" }}`
- **Content items**: `{% contentitem id: Model.ContentItemId, assign_model: "item" %}`

## Email Workflow Activities

When the `OrchardCore.Email` feature is enabled alongside `OrchardCore.Workflows`, a **Send Email** activity becomes available in the workflow editor.

### Send Email Activity Properties

| Property | Description |
|---|---|
| Sender | The "From" address. Defaults to the configured default sender. |
| Recipients | Comma-separated recipient addresses. Supports Liquid expressions. |
| CC | Comma-separated CC addresses. Supports Liquid expressions. |
| BCC | Comma-separated BCC addresses. Supports Liquid expressions. |
| Reply-To | Reply-to address. Supports Liquid expressions. |
| Subject | Email subject. Supports Liquid expressions. |
| Body | Email body. Supports full Liquid template syntax with HTML. |
| Is HTML Body | Whether the body should be treated as HTML. |

In workflow Liquid expressions, access the current workflow context with `{{ Workflow }}` and the triggering content item with `{{ ContentItem }}`.

### Example Workflow: Notify Admin on Content Publication

Create a workflow that sends an email when a content item is published:

1. Add a **Content Published Event** as the starting activity.
2. Connect it to a **Send Email** activity with:
   - **Recipients**: `admin@example.com`
   - **Subject**: `Content Published: {{ ContentItem.DisplayText }}`
   - **Body**:
     ```
     <p>The content item <strong>{{ ContentItem.DisplayText }}</strong> of type
     <em>{{ ContentItem.ContentType }}</em> was published.</p>
     <p>Published by: {{ Workflow.Input.Owner }}</p>
     ```

## Email Notification Events

Orchard Core raises email-related events that modules can hook into. Implement `IEmailNotificationEvents` or listen for specific email notification events to customize behavior before or after emails are sent.

### Custom Email Event Handler

```csharp
using OrchardCore.Email;
using OrchardCore.Email.Events;

public sealed class EmailAuditHandler : IEmailNotificationEvents
{
    private readonly ILogger<EmailAuditHandler> _logger;

    public EmailAuditHandler(ILogger<EmailAuditHandler> logger)
    {
        _logger = logger;
    }

    public Task SendingAsync(MailMessage message)
    {
        _logger.LogInformation(
            "Sending email to {Recipients} with subject '{Subject}'.",
            message.To,
            message.Subject);

        return Task.CompletedTask;
    }

    public Task SentAsync(MailMessage message)
    {
        _logger.LogInformation(
            "Email sent to {Recipients} successfully.",
            message.To);

        return Task.CompletedTask;
    }

    public Task FailedAsync(MailMessage message)
    {
        _logger.LogWarning(
            "Failed to send email to {Recipients}.",
            message.To);

        return Task.CompletedTask;
    }
}
```

Register the handler:

```csharp
using Microsoft.Extensions.DependencyInjection;
using OrchardCore.Email.Events;
using OrchardCore.Modules;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IEmailNotificationEvents, EmailAuditHandler>();
    }
}
```

## Testing Email Configuration

Use the admin **Email Test** page at **Configuration → Settings → Email → Test** to send a test message. This validates that SMTP or Azure Communication Services settings are correctly configured.

## Troubleshooting

| Symptom | Possible Cause |
|---|---|
| Emails not sent | SMTP feature not enabled or credentials are incorrect. |
| Authentication failures | Wrong username/password or encryption method mismatch. |
| Connection timeouts | Firewall blocking SMTP port, or incorrect host/port. |
| Azure emails rejected | Sender domain not verified in Azure Communication Services. |
| Liquid variables empty | Model properties not passed to the template correctly. |
