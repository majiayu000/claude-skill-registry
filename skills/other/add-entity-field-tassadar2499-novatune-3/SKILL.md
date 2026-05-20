---
description: Add a new field to an existing entity/model with related service and endpoint updates
---
# Add Entity Field Skill

Add a new field to an existing entity/model in the NovaTune project.

## Steps

1. **Identify the entity file**
   - Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/`
   - File naming: `{EntityName}.cs`

2. **Add the property to the entity class**
   ```csharp
   public required string NewFieldName { get; set; }
   // Or for optional fields:
   public string? OptionalFieldName { get; set; }
   ```

3. **Update related services**
   - Check `src/NovaTuneApp/NovaTuneApp.ApiService/Services/` for services that use this entity
   - Update DTOs if they exist
   - Update any mapping logic

4. **Update endpoints**
   - Check `src/NovaTuneApp/NovaTuneApp.ApiService/Endpoints/` for affected endpoints
   - Update request/response models if needed

5. **Update RavenDB indexes if applicable**
   - Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/RavenDb/`
   - Add field to index if it will be queried

6. **Add tests**
   - Unit tests: `src/unit_tests/`
   - Integration tests: `src/NovaTuneApp/NovaTuneApp.Tests/`

## Code Style

- Use `required` for mandatory fields
- Use nullable reference types (`?`) for optional fields
- PascalCase for property names
- Add XML documentation comments for public APIs