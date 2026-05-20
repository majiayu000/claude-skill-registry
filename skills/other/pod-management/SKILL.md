---
name: pod-management
description: Kubernetes Pod 管理与调试
version: 1.0.0
author: terminal-skills
tags: [kubernetes, pod, k8s, container, debug]
---

# Pod 管理与调试

## 概述
Pod 生命周期管理、日志查看、exec 调试等技能。

## Pod 查看

```bash
# 列出 Pod
kubectl get pods
kubectl get pods -o wide                    # 详细信息
kubectl get pods -A                         # 所有命名空间
kubectl get pods -n namespace
kubectl get pods -l app=nginx               # 按标签过滤
kubectl get pods --field-selector status.phase=Running

# Pod 详情
kubectl describe pod pod-name
kubectl get pod pod-name -o yaml
kubectl get pod pod-name -o jsonpath='{.status.phase}'
```

## 日志查看

```bash
# 查看日志
kubectl logs pod-name
kubectl logs pod-name -c container-name     # 指定容器
kubectl logs pod-name --all-containers      # 所有容器

# 实时跟踪
kubectl logs -f pod-name
kubectl logs -f pod-name --since=1h         # 最近1小时
kubectl logs -f pod-name --tail=100         # 最后100行

# 上一个容器的日志（崩溃后）
kubectl logs pod-name --previous

# 多 Pod 日志
kubectl logs -l app=nginx                   # 按标签
kubectl logs -l app=nginx --max-log-requests=10
```

## 容器调试

### exec 进入容器
```bash
# 进入容器
kubectl exec -it pod-name -- /bin/bash
kubectl exec -it pod-name -- sh
kubectl exec -it pod-name -c container-name -- /bin/bash

# 执行命令
kubectl exec pod-name -- ls -la
kubectl exec pod-name -- cat /etc/hosts
kubectl exec pod-name -- env
```

### 调试容器
```bash
# 使用 debug 容器（K8s 1.18+）
kubectl debug pod-name -it --image=busybox --target=container-name

# 复制 Pod 进行调试
kubectl debug pod-name -it --copy-to=debug-pod --container=debug --image=busybox

# 节点调试
kubectl debug node/node-name -it --image=busybox
```

### 端口转发
```bash
# 转发到本地
kubectl port-forward pod-name 8080:80
kubectl port-forward pod-name 8080:80 --address 0.0.0.0

# 后台运行
kubectl port-forward pod-name 8080:80 &
```

## Pod 生命周期

### 创建 Pod
```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 10
      periodSeconds: 5
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 3
```

```bash
kubectl apply -f pod.yaml
kubectl create -f pod.yaml
```

### 删除 Pod
```bash
kubectl delete pod pod-name
kubectl delete pod pod-name --force --grace-period=0   # 强制删除
kubectl delete pods -l app=nginx                        # 按标签删除
kubectl delete pods --all -n namespace                  # 删除所有
```

### Pod 状态
```bash
# 查看 Pod 状态
kubectl get pod pod-name -o jsonpath='{.status.phase}'

# 等待 Pod 就绪
kubectl wait --for=condition=Ready pod/pod-name --timeout=60s

# 查看事件
kubectl get events --field-selector involvedObject.name=pod-name
```

## 资源管理

### 查看资源使用
```bash
# Pod 资源使用
kubectl top pods
kubectl top pods -n namespace
kubectl top pod pod-name --containers

# 按资源排序
kubectl top pods --sort-by=cpu
kubectl top pods --sort-by=memory
```

### 资源配置
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

## 常见场景

### 场景 1：排查 Pod 启动失败
```bash
# 1. 查看 Pod 状态
kubectl get pod pod-name -o wide

# 2. 查看事件
kubectl describe pod pod-name | grep -A 20 Events

# 3. 查看日志
kubectl logs pod-name
kubectl logs pod-name --previous    # 如果容器重启

# 4. 检查镜像
kubectl get pod pod-name -o jsonpath='{.spec.containers[*].image}'
```

### 场景 2：排查 CrashLoopBackOff
```bash
# 1. 查看退出原因
kubectl describe pod pod-name | grep -A 5 "Last State"

# 2. 查看上一次日志
kubectl logs pod-name --previous

# 3. 检查资源限制
kubectl describe pod pod-name | grep -A 10 "Limits"

# 4. 检查探针配置
kubectl get pod pod-name -o yaml | grep -A 10 "livenessProbe"
```

### 场景 3：临时运行调试 Pod
```bash
# 运行临时 Pod
kubectl run debug --rm -it --image=busybox -- sh
kubectl run debug --rm -it --image=nicolaka/netshoot -- bash

# 在特定节点运行
kubectl run debug --rm -it --image=busybox --overrides='{"spec":{"nodeName":"node-name"}}' -- sh
```

### 场景 4：复制文件
```bash
# 从 Pod 复制到本地
kubectl cp pod-name:/path/to/file ./local-file
kubectl cp namespace/pod-name:/path/to/file ./local-file

# 从本地复制到 Pod
kubectl cp ./local-file pod-name:/path/to/file
```

## 故障排查

| 状态 | 可能原因 | 排查方法 |
|------|----------|----------|
| Pending | 资源不足/调度问题 | `kubectl describe pod` 查看事件 |
| ImagePullBackOff | 镜像拉取失败 | 检查镜像名、仓库认证 |
| CrashLoopBackOff | 应用崩溃 | `kubectl logs --previous` |
| OOMKilled | 内存超限 | 增加 memory limits |
| Evicted | 节点资源不足 | 检查节点资源、清理 Pod |
| Unknown | 节点失联 | 检查节点状态 |
