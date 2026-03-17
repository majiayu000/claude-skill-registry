---
name: orchardcore-data-migrations
description: Skill for creating data migrations in Orchard Core. Covers content type migrations, YesSql index table creation, schema alterations, data seeding, and migration versioning patterns.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Data Migrations - Prompt Templates

## Create Data Migrations

You are an Orchard Core expert. Generate data migration code for Orchard Core modules.

### Guidelines

- Data migrations inherit from `DataMigration`.
- Migrations define content types, parts, fields, and database indexes.
- Use `CreateAsync()` for initial migration, `UpdateFrom1Async()`, `UpdateFrom2Async()` for incremental updates.
- Register migrations in `Startup.cs` using `services.AddScoped<IDataMigration, Migrations>()`.
- `IContentDefinitionManager` is used to define content types and parts.
- `SchemaBuilder` is used to create and alter YesSql index tables.
- Always seal classes.

### Basic Migration with Content Type

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
        await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
            .DisplayedAs("{{DisplayName}}")
            .Creatable()
            .Listable()
            .Draftable()
            .Versionable()
            .WithPart("TitlePart", part => part.WithPosition("0"))
            .WithPart("AutoroutePart", part => part
                .WithPosition("1")
                .WithSettings(new AutoroutePartSettings
                {
                    AllowCustomPath = true,
                    Pattern = "{{ ContentItem | display_text | slugify }}"
                })
            )
            .WithPart("HtmlBodyPart", part => part
                .WithPosition("2")
                .WithEditor("Wysiwyg")
            )
            .WithPart("{{ContentType}}Part", part => part.WithPosition("3"))
        );

        return 1;
    }
}
```

### Migration with Custom Content Part and Fields

```csharp
public sealed class Migrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public Migrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public async Task<int> CreateAsync()
    {
        // Define the custom part with fields
        await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
            .WithField("{{FieldName}}", field => field
                .OfType("TextField")
                .WithDisplayName("{{FieldDisplayName}}")
                .WithPosition("0")
                .WithSettings(new TextFieldSettings
                {
                    Required = true,
                    Hint = "{{FieldHint}}"
                })
            )
            .WithField("Description", field => field
                .OfType("TextField")
                .WithDisplayName("Description")
                .WithPosition("1")
                .WithEditor("TextArea")
            )
            .WithField("Image", field => field
                .OfType("MediaField")
                .WithDisplayName("Image")
                .WithPosition("2")
            )
        );

        // Define the content type with the custom part
        await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
            .DisplayedAs("{{DisplayName}}")
            .Creatable()
            .Listable()
            .WithPart("TitlePart", part => part.WithPosition("0"))
            .WithPart("{{PartName}}", part => part.WithPosition("1"))
        );

        return 1;
    }
}
```

### Migration with YesSql Index Table

```csharp
using OrchardCore.Data.Migration;
using YesSql.Sql;

public sealed class Migrations : DataMigration
{
    public async Task<int> CreateAsync()
    {
        await SchemaBuilder.CreateMapIndexTableAsync<{{IndexName}}>(table => table
            .Column<string>(nameof({{IndexName}}.ContentItemId), col => col.WithLength(26))
            .Column<string>(nameof({{IndexName}}.{{PropertyName}}), col => col.WithLength(256))
            .Column<bool>(nameof({{IndexName}}.Published))
            .Column<DateTime>(nameof({{IndexName}}.CreatedUtc))
        );

        await SchemaBuilder.AlterIndexTableAsync<{{IndexName}}>(table => table
            .CreateIndex(
                "IDX_{{IndexName}}_{{PropertyName}}",
                nameof({{IndexName}}.{{PropertyName}}),
                nameof({{IndexName}}.Published)
            )
        );

        return 1;
    }
}
```

### Incremental Migration (UpdateFrom)

```csharp
public sealed class Migrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public Migrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public async Task<int> CreateAsync()
    {
        // Initial migration
        await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
            .DisplayedAs("{{DisplayName}}")
            .Creatable()
            .Listable()
            .WithPart("TitlePart")
        );

        return 1;
    }

    public async Task<int> UpdateFrom1Async()
    {
        // Add a new field in version 2
        await _contentDefinitionManager.AlterPartDefinitionAsync("{{ContentType}}", part => part
            .WithField("Category", field => field
                .OfType("TextField")
                .WithDisplayName("Category")
                .WithPosition("2")
            )
        );

        return 2;
    }

    public async Task<int> UpdateFrom2Async()
    {
        // Add an index table in version 3
        await SchemaBuilder.CreateMapIndexTableAsync<{{ContentType}}Index>(table => table
            .Column<string>("ContentItemId", col => col.WithLength(26))
            .Column<string>("Category", col => col.WithLength(256))
            .Column<bool>("Published")
        );

        return 3;
    }
}
```

### Registering Migrations and Indexes

```csharp
using OrchardCore.Data.Migration;
using YesSql.Indexes;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IDataMigration, Migrations>();
        services.AddIndexProvider<{{IndexName}}Provider>();
    }
}
```

### Uninstall Migration

Handle cleanup when a feature is disabled:

```csharp
public sealed class Migrations : DataMigration
{
    public async Task UninstallAsync()
    {
        await SchemaBuilder.DropMapIndexTableAsync<{{IndexName}}>();
    }
}
```
