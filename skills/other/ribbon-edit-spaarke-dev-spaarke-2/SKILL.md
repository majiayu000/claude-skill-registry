---
description: Edit Dataverse ribbon customizations via solution export/import
alwaysApply: false
---

# Ribbon Edit

> **Category**: Development
> **Last Updated**: December 2025

---

## Purpose

Automate editing Dataverse Application Ribbon customizations by exporting solutions, modifying the RibbonDiffXml in customizations.xml, and re-importing. Bypasses the complex XrmToolBox Ribbon Workbench visual editor.

---

## Applies When

- User requests ribbon customization (flyout menus, buttons, commands)
- Adding JavaScript-triggered ribbon actions
- Modifying Application Ribbon (global ribbon visible on all forms/views)
- Entity-specific ribbon changes
- **Trigger phrases**: "edit ribbon", "add ribbon button", "ribbon customization", "command bar button"

---

## Prerequisites

1. **PAC CLI authenticated**: Run `pac auth list` to verify connection
2. **Dedicated ribbon solution exists** (see Solution Setup below)
3. **Web resources deployed**: Any JS libraries and icons must be deployed before ribbon import

---

## Critical Requirements

### The `Alt` Attribute

**CRITICAL**: The `Alt` attribute is **REQUIRED** on all `Button` and `FlyoutAnchor` elements. Without it, the solution may fail to publish.

```xml
<!-- ✅ Correct -->
<Button Alt="$LocLabels:sprk.Feature.Button.Alt" Id="sprk.Feature.Button" ... />

<!-- ❌ Wrong - missing Alt -->
<Button Id="sprk.Feature.Button" ... />
```

### Icon Attributes for Modern UCI

For icons to display correctly in the modern command bar:

| Attribute | Format | Notes |
|-----------|--------|-------|
| `Image16by16` | `$webresource:prefix_Icon16.svg` | Use `.svg` extension |
| `Image32by32` | `$webresource:prefix_Icon32.svg` | Use `.svg` extension |
| `ModernImage` | `$webresource:prefix_Icon32.svg` | **Required for UCI** - use 32px SVG |

**Example:**
```xml
<FlyoutAnchor
    Alt="$LocLabels:sprk.ThemeMenu.Alt"
    Image16by16="$webresource:sprk_ThemeMenu16.svg"
    Image32by32="$webresource:sprk_ThemeMenu32.svg"
    ModernImage="$webresource:sprk_ThemeMenu32.svg"
    ... />
```

### SVG Best Practices

**Recommended SVG structure for ribbon icons:**

```xml
<!-- sprk_IconName.svg - Use this structure -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
  <path d="..."/>
</svg>
```

**Requirements:**
- ✅ Use `fill="currentColor"` - adapts to light/dark mode automatically
- ✅ Use `viewBox="0 0 20 20"` - Modern UI standard size
- ✅ Keep paths simple - complex SVGs render poorly at small sizes
- ❌ **Do NOT** include `width` or `height` attributes (causes icon not to show)
- ❌ **Do NOT** use hardcoded colors (breaks dark mode)

### MenuSection DisplayMode

Always include `DisplayMode="Menu16"` on MenuSection elements:

```xml
<MenuSection Id="sprk.Feature.MenuSection"
             Title="$LocLabels:sprk.Feature.Title"
             Sequence="10"
             DisplayMode="Menu16">
```

---

## Solution Setup (One-Time)

Ribbon Workbench and solution import require a **dedicated solution** containing ONLY the ribbon component - no other entities, web resources, or components.

### For Application Ribbon (Global - all forms/views)

1. **Create new unmanaged solution** in Power Apps maker portal:
   - Name: `ApplicationRibbon` (or similar)
   - Publisher: **Spaarke** (default publisher - required)
   - Version: `1.0.0.0`
   - **Must be unmanaged** (not managed)

2. **Add Application Ribbon component**:
   - In the solution, click **Add existing** → **More** → **Other** → **Application Ribbons**
   - Select "Application Ribbon" and add it
   - **Do NOT add any other components** (entities, web resources, etc.)

3. **Publish** the solution

### For Entity-Specific Ribbon

1. **Create new unmanaged solution**:
   - Name: `{EntityName}Ribbon` (e.g., `DocumentRibbons`, `MatterRibbons`)
   - Publisher: **Spaarke** (default publisher - required)
   - **Must be unmanaged** (not managed)

2. **Add ONLY the entity**:
   - Click **Add existing** → **Table**
   - Select the entity → **Add** (select "Include table metadata" only, no subcomponents)
   - **Do NOT add forms, views, or other components**

3. **Publish** the solution

> **Why dedicated solutions?** Ribbon Workbench and solution import merge RibbonDiffXml. Including other components can cause conflicts or unintended overwrites.

> **Why Spaarke publisher?** Using the default "Spaarke" publisher ensures consistent prefixes (`sprk_`) across all components and avoids conflicts when deploying between environments.

---

## Workflow

### Step 1: Export Dedicated Ribbon Solution

Export the **dedicated ribbon solution** created in Solution Setup (not a solution with other components):

```powershell
# Create temp directory
New-Item -ItemType Directory -Force -Path "infrastructure\dataverse\ribbon\temp"

# List solutions to find exact name
pac solution list | Select-String -Pattern "ribbon" -CaseSensitive:$false

# Export the dedicated ribbon solution
pac solution export --name {RibbonSolutionName} --path "infrastructure\dataverse\ribbon\temp\{RibbonSolutionName}.zip" --managed false
```

**Common solution names:**
- `ApplicationRibbon` - Global ribbon (all forms/views)
- `DocumentRibbons` - sprk_document entity ribbon
- `MatterRibbons` - sprk_matter entity ribbon

### Step 2: Extract Solution

```powershell
# Extract the solution zip
Expand-Archive -Path "infrastructure\dataverse\ribbon\temp\{SolutionName}.zip" -DestinationPath "infrastructure\dataverse\ribbon\temp\{SolutionName}_extracted" -Force
```

### Step 3: Edit customizations.xml

Locate `{SolutionName}_extracted/customizations.xml` and find the `<RibbonDiffXml>` section.

**Structure:**
```xml
<RibbonDiffXml>
  <CustomActions>
    <!-- UI elements (FlyoutAnchor, Button, etc.) -->
  </CustomActions>
  <Templates>
    <RibbonTemplates Id="Mscrm.Templates"></RibbonTemplates>
  </Templates>
  <CommandDefinitions>
    <!-- Command definitions with JavaScriptFunction actions -->
  </CommandDefinitions>
  <RuleDefinitions>
    <TabDisplayRules />
    <DisplayRules />
    <EnableRules>
      <!-- Enable rules for commands -->
    </EnableRules>
  </RuleDefinitions>
  <LocLabels>
    <!-- Localized labels - REQUIRED for Alt attributes -->
  </LocLabels>
</RibbonDiffXml>
```

### Step 4: Re-package Solution

```powershell
# Re-package the modified solution
Compress-Archive -Path "infrastructure\dataverse\ribbon\temp\{SolutionName}_extracted\*" -DestinationPath "infrastructure\dataverse\ribbon\temp\{SolutionName}_modified.zip" -Force
```

### Step 5: Import Solution

```powershell
pac solution import --path "infrastructure\dataverse\ribbon\temp\{SolutionName}_modified.zip" --publish-changes
```

### Step 6: Clean Up

```powershell
# Option A: Archive the original export for rollback (recommended)
Move-Item "infrastructure\dataverse\ribbon\temp\{SolutionName}.zip" "infrastructure\dataverse\ribbon\{SolutionName}\{SolutionName}_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip"

# Option B: Delete temp folder entirely (only after confirming import worked)
Remove-Item -Path "infrastructure\dataverse\ribbon\temp" -Recurse -Force
```

> **Tip**: Keep at least one backup of the original export before cleaning up. This allows rollback if issues are discovered later.

---

## Conventions

### Ribbon Element IDs

Use publisher prefix and descriptive names:
- `{prefix}.{Feature}.{ElementType}` - e.g., `sprk.ThemeMenu.FlyoutAnchor`

### CustomAction Locations

| Location | Description |
|----------|-------------|
| `Mscrm.GlobalTab.MainTab.More._children` | "More Commands" overflow menu |
| `Mscrm.HomepageGrid.{entity}.MainTab.Actions.Controls._children` | Entity homepage grid actions |
| `Mscrm.SubGrid.{entity}.MainTab.Management.Controls._children` | Subgrid management buttons |
| `Mscrm.Form.{entity}.MainTab.Save.Controls._children` | Entity form save group |

> **Note**: `{entity}` must be **lowercase** logical name (e.g., `sprk_document`, not `sprk_Document`)

### Web Resource References

```xml
Image16by16="$webresource:prefix_IconName16.svg"
Image32by32="$webresource:prefix_IconName32.svg"
ModernImage="$webresource:prefix_IconName32.svg"
Library="$webresource:prefix_ScriptName.js"
```

### JavaScript Function Pattern

```xml
<JavaScriptFunction Library="$webresource:prefix_Script.js"
                    FunctionName="Namespace.Function.name">
  <StringParameter Value="paramValue" />
  <CrmParameter Value="PrimaryControl" />
</JavaScriptFunction>
```

---

## Resources

| Resource | Purpose |
|----------|----------|
| `docs/reference/articles/RIBBON-COMMAND-BAR-MODIFICATIONS.md` | Full templates and location reference |
| `docs/reference/articles/document-ribbon-example.xml` | Working Dark Mode menu example |
| `infrastructure/dataverse/ribbon/` | Ribbon XML templates and documentation |
| `src/client/webresources/js/` | JavaScript web resources |
| `src/client/assets/icons/` | SVG icons for ribbon buttons |

---

## Output Format

```markdown
## Ribbon Edit Results

**Solution**: {SolutionName}
**Action**: {Added|Modified|Removed} {ElementType}
**Elements**:
- {Element1 Id}
- {Element2 Id}

**Status**: ✅ Imported and published successfully
```

---

## Examples

### Adding a Flyout Menu

**Input:** "Add a Theme flyout menu to the Entity Ribbon"

**Steps:**
1. Export entity ribbon solution
2. Add FlyoutAnchor with:
   - `Alt` attribute (required)
   - `Image16by16`, `Image32by32`, `ModernImage` (all SVG)
   - Menu/MenuSection with `DisplayMode="Menu16"`
   - Buttons with `Alt` attribute
3. Add CommandDefinitions with JavaScriptFunction actions
4. Add EnableRules
5. Add all required LocLabels
6. Re-import solution

---

## Error Handling

| Situation | Response |
|-----------|----------|
| `pac auth list` shows no connections | Run `pac auth create` to authenticate to Dataverse |
| Solution export fails with "not found" | Verify exact solution name with `pac solution list` |
| Import fails with "web resource not found" | Deploy missing JS/icon web resources first, then retry import |
| Import fails with "duplicate ID" | Check for conflicting ribbon elements; use unique `sprk.` prefixed IDs |
| Import fails with validation error | Ensure all `Alt` attributes are present on buttons/flyouts |
| Icons show as placeholder (jigsaw) | Use SVG web resources with `.svg` extension in `ModernImage` |
| **Icon not showing at all** | Remove `width`/`height` from SVG; use only `viewBox` |
| **Icon wrong color in dark mode** | Use `fill="currentColor"` instead of hardcoded colors |
| Ribbon not appearing after import | Run `pac solution publish` or publish from Power Apps maker portal |
| XML parsing error | Validate `customizations.xml` structure; check for unclosed tags |
| Changes not visible in app | Clear browser cache; try Ctrl+F5 hard refresh |
| **Subgrid button not appearing** | Use `Mscrm.SubGrid.{entity}` location, not `Mscrm.HomepageGrid` |
| **Subgrid JS error: undefined** | Use `SelectedControl` CrmParameter, not `PrimaryControl` |
| **HideCustomAction not working** | Verify `HideActionId` matches exact original `<CustomAction>` Id |

---

## Related Skills

- `adr-aware` - Automatically loads ADR-006 (PCF over webresources) when working with ribbon JS
- `spaarke-conventions` - Naming conventions for ribbon element IDs and web resources

---

## Tips for AI

- **Always include `Alt` attribute** on all buttons and flyout anchors
- **Always use SVG** for `ModernImage` attribute with `.svg` extension
- Use `ModernImage` with 32.svg for FlyoutAnchor, 16.svg for menu buttons
- Include `DisplayMode="Menu16"` on MenuSection elements
- Always verify web resources exist before importing ribbon (icons, JS files)
- Use `pac solution list` to find exact solution names
- Keep a backup of the original exported solution
- Test ribbon changes in DEV before promoting to higher environments
- The `Sequence` attribute controls button order (lower = earlier)
- Use `Default="true"` on EnableRules to show button while JS loads
- When duplicating ribbon elements for multiple entities, use pattern: `sprk.{Feature}.{EntityName}.{ElementType}`
- `TemplateAlias="o1"` is required for buttons to appear in the overflow menu
- For subgrids, use `SelectedControl` CrmParameter instead of `PrimaryControl`
- Reference `docs/reference/articles/RIBBON-COMMAND-BAR-MODIFICATIONS.md` for HideCustomAction and subgrid details
- Reference [RIBBON-COMMAND-BAR-MODIFICATIONS.md](../../../docs/reference/articles/RIBBON-COMMAND-BAR-MODIFICATIONS.md) for templates
