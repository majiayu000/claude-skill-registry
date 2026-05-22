---
name: Framework Detector
version: 1.0.0
framework_versions:
  min: 1.0.0
  recommended: 1.0.0
compatible_agents:
  backend-developer: ">=3.0.0"
  frontend-developer: ">=3.0.0"
  tech-lead-orchestrator: ">=2.5.0"
description: Multi-signal framework detection with confidence scoring for 6 major frameworks
frameworks:
  - framework-detector
languages:
  - javascript
  - typescript
category: utility
updated: 2025-10-22
---

# Framework Detector Skill

## Quick Reference

**When to Use**: Automatically detect framework in project before loading framework-specific skills

**Supported Frameworks**: NestJS, React, Phoenix, Rails, .NET/ASP.NET Core, Blazor

**Detection Method**: Multi-signal analysis with weighted confidence scoring

## Usage

### Basic Detection

```javascript
const FrameworkDetector = require('./detect-framework');

const detector = new FrameworkDetector('/path/to/project');
const result = await detector.detect();

console.log(result.primary);    // "nestjs"
console.log(result.confidence); // 0.92
console.log(result.alternates); // [{ framework: "dotnet", confidence: 0.45 }]
```

### CLI Usage

```bash
# Detect framework in current directory
./detect-framework.js

# Detect framework in specific project
./detect-framework.js /path/to/project

# Output format (JSON)
{
  "primary": "react",
  "confidence": 0.89,
  "alternates": [],
  "details": { ... }
}
```

## Detection Signals

### 1. Package Manager (Weight: 10)
- **Node.js**: `package.json` dependencies
- **Ruby**: `Gemfile` gems
- **Elixir**: `mix.exs` dependencies
- **.NET**: `*.csproj` PackageReferences

### 2. Files (Weight: 8-9)
- Required: Framework-specific config files
- Optional: Common project structure files
- Wildcards: Pattern matching (e.g., `*.csproj`)

### 3. Imports (Weight: 7-8)
- Code pattern analysis in source files
- Regex-based matching
- File sampling for performance (max 20 files)

### 4. Boost Factors (Multiplier: 1.2-1.6x)
- Strong indicators multiply confidence
- Framework-specific patterns
- Examples:
  - NestJS: `nest-cli.json` (+50%)
  - React: JSX files (+40%)
  - Blazor: `.razor` files (+60%)

## Confidence Threshold

**Default**: 0.8 (80% confidence required)

**Interpretation**:
- ≥ 0.9: Very high confidence
- 0.8-0.9: High confidence
- 0.6-0.8: Medium confidence (below threshold)
- < 0.6: Low confidence

## Framework-Specific Patterns

### NestJS Detection
```
✓ @nestjs/core in package.json
✓ nest-cli.json exists
✓ @Module decorator in .ts files
✓ @Controller decorator in .ts files
```

### React Detection
```
✓ react in package.json
✓ .jsx or .tsx files exist
✓ useState or useEffect in code
✓ createRoot in code
```

### Phoenix Detection
```
✓ {:phoenix, in mix.exs
✓ config/config.exs exists
✓ Phoenix.Endpoint in .ex files
✓ Phoenix.Router in .ex files
```

### Rails Detection
```
✓ gem 'rails' in Gemfile
✓ config/application.rb exists
✓ Rails.application in code
✓ ActiveRecord::Base in code
```

### .NET Detection
```
✓ Microsoft.AspNetCore in .csproj
✓ Program.cs exists
✓ [ApiController] in .cs files
✓ using Microsoft.AspNetCore
```

### Blazor Detection
```
✓ Microsoft.AspNetCore.Components in .csproj
✓ .razor files exist
✓ @page directive in .razor files
✓ ComponentBase in code
```

## Performance

**Optimizations**:
- File sampling (10-20 files max per check)
- Glob ignore patterns (node_modules, dist, build)
- Early exit on strong matches
- Async/await for parallel checks

**Typical Detection Time**: 100-500ms

## Error Handling

**No Frameworks Detected**:
```javascript
{
  primary: null,
  confidence: 0,
  alternates: [],
  details: {}
}
```

**Multiple Frameworks** (e.g., monorepo):
```javascript
{
  primary: "react",
  confidence: 0.91,
  alternates: [
    { framework: "nestjs", confidence: 0.87 }
  ]
}
```

## Integration with SkillLoader

```javascript
const { SkillLoader } = require('../skill-loader');
const FrameworkDetector = require('./detect-framework');

async function loadFrameworkSkill(projectRoot) {
  // 1. Detect framework
  const detector = new FrameworkDetector(projectRoot);
  const result = await detector.detect();

  // 2. Handle low confidence
  if (result.confidence < 0.8) {
    // Prompt user or use alternates
    console.warn('Low confidence detection');
  }

  // 3. Load skill
  const loader = new SkillLoader({
    agentName: 'backend-developer',
    agentVersion: '3.0.0'
  });

  const skill = await loader.loadSkill(result.primary, 'quick');
  return skill;
}
```

## Configuration

Edit `framework-patterns.json` to:
- Add new frameworks
- Adjust detection weights
- Modify confidence threshold
- Update boost factors

## See Also

- [framework-patterns.json](./framework-patterns.json) - Detection patterns configuration
- [detect-framework.js](./detect-framework.js) - Implementation source
- ../../lib/skill-loader.js - Skill loading integration
