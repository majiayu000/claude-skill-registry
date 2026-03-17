---
name: orchardcore-forms
description: Skill for building and managing forms in Orchard Core using the OrchardCore.Forms module. Covers form widget content types, form validation, form submissions with workflows, anti-forgery tokens, and custom form elements.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Forms - Prompt Templates

## Create and Configure Forms

You are an Orchard Core expert. Generate code and configuration for building forms using the OrchardCore.Forms module.

### Guidelines

- Enable the `OrchardCore.Forms` feature to use form widgets in content layouts.
- Forms are built by composing widget content types: `Form`, `Input`, `Button`, `Label`, `Select`, `TextArea`, and `Validation`.
- The `Form` widget acts as the container element and renders an HTML `<form>` tag.
- Each form element widget maps to a standard HTML form element with configurable attributes.
- Use the `FormInputElementPart` and `FormElementPart` to configure element names, IDs, and CSS classes.
- Anti-forgery tokens are included automatically in forms rendered by the `Form` widget.
- Pair forms with the `OrchardCore.Workflows` module to handle form submissions via the `HttpRequestEvent` or form-specific workflow events.
- Form validation is handled via `Validation` widgets that display model state errors for specific fields.
- Place form element widgets inside a `Form` widget using a `FlowPart` or zone-based layout.

### Enabling the Forms Feature

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Forms",
        "OrchardCore.Flows",
        "OrchardCore.Widgets"
      ],
      "disable": []
    }
  ]
}
```

### Form Widget Content Types

The `OrchardCore.Forms` module provides the following widget content types:

| Content Type | HTML Element | Purpose |
|---|---|---|
| `Form` | `<form>` | Container for all form elements. Configures method, action URL, and encoding type. |
| `Input` | `<input>` | Text, email, password, hidden, number, and other standard input types. |
| `Button` | `<button>` | Submit, reset, or custom buttons. |
| `Label` | `<label>` | Labels associated with form inputs via the `for` attribute. |
| `Select` | `<select>` | Dropdown lists and multi-select fields. |
| `TextArea` | `<textarea>` | Multi-line text input fields. |
| `Validation` | `<span>` | Displays validation error messages for a specific input element. |
| `ValidationSummary` | `<div>` | Displays a summary of all validation errors in the form. |

### Form Content Type Settings

The `Form` widget has these key settings:

- **Action** - The URL the form submits to. Leave empty to post back to the current page.
- **Method** - HTTP method: `GET` or `POST` (default is `POST`).
- **Encoding Type** - The `enctype` attribute: `application/x-www-form-urlencoded`, `multipart/form-data`, or `text/plain`.
- **Enable Anti-forgery Token** - When enabled, an anti-forgery token is automatically included in the form.
- **Workflow Type ID** - Associates a workflow to execute when the form is submitted.

### Input Element Configuration

The `Input` widget supports these HTML input types:

- `text` - Standard single-line text input.
- `email` - Email address input with browser validation.
- `password` - Masked password input.
- `number` - Numeric input with optional min/max.
- `hidden` - Hidden input for passing data.
- `checkbox` - Boolean checkbox input.
- `radio` - Radio button for single selection.
- `url` - URL input with browser validation.
- `tel` - Telephone number input.
- `date` - Date picker input.
- `color` - Color picker input.

### Input Element Properties

Each input element has the following configurable properties via `FormInputElementPart`:

- **Name** - The `name` attribute used for form submission and model binding.
- **Type** - The HTML input type (text, email, password, number, hidden, etc.).
- **Placeholder** - Placeholder text displayed when the field is empty.
- **Default Value** - The initial value of the input field.

And via `FormElementPart`:

- **Id** - The `id` attribute for the HTML element.
- **CSS Class** - Additional CSS classes applied to the element.

## Form Validation

### Using Validation Widgets

Add a `Validation` widget after each form input to display field-level error messages. Set the **For** property to the `name` attribute of the input element it validates.

Add a `ValidationSummary` widget at the top or bottom of the form to display a summary list of all validation errors.

### Server-Side Validation in Workflows

When processing form submissions in a workflow, use the `ValidateAntiforgeryTokenTask` activity to verify the anti-forgery token. Use a `ScriptTask` to perform custom validation and add model state errors:

```javascript
// In a ScriptTask within a workflow
var name = requestFormAsDict["Name"];

if (!name || name.trim() === "") {
    addModelError("Name", "The Name field is required.");
}

var email = requestFormAsDict["Email"];

if (!email || !email.includes("@")) {
    addModelError("Email", "Please enter a valid email address.");
}

if (modelState.isValid) {
    setOutcome("Valid");
} else {
    setOutcome("Invalid");
}
```

### Anti-Forgery Token Handling

- The `Form` widget automatically generates and embeds a `__RequestVerificationToken` hidden field when anti-forgery is enabled.
- When building custom form handlers or controllers, always validate the token using `[ValidateAntiForgeryToken]` or by including `ValidateAntiforgeryTokenTask` in your workflow.
- For AJAX form submissions, include the token in the request header as `RequestVerificationToken`.

## Form Submissions with Workflows

### Configuring a Form Workflow

1. Enable `OrchardCore.Workflows` and `OrchardCore.Workflows.Http`.
2. Create a workflow with an `HttpRequestEvent` or `FormSubmissionEvent` as the starting activity.
3. Add a `ValidateAntiforgeryTokenTask` as the first task after the event.
4. Use `ScriptTask` activities to read form data and perform validation.
5. Use `NotifyTask` to display success or error messages.
6. Use `HttpRedirectTask` to redirect after successful submission.

### Reading Form Data in Workflows

Access submitted form values through the `requestFormAsDict` object in workflow scripts:

```javascript
// Access form field values by their name attribute
var firstName = requestFormAsDict["FirstName"];
var lastName = requestFormAsDict["LastName"];
var email = requestFormAsDict["Email"];
var message = requestFormAsDict["Message"];

// Set workflow properties for use in subsequent activities
setProperty("FullName", firstName + " " + lastName);
setProperty("Email", email);
setProperty("Message", message);

setOutcome("Done");
```

### Sending Email from Form Submissions

After reading and validating form data, use a `SendEmailTask` to process the submission:

- Set **Subject**, **Body**, **Recipients** using Liquid templates that reference workflow properties.
- Example body template: `{{ Workflow.Properties.FullName }} submitted: {{ Workflow.Properties.Message }}`

## Creating Custom Form Elements

### Custom Form Element Content Part

```csharp
using OrchardCore.ContentManagement;

public sealed class RatingFieldPart : ContentPart
{
    public int MinValue { get; set; } = 1;
    public int MaxValue { get; set; } = 5;
    public int DefaultValue { get; set; } = 3;
    public string Label { get; set; }
    public string Name { get; set; }
}
```

### Custom Form Element Display Driver

```csharp
using OrchardCore.ContentManagement.Display.ContentDisplay;
using OrchardCore.ContentManagement.Display.Models;
using OrchardCore.DisplayManagement.ModelBinding;
using OrchardCore.DisplayManagement.Views;

public sealed class RatingFieldPartDisplayDriver : ContentPartDisplayDriver<RatingFieldPart>
{
    public override IDisplayResult Display(RatingFieldPart part, BuildPartDisplayContext context)
    {
        return Initialize<RatingFieldPartViewModel>("RatingFieldPart", model =>
        {
            model.MinValue = part.MinValue;
            model.MaxValue = part.MaxValue;
            model.DefaultValue = part.DefaultValue;
            model.Label = part.Label;
            model.Name = part.Name;
        }).Location("Detail", "Content");
    }

    public override IDisplayResult Edit(RatingFieldPart part, BuildPartEditorContext context)
    {
        return Initialize<RatingFieldPartViewModel>("RatingFieldPart_Edit", model =>
        {
            model.MinValue = part.MinValue;
            model.MaxValue = part.MaxValue;
            model.DefaultValue = part.DefaultValue;
            model.Label = part.Label;
            model.Name = part.Name;
        }).Location("Content");
    }

    public override async Task<IDisplayResult> UpdateAsync(
        RatingFieldPart part,
        UpdatePartEditorContext context)
    {
        var model = new RatingFieldPartViewModel();
        await context.Updater.TryUpdateModelAsync(model, Prefix);

        part.MinValue = model.MinValue;
        part.MaxValue = model.MaxValue;
        part.DefaultValue = model.DefaultValue;
        part.Label = model.Label;
        part.Name = model.Name;

        return Edit(part, context);
    }
}
```

### Registering a Custom Form Element

```csharp
using OrchardCore.ContentManagement;
using OrchardCore.ContentManagement.Display.ContentDisplay;
using OrchardCore.Modules;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddContentPart<RatingFieldPart>()
            .UseDisplayDriver<RatingFieldPartDisplayDriver>();
    }
}
```

### Custom Form Element Migration

```csharp
using OrchardCore.ContentManagement.Metadata;
using OrchardCore.ContentManagement.Metadata.Settings;
using OrchardCore.Data.Migration;

public sealed class Migrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public Migrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public async Task<int> CreateAsync()
    {
        await _contentDefinitionManager.AlterPartDefinitionAsync("RatingFieldPart", part => part
            .Attachable()
            .WithDescription("Renders a rating input element in a form.")
        );

        await _contentDefinitionManager.AlterTypeDefinitionAsync("RatingField", type => type
            .DisplayedAs("Rating Field")
            .Stereotype("Widget")
            .WithPart("RatingFieldPart")
        );

        return 1;
    }
}
```

## Form Element Placement and Styling

### Placement in FlowPart

Form elements are arranged inside a `Form` widget using `FlowPart`. Each element widget is a child of the flow and is rendered in the order it appears.

Typical form structure:

1. `Form` (container with method, action, and encoding settings)
   - `Label` (for first input)
   - `Input` (first input field)
   - `Validation` (validation message for first input)
   - `Label` (for second input)
   - `TextArea` (second input field)
   - `Validation` (validation message for second input)
   - `ValidationSummary` (summary of all errors)
   - `Button` (submit button)

### Applying CSS Classes

Use the `FormElementPart` CSS Class property to apply styling classes:

- Bootstrap classes: `form-control`, `form-select`, `btn btn-primary`, `form-label`.
- Custom CSS classes for project-specific styling.
- Wrapper classes for layout: `mb-3`, `row`, `col-md-6`.

### Select Element Options

The `Select` widget options are defined as a list of text entries with one option per line. Each line uses the format `value=Display Text` or simply `Display Text` (where the display text is used as both value and label).

### Button Types

The `Button` widget supports these types:

- `submit` - Submits the form.
- `reset` - Resets form fields to default values.
- `button` - A generic button for custom JavaScript actions.

## Recipe Configuration for Forms

### Creating a Contact Form via Recipe

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Forms",
        "OrchardCore.Flows",
        "OrchardCore.Widgets",
        "OrchardCore.Workflows",
        "OrchardCore.Workflows.Http"
      ],
      "disable": []
    }
  ]
}
```

### Content Definition for a Form Page

```json
{
  "steps": [
    {
      "name": "ContentDefinition",
      "ContentTypes": [
        {
          "Name": "FormPage",
          "DisplayName": "Form Page",
          "Settings": {
            "ContentTypeSettings": {
              "Creatable": true,
              "Listable": true,
              "Draftable": true
            }
          },
          "ContentTypePartDefinitionRecords": [
            {
              "PartName": "TitlePart",
              "Name": "TitlePart",
              "Settings": {
                "ContentTypePartSettings": {
                  "Position": "0"
                }
              }
            },
            {
              "PartName": "AutoroutePart",
              "Name": "AutoroutePart",
              "Settings": {
                "ContentTypePartSettings": {
                  "Position": "1"
                },
                "AutoroutePartSettings": {
                  "AllowCustomPath": true,
                  "Pattern": "{{ ContentItem | display_text | slugify }}"
                }
              }
            },
            {
              "PartName": "FlowPart",
              "Name": "FlowPart",
              "Settings": {
                "ContentTypePartSettings": {
                  "Position": "2"
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```
