---
name: validate-build
description: Run production build validation (npm run build, vite build, tsc) to ensure code compiles and builds successfully. Returns structured output with build status, duration, size metrics, and error details. Used for quality gates and deployment readiness checks.
---

# Validate Build

Executes production build process to validate that code compiles and bundles successfully.

## Usage

This skill runs the build command and returns structured validation results.

## Supported Build Tools

- **Vite**: Modern bundler for frontend
- **TypeScript**: tsc --build
- **Webpack**: Production webpack builds
- **esbuild/Rollup**: Modern bundlers
- Works with any `npm run build` script

## Output Format

### Success (Build Passes)

```json
{
  "status": "success",
  "build": {
    "status": "passing",
    "duration": "12.3s",
    "outputSize": "245.8 kB",
    "errors": [],
    "warnings": []
  },
  "canProceed": true
}
```

### Build Fails

```json
{
  "status": "error",
  "build": {
    "status": "failing",
    "duration": "5.2s",
    "errors": [
      {
        "file": "src/components/Settings.tsx",
        "message": "Property 'user' does not exist on type 'AppState'",
        "line": 42
      }
    ],
    "warnings": [
      {
        "message": "Circular dependency detected",
        "details": "src/utils/helpers.ts -> src/components/Card.tsx -> src/utils/helpers.ts"
      }
    ]
  },
  "canProceed": false,
  "details": "Build failed with 1 error(s)"
}
```

## When to Use

- Quality gate validation (before PR)
- Deployment readiness check
- After significant code changes
- Conductor Phase 3 (Quality Assurance)
- CI/CD pipeline validation

## Requirements

- Build script configured in package.json
- Typical scripts: `"build": "vite build"` or `"build": "tsc"`
- Node modules installed
