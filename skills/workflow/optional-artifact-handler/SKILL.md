---
name: optional-artifact-handler
description: Handles optional artifact inputs in workflows. Manages workflows that can proceed with or without optional artifacts, provides defaults when artifacts are missing, and documents optional artifact handling.
allowed-tools: read, grep, glob
---

# Optional Artifact Handler Skill

Handles optional artifact inputs in workflows, allowing workflows to proceed with or without optional artifacts.

## When to Use

Use this skill when:

- **Executing workflow steps** with inputs marked as `(optional)` in YAML
- **Building adaptive workflows** that gracefully degrade without certain inputs
- **Implementing fallback logic** for missing documentation artifacts
- **Documenting decision rationale** about optional artifact handling
- **Recovering from incomplete previous steps** without blocking progress

**Trigger Phrases**:

- "Check for optional artifact X"
- "Handle missing optional input"
- "Provide defaults for optional artifact"
- "Process step with optional artifacts"

## Invocation Examples

### Natural Language (Recommended)

```
"Check if infrastructure-config.json is available as an optional input"
"Handle the optional UX spec artifact for code review"
"Provide defaults for missing test-plan from Step 5"
```

### Skill Tool (Programmatic)

```javascript
// In agent workflow execution
Skill: optional - artifact - handler;

// With specific context
await skillManager.invoke('optional-artifact-handler', {
  artifactName: 'infrastructure-config.json',
  workflowId: 'workflow-123',
  step: 7,
});
```

## Instructions

### Step 1: Detect Optional Artifacts

1. **Check workflow step definition**:
   - Review step inputs in workflow YAML
   - Identify which inputs are marked as optional
   - Check artifact registry for availability

2. **Check artifact registry**:
   - Location: `.claude/context/artifacts/registry-{workflow_id}.json`
   - Check if optional artifact exists
   - Verify artifact validation status if present

**Example Registry Check**:

```json
{
  "artifacts": [
    {
      "name": "infrastructure-config.json",
      "path": ".claude/context/artifacts/infrastructure-config-workflow-123.json",
      "step": 4.5,
      "agent": "devops",
      "validated": true,
      "created_at": "2025-01-03T10:30:00Z"
    }
  ]
}
```

### Step 2: Handle Missing Optional Artifacts

1. **If artifact missing**:
   - Log in reasoning file: "Optional artifact {name} not found, using default"
   - Use default value or behavior
   - Continue workflow execution

2. **If artifact present**:
   - Load artifact from registry
   - Verify validation status
   - Use artifact value

**Example Handling Logic**:

```javascript
// Check registry
const registry = await readFile('.claude/context/artifacts/registry-workflow-123.json');
const artifact = registry.artifacts.find(a => a.name === 'infrastructure-config.json');

if (!artifact) {
  // Missing optional artifact - use defaults
  console.log(
    '[optional-artifact-handler] infrastructure-config.json not found, using empty config'
  );
  const config = { resources: [], environment_variables: {} };

  // Log decision
  await appendToReasoningFile({
    optional_artifact_handling: {
      artifact: 'infrastructure-config.json',
      status: 'missing',
      default_used: 'empty config object',
      impact: 'Cloud service integration stubs will use placeholder values',
    },
  });

  return config;
} else {
  // Artifact available - load it
  console.log(
    '[optional-artifact-handler] infrastructure-config.json found, loading from registry'
  );
  const config = await readFile(artifact.path);

  // Log decision
  await appendToReasoningFile({
    optional_artifact_handling: {
      artifact: 'infrastructure-config.json',
      status: 'available',
      source: artifact.path,
      impact: 'Cloud service integration will use actual resource names',
    },
  });

  return config;
}
```

### Step 3: Provide Defaults

1. **Default values**:
   - Use sensible defaults based on workflow context
   - Document default choice in reasoning file
   - Ensure defaults don't break workflow

2. **Default behaviors**:
   - Skip optional step if artifact missing
   - Use fallback logic when artifact unavailable
   - Continue with reduced functionality

**Example Default Strategies**:

| Optional Artifact            | Default Value                                  | Rationale                                                       |
| ---------------------------- | ---------------------------------------------- | --------------------------------------------------------------- |
| `infrastructure-config.json` | `{ resources: [], environment_variables: {} }` | Empty config allows code generation to proceed with stubs       |
| `ui-spec.json`               | `null`                                         | Code reviewer skips UI compliance checks                        |
| `test-plan.json`             | `{ test_cases: [] }`                           | Developer proceeds without test guidance                        |
| `prd.json`                   | `null`                                         | Architect designs without product requirements (technical debt) |

### Step 4: Document Handling

1. **Log in reasoning file**:
   - Document which optional artifacts were used
   - Document which defaults were applied
   - Record decision rationale

2. **Update plan**:
   - Note optional artifact handling in plan
   - Document impact on workflow execution
   - Track optional artifact usage

**Example Reasoning File Output**:

```json
{
  "step": 7,
  "agent": "developer",
  "optional_artifact_handling": {
    "timestamp": "2025-01-03T10:45:00Z",
    "artifacts_checked": [
      {
        "name": "infrastructure-config.json",
        "required": false,
        "found": false,
        "default_applied": "empty config object",
        "impact": "Cloud integration stubs will use placeholder resource names"
      },
      {
        "name": "ui-spec.json",
        "required": false,
        "found": true,
        "source": ".claude/context/artifacts/ui-spec-workflow-123.json",
        "impact": "UI components will follow specified design system"
      }
    ],
    "workflow_impact": "Proceeded with partial context - cloud integration requires manual configuration",
    "recommendations": [
      "Run DevOps step (4.5) to generate infrastructure-config.json",
      "Update cloud service stubs with actual resource names after infrastructure provisioning"
    ]
  }
}
```

## Complete Workflow Example

### Scenario: Developer Step with Optional Infrastructure Config

**Workflow YAML** (Step 7):

```yaml
- step: 7
  agent: developer
  prompt: Implement API endpoints and cloud integration
  inputs:
    - plan.json (from step 3)
    - architecture.json (from step 4)
    - infrastructure-config.json (from step 4.5, optional)
  outputs:
    - dev-manifest.json
  validation:
    schema: .claude/schemas/dev_manifest.schema.json
```

**Step 1: Check Registry**

```bash
# Agent reads artifact registry
cat .claude/context/artifacts/registry-workflow-123.json

# Output:
# {
#   "artifacts": [
#     {
#       "name": "plan.json",
#       "path": ".claude/context/artifacts/plan-workflow-123.json",
#       "step": 3,
#       "validated": true
#     },
#     {
#       "name": "architecture.json",
#       "path": ".claude/context/artifacts/architecture-workflow-123.json",
#       "step": 4,
#       "validated": true
#     }
#     // Note: infrastructure-config.json is MISSING
#   ]
# }
```

**Step 2: Detect Missing Optional Artifact**

```javascript
// Developer agent logic
const requiredArtifacts = ['plan.json', 'architecture.json'];
const optionalArtifacts = ['infrastructure-config.json'];

// Check required artifacts (must exist)
for (const artifact of requiredArtifacts) {
  const found = registry.artifacts.find(a => a.name === artifact);
  if (!found) {
    throw new Error(`Required artifact ${artifact} not found`);
  }
}

// Check optional artifacts (graceful degradation)
const infraConfig = registry.artifacts.find(a => a.name === 'infrastructure-config.json');
if (!infraConfig) {
  console.log('[optional-artifact-handler] infrastructure-config.json missing - using defaults');
}
```

**Step 3: Apply Defaults**

```javascript
// Use default empty infrastructure config
const infrastructureConfig = infraConfig
  ? await readFile(infraConfig.path)
  : {
      cloud_provider: 'gcp',
      resources: [],
      environment_variables: {},
      service_accounts: [],
    };

// Generate code with placeholders
const storageClient = `
// TODO: Update with actual bucket name from infrastructure-config.json
const bucketName = process.env.STORAGE_BUCKET || 'placeholder-bucket';
const storage = new Storage({ projectId: process.env.GCP_PROJECT_ID });
`;
```

**Step 4: Document in Reasoning File**

```json
{
  "step": 7,
  "agent": "developer",
  "optional_artifact_handling": {
    "timestamp": "2025-01-03T10:45:00Z",
    "missing_optional_artifacts": ["infrastructure-config.json"],
    "defaults_applied": {
      "infrastructure-config.json": {
        "default_value": "empty config with placeholder resource names",
        "rationale": "DevOps step (4.5) was skipped - proceeding with stubs",
        "workaround": "Using environment variables and placeholder names",
        "follow_up_required": true,
        "follow_up_action": "Run DevOps step to generate actual infrastructure config"
      }
    },
    "code_generation_impact": [
      "Cloud storage client uses placeholder bucket name",
      "Database connection uses placeholder credentials",
      "Message queue client uses default topic names"
    ],
    "runtime_requirements": [
      "Set STORAGE_BUCKET environment variable before deployment",
      "Set DATABASE_URL environment variable before deployment",
      "Configure GCP_PROJECT_ID environment variable"
    ]
  }
}
```

**Step 5: Continue Execution**

```javascript
// Developer continues with implementation
const manifest = {
  files_created: [
    'src/services/storage.ts', // Uses placeholder bucket name
    'src/services/database.ts', // Uses placeholder connection string
    'src/api/upload.ts', // API endpoint implementation
  ],
  files_modified: [],
  dependencies_added: ['@google-cloud/storage', 'pg'],
  tests_created: ['tests/api/upload.test.ts'],
  notes: [
    'infrastructure-config.json was not available',
    'Cloud service clients use placeholder resource names',
    'Run DevOps step (4.5) and update service configurations',
  ],
};

// Save manifest
await writeFile('.claude/context/artifacts/dev-manifest-workflow-123.json', manifest);
```

## Optional Artifact Patterns

### Pattern 1: Optional Documentation

**Use Case**: Code review can proceed without PRD or UX spec

```yaml
- step: 8
  agent: code-reviewer
  inputs:
    - dev-manifest.json (from step 7)
    - prd.json (from step 2, optional)
    - ui-spec.json (from step 4.1, optional)
```

**Handling Logic**:

```javascript
const prd = await loadOptionalArtifact('prd.json');
const uiSpec = await loadOptionalArtifact('ui-spec.json');

const reviewChecks = {
  code_quality: true, // Always check
  architecture_compliance: true, // Always check
  prd_alignment: !!prd, // Only if PRD available
  ui_compliance: !!uiSpec, // Only if UI spec available
};

if (!prd) {
  console.log('[code-reviewer] PRD not available - skipping requirements alignment check');
}

if (!uiSpec) {
  console.log('[code-reviewer] UI spec not available - skipping design system compliance');
}
```

### Pattern 2: Optional Previous Artifacts

**Use Case**: Architect can design without existing legacy system analysis

```yaml
- step: 4
  agent: architect
  inputs:
    - prd.json (from step 2)
    - legacy-analysis.json (from step 3.5, optional)
```

**Handling Logic**:

```javascript
const legacyAnalysis = await loadOptionalArtifact('legacy-analysis.json');

const architectureConstraints = legacyAnalysis
  ? {
      legacy_integrations: legacyAnalysis.integration_points,
      migration_requirements: legacyAnalysis.migration_strategy,
      compatibility_constraints: legacyAnalysis.constraints,
    }
  : {
      legacy_integrations: [],
      migration_requirements: 'greenfield',
      compatibility_constraints: [],
    };
```

### Pattern 3: Optional Validation Artifacts

**Use Case**: QA can test without performance benchmarks

```yaml
- step: 9
  agent: qa
  inputs:
    - dev-manifest.json (from step 7)
    - performance-baseline.json (from step 8.5, optional)
```

**Handling Logic**:

```javascript
const performanceBaseline = await loadOptionalArtifact('performance-baseline.json');

const testSuite = {
  unit_tests: true, // Always run
  integration_tests: true, // Always run
  e2e_tests: true, // Always run
  performance_tests: !!performanceBaseline, // Only if baseline available
};

if (!performanceBaseline) {
  console.log('[qa] Performance baseline not available - skipping performance regression tests');
  console.log('[qa] Will establish new baseline instead of comparing against existing');
}
```

## Example Output/Logging Format

### Console Logging Pattern

```
[optional-artifact-handler] Checking for optional artifact: infrastructure-config.json
[optional-artifact-handler] Registry path: .claude/context/artifacts/registry-workflow-123.json
[optional-artifact-handler] ✗ infrastructure-config.json NOT FOUND (optional)
[optional-artifact-handler] ✓ Applying default: empty config object
[optional-artifact-handler] Impact: Cloud integration stubs will use placeholder values
[optional-artifact-handler] Recommendation: Run DevOps step (4.5) to generate infrastructure config
[optional-artifact-handler] Documenting decision in reasoning file
```

### Reasoning File Entry

```json
{
  "optional_artifact_handling": {
    "timestamp": "2025-01-03T10:45:00Z",
    "workflow_id": "workflow-123",
    "step": 7,
    "agent": "developer",
    "artifacts_checked": [
      {
        "name": "infrastructure-config.json",
        "required": false,
        "found": false,
        "registry_path": ".claude/context/artifacts/registry-workflow-123.json",
        "default_strategy": "empty_config",
        "default_value": {
          "cloud_provider": "gcp",
          "resources": [],
          "environment_variables": {},
          "service_accounts": []
        },
        "impact_assessment": {
          "severity": "medium",
          "areas_affected": ["cloud_integration", "deployment"],
          "workarounds_applied": ["environment_variables", "placeholder_names"],
          "follow_up_required": true,
          "follow_up_steps": ["Run step 4.5 (DevOps)", "Update service configurations"]
        }
      }
    ],
    "workflow_continuity": "proceeded_with_defaults",
    "quality_impact": "technical_debt_introduced",
    "recommendations": [
      "Run DevOps workflow step (4.5) to generate infrastructure-config.json",
      "Update cloud service clients with actual resource names after infrastructure provisioning",
      "Set required environment variables before deployment"
    ]
  }
}
```

### Artifact Registry Update

```json
{
  "artifacts": [
    {
      "name": "dev-manifest.json",
      "path": ".claude/context/artifacts/dev-manifest-workflow-123.json",
      "step": 7,
      "agent": "developer",
      "validated": true,
      "created_at": "2025-01-03T10:50:00Z",
      "metadata": {
        "optional_artifacts_used": [],
        "optional_artifacts_missing": ["infrastructure-config.json"],
        "defaults_applied": ["infrastructure-config.json"],
        "quality_notes": "Cloud integration uses placeholder values - requires manual configuration"
      }
    }
  ]
}
```

## Related Documentation

- [Orchestrator Agent](../../agents/orchestrator.md) - Optional Input Handling
- [Developer Agent](../../agents/developer.md) - Cloud Integration Patterns
- [Workflow Guide](../../workflows/WORKFLOW-GUIDE.md) - Optional Inputs Section
- [CUJ-038](../../docs/cujs/CUJ-038.md) - Optional Artifact Handling
