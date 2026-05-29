---
name: name-phase-outputs
description: Phase output file naming conventions and format standards
---

# Output File Naming Convention

## Standard Format

All phase outputs MUST follow this naming convention:

```
.claude/.localmemory/create-{module-identifier}/phase-{NN}-{phase-name}.json
```

Where:
- `{module-identifier}`: Module identifier (e.g., `github-github`, `amazon-aws-s3`)
- `{NN}`: Two-digit phase number (01, 02, 03, etc.)
- `{phase-name}`: Short descriptive name (lowercase, hyphen-separated)

## Phase Output Files

### Phase 1: Discovery & Analysis
**File:** `phase-01-discovery.json`

**Content:**
```json
{
  "phase": 1,
  "name": "Discovery & Analysis",
  "status": "completed",
  "timestamp": "2025-10-08T10:00:00Z",
  "productPackage": "@auditlogic/product-github-github",
  "modulePackage": "@zerobias-org/module-github-github",
  "moduleIdentifier": "github-github",
  "serviceName": "GitHub",
  "productInfo": {
    "vendor": "github",
    "suite": null,
    "service": "github",
    "description": "GitHub API",
    "baseUrl": "https://api.github.com"
  },
  "credentials": {
    "status": "found",
    "authMethod": "Bearer token",
    "profile": "tokenProfile.yml"
  },
  "selectedOperation": {
    "name": "listRepositories",
    "method": "GET",
    "endpoint": "/user/repos",
    "reasoning": "Simplest GET operation with no required parameters"
  },
  "apiResearch": {
    "connectionTested": true,
    "operationTested": true,
    "responsesFolder": "_work/test-responses/"
  }
}
```

### Phase 2: Module Scaffolding
**File:** `phase-02-scaffolding.json`

**Content:**
```json
{
  "phase": 2,
  "name": "Module Scaffolding",
  "status": "completed",
  "timestamp": "2025-10-08T10:30:00Z",
  "modulePath": "package/github/github",
  "moduleIdentifier": "github-github",
  "yeomanCommand": "yo @auditmation/hub-module ...",
  "validations": {
    "1_directoryStructure": { "status": "passed" },
    "2_packageJsonMetadata": { "status": "passed" },
    "3_apiYmlProductReference": { "status": "passed" },
    "4_apiYmlTitleVersion": { "status": "passed" },
    "5_connectionProfileExists": { "status": "passed" },
    "6_connectionStateExists": { "status": "passed" },
    "7_sourceFilesExist": { "status": "passed" },
    "8_testFilesExist": { "status": "passed" },
    "9_dependenciesInstalled": { "status": "passed" },
    "10_symlinksCreated": { "status": "passed" },
    "11_typescriptConfigValid": { "status": "passed" }
  },
  "validationSummary": {
    "total": 11,
    "passed": 11,
    "failed": 0
  },
  "note": "Build validation deferred to Phase 8 (stubs are not yet fully implemented)",
  "gitCommit": {
    "hash": "abc123...",
    "message": "chore: scaffold github-github module"
  }
}
```

### Phase 3: API Specification
**File:** `phase-03-api-spec.json`

**Content:**
```json
{
  "phase": 3,
  "name": "API Specification",
  "status": "completed",
  "timestamp": "2025-10-08T11:00:00Z",
  "files": {
    "apiYml": "package/github/github/api.yml",
    "connectionProfile": "package/github/github/connectionProfile.yml",
    "connectionState": "package/github/github/connectionState.yml"
  },
  "apiSpec": {
    "operations": ["connect", "listRepositories"],
    "schemas": ["ConnectionProfile", "ConnectionState", "Repository"],
    "securityScheme": "bearer"
  },
  "gate1": {
    "status": "passed",
    "validations": {
      "noDescribeOperations": "passed",
      "onlySuccessResponses": "passed",
      "camelCaseProperties": "passed",
      "nestedObjectsUseRef": "passed",
      "noEnvelopeSchemas": "passed"
    }
  }
}
```

### Phase 4: Type Generation
**File:** `phase-04-type-generation.json`

**Content:**
```json
{
  "phase": 4,
  "name": "Type Generation",
  "status": "completed",
  "timestamp": "2025-10-08T11:15:00Z",
  "command": "npm run clean && npm run generate",
  "exitCode": 0,
  "generatedFiles": [
    "generated/api/index.ts",
    "generated/api/GithubConnector.ts",
    "generated/model/Repository.ts",
    "generated/model/ConnectionProfile.ts",
    "generated/model/ConnectionState.ts"
  ],
  "gate2": {
    "status": "passed",
    "validations": {
      "generationSuccess": "passed",
      "noInlineTypes": "passed",
      "noCompilationErrors": "passed"
    }
  }
}
```

### Phase 5: Core Implementation
**File:** `phase-05-implementation.json`

**Content:**
```json
{
  "phase": 5,
  "name": "Core Implementation",
  "status": "completed",
  "timestamp": "2025-10-08T12:00:00Z",
  "implementedFiles": {
    "client": "src/Client.ts",
    "connector": "src/GithubConnectorImpl.ts",
    "producers": ["src/RepositoryProducer.ts"],
    "mappers": "src/Mappers.ts"
  },
  "gate3": {
    "status": "passed",
    "validations": {
      "noAnyTypes": "passed",
      "usingGeneratedTypes": "passed",
      "connectorExtendsInterface": "passed",
      "metadataBoilerplate": "passed",
      "isSupportedBoilerplate": "passed",
      "mappersUseConstOutput": "passed"
    }
  }
}
```

### Phase 6: Testing Setup
**File:** `phase-06-testing.json`

**Content:**
```json
{
  "phase": 6,
  "name": "Testing Setup",
  "status": "completed",
  "timestamp": "2025-10-08T13:00:00Z",
  "testFiles": {
    "connectionUnit": "test/unit/ConnectionTest.ts",
    "repositoryUnit": "test/unit/RepositoryProducerTest.ts",
    "connectionIntegration": "test/integration/ConnectionTest.ts",
    "repositoryIntegration": "test/integration/RepositoryTest.ts"
  },
  "testExecution": {
    "command": "npm test",
    "exitCode": 0,
    "totalTests": 12,
    "passed": 12,
    "failed": 0
  },
  "gate4": {
    "status": "passed",
    "validations": {
      "testsCreated": "passed",
      "onlyNockForMocking": "passed",
      "noHardcodedValues": "passed"
    }
  },
  "gate5": {
    "status": "passed",
    "validations": {
      "allTestsPass": "passed",
      "noRegressions": "passed"
    }
  }
}
```

### Phase 7: Documentation
**File:** `phase-07-documentation.json`

**Content:**
```json
{
  "phase": 7,
  "name": "Documentation",
  "status": "completed",
  "timestamp": "2025-10-08T13:30:00Z",
  "files": {
    "userguide": "package/github/github/USERGUIDE.md",
    "readme": "package/github/github/README.md"
  },
  "content": {
    "credentialAcquisition": true,
    "connectionSetup": true,
    "operationExamples": true
  }
}
```

### Phase 8: Build & Finalization
**File:** `phase-08-build.json`

**Content:**
```json
{
  "phase": 8,
  "name": "Build & Finalization",
  "status": "completed",
  "timestamp": "2025-10-08T14:00:00Z",
  "build": {
    "command": "npm run build",
    "exitCode": 0,
    "outputFiles": ["dist/index.js", "dist/index.d.ts"]
  },
  "shrinkwrap": {
    "command": "npm run shrinkwrap",
    "exitCode": 0,
    "file": "npm-shrinkwrap.json"
  },
  "gate6": {
    "status": "passed",
    "validations": {
      "buildSuccess": "passed",
      "noErrors": "passed",
      "distFilesCreated": "passed",
      "shrinkwrapCreated": "passed"
    }
  }
}
```

### Phase 9: Final Validation
**File:** `phase-09-validation.json`

**Content:**
```json
{
  "phase": 9,
  "name": "Final Validation",
  "status": "completed",
  "timestamp": "2025-10-08T14:15:00Z",
  "allGates": {
    "gate1_apiSpec": "passed",
    "gate2_typeGeneration": "passed",
    "gate3_implementation": "passed",
    "gate4_testCreation": "passed",
    "gate5_testExecution": "passed",
    "gate6_build": "passed"
  },
  "moduleReady": true,
  "deploymentReady": true
}
```

## Sub-Step Outputs (Optional)

If a phase has multiple sub-steps that need separate tracking:

```
phase-01-product-discovery.json
phase-01-api-research.json
phase-01-operation-selection.json
phase-01-credentials.json
```

**Format:** `phase-{NN}-{step-name}.json`

Use this ONLY when sub-steps are significant enough to warrant separate output files.

## Working Files (Not Phase Outputs)

Files in `_work/` directory don't follow this convention:

```
.claude/.localmemory/create-{module-id}/_work/
├── product-model.md
├── api-research.md
├── operation-selection.md
├── credentials-status.md
└── test-responses/
    ├── auth-response.json
    └── operation-response.json
```

These are intermediate working files, not formal phase outputs.

## Agent Responsibilities

**Every agent** must:
1. Know which phase output file to read from (input)
2. Know which phase output file to write to (output)
3. Update the status field appropriately
4. Include timestamp for all operations
5. Report validation results in structured format

## File Lifecycle

```
Phase N starts
  ↓
Read: phase-{N-1}-*.json (previous phase output)
  ↓
Execute work
  ↓
Write: phase-{N}-*.json (current phase output)
  ↓
Phase N complete
```

## Rules Enforcement

- ✅ ALWAYS use this naming convention
- ✅ ALWAYS include phase number, name, status, timestamp
- ✅ ALWAYS use structured JSON format
- ❌ NEVER use arbitrary file names
- ❌ NEVER skip phase output files
- ❌ NEVER use old naming (task-01, task-02, etc.)

## Migration from Old Naming

**Old:** `task-01-output.json`, `task-02-output.json`, etc.
**New:** `phase-01-discovery.json`, `phase-02-scaffolding.json`, etc.

All new work uses the NEW naming convention.
