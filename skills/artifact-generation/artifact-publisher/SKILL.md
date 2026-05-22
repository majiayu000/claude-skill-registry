---
name: artifact-publisher
version: 1.0.0
description: Publish and share Claude Artifacts with Projects, Cursor, and downstream agents. Use when a user wants to "save", "share", or "finalize" a generated artifact.
allowed-tools: create_artifact, share_artifact, publish_artifact
publish_policy: manual # Options: manual, auto-on-pass, auto-on-complete
retry_config:
  max_attempts: 3
  backoff_strategy: exponential
  initial_delay_ms: 1000
  max_delay_ms: 8000
validation_required: true # Only publish artifacts with validation_status: 'pass' unless override
---

<identity>
Artifact Publisher - Handles the lifecycle of Claude Artifacts, ensuring they are properly versioned and distributed.

**Platform Support**: This skill works across all platforms (Claude, Cursor, Factory, OpenCode) with platform-specific invocation methods but consistent metadata structure.
</identity>

<capabilities>
- Publishing and sharing Claude Artifacts with Projects, Cursor, and downstream agents
- Saving, sharing, or finalizing generated artifacts
- Versioning artifacts
- Distributing artifacts to external integrations
</capabilities>

<instructions>
<execution_process>
1. **Check Registry**: If artifact is registered, check registry metadata for:
   - Use `readArtifactRegistry(runId)` from `.claude/tools/run-manager.mjs` to load registry
   - Check `publishable: true` - Should this artifact be published?
   - Check `publish_targets` - Where to publish (e.g., `["project_feed", "cursor"]`)
   - Extract `workflow_id` and `step_number` from registry metadata
   
2. **Creation**: Use `create_artifact` to finalize a code block or document into a persistent artifact.
   - Include metadata: `workflow_id`, `step_number`, `dependencies` from registry
   - Add validation status from gate file if available
   
3. **Distribution**: Use `share_artifact` to push the artifact to the Claude Project feed or external integrations.
   - Publish to targets specified in registry metadata or default to `["project_feed"]`
   
4. **Publishing**: Use `publish_artifact` to formally publish an artifact, updating its `published` status and `published_at` timestamp in the artifact registry.
   - This is the formal publishing step that marks an artifact as published
   - Updates registry metadata with publishing status
   
5. **Update Registry**: After publishing (success or failure):
   - Use `updateArtifactPublishingStatus(runId, artifactName, status)` from `.claude/tools/run-manager.mjs`
   - Update `published: true/false` in registry metadata
   - Set `published_at` timestamp on success
   - Update `publish_status`: 'success' or 'failed'
   - Record `publish_error` if publication failed
   - Add to `publish_attempts` array for retry tracking
   - Example call:
     ```javascript
     await updateArtifactPublishingStatus(runId, artifactName, {
       published: true,
       published_at: new Date().toISOString(),
       publish_status: 'success',
       attempt: {
         timestamp: new Date().toISOString(),
         status: 'success',
         target: 'project_feed'
       }
     });
     ```
   
6. **Error Handling & Retry**:
   - **Retry Logic**: If publication fails, retry up to `max_attempts` (default: 3) with exponential backoff
   - **Backoff Strategy**: Use delays from `retry_config`: initial_delay_ms (1000ms), then 2x, 4x, up to max_delay_ms (8000ms)
   - **Status Tracking**: Track each attempt in `publish_attempts` array with timestamp and error using `updateArtifactPublishingStatus()`
   - **Validation Check**: Only publish artifacts with `validation_status: 'pass'` unless `validation_required: false` override
   - **Notifications**: Log publishing success/failure; include in gate file if available
   - **Fallback**: If all retries fail, mark as `publish_status: 'failed'` and log error for manual intervention
   - **Retry Implementation**:
     ```javascript
     async function publishWithRetry(artifact, runId, maxRetries = 3) {
       const delays = [1000, 2000, 4000]; // From retry_config
       for (let attempt = 0; attempt < maxRetries; attempt++) {
         try {
           await publishArtifact(artifact);
           await updateArtifactPublishingStatus(runId, artifact.name, {
             status: 'success',
             published: true,
             published_at: new Date().toISOString(),
             attempt: { timestamp: new Date().toISOString(), status: 'success' }
           });
           return;
         } catch (error) {
           await updateArtifactPublishingStatus(runId, artifact.name, {
             status: attempt === maxRetries - 1 ? 'failed' : 'pending',
             publish_error: error.message,
             attempt: { timestamp: new Date().toISOString(), status: 'failed', error: error.message }
           });
           if (attempt < maxRetries - 1) {
             await new Promise(resolve => setTimeout(resolve, delays[attempt]));
           }
         }
       }
       throw new Error(`Publishing failed after ${maxRetries} attempts`);
     }
     ```
</execution_process>

<error_handling>
**Publishing Failures**:

1. **Transient Errors** (network, rate limits):
   - Retry with exponential backoff: 1s, 2s, 4s
   - Maximum 3 retries
   - Log each attempt in registry metadata

2. **Permanent Errors** (invalid artifact, permission denied):
   - Fail immediately (no retry)
   - Log error in registry: `publish_error`
   - Set `publish_status: 'failed'`
   - Include error details in gate file if available

3. **Status Tracking**:

   ```javascript
   metadata: {
     publish_attempts: [
       { timestamp: "2025-11-29T10:00:00Z", status: "failed", error: "Network timeout" },
       { timestamp: "2025-11-29T10:00:01Z", status: "success" }
     ],
     publish_status: "success" | "failed" | "pending",
     publish_error: null | "Error message"
   }
   ```

4. **Notifications**:
   - Log success: "✅ Artifact published successfully to project_feed"
   - Log failure: "❌ Artifact publishing failed after 3 retries: [error]"
   - Include in gate file validation results if available
     </error_handling>

<workflow_integration>

- **Post-Tool Trigger**: This skill is often invoked automatically after a `PostToolUse` hook to snapshot the results of a tool execution.
- **Factory Droid**: Published artifacts are the primary way Factory Droids consume instructions from Claude.
- **Publishing Policy**: The `publish_policy` in the frontmatter dictates when artifacts are automatically published:
  - `manual`: Requires explicit `publish_artifact` call.
  - `auto-on-pass`: Automatically publishes if the artifact's validation status is 'pass'.
  - `auto-on-complete`: Automatically publishes upon workflow completion.
- **Artifact Registry Integration**:
  - Use `readArtifactRegistry(runId)` from `.claude/tools/run-manager.mjs` to check registry
  - Check artifact registry for `publishable: true` metadata to auto-publish
  - Use `updateArtifactPublishingStatus(runId, artifactName, status)` to update registry after publication
  - Read `workflow_id` and `step_number` from registry metadata
  - Track publishing attempts and errors in registry via `publish_attempts` array
  - **Migration Note**: Prefer run-manager.mjs over artifact-registry.mjs (deprecated)

**Publishing Policy Examples**:

1. **Manual Publishing** (`publish_policy: manual`):

   ```yaml
   # In workflow YAML or skill frontmatter
   publish_policy: manual
   ```

   - Artifacts are only published when explicitly requested
   - Use: "Publish this artifact" or `publish_artifact` tool call
   - Example: User reviews artifact, then explicitly publishes it

2. **Auto-on-Pass** (`publish_policy: auto-on-pass`):

   ```yaml
   # In workflow YAML or skill frontmatter
   publish_policy: auto-on-pass
   ```

   - Artifacts are automatically published when validation status is 'pass'
   - Use: When you want to publish all validated artifacts automatically
   - Example: After gate file validation passes, artifact is automatically published
   - Implementation:

   ```javascript
   // After gate validation passes
   if (artifact.validationStatus === 'pass' && publishPolicy === 'auto-on-pass') {
     await publishArtifact(artifact);
     await updateArtifactPublishingStatus(runId, artifact.name, {
       published: true,
       published_at: new Date().toISOString(),
       publish_status: 'success',
     });
   }
   ```

3. **Auto-on-Complete** (`publish_policy: auto-on-complete`):

   ```yaml
   # In workflow YAML or skill frontmatter
   publish_policy: auto-on-complete
   ```

   - Artifacts are automatically published when workflow completes
   - Use: When you want to publish all artifacts at workflow end
   - Example: At workflow completion, all artifacts with `publishable: true` are published
   - Implementation:

   ```javascript
   // At workflow completion
   if (workflowStatus === 'completed' && publishPolicy === 'auto-on-complete') {
     const registry = await readArtifactRegistry(runId);
     for (const [name, artifact] of Object.entries(registry.artifacts)) {
       if (artifact.publishable && !artifact.published) {
         await publishArtifact(artifact);
         await updateArtifactPublishingStatus(runId, name, {
           published: true,
           published_at: new Date().toISOString(),
           publish_status: 'success',
         });
       }
     }
   }
   ```

**Configuring Publish Targets Per Artifact**:

```javascript
// When registering artifact
await registerArtifact(runId, {
  name: 'plan-123.json',
  step: 0,
  agent: 'planner',
  publishable: true,
  publish_targets: ['project_feed', 'cursor'], // Multiple targets
  // ... other fields
});
```

**Handling Publishing Failures in Workflows**:

- If publishing fails, workflow continues (non-blocking)
- Publishing errors are logged in registry: `publish_error`
- Failed artifacts can be retried manually or in next workflow run
- Gate files include publishing status for visibility
  </workflow_integration>
  </instructions>

<platform_invocation>
**Claude (this platform)**:

- Use `create_artifact` and `share_artifact` tools directly
- Invoke: "Use artifact-publisher skill to publish this artifact"

**Cursor**:

- Use `@artifact-publisher` mention
- Invoke: "Use @artifact-publisher to publish this plan"

**Factory**:

- Use Task tool with skill
- Invoke: "Run Task tool with skill artifact-publisher to publish this spec"

**OpenCode**:

- Use file system operations
- Invoke: "Publish artifact to .opencode/context/artifacts/published/"

**Cross-Platform Metadata**:
All platforms should use consistent metadata structure:

```json
{
  "id": "artifact-{timestamp}-{sequence}",
  "type": "plan|architecture|specification|implementation|test-results",
  "title": "Artifact Title",
  "created": "ISO 8601 timestamp",
  "workflow_id": "workflow-id",
  "step_number": 0,
  "agent": "agent-name",
  "dependencies": ["artifact1.json", "artifact2.json"],
  "validation_status": "pass|fail|pending",
  "tags": ["tag1", "tag2"],
  "publish_targets": ["project_feed", "cursor"],
  "published": true,
  "published_at": "ISO 8601 timestamp"
}
```

</platform_invocation>

<examples>
<usage_example>
**Publishing a Design Doc (Claude)**:

```
create_artifact --title "System Architecture" --type "markdown" --content "..."
share_artifact --id <artifact_id> --target "project_feed"
```

</usage_example>

<usage_example>
**Publishing a Plan (Cursor)**:

```
Use @artifact-publisher to publish this plan
```

</usage_example>

<usage_example>
**Publishing a Spec (Factory)**:

```
Run Task tool with skill artifact-publisher to publish this spec
```

</usage_example>
</examples>
