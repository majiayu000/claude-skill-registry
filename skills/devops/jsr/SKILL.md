---
name: jsr
description: jsr release workflow for Deno projects. Use when publishing or releasing packages to JSR (JavaScript Registry) using Deno.
---

## Add `deno task release`

```ts
// scripts/release.ts
const denoJsonPath = new URL("../deno.json", import.meta.url);
const denoJson = JSON.parse(Deno.readTextFileSync(denoJsonPath));
const currentVersion = denoJson.version;

let newVersion = Deno.args[0];

if (!newVersion) {
  console.log(`Current version: ${currentVersion}`);
  const input = prompt("Enter new version:");
  if (!input) {
    console.error("Version is required");
    Deno.exit(1);
  }
  newVersion = input;
}

if (newVersion.startsWith("v")) {
  newVersion = newVersion.substring(1);
}

// Update deno.json
denoJson.version = newVersion;
Deno.writeTextFileSync(
  denoJsonPath,
  JSON.stringify(denoJson, null, 2) + "\n",
);
console.log(`Updated deno.json version to ${newVersion}`);

// Run git commands
async function run(cmd: string[]) {
  console.log(`> ${cmd.join(" ")}`);
  const command = new Deno.Command(cmd[0], {
    args: cmd.slice(1),
    stdout: "inherit",
    stderr: "inherit",
  });
  const { code } = await command.output();
  if (code !== 0) {
    console.error(`Command failed with code ${code}`);
    Deno.exit(code);
  }
}

await run(["git", "add", "deno.json"]);
await run(["git", "commit", "-m", `chore: bump version to ${newVersion}`]);

console.log(
  `\nSuccessfully bumped version to ${newVersion}. Please push to trigger release workflow.`,
);
```

## Add release workflow under `.github/workflows/ci.yml`

```yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Setup Deno
        uses: denoland/setup-deno@v2

      - run: deno lint
      - run: deno check
      - run: deno test -P
      - run: deno fmt --check

  release:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Check version
        id: check
        run: |
          VERSION="v$(jq -r .version deno.json)"
          echo "Version: $VERSION"
          git fetch --tags
          if git rev-parse "$VERSION" >/dev/null 2>&1; then
            echo "Tag $VERSION already exists."
            echo "exists=true" >> "$GITHUB_OUTPUT"
          else
            echo "Tag $VERSION not found."
            echo "exists=false" >> "$GITHUB_OUTPUT"
            echo "version=$VERSION" >> "$GITHUB_OUTPUT"
          fi

      - name: Setup Deno
        if: steps.check.outputs.exists == 'false'
        uses: denoland/setup-deno@v2

      - name: Create Tag and Publish
        if: steps.check.outputs.exists == 'false'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          VERSION="${{ steps.check.outputs.version }}"

          git tag "$VERSION"
          git push origin "$VERSION"
          deno publish
```
