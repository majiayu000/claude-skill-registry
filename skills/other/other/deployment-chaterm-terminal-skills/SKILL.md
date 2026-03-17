---
name: deployment
description: Kubernetes Deployment 管理
version: 1.0.0
author: terminal-skills
tags: [kubernetes, deployment, k8s, rollout, scaling]
---

# Deployment 管理

## 概述
Deployment 滚动更新、回滚、扩缩容等技能。

## 基础操作

### 查看 Deployment
```bash
# 列出 Deployment
kubectl get deployments
kubectl get deploy -o wide
kubectl get deploy -n namespace

# 详细信息
kubectl describe deploy deployment-name
kubectl get deploy deployment-name -o yaml
```

### 创建 Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

```bash
kubectl apply -f deployment.yaml
kubectl create deployment nginx --image=nginx:1.20 --replicas=3
```

### 删除 Deployment
```bash
kubectl delete deploy deployment-name
kubectl delete -f deployment.yaml
```

## 扩缩容

```bash
# 手动扩缩容
kubectl scale deploy deployment-name --replicas=5

# 自动扩缩容 (HPA)
kubectl autoscale deploy deployment-name --min=2 --max=10 --cpu-percent=80

# 查看 HPA
kubectl get hpa
kubectl describe hpa deployment-name
```

### HPA 配置
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 滚动更新

### 更新策略配置
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%           # 最多超出期望副本数
      maxUnavailable: 25%     # 最多不可用副本数
```

### 执行更新
```bash
# 更新镜像
kubectl set image deploy/deployment-name container-name=nginx:1.21

# 更新环境变量
kubectl set env deploy/deployment-name ENV_VAR=value

# 更新资源限制
kubectl set resources deploy/deployment-name -c container-name --limits=cpu=200m,memory=256Mi

# 应用配置文件更新
kubectl apply -f deployment.yaml

# 记录更新原因
kubectl set image deploy/deployment-name container-name=nginx:1.21 --record
```

### 查看更新状态
```bash
# 查看滚动更新状态
kubectl rollout status deploy/deployment-name

# 查看更新历史
kubectl rollout history deploy/deployment-name
kubectl rollout history deploy/deployment-name --revision=2

# 暂停/恢复更新
kubectl rollout pause deploy/deployment-name
kubectl rollout resume deploy/deployment-name
```

## 回滚

```bash
# 回滚到上一版本
kubectl rollout undo deploy/deployment-name

# 回滚到指定版本
kubectl rollout undo deploy/deployment-name --to-revision=2

# 查看回滚状态
kubectl rollout status deploy/deployment-name
```

## 高级配置

### 健康检查
```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          failureThreshold: 30
          periodSeconds: 10
```

### 亲和性配置
```yaml
spec:
  template:
    spec:
      affinity:
        # Pod 反亲和（分散部署）
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: nginx
              topologyKey: kubernetes.io/hostname
        # 节点亲和
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-type
                operator: In
                values:
                - worker
```

### 容忍度
```yaml
spec:
  template:
    spec:
      tolerations:
      - key: "node-role.kubernetes.io/master"
        operator: "Exists"
        effect: "NoSchedule"
```

## 常见场景

### 场景 1：蓝绿部署
```bash
# 创建新版本 Deployment
kubectl apply -f deployment-v2.yaml

# 切换 Service 到新版本
kubectl patch service my-service -p '{"spec":{"selector":{"version":"v2"}}}'

# 验证后删除旧版本
kubectl delete deploy deployment-v1
```

### 场景 2：金丝雀发布
```yaml
# 创建金丝雀 Deployment（少量副本）
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
      track: canary
  template:
    metadata:
      labels:
        app: nginx
        track: canary
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
```

### 场景 3：批量重启 Pod
```bash
# 触发滚动重启
kubectl rollout restart deploy/deployment-name

# 或添加注解触发更新
kubectl patch deploy deployment-name -p '{"spec":{"template":{"metadata":{"annotations":{"date":"'$(date +%s)'"}}}}}'
```

### 场景 4：查看 Pod 分布
```bash
# 查看 Pod 所在节点
kubectl get pods -l app=nginx -o wide

# 按节点统计
kubectl get pods -l app=nginx -o jsonpath='{range .items[*]}{.spec.nodeName}{"\n"}{end}' | sort | uniq -c
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 更新卡住 | `kubectl rollout status`, 检查 Pod 状态 |
| Pod 无法调度 | `kubectl describe pod`, 检查资源和亲和性 |
| 更新后服务异常 | 检查健康检查配置、回滚 |
| HPA 不生效 | 检查 metrics-server、资源配置 |

```bash
# 查看 Deployment 事件
kubectl describe deploy deployment-name | grep -A 20 Events

# 查看 ReplicaSet
kubectl get rs -l app=nginx
kubectl describe rs rs-name
```
