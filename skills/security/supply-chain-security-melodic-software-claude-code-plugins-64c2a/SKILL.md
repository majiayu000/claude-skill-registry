---
name: supply-chain-security
description: Software supply chain security guidance covering SBOM generation, SLSA framework, dependency scanning, SCA tools, and protection against supply chain attacks like dependency confusion and typosquatting.
allowed-tools: Read, Glob, Grep, Task
---

# Supply Chain Security

Comprehensive guidance for securing the software supply chain, including dependency management, SBOM generation, vulnerability scanning, and protection against supply chain attacks.

## When to Use This Skill

- Generating Software Bill of Materials (SBOM)
- Implementing SLSA framework compliance
- Setting up dependency vulnerability scanning
- Protecting against dependency confusion attacks
- Configuring lock files and integrity verification
- Implementing code signing with Sigstore
- Verifying software provenance
- Evaluating project security with OpenSSF Scorecard

## Quick Reference

### Supply Chain Attack Types

| Attack Type | Description | Prevention |
|-------------|-------------|------------|
| **Dependency Confusion** | Attacker publishes malicious package with internal package name | Namespace scoping, private registries |
| **Typosquatting** | Malicious packages with similar names (`lodash` vs `1odash`) | Lockfiles, careful review, tools |
| **Compromised Maintainer** | Legitimate package hijacked | Pin versions, verify signatures |
| **Build System Attack** | CI/CD pipeline compromised | SLSA compliance, hermetic builds |
| **Malicious Dependency** | New dependency contains malware | SCA scanning, SBOM review |

### SLSA Levels Quick Reference

| Level | Requirements | Protection |
|-------|--------------|------------|
| **SLSA 1** | Documentation of build process | Basic transparency |
| **SLSA 2** | Authenticated provenance, hosted build | Tampering after build |
| **SLSA 3** | Hardened build platform, non-falsifiable provenance | Tampering during build |
| **SLSA 4** | Two-person review, hermetic builds | Insider threats |

### Essential Tools by Ecosystem

| Ecosystem | Vulnerability Scanning | Lock File | SBOM Generation |
|-----------|----------------------|-----------|-----------------|
| **npm/Node.js** | `npm audit`, Snyk | `package-lock.json` | `@cyclonedx/cyclonedx-npm` |
| **Python** | `pip-audit`, Safety | `requirements.txt` + hashes, `poetry.lock` | `cyclonedx-python` |
| **Go** | `govulncheck`, Snyk | `go.sum` | `cyclonedx-gomod` |
| **.NET** | `dotnet list package --vulnerable` | `packages.lock.json` | `CycloneDX` NuGet |
| **Java/Maven** | OWASP Dependency-Check | `pom.xml` with versions | `cyclonedx-maven-plugin` |
| **Rust** | `cargo audit` | `Cargo.lock` | `cargo-cyclonedx` |

## SBOM (Software Bill of Materials)

### SBOM Formats

| Format | Standard | Best For |
|--------|----------|----------|
| **CycloneDX** | OASIS | Security-focused, VEX support |
| **SPDX** | Linux Foundation | License compliance, legal |
| **SWID** | ISO/IEC 19770-2 | Software asset management |

### CycloneDX SBOM Generation

**Node.js:**

```bash
# Install CycloneDX CLI
npm install -g @cyclonedx/cyclonedx-npm

# Generate SBOM
cyclonedx-npm --output-file sbom.json
cyclonedx-npm --output-file sbom.xml --output-format xml
```

**Python:**

```bash
# Install CycloneDX
pip install cyclonedx-bom

# Generate from requirements.txt
cyclonedx-py requirements -i requirements.txt -o sbom.json --format json

# Generate from Poetry
cyclonedx-py poetry -o sbom.json --format json

# Generate from pip environment
cyclonedx-py environment -o sbom.json
```

**.NET:**

```bash
# Install CycloneDX tool
dotnet tool install --global CycloneDX

# Generate SBOM
dotnet CycloneDX myproject.csproj -o sbom.json -j
```

**Go:**

```bash
# Install cyclonedx-gomod
go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest

# Generate SBOM
cyclonedx-gomod mod -json -output sbom.json
```

### SBOM in CI/CD

```yaml
# GitHub Actions - Generate and upload SBOM
name: Generate SBOM
on:
  release:
    types: [published]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Generate SBOM
        uses: CycloneDX/gh-node-module-generatebom@v1
        with:
          output: sbom.json

      - name: Upload SBOM to release
        uses: actions/upload-release-asset@v1
        with:
          upload_url: ${{ github.event.release.upload_url }}
          asset_path: sbom.json
          asset_name: sbom.json
          asset_content_type: application/json

      - name: Submit to Dependency Track
        run: |
          curl -X POST \
            -H "X-Api-Key: ${{ secrets.DTRACK_API_KEY }}" \
            -H "Content-Type: multipart/form-data" \
            -F "project=${{ github.repository }}" \
            -F "bom=@sbom.json" \
            "${{ secrets.DTRACK_URL }}/api/v1/bom"
```

## Vulnerability Scanning

### npm/Node.js

```bash
# Built-in audit
npm audit
npm audit --json > audit-results.json
npm audit fix  # Auto-fix where possible

# Check for outdated packages
npm outdated

# Use better-npm-audit for CI
npx better-npm-audit audit --level moderate
```

### Python

```bash
# pip-audit (recommended)
pip install pip-audit
pip-audit
pip-audit --fix  # Auto-fix
pip-audit -r requirements.txt
pip-audit --format json > audit.json

# Safety (alternative)
pip install safety
safety check
safety check -r requirements.txt
```

### .NET

```bash
# Built-in vulnerability check
dotnet list package --vulnerable
dotnet list package --vulnerable --include-transitive

# Output as JSON for CI
dotnet list package --vulnerable --format json > vulnerabilities.json
```

### Go

```bash
# govulncheck (official Go tool)
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...
govulncheck -json ./... > vuln.json
```

### Rust

```bash
# cargo-audit
cargo install cargo-audit
cargo audit
cargo audit --json > audit.json
cargo audit fix  # Auto-fix (with cargo-audit-fix)
```

## Lock Files and Integrity

### Lock File Best Practices

```csharp
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.Json.Serialization;

/// <summary>
/// Lock file verification utilities for supply chain security.
/// </summary>
public static class LockFileVerification
{
    /// <summary>
    /// Verify npm package-lock.json integrity hashes.
    /// </summary>
    public static Dictionary<string, PackageIntegrityResult> VerifyNpmIntegrity(string packageLockPath)
    {
        var json = File.ReadAllText(packageLockPath);
        var lockData = JsonSerializer.Deserialize<NpmPackageLock>(json)!;

        var results = new Dictionary<string, PackageIntegrityResult>();

        foreach (var (name, info) in lockData.Packages ?? new())
        {
            if (string.IsNullOrEmpty(name)) continue;  // Root package

            if (!string.IsNullOrEmpty(info.Integrity))
            {
                var parts = info.Integrity.Split('-', 2);
                results[name] = new PackageIntegrityResult(
                    HasIntegrity: true,
                    Algorithm: parts[0]);
            }
            else
            {
                results[name] = new PackageIntegrityResult(HasIntegrity: false, Algorithm: null);
            }
        }

        return results;
    }

    /// <summary>
    /// Verify NuGet packages.lock.json integrity.
    /// </summary>
    public static Dictionary<string, PackageIntegrityResult> VerifyNuGetLockFile(string lockFilePath)
    {
        var json = File.ReadAllText(lockFilePath);
        var lockData = JsonSerializer.Deserialize<NuGetPackagesLock>(json)!;

        var results = new Dictionary<string, PackageIntegrityResult>();

        foreach (var (framework, dependencies) in lockData.Dependencies ?? new())
        {
            foreach (var (packageName, info) in dependencies)
            {
                var key = $"{packageName}@{info.Resolved}";
                results[key] = new PackageIntegrityResult(
                    HasIntegrity: !string.IsNullOrEmpty(info.ContentHash),
                    Algorithm: !string.IsNullOrEmpty(info.ContentHash) ? "SHA512" : null);
            }
        }

        return results;
    }
}

public sealed record PackageIntegrityResult(bool HasIntegrity, string? Algorithm);

public sealed record NpmPackageLock(
    [property: JsonPropertyName("packages")] Dictionary<string, NpmPackageInfo>? Packages);

public sealed record NpmPackageInfo(
    [property: JsonPropertyName("integrity")] string? Integrity);

public sealed record NuGetPackagesLock(
    [property: JsonPropertyName("dependencies")] Dictionary<string, Dictionary<string, NuGetDependencyInfo>>? Dependencies);

public sealed record NuGetDependencyInfo(
    [property: JsonPropertyName("resolved")] string? Resolved,
    [property: JsonPropertyName("contentHash")] string? ContentHash);
```

### pip with Hash Verification

```text
# requirements.txt with hashes (most secure)
requests==2.31.0 \
    --hash=sha256:58cd2187c01e70e6e26505bca751777aa9f2ee0b7f4300988b709f44e013003f \
    --hash=sha256:942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1

certifi==2024.2.2 \
    --hash=sha256:dc383c07b76109f368f6106eee2b593b04a011ea4d55f652c6ca24a754d1cdd1 \
    --hash=sha256:922820b53db7a7257ffbda3f597266d435245903d80737e34f8a45ff3e3230d8
```

### Generate Hashes Automatically

```bash
# pip-tools for hash generation
pip install pip-tools

# Generate requirements with hashes
pip-compile --generate-hashes requirements.in -o requirements.txt

# Poetry with hash export
poetry export --format requirements.txt --with-hashes > requirements.txt
```

## Dependency Confusion Prevention

### Private Registry Configuration

**npm (.npmrc):**

```ini
# Scope packages to private registry
@mycompany:registry=https://npm.mycompany.com/
//npm.mycompany.com/:_authToken=${NPM_TOKEN}

# Always use exact versions
save-exact=true
```

**Python (pip.conf):**

```ini
[global]
index-url = https://pypi.mycompany.com/simple/
extra-index-url = https://pypi.org/simple/
trusted-host = pypi.mycompany.com

[install]
# Prefer private packages
prefer-binary = true
```

**Preventive Measures:**

```csharp
using System.Net.Http.Json;
using System.Text.Json.Serialization;

/// <summary>
/// Dependency confusion detection and prevention utilities.
/// </summary>
public sealed class DependencyConfusionChecker(HttpClient httpClient)
{
    /// <summary>
    /// Check if internal NuGet package names exist on nuget.org.
    /// </summary>
    public async Task<Dictionary<string, ConfusionCheckResult>> CheckNuGetConfusionAsync(
        IEnumerable<string> internalPackages,
        CancellationToken cancellationToken = default)
    {
        var results = new Dictionary<string, ConfusionCheckResult>();

        foreach (var package in internalPackages)
        {
            try
            {
                var response = await httpClient.GetAsync(
                    $"https://api.nuget.org/v3/registration5-semver1/{package.ToLowerInvariant()}/index.json",
                    cancellationToken);

                if (response.IsSuccessStatusCode)
                {
                    var registration = await response.Content.ReadFromJsonAsync<NuGetRegistration>(
                        cancellationToken: cancellationToken);

                    var latestVersion = registration?.Items?.LastOrDefault()?.Upper;

                    results[package] = new ConfusionCheckResult(
                        ExistsPublicly: true,
                        PublicVersion: latestVersion,
                        Risk: ConfusionRisk.High,
                        Recommendation: "Register placeholder on nuget.org or use package prefix reservation");
                }
                else if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    results[package] = new ConfusionCheckResult(
                        ExistsPublicly: false,
                        PublicVersion: null,
                        Risk: ConfusionRisk.Low,
                        Recommendation: "Consider registering placeholder package");
                }
            }
            catch (Exception ex)
            {
                results[package] = new ConfusionCheckResult(
                    ExistsPublicly: false,
                    PublicVersion: null,
                    Risk: ConfusionRisk.Unknown,
                    Recommendation: $"Check failed: {ex.Message}");
            }
        }

        return results;
    }

    /// <summary>
    /// Generate placeholder .csproj for NuGet package reservation.
    /// </summary>
    public static string GeneratePlaceholderProject(
        string packageId,
        string description = "Internal package - not for public use")
    {
        return $"""
            <Project Sdk="Microsoft.NET.Sdk">
              <PropertyGroup>
                <TargetFramework>netstandard2.0</TargetFramework>
                <PackageId>{packageId}</PackageId>
                <Version>0.0.1</Version>
                <Description>{description}</Description>
                <Authors>Security Team</Authors>
                <PackageTags>placeholder;internal;reserved</PackageTags>
                <IncludeSymbols>false</IncludeSymbols>
                <IncludeSource>false</IncludeSource>
              </PropertyGroup>
            </Project>
            """;
    }
}

public sealed record ConfusionCheckResult(
    bool ExistsPublicly,
    string? PublicVersion,
    ConfusionRisk Risk,
    string Recommendation);

public enum ConfusionRisk { Low, Medium, High, Unknown }

public sealed record NuGetRegistration(
    [property: JsonPropertyName("items")] List<NuGetCatalogPage>? Items);

public sealed record NuGetCatalogPage(
    [property: JsonPropertyName("upper")] string? Upper);
```

## Code Signing with Sigstore

### Sigstore Overview

Sigstore provides keyless signing using OIDC identity:

```bash
# Install cosign
# macOS
brew install cosign

# Linux
curl -O -L "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64"
chmod +x cosign-linux-amd64
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
```

### Sign Container Images

```bash
# Sign with keyless (OIDC)
cosign sign ghcr.io/myorg/myimage:v1.0.0

# Sign with key
cosign generate-key-pair
cosign sign --key cosign.key ghcr.io/myorg/myimage:v1.0.0

# Verify signature
cosign verify ghcr.io/myorg/myimage:v1.0.0 \
  --certificate-identity=ci@myorg.com \
  --certificate-oidc-issuer=https://github.com/login/oauth
```

### Sign Python Packages

```bash
# Install sigstore
pip install sigstore

# Sign a package
python -m sigstore sign dist/mypackage-1.0.0.tar.gz

# Verify signature
python -m sigstore verify identity \
  --cert-identity ci@myorg.com \
  --cert-oidc-issuer https://github.com/login/oauth \
  dist/mypackage-1.0.0.tar.gz
```

### Sign npm Packages

```bash
# npm provenance (built-in since npm 9.5.0)
npm publish --provenance

# Verify provenance
npm audit signatures
```

## OpenSSF Scorecard

### Running Scorecard

```bash
# Install scorecard
# macOS
brew install scorecard

# Run on GitHub repo
scorecard --repo=github.com/myorg/myproject

# Run with specific checks
scorecard --repo=github.com/myorg/myproject \
  --checks=Vulnerabilities,Dependency-Update-Tool,Pinned-Dependencies

# Output as JSON
scorecard --repo=github.com/myorg/myproject --format=json > scorecard.json
```

### GitHub Action for Scorecard

```yaml
name: Scorecard Analysis
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday

permissions:
  security-events: write
  id-token: write
  contents: read
  actions: read

jobs:
  analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Run Scorecard
        uses: ossf/scorecard-action@v2
        with:
          results_file: results.sarif
          results_format: sarif
          publish_results: true

      - name: Upload to Security tab
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
```

### Scorecard Checks Explained

| Check | What It Measures | How to Improve |
|-------|------------------|----------------|
| **Vulnerabilities** | Known vulnerabilities in dependencies | Enable Dependabot, fix vulns |
| **Dependency-Update-Tool** | Automated dependency updates | Enable Dependabot/Renovate |
| **Pinned-Dependencies** | CI uses pinned dependencies | Pin action versions, use hashes |
| **Token-Permissions** | Minimal CI token permissions | Use least-privilege tokens |
| **Branch-Protection** | Main branch protection | Require reviews, status checks |
| **Code-Review** | PRs require review | Enable required reviews |
| **Signed-Releases** | Releases are signed | Use Sigstore/GPG signing |
| **Binary-Artifacts** | Repo contains binaries | Remove binaries, use releases |

## Security Checklist

### Pre-Release Checklist

- [ ] Generate SBOM for release
- [ ] Run vulnerability scan (npm audit, pip-audit, etc.)
- [ ] Verify all dependencies have lock file entries
- [ ] Check for dependency confusion risks
- [ ] Sign release artifacts with Sigstore
- [ ] Run OpenSSF Scorecard
- [ ] Verify provenance generation is enabled

### Repository Security

- [ ] Enable Dependabot or Renovate
- [ ] Configure branch protection rules
- [ ] Pin CI/CD action versions with hashes
- [ ] Use minimal token permissions
- [ ] Enable secret scanning
- [ ] Configure code owners for security files

### Dependency Management

- [ ] Use lock files in all projects
- [ ] Enable integrity hash verification
- [ ] Configure private registry for internal packages
- [ ] Register placeholder packages on public registries
- [ ] Review new dependencies before adding
- [ ] Monitor for typosquatting attempts

## References

- **SBOM Generation**: See `references/sbom-generation.md` for advanced SBOM workflows
- **SLSA Framework**: See `references/slsa-levels.md` for implementation guidance
- **Attack Prevention**: See `references/dependency-attacks.md` for detailed attack patterns

## Related Skills

- `secure-coding` - Secure development practices
- `devsecops-practices` - CI/CD security integration
- `container-security` - Container image signing and scanning

---

**Last Updated:** 2025-12-26
