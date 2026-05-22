---
name: service-ingress
description: Kubernetes Service 与 Ingress
version: 1.0.0
author: terminal-skills
tags: [kubernetes, service, ingress, k8s, networking]
---

# Service 与 Ingress

## 概述
服务暴露、Ingress 配置、TLS 终止等技能。

## Service 类型

### ClusterIP（默认）
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 8080
```

### NodePort
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080      # 30000-32767
```

### LoadBalancer
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 8080
```

### ExternalName
```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.example.com
```

### Headless Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: headless-service
spec:
  clusterIP: None
  selector:
    app: nginx
  ports:
  - port: 80
```

## Service 操作

```bash
# 查看 Service
kubectl get svc
kubectl get svc -o wide
kubectl describe svc service-name

# 创建 Service
kubectl expose deploy deployment-name --port=80 --target-port=8080
kubectl expose deploy deployment-name --type=NodePort --port=80

# 删除 Service
kubectl delete svc service-name

# 测试 Service
kubectl run test --rm -it --image=busybox -- wget -qO- http://service-name
```

## Ingress 配置

### 基础 Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

### 多路径 Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-path-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /web
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### 多域名 Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-host-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
  - host: web.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

## TLS 配置

### 创建 TLS Secret
```bash
# 从证书文件创建
kubectl create secret tls tls-secret --cert=cert.pem --key=key.pem

# 查看 Secret
kubectl get secret tls-secret -o yaml
```

### Ingress TLS
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - example.com
    secretName: tls-secret
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

### cert-manager 自动证书
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: auto-tls-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - example.com
    secretName: example-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

## Ingress 注解

### Nginx Ingress 常用注解
```yaml
metadata:
  annotations:
    # 重写路径
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    
    # SSL 重定向
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    
    # 代理超时
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
    
    # 请求体大小
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    
    # 限流
    nginx.ingress.kubernetes.io/limit-rps: "10"
    
    # WebSocket
    nginx.ingress.kubernetes.io/proxy-http-version: "1.1"
    nginx.ingress.kubernetes.io/upstream-hash-by: "$request_uri"
    
    # 跨域
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "*"
```

## Ingress 操作

```bash
# 查看 Ingress
kubectl get ingress
kubectl get ing -o wide
kubectl describe ing ingress-name

# 查看 Ingress Controller
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# 测试 Ingress
curl -H "Host: example.com" http://ingress-ip/
```

## 常见场景

### 场景 1：路径重写
```yaml
# /api/v1/users -> /users
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /api(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### 场景 2：会话保持
```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "route"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
```

### 场景 3：基础认证
```bash
# 创建认证 Secret
htpasswd -c auth admin
kubectl create secret generic basic-auth --from-file=auth
```

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: "Authentication Required"
```

### 场景 4：调试 Service 连通性
```bash
# 检查 Endpoints
kubectl get endpoints service-name

# 测试 Pod 到 Service
kubectl run test --rm -it --image=busybox -- sh
wget -qO- http://service-name:port

# 检查 DNS
kubectl run test --rm -it --image=busybox -- nslookup service-name
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| Service 无法访问 | 检查 Endpoints、Pod 标签 |
| Ingress 404 | 检查路径配置、后端 Service |
| TLS 错误 | 检查证书 Secret、域名匹配 |
| 502 Bad Gateway | 检查后端 Pod 状态、健康检查 |

```bash
# 检查 Service Endpoints
kubectl get endpoints service-name

# 检查 Ingress Controller 日志
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=100

# 测试后端连通性
kubectl port-forward svc/service-name 8080:80
curl localhost:8080
```
