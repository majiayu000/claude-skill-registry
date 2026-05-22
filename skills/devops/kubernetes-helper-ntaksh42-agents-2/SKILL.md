---
name: kubernetes-helper
description: Generate and manage Kubernetes manifests including deployments, services, and ingress. Use when deploying applications to Kubernetes or managing k8s resources.
---

# Kubernetes Helper Skill

Kubernetesマニフェストとコマンドを生成するスキルです。

## 概要

Deployment、Service、ConfigMap等のマニフェストを自動生成します。

## 主な機能

- **マニフェスト生成**: Deployment、Service、Ingress等
- **ベストプラクティス**: リソース制限、ヘルスチェック
- **Helm Charts**: チャート生成
- **トラブルシューティング**: よくある問題の解決

## 生成例

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  app.conf: |
    server {
      listen 80;
      server_name example.com;
    }
  database.yml: |
    production:
      adapter: postgresql
      database: myapp
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  database-url: postgresql://user:pass@host:5432/db
  api-key: sk_live_abc123
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
spec:
  tls:
  - hosts:
    - example.com
    secretName: myapp-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

## よく使うコマンド

```bash
# Podの確認
kubectl get pods

# ログ確認
kubectl logs <pod-name>

# Podに入る
kubectl exec -it <pod-name> -- /bin/sh

# マニフェスト適用
kubectl apply -f deployment.yaml

# リソース削除
kubectl delete -f deployment.yaml

# スケーリング
kubectl scale deployment myapp --replicas=5
```

## バージョン情報

- スキルバージョン: 1.0.0
