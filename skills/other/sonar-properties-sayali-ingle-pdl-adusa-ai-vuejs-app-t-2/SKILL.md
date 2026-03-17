---
name: sonar-properties
description: Generates sonar-project.properties for SonarQube code quality analysis and coverage reporting. Auto-detects test framework (Jest/Vitest) and configures coverage paths.
---

# SonarQube Properties Skill

## Purpose
Generate SonarQube project configuration file for code quality analysis and coverage reporting with automatic detection of test framework and coverage paths.

## 🚨 MANDATORY FILE COUNT
**Expected Output**: **1 file**
- `sonar-project.properties`

## 🔍 BEFORE GENERATING - CRITICAL RESEARCH REQUIRED

Perform these checks in order before generating the configuration:

1. **Application Name Detection**: Use `application_name` parameter
   - **Format**: Use application_name as-is for projectKey and projectName
   - **Placeholder**: `{application_name}` will be replaced with actual value
   - **User Action Required**: Inform user to review and update projectKey, projectName, and projectDescription after generation

2. **Test Framework Detection**: Determine which test framework is used
   - **Check `package.json` dependencies**:
     - If `"vitest"` found → **Vitest** (uses `coverage/lcov.info`, coverage provider: v8 or istanbul)
     - If `"jest"` found → **Jest** (uses `coverage/lcov.info` and `coverage/clover.xml`)
     - If neither found → **Default to Vitest** (Vue 3 standard)
   - **Impact**: Determines which coverage report paths to include

3. **Coverage Report Path Detection**: Verify coverage output location
   - **Default**: `./coverage/lcov.info` (both Jest and Vitest)
   - **Additional for Jest**: `./coverage/clover.xml`
   - **Vitest v8 provider**: Only `lcov.info` (no clover)
   - **Check**: Verify coverage configuration in test framework config
   - **Fallback**: Use standard paths if not specified

4. **Source Directory Detection**: Verify source code location
   - **Standard**: `src` directory
   - **Check**: Verify `src/` exists in project structure
   - **Alternative**: If different, detect from `package.json` or `tsconfig.json`

5. **Coverage Exclusion Patterns**: Detect files to exclude from coverage
   - **Always Exclude**:
     - Test files: `src/**/*.spec.ts`
     - Entry point: `src/main.ts` (if exists)
   - **Conditionally Exclude** (check if exists):
     - Services: `src/services/**/*.ts` (API layer, tested with mocks)
     - Router: `src/**/router/*.ts` (configuration, tested E2E)
     - Store index: `src/store/index.ts` (setup file)
     - Interfaces: `src/**/interfaces/*.ts` (type definitions only)
     - Constants: `src/**/shared/constants/**/*.ts` (static data)
   - **Action**: Build exclusion list based on detected files

6. **Language Detection**: Verify primary language
   - **Standard**: TypeScript (`ts`)
   - **Check**: Look for `typescript` in package.json dependencies
   - **Alternative**: If no TypeScript, use `js`

7. **Git Provider Detection**: Determine SCM provider
   - **Default**: `git`
   - **Check**: `.git` directory exists
   - **Note**: SonarQube property is informational

8. **Encoding Verification**: Confirm source file encoding
   - **Standard**: `UTF-8`
   - **Note**: Modern projects always use UTF-8

## Execution Checklist

Execute in this order:

- [ ] 1. Get `application_name` from configuration parameters
- [ ] 2. Detect test framework (Vitest vs Jest) from package.json
- [ ] 3. Determine coverage report paths based on test framework
- [ ] 4. Verify `src/` directory exists
- [ ] 5. Detect which files/directories exist for coverage exclusions:
  - [ ] `src/main.ts`
  - [ ] `src/services/` directory
  - [ ] `src/**/router/` directories
  - [ ] `src/store/index.ts`
  - [ ] `src/**/interfaces/` directories
  - [ ] `src/**/shared/constants/` directories
- [ ] 6. Build coverage.exclusions list from detected patterns
- [ ] 7. Verify TypeScript is used (check package.json)
- [ ] 8. Generate `sonar-project.properties` with detected configuration
- [ ] 9. Run validation script to confirm file exists and properties are valid
- [ ] 10. **IMPORTANT**: Notify user to review projectKey, projectName, and projectDescription

## Output

### Primary Format: `sonar-project.properties`

**For Vitest Projects** (recommended):
```properties
sonar.projectKey={application_name}
sonar.projectName={application_name}
sonar.projectDescription=Vue 3 application for {application_name}
sonar.sources=src
sonar.language=ts
sonar.sourceEncoding=UTF-8
sonar.scm.provider=git
sonar.qualitygate.wait=true
sonar.javascript.lcov.reportPaths=./coverage/lcov.info
sonar.tests=src
sonar.test.inclusions=src/**/*.spec.ts
sonar.exclusions=src/**/*.spec.ts
sonar.coverage.exclusions=src/main.ts,src/services/**/*.ts,src/**/router/*.ts
```

**For Jest Projects**:
```properties
sonar.projectKey={application_name}
sonar.projectName={application_name}
sonar.projectDescription=Vue 3 application for {application_name}
sonar.sources=src
sonar.language=ts
sonar.sourceEncoding=UTF-8
sonar.scm.provider=git
sonar.qualitygate.wait=true
sonar.javascript.lcov.reportPaths=./coverage/lcov.info
sonar.clover.reportPaths=./coverage/clover.xml
sonar.tests=src
sonar.test.inclusions=src/**/*.spec.ts
sonar.exclusions=src/**/*.spec.ts
sonar.coverage.exclusions=src/main.ts,src/services/**/*.ts,src/**/router/*.ts
```

**Key Difference**: Jest includes `sonar.clover.reportPaths`, Vitest does not.

## 🛑 BLOCKING VALIDATION CHECKPOINT

After generating the file, run this validation:

```bash
#!/bin/bash

# Validate sonar-project.properties exists
if [ ! -f "sonar-project.properties" ]; then
  echo "✗ ERROR: sonar-project.properties not found"
  exit 1
fi

echo "✓ Found: sonar-project.properties"

# Validate required properties exist
REQUIRED_PROPS=(
  "sonar.projectKey"
  "sonar.projectName"
  "sonar.sources"
  "sonar.language"
  "sonar.sourceEncoding"
  "sonar.qualitygate.wait"
  "sonar.javascript.lcov.reportPaths"
  "sonar.tests"
  "sonar.test.inclusions"
  "sonar.exclusions"
  "sonar.coverage.exclusions"
)

MISSING_PROPS=()
for prop in "${REQUIRED_PROPS[@]}"; do
  if ! grep -q "^$prop=" sonar-project.properties; then
    MISSING_PROPS+=("$prop")
  fi
done

if [ ${#MISSING_PROPS[@]} -gt 0 ]; then
  echo "✗ ERROR: Missing required properties:"
  printf '  - %s\n' "${MISSING_PROPS[@]}"
  exit 1
fi

# Validate coverage report paths exist or are configured
LCOV_PATH=$(grep "^sonar.javascript.lcov.reportPaths=" sonar-project.properties | cut -d'=' -f2)
if [ -z "$LCOV_PATH" ]; then
  echo "✗ ERROR: Missing LCOV report path"
  exit 1
fi

# Check for test framework specific paths
if grep -q "vitest" package.json; then
  echo "✓ Detected Vitest - LCOV only"
  if grep -q "sonar.clover.reportPaths" sonar-project.properties; then
    echo "⚠️ WARNING: Vitest detected but clover path included (Jest-specific)"
  fi
elif grep -q "jest" package.json; then
  echo "✓ Detected Jest - LCOV + Clover"
  if ! grep -q "sonar.clover.reportPaths" sonar-project.properties; then
    echo "⚠️ WARNING: Jest detected but clover path missing"
  fi
fi

# Validate sources directory exists
SOURCES_DIR=$(grep "^sonar.sources=" sonar-project.properties | cut -d'=' -f2)
if [ ! -d "$SOURCES_DIR" ]; then
  echo "✗ ERROR: Sources directory not found: $SOURCES_DIR"
  exit 1
fi

echo "✓ Sources directory exists: $SOURCES_DIR"

# Validate language is set correctly
LANGUAGE=$(grep "^sonar.language=" sonar-project.properties | cut -d'=' -f2)
if [ "$LANGUAGE" != "ts" ] && [ "$LANGUAGE" != "js" ]; then
  echo "✗ ERROR: Invalid language: $LANGUAGE (expected 'ts' or 'js')"
  exit 1
fi

echo "✓ Language: $LANGUAGE"

# Validate encoding
ENCODING=$(grep "^sonar.sourceEncoding=" sonar-project.properties | cut -d'=' -f2)
if [ "$ENCODING" != "UTF-8" ]; then
  echo "⚠️ WARNING: Non-standard encoding: $ENCODING (expected 'UTF-8')"
fi

# Validate exclusions are properly formatted (no spaces after commas in list)
EXCLUSIONS=$(grep "^sonar.coverage.exclusions=" sonar-project.properties | cut -d'=' -f2)
if [[ "$EXCLUSIONS" =~ ", " ]]; then
  echo "⚠️ WARNING: Coverage exclusions contain spaces after commas (should be comma-separated without spaces)"
fi

echo ""
echo "✓ SonarQube configuration validation passed"
echo ""
echo "⚠️ IMPORTANT: Please review and update the following properties:"
echo "   - sonar.projectKey (currently: $(grep '^sonar.projectKey=' sonar-project.properties | cut -d'=' -f2))"
echo "   - sonar.projectName (currently: $(grep '^sonar.projectName=' sonar-project.properties | cut -d'=' -f2))"
echo "   - sonar.projectDescription (currently: $(grep '^sonar.projectDescription=' sonar-project.properties | cut -d'=' -f2))"
```

**Validation Requirements**:
1. ✅ File `sonar-project.properties` exists
2. ✅ All required properties present
3. ✅ Coverage report paths configured based on test framework
4. ✅ Sources directory exists
5. ✅ Language is valid (`ts` or `js`)
6. ✅ Encoding is UTF-8
7. ⚠️ Coverage exclusions properly formatted (no spaces)
8. ⚠️ User notified to review projectKey, projectName, projectDescription

## Template Reference
See: `examples.md` in this directory for:
- Complete `sonar-project.properties` examples (Vitest and Jest variants)
- Detailed property explanations with why each is configured
- Test framework detection guide
- Coverage path verification commands
- Common issues and troubleshooting
- Property customization guide

## Notes

### Key Features
- **Automatic Test Framework Detection**: Vitest vs Jest from package.json
- **Dynamic Coverage Paths**: Adapts to test framework capabilities
- **Smart Exclusions**: Only excludes files that exist in project
- **Application Name Integration**: Uses configured application_name parameter
- **User Review Required**: Notifies user to update project metadata

### Property Essentials
- **projectKey/projectName**: Uses application_name, user must review
- **projectDescription**: Generic description, user should customize
- **sources**: Always `src` (standard Vue project structure)
- **language**: `ts` for TypeScript projects
- **sourceEncoding**: Always `UTF-8` (modern standard)
- **scm.provider**: `git` (standard version control)
- **qualitygate.wait**: `true` (wait for quality gate results)

### Coverage Configuration
- **LCOV**: Universal format supported by both Jest and Vitest
- **Clover**: Jest-specific XML format (not used by Vitest)
- **Test Inclusions**: `src/**/*.spec.ts` (all test files)
- **Source Exclusions**: Test files excluded from analysis
- **Coverage Exclusions**: Entry points, services, routers, config files

### Coverage Exclusion Philosophy
- **Test Files**: No runtime code, shouldn't count toward coverage
- **Entry Point (main.ts)**: Application bootstrap, tested through E2E
- **Services**: API layer, tested with mocks, not unit testable
- **Router**: Configuration files, tested through E2E navigation
- **Store Index**: Setup/configuration, not meaningful to unit test
- **Interfaces**: TypeScript type definitions only, no runtime code
- **Constants**: Static data, no logic to test

### Test Framework Differences
- **Vitest**: Modern, Vue 3 recommended, v8 or istanbul coverage, LCOV only
- **Jest**: Legacy but widely used, multiple coverage formats (LCOV + Clover)
- **Detection**: Check package.json dependencies for framework presence
- **Default**: Assume Vitest if neither found (Vue 3 standard)

### Quality Gate Configuration
- **qualitygate.wait=true**: CI/CD pipeline waits for SonarQube analysis
- **Purpose**: Prevent merging code that fails quality standards
- **Timeout**: Controlled by SonarQube server configuration
- **Impact**: CI/CD build may fail if quality gate not passed

### Maintenance Considerations
- **SonarQube Version**: Properties may change between SonarQube versions
- **Coverage Formats**: Verify test framework still generates expected formats
- **Path Changes**: Update if project structure changes
- **New Exclusions**: Add patterns as project grows
- **Property Deprecation**: Monitor SonarQube release notes

### Common Customizations
- **Organization Key**: Add `sonar.organization` for SonarCloud
- **Branch Analysis**: Add `sonar.branch.name` for branch-specific analysis
- **PR Analysis**: Add PR-specific properties for pull request decoration
- **Authentication**: Add `sonar.login` token (usually in CI/CD environment)
- **Additional Exclusions**: Extend based on project needs

