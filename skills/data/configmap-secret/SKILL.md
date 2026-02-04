---
name: configmap-secret
description: Kubernetes ConfigMap 与 Secret
version: 1.0.0
author: terminal-skills
tags: [kubernetes, configmap, secret, k8s, configuration]
---

# ConfigMap 与 Secret

## 概述
配置管理、敏感信息处理等技能。

## ConfigMap

### 创建 ConfigMap

```bash
# 从字面值创建
kubectl create configmap my-config --from-literal=key1=value1 --from-literal=key2=value2

# 从文件创建
kubectl create configmap my-config --from-file=config.properties
kubectl create configmap my-config --from-file=my-key=config.properties

# 从目录创建
kubectl create configmap my-config --from-file=config-dir/

# 从环境文件创建
kubectl create configmap my-config --from-env-file=env.properties
```

### ConfigMap YAML
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  # 简单键值对
  database_url: "mysql://localhost:3306/mydb"
  log_level: "info"
  
  # 多行配置文件
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        location / {
            root /usr/share/nginx/html;
        }
    }
  
  # JSON 配置
  config.json: |
    {
      "debug": true,
      "port": 8080
    }
```

### 使用 ConfigMap

#### 环境变量方式
```yaml
spec:
  containers:
  - name: app
    env:
    # 单个键
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: my-config
          key: database_url
    # 所有键
    envFrom:
    - configMapRef:
        name: my-config
```

#### 挂载为文件
```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: my-config
      # 可选：指定特定键
      items:
      - key: nginx.conf
        path: nginx.conf
```

#### 挂载为单个文件（不覆盖目录）
```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: config-volume
      mountPath: /etc/app/config.json
      subPath: config.json
  volumes:
  - name: config-volume
    configMap:
      name: my-config
```

## Secret

### 创建 Secret

```bash
# 从字面值创建
kubectl create secret generic my-secret --from-literal=username=admin --from-literal=password=secret123

# 从文件创建
kubectl create secret generic my-secret --from-file=ssh-privatekey=~/.ssh/id_rsa

# TLS Secret
kubectl create secret tls tls-secret --cert=cert.pem --key=key.pem

# Docker Registry Secret
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=password \
  --docker-email=user@example.com
```

### Secret YAML
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  # Base64 编码
  username: YWRtaW4=
  password: c2VjcmV0MTIz
---
# 使用 stringData（自动编码）
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
stringData:
  username: admin
  password: secret123
```

### Secret 类型
```yaml
# Opaque（默认）
type: Opaque

# TLS
type: kubernetes.io/tls
data:
  tls.crt: <base64>
  tls.key: <base64>

# Docker Registry
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64>

# Basic Auth
type: kubernetes.io/basic-auth
data:
  username: <base64>
  password: <base64>

# SSH Auth
type: kubernetes.io/ssh-auth
data:
  ssh-privatekey: <base64>
```

### 使用 Secret

#### 环境变量方式
```yaml
spec:
  containers:
  - name: app
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: my-secret
          key: password
    envFrom:
    - secretRef:
        name: my-secret
```

#### 挂载为文件
```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: my-secret
      defaultMode: 0400
```

#### 镜像拉取凭证
```yaml
spec:
  imagePullSecrets:
  - name: regcred
  containers:
  - name: app
    image: registry.example.com/myapp:latest
```

## 操作命令

```bash
# 查看 ConfigMap
kubectl get configmap
kubectl describe configmap my-config
kubectl get configmap my-config -o yaml

# 查看 Secret
kubectl get secret
kubectl describe secret my-secret
kubectl get secret my-secret -o yaml

# 解码 Secret
kubectl get secret my-secret -o jsonpath='{.data.password}' | base64 -d

# 编辑
kubectl edit configmap my-config
kubectl edit secret my-secret

# 删除
kubectl delete configmap my-config
kubectl delete secret my-secret
```

## 常见场景

### 场景 1：应用配置热更新
```yaml
# 使用 ConfigMap 挂载（自动更新）
spec:
  containers:
  - name: app
    volumeMounts:
    - name: config
      mountPath: /etc/config
  volumes:
  - name: config
    configMap:
      name: my-config
# 注意：subPath 挂载不会自动更新
```

### 场景 2：多环境配置
```bash
# 创建不同环境的 ConfigMap
kubectl create configmap app-config-dev --from-file=config-dev/
kubectl create configmap app-config-prod --from-file=config-prod/

# 在 Deployment 中引用
# 通过 Kustomize 或 Helm 管理不同环境
```

### 场景 3：外部 Secret 管理
```yaml
# 使用 External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: my-external-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: my-secret
  data:
  - secretKey: password
    remoteRef:
      key: prod/db/password
```

### 场景 4：配置文件模板
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  application.yaml: |
    server:
      port: ${SERVER_PORT:8080}
    database:
      url: ${DATABASE_URL}
      username: ${DATABASE_USER}
```

## 最佳实践

```bash
# 1. 不要在 Git 中存储 Secret
# 使用 Sealed Secrets 或 External Secrets

# 2. 限制 Secret 访问权限
# 使用 RBAC 控制

# 3. 定期轮换 Secret
# 使用自动化工具

# 4. 使用 immutable ConfigMap/Secret（K8s 1.21+）
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: immutable-config
immutable: true
data:
  key: value
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 配置未更新 | 检查是否使用 subPath、重启 Pod |
| Secret 解码错误 | 检查 Base64 编码是否正确 |
| 权限问题 | 检查 defaultMode、RBAC |
| 挂载失败 | 检查 ConfigMap/Secret 是否存在 |

```bash
# 检查挂载
kubectl exec pod-name -- ls -la /etc/config
kubectl exec pod-name -- cat /etc/config/key

# 检查环境变量
kubectl exec pod-name -- env | grep KEY
```
