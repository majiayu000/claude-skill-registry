---
name: humanizer
description: >
  Guidance for Humanizer library for .NET string, date, number, and enum formatting.
  USE FOR: human-readable date/time formatting, pluralization, number-to-words conversion, enum display names, truncation, byte size formatting, casing transformations.
  DO NOT USE FOR: localization infrastructure (use IStringLocalizer), parsing human input back to types, business logic, data storage formatting.
license: MIT
metadata:
  displayName: Humanizer
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Humanizer GitHub Repository"
    url: "https://github.com/Humanizr/Humanizer"
  - title: "Humanizer NuGet Package"
    url: "https://www.nuget.org/packages/Humanizer"
  - title: "Humanizer.Core NuGet Package"
    url: "https://www.nuget.org/packages/Humanizer.Core"
---

# Humanizer

## Overview

Humanizer is a .NET library that manipulates and displays strings, enums, dates, times, timespans, numbers, and quantities in a human-friendly format. It provides extension methods that transform programmatic values into natural language and vice versa. Humanizer supports over 40 languages for localized output.

The library is designed for presentation layers where raw data values need to be displayed as readable text. It converts `DateTime` differences into phrases like "3 hours ago", numbers into words, enums into display-friendly strings, and byte counts into formatted sizes.

Install via NuGet:
```
dotnet add package Humanizer
```

## Date and Time Humanization

Transform `DateTime` and `TimeSpan` values into human-readable relative time strings.

```csharp
using System;
using Humanizer;

// Relative time from DateTime
var pastDate = DateTime.UtcNow.AddHours(-3);
Console.WriteLine(pastDate.Humanize()); // "3 hours ago"

var futureDate = DateTime.UtcNow.AddDays(2);
Console.WriteLine(futureDate.Humanize()); // "2 days from now"

// TimeSpan humanization with precision
var duration = TimeSpan.FromMinutes(187);
Console.WriteLine(duration.Humanize()); // "3 hours"
Console.WriteLine(duration.Humanize(precision: 2)); // "3 hours, 7 minutes"

var uptime = TimeSpan.FromSeconds(93784);
Console.WriteLine(uptime.Humanize(precision: 3)); // "1 day, 2 hours, 3 minutes"

// DateTimeOffset support
var offset = DateTimeOffset.UtcNow.AddMinutes(-45);
Console.WriteLine(offset.Humanize()); // "45 minutes ago"
```

## String Transformations

Humanizer provides extensive string manipulation including casing, truncation, and word transformations.

```csharp
using Humanizer;

// Case transformations
Console.WriteLine("PascalCaseProperty".Humanize()); // "Pascal case property"
Console.WriteLine("some_database_column".Humanize()); // "Some database column"
Console.WriteLine("HTML parser".Humanize()); // "HTML parser"

// Specific casing
Console.WriteLine("the quick brown fox".Pascalize()); // "TheQuickBrownFox"
Console.WriteLine("the quick brown fox".Camelize()); // "theQuickBrownFox"
Console.WriteLine("the quick brown fox".Underscore()); // "the_quick_brown_fox"
Console.WriteLine("the quick brown fox".Kebaberize()); // "the-quick-brown-fox"
Console.WriteLine("the quick brown fox".Transform(To.TitleCase)); // "The Quick Brown Fox"
Console.WriteLine("the quick brown fox".Transform(To.SentenceCase)); // "The quick brown fox"

// Truncation
Console.WriteLine("Long descriptive text here".Truncate(15)); // "Long descriptiv..."
Console.WriteLine("Long descriptive text here".Truncate(15, Truncator.FixedNumberOfWords));
Console.WriteLine("Long text here".Truncate(10, "---")); // "Long te---"
```

## Pluralization and Singularization

Convert between singular and plural forms of English words.

```csharp
using Humanizer;

// Pluralize
Console.WriteLine("person".Pluralize()); // "people"
Console.WriteLine("mouse".Pluralize()); // "mice"
Console.WriteLine("criterion".Pluralize()); // "criteria"
Console.WriteLine("octopus".Pluralize()); // "octopi"

// Singularize
Console.WriteLine("people".Singularize()); // "person"
Console.WriteLine("mice".Singularize()); // "mouse"
Console.WriteLine("categories".Singularize()); // "category"

// Quantity-aware formatting
Console.WriteLine("item".ToQuantity(0)); // "0 items"
Console.WriteLine("item".ToQuantity(1)); // "1 item"
Console.WriteLine("item".ToQuantity(5)); // "5 items"
Console.WriteLine("item".ToQuantity(5, ShowQuantityAs.Words)); // "five items"
```

## Number to Words and Ordinals

Convert numeric values to their word representations and ordinal forms.

```csharp
using Humanizer;

// Numbers to words
Console.WriteLine(42.ToWords()); // "forty-two"
Console.WriteLine(1234.ToWords()); // "one thousand two hundred and thirty-four"

// Ordinals
Console.WriteLine(1.Ordinalize()); // "1st"
Console.WriteLine(2.Ordinalize()); // "2nd"
Console.WriteLine(3.Ordinalize()); // "3rd"
Console.WriteLine(11.Ordinalize()); // "11th"
Console.WriteLine(21.Ordinalize()); // "21st"

// Ordinal words
Console.WriteLine(1.ToOrdinalWords()); // "first"
Console.WriteLine(21.ToOrdinalWords()); // "twenty-first"

// Roman numerals
Console.WriteLine(2025.ToRoman()); // "MMXXV"
Console.WriteLine("XIV".FromRoman()); // 14
```

## Enum Humanization

Display enum values as human-readable strings using `[Description]` attributes or automatic PascalCase splitting.

```csharp
using System.ComponentModel;
using Humanizer;

public enum OrderStatus
{
    [Description("Awaiting Payment")]
    PendingPayment,

    [Description("Being Processed")]
    InProcessing,

    Shipped,

    [Description("Delivered to Customer")]
    Delivered,

    ReturnRequested
}

// Humanize enums
Console.WriteLine(OrderStatus.PendingPayment.Humanize()); // "Awaiting Payment"
Console.WriteLine(OrderStatus.InProcessing.Humanize()); // "Being Processed"
Console.WriteLine(OrderStatus.Shipped.Humanize()); // "Shipped"
Console.WriteLine(OrderStatus.ReturnRequested.Humanize()); // "Return requested"

// Dehumanize back to enum
var status = "Awaiting Payment".DehumanizeTo<OrderStatus>(); // OrderStatus.PendingPayment
```

## Byte Size Formatting

Format byte counts into human-readable file sizes.

```csharp
using Humanizer;
using Humanizer.Bytes;

var fileSize = ByteSize.FromBytes(1548576);
Console.WriteLine(fileSize.ToString()); // "1.48 MB"
Console.WriteLine(fileSize.Humanize()); // "1.48 MB"

// Specific units
Console.WriteLine(ByteSize.FromKilobytes(512).ToString()); // "512 KB"
Console.WriteLine(ByteSize.FromGigabytes(2.5).ToString()); // "2.5 GB"

// Arithmetic
var total = ByteSize.FromMegabytes(100) + ByteSize.FromMegabytes(250);
Console.WriteLine(total.Humanize()); // "350 MB"

// Per-second rates
Console.WriteLine(ByteSize.FromMegabytes(10).Per(TimeSpan.FromSeconds(1)).Humanize());
// "10 MB/s"
```

## Localization

Humanizer supports localized output by setting the current culture.

```csharp
using System.Globalization;
using Humanizer;

// German
var deCulture = new CultureInfo("de-DE");
Console.WriteLine(DateTime.UtcNow.AddHours(-3).Humanize(culture: deCulture));
// "vor 3 Stunden"

// French
var frCulture = new CultureInfo("fr-FR");
Console.WriteLine(42.ToWords(frCulture)); // "quarante-deux"
Console.WriteLine(DateTime.UtcNow.AddDays(-1).Humanize(culture: frCulture));
// "hier"
```

## Best Practices

1. **Use Humanizer only at presentation boundaries** (UI, API responses, notifications) -- never store humanized strings in databases or use them for logic.
2. **Cache compiled templates or precomputed humanized values** when rendering lists, since calling `.Humanize()` in tight loops on thousands of items adds measurable overhead.
3. **Pass `CultureInfo` explicitly** when localizing output rather than relying on `Thread.CurrentThread.CurrentCulture`, which can change unexpectedly in async code.
4. **Use `.ToQuantity()` for count-dependent labels** like "3 items" instead of manually concatenating count + pluralized noun.
5. **Annotate enums with `[Description]`** for display text that differs from the member name, and rely on `.Humanize()` for simple PascalCase splitting.
6. **Prefer `.Truncate()` with a word-based truncator** for user-facing text to avoid cutting words in half.
7. **Use `ByteSize` for file and bandwidth formatting** instead of manual division-by-1024 logic, which is error-prone and inconsistent.
8. **Specify precision in `TimeSpan.Humanize(precision: N)`** to control how many time units appear (e.g., "2 hours, 30 minutes" vs. "2 hours").
9. **Avoid `.Humanize()` on untrusted user input strings** -- Humanizer assumes well-formed PascalCase or snake_case identifiers and may produce unexpected output on arbitrary text.
10. **Use `.Dehumanize()` and `.DehumanizeTo<T>()`** only for round-tripping display strings back to enums or known values, not for parsing arbitrary user input.
