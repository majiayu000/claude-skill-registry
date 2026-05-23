---
name: iot-edge-module
description: This skill should be used when creating a new Azure IoT Edge module. Use when the user requests to scaffold, create, or set up a new edge module. The skill automates module scaffolding, manifest configuration, and shared contract generation with intelligent project structure detection.
---

# IoT Edge Module Scaffolding Skill

This skill automates the creation of new Azure IoT Edge modules. Use this skill to scaffold a complete module structure including source code, Docker configuration, deployment manifests, and shared contracts.

## Execution Environment

**IMPORTANT: All bash commands MUST use Unix syntax regardless of platform.**

- Always use Unix bash syntax (e.g., `test -d`, `[ -f ]`, etc.)
- NEVER use Windows CMD syntax (e.g., `if exist`, `dir`, etc.)
- NEVER pipe commands to null (`2>/dev/null`, `2>nul`, etc.) - let all output and errors show naturally
- Bash is available on all platforms: native on Linux/macOS, via WSL/Git Bash on Windows
- Python scripts are cross-platform and handle path normalization internally

## Communication Guidelines

**Be concise and avoid stating obvious or expected behavior:**

- Don't explain why assets are in the plugin directory (this is expected)
- Don't describe where script files "should" be located (this is obvious)
- Focus output on actionable information, progress, and actual errors only
- Avoid verbose explanations of normal/expected conditions

## When to Use This Skill

Trigger this skill when the user requests to:

- Create a new IoT Edge module
- Scaffold an edge module
- Set up a new module for IoT Edge
- Add a new module to the edge deployment

## Prerequisites

Before scaffolding a module, gather the following information from the user:

1. **Module name** (PascalCase, e.g., "DataProcessorModule")
2. **Module description** (brief description of module purpose)

## Scaffolding Process

Follow these steps in order to scaffold a new IoT Edge module:

### Step 1: Detect or Load Project Structure

Run the project structure detection script to identify existing patterns:

```bash
python scripts/detect_project_structure.py --root .
```

### Step 1.5: Verify IoTEdgeModules Folder Structure

**Check if the IoTEdgeModules folder exists:**

If the detection script couldn't find `modules_base_path` or it doesn't exist:

**Prompt user:**

```
IoTEdgeModules folder not found. Where should modules be created?

1. Create at default location: src/IoTEdgeModules/modules/
2. Specify custom path
3. Cancel scaffolding

Choose option (1/2/3):
```

**If option 1 selected:**

- Create directory structure:
  ```
  src/IoTEdgeModules/
  ├── modules/
  └── config/
  ```
- Update detected configuration with this path

**If option 2 selected:**

- Prompt: "Enter custom IoTEdgeModules path (e.g., edge/modules/):"
- Validate path is reasonable
- Create directory structure at custom location
- Update detected configuration

**If option 3 selected:**

- Exit scaffolding with message: "Scaffolding cancelled by user"

**What this detects:**

- Modules base path (e.g., `src/IoTEdgeModules/modules`)
- Contracts project path and name
- Deployment manifests location
- Project namespace
- Container registry URL
- NuGet feed URL (if configured)

**Processing the output:**

1. Parse the JSON output
2. If `config_source` is `"saved"`, use the saved configuration silently
3. If `config_source` is `"detected"`, present findings to user for confirmation
4. If detection fails or user rejects, prompt for each value manually

**Confirmation prompt (if detected, not saved):**

Display the detected configuration to the user in a clear, readable format:

```
Detected project structure:
• Modules location: <modules_base_path>
• Project namespace: <project_namespace>
• Container registry: <container_registry>
• Contracts project: <contracts_project_name> (<contracts_project_path>)
• Deployment manifests: <manifests_found count> found
• NuGet feed: <nuget_feed_url or "Not configured">
```

Then use AskUserQuestion tool to ask for confirmation:

- **Question**: "Use this detected configuration?"
- **Header**: "Config"
- **Options**:
  1. "Yes, use it" - "Proceed with the detected configuration"
  2. "Save and use" - "Save this configuration for future modules and use it now"
  3. "No, customize" - "Manually specify configuration values instead"

**If user selects "Save and use":**

```bash
python scripts/detect_project_structure.py --root . --save
```

**If user selects "No, customize" or if detection fails, prompt for:**

- Project namespace (e.g., "Company.IoT.EdgeAPI")
- Container registry URL (e.g., "myregistry.azurecr.io")
- Modules base path (default: "src/IoTEdgeModules/modules")
- Contracts project name and path (or "none" if not using shared contracts)

### Step 2: Gather Module-Specific Information

Ask the user for:

**Required:**

1. **Module name** (PascalCase)
2. **Module description**

**Optional Features:**

**A. Private NuGet Feed**

- Ask: "Does this project require a private NuGet feed? (Yes/No)"
- If Yes and not detected: Prompt for NuGet feed URL
- If Yes and detected: Confirm detected URL or allow override

**B. Shared Contracts Project**

- If contracts project was detected: Automatically use it for module constants (no prompt needed)
- If not detected: Ask "Do you have a shared contracts project? (Yes/No/Create standalone)"

### Step 3: Validate and Normalize Module Names

Convert the user-provided module name to required formats:

**ModuleName (PascalCase):**

- Remove "Module" suffix if present, then add it back
- Example: "DataProcessor" → "DataProcessorModule"
- Example: "DataProcessorModule" → "DataProcessorModule"

**modulename (lowercase):**

- Convert ModuleName to lowercase
- Example: "DataProcessorModule" → "dataprocessormodule"

**Confirm with user using AskUserQuestion tool:**

Present the module details and ask for confirmation:

- **Question**: "Proceed with creating this module?"
- **Header**: "Confirm Module"
- **Options**:
  - "Yes, create module" → Continue to Step 4
  - "No, use different name" → Go back to Step 2 (gather module name)

Display in the question description:

```
Module will be created as:
• C# class name: <ModuleName>
• Module ID: <modulename>
• Directory: <modules_base_path>/<modulename>/
```

**Do NOT assume "Yes" or proceed without using AskUserQuestion tool and getting explicit user confirmation**

### Step 4: Create Module Directory Structure

Create the module directory:

```
<modules_base_path>/<modulename>/
```

Check if directory already exists (MUST use this exact bash syntax):

```bash
test -d "<modules_base_path>/<modulename>" && echo "EXISTS" || echo "NOT_EXISTS"
```

**Note:** Do NOT use Windows CMD syntax like `if exist`. Always use Unix bash syntax as shown above.

- If EXISTS: Ask user "Module directory exists. Overwrite? (Yes/Rename/Cancel)"
- If Rename: Prompt for new name and restart from Step 3

### Step 5: Generate Module Files from Templates

Use the template files in `assets/` to generate module files with runtime substitutions. The skill generates 11 files total.

**Placeholder substitutions:**

| Placeholder | Value | Example |
|-------------|-------|---------|
| `{{ModuleName}}` | PascalCase module name | DataProcessorModule |
| `{{modulename}}` | Lowercase module name | dataprocessormodule |
| `{{ModuleDescription}}` | User-provided description | Processes sensor data |
| `{{CONTAINER_REGISTRY}}` | Detected or provided registry | myregistry.azurecr.io |
| `{{PROJECT_NAMESPACE}}` | Detected or provided namespace | Company.IoT.EdgeAPI |
| `{{MODULE_CSPROJ_PATH}}` | Calculated module csproj path: `<modules_base_path>/<modulename>/<ModuleName>.csproj` | src/IoTEdgeModules/modules/dataprocessormodule/DataProcessorModule.csproj |
| `{{MODULE_PUBLISH_PATH}}` | Calculated publish path | src/IoTEdgeModules/modules/dataprocessormodule |
| `{{CONTRACTS_PROJECT_REFERENCE}}` | Conditional contracts reference | See below |
| `{{CONTRACTS_CSPROJ_COPY}}` | Conditional Dockerfile COPY | See below |
| `{{NUGET_CONFIG_SECTION}}` | Conditional NuGet configuration | See below |

**Conditional placeholder handling:**

**A. Contracts Project Reference (`{{CONTRACTS_PROJECT_REFERENCE}}`)**

**Calculate relative path from module directory to contracts directory:**

Example:

- Module at: `src/IoTEdgeModules/modules/mydemomodule/`
- Contracts at: `src/Company.IoT.Modules.Contracts/`
- Relative path: `../../../Company.IoT.Modules.Contracts`
  - Go up 3 levels: `mydemomodule/` → `modules/` → `IoTEdgeModules/` → `src/`
  - Then down to: `Company.IoT.Modules.Contracts/`

If using shared contracts:

```xml
  <ItemGroup>
    <ProjectReference Include="<relative-path-to-contracts>/<contracts_project_name>.csproj" />
  </ItemGroup>
```

If NOT using shared contracts:

```xml
  <!-- No shared contracts project -->
```

**B. Contracts Dockerfile COPY (`{{CONTRACTS_CSPROJ_COPY}}`)**

If using shared contracts:

```dockerfile
COPY <contracts_project_path>/*.csproj ./src/
```

If NOT using shared contracts:
```
(empty - no COPY line)
```

**C. NuGet Configuration (`{{NUGET_CONFIG_SECTION}}`)**

If using private NuGet feed:

```dockerfile
ENV VSS_NUGET_EXTERNAL_FEED_ENDPOINTS="{\"endpointCredentials\": [{\"endpoint\":\"<nuget_feed_url>\", \"username\":\"docker\", \"password\":\"${FEED_ACCESSTOKEN}\"}]}"

```

If NOT using private NuGet feed:

```
(empty - no ENV line)
```

**Template file mappings:**

| Template File | Target File | Notes |
|---------------|-------------|-------|
| `template.csproj` | `<ModuleName>.csproj` | Rename to match ModuleName |
| `template-module.json` | `module.json` | - |
| `template-Program.cs` | `Program.cs` | - |
| `template-Service.cs` | `<ModuleName>Service.cs` | Rename to match ModuleName |
| `template-GlobalUsings.cs` | `GlobalUsings.cs` | - |
| `template-ServiceLoggerMessages.cs` | `<ModuleName>ServiceLoggerMessages.cs` | Rename to match ModuleName |
| `template-Dockerfile.amd64` | `Dockerfile.amd64` | - |
| `template-Dockerfile.amd64.debug` | `Dockerfile.amd64.debug` | - |
| `template-.dockerignore` | `.dockerignore` | - |
| `template-.gitignore` | `.gitignore` | - |
| `template-launchSettings.json` | `Properties/launchSettings.json` | Create Properties/ first |

**Processing workflow:**

For each template file listed in the table above, process sequentially:

1. Read the template file from `assets/`
2. Replace all placeholders with calculated values
3. Write to target location in module directory using the target filename from the table
4. Report progress: "✓ Created <filename>"

Process all 11 files one at a time before proceeding to Step 6.

### Step 6: Create Shared Contract Constants (Conditional)

**If using shared contracts project:**

**Directory:** `<contracts_project_path>/<ModuleName>/`

**File:** `<ModuleName>Constants.cs`

**Process:**

1. Create directory if it doesn't exist
2. Read `template-ModuleConstants.cs`
3. Replace placeholders
4. Write to contracts project location

**If NOT using shared contracts:**

**Directory:** `<modules_base_path>/<modulename>/Contracts/`

**File:** `<ModuleName>Constants.cs`

**Process:**

1. Create `Contracts/` folder in module directory
2. Read `template-ModuleConstants.cs`
3. Replace `{{PROJECT_NAMESPACE}}.Modules.Contracts` with just `{{ModuleName}}.Contracts`
4. Write to module's Contracts folder

### Step 6.5: Create LoggingBuilderExtensions (First Module Only)

This extension method is required for `AddModuleConsoleLogging()` in Program.cs.

**If using shared contracts project:**

Check if `<contracts_project_path>/Extensions/LoggingBuilderExtensions.cs` exists:

- If file exists: Skip this step (already created by previous module)
- If file does NOT exist: Create it

**Directory:** `<contracts_project_path>/Extensions/`

**File:** `LoggingBuilderExtensions.cs`

**Process:**

1. Create `Extensions/` directory if it doesn't exist
2. Read `template-LoggingBuilderExtensions.cs`
3. Replace `{{PROJECT_NAMESPACE}}` placeholder
4. Write to contracts project Extensions folder
5. Report to user: "✓ Created LoggingBuilderExtensions.cs in shared contracts project"

**If NOT using shared contracts:**

**Directory:** `<modules_base_path>/<modulename>/Extensions/`

**File:** `LoggingBuilderExtensions.cs`

**Process:**

1. Create `Extensions/` folder in module directory
2. Read `template-LoggingBuilderExtensions.cs`
3. Replace `{{PROJECT_NAMESPACE}}.Modules.Contracts` with `{{ModuleName}}`
4. Write to module's Extensions folder

### Step 7: Scan and Select Deployment Manifests

Run the manifest scanning script:

```bash
python scripts/scan_manifests.py --root .
```

**Process the output:**

1. Parse JSON to get list of manifest files
2. If 0 manifests found: Go to Step 7.5 (create base manifest)
3. If 1 manifest found: Ask "Add module to <manifest_name>? (Yes/No)"
4. If multiple manifests found: Present selection list

### Step 7.5: Handle "No Manifests Found" Scenario

**If scan_manifests.py returns 0 manifests:**

**Prompt user:**

```
No deployment manifests found. This appears to be the first module in the project.

Create a base deployment manifest with this module? (Yes/No)
```

**If user selects No:**

- Skip to Step 9 (README update)
- Inform user: "Module created without deployment manifest. You'll need to create a manifest manually."

**If user selects Yes:**

1. **Prompt for manifest name:**
   ```
   Manifest name (default: base): _
   ```
   - Accept user input or use "base" as default
   - Validate name (alphanumeric, dashes, underscores only)

2. **Create base deployment manifest:**
   - Read template: `assets/template-base.deployment.manifest.json`
   - Determine manifest path: `<manifests_base_path>/{name}.deployment.manifest.json`
   - If `manifests_base_path` not detected, use `<modules_base_path>/../{name}.deployment.manifest.json`
   - Write base manifest to file

3. **Add the new module to the base manifest:**
   - Run update script:
     ```bash
     python scripts/update_deployment_manifest.py \
       "<manifest_path>" \
       "<modulename>" \
       --registry "<container_registry>"
     ```
   - This adds the newly scaffolded module as the first custom module

4. **Report to user:**
   ```
   ✓ Created base deployment manifest: <manifest_path>
   ✓ Added <modulename> to manifest (startup order: 1)
   ```

**Continue to Step 8 (or Step 9 if no updates needed)**

**Multi-manifest selection prompt:**

```
Found <count> deployment manifests:

1. <manifest_basename> (<modules_count> modules)
   Path: <manifest_path>

2. <manifest_basename> (<modules_count> modules)
   Path: <manifest_path>

Which manifest(s) should include this module?
(Enter numbers separated by commas, or 'all', or 'none')
```

### Step 8: Update Deployment Manifests (Automated)

For each selected manifest, run the update script:

```bash
python scripts/update_deployment_manifest.py \
  "<manifest_path>" \
  "<modulename>" \
  --registry "<container_registry>"
```

**Process the output:**

1. Check for `"success": true` in JSON output
2. Report to user: "✓ Added <modulename> to <manifest_name> (startup order: <startup_order>)"
3. If error: Report error and provide manual fallback instructions

**Error handling:**

If the script fails (e.g., module already exists, invalid JSON):

1. Show error message from script
2. Provide manual instructions:

```
Manual update required for <manifest_path>:

Add to $edgeAgent.properties.desired.modules:
{
  "<modulename>": {
    "version": "1.0",
    "type": "docker",
    "status": "running",
    "restartPolicy": "always",
    "startupOrder": <next-order>,
    "settings": {
      "image": "${MODULES.<modulename>}",
      "createOptions": {
        "HostConfig": {
          "LogConfig": {
            "Type": "json-file",
            "Config": {
              "max-size": "10m",
              "max-file": "10"
            }
          },
          "Mounts": [{
            "Type": "volume",
            "Target": "/app/data/",
            "Source": "<modulename>"
          }]
        }
      }
    }
  }
}

Add to $edgeHub.properties.desired.routes:
{
  "<modulename>ToIoTHub": {
    "route": "FROM /messages/modules/<modulename>/outputs/* INTO $upstream",
    "priority": 0,
    "timeToLiveSecs": 86400
  }
}
```

### Step 9: Update README.md (Optional)

Search for "Solution project overview" or "IoTEdge modules" section in README.md:

**If section exists:**

- Add entry: `- **<modulename>** (\`<module_path>\`) - <ModuleDescription>`
- Insert alphabetically

**If section doesn't exist:**

- Ask user: "README.md section not found. Create it? (Yes/No)"

### Step 9.5: Add Module to Solution File

**Detect solution file:**

Run the solution detection script:

```bash
python scripts/manage_solution.py --root . --detect
```

**Process detection results:**

**If .slnx file found:**

Automatically add module to solution:

```bash
python scripts/manage_solution.py \
  --root . \
  --add-module "<module_csproj_path>" \
  --module-name "<ModuleName>"
```

- Parse JSON output
- If `action: "added"`: Report "✓ Added to solution at position <insertion_index>"
- If `action: "already_exists"`: Report "Module already in solution"
- If `action: "error"`: Show error and continue

**If .sln file found:**

- Run manual instruction generator:
  ```bash
  python scripts/manage_solution.py \
    --root . \
    --add-module "<module_csproj_path>" \
    --module-name "<ModuleName>"
  ```
- Parse JSON output and display `instructions` field to user
- Recommend using: `dotnet sln add "<module_csproj_path>"`

**If no solution file found:**

- Skip this step
- Inform user: "No solution file found. Module created successfully without solution integration."

### Step 10: Provide Summary and Next Steps

**Summary of created files:**
```
✓ Module scaffolding complete!

Created:
• Module directory: <module_full_path>/ (11 files)
• Constants file: <constants_full_path>
• LoggingBuilderExtensions: <"Created" or "Already exists - skipped">
• Updated manifests: <manifest_count> manifest(s) [or "Created base manifest" if first module]
• Solution integration: <"Added to .slnx" or "Manual instructions provided" or "Skipped">

Configuration:
• Container registry: <container_registry>
• Project namespace: <project_namespace>
• NuGet feed: <nuget_feed_url or "None">
• Shared contracts: <"Yes" or "No">
```

**Next steps for the user:**

1. **Implement module logic:**
   - Edit `<ModuleName>Service.cs`
   - Add business logic in `ExecuteAsync()`
   - Register direct method handlers if needed

2. **Add dependencies (if needed):**
   - Update `<ModuleName>.csproj` with additional NuGet packages
   - Add service registrations in `Program.cs`

3. **Configure module (if needed):**
   - Create options classes in `Options/` folder
   - Add environment variables to deployment manifest:
     ```json
     "env": {
       "MyOptions__Setting": { "value": "value" }
     }
     ```

4. **Test locally:**
   - Use `Properties/launchSettings.json` for standalone mode
   - Run: `dotnet run --project <module_path>`
   - Module runs with mock IoT Hub client

5. **Add direct methods (if needed):**
   - Add method names to `<ModuleName>Constants.cs`
   - Register handlers in service:
     ```csharp
     await moduleClient.RegisterMethodHandlerAsync(
         YourModuleConstants.DirectMethodName,
         HandleMethodAsync,
         stoppingToken);
     ```

6. **Customize routing (if needed):**
   - Default route: Module → IoT Hub (`$upstream`)
   - For module-to-module: Update route to use `BrokeredEndpoint`
   - Edit in deployment manifest

7. **Build and deploy:**
   - Build module Docker image
   - Push to container registry
   - Deploy manifest to IoT Hub

**File paths for quick reference:**

- Module source: `<module_full_path>/`
- Constants: `<constants_full_path>`
- Deployment manifest(s): `<manifest_paths>`

## Reference Documentation

For detailed information, see reference files:

- `references/module-structure.md` - Complete module structure reference
- `references/deployment-manifests.md` - Deployment manifest reference

Load these when:

- User asks about module structure details
- User needs help with deployment manifest configuration
- Debugging scaffolding issues
- Understanding naming conventions

## Common Customizations

After scaffolding, users may want to:

**1. Add Quartz scheduler support:**

- Add NuGet package `Quartz`
- Register: `services.AddQuartz()`
- Create `Jobs/` folder with `IJob` implementations

**2. Add configuration options:**

- Create `Options/` folder
- Define option classes
- Register: `services.Configure<MyOptions>(hostContext.Configuration)`
- Set via env vars in deployment manifest

**3. Add module-to-module routing:**

- Update route in deployment manifest:
  ```json
  "route": "FROM /messages/modules/source/* INTO BrokeredEndpoint(\"/modules/target/inputs/input1\")"
  ```

**4. Add host binds (replace volume mounts):**

- Update deployment manifest `createOptions`:
  ```json
  "Binds": ["/host/path/:/container/path/"]
  ```

**5. Add privileged access (for device access like TPM):**

- Update deployment manifest `createOptions.HostConfig`:
  ```json
  "Privileged": true
  ```

**6. Remove volume mount (for stateless modules):**

- Delete `Mounts` section from deployment manifest

## Error Handling

**Module directory exists:**

- Prompt: "Overwrite/Rename/Cancel"
- If Overwrite: Delete existing directory first
- If Rename: Go back to Step 3 with new name

**Manifest update fails:**

- Show error from Python script
- Provide manual update instructions
- Continue with other manifests

**Detection fails:**

- Fall back to manual prompts for each value
- Offer to save configuration for future runs

**Missing Python:**

- If Python not available, provide manual instructions for all steps
- Skip automated manifest updates, provide JSON templates

## Advanced: Configuration File Format

Saved configuration (`.claude/.iot-edge-module-config.json`):

```json
{
  "config_source": "detected",
  "modules_base_path": "src/IoTEdgeModules/modules",
  "contracts_project_path": "src/Company.Modules.Contracts",
  "contracts_project_name": "Company.Modules.Contracts",
  "manifests_base_path": "src/IoTEdgeModules",
  "project_namespace": "Company.IoT.EdgeAPI",
  "container_registry": "myregistry.azurecr.io",
  "nuget_feed_url": null,
  "has_contracts_project": true,
  "has_nuget_feed": false
}
```

Users can manually edit this file to override auto-detection.

## Notes

- Module directory names: lowercase with "module" suffix (e.g., `dataprocessormodule`)
- C# class names: PascalCase with "Module" suffix (e.g., `DataProcessorModule`)
- Namespaces: PascalCase, no "module" suffix (e.g., `namespace DataProcessorModule;`)
- All modules use non-root user (moduleuser, UID 2000) for security
- Build context is repo root (`contextPath: "../../../"`)
- Log rotation: 10MB max size, 10 files
- Default route: Module outputs → `$upstream` (IoT Hub)
