---
name: app-configuration
description: >
  Application configuration options reference for the HMIS project. Use when working with
  feature toggles, configuration keys, configOptionApplicationController, bill number
  configuration, printer configuration, or any configurable application behavior.
user-invocable: true
---

# Application Configuration Guide

## Configuration System

HMIS uses `configOptionApplicationController` for feature toggles and runtime configuration.

### Usage Pattern

```xhtml
<!-- Boolean toggle with default false -->
rendered="#{configOptionApplicationController.getBooleanValueByKey('Feature Key')}"

<!-- Boolean toggle with explicit default true -->
rendered="#{configOptionApplicationController.getBooleanValueByKey('Feature Key', true)}"
```

### Key Naming Convention

- Use descriptive, hierarchical names
- Module prefix: `Pharmacy Transfer Issue - Show Rate and Value`
- Report columns: `Pharmacy Disbursement Reports - Display Serial Number`

## Configuration Categories

### Pharmacy Transfer
- Rate display toggles (Purchase/Cost/Retail Rate)
- Bill format options (POS, Template)
- Footer customization (CSS and text)

### Report Display
- Column visibility toggles per report type
- Font size settings
- Serial number display

### Bill Number
- Prefix and year counting strategies
- Department-specific number generation

### Printer
- Printing profiles and templates
- Per-department printer assignment

For complete reference, read:
- [Application Options](../../developer_docs/configuration/application-options.md)
- [Bill Number Config](../../developer_docs/configuration/bill-number-config-options.md)
- [Printer Configuration](../../developer_docs/configuration/printer-configuration-system.md)
