---
name: helm
description: Helm 包管理
version: 1.0.0
author: terminal-skills
tags: [kubernetes, helm, k8s, package, chart]
---

# Helm 包管理

## 概述
Helm Chart 开发、仓库管理、版本升级等技能。

## 基础命令

### 仓库管理
```bash
# 添加仓库
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add stable https://charts.helm.sh/stable

# 更新仓库
helm repo update

# 列出仓库
helm repo list

# 搜索 Chart
helm search repo nginx
helm search hub nginx               # 搜索 Artifact Hub

# 删除仓库
helm repo remove bitnami
```

### 安装与卸载
```bash
# 安装 Chart
helm install my-release bitnami/nginx
helm install my-release bitnami/nginx -n namespace --create-namespace

# 指定 values
helm install my-release bitnami/nginx -f values.yaml
helm install my-release bitnami/nginx --set replicaCount=3

# 模拟安装（不实际执行）
helm install my-release bitnami/nginx --dry-run

# 生成模板
helm template my-release bitnami/nginx

# 卸载
helm uninstall my-release
helm uninstall my-release -n namespace
```

### 查看与管理
```bash
# 列出已安装的 Release
helm list
helm list -A                        # 所有命名空间
helm list -n namespace

# 查看 Release 状态
helm status my-release

# 查看 Release 历史
helm history my-release

# 获取 Release 的 values
helm get values my-release
helm get values my-release --all    # 包含默认值

# 获取 Release 的 manifest
helm get manifest my-release

# 获取 Release 的 notes
helm get notes my-release
```

## 升级与回滚

```bash
# 升级 Release
helm upgrade my-release bitnami/nginx
helm upgrade my-release bitnami/nginx -f values.yaml
helm upgrade my-release bitnami/nginx --set replicaCount=5

# 安装或升级
helm upgrade --install my-release bitnami/nginx

# 回滚
helm rollback my-release            # 回滚到上一版本
helm rollback my-release 2          # 回滚到指定版本

# 查看历史
helm history my-release
```

## Chart 开发

### 创建 Chart
```bash
# 创建新 Chart
helm create mychart

# Chart 目录结构
mychart/
├── Chart.yaml          # Chart 元数据
├── values.yaml         # 默认配置值
├── charts/             # 依赖 Chart
├── templates/          # 模板文件
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl    # 模板助手
│   ├── NOTES.txt       # 安装说明
│   └── tests/
└── .helmignore
```

### Chart.yaml
```yaml
apiVersion: v2
name: mychart
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
keywords:
  - app
  - web
maintainers:
  - name: Your Name
    email: your@email.com
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

### values.yaml
```yaml
replicaCount: 1

image:
  repository: nginx
  tag: "latest"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: nginx
  hosts:
    - host: example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

postgresql:
  enabled: true
```

### 模板语法
```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: 80
        {{- if .Values.resources }}
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        {{- end }}
```

### 模板助手
```yaml
# templates/_helpers.tpl
{{- define "mychart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## Chart 打包与发布

```bash
# 验证 Chart
helm lint mychart/

# 打包 Chart
helm package mychart/

# 生成索引
helm repo index . --url https://example.com/charts

# 推送到 OCI 仓库
helm push mychart-0.1.0.tgz oci://registry.example.com/charts
```

## 依赖管理

```bash
# 更新依赖
helm dependency update mychart/

# 构建依赖
helm dependency build mychart/

# 列出依赖
helm dependency list mychart/
```

## 常见场景

### 场景 1：多环境部署
```bash
# 不同环境的 values 文件
helm upgrade --install my-release ./mychart \
  -f values.yaml \
  -f values-prod.yaml \
  -n production
```

### 场景 2：条件渲染
```yaml
# templates/ingress.yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  # ...
{{- end }}
```

### 场景 3：循环渲染
```yaml
{{- range .Values.ingress.hosts }}
- host: {{ .host | quote }}
  http:
    paths:
    {{- range .paths }}
    - path: {{ .path }}
      pathType: {{ .pathType }}
      backend:
        service:
          name: {{ include "mychart.fullname" $ }}
          port:
            number: {{ $.Values.service.port }}
    {{- end }}
{{- end }}
```

### 场景 4：调试模板
```bash
# 渲染模板但不安装
helm template my-release ./mychart -f values.yaml

# 调试特定模板
helm template my-release ./mychart --show-only templates/deployment.yaml

# 使用 --debug 查看详细信息
helm install my-release ./mychart --dry-run --debug
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 模板渲染错误 | `helm template --debug` |
| 安装失败 | `helm status`, `kubectl describe` |
| 升级失败 | `helm history`, `helm rollback` |
| 依赖问题 | `helm dependency update` |

```bash
# 查看渲染后的 manifest
helm get manifest my-release

# 查看安装 hooks
helm get hooks my-release

# 强制替换资源
helm upgrade my-release ./mychart --force
```
