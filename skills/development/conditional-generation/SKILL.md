---
name: conditional-generation
description: Determines which files and dependencies to generate based on application type (standalone vs micro-frontend). Controls conditional features.
---

# Conditional File Generation Skill

## Purpose
Determine which files, dependencies, and environment variables to include based on the application type (standalone vs micro-frontend).

## When to Use
Execute this skill after configuration is loaded and before file generation (Step 6 in AGENT_INSTRUCTIONS.md).

## Input Parameters
From configuration:
- `application_type` - Either `"standalone"` or `"micro-frontend"`
- `is_standalone` - Boolean derived from application_type
- `is_microfrontend` - Boolean derived from application_type
- `enable_single_spa` - Boolean flag for single-spa integration

## Key Differences: Standalone vs Micro-Frontend

| Feature | Micro-Frontend | Standalone |
|---------|---------------|------------|
| `.env.standalone` | ✅ Create | ❌ Skip |
| `single-spa-vue` dependency | ✅ Include | ❌ Skip |
| `serve` npm script | `npm-run-all --parallel build:watch dev lint:init:watch` | `vite serve --port {port} --mode standalone` |
| `VITE_LAUNCHER_APP_URL` | ✅ Include | ❌ Skip |
| `launcherAppUrl` in EnvConsts | ✅ Export | ❌ Skip |
| main.ts template | single-spa lifecycle | Simple mount |
| index.html mount | `#single-spa-application:...` | `#app` |
| Build format | `system` (SystemJS) | `es` (ES modules) |
| Router base | `/scoped-path` | `/` (typically) |

## Instructions

### Step 1: Auto-Correct Inconsistent Configuration

```javascript
// Validate and auto-correct enable_single_spa for standalone apps
if (userConfig.is_standalone && userConfig.enable_single_spa) {
  console.warn('⚠️  Warning: Standalone apps typically do not use single-spa.');
  console.warn('   Auto-correcting: enable_single_spa = false\n');
  userConfig.enable_single_spa = false;
}

// Validate and ensure enable_single_spa is true for micro-frontends
if (userConfig.is_microfrontend && !userConfig.enable_single_spa) {
  console.warn('⚠️  Warning: Micro-frontend apps require single-spa.');
  console.warn('   Auto-correcting: enable_single_spa = true\n');
  userConfig.enable_single_spa = true;
}
```

### Step 2: Determine Files to Generate

```javascript
// Files that should ONLY be created for micro-frontend applications
const conditionalFiles = {
  '.env.standalone': userConfig.is_microfrontend
};

// Create a helper function
function shouldGenerateFile(filename) {
  if (filename in conditionalFiles) {
    return conditionalFiles[filename];
  }
  return true;  // Generate by default
}
```

### Step 3: Determine Dependencies to Include

```javascript
// Dependencies that should ONLY be included for micro-frontend applications
const conditionalDependencies = {
  'single-spa-vue': userConfig.is_microfrontend
};

// Create a helper function
function shouldIncludeDependency(dependencyName) {
  if (dependencyName in conditionalDependencies) {
    return conditionalDependencies[dependencyName];
  }
  return true;  // Include by default
}
```

### Step 4: Determine Environment Variables to Include

```javascript
// Environment variables that should ONLY be included for micro-frontend applications
const conditionalEnvVars = {
  'VITE_LAUNCHER_APP_URL': userConfig.is_microfrontend,
  'launcherAppUrl': userConfig.is_microfrontend  // For EnvConsts.ts
};

// Create a helper function
function shouldIncludeEnvVar(varName) {
  if (varName in conditionalEnvVars) {
    return conditionalEnvVars[varName];
  }
  return true;  // Include by default
}
```

### Step 5: Select Appropriate Templates

```javascript
// Determine which template to use for each file
const templates = {
  'main.ts': userConfig.is_microfrontend 
    ? 'main-microfrontend.ts' 
    : 'main-standalone.ts',
    
  'EnvConsts.ts': userConfig.is_microfrontend
    ? 'EnvConsts-microfrontend.ts'
    : 'EnvConsts-standalone.ts',
    
  'index.html': userConfig.is_microfrontend
    ? 'index-microfrontend.html'
    : 'index-standalone.html'
};

// Helper function
function getTemplate(filename) {
  return templates[filename] || filename;
}
```

### Step 6: Configure Build Settings

```javascript
// Set vite build format based on application type
userConfig.vite_build_format = userConfig.is_microfrontend ? 'system' : 'es';

// Set default router base based on application type
if (!userConfig.router_base_path) {
  userConfig.router_base_path = userConfig.is_microfrontend 
    ? `/${userConfig.application_name.replace('-web', '')}`
    : '/';
}
```

### Step 7: Display Conditional Generation Summary

```javascript
console.log('\n' + '─'.repeat(60));
console.log('  CONDITIONAL FILE GENERATION');
console.log('─'.repeat(60));
console.log(`Application Type:  ${userConfig.application_type}`);
console.log(`Build Format:      ${userConfig.vite_build_format}`);
console.log(`Single-SPA:        ${userConfig.enable_single_spa ? 'Enabled' : 'Disabled'}`);

if (userConfig.is_microfrontend) {
  console.log('\nMicro-Frontend Files:');
  console.log('  ✓ .env.standalone');
  console.log('  ✓ main.ts (single-spa lifecycle)');
  console.log('  ✓ EnvConsts.ts (with launcherAppUrl)');
  console.log('  ✓ Dependencies: single-spa-vue');
} else {
  console.log('\nStandalone App Files:');
  console.log('  ✗ .env.standalone (skipped)');
  console.log('  ✓ main.ts (simple mount)');
  console.log('  ✓ EnvConsts.ts (without launcherAppUrl)');
  console.log('  ✗ single-spa-vue (skipped)');
}

console.log('─'.repeat(60) + '\n');
```

## Output

### For Micro-Frontend Applications

**Files Created:**
- `.env.standalone` ✅
- `main.ts` (with single-spa lifecycle) ✅
- `EnvConsts.ts` (with launcherAppUrl) ✅
- `index.html` (with #single-spa-application:...) ✅

**Dependencies Added:**
- `single-spa-vue` ✅

**Environment Variables:**
- `VITE_LAUNCHER_APP_URL` ✅

**Build Configuration:**
- `vite_build_format`: `"system"`

### For Standalone Applications

**Files Created:**
- `.env.standalone` ❌ (skipped)
- `main.ts` (simple mount) ✅
- `EnvConsts.ts` (without launcherAppUrl) ✅
- `index.html` (with #app) ✅

**Dependencies Added:**
- `single-spa-vue` ❌ (skipped)

**Environment Variables:**
- `VITE_LAUNCHER_APP_URL` ❌ (skipped)

**Build Configuration:**
- `vite_build_format`: `"es"`

## Decision Flow Diagram

```
User sets application_type
    │
    ├─── "micro-frontend" ────┐
    │                         │
    │                         ▼
    │                   Create .env.standalone
    │                   Include single-spa-vue
    │                   Add VITE_LAUNCHER_APP_URL
    │                   Use main-microfrontend.ts
    │                   Export launcherAppUrl
    │                   Set enable_single_spa = true
    │                   Use #single-spa-application:... mount
    │                   Build format = "system"
    │
    └─── "standalone" ────────┐
                              │
                              ▼
                        Skip .env.standalone
                        Skip single-spa-vue
                        Skip VITE_LAUNCHER_APP_URL
                        Use main-standalone.ts
                        Skip launcherAppUrl
                        Set enable_single_spa = false
                        Use #app mount
                        Build format = "es"
```

## Validation Rules

### Auto-Correction Rules

1. **Standalone + enable_single_spa = true**
   - Auto-correct to `enable_single_spa = false`
   - Show warning to user

2. **Micro-frontend + enable_single_spa = false**
   - Auto-correct to `enable_single_spa = true`
   - Show warning to user

### Consistency Checks

```javascript
// Validate configuration consistency
function validateConditionalGeneration(config) {
  const issues = [];
  
  // Check 1: Standalone should not have single-spa
  if (config.is_standalone && config.enable_single_spa) {
    issues.push('Standalone apps should not use single-spa');
    config.enable_single_spa = false;  // Auto-fix
  }
  
  // Check 2: Micro-frontend requires single-spa
  if (config.is_microfrontend && !config.enable_single_spa) {
    issues.push('Micro-frontend apps require single-spa');
    config.enable_single_spa = true;  // Auto-fix
  }
  
  // Check 3: Build format matches app type
  if (config.is_microfrontend && config.vite_build_format !== 'system') {
    issues.push('Micro-frontend should use "system" build format');
    config.vite_build_format = 'system';  // Auto-fix
  }
  
  if (config.is_standalone && config.vite_build_format !== 'es') {
    issues.push('Standalone should use "es" build format');
    config.vite_build_format = 'es';  // Auto-fix
  }
  
  // Display issues and fixes
  if (issues.length > 0) {
    console.warn('\n⚠️  Configuration Auto-Corrections:');
    issues.forEach(issue => console.warn(`   - ${issue}`));
    console.warn('');
  }
  
  return config;
}
```

## Integration with Skills

### Affects env-standalone Skill
- Micro-frontend: Generate file
- Standalone: Skip file

### Affects main-entry Skill
- Micro-frontend: Use template with single-spa lifecycle
- Standalone: Use template with simple mount

### Affects env-constants Skill
- Micro-frontend: Include launcherAppUrl export
- Standalone: Exclude launcherAppUrl export

### Affects index-html Skill
- Micro-frontend: Use `#single-spa-application:{app-name}` mount point
- Standalone: Use `#app` mount point

### Affects package-json Skill
- Micro-frontend: Include single-spa-vue dependency
- Standalone: Exclude single-spa-vue dependency
- Micro-frontend: `serve` script = `"npm-run-all --parallel build:watch dev lint:init:watch"`
- Standalone: `serve` script = `"vite serve --port {{default_port}} --mode standalone"`

### Affects vite-config Skill
- Micro-frontend: Set build.lib.formats = ['system']
- Standalone: Set build.lib.formats = ['es']

## Related Skills
- **configuration**: Provides application_type and derived flags
- **env-standalone**: Conditionally generated file
- **main-entry**: Uses different templates
- **env-constants**: Uses different templates
- **index-html**: Uses different mount points
- **package-json**: Includes different dependencies
- **vite-config**: Uses different build formats

## Testing Checklist

- [ ] Generate micro-frontend → Verify .env.standalone exists
- [ ] Generate standalone → Verify .env.standalone does NOT exist
- [ ] Check micro-frontend main.ts → Has single-spa lifecycle
- [ ] Check standalone main.ts → Simple createApp and mount
- [ ] Check micro-frontend EnvConsts.ts → Has launcherAppUrl
- [ ] Check standalone EnvConsts.ts → NO launcherAppUrl
- [ ] Check micro-frontend package.json → Has single-spa-vue
- [ ] Check standalone package.json → NO single-spa-vue
- [ ] Verify auto-correction when enable_single_spa conflicts with standalone
- [ ] Verify auto-correction when enable_single_spa missing for micro-frontend
- [ ] Check micro-frontend vite.config.ts → format: 'system'
- [ ] Check standalone vite.config.ts → format: 'es'
