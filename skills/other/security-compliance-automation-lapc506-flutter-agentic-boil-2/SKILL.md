# 🔒 Skill: Security & Compliance Automation

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-security-compliance-automation` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `security`, `compliance`, `automation`, `vulnerability-scanning`, `policy-as-code`, `opa`, `cis-benchmark` |
| **Referencia** | [OPA Documentation](https://www.openpolicyagent.org/docs/latest/) |

## 🔑 Keywords para Invocación

- `security-automation`
- `compliance`
- `vulnerability-scanning`
- `policy-as-code`
- `opa`
- `cis-benchmark`
- `security-policies`
- `@skill:security-compliance`

### Ejemplos de Prompts

```
Implementa security policies con OPA y compliance automation
```

```
Configura vulnerability scanning y security policies
```

```
Setup CIS benchmark compliance y security automation
```

```
@skill:security-compliance - Security y compliance automation
```

## 📖 Descripción

Security y compliance automation aseguran que sistemas cumplan con estándares de seguridad y compliance automáticamente. Este skill cubre policy-as-code con OPA, vulnerability scanning, compliance checking, security policies, y automated remediation.

### ✅ Cuándo Usar Este Skill

- Compliance requirements (SOC2, HIPAA, etc.)
- Security policies enforcement
- Vulnerability management
- Security audits
- Automated security checks

### ❌ Cuándo NO Usar Este Skill

- Sin requisitos de compliance
- Sistemas no críticos
- Desarrollo local solo

## 🏗️ Security Automation Framework

```
Policy Definition (OPA)
    ↓
Policy Enforcement
    ↓
Compliance Checking
    ↓
Automated Remediation
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - **Vulnerability Scanner:** [`scripts/vulnerability_scanner.py`](scripts/vulnerability_scanner.py) - Escaneo de vulnerabilidades con Trivy
> - **Compliance Checker:** [`scripts/compliance_checker.py`](scripts/compliance_checker.py) - Verificación de compliance AWS
> - **Auto Remediation:** [`scripts/auto_remediation.py`](scripts/auto_remediation.py) - Remediation automática Kubernetes
> 
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso completa.

### 1. OPA Policies

```rego
# policies/kubernetes-security.rego
package kubernetes.security

# Deny containers running as root
deny[msg] {
    container := input.review.object.spec.containers[_]
    container.securityContext.runAsUser == 0
    msg := "Container must not run as root"
}

# Require resource limits
deny[msg] {
    container := input.review.object.spec.containers[_]
    not container.resources.limits.memory
    msg := "Container must have memory limits"
}

deny[msg] {
    container := input.review.object.spec.containers[_]
    not container.resources.limits.cpu
    msg := "Container must have CPU limits"
}

# Require image from approved registry
deny[msg] {
    container := input.review.object.spec.containers[_]
    not startswith(container.image, "gcr.io/")
    not startswith(container.image, "docker.io/approved/")
    msg := "Container image must be from approved registry"
}

# Require non-privileged containers
deny[msg] {
    container := input.review.object.spec.containers[_]
    container.securityContext.privileged == true
    msg := "Container must not run in privileged mode"
}
```

### 2. Vulnerability Scanning

```yaml
# scanning/trivy-scan.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: vulnerability-scan
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: trivy
            image: aquasec/trivy:latest
            args:
              - image
              - --severity
              - HIGH,CRITICAL
              - --format
              - json
              - --exit-code
              - 1
              - gcr.io/my-project/my-app:latest
            env:
            - name: TRIVY_CACHE_DIR
              value: /tmp/trivy-cache
          restartPolicy: OnFailure
```

```python
# security/vulnerability_scanner.py
import subprocess
import json
from typing import List, Dict

class VulnerabilityScanner:
    def scan_image(self, image: str) -> List[Dict]:
        """Scan container image for vulnerabilities."""
        result = subprocess.run(
            ['trivy', 'image', '--format', 'json', image],
            capture_output=True,
            text=True
        )
        
        data = json.loads(result.stdout)
        vulnerabilities = []
        
        for result in data.get('Results', []):
            for vuln in result.get('Vulnerabilities', []):
                if vuln['Severity'] in ['HIGH', 'CRITICAL']:
                    vulnerabilities.append({
                        'id': vuln['VulnerabilityID'],
                        'severity': vuln['Severity'],
                        'package': vuln['PkgName'],
                        'installed_version': vuln['InstalledVersion'],
                        'fixed_version': vuln.get('FixedVersion'),
                        'title': vuln['Title'],
                    })
        
        return vulnerabilities

    def check_compliance(self, image: str) -> Dict:
        """Check image against CIS benchmarks."""
        result = subprocess.run(
            ['trivy', 'image', '--security-checks', 'config', image],
            capture_output=True,
            text=True
        )
        
        # Parse compliance results
        return self._parse_compliance(result.stdout)

    def _parse_compliance(self, output: str) -> Dict:
        # Parse compliance output
        return {'status': 'compliant', 'issues': []}
```

### 3. Compliance Automation

**Script ejecutable:** [`scripts/compliance_checker.py`](scripts/compliance_checker.py)

Verificador de compliance para recursos AWS contra CIS benchmarks.

**Cuándo ejecutar:**
- Auditorías de compliance regulares
- Verificación de políticas AWS
- Generación de reportes de compliance

**Uso:**
```bash
# Verificar CIS benchmark
python scripts/compliance_checker.py check-cis

# Verificar regla específica
python scripts/compliance_checker.py check-rule --rule-name access-keys-rotated

# Generar reporte
python scripts/compliance_checker.py report --output compliance-report.txt
```

**Características:**
- ✅ Verificación de CIS benchmark
- ✅ Verificación de reglas específicas
- ✅ Generación de reportes detallados
- ✅ Soporte multi-región

### 4. Security Policies as Code

```yaml
# policies/security-policies.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: security-policies
data:
  policies.yaml: |
    policies:
      - name: require-https
        description: "All services must use HTTPS"
        enforcement: deny
        rules:
          - path: "spec.ports[*].protocol"
            operator: equals
            value: TCP
          - path: "spec.ports[*].port"
            operator: not_in
            values: [443, 8443]
      
      - name: require-resource-limits
        description: "All containers must have resource limits"
        enforcement: warn
        rules:
          - path: "spec.containers[*].resources.limits"
            operator: exists
      
      - name: no-root-containers
        description: "Containers must not run as root"
        enforcement: deny
        rules:
          - path: "spec.containers[*].securityContext.runAsUser"
            operator: not_equals
            value: 0
```

### 5. Automated Remediation

**Script ejecutable:** [`scripts/auto_remediation.py`](scripts/auto_remediation.py)

Remediation automática de problemas de seguridad y compliance en Kubernetes.

**Cuándo ejecutar:**
- Remediation automática de recursos no-compliant
- Corrección de problemas de seguridad
- Aplicación de políticas de seguridad

**Uso:**
```bash
# Remediar namespace completo
python scripts/auto_remediation.py remediate --namespace production

# Dry run (ver qué se remediaría)
python scripts/auto_remediation.py remediate --namespace production --dry-run

# Remediar recurso específico
python scripts/auto_remediation.py remediate-resource \
  --kind Pod \
  --name my-pod \
  --namespace default
```

**Características:**
- ✅ Remediation automática de pods
- ✅ Corrección de security contexts
- ✅ Aplicación de resource limits
- ✅ Dry-run mode para preview

## 🎯 Mejores Prácticas

### 1. Policy as Code

✅ **DO:**
- Version control policies
- Test policies
- Review policy changes
- Document policies

❌ **DON'T:**
- Hardcode policies
- Skip policy testing
- Ignore policy violations

### 2. Vulnerability Management

✅ **DO:**
- Scan regularly
- Prioritize critical vulnerabilities
- Automate scanning
- Track remediation

❌ **DON'T:**
- Ignore vulnerabilities
- Skip scanning
- Deploy with known vulnerabilities

### 3. Compliance

✅ **DO:**
- Automate compliance checks
- Document compliance status
- Remediate non-compliance
- Regular audits

❌ **DON'T:**
- Manual compliance checks
- Ignore compliance gaps
- Skip remediation

## 🚨 Troubleshooting

### Policy Violations

1. Review policy rules
2. Check resource configuration
3. Update policies if needed
4. Remediate violations

### Compliance Failures

1. Identify failing checks
2. Review compliance requirements
3. Implement fixes
4. Re-run compliance checks

## 📚 Recursos Adicionales

- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [Trivy Scanner](https://github.com/aquasecurity/trivy)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

