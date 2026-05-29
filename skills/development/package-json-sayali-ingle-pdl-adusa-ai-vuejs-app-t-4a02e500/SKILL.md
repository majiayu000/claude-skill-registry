---
name: package-json
description: Generates package.json with all necessary dependencies, dev dependencies, and scripts. Fetches latest package versions from npm registry.
---

# Package JSON Skill

## Purpose
Generate the `package.json` file for a Vue 3 Vite application with all necessary dependencies, dev dependencies, and scripts using the latest package versions from npm.

## Instructions

1. **Gather Input Parameters** from user (see Input Parameters section below)
2. **Fetch latest versions** from npm: `npm view <package> version`
3. **Generate** package.json using the `reference/latest-versions.md` template
4. **Replace placeholders** with resolved versions
5. **Validate** output meets all requirements
6. **Create** the file at project root: `package.json`

## Input Parameters

Ask the user or read from `copilot-instructions.md` and `docs/requirements/application-parameters.md`:
- `application_name`: The application name in kebab-case
- `project_scope`: The NPM scope/organization
- `default_port`: The development server port
- `application_type`: Either `standalone` or `micro-frontend` (determines serve command)
- `test_framework`: Testing framework - always `vitest` (latest recommended)
- `state_management`: State management library - always `pinia` (latest recommended)

## Version Strategy

**Always use latest versions from npm**:
- Fetch from npm: `npm view <package> version`
- **Exception**: Component library packages use `npm show` (see component-library skill)
- Apply caret prefix: `3.5.13` → `^3.5.13`
- Use template: `reference/latest-versions.md`
- Use recommended tools: Vitest + Pinia

## Template Reference

Use: `reference/latest-versions.md` (fetches latest versions from npm)

## Output
- File: `package.json` at project root
- Format: Valid JSON with proper indentation (2 spaces)

## Template Structure

```json
{
  "name": "{{project_scope}}/{{application_name}}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "serve": "{{serve_command}}"  // Conditional based on application_type
    // See reference/latest-versions.md for complete scripts list
  },
  "dependencies": {
    // See reference/latest-versions.md for complete dependencies
  },
  "devDependencies": {
    // See reference/latest-versions.md for complete devDependencies
  }
}
```

## Validation
- All version placeholders are replaced with actual values
- Package name follows format `@scope/name`
- `type` field is set to `"module"`
- All required scripts are defined
- Valid JSON syntax

## Version Management

### Fetching Latest Versions

1. **Load version configuration** from this SKILL.md (see Version Configuration section below)

2. **Resolve "latest" entries**:
   - For all packages marked as `"latest"` in the configuration
   - Fetch current version from npm: `npm view <package> version`
   - **Exception**: Component library packages use `npm show` instead of `npm view`
   - Example: `"vue": "latest"` → `npm view vue version` → `"vue": "^3.5.13"`

3. **Apply resolved versions**:
   ```json
   {
     "dependencies": {
       "vue": "{{vue_version}}",           // Resolved from npm
       "vue-router": "{{vue_router_version}}",
       "pinia": "{{pinia_version}}"
     }
   }
   ```

### Version Resolution Example

```json
// Version Configuration (from this SKILL.md)
{
  "core": {
    "vue": "latest",
    "vite": "latest"
  }
}

// After fetching from npm
{
  "dependencies": {
    "vue": "^3.5.13"
  },
  "devDependencies": {
    "vite": "^6.3.5"
  }
}
```

## Version Configuration (versions.json)

This is the central version configuration embedded in this SKILL.md.

Use this configuration to determine which versions to use:

```json
{
  "core": {
    "node": "latest",
    "vue": "latest",
    "vite": "latest",
    "typescript": "latest"
  },
  
  "dependencies": {
    "vue-router": "latest",
    "vuex": "latest",
    "pinia": "latest",
    "axios": "latest",
    "core-js": "latest",
    "single-spa-vue": "latest",
    "vue-class-component": "latest",
    "vue-tippy": "latest",
    "date-fns": "latest",
    "date-fns-tz": "latest",
    "@datadog/browser-rum": "latest"
  },
  
  "devDependencies": {
    "@vitejs/plugin-vue": "latest",
    "@types/node": "latest",
    "@types/jest": "latest",
    "@types/jsdom": "latest",
    "vite-plugin-css-injected-by-js": "latest",
    "vite-svg-loader": "latest",
    "vitest": "latest",
    "@vitest/ui": "latest",
    "@vitest/coverage-v8": "latest",
    "jsdom": "latest",
    "jest": "latest",
    "@vue/test-utils": "latest",
    "@vue/vue3-jest": "latest",
    "babel-jest": "latest",
    "ts-jest": "latest",
    "@babel/core": "latest",
    "@babel/plugin-transform-runtime": "latest",
    "@babel/preset-env": "latest",
    "eslint": "latest",
    "eslint-plugin-vue": "latest",
    "@typescript-eslint/eslint-plugin": "latest",
    "@typescript-eslint/parser": "latest",
    "vue-eslint-parser": "latest",
    "@vue/eslint-config-typescript": "latest",
    "eslint-config-prettier": "latest",
    "eslint-plugin-prettier": "latest",
    "@eslint/js": "latest",
    "@eslint/eslintrc": "latest",
    "prettier": "latest",
    "sass": "latest",
    "sass-loader": "latest",
    "stylelint": "latest",
    "stylelint-config-recommended-vue": "latest",
    "stylelint-config-standard-scss": "latest",
    "husky": "latest",
    "lint-staged": "latest",
    "npm-run-all": "latest",
    "chokidar-cli": "latest",
    "onchange": "latest"
  },
  
  "componentLibraries": {
    "@royalaholddelhaize/pdl-spectrum-component-library-web": "latest"
  },
  
  "docker": {
    "node": "22-stable",
    "nginx": "alpine"
  }
}
```

**Version Strategies**:
- `"latest"` - Fetch current version from npm registry (e.g., `npm view vue version`)
- **Note**: Component library packages use `npm show` instead of `npm view`
- `"^6.3.5"` - Pin to specific version with caret (allows minor/patch updates)
- `"~6.3.5"` - Pin with tilde (allows patch updates only)
- `"6.3.5"` - Exact version (no updates)

**Note**: This configuration is embedded in this SKILL.md file. There is no separate versions.json file needed.

## References

- **Version Configuration**: See "Version Configuration (versions.json)" section above in this file
- **Package Templates**: `reference/` directory (jest-vuex.md, vitest-pinia.md, latest-versions.md)
- **Complete Examples**: `examples.md`


