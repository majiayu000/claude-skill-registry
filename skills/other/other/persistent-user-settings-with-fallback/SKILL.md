---
name: "persistent-user-settings-with-fallback"
description: "Pattern for persisting user-chosen settings (paths, locations) with automatic fallback to defaults"
domain: "settings-management"
confidence: "high"
source: "material-library-repointing-design-review"
applies_to: ["desktop-host", "persistence"]
---

## Context

Use this pattern when your app needs to let users choose a custom location for a critical resource (file path, directory, data store) and must gracefully handle cases where the custom location becomes unavailable (deleted, disconnected USB drive, permissions revoked).

**Example:** Material library repointing, project directory selection, custom workspace location, database file location.

## Pattern

### 1. Separate the "Settings" Layer from the "Resource" Layer

- **Settings layer:** A small, focused JSON file (e.g., `app-settings.json`) that stores user choices. One file, one schema, read/written atomically.
- **Resource layer:** The actual business logic (repository, file I/O, etc.) that uses the resolved path.

```csharp
// Settings: what user chose
public class AppSettings
{
    public string? ActiveLibraryPath { get; set; }  // null = use default
}

// Resolution: get the actual path to use
public static string ResolveLibraryPath(AppSettings settings)
{
    return settings.ActiveLibraryPath ?? DefaultPath;
}

// Resource: doesn't know or care where it came from
var repository = new JsonMaterialRepository(ResolveLibraryPath(settings));
```

### 2. Implement Silent Fallback at Startup

If the custom setting points to an unavailable resource, **don't fail.** Silently fall back to the default and report a non-modal status message.

```csharp
public async Task InitializeAsync()
{
    var settings = LoadAppSettings();
    var resolvedPath = ResolveLibraryPath(settings);

    try
    {
        // Try to use user's choice
        _repository = new JsonMaterialRepository(resolvedPath);
        await _repository.GetAllAsync();  // Validate it works
        _statusMessage = $"Loaded materials from {resolvedPath}";
    }
    catch (Exception ex)
    {
        // Fall back to default silently
        _repository = new JsonMaterialRepository(DefaultPath);
        settings.ActiveLibraryPath = null;
        await SaveAppSettingsAsync(settings);  // Persist the revert
        _statusMessage = $"Could not access custom location ({ex.Message}). Using default.";
    }
}
```

### 3. Expose Change/Restore as Bridge Messages

**Two handlers:**

- `change-*-location`: Validate input, create if needed, persist setting, return confirmed path.
- `restore-default-*-location`: Clear the setting, create/validate default if needed, return default path.

Both handlers are idempotent and account for edge cases (path doesn't exist, permission denied, file corrupt).

```csharp
dispatcher.Register<ChangeLibraryLocationRequest>(
    "change-library-location",
    async (request, cancellationToken) =>
    {
        try
        {
            // Validate & create if needed
            var validatedPath = ValidateAndPrepareLibraryPath(request.NewLibraryPath);
            
            // Persist setting
            var settings = LoadAppSettings();
            settings.ActiveLibraryPath = validatedPath;
            await SaveAppSettingsAsync(settings);
            
            // Reload repository with new path
            _repository = new JsonMaterialRepository(validatedPath);
            await _repository.GetAllAsync();  // Sanity check
            
            return new ChangeLibraryLocationResponse
            {
                Success = true,
                LibraryPath = validatedPath,
                Message = $"Material library now points to {validatedPath}"
            };
        }
        catch (Exception ex)
        {
            return new ChangeLibraryLocationResponse
            {
                Success = false,
                Error = BridgeError.Create("invalid-path", ex.Message)
            };
        }
    });
```

### 4. Design Error Codes for User Clarity

Reuse generic codes but add context in the user message:

```csharp
public static string? ResolveUserMessage(string code, string message, string? userMessage)
{
    return code switch
    {
        "invalid-path" => 
            "The file path is invalid or cannot be accessed. Choose a different location.",
        "path-not-accessible" =>
            "The directory does not exist and could not be created. Check permissions.",
        "write-permission-denied" =>
            "You don't have permission to write to that location. Choose a different folder.",
        "invalid-library-file" =>
            "The file at that location is not a valid material library. Choose a different file.",
        // ... etc
        _ => message
    };
}
```

### 5. Settings File Format

Keep it minimal and human-readable:

```json
{
  "version": 1,
  "activeLibraryPath": "C:\\Users\\Alice\\Documents\\MyMaterials.json"
}
```

Or for null (use default):

```json
{
  "version": 1,
  "activeLibraryPath": null
}
```

Read strategy:
- If file doesn't exist → treat as empty (all settings are default).
- If file is corrupt JSON → log warning, ignore, use defaults.
- If a setting is null → treat as "not set, use built-in default."

### 6. Testing

**Unit tests:**
- Fallback when path is missing.
- Fallback when file is corrupt.
- Fallback when directory is not writable.
- Settings file is created and updated correctly.
- Null/missing settings fields are handled gracefully.

**Integration tests:**
- Change location, verify setting persists across app restart.
- Delete custom file, reopen app, verify fallback occurs.
- Restore default after custom path was set.
- Concurrent access (if relevant).

```csharp
[Fact]
public async Task WhenCustomPathIsDeletedAtStartup_FallsBackToDefault()
{
    var settings = new AppSettings { ActiveLibraryPath = "/invalid/path" };
    var host = new TestHost(settings);
    
    await host.InitializeAsync();
    
    Assert.Equal(DefaultPath, host.ResolvedPath);
Assert.Null(host.LoadedSettings.ActiveLibraryPath);  // Reverted
}
```

### 6b. Distinguish Explicit Repoint From Implicit Recovery

If the architecture forces the repository/resource layer to own the persisted location (instead of a separate settings host), keep **two different code paths**:

- **Explicit repoint/restore commands:** user intentionally chose a location, so normalize the path, validate it, and create/seed the file if that is part of the feature contract.
- **Implicit reload/restart recovery:** the app is reopening a previously stored custom path. If that file is now missing, corrupt, or fails validation, do **not** recreate it silently. Fall back to the canonical default resource and clear the stored override best-effort.

This distinction keeps recovery deterministic and explainable. It also avoids reviving a broken custom path forever just because the loader auto-seeds missing files.

### 7. UI Companion Pattern: Return Location + Refreshed Data Together

For WebView/desktop splits, location-changing handlers should return both the confirmed location metadata and the reloaded resource payload in one response. On the frontend, funnel `list`, `change`, and `restore default` through one shared state helper so the table contents, selection, and current-path UI refresh in the same reducer transition.

```ts
type MaterialLibraryResponse = {
  success: boolean;
  materials: Material[];
  libraryLocation?: MaterialLibraryLocation | null;
};

function applyMaterialLibraryResponse(response: MaterialLibraryResponse) {
  dispatch({
    type: 'materials-loaded',
    materials: response.materials,
    materialLibraryLocation: response.libraryLocation,
    selectedMaterialId: pickMaterialId(
      response.materials,
      selectionContext.importResponse,
      selectionContext.selectedMaterialId,
    ),
  });
}
```

### 8. UI Placement: Keep Path Controls With the Resource They Change

Show the current path and `Choose…` / `Restore default` actions inside the workspace that owns the resource (for PanelNester, the Materials page's Library panel), not in global chrome. Keep top-level chrome reserved for app-wide host state; path management is easier to scan when it sits next to the table it refreshes.

When the page also exposes a `Refresh` action for that resource, keep it in the same local control row. Splitting Refresh into separate page chrome makes it harder to reason about whether the path copy, table contents, and selection are all reflecting the same bridge response.

## Why It Works

✅ **Graceful degradation:** If user's choice becomes unavailable, app keeps working.
✅ **No modal errors:** Fallback is silent; status message is informational.
✅ **Transparent to domain logic:** Resource layer doesn't know about settings.
✅ **Backward compatible:** Missing settings file = use defaults, no migration needed.
✅ **User expectation:** "I chose X, if it breaks, go back to Y" is intuitive.

## Anti-Patterns

❌ **Don't embed the user choice inside the resource:** Leads to coupling and makes testing harder.
❌ **Don't throw exceptions on fallback:** Catch them and silently revert instead.
❌ **Don't split location updates from resource reloads in the UI:** Returning only the new path makes it easy to leave stale table/selection state behind.
❌ **Don't move resource-specific path controls into global chrome:** It hides the context operators need when the refreshed data lives on one page.
❌ **Don't nullish-fallback the displayed location to previous state in the reducer:** a bridge response that returns `null`/`undefined` for location metadata should clear stale path UI, not preserve it.
❌ **Don't require user interaction to recover:** Automatic fallback is better UX.
❌ **Don't use binary/encrypted formats for settings:** Keep it JSON for debuggability.

## Variants

- **Multiple settings:** If you have 5+ user choices (theme, workspace layout, etc.), use a single settings file with 5 fields instead of 5 separate files.
- **Scoped settings:** Per-project custom paths (e.g., project-specific materials file) use same pattern but store in project metadata.
- **Repository-owned recovery seam:** If you cannot keep path persistence outside the resource layer, expose explicit `RepointAsync`/`RestoreDefaultAsync` operations and keep implicit load fallback logic separate, as described above.
- **Notification on fallback:** If critical, notify user via a status banner or toast instead of silent status message.

## References

- Related skill: `webview2-user-data-relocation` — Similar pattern for runtime profile location.
- PanelNester implementation: `.squad/decisions/inbox/ripley-material-library-repointing.md`

### 3b. Host-Owned Picker Variant for Desktop/Web Bridges

When the frontend only needs to *request* a location change, keep the bridge payload empty and let the desktop host own the native picker. Use a save-style dialog for file-backed resources so the user can point at a new file path even when it does not exist yet, and disable overwrite prompts when the action is selecting a library location rather than overwriting confirmed data.

```csharp
dispatcher.Register<ChooseLibraryLocationRequest>(
    "choose-library-location",
    async (_, cancellationToken) =>
    {
        var dialogResult = await fileDialogService.SaveAsync(
            new SaveFileDialogRequest(
                "Choose library location",
                "materials.json",
                [new FileDialogFilter("Library files", ["json"])],
                ".json",
                overwritePrompt: false),
            cancellationToken);

        if (!dialogResult.Success || string.IsNullOrWhiteSpace(dialogResult.FilePath))
        {
            return ChooseLibraryLocationResponse.Cancelled();
        }

        var location = await locationService.RepointAsync(dialogResult.FilePath, cancellationToken);
        var materials = await materialService.ListAsync(cancellationToken);
        return new ChooseLibraryLocationResponse(true, materials, location, null, "Library updated.");
    });
```

Why this variant matters:
- The web side stays ignorant of native file-dialog details.
- The host returns one authoritative response with both refreshed data and confirmed location metadata.
- Explicit choose flows remain separate from restart-time fallback recovery.
