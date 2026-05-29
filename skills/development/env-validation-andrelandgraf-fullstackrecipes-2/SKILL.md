---
name: env-validation
description: Validate environment variables on server start and before builds. Catch missing or invalid variables early with clear error messages.
---

# Build-Time Environment Variable Validation

Validate environment variables on server start and before builds. Catch missing or invalid variables early with clear error messages.

## Implement Environment Validation

Validate environment variables on server start and before builds. Catch missing or invalid variables early with clear error messages.

**See:**

- Resource: `env-validation` in Fullstack Recipes
- URL: https://fullstackrecipes.com/recipes/env-validation

---

### Validating Configs on Server Start

Some environment variables are read internally by packages rather than passed as arguments. To catch missing variables early instead of at runtime, import your configs in `instrumentation.ts`:

```typescript
// src/instrumentation.ts
import * as Sentry from "@sentry/nextjs";
import { sentryConfig } from "./lib/sentry/config";

// Validate required configs on server start
import "./lib/ai/config";
import "./lib/db/config";

export async function register() {
  // ... initialization code
}
```

The side-effect imports trigger `configSchema` validation immediately when the server starts. If any required environment variable is missing, the server fails to start with a clear error rather than failing later when the code path is executed.

---

### Validating Environment Files Pre-Build

**Install via shadcn registry:**

```bash
bunx --bun shadcn@latest add https://fullstackrecipes.com/r/validate-env.json
```

**Or copy the source code:**

`scripts/validate-env.ts`:

```typescript
#!/usr/bin/env bun
/**
 * Validate environment configuration
 *
 * Usage:
 *   bun run validate-env
 *   bun run validate-env --environment=development
 *   bun run validate-env --environment=production
 *
 * This script:
 * 1. Loads env files using Next.js's loadEnvConfig
 * 2. Finds all config.ts files in src/lib/\*\/
 * 3. Validates each config by importing it (triggers configSchema validation)
 * 4. Warns about env variables in .env files that aren't used by any config
 */

import { loadEnvConfig } from "@next/env";
import { Glob } from "bun";
import path from "path";

// ANSI colors
const green = (s: string) => `\x1b[32m${s}\x1b[0m`;
const yellow = (s: string) => `\x1b[33m${s}\x1b[0m`;
const red = (s: string) => `\x1b[31m${s}\x1b[0m`;
const dim = (s: string) => `\x1b[2m${s}\x1b[0m`;
const bold = (s: string) => `\x1b[1m${s}\x1b[0m`;

// Parse CLI args
function parseArgs(): { environment?: string } {
  const args = process.argv.slice(2);
  const result: { environment?: string } = {};

  for (const arg of args) {
    if (arg.startsWith("--environment=")) {
      result.environment = arg.split("=")[1];
    }
  }

  return result;
}

// Track which env vars are referenced by configs
const referencedEnvVars = new Set<string>();

// Patch process.env to track access
function trackEnvAccess() {
  const originalEnv = process.env;
  const handler: ProxyHandler<NodeJS.ProcessEnv> = {
    get(target, prop) {
      if (typeof prop === "string" && !prop.startsWith("_")) {
        referencedEnvVars.add(prop);
      }
      return Reflect.get(target, prop);
    },
  };
  process.env = new Proxy(originalEnv, handler);
}

async function main() {
  const args = parseArgs();
  const projectDir = process.cwd();

  console.log(bold("\n🔍 Environment Configuration Validator\n"));

  // Set NODE_ENV if environment specified
  const environment = args.environment ?? process.env.NODE_ENV ?? "development";
  (process.env as Record<string, string>).NODE_ENV = environment;
  console.log(dim(`  Environment: ${environment}\n`));

  // Load env files
  // Second param `dev` tells loadEnvConfig to load .env.development files
  const isDev = environment === "development";
  console.log(dim("  Loading environment files..."));

  const loadedEnvFiles: string[] = [];
  const { combinedEnv, loadedEnvFiles: files } = loadEnvConfig(
    projectDir,
    isDev,
  );

  for (const file of files) {
    loadedEnvFiles.push(file.path);
    console.log(dim(`    ✓ ${path.relative(projectDir, file.path)}`));
  }

  if (loadedEnvFiles.length === 0) {
    console.log(dim("    No .env files found"));
  }

  console.log("");

  // Start tracking env access before importing configs
  trackEnvAccess();

  // Find all config.ts files
  const configGlob = new Glob("src/lib/*/config.ts");
  const configFiles: string[] = [];

  for await (const file of configGlob.scan(projectDir)) {
    configFiles.push(file);
  }

  if (configFiles.length === 0) {
    console.log(yellow("  ⚠ No config.ts files found in src/lib/*/\n"));
    process.exit(0);
  }

  console.log(dim(`  Found ${configFiles.length} config files:\n`));

  // Validate each config
  const errors: { file: string; error: Error }[] = [];
  const validated: string[] = [];

  for (const configFile of configFiles) {
    const relativePath = configFile;
    const absolutePath = path.join(projectDir, configFile);

    try {
      // Import the config module - this triggers validation
      await import(absolutePath);
      console.log(green(`  ✓ ${relativePath}`));
      validated.push(relativePath);
    } catch (error) {
      if (error instanceof Error) {
        // Check if it's a disabled feature flag (not an error)
        if (error.message.includes("isEnabled: false")) {
          console.log(dim(`  ○ ${relativePath} (feature disabled)`));
          validated.push(relativePath);
        } else {
          console.log(red(`  ✗ ${relativePath}`));
          errors.push({ file: relativePath, error });
        }
      }
    }
  }

  console.log("");

  // Report validation errors
  if (errors.length > 0) {
    console.log(red(bold("Validation Errors:\n")));

    for (const { file, error } of errors) {
      console.log(red(`  ${file}:`));
      // Extract the actual error message
      const message = error.message.split("\n").slice(0, 3).join("\n    ");
      console.log(red(`    ${message}\n`));
    }
  }

  // Find unused env variables (in .env files but not referenced by configs)
  const envVarsInFiles = new Set<string>();

  // Parse loaded env files to get all defined variables
  for (const envFile of loadedEnvFiles) {
    try {
      const content = await Bun.file(envFile).text();
      const lines = content.split("\n");

      for (const line of lines) {
        const trimmed = line.trim();
        // Skip comments and empty lines
        if (!trimmed || trimmed.startsWith("#")) continue;

        // Extract variable name (before = sign)
        const match = trimmed.match(/^([A-Z_][A-Z0-9_]*)\s*=/);
        if (match) {
          envVarsInFiles.add(match[1]);
        }
      }
    } catch {
      // Ignore file read errors
    }
  }

  // Common system/framework vars to ignore
  const ignoredVars = new Set([
    // System
    "NODE_ENV",
    "PATH",
    "HOME",
    "USER",
    "SHELL",
    "TERM",
    "LANG",
    "PWD",
    "OLDPWD",
    "HOSTNAME",
    "LOGNAME",
    "TMPDIR",
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
    "XDG_CACHE_HOME",
    "CI",
    "TZ",
    // Vercel
    "VERCEL",
    "VERCEL_ENV",
    "VERCEL_URL",
    "VERCEL_REGION",
    "VERCEL_TARGET_ENV",
    "VERCEL_GIT_COMMIT_SHA",
    "VERCEL_GIT_COMMIT_MESSAGE",
    "VERCEL_GIT_COMMIT_AUTHOR_LOGIN",
    "VERCEL_GIT_COMMIT_AUTHOR_NAME",
    "VERCEL_GIT_PREVIOUS_SHA",
    "VERCEL_GIT_PROVIDER",
    "VERCEL_GIT_REPO_ID",
    "VERCEL_GIT_REPO_OWNER",
    "VERCEL_GIT_REPO_SLUG",
    "VERCEL_GIT_COMMIT_REF",
    "VERCEL_GIT_PULL_REQUEST_ID",
    // Build tools (Turbo, NX)
    "TURBO_CACHE",
    "TURBO_REMOTE_ONLY",
    "TURBO_RUN_SUMMARY",
    "TURBO_DOWNLOAD_LOCAL_ENABLED",
    "NX_DAEMON",
  ]);

  // Find vars in .env files but not referenced by configs
  const unusedVars: { name: string; files: string[] }[] = [];

  for (const envVar of envVarsInFiles) {
    if (ignoredVars.has(envVar)) continue;
    if (referencedEnvVars.has(envVar)) continue;

    // Find which files define this var
    const definingFiles: string[] = [];
    for (const envFile of loadedEnvFiles) {
      try {
        const content = await Bun.file(envFile).text();
        if (new RegExp(`^${envVar}\\s*=`, "m").test(content)) {
          definingFiles.push(path.relative(projectDir, envFile));
        }
      } catch {
        // Ignore
      }
    }

    if (definingFiles.length > 0) {
      unusedVars.push({ name: envVar, files: definingFiles });
    }
  }

  // Report unused vars
  if (unusedVars.length > 0) {
    console.log(yellow(bold("Unused Environment Variables:\n")));
    console.log(
      dim(
        "  These variables are defined in .env files but not used by any config:\n",
      ),
    );

    for (const { name, files } of unusedVars.sort((a, b) =>
      a.name.localeCompare(b.name),
    )) {
      console.log(yellow(`  ⚠ ${name}`));
      console.log(dim(`    defined in: ${files.join(", ")}`));
    }

    console.log("");
  }

  // Summary
  console.log(bold("Summary:\n"));
  console.log(`  Configs validated: ${green(String(validated.length))}`);
  console.log(
    `  Validation errors: ${errors.length > 0 ? red(String(errors.length)) : green("0")}`,
  );
  console.log(
    `  Unused env vars:   ${unusedVars.length > 0 ? yellow(String(unusedVars.length)) : green("0")}`,
  );
  console.log("");

  // Exit with error code if validation failed
  if (errors.length > 0) {
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(red("Unexpected error:"), error);
  process.exit(1);
});
```

Add the validation script to your `package.json`:

```json
{
  "scripts": {
    "prebuild": "bun run env:validate:prod",
    "env:validate": "bun run scripts/validate-env.ts --environment=development",
    "env:validate:prod": "bun run scripts/validate-env.ts --environment=production"
  }
}
```

Use the `env:validate` and `env:validate:prod` scripts to validate all your configs (`config.ts` files in `src/lib/*/`) against your `.env` files.

The `prebuild` script (configured above) runs automatically before `build`, ensuring environment variables are validated before every build (locally and in CI/Vercel). If validation fails, the build stops early with a clear error.

The script:

1. Loads `.env` files using Next.js's `loadEnvConfig` (respects the same load order as Next.js)
2. Finds all `config.ts` files in `src/lib/*/`
3. Imports each config to trigger `configSchema` validation
4. Reports any missing or invalid environment variables
5. Warns about variables defined in `.env` files but not used by any config

Example output with a validation error:

```
🔍 Environment Configuration Validator

  Environment: development

  Loading environment files...
    ✓ .env.local
    ✓ .env.development

  Found 5 config files:

  ✗ src/lib/resend/config.ts
  ✓ src/lib/sentry/config.ts
  ✓ src/lib/db/config.ts
  ✓ src/lib/ai/config.ts
  ✓ src/lib/auth/config.ts

Validation Errors:

  src/lib/resend/config.ts:
    Configuration validation error for Resend!
    Did you correctly set all required environment variables in your .env* file?
     - server.fromEmail (FROM_EMAIL) must be defined.

Summary:

  Configs validated: 4
  Validation errors: 1
  Unused env vars:   0
```

Example output with an unused variable:

```
🔍 Environment Configuration Validator

  Environment: development

  Loading environment files...
    ✓ .env.local
    ✓ .env.development

  Found 5 config files:

  ✓ src/lib/resend/config.ts
  ✓ src/lib/sentry/config.ts
  ✓ src/lib/db/config.ts
  ✓ src/lib/ai/config.ts
  ✓ src/lib/auth/config.ts

Unused Environment Variables:

  These variables are defined in .env files but not used by any config:

  ⚠ OLD_API_KEY
    defined in: .env.local

Summary:

  Configs validated: 5
  Validation errors: 0
  Unused env vars:   1
```

The script exits with code 1 if any validation errors occur (useful for CI), but unused variables only trigger warnings without failing the build.
