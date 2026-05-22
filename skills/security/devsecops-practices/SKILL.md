---
name: devsecops-practices
description: DevSecOps methodology guidance covering shift-left security, SAST/DAST/IAST integration, security gates in CI/CD pipelines, vulnerability management workflows, and security champions programs.
allowed-tools: Read, Glob, Grep, Task
---

# DevSecOps Practices

Comprehensive guidance for integrating security throughout the software development lifecycle using DevSecOps principles.

## When to Use This Skill

- Implementing shift-left security practices
- Setting up SAST tools (Semgrep, CodeQL, SonarQube)
- Configuring DAST scanning (OWASP ZAP, Burp Suite)
- Integrating security gates in CI/CD pipelines
- Building vulnerability management workflows
- Establishing security champions programs
- Creating secure SDLC processes

## Quick Reference

### DevSecOps Maturity Levels

| Level | Characteristics | Key Practices |
|-------|-----------------|---------------|
| **Level 1: Initial** | Manual security reviews, ad-hoc testing | Basic vulnerability scanning, security training |
| **Level 2: Managed** | Automated scanning in CI/CD, defined processes | SAST integration, security gates |
| **Level 3: Defined** | Security embedded in all phases, metrics tracked | DAST/IAST, threat modeling, SLAs |
| **Level 4: Measured** | Continuous monitoring, risk-based decisions | Full automation, security dashboards |
| **Level 5: Optimizing** | Predictive security, continuous improvement | AI-assisted, chaos engineering |

### Security Testing Types

| Type | When | What It Finds | Tools |
|------|------|---------------|-------|
| **SAST** | Build time | Code vulnerabilities, patterns | Semgrep, CodeQL, SonarQube |
| **SCA** | Build time | Dependency vulnerabilities | Snyk, Dependabot, npm audit |
| **DAST** | Runtime | Running application vulns | OWASP ZAP, Burp Suite |
| **IAST** | Runtime | Combined SAST+DAST | Contrast, Seeker |
| **Secrets** | Commit time | Hardcoded credentials | Gitleaks, truffleHog |

### Security Gates by Pipeline Stage

```text
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Commit  │───►│  Build   │───►│  Test    │───►│  Deploy  │───►│Production│
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │               │               │
     ▼               ▼               ▼               ▼               ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│Secrets  │    │SAST     │    │DAST     │    │Container│    │Runtime  │
│Scanning │    │SCA      │    │Pen Test │    │Scanning │    │Security │
│Pre-commit    │License  │    │IAST     │    │Config   │    │Monitoring
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

## SAST (Static Application Security Testing)

### Semgrep Setup

```yaml
# .github/workflows/semgrep.yml
name: Semgrep
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep

    steps:
      - uses: actions/checkout@v5

      - name: Run Semgrep
        run: semgrep scan --config auto --sarif --output semgrep.sarif

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
```

### Semgrep Rules Configuration

```yaml
# .semgrep.yml
rules:
  # SQL Injection
  - id: sql-injection
    patterns:
      - pattern-either:
          - pattern: cursor.execute($QUERY % ...)
          - pattern: cursor.execute($QUERY.format(...))
          - pattern: cursor.execute(f"...")
    message: "Potential SQL injection. Use parameterized queries."
    severity: ERROR
    languages: [python]

  # Hardcoded Secrets
  - id: hardcoded-password
    pattern-regex: '(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{8,}["\']'
    message: "Hardcoded password detected"
    severity: ERROR
    languages: [python, javascript, typescript]

  # Insecure Crypto
  - id: insecure-hash
    patterns:
      - pattern-either:
          - pattern: hashlib.md5(...)
          - pattern: hashlib.sha1(...)
    message: "Use SHA-256 or stronger for cryptographic purposes"
    severity: WARNING
    languages: [python]
```

### CodeQL Setup

```yaml
# .github/workflows/codeql.yml
name: CodeQL Analysis
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write

    strategy:
      matrix:
        language: [javascript, python]

    steps:
      - uses: actions/checkout@v5

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: +security-extended

      - name: Build (if needed)
        uses: github/codeql-action/autobuild@v3

      - name: Perform Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
```

### SonarQube Integration

```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0  # Full history for accurate blame

      - name: SonarQube Scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

      - name: Quality Gate Check
        uses: sonarsource/sonarqube-quality-gate-action@master
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

```properties
# sonar-project.properties
sonar.projectKey=my-project
sonar.organization=my-org

# Source paths
sonar.sources=src
sonar.tests=tests

# Exclusions
sonar.exclusions=**/node_modules/**,**/*.test.js,**/vendor/**

# Coverage
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.python.coverage.reportPaths=coverage.xml

# Security hotspots review
sonar.security.hotspots.review.priority=HIGH
```

## DAST (Dynamic Application Security Testing)

### OWASP ZAP Integration

```yaml
# .github/workflows/zap.yml
name: OWASP ZAP Scan
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * 0'  # Weekly Sunday 2 AM

jobs:
  zap-scan:
    runs-on: ubuntu-latest
    services:
      app:
        image: my-app:latest
        ports:
          - 8080:8080

    steps:
      - uses: actions/checkout@v5

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.11.0
        with:
          target: 'http://localhost:8080'
          rules_file_name: '.zap/rules.tsv'

      - name: ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.9.0
        with:
          target: 'http://localhost:8080'
          cmd_options: '-a -j'

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: report_html.html
```

### ZAP Rules Configuration

```tsv
# .zap/rules.tsv
# Rule ID    Action    Description
10010       IGNORE    # Cookie No HttpOnly Flag (handled by framework)
10011       WARN      # Cookie Without Secure Flag
10015       FAIL      # Incomplete or No Cache-control and Pragma
10016       WARN      # Web Browser XSS Protection Not Enabled
10017       FAIL      # Cross-Domain JavaScript Source File Inclusion
10019       FAIL      # Content-Type Header Missing
10020       FAIL      # X-Frame-Options Header Not Set
10021       FAIL      # X-Content-Type-Options Header Missing
10038       FAIL      # Content Security Policy Header Not Set
```

### DAST in Docker Compose

```yaml
# docker-compose.security.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 5s
      timeout: 10s
      retries: 5

  zap:
    image: ghcr.io/zaproxy/zaproxy:stable
    depends_on:
      app:
        condition: service_healthy
    volumes:
      - ./zap-reports:/zap/wrk
    command: >
      zap-full-scan.py
      -t http://app:8080
      -r zap-report.html
      -J zap-report.json
      -x zap-report.xml
```

## Security Gates

### Gate Configuration

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

/// <summary>
/// Security gate enforcement for CI/CD pipelines.
/// </summary>
public enum Severity { Critical, High, Medium, Low, Info }

public enum GateDecision { Pass, Warn, Fail }

/// <summary>
/// Configuration for security gate thresholds.
/// </summary>
public sealed record SecurityGateConfig
{
    // SAST thresholds
    public int SastCriticalMax { get; init; } = 0;
    public int SastHighMax { get; init; } = 0;
    public int SastMediumMax { get; init; } = 5;

    // SCA thresholds
    public int ScaCriticalMax { get; init; } = 0;
    public int ScaHighMax { get; init; } = 2;
    public double ScaCvssThreshold { get; init; } = 7.0;

    // DAST thresholds
    public int DastCriticalMax { get; init; } = 0;
    public int DastHighMax { get; init; } = 1;

    // Secrets
    public int SecretsAllowed { get; init; } = 0;

    // License restrictions
    public IReadOnlyList<string> ForbiddenLicenses { get; init; } = ["GPL-3.0", "AGPL-3.0"];
}

/// <summary>
/// Aggregated results from security scans.
/// </summary>
public sealed record ScanResults(
    Dictionary<string, int> SastFindings,
    Dictionary<string, int> ScaFindings,
    Dictionary<string, int> DastFindings,
    int SecretsFound,
    IReadOnlyList<string> Licenses);

/// <summary>
/// Evaluates security gates for CI/CD pipelines.
/// </summary>
public static class SecurityGateEvaluator
{
    public static (GateDecision Decision, List<string> Reasons) Evaluate(
        SecurityGateConfig config,
        ScanResults results)
    {
        var reasons = new List<string>();
        var decision = GateDecision.Pass;

        // Check SAST
        if (results.SastFindings.GetValueOrDefault("critical", 0) > config.SastCriticalMax)
        {
            decision = GateDecision.Fail;
            reasons.Add($"SAST: {results.SastFindings["critical"]} critical findings (max: {config.SastCriticalMax})");
        }

        if (results.SastFindings.GetValueOrDefault("high", 0) > config.SastHighMax)
        {
            decision = GateDecision.Fail;
            reasons.Add($"SAST: {results.SastFindings["high"]} high findings (max: {config.SastHighMax})");
        }

        // Check SCA
        if (results.ScaFindings.GetValueOrDefault("critical", 0) > config.ScaCriticalMax)
        {
            decision = GateDecision.Fail;
            reasons.Add($"SCA: {results.ScaFindings["critical"]} critical vulnerabilities (max: {config.ScaCriticalMax})");
        }

        // Check secrets
        if (results.SecretsFound > config.SecretsAllowed)
        {
            decision = GateDecision.Fail;
            reasons.Add($"Secrets: {results.SecretsFound} secrets detected");
        }

        // Check licenses
        foreach (var license in results.Licenses)
        {
            if (config.ForbiddenLicenses.Contains(license))
            {
                decision = GateDecision.Fail;
                reasons.Add($"License: Forbidden license {license} detected");
            }
        }

        // Warnings (don't fail but report)
        if (results.SastFindings.GetValueOrDefault("medium", 0) > config.SastMediumMax)
        {
            if (decision == GateDecision.Pass)
                decision = GateDecision.Warn;
            reasons.Add($"SAST: {results.SastFindings["medium"]} medium findings (threshold: {config.SastMediumMax})");
        }

        return (decision, reasons);
    }
}

// Usage in CI (console app entry point)
public static class SecurityGateCli
{
    public static async Task<int> Main(string[] args)
    {
        var jsonPath = args.FirstOrDefault() ?? "scan-results.json";
        var json = await File.ReadAllTextAsync(jsonPath);
        var rawResults = JsonSerializer.Deserialize<RawScanResults>(json)!;

        var results = new ScanResults(
            rawResults.Sast ?? new(),
            rawResults.Sca ?? new(),
            rawResults.Dast ?? new(),
            rawResults.Secrets,
            rawResults.Licenses ?? []);

        var config = new SecurityGateConfig();
        var (decision, reasons) = SecurityGateEvaluator.Evaluate(config, results);

        Console.WriteLine($"Security Gate: {decision.ToString().ToUpper()}");
        foreach (var reason in reasons)
            Console.WriteLine($"  - {reason}");

        return decision == GateDecision.Fail ? 1 : 0;
    }

    private sealed record RawScanResults(
        [property: JsonPropertyName("sast")] Dictionary<string, int>? Sast,
        [property: JsonPropertyName("sca")] Dictionary<string, int>? Sca,
        [property: JsonPropertyName("dast")] Dictionary<string, int>? Dast,
        [property: JsonPropertyName("secrets")] int Secrets,
        [property: JsonPropertyName("licenses")] List<string>? Licenses);
}
```

### GitHub Actions Security Gate

```yaml
# .github/workflows/security-gate.yml
name: Security Gate
on:
  pull_request:
    branches: [main]

jobs:
  security-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      # Run all security scans
      - name: SAST - Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: auto
          generateSarif: true

      - name: SCA - npm audit
        run: npm audit --json > npm-audit.json || true

      - name: Secrets - Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # Aggregate and evaluate
      - name: Evaluate Security Gate
        run: |
          python scripts/security_gate.py \
            --sast-results semgrep.sarif \
            --sca-results npm-audit.json \
            --secrets-results gitleaks.json

      - name: Comment on PR
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('security-report.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: report
            });
```

## Secrets Scanning

### Pre-commit Hook with Gitleaks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### Gitleaks Configuration

```toml
# .gitleaks.toml
title = "Gitleaks Configuration"

[extend]
useDefault = true

[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''(?i)api[_-]?key\s*[:=]\s*['"]?[a-zA-Z0-9]{32,}['"]?'''
tags = ["key", "api"]

[[rules]]
id = "custom-password"
description = "Hardcoded Password"
regex = '''(?i)(password|passwd|pwd)\s*[:=]\s*['"][^'"]{8,}['"]'''
tags = ["password"]

[allowlist]
description = "Global allowlist"
paths = [
  '''\.gitleaks\.toml$''',
  '''\.secrets\.baseline$''',
  '''test/.*\.py$''',
  '''.*_test\.go$''',
]
```

### GitHub Secret Scanning

```yaml
# .github/workflows/secret-scanning.yml
name: Secret Scanning
on:
  push:
    branches: [main]
  pull_request:

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  trufflehog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified
```

## Vulnerability Management Workflow

### Vulnerability Tracking

```csharp
/// <summary>
/// Vulnerability management workflow automation.
/// </summary>
public enum VulnStatus
{
    New,
    Triaged,
    InProgress,
    Resolved,
    AcceptedRisk,
    FalsePositive
}

public enum VulnSeverity { Critical = 1, High = 2, Medium = 3, Low = 4 }

/// <summary>
/// Tracked vulnerability with lifecycle management.
/// </summary>
public sealed class Vulnerability
{
    public required string Id { get; init; }
    public string? CveId { get; init; }
    public required string Title { get; init; }
    public required string Description { get; init; }
    public required VulnSeverity Severity { get; init; }
    public required double CvssScore { get; init; }
    public required string AffectedComponent { get; init; }
    public required string AffectedVersion { get; init; }
    public string? FixedVersion { get; init; }

    // Tracking
    public VulnStatus Status { get; set; } = VulnStatus.New;
    public string? Assignee { get; set; }
    public DateTime DiscoveredDate { get; init; } = DateTime.UtcNow;
    public DateTime? DueDate { get; set; }
    public DateTime? ResolvedDate { get; set; }
    public List<string> Notes { get; } = [];
}

/// <summary>
/// Manages vulnerability lifecycle with SLA tracking.
/// </summary>
public sealed class VulnerabilityManager
{
    private static readonly IReadOnlyDictionary<VulnSeverity, int> SlaDays = new Dictionary<VulnSeverity, int>
    {
        [VulnSeverity.Critical] = 7,
        [VulnSeverity.High] = 30,
        [VulnSeverity.Medium] = 90,
        [VulnSeverity.Low] = 180,
    };

    private readonly Dictionary<string, Vulnerability> _vulnerabilities = new();

    public void AddVulnerability(Vulnerability vuln)
    {
        // Auto-set due date based on SLA
        vuln.DueDate ??= vuln.DiscoveredDate.AddDays(
            SlaDays.GetValueOrDefault(vuln.Severity, 90));

        _vulnerabilities[vuln.Id] = vuln;
    }

    public void Triage(string vulnId, string assignee, VulnStatus status = VulnStatus.Triaged)
    {
        if (_vulnerabilities.TryGetValue(vulnId, out var vuln))
        {
            vuln.Status = status;
            vuln.Assignee = assignee;
            vuln.Notes.Add($"{DateTime.UtcNow:O}: Triaged to {assignee}");
        }
    }

    public void Resolve(string vulnId, string resolution, VulnStatus status = VulnStatus.Resolved)
    {
        if (_vulnerabilities.TryGetValue(vulnId, out var vuln))
        {
            vuln.Status = status;
            vuln.ResolvedDate = DateTime.UtcNow;
            vuln.Notes.Add($"{DateTime.UtcNow:O}: Resolved - {resolution}");
        }
    }

    public void AcceptRisk(string vulnId, string justification, string approver)
    {
        if (_vulnerabilities.TryGetValue(vulnId, out var vuln))
        {
            vuln.Status = VulnStatus.AcceptedRisk;
            vuln.Notes.Add($"{DateTime.UtcNow:O}: Risk accepted by {approver} - {justification}");
        }
    }

    public IEnumerable<Vulnerability> GetOverdue()
    {
        var now = DateTime.UtcNow;
        return _vulnerabilities.Values.Where(v =>
            v.Status is not (VulnStatus.Resolved or VulnStatus.AcceptedRisk or VulnStatus.FalsePositive) &&
            v.DueDate.HasValue &&
            v.DueDate.Value < now);
    }

    public VulnerabilityMetrics GetMetrics()
    {
        var vulns = _vulnerabilities.Values.ToList();

        return new VulnerabilityMetrics(
            Total: vulns.Count,
            Open: vulns.Count(v => v.Status is VulnStatus.New or VulnStatus.Triaged or VulnStatus.InProgress),
            Resolved: vulns.Count(v => v.Status == VulnStatus.Resolved),
            Overdue: GetOverdue().Count(),
            BySeverity: Enum.GetValues<VulnSeverity>().ToDictionary(
                sev => sev.ToString(),
                sev => vulns.Count(v => v.Severity == sev)),
            MttrDays: CalculateMttr(vulns));
    }

    private static double CalculateMttr(List<Vulnerability> vulns)
    {
        var resolved = vulns
            .Where(v => v.Status == VulnStatus.Resolved && v.ResolvedDate.HasValue)
            .ToList();

        if (resolved.Count == 0) return 0.0;

        var totalDays = resolved.Sum(v => (v.ResolvedDate!.Value - v.DiscoveredDate).TotalDays);
        return totalDays / resolved.Count;
    }
}

public sealed record VulnerabilityMetrics(
    int Total,
    int Open,
    int Resolved,
    int Overdue,
    Dictionary<string, int> BySeverity,
    double MttrDays);
```

## Security Champions Program

### Program Structure

```markdown
# Security Champions Program

## Roles and Responsibilities

### Security Champion
- Embedded security advocate within development team
- First point of contact for security questions
- Participates in security training and shares knowledge
- Reviews security-critical code changes
- Triages security findings for their team

### Time Commitment
- 10-20% of work time on security activities
- Weekly security standup (30 min)
- Monthly security training (2 hours)
- Quarterly security deep-dive (4 hours)

## Selection Criteria
- 1+ year on the team
- Interest in security
- Good communication skills
- Technical credibility with peers

## Training Path
1. **Month 1**: Security fundamentals
   - OWASP Top 10
   - Secure coding basics
   - Company security policies

2. **Month 2**: Tools and processes
   - SAST/DAST tool usage
   - Security gate process
   - Vulnerability management

3. **Month 3**: Advanced topics
   - Threat modeling
   - Security architecture review
   - Incident response basics

## Metrics
- Vulnerabilities found by champion reviews
- Security training completion rate
- Time to remediate findings
- Security culture survey scores
```

## Security Checklist

### Pre-Development

- [ ] Threat model completed for new features
- [ ] Security requirements documented
- [ ] Secure design patterns identified
- [ ] Security champions assigned

### During Development

- [ ] Pre-commit hooks enabled (secrets, linting)
- [ ] SAST integrated in IDE
- [ ] Secure coding guidelines followed
- [ ] Security-sensitive code reviewed by champion

### Pre-Deployment

- [ ] All security gates passed
- [ ] SAST findings addressed
- [ ] SCA vulnerabilities resolved or accepted
- [ ] DAST scan completed
- [ ] Security review approved

### Post-Deployment

- [ ] Runtime security monitoring enabled
- [ ] Vulnerability scanning scheduled
- [ ] Incident response plan updated
- [ ] Security metrics collected

## References

- **SAST Tools**: See `references/sast-tools.md` for detailed tool configurations
- **Security Gates**: See `references/security-gates.md` for gate implementation
- **Vulnerability Workflow**: See `references/vulnerability-workflow.md` for complete workflow

## Related Skills

- `secure-coding` - Secure development practices
- `supply-chain-security` - Dependency and SBOM management
- `threat-modeling` - Threat identification and mitigation

---

**Last Updated:** 2025-12-26
