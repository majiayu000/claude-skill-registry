---
name: settings-hierarchy
description: Hierarchical settings patterns for SaaS. Covers org, team, and user-level settings with inheritance and override patterns.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason
---

# Settings Hierarchy Skill

## When to Use This Skill

Use this skill when:

- **Settings Hierarchy tasks** - Working on hierarchical settings patterns for saas. covers org, team, and user-level settings with inheritance and override patterns
- **Planning or design** - Need guidance on Settings Hierarchy approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Patterns for implementing multi-level settings with inheritance in SaaS applications.

SaaS applications need settings at multiple levels - organization defaults, team overrides, and user preferences. This skill covers how to structure, store, and resolve hierarchical settings.

## Settings Hierarchy

```text
+------------------------------------------------------------------+
|                    Settings Hierarchy                             |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------+                                             |
|  | System Defaults  |  (hardcoded/config)                        |
|  +------------------+                                             |
|           |                                                       |
|           v                                                       |
|  +------------------+                                             |
|  | Org/Tenant       |  (tenant admins set)                       |
|  | Settings         |                                             |
|  +------------------+                                             |
|           |                                                       |
|           v                                                       |
|  +------------------+                                             |
|  | Team/Workspace   |  (team leads set)                          |
|  | Settings         |                                             |
|  +------------------+                                             |
|           |                                                       |
|           v                                                       |
|  +------------------+                                             |
|  | User Preferences |  (individual users set)                    |
|  +------------------+                                             |
|                                                                   |
|  Resolution: User → Team → Org → System Default                  |
+------------------------------------------------------------------+
```

## Settings Categories

```text
+------------------------------------------------------------------+
|                  Setting Types by Level                           |
+------------------------------------------------------------------+
| Level  | Examples                           | Override?           |
+--------+------------------------------------+---------------------+
| System | Feature flags, platform limits     | No                  |
| Org    | Branding, security policies, SSO   | No (enforced)       |
| Org    | Default timezone, language         | Yes (if allowed)    |
| Team   | Team-specific workflows, templates | Yes (if allowed)    |
| User   | Theme, notifications, shortcuts    | Always              |
+--------+------------------------------------+---------------------+
```

## Data Model

### Settings Tables

```csharp
public sealed class Setting
{
    public required Guid Id { get; init; }
    public required string Key { get; init; }
    public required string Value { get; init; }
    public required string ValueType { get; init; } // "string", "bool", "int", "json"
    public required SettingScope Scope { get; init; }
    public Guid? TenantId { get; init; }
    public Guid? TeamId { get; init; }
    public Guid? UserId { get; init; }
    public DateTimeOffset UpdatedAt { get; init; }
    public Guid? UpdatedBy { get; init; }
}

public enum SettingScope
{
    System,
    Tenant,
    Team,
    User
}

public sealed class SettingDefinition
{
    public required string Key { get; init; }
    public required string DisplayName { get; init; }
    public required string Description { get; init; }
    public required string ValueType { get; init; }
    public required string DefaultValue { get; init; }
    public required SettingScope MinScope { get; init; } // Lowest level that can set
    public required SettingScope MaxScope { get; init; } // Highest level that can set
    public required bool AllowOverride { get; init; }    // Lower levels can override?
    public string? ValidationRegex { get; init; }
    public List<string>? AllowedValues { get; init; }
}
```

### Setting Definitions

```csharp
public static class SettingDefinitions
{
    public static readonly SettingDefinition[] All =
    [
        // Org-level, no override (enforced)
        new()
        {
            Key = "security.mfa_required",
            DisplayName = "Require MFA",
            Description = "Require multi-factor authentication for all users",
            ValueType = "bool",
            DefaultValue = "false",
            MinScope = SettingScope.Tenant,
            MaxScope = SettingScope.Tenant,
            AllowOverride = false
        },

        // Org-level, with override
        new()
        {
            Key = "locale.timezone",
            DisplayName = "Default Timezone",
            Description = "Default timezone for the organization",
            ValueType = "string",
            DefaultValue = "UTC",
            MinScope = SettingScope.Tenant,
            MaxScope = SettingScope.User,
            AllowOverride = true
        },

        // User-level only
        new()
        {
            Key = "ui.theme",
            DisplayName = "Theme",
            Description = "Application color theme",
            ValueType = "string",
            DefaultValue = "light",
            MinScope = SettingScope.User,
            MaxScope = SettingScope.User,
            AllowOverride = true,
            AllowedValues = ["light", "dark", "system"]
        },

        // Team-level with user override
        new()
        {
            Key = "notifications.email_digest",
            DisplayName = "Email Digest",
            Description = "How often to receive email digests",
            ValueType = "string",
            DefaultValue = "daily",
            MinScope = SettingScope.Team,
            MaxScope = SettingScope.User,
            AllowOverride = true,
            AllowedValues = ["none", "daily", "weekly"]
        }
    ];
}
```

## Settings Resolution

### Resolution Service

```csharp
public sealed class SettingsService(
    IDbContext db,
    ITenantContext tenant)
{
    private readonly Dictionary<string, SettingDefinition> _definitions =
        SettingDefinitions.All.ToDictionary(d => d.Key);

    public async Task<T> GetAsync<T>(string key, CancellationToken ct = default)
    {
        var value = await ResolveSettingAsync(key, ct);
        return ConvertValue<T>(value);
    }

    public async Task<string> ResolveSettingAsync(string key, CancellationToken ct)
    {
        if (!_definitions.TryGetValue(key, out var definition))
            throw new UnknownSettingException(key);

        // Try user-level first
        if (definition.AllowOverride || definition.MinScope == SettingScope.User)
        {
            var userSetting = await db.Settings
                .Where(s => s.Key == key && s.UserId == tenant.UserId)
                .FirstOrDefaultAsync(ct);

            if (userSetting != null)
                return userSetting.Value;
        }

        // Try team-level
        if (definition.AllowOverride || definition.MinScope <= SettingScope.Team)
        {
            var teamSetting = await db.Settings
                .Where(s => s.Key == key && s.TeamId == tenant.TeamId)
                .FirstOrDefaultAsync(ct);

            if (teamSetting != null)
                return teamSetting.Value;
        }

        // Try tenant-level
        var tenantSetting = await db.Settings
            .Where(s => s.Key == key && s.TenantId == tenant.TenantId && s.TeamId == null && s.UserId == null)
            .FirstOrDefaultAsync(ct);

        if (tenantSetting != null)
            return tenantSetting.Value;

        // Return default
        return definition.DefaultValue;
    }

    public async Task<SettingResolution> GetResolutionAsync(string key, CancellationToken ct)
    {
        // Returns full resolution chain for UI display
        var chain = new List<SettingValue>();

        // System default
        var definition = _definitions[key];
        chain.Add(new SettingValue(SettingScope.System, definition.DefaultValue, null));

        // Tenant setting
        var tenantSetting = await GetSettingAtScopeAsync(key, SettingScope.Tenant, ct);
        if (tenantSetting != null)
            chain.Add(new SettingValue(SettingScope.Tenant, tenantSetting.Value, tenantSetting.UpdatedBy));

        // Team setting
        var teamSetting = await GetSettingAtScopeAsync(key, SettingScope.Team, ct);
        if (teamSetting != null)
            chain.Add(new SettingValue(SettingScope.Team, teamSetting.Value, teamSetting.UpdatedBy));

        // User setting
        var userSetting = await GetSettingAtScopeAsync(key, SettingScope.User, ct);
        if (userSetting != null)
            chain.Add(new SettingValue(SettingScope.User, userSetting.Value, userSetting.UpdatedBy));

        return new SettingResolution(key, chain, chain.Last().Value);
    }
}
```

### Effective Settings

```csharp
public sealed class EffectiveSettingsService(ISettingsService settings)
{
    public async Task<EffectiveSettings> GetEffectiveSettingsAsync(CancellationToken ct)
    {
        // Get all resolved settings for current context
        var effective = new Dictionary<string, object>();

        foreach (var definition in SettingDefinitions.All)
        {
            var value = await settings.GetAsync<object>(definition.Key, ct);
            effective[definition.Key] = value;
        }

        return new EffectiveSettings(effective);
    }
}

public sealed class EffectiveSettings(Dictionary<string, object> settings)
{
    public bool MfaRequired => (bool)settings["security.mfa_required"];
    public string Timezone => (string)settings["locale.timezone"];
    public string Theme => (string)settings["ui.theme"];
    public string EmailDigest => (string)settings["notifications.email_digest"];
}
```

## Settings API

```csharp
[ApiController]
[Route("api/settings")]
public class SettingsController : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<SettingsResponse>> GetSettings(CancellationToken ct)
    {
        var settings = await _settingsService.GetAllAsync(ct);
        return Ok(settings);
    }

    [HttpGet("{key}")]
    public async Task<ActionResult<SettingResolution>> GetSetting(string key, CancellationToken ct)
    {
        var resolution = await _settingsService.GetResolutionAsync(key, ct);
        return Ok(resolution);
    }

    [HttpPut("{key}")]
    public async Task<ActionResult> UpdateSetting(
        string key,
        [FromBody] UpdateSettingRequest request,
        CancellationToken ct)
    {
        // Validate scope permission
        if (!CanUpdateAtScope(request.Scope))
            return Forbid();

        await _settingsService.SetAsync(key, request.Value, request.Scope, ct);
        return Ok();
    }

    [HttpDelete("{key}")]
    public async Task<ActionResult> ResetSetting(
        string key,
        [FromQuery] SettingScope scope,
        CancellationToken ct)
    {
        // Remove override, fall back to higher level
        await _settingsService.ResetAsync(key, scope, ct);
        return Ok();
    }
}
```

## Settings UI

### Settings Panel Component

```typescript
interface SettingUIProps {
  setting: SettingDefinition;
  resolution: SettingResolution;
  onUpdate: (value: any, scope: SettingScope) => void;
}

const SettingRow: React.FC<SettingUIProps> = ({ setting, resolution, onUpdate }) => {
  const { currentScope, canOverride } = useSettingContext();

  return (
    <div className="setting-row">
      <div className="setting-info">
        <h4>{setting.displayName}</h4>
        <p>{setting.description}</p>
      </div>

      <div className="setting-value">
        <SettingInput
          type={setting.valueType}
          value={resolution.effectiveValue}
          options={setting.allowedValues}
          onChange={value => onUpdate(value, currentScope)}
          disabled={!canOverride}
        />

        {resolution.chain.length > 1 && (
          <div className="inheritance-indicator">
            <span>Inherited from {resolution.inheritedFrom}</span>
            {canOverride && (
              <button onClick={() => onUpdate(null, currentScope)}>
                Reset to inherited
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
```

### Settings Inheritance Visualization

```text
Setting Display UI:
+------------------------------------------------------------------+
| Setting: Default Timezone                                         |
| Description: Default timezone for the organization                |
+------------------------------------------------------------------+
| Effective Value: America/New_York                                 |
+------------------------------------------------------------------+
| Resolution Chain:                                                 |
| ├─ System Default: UTC                                            |
| ├─ Organization: America/New_York ← You are here                 |
| ├─ Team: (not set, using org)                                    |
| └─ User: (not set, using team)                                   |
+------------------------------------------------------------------+
| [Reset to default] [Override for my team] [Override for me]      |
+------------------------------------------------------------------+
```

## Best Practices

```text
Settings Hierarchy Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| Clear inheritance display   | Users understand effective value   |
| Reset to inherited option   | Easy to remove overrides           |
| Audit trail                 | Track who changed what             |
| Validation at definition    | Consistent valid values            |
| Scope-based permissions     | Right people change right settings |
| Export/import               | Easy migration between envs        |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Flat settings | No inheritance | Hierarchical model |
| No defaults | All settings required | System defaults |
| Hidden inheritance | Confusion about source | Show chain |
| No validation | Invalid values | Schema + validation |
| No reset option | Stuck with overrides | Reset to inherited |

## Related Skills

- `white-labeling` - Branding settings
- `team-management-ux` - Team-level settings access
- `tenant-provisioning` - Initial settings setup

## MCP Research

For current patterns:

```text
perplexity: "SaaS settings hierarchy 2024" "multi-tenant configuration inheritance"
```
