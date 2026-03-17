---
name: penetration-testing
description: Ethical hacking and security testing methodologies using penetration testing tools, exploit frameworks, and manual security validation. Use when assessing application security posture and identifying exploitable vulnerabilities.
---

# Penetration Testing

## Overview

Systematic security testing to identify, exploit, and document vulnerabilities in applications, networks, and infrastructure through simulated attacks.

## When to Use

- Pre-production security validation
- Annual security assessments
- Compliance requirements (PCI-DSS, ISO 27001)
- Post-incident security review
- Third-party security audits
- Red team exercises

## Implementation Examples

### 1. **Automated Penetration Testing Framework**

```python
# pentest_framework.py
import requests
import socket
import subprocess
import json
from typing import List, Dict
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Finding:
    severity: str
    category: str
    target: str
    vulnerability: str
    evidence: str
    remediation: str
    cvss_score: float

class PenetrationTester:
    def __init__(self, target: str):
        self.target = target
        self.findings: List[Finding] = []

    def test_sql_injection(self, url: str) -> None:
        """Test for SQL injection vulnerabilities"""
        print(f"Testing SQL injection on {url}")

        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users--",
            "' UNION SELECT NULL, NULL, NULL--",
            "1' AND 1=1--",
            "admin'--"
        ]

        for payload in payloads:
            try:
                response = requests.get(
                    url,
                    params={'id': payload},
                    timeout=5
                )

                # Check for SQL errors
                sql_errors = [
                    'mysql_fetch_array',
                    'SQLServer JDBC Driver',
                    'ORA-01756',
                    'PostgreSQL',
                    'sqlite3.OperationalError'
                ]

                for error in sql_errors:
                    if error in response.text:
                        self.findings.append(Finding(
                            severity='critical',
                            category='SQL Injection',
                            target=url,
                            vulnerability=f'SQL Injection detected with payload: {payload}',
                            evidence=f'Error message: {error}',
                            remediation='Use parameterized queries or prepared statements',
                            cvss_score=9.8
                        ))
                        break

            except Exception as e:
                print(f"Error testing {url}: {e}")

    def test_xss(self, url: str) -> None:
        """Test for Cross-Site Scripting vulnerabilities"""
        print(f"Testing XSS on {url}")

        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "'-alert('XSS')-'"
        ]

        for payload in payloads:
            try:
                response = requests.get(
                    url,
                    params={'q': payload},
                    timeout=5
                )

                if payload in response.text:
                    self.findings.append(Finding(
                        severity='high',
                        category='Cross-Site Scripting',
                        target=url,
                        vulnerability=f'Reflected XSS detected with payload: {payload}',
                        evidence='Payload reflected in response without sanitization',
                        remediation='Implement output encoding and Content Security Policy',
                        cvss_score=7.3
                    ))
                    break

            except Exception as e:
                print(f"Error testing {url}: {e}")

    def test_authentication(self, login_url: str) -> None:
        """Test authentication mechanisms"""
        print(f"Testing authentication on {login_url}")

        # Test default credentials
        default_creds = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('root', 'root'),
            ('administrator', 'administrator')
        ]

        for username, password in default_creds:
            try:
                response = requests.post(
                    login_url,
                    data={'username': username, 'password': password},
                    timeout=5
                )

                if response.status_code == 200 and 'dashboard' in response.text.lower():
                    self.findings.append(Finding(
                        severity='critical',
                        category='Weak Authentication',
                        target=login_url,
                        vulnerability=f'Default credentials accepted: {username}/{password}',
                        evidence='Successful authentication with default credentials',
                        remediation='Enforce strong password policy and remove default accounts',
                        cvss_score=9.1
                    ))

            except Exception as e:
                print(f"Error testing credentials: {e}")

    def test_security_headers(self, url: str) -> None:
        """Test for missing security headers"""
        print(f"Testing security headers on {url}")

        try:
            response = requests.get(url, timeout=5)

            critical_headers = {
                'Strict-Transport-Security': 'HSTS not implemented',
                'X-Frame-Options': 'Clickjacking protection missing',
                'X-Content-Type-Options': 'MIME sniffing prevention missing',
                'Content-Security-Policy': 'CSP not implemented',
                'X-XSS-Protection': 'XSS protection header missing'
            }

            for header, description in critical_headers.items():
                if header not in response.headers:
                    self.findings.append(Finding(
                        severity='medium',
                        category='Missing Security Header',
                        target=url,
                        vulnerability=f'Missing header: {header}',
                        evidence=description,
                        remediation=f'Add {header} header to all responses',
                        cvss_score=5.3
                    ))

        except Exception as e:
            print(f"Error testing headers: {e}")

    def test_directory_traversal(self, url: str) -> None:
        """Test for directory traversal vulnerabilities"""
        print(f"Testing directory traversal on {url}")

        payloads = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '....//....//....//etc/passwd',
            '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd'
        ]

        for payload in payloads:
            try:
                response = requests.get(
                    url,
                    params={'file': payload},
                    timeout=5
                )

                # Check for Unix passwd file
                if 'root:' in response.text or 'daemon:' in response.text:
                    self.findings.append(Finding(
                        severity='critical',
                        category='Directory Traversal',
                        target=url,
                        vulnerability=f'Path traversal detected with payload: {payload}',
                        evidence='System file contents exposed',
                        remediation='Validate and sanitize file paths, use whitelist approach',
                        cvss_score=8.6
                    ))
                    break

            except Exception as e:
                print(f"Error testing traversal: {e}")

    def test_ssl_tls(self) -> None:
        """Test SSL/TLS configuration"""
        print(f"Testing SSL/TLS on {self.target}")

        try:
            result = subprocess.run(
                ['testssl.sh', '--jsonfile', 'ssl-results.json', self.target],
                capture_output=True,
                text=True,
                timeout=60
            )

            # Parse SSL test results
            # This is a simplified check
            weak_protocols = ['SSLv2', 'SSLv3', 'TLSv1.0']
            for protocol in weak_protocols:
                self.findings.append(Finding(
                    severity='high',
                    category='Weak SSL/TLS',
                    target=self.target,
                    vulnerability=f'Weak protocol enabled: {protocol}',
                    evidence='Outdated SSL/TLS protocol support',
                    remediation='Disable weak protocols, enforce TLS 1.2+',
                    cvss_score=7.5
                ))

        except Exception as e:
            print(f"SSL test error: {e}")

    def run_full_pentest(self, target_urls: List[str]) -> Dict:
        """Execute comprehensive penetration test"""
        for url in target_urls:
            self.test_sql_injection(url)
            self.test_xss(url)
            self.test_security_headers(url)
            self.test_directory_traversal(url)

        self.test_ssl_tls()

        return self.generate_report()

    def generate_report(self) -> Dict:
        """Generate comprehensive pentest report"""
        summary = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }

        for finding in self.findings:
            if finding.severity in summary:
                summary[finding.severity] += 1

        report = {
            'timestamp': datetime.now().isoformat(),
            'target': self.target,
            'total_findings': len(self.findings),
            'summary': summary,
            'findings': [asdict(f) for f in self.findings],
            'risk_score': self._calculate_risk_score(),
            'recommendations': self._generate_recommendations()
        }

        with open('pentest-report.json', 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def _calculate_risk_score(self) -> float:
        """Calculate overall risk score"""
        if not self.findings:
            return 0.0

        total_cvss = sum(f.cvss_score for f in self.findings)
        return round(total_cvss / len(self.findings), 2)

    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        categories = {}
        for finding in self.findings:
            if finding.category not in categories:
                categories[finding.category] = []
            categories[finding.category].append(finding)

        for category, findings in sorted(
            categories.items(),
            key=lambda x: len(x[1]),
            reverse=True
        ):
            recommendations.append(
                f"Address {len(findings)} {category} vulnerabilities"
            )

        return recommendations[:5]

# Usage
if __name__ == '__main__':
    tester = PenetrationTester('https://example.com')

    target_urls = [
        'https://example.com/api/users',
        'https://example.com/search',
        'https://example.com/download'
    ]

    report = tester.run_full_pentest(target_urls)

    print("\n=== Penetration Test Report ===")
    print(f"Target: {report['target']}")
    print(f"Total Findings: {report['total_findings']}")
    print(f"Risk Score: {report['risk_score']}")
    print(f"\nFindings by Severity:")
    print(f"  Critical: {report['summary']['critical']}")
    print(f"  High: {report['summary']['high']}")
    print(f"  Medium: {report['summary']['medium']}")
    print(f"  Low: {report['summary']['low']}")
```

### 2. **Burp Suite Automation Script**

```javascript
// burp-automation.js - Node.js Burp Suite integration
const axios = require('axios');
const fs = require('fs').promises;

class BurpSuiteAutomation {
  constructor(burpApiUrl = 'http://127.0.0.1:1337') {
    this.apiUrl = burpApiUrl;
    this.taskId = null;
  }

  async startScan(targetUrl) {
    console.log(`Starting Burp scan for ${targetUrl}`);

    const scanConfig = {
      urls: [targetUrl],
      scan_configurations: [
        {
          name: 'Crawl and Audit - Lightweight',
          type: 'NamedConfiguration'
        }
      ]
    };

    try {
      const response = await axios.post(
        `${this.apiUrl}/v0.1/scan`,
        scanConfig
      );

      this.taskId = response.data.task_id;
      console.log(`Scan started with task ID: ${this.taskId}`);

      return this.taskId;
    } catch (error) {
      console.error('Failed to start scan:', error.message);
      throw error;
    }
  }

  async getScanStatus() {
    if (!this.taskId) {
      throw new Error('No active scan task');
    }

    const response = await axios.get(
      `${this.apiUrl}/v0.1/scan/${this.taskId}`
    );

    return {
      taskId: this.taskId,
      status: response.data.scan_status,
      metrics: response.data.scan_metrics
    };
  }

  async waitForCompletion() {
    console.log('Waiting for scan to complete...');

    while (true) {
      const status = await this.getScanStatus();

      console.log(`Progress: ${status.metrics.crawl_requests_made} requests`);

      if (status.status === 'succeeded') {
        console.log('Scan completed successfully');
        break;
      } else if (status.status === 'failed') {
        throw new Error('Scan failed');
      }

      await new Promise(resolve => setTimeout(resolve, 10000));
    }
  }

  async getIssues() {
    if (!this.taskId) {
      throw new Error('No active scan task');
    }

    const response = await axios.get(
      `${this.apiUrl}/v0.1/scan/${this.taskId}/issues`
    );

    return response.data.issues;
  }

  async generateReport() {
    const issues = await this.getIssues();

    const report = {
      summary: {
        high: 0,
        medium: 0,
        low: 0,
        info: 0
      },
      issues: []
    };

    for (const issue of issues) {
      report.summary[issue.severity.toLowerCase()]++;

      report.issues.push({
        severity: issue.severity,
        confidence: issue.confidence,
        name: issue.name,
        path: issue.path,
        description: issue.description,
        remediation: issue.remediation
      });
    }

    await fs.writeFile(
      'burp-report.json',
      JSON.stringify(report, null, 2)
    );

    return report;
  }
}

// Usage
async function runBurpScan() {
  const burp = new BurpSuiteAutomation();

  await burp.startScan('https://example.com');
  await burp.waitForCompletion();

  const report = await burp.generateReport();

  console.log('\n=== Burp Suite Scan Results ===');
  console.log(`High: ${report.summary.high}`);
  console.log(`Medium: ${report.summary.medium}`);
  console.log(`Low: ${report.summary.low}`);
}

runBurpScan().catch(console.error);
```

## Best Practices

### ✅ DO
- Get written authorization
- Define clear scope
- Use controlled environments
- Document all findings
- Follow responsible disclosure
- Provide remediation guidance
- Verify fixes after patching
- Maintain chain of custody

### ❌ DON'T
- Test production without approval
- Cause service disruption
- Exfiltrate sensitive data
- Share findings publicly
- Exceed authorized scope
- Use destructive payloads

## Penetration Testing Phases

1. **Reconnaissance**: Information gathering
2. **Scanning**: Vulnerability identification
3. **Exploitation**: Proof of concept
4. **Post-Exploitation**: Assess impact
5. **Reporting**: Document findings
6. **Remediation**: Assist with fixes

## Common Tools

- **Burp Suite**: Web application testing
- **OWASP ZAP**: Free security scanner
- **Metasploit**: Exploitation framework
- **Nmap**: Network scanning
- **SQLMap**: SQL injection testing
- **testssl.sh**: SSL/TLS testing
- **Nikto**: Web server scanner

## Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PTES Technical Guidelines](http://www.pentest-standard.org/)
- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [Metasploit Unleashed](https://www.metasploitunleashed.com/)
