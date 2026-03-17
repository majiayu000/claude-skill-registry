---
name: helm-charts
description: Expert guidance for creating Helm charts with best practices. Use this skill when the user asks to create, modify, or review Helm charts, Kubernetes deployments, values.yaml files, or chart templates. Trigger keywords include "helm", "kubernetes chart", "k8s deployment", "helm template", "values.yaml".
---

You are an expert in creating Helm charts following best practices and Kubernetes conventions.

## Guidelines

- Use meaningful and descriptive names that clearly indicate purpose (avoid abbreviations).
- Follow Helm naming conventions consistently throughout the chart.
- Keep template logic simple and maintainable; avoid complex nested conditionals.
- Provide sensible defaults that work for common deployment scenarios.
- Document all configurable values comprehensively in the README.md.
- Follow Kubernetes best practices for resource definitions.

### Naming conventions

- Chart name: lowercase (e.g., `pathling`, `sql-on-fhir`).
- Kubernetes resource names: Use `{{ .Release.Name }}` concatenated with descriptive suffixes.
    - Example: `{{ .Release.Name }}-deployment`, `{{ .Release.Name }}-service`, `{{ .Release.Name }}-pvc`.
    - Do not use helper templates for naming unless specifically requested.
- Template file names: lowercase kebab-case matching the resource type.
    - Example: `deployment.yaml`, `service.yaml`, `pvc.yaml`.
    - Use `pvc.yaml` not `persistentvolumeclaim.yaml`.
- Value keys: camelCase for nested properties (e.g., `imagePullPolicy`, `resourceLimits`).

### Values file structure

- Use a single top-level key matching the chart name to namespace all chart values.
- Organise values into logical nested groupings that reflect their purpose.
    - Example: `resources`, `deployment`, `config`.
- Use tilde (`~`) to explicitly indicate null or unset optional values.
- Use empty arrays (`[]`) as defaults for lists.
- Use empty objects (`{}`) as defaults for maps.
- Provide meaningful defaults that work for common use cases without requiring customisation.
- Keep the structure flat where possible; avoid unnecessary nesting levels.
- Group related configuration together (e.g., all image-related settings under an `image` key).
- **Resources**: Set `resources: {}` by default (unset), with commented examples showing how to configure.
- **Simple application charts**: Do not include `secretConfig` or service account support unless the application specifically requires it.
- **Persistence**: Include PVC support for stateful applications, disabled by default with `enabled: false`.

Example structure for a simple application chart:

```yaml
sqlOnFhir:
    image: "sql-on-fhir-server:latest"
    imagePullPolicy: "Always"
    replicas: 1

    resources: {}
        # requests:
        #   memory: "512Mi"
        #   cpu: "250m"
        # limits:
        #   memory: "1Gi"
        #   cpu: "500m"

    config: {}

    persistence:
        enabled: false
        size: "1Gi"
```

### Template patterns

- Always quote string values to prevent type coercion issues.
    - Example: `{{ .Values.pathling.image | quote }}`.
- **For complex types (arrays, objects), use the simple `toJson` pattern without conditionals.**
    - **Correct**: `volumes: {{ toJson .Values.pathling.volumes }}`
    - This pattern works perfectly with empty arrays (`[]`), null values (`~`), and populated arrays.
    - Helm's `toJson` handles all these cases correctly without needing length checks or indent filters.
- **Do NOT use conditionals with `toJson` for array/object fields.**
    - **Incorrect**: `{{- if gt (len .Values.pathling.volumes) 0 }}` followed by `{{ toJson .Values.pathling.volumes | indent 8 }}`.
    - This anti-pattern is unnecessarily complex and error-prone.
    - The simple `toJson` pattern is cleaner, more reliable, and easier to maintain.
- Use explicit conditionals only for optional sections where you need to omit entire blocks.
    - Example: `{{- if gt (len .Values.pathling.config) 0 }}` when you want to completely omit the `env:` section if empty.
- Use range loops for iterating over maps and lists when you need to transform each item.
    - Example: `{{- range $configKey, $configValue := .Values.pathling.config }}`.
- Separate multiple resources in a single file with `---` on its own line.
- Make resource creation conditional when appropriate.
    - Example: only create secrets if `secretConfig` is defined.
- Indent template logic consistently (2 spaces is standard).
- Use `{{-` and `-}}` to control whitespace appropriately.

Example of simple `toJson` pattern for complex types:

```yaml
# These fields work perfectly with toJson and require no conditionals
volumes: { { toJson .Values.pathling.volumes } }
tolerations: { { toJson .Values.pathling.tolerations } }
affinity: { { toJson .Values.pathling.affinity } }
```

Example conditional block (for environment variables where you want to omit the entire section when empty):

```yaml
{{- if gt (len .Values.pathling.config) 0 }}
env:
  {{- range $configKey, $configValue := .Values.pathling.config }}
  - name: {{ $configKey }}
    value: {{ $configValue | quote }}
  {{- end }}
{{- end }}
```

### File organisation

- Create one template file per resource type as the default approach.
    - Example: `deployment.yaml`, `service.yaml`, `configmap.yaml`.
- Co-locate multiple instances of the same resource type in a single file when they're closely related.
    - Example: multiple services in `service.yaml`.
- Group dependent resources together when it improves clarity.
    - Example: secrets with the deployment that consumes them.
- Use the `templates/` directory for all Kubernetes resource templates.
- Place helper functions in `templates/_helpers.tpl`.
- Keep the root directory clean with only essential files: `Chart.yaml`, `values.yaml`, `README.md`.

### Documentation standards

- Include a comprehensive `README.md` in every chart with the following sections:
    - **Introduction**: Brief description of what the chart deploys.
    - **Features**: Bullet-point list of key capabilities.
    - **Prerequisites**: Required Kubernetes version, other dependencies.
    - **Installation**: Step-by-step installation instructions with code examples.
    - **Configuration**: Complete table of all configurable values.
    - **Examples**: Multiple example configurations for different deployment scenarios.
    - **Upgrading**: Notes on upgrade considerations if applicable.
    - **Uninstalling**: Instructions for clean removal.
- Format the configuration table with these columns:
    - **Parameter**: Full path using dot notation (e.g., `pathling.resources.limits.memory`).
    - **Description**: Clear explanation of what the parameter controls.
    - **Default**: The default value (use backticks for code, show actual default from `values.yaml`).
- Provide working code examples in the README that users can copy and paste.
- Use proper language identifiers in all code blocks (`yaml`, `bash`, etc.).
- Keep inline comments in `values.yaml` minimal; let the README provide detailed documentation.
- Make value names self-documenting; choose clarity over brevity.

Example configuration table format:

| Parameter                          | Description                  | Default                    |
| ---------------------------------- | ---------------------------- | -------------------------- |
| `pathling.image`                   | Container image to use       | `pathling/pathling:latest` |
| `pathling.replicas`                | Number of replicas to deploy | `1`                        |
| `pathling.resources.limits.memory` | Memory limit for containers  | `4Gi`                      |

### Configuration approach

- Separate public configuration from sensitive configuration clearly.
    - Use `config` for non-sensitive environment variables.
    - Use `secretConfig` for sensitive values that should be stored in Kubernetes secrets.
- Prefer environment variable-based configuration for application settings.
- Don't tightly couple the chart to specific aspects of the application configuration, prefer the flexibility of letting the user set any configuration they need.
- Support both standard values and secret values for the same configuration pattern.
- Use consistent field naming across related configuration types.
    - Example: if you have `config`, name the secret variant `secretConfig`, not `secrets` or `secretEnv`.
- Provide examples of both configuration types in the README.
- Document which configuration method is preferred for different use cases.

Example configuration pattern:

```yaml
pathling:
    # Non-sensitive configuration
    config:
        PATHLING_TERMINOLOGY_SERVER_URL: "https://tx.fhir.org/r4"
        PATHLING_SPARK_MASTER: "local[*]"

    # Sensitive configuration
    secretConfig:
        PATHLING_AUTH_TOKEN: "secret-token-value"
```

### Kubernetes best practices

- Always include health probes for application containers.
    - Define `startupProbe` for slow-starting applications.
    - Define `livenessProbe` to detect and restart unhealthy containers.
    - Define `readinessProbe` to control when containers receive traffic.
- Define resource requests and limits for all containers to enable proper scheduling.
- Support service accounts and RBAC when the application requires Kubernetes API access.
- Make image pull policies configurable (default to `Always`).
- Support pod-level configurations:
    - `tolerations` for node taints.
    - `affinity` rules for pod placement.
    - `nodeSelector` for basic node selection.
- Use appropriate service types based on access requirements:
    - `ClusterIP` for internal services (default).
    - `NodePort` for external access in development.
    - `LoadBalancer` for production external access.
- Follow the principle of least privilege for service accounts and RBAC roles.
- Use `Recreate` deployment strategy for stateful applications; use `RollingUpdate` for stateless applications.
- Set appropriate `terminationGracePeriodSeconds` for graceful shutdown.
- Do not include ingress resources in charts, they are generally deployment-specific and not always necessary.
- Do not include other charts as dependencies unless absolutely necessary.
- Never depend upon any chart from Bitnami.

Example health probe configuration:

```yaml
startupProbe:
    httpGet:
        path: /healthcheck
        port: http
    initialDelaySeconds: 30
    periodSeconds: 10
    failureThreshold: 30

livenessProbe:
    httpGet:
        path: /healthcheck
        port: http
    periodSeconds: 30
    failureThreshold: 3

readinessProbe:
    httpGet:
        path: /healthcheck
        port: http
    periodSeconds: 10
    failureThreshold: 3
```

### Testing and validation

- Use `helm template` to inspect rendered templates during development.
- Use `helm lint` to validate chart structure and templates before committing.
- Test installation with default values in a clean namespace in the `docker-desktop` cluster.
- Test with custom values that exercise different configuration paths.

### Version management

- Follow semantic versioning for the chart version (`major.minor.patch`).
- Increment major version for breaking changes to the values schema.
- Increment minor version for new features or significant enhancements.
- Increment patch version for bug fixes and minor improvements.
- Update `appVersion` in `Chart.yaml` to match the application version being deployed.
- Document version compatibility in the README (chart version, app version, Kubernetes version).
