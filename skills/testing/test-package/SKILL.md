---
name: test-package
description: Run grok test for one or more Datagrok packages against a server host and report results
argument-hint: <PackageName(s)> [--host host] [--category cat] [--test name] [--verbose] [--skip-build] [--no-retry]
---

# Test Package

Run `grok test` for one or more Datagrok packages and provide a summary of results.

## Instructions

1. Parse the user's input to extract:
   - One or more package names (required). These are directory names under `public/packages/`.
   - `--host` value (default: `localhost`)
   - Use `--csv` flag to get csv output 
   - Check if npm install is needed
   - Check if package needs to be rebuilt. Compare /dist/*.js timestamp with the most recent timestamp in *.ts or *.js file in the package. If dist folder is newer, use --skip-build
   - Any extra `grok test` flags (`--category`, `--test`, `--verbose`, `--skip-build`, `--gui`, `--no-retry`, `--benchmark`, `--tag`)

2. For each package, run tests from the package directory using the Bash tool:
   ```
   cd /c/Repos/Datagrok/public/packages/<PackageName> && node grok test --host <host> --no-retry [extra flags]
   ```
   Use a timeout of 600000ms (10 minutes). Print output to console.

3. After all packages finish, provide a **summary table** with:
   - Package name
   - Total passed / failed / skipped counts (parse csv output file test-results.csv)
   - List of any failed categories and test names
   - Overall verdict: PASSED or FAILED

4. Cleanup csv output file