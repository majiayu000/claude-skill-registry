---
name: umbraco-property-value-preset
description: Implement property value presets in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Property Value Preset

## What is it?
Property Value Presets provide default values when users create new content. They use an API to supply preset values for specific property editors, enabling streamlined content creation with sensible defaults. Multiple presets can work together using the `weight` property to progressively modify values.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/property-value-preset
- **Property Editors**: https://docs.umbraco.com/umbraco-cms/customizing/property-editors
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Which property editor? What default value? Static or dynamic?
3. **Generate files** - Create manifest + preset API based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestPropertyValuePreset } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestPropertyValuePreset = {
  type: 'propertyValuePreset',
  alias: 'My.PropertyValuePreset.DefaultText',
  name: 'Default Text Preset',
  api: () => import('./default-text-preset.js'),
  forPropertyEditorUiAlias: 'Umb.PropertyEditorUi.TextBox',
};

export const manifests = [manifest];
```

### Preset Implementation (default-text-preset.ts)
```typescript
import type { UmbPropertyValuePresetApi } from '@umbraco-cms/backoffice/property';

export class DefaultTextPreset implements UmbPropertyValuePresetApi {
  async processValue(value: unknown, config: unknown): Promise<unknown> {
    // Return default if no value exists
    return value ? value : 'Default text value';
  }

  destroy() {
    // Cleanup if needed
  }
}

export default DefaultTextPreset;
```

### Dynamic Default Based on Config
```typescript
import type { UmbPropertyValuePresetApi, UmbPropertyEditorConfigCollection } from '@umbraco-cms/backoffice/property';

export class DynamicPreset implements UmbPropertyValuePresetApi {
  async processValue(value: unknown, config: UmbPropertyEditorConfigCollection): Promise<unknown> {
    if (value) return value;

    // Use configuration to determine default
    const defaultFromConfig = config?.getValueByAlias('defaultValue');
    return defaultFromConfig || 'Fallback default';
  }

  destroy() {}
}

export default DynamicPreset;
```

### Async Default (e.g., from API)
```typescript
import type { UmbPropertyValuePresetApi } from '@umbraco-cms/backoffice/property';

export class ApiPreset implements UmbPropertyValuePresetApi {
  async processValue(value: unknown, config: unknown): Promise<unknown> {
    if (value) return value;

    // Fetch default from server
    const response = await fetch('/api/defaults/text');
    const data = await response.json();
    return data.defaultValue;
  }

  destroy() {}
}

export default ApiPreset;
```

### Target by Schema Alias
```typescript
const manifest: ManifestPropertyValuePreset = {
  type: 'propertyValuePreset',
  alias: 'My.PropertyValuePreset.JsonDefault',
  name: 'JSON Default Preset',
  api: () => import('./json-preset.js'),
  forPropertyEditorSchemaAlias: 'Umbraco.Plain.Json', // Target schema instead of UI
};
```

### Multiple Presets with Weight
```typescript
// First preset (runs first due to lower weight)
const basePreset: ManifestPropertyValuePreset = {
  type: 'propertyValuePreset',
  alias: 'My.PropertyValuePreset.Base',
  name: 'Base Preset',
  weight: 100,
  api: () => import('./base-preset.js'),
  forPropertyEditorUiAlias: 'Umb.PropertyEditorUi.TextBox',
};

// Second preset (runs after, can modify base value)
const enhancedPreset: ManifestPropertyValuePreset = {
  type: 'propertyValuePreset',
  alias: 'My.PropertyValuePreset.Enhanced',
  name: 'Enhanced Preset',
  weight: 200,
  api: () => import('./enhanced-preset.js'),
  forPropertyEditorUiAlias: 'Umb.PropertyEditorUi.TextBox',
};
```

### Date Default Example
```typescript
export class TodayDatePreset implements UmbPropertyValuePresetApi {
  async processValue(value: unknown, config: unknown): Promise<unknown> {
    if (value) return value;
    return new Date().toISOString().split('T')[0]; // Today's date
  }

  destroy() {}
}

export default TodayDatePreset;
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
