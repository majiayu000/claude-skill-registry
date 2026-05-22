---
name: umbraco-property-editor-schema
description: Implement property editor schemas in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Property Editor Schema

## What is it?
A Property Editor Schema defines the server-side metadata and configuration structure for a property editor - essentially the "blueprint" for how data is stored and processed. It's one half of a property editor (paired with a Property Editor UI). The schema determines data validation, storage format, and how property data is made available when rendering the website. Most custom editors can use built-in schemas; custom schemas are needed for specialized data handling.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/property-editors
- **Tutorial**: https://docs.umbraco.com/umbraco-cms/tutorials/creating-a-property-editor
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## When to Create a Custom Schema

Use a built-in schema when possible. Create a custom schema when you need:
- Custom server-side validation
- Special data transformation before storage
- Custom property value converters for rendering
- Complex data structures not covered by built-in schemas

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Can a built-in schema work? What data validation needed? Custom value converter?
3. **Generate files** - Create C# schema class if needed, or use built-in schema alias
4. **Explain** - Show what was created and how to test

## Built-in Schema Aliases

Use these in your Property Editor UI manifest's `propertyEditorSchemaAlias`:

| Alias | Use Case |
|-------|----------|
| `Umbraco.Plain.String` | Simple string, no validation |
| `Umbraco.Plain.Integer` | Simple integer |
| `Umbraco.Plain.Decimal` | Decimal numbers |
| `Umbraco.Plain.DateTime` | Date/time values |
| `Umbraco.Plain.Json` | JSON objects/arrays |
| `Umbraco.TextBox` | String with maxlength validation |
| `Umbraco.TextArea` | Multi-line text |
| `Umbraco.TrueFalse` | Boolean values |
| `Umbraco.ColorPicker` | Color values |
| `Umbraco.ContentPicker` | Content node references |
| `Umbraco.MediaPicker` | Media references |
| `Umbraco.MultiUrlPicker` | Multiple URL links |
| `Umbraco.Tags` | Tag collections |
| `Umbraco.RichText` | Rich text HTML |

## Minimal Examples

### Using Built-in Schema (Most Common)
```json
{
  "type": "propertyEditorUi",
  "alias": "My.PropertyEditorUi.Custom",
  "name": "My Custom Editor",
  "element": "/App_Plugins/MyEditor/editor.js",
  "meta": {
    "propertyEditorSchemaAlias": "Umbraco.Plain.String"
  }
}
```

### Custom Schema (C#) - Only When Needed
```csharp
using Umbraco.Cms.Core.IO;
using Umbraco.Cms.Core.PropertyEditors;
using Umbraco.Cms.Core.Services;

namespace MyPackage.PropertyEditors;

[DataEditor(
    alias: "My.PropertyEditor.Custom",
    name: "My Custom Editor",
    view: "~/App_Plugins/MyEditor/editor.html")]
public class MyPropertyEditor : DataEditor
{
    private readonly IIOHelper _ioHelper;
    private readonly IEditorConfigurationParser _editorConfigurationParser;

    public MyPropertyEditor(
        IDataValueEditorFactory dataValueEditorFactory,
        IIOHelper ioHelper,
        IEditorConfigurationParser editorConfigurationParser)
        : base(dataValueEditorFactory)
    {
        _ioHelper = ioHelper;
        _editorConfigurationParser = editorConfigurationParser;
        SupportsReadOnly = true;
    }

    protected override IConfigurationEditor CreateConfigurationEditor() =>
        new MyConfigurationEditor(_ioHelper, _editorConfigurationParser);
}
```

### Custom Configuration Editor
```csharp
using Umbraco.Cms.Core.IO;
using Umbraco.Cms.Core.PropertyEditors;
using Umbraco.Cms.Core.Services;

namespace MyPackage.PropertyEditors;

public class MyConfigurationEditor : ConfigurationEditor<MyConfiguration>
{
    public MyConfigurationEditor(
        IIOHelper ioHelper,
        IEditorConfigurationParser editorConfigurationParser)
        : base(ioHelper, editorConfigurationParser)
    {
    }
}

public class MyConfiguration
{
    [ConfigurationField("maxItems", "Maximum Items", "number")]
    public int MaxItems { get; set; } = 10;

    [ConfigurationField("allowNull", "Allow Empty", "boolean")]
    public bool AllowNull { get; set; } = true;
}
```

### Custom Value Converter
```csharp
using Umbraco.Cms.Core.Models.PublishedContent;
using Umbraco.Cms.Core.PropertyEditors;

namespace MyPackage.PropertyEditors;

public class MyValueConverter : PropertyValueConverterBase
{
    public override bool IsConverter(IPublishedPropertyType propertyType)
        => propertyType.EditorAlias == "My.PropertyEditor.Custom";

    public override Type GetPropertyValueType(IPublishedPropertyType propertyType)
        => typeof(MyModel);

    public override object? ConvertSourceToIntermediate(
        IPublishedElement owner,
        IPublishedPropertyType propertyType,
        object? source,
        bool preview)
    {
        if (source is string json && !string.IsNullOrEmpty(json))
        {
            return JsonSerializer.Deserialize<MyModel>(json);
        }
        return null;
    }
}
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
