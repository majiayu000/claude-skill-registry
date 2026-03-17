# 🛡️ Skill: Container Security

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-container-security` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `container-security`, `image-scanning`, `runtime-security`, `falco`, `notary`, `image-signing`, `cve-scanning` |
| **Referencia** | [Falco Documentation](https://falco.org/docs/) |

## 🔑 Keywords para Invocación

- `container-security`
- `image-scanning`
- `runtime-security`
- `falco`
- `notary`
- `image-signing`
- `cve-scanning`
- `@skill:container-security`

### Ejemplos de Prompts

```
Implementa container security con image scanning y runtime protection
```

```
Configura Falco para runtime security monitoring
```

```
Setup image signing y vulnerability scanning
```

```
@skill:container-security - Container security completo
```

## 📖 Descripción

Container security protege aplicaciones containerizadas a través de image scanning, runtime protection, image signing, y security policies. Este skill cubre herramientas como Falco, Trivy, Notary, y best practices de container security.

### ✅ Cuándo Usar Este Skill

- Container-based deployments
- Kubernetes clusters
- Security requirements
- Compliance requirements
- Production environments

### ❌ Cuándo NO Usar Este Skill

- No container usage
- Development only
- No security requirements

## 🏗️ Container Security Layers

```
Image Security
    ↓
Build Security
    ↓
Registry Security
    ↓
Runtime Security
    ↓
Orchestration Security
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - **Image Signing:** [`scripts/sign-image.sh`](scripts/sign-image.sh) - Firmar imágenes con Notary (Bash)
> - **Admission Controller:** [`scripts/admission_controller.py`](scripts/admission_controller.py) - Validación de seguridad de pods (Python CLI)
>
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso completa.

### 1. Image Scanning

```yaml
# security/trivy-scan.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: trivy-config
data:
  trivy.yaml: |
    db:
      repository: ghcr.io/aquasecurity/trivy-db
      cacheDir: /tmp/trivy-db
    cache:
      dir: /tmp/trivy-cache
    severity: CRITICAL,HIGH
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: image-scan
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: trivy
            image: aquasec/trivy:latest
            command:
            - trivy
            - image
            - --severity
            - CRITICAL,HIGH
            - --format
            - json
            - --exit-code
            - 1
            - gcr.io/my-project/my-app:latest
          restartPolicy: OnFailure
```

### 2. Falco Runtime Security

```yaml
# security/falco-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: falco-config
data:
  falco.yaml: |
    rules_file:
      - /etc/falco/falco_rules.yaml
      - /etc/falco/rules.d/

    json_output: true
    json_include_output_property: true
    json_include_tags_property: true

    log_stderr: true
    log_syslog: false
    log_level: info

    http_output:
      enabled: true
      url: http://falco-sidekick:2801

    webserver:
      enabled: true
      listen_port: 8765
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: falco
spec:
  selector:
    matchLabels:
      app: falco
  template:
    metadata:
      labels:
        app: falco
    spec:
      hostNetwork: true
      containers:
      - name: falco
        image: falcosecurity/falco:latest
        securityContext:
          privileged: true
        volumeMounts:
        - name: dev-fs
          mountPath: /host/dev
        - name: proc-fs
          mountPath: /host/proc
          readOnly: true
        - name: sys-fs
          mountPath: /host/sys
          readOnly: true
        - name: boot-fs
          mountPath: /host/boot
          readOnly: true
        - name: modules-fs
          mountPath: /host/lib/modules
          readOnly: true
        - name: usr-fs
          mountPath: /host/usr
          readOnly: true
        - name: falco-config
          mountPath: /etc/falco
      volumes:
      - name: dev-fs
        hostPath:
          path: /dev
      - name: proc-fs
        hostPath:
          path: /proc
      - name: sys-fs
        hostPath:
          path: /sys
      - name: boot-fs
        hostPath:
          path: /boot
      - name: modules-fs
        hostPath:
          path: /lib/modules
      - name: usr-fs
        hostPath:
          path: /usr
      - name: falco-config
        configMap:
          name: falco-config
```

### 3. Falco Rules

```yaml
# security/falco-rules.yaml
- rule: Write below binary dir
  desc: Detect writes to binary directories
  condition: >
    bin_dir and evt.dir = < and open_write
    and not package_mgmt_procs
    and not exe_running_docker_save
    and not python_running_getsched
    and not user_expected_write_binary_dir_conditions
  output: >
    File below a known binary directory opened for writing
    (user=%user.name user_loginuid=%user.loginuid command=%proc.cmdline
    file=%fd.name parent=%proc.pname pcmdline=%proc.pcmdline gparent=%proc.aname[2]
    container_id=%container.id image=%container.image.repository)
  priority: ERROR
  tags: [filesystem, mitre_persistence]

- rule: Detect shell in container
  desc: Notice shell activity within a container
  condition: >
    spawned_process and container
    and shell_procs and proc.tty != 0
    and container_entrypoint
    and not user_expected_shell_in_container_conditions
  output: >
    Shell spawned in container (user=%user.name user_loginuid=%user.loginuid
    %container.info shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline
    terminal=%proc.tty container_id=%container.id image=%container.image.repository)
  priority: NOTICE
  tags: [shell, mitre_execution]

- rule: Unexpected network activity
  desc: Detect unexpected network connections
  condition: >
    evt.type = connect and evt.dir = < and container
    and not trusted_containers
    and fd.sip != "127.0.0.1"
    and not user_expected_network_activity_conditions
  output: >
    Unexpected network connection (user=%user.name command=%proc.cmdline
    connection=%fd.name container_id=%container.id image=%container.image.repository)
  priority: WARNING
  tags: [network, mitre_command_and_control]
```

### 4. Image Signing

**Script ejecutable:** [`scripts/sign-image.sh`](scripts/sign-image.sh)

Script para firmar imágenes de contenedores con Notary.

**Cuándo ejecutar:**
- Firmar imágenes antes de deployment
- CI/CD pipelines
- Verificación de integridad de imágenes

**Uso:**
```bash
chmod +x scripts/sign-image.sh

# Firmar imagen
./scripts/sign-image.sh --image gcr.io/my-project/my-app:latest

# Con servidor Notary personalizado
./scripts/sign-image.sh \
  --image my-image:latest \
  --notary-server https://notary-server:4443
```

**Características:**
- ✅ Pull y push automático
- ✅ Firma con Notary
- ✅ Extracción automática de digest

### 5. Security Policies

```yaml
# security/security-policy.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: true
```

### 6. Admission Controller

**Script ejecutable:** [`scripts/admission_controller.py`](scripts/admission_controller.py)

Validador de seguridad para pods en Kubernetes admission webhook.

**Cuándo ejecutar:**
- Validación de pods antes de creación
- CI/CD pipelines
- Verificación de compliance de seguridad

**Uso:**
```bash
# Validar pod spec
python scripts/admission_controller.py validate --pod-spec pod.json

# Validar deployment spec
python scripts/admission_controller.py validate --deployment-spec deployment.json
```

**Características:**
- ✅ Validación de privileged containers
- ✅ Validación de root user
- ✅ Validación de resource limits
- ✅ Validación de security contexts
- ✅ Warnings y errors separados

## 🎯 Mejores Prácticas

### 1. Image Security

✅ **DO:**
- Scan all images
- Use minimal base images
- Sign images
- Keep images updated

❌ **DON'T:**
- Use untrusted images
- Ignore vulnerabilities
- Use outdated images

### 2. Runtime Security

✅ **DO:**
- Monitor runtime behavior
- Use security policies
- Limit privileges
- Monitor with Falco

❌ **DON'T:**
- Run as root
- Use privileged containers
- Ignore runtime alerts

### 3. Policies

✅ **DO:**
- Enforce security policies
- Use admission controllers
- Review policies regularly
- Test policies

❌ **DON'T:**
- Allow privileged containers
- Skip policy enforcement
- Ignore violations

## 🚨 Troubleshooting

### Image Scan Failures

1. Check scan configuration
2. Verify image accessibility
3. Review scan results
4. Fix vulnerabilities

### Runtime Alerts

1. Review Falco rules
2. Check container behavior
3. Investigate alerts
4. Adjust rules if needed

## 📚 Recursos Adicionales

- [Falco Documentation](https://falco.org/docs/)
- [Trivy Scanner](https://github.com/aquasecurity/trivy)
- [Container Security Best Practices](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
