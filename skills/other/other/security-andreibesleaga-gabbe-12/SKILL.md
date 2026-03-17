---
name: dependency-security
description: Managing Supply Chain Security, SBOM generation, and vulnerability patching (SCA).
role: ops-security, ops-devops
triggers:
  - supply chain
  - sbom
  - dependency scan
  - npm audit
  - deps
  - vulnerability
---

# dependency-security Skill

This skill secures the software supply chain.

## 1. Software Composition Analysis (SCA)
> "You are what you import."

- **Audit**: Run `npm audit` / `pip-audit` / `cargo audit` in CI.
- **Block**: Fail the build on `CRITICAL` or `HIGH` vulnerabilities.
- **Lock**: Always verify lockfiles (`package-lock.json`) match `package.json`.

## 2. SBOM (Software Bill of Materials)
- Generate a list of all ingredients in your software.
- Tools: `syft`, `cyclonedx-cli`.
- Why? Rapid response when the next Log4Shell happens.

## 3. Dependency Pinning
- **Pin Exact Versions**: Avoid `^1.2.3` in critical apps. Use `1.2.3` to prevent "works on my machine" drift.
- **Private Registry**: For enterprise, proxy public registries to prevent "Left-Pad" incidents.

## 4. Typosquatting Defense
- **Scope**: Use `@myorg/package` scopes.
- **Verify**: Check download counts and maintainer reputation before adding new deps.
