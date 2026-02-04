---
name: kubectl-basics
description: kubectl 基础操作与常用命令
version: 1.0.0
author: terminal-skills
tags: [kubernetes, kubectl, k8s, container]
---

# kubectl 基础操作

## 概述
kubectl 是 Kubernetes 的命令行工具，用于与集群进行交互。本 skill 涵盖日常运维中最常用的命令。

## 集群信息

```bash
# 集群信息
kubectl cluster-info
kubectl version

# 节点信息
kubectl get nodes
kubectl describe node <node-name>

# 上下文切换
kubectl config get-contexts
kubectl config use-context <context-name>
```

## 资源查看

### 常用资源
```bash
# Pod
kubectl get pods
kubectl get pods -o wide
kubectl get pods -A                    # 所有命名空间

# Deployment
kubectl get deployments
kubectl get deploy -o yaml

# Service
kubectl get services
kubectl get svc

# 所有资源
kubectl get all
kubectl get all -n <namespace>
```

### 输出格式
```bash
kubectl get pods -o wide               # 详细信息
kubectl get pods -o yaml               # YAML 格式
kubectl get pods -o json               # JSON 格式
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
```

## 资源操作

### 创建与删除
```bash
# 从文件创建
kubectl apply -f manifest.yaml
kubectl create -f manifest.yaml

# 删除资源
kubectl delete -f manifest.yaml
kubectl delete pod <pod-name>
kubectl delete pod <pod-name> --force --grace-period=0
```

### 编辑与更新
```bash
# 编辑资源
kubectl edit deployment <name>

# 打补丁
kubectl patch deployment <name> -p '{"spec":{"replicas":3}}'

# 扩缩容
kubectl scale deployment <name> --replicas=5
```

## Pod 调试

```bash
# 查看日志
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container>
kubectl logs <pod-name> -f              # 实时跟踪
kubectl logs <pod-name> --previous      # 上一个容器

# 进入容器
kubectl exec -it <pod-name> -- /bin/bash
kubectl exec -it <pod-name> -c <container> -- sh

# 端口转发
kubectl port-forward <pod-name> 8080:80
kubectl port-forward svc/<service> 8080:80
```

## 常见场景

### 场景 1：快速排查 Pod 问题
```bash
# 1. 查看 Pod 状态
kubectl get pod <name> -o wide

# 2. 查看事件
kubectl describe pod <name> | grep -A 20 Events

# 3. 查看日志
kubectl logs <name> --tail=100
```

### 场景 2：滚动更新
```bash
# 更新镜像
kubectl set image deployment/<name> container=image:tag

# 查看更新状态
kubectl rollout status deployment/<name>

# 回滚
kubectl rollout undo deployment/<name>
kubectl rollout history deployment/<name>
```

## 快捷别名

```bash
# 推荐添加到 ~/.bashrc 或 ~/.zshrc
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgd='kubectl get deploy'
alias kd='kubectl describe'
alias kl='kubectl logs'
alias ke='kubectl exec -it'
```

## 故障排查

| 状态 | 可能原因 | 排查命令 |
|------|----------|----------|
| Pending | 资源不足/调度问题 | `kubectl describe pod` |
| CrashLoopBackOff | 应用崩溃 | `kubectl logs --previous` |
| ImagePullBackOff | 镜像拉取失败 | `kubectl describe pod` |
| OOMKilled | 内存超限 | 检查 resources.limits |
