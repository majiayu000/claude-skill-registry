---
name: extensions-compliance
description: >
  Guidance for Microsoft.Extensions.Compliance data classification and redaction.
  USE FOR: classifying sensitive data (PII, EUII, financial), redacting log output, enforcing data handling policies, compliance-aware telemetry, audit-safe logging pipelines.
  DO NOT USE FOR: encryption at rest (use Data Protection APIs), access control/authorization (use ASP.NET Identity), GDPR consent management, full DLP solutions.
license: MIT
metadata:
  displayName: Compliance
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Data Redaction in .NET Documentation on Microsoft Learn"
    url: "https://learn.microsoft.com/dotnet/core/extensions/data-redaction"
  - title: "Microsoft.Extensions.Compliance.Redaction NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.Compliance.Redaction"
  - title: "Microsoft.Extensions.Compliance.Abstractions NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.Compliance.Abstractions"
---

# Microsoft.Extensions.Compliance

## Overview

`Microsoft.Extensions.Compliance` provides a framework for classifying data by sensitivity level and automatically redacting sensitive values in logging and telemetry pipelines. It integrates with `Microsoft.Extensions.Logging` to ensure that PII, financial data, and other regulated information is never written to logs in plain text.

The library uses a taxonomy-based approach: you define data classification attributes (e.g., `PersonalData`, `FinancialData`) and apply them to log message parameters. At runtime, a configured `IRedactorProvider` selects the appropriate redactor for each classification, replacing sensitive values before they reach log sinks.

Install via NuGet:
```
dotnet add package Microsoft.Extensions.Compliance.Abstractions
dotnet add package Microsoft.Extensions.Compliance.Redaction
```

## Defining Data Classifications

Data classifications are defined as static taxonomy instances. Each classification represents a sensitivity category that maps to a redaction strategy.

```csharp
using Microsoft.Extensions.Compliance.Classification;

public static class DataTaxonomy
{
    public static DataClassificationSet PersonalData { get; } =
        new DataClassificationSet(new DataClassification("MyApp", "PersonalData"));

    public static DataClassificationSet FinancialData { get; } =
        new DataClassificationSet(new DataClassification("MyApp", "FinancialData"));

    public static DataClassificationSet InternalOnly { get; } =
        new DataClassificationSet(new DataClassification("MyApp", "InternalOnly"));
}
```

## Creating Classification Attributes

Define attributes that map to your taxonomy for use on log message parameters and model properties.

```csharp
using System;
using Microsoft.Extensions.Compliance.Classification;

public class PersonalDataAttribute : DataClassificationAttribute
{
    public PersonalDataAttribute()
        : base(DataTaxonomy.PersonalData) { }
}

public class FinancialDataAttribute : DataClassificationAttribute
{
    public FinancialDataAttribute()
        : base(DataTaxonomy.FinancialData) { }
}

public class InternalOnlyAttribute : DataClassificationAttribute
{
    public InternalOnlyAttribute()
        : base(DataTaxonomy.InternalOnly) { }
}
```

## Using Classifications in Logging

Apply classification attributes to log message parameters. The logging infrastructure uses the registered redactor to transform classified values before writing.

```csharp
using Microsoft.Extensions.Logging;

public static partial class LogMessages
{
    [LoggerMessage(Level = LogLevel.Information,
        Message = "Processing order {OrderId} for user {UserEmail}")]
    public static partial void OrderProcessed(
        ILogger logger,
        string orderId,
        [PersonalData] string userEmail);

    [LoggerMessage(Level = LogLevel.Information,
        Message = "Payment of {Amount} received from card {CardNumber}")]
    public static partial void PaymentReceived(
        ILogger logger,
        [FinancialData] decimal amount,
        [FinancialData] string cardNumber);

    [LoggerMessage(Level = LogLevel.Debug,
        Message = "User profile loaded: {UserId}, {FullName}")]
    public static partial void ProfileLoaded(
        ILogger logger,
        [InternalOnly] string userId,
        [PersonalData] string fullName);
}
```

## Implementing Custom Redactors

A redactor transforms a classified value into a safe representation. Implement `Redactor` for custom strategies such as hashing, masking, or replacing with a fixed string.

```csharp
using System;
using Microsoft.Extensions.Compliance.Redaction;

public class HashingRedactor : Redactor
{
    public override int GetRedactedLength(ReadOnlySpan<char> input) => 16;

    public override int Redact(ReadOnlySpan<char> source, Span<char> destination)
    {
        var hash = source.ToString().GetHashCode();
        var redacted = $"HASH:{hash:X8}____";
        redacted.AsSpan().CopyTo(destination);
        return redacted.Length;
    }
}

public class MaskingRedactor : Redactor
{
    private const string MaskedValue = "***REDACTED***";

    public override int GetRedactedLength(ReadOnlySpan<char> input) => MaskedValue.Length;

    public override int Redact(ReadOnlySpan<char> source, Span<char> destination)
    {
        MaskedValue.AsSpan().CopyTo(destination);
        return MaskedValue.Length;
    }
}
```

## Registering Redactors with DI

Configure the redaction pipeline in your host builder. Map each data classification to a specific redactor implementation.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Compliance.Redaction;
using Microsoft.Extensions.Compliance.Classification;

var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddRedaction(redaction =>
{
    // Personal data gets hashed for correlation without exposure
    redaction.SetRedactor<HashingRedactor>(DataTaxonomy.PersonalData);

    // Financial data is fully masked
    redaction.SetRedactor<MaskingRedactor>(DataTaxonomy.FinancialData);

    // Internal data uses the built-in erasing redactor
    redaction.SetRedactor<ErasingRedactor>(DataTaxonomy.InternalOnly);
});

// Enable compliance-aware logging
builder.Logging.EnableRedaction();

builder.Services.AddTransient<OrderService>();

using var host = builder.Build();
await host.RunAsync();
```

## Using IRedactorProvider Directly

You can also redact values programmatically outside of the logging pipeline using `IRedactorProvider`.

```csharp
using Microsoft.Extensions.Compliance.Classification;
using Microsoft.Extensions.Compliance.Redaction;

public class AuditService
{
    private readonly IRedactorProvider _redactorProvider;

    public AuditService(IRedactorProvider redactorProvider)
    {
        _redactorProvider = redactorProvider;
    }

    public string RedactForAudit(string sensitiveValue, DataClassificationSet classification)
    {
        var redactor = _redactorProvider.GetRedactor(classification);
        return redactor.Redact(sensitiveValue);
    }

    public void WriteAuditEntry(string userId, string email)
    {
        var safeUserId = RedactForAudit(userId, DataTaxonomy.InternalOnly);
        var safeEmail = RedactForAudit(email, DataTaxonomy.PersonalData);

        // Write to audit log with redacted values
        Console.WriteLine($"Audit: user={safeUserId}, email={safeEmail}");
    }
}
```

## Redaction Strategies Comparison

| Strategy | Redactor | Reversible | Use Case |
|----------|----------|------------|----------|
| Erasing | `ErasingRedactor` | No | Remove entirely, highest security |
| Hashing | Custom `HashingRedactor` | No | Correlate events without exposing value |
| Masking | Custom `MaskingRedactor` | No | Show redacted placeholder |
| Partial masking | Custom | No | Show last 4 digits (e.g., card numbers) |
| Pass-through | None (no redactor set) | Yes | Non-sensitive data, no transformation |

## Best Practices

1. **Define a centralized data taxonomy** in a shared project so all services in your solution use the same classification names and consistent redaction behavior.
2. **Apply classification attributes on every log parameter that contains PII** including email addresses, names, IP addresses, phone numbers, and user identifiers.
3. **Enable redaction on the logging builder** with `builder.Logging.EnableRedaction()` -- without this call, classification attributes are ignored and sensitive data is logged in plain text.
4. **Use `ErasingRedactor` as the default fallback** for any unclassified sensitive data to ensure nothing leaks if a classification is missing.
5. **Use hashing redactors for correlation** so you can trace a user's activity across log entries without storing their actual identity.
6. **Test redaction in unit tests** by resolving `IRedactorProvider` from a test service provider and verifying that classified values are transformed correctly.
7. **Avoid logging sensitive values outside the structured logging pipeline** -- if you use string interpolation with `Console.WriteLine`, the redaction system is bypassed entirely.
8. **Classify financial data separately from PII** because regulatory requirements (PCI-DSS vs GDPR) may require different retention and redaction strategies.
9. **Review log output after enabling redaction** to confirm that no sensitive values leak through unclassified parameters or exception messages.
10. **Combine compliance redaction with log filtering** to ensure that debug-level logs containing classified data are not emitted in production, even if redaction is applied.
