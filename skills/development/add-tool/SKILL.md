---
name: add-tool
description: Investigate a tool from a GitHub issue and add it to the opt-out flake
---

# Add tool

Investigate the tool described in GitHub issue $ARGUMENTS and determine whether it qualifies for the opt-out flake.

1. **Read the GitHub issue** using `gh issue view` to get the tool name and any linked documentation.

2. **Research the tool** by visiting its official documentation and source repository. Look specifically for environment variables that disable telemetry, analytics, or crash reporting.

3. **Verify eligibility.** Only environment variable opt-outs qualify. The following do NOT qualify:
   - Update check suppression (e.g., `DENO_NO_UPDATE_CHECK`)
   - CLI-command-based opt-out (e.g., `flutter --disable-analytics`)
   - Settings-file-based opt-out

4. **Check for duplicates.** Verify the tool does not already exist in `tools/` (including `_`-prefixed excluded files).

5. **Create the tool file:**

   **If a valid env var opt-out exists**, create `tools/<toolname>.nix`:

   ```nix
   {
     name = "<toolname>";
     meta = {
       description = "<description of the tool itself — do not reference other tools>";
       homepage = "<link to the tool's git repository>";
       documentation = "<link to the specific documentation page proving the env var opt-out>";
       lastChecked = "YYYY-MM-DD";
       hasTelemetry = true;
     };
     variables = {
       ENV_VAR_NAME = "value";
     };
     commands = { };
   }
   ```

   If the tool also has CLI commands for telemetry (e.g., to check status or disable), add them:

   ```nix
     commands = {
       disable = "tool --disable-analytics";
       status = "tool analytics status";
     };
   ```

   **If NO valid env var opt-out exists**, create `tools/_<toolname>.nix` (do **not** add comments explaining why the tool is excluded — the metadata fields are self-documenting):

   ```nix
   {
     name = "<toolname>";
     meta = {
       description = "<description of the tool itself — do not reference other tools>";
       homepage = "<link to the tool's git repository>";
       documentation = "<link to relevant documentation>";
       lastChecked = "YYYY-MM-DD";
       hasTelemetry = true;
     };
     variables = { };
     commands = { };
     config = { };
   }
   ```

   If the tool has a config-file-based opt-out, populate the `config` map with the file path as key and key/value settings as the value:

   ```nix
     config = {
       "~/.toolname/config.toml" = {
         "telemetry.enabled" = "false";
       };
     };
   ```

   Set `hasTelemetry = false;` only if the tool was investigated and confirmed to have no telemetry at all.

6. **Metadata rules:**
   - The `description` must describe only the tool being added. Do not mention other tools, frameworks, or ecosystems.
   - The `homepage` must link to the tool's own repository.
   - The `documentation` must link to the tool's own documentation page that covers telemetry/analytics opt-out. Prefer official website docs over source code links — only link to source code if no public documentation exists.
   - Set `lastChecked` to today's date in `YYYY-MM-DD` format.
   - Set `hasTelemetry` to `true` for tools with telemetry (even excluded ones that only have CLI opt-out). Set to `false` only if the tool was investigated and confirmed to have no telemetry.

7. **Stage, format, and validate:**

   ```bash
   git add tools/<filename>.nix
   mise run fmt
   mise run lint
   mise run flake-check
   ```

8. **Update README if the tool was added (not `_`-prefixed):**

   ```bash
   mise run readme-vars
   git add README.md
   ```

9. **Commit, push, and create a PR:**
   - Create a branch named `add-tool/<toolname>`
   - Commit with a clear message describing the addition
   - Push and create a PR using `gh pr create`
   - **Assign the PR to `@adampie`**
   - **Link to the GitHub issue in the PR body** with `Closes #<number>`
