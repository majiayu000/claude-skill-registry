---
name: troubleshooting
description: Kubernetes 故障排查
version: 1.0.0
author: terminal-skills
tags: [kubernetes, troubleshooting, k8s, debug, diagnosis]
---

# Kubernetes 故障排查

## 概述
故障诊断、事件分析、资源调试等技能。

## 集群状态检查

### 节点状态
```bash
# 查看节点
kubectl get nodes
kubectl get nodes -o wide

# 节点详情
kubectl describe node node-name

# 节点资源使用
kubectl top nodes

# 节点条件
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Ready")].status}{"\n"}{end}'
```

### 组件状态
```bash
# 查看组件状态
kubectl get componentstatuses
kubectl get cs

# 查看系统 Pod
kubectl get pods -n kube-system

# API Server 健康检查
kubectl get --raw='/healthz'
kubectl get --raw='/readyz'
```

## Pod 故障排查

### Pod 状态分析
```bash
# 查看 Pod 状态
kubectl get pods -o wide
kubectl get pods --field-selector status.phase!=Running

# Pod 详情
kubectl describe pod pod-name

# 查看事件
kubectl get events --sort-by='.lastTimestamp'
kubectl get events --field-selector involvedObject.name=pod-name
```

### 常见 Pod 状态

#### Pending
```bash
# 原因：资源不足、调度问题、PVC 未绑定

# 排查步骤
kubectl describe pod pod-name | grep -A 10 Events
kubectl describe pod pod-name | grep -A 5 "Conditions"

# 检查节点资源
kubectl describe nodes | grep -A 5 "Allocated resources"

# 检查 PVC
kubectl get pvc
kubectl describe pvc pvc-name
```

#### ImagePullBackOff
```bash
# 原因：镜像不存在、认证失败、网络问题

# 排查步骤
kubectl describe pod pod-name | grep -A 5 "Events"

# 检查镜像名
kubectl get pod pod-name -o jsonpath='{.spec.containers[*].image}'

# 检查 imagePullSecrets
kubectl get pod pod-name -o jsonpath='{.spec.imagePullSecrets}'

# 手动拉取测试
docker pull image-name
```

#### CrashLoopBackOff
```bash
# 原因：应用崩溃、配置错误、资源不足

# 查看日志
kubectl logs pod-name
kubectl logs pod-name --previous

# 查看退出码
kubectl describe pod pod-name | grep -A 5 "Last State"

# 检查资源限制
kubectl describe pod pod-name | grep -A 10 "Limits"

# 进入容器调试
kubectl exec -it pod-name -- sh
```

#### OOMKilled
```bash
# 原因：内存超限

# 查看退出原因
kubectl describe pod pod-name | grep -i oom

# 查看资源使用
kubectl top pod pod-name

# 增加内存限制
kubectl set resources deployment/deploy-name --limits=memory=512Mi
```

## 网络故障排查

### Service 连通性
```bash
# 检查 Service
kubectl get svc service-name
kubectl describe svc service-name

# 检查 Endpoints
kubectl get endpoints service-name

# 测试连通性
kubectl run test --rm -it --image=busybox -- sh
wget -qO- http://service-name:port
nslookup service-name
```

### DNS 排查
```bash
# 检查 CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns

# DNS 测试
kubectl run test --rm -it --image=busybox -- nslookup kubernetes
kubectl run test --rm -it --image=busybox -- nslookup service-name.namespace.svc.cluster.local
```

### 网络策略
```bash
# 查看网络策略
kubectl get networkpolicy
kubectl describe networkpolicy policy-name

# 测试网络连通
kubectl run test --rm -it --image=nicolaka/netshoot -- bash
curl -v http://service-name:port
```

## 存储故障排查

### PV/PVC 问题
```bash
# 查看 PV/PVC
kubectl get pv
kubectl get pvc
kubectl describe pvc pvc-name

# 常见问题
# - PVC Pending: 没有匹配的 PV
# - PV Released: 需要手动回收或删除

# 检查 StorageClass
kubectl get storageclass
kubectl describe storageclass sc-name
```

### 挂载问题
```bash
# 查看挂载
kubectl describe pod pod-name | grep -A 10 "Volumes"

# 检查 Pod 内挂载
kubectl exec pod-name -- df -h
kubectl exec pod-name -- ls -la /mount/path
```

## 资源问题排查

### 资源配额
```bash
# 查看配额
kubectl get resourcequota -n namespace
kubectl describe resourcequota quota-name

# 查看 LimitRange
kubectl get limitrange -n namespace
kubectl describe limitrange limit-name
```

### 资源使用
```bash
# Pod 资源使用
kubectl top pods
kubectl top pods --containers

# 节点资源使用
kubectl top nodes

# 资源请求/限制
kubectl describe pod pod-name | grep -A 10 "Requests"
```

## 日志收集

### 容器日志
```bash
# 当前日志
kubectl logs pod-name
kubectl logs pod-name -c container-name

# 历史日志
kubectl logs pod-name --previous

# 实时日志
kubectl logs -f pod-name --since=1h

# 多 Pod 日志
kubectl logs -l app=nginx --all-containers
```

### 系统日志
```bash
# kubelet 日志
journalctl -u kubelet -f

# 容器运行时日志
journalctl -u containerd -f
journalctl -u docker -f

# API Server 日志
kubectl logs -n kube-system kube-apiserver-master
```

## 调试工具

### kubectl debug
```bash
# 调试 Pod
kubectl debug pod-name -it --image=busybox --target=container-name

# 复制 Pod 调试
kubectl debug pod-name -it --copy-to=debug-pod --container=debug --image=nicolaka/netshoot

# 节点调试
kubectl debug node/node-name -it --image=busybox
```

### 临时调试 Pod
```bash
# 网络调试
kubectl run netshoot --rm -it --image=nicolaka/netshoot -- bash

# DNS 调试
kubectl run dnsutils --rm -it --image=gcr.io/kubernetes-e2e-test-images/dnsutils -- sh

# 通用调试
kubectl run debug --rm -it --image=busybox -- sh
```

## 常见场景

### 场景 1：应用无法访问
```bash
# 1. 检查 Pod 状态
kubectl get pods -l app=myapp

# 2. 检查 Service
kubectl get svc myapp-service
kubectl get endpoints myapp-service

# 3. 检查 Ingress
kubectl get ingress
kubectl describe ingress myapp-ingress

# 4. 测试连通性
kubectl run test --rm -it --image=busybox -- wget -qO- http://myapp-service
```

### 场景 2：Pod 调度失败
```bash
# 1. 查看 Pod 事件
kubectl describe pod pod-name | grep -A 20 Events

# 2. 检查节点资源
kubectl describe nodes | grep -A 10 "Allocated resources"

# 3. 检查污点和容忍
kubectl describe nodes | grep Taints
kubectl get pod pod-name -o yaml | grep -A 5 tolerations

# 4. 检查亲和性
kubectl get pod pod-name -o yaml | grep -A 20 affinity
```

### 场景 3：集群证书问题
```bash
# 检查证书过期
kubeadm certs check-expiration

# 更新证书
kubeadm certs renew all

# 检查 API Server 证书
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -dates
```

## 故障排查清单

| 问题类型 | 排查命令 |
|----------|----------|
| Pod 状态 | `kubectl describe pod`, `kubectl logs` |
| 网络问题 | `kubectl get svc/ep`, DNS 测试 |
| 存储问题 | `kubectl get pv/pvc`, `kubectl describe` |
| 资源问题 | `kubectl top`, `kubectl describe quota` |
| 调度问题 | `kubectl describe pod`, 检查节点资源 |
| 认证问题 | 检查 ServiceAccount, RBAC |
