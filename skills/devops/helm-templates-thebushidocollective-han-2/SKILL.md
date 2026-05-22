---
name: helm-templates
description: Use when working with Helm templates and template functions for generating Kubernetes manifests dynamically.
allowed-tools: []
---

# Helm Templates

Working with Helm templates and template functions.

## Basic Templating

### Values Access

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: {{ .Values.name }}
  namespace: {{ .Release.Namespace }}
spec:
  containers:
  - name: {{ .Chart.Name }}
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
```

### Built-in Objects

- `.Values`: Values from values.yaml and overrides
- `.Release`: Release information (Name, Namespace, IsUpgrade, IsInstall)
- `.Chart`: Chart metadata from Chart.yaml
- `.Files`: Access non-template files in chart
- `.Capabilities`: Kubernetes cluster capabilities
- `.Template`: Current template information

## Template Functions

### String Functions

```yaml
# upper, lower, title
name: {{ .Values.name | upper }}

# quote
value: {{ .Values.password | quote }}

# trimSuffix, trimPrefix
image: {{ .Values.image | trimSuffix ":latest" }}

# replace
url: {{ .Values.url | replace "http" "https" }}
```

### Default Values

```yaml
# default function
port: {{ .Values.port | default 8080 }}
tag: {{ .Values.image.tag | default .Chart.AppVersion }}

# required function
database: {{ required "database.host is required" .Values.database.host }}
```

### Type Conversion

```yaml
# toString, toJson, toYaml
replicas: {{ .Values.replicas | toString }}

annotations:
{{ toYaml .Values.annotations | indent 2 }}

config: |
{{ toJson .Values.config | indent 2 }}
```

### Conditionals

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}
spec:
  # ...
{{- end }}

{{- if and .Values.persistence.enabled .Values.persistence.existingClaim }}
# Use existing claim
{{- else if .Values.persistence.enabled }}
# Create new claim
{{- end }}
```

### Loops

```yaml
{{- range .Values.environments }}
- name: {{ .name }}
  value: {{ .value | quote }}
{{- end }}

{{- range $key, $value := .Values.config }}
{{ $key }}: {{ $value | quote }}
{{- end }}
```

## Named Templates (_helpers.tpl)

### Define Templates

```yaml
{{/*
Common labels
*/}}
{{- define "mychart.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### Use Templates

```yaml
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
```

## Flow Control

### With

```yaml
{{- with .Values.service }}
apiVersion: v1
kind: Service
metadata:
  name: {{ .name }}
spec:
  type: {{ .type }}
  ports:
  - port: {{ .port }}
{{- end }}
```

### Range with Index

```yaml
{{- range $index, $value := .Values.items }}
item-{{ $index }}: {{ $value }}
{{- end }}
```

## Whitespace Control

```yaml
# Remove leading whitespace
{{- .Values.name }}

# Remove trailing whitespace
{{ .Values.name -}}

# Remove both
{{- .Values.name -}}
```

## Files Access

### Read Files

```yaml
config: |
{{ .Files.Get "config/app.conf" | indent 2 }}
```

### Glob Files

```yaml
{{- range $path, $content := .Files.Glob "config/*.yaml" }}
{{ $path }}: |
{{ $content | indent 2 }}
{{- end }}
```

## Advanced Functions

### Ternary

```yaml
environment: {{ ternary "production" "development" .Values.production }}
```

### Coalesce

```yaml
# Returns first non-empty value
port: {{ coalesce .Values.service.port .Values.port 8080 }}
```

### List Functions

```yaml
# list, append, prepend, concat
args:
{{- range list "arg1" "arg2" "arg3" }}
  - {{ . }}
{{- end }}
```

### Dict Functions

```yaml
# dict, set, unset, hasKey
{{- $config := dict "key1" "value1" "key2" "value2" }}
{{- if hasKey $config "key1" }}
found: true
{{- end }}
```

## Debugging

```yaml
# Print debug info
{{ printf "%#v" .Values | indent 2 }}

# Fail on purpose to see values
{{ fail (printf "Debug: %#v" .Values) }}
```

## Best Practices

### Use Helpers for Repeated Logic

```yaml
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
```

### Validate Input

```yaml
{{- if not (has .Values.service.type (list "ClusterIP" "NodePort" "LoadBalancer")) }}
{{- fail "service.type must be ClusterIP, NodePort, or LoadBalancer" }}
{{- end }}
```

### Quote String Values

```yaml
# Always quote strings
value: {{ .Values.string | quote }}
```
