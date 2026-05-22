---
name: istio
description: Service mesh installation and configuration examples with authorization policies and traffic routing.
---

# istio

```bash
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.26.3
export PATH=$PWD/bin:$PATH
istioctl version
istioctl install --set profile=ambient --skip-confirmation

```

### example
```bash

kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/bookinfo/platform/kube/bookinfo.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/bookinfo/platform/kube/bookinfo-versions.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/bookinfo/gateway-api/bookinfo-gateway.yaml
kubectl annotate gateway bookinfo-gateway networking.istio.io/service-type=ClusterIP --namespace=default
kubectl get gateway
kubectl port-forward svc/bookinfo-gateway-istio 8080:80
kubectl label namespace default istio.io/dataplane-mode=ambient
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/addons/kiali.yaml
istioctl dashboard kiali
for i in $(seq 1 100); do curl -sSI -o /dev/null http://localhost:8080/productpage; done

kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-ztunnel
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
EOF
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.26/samples/curl/curl.yaml
kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage"
istioctl waypoint apply --enroll-namespace --wait
kubectl get gtw waypoint
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-waypoint
  namespace: default
spec:
  targetRefs:
  - kind: Service
    group: ""
    name: productpage
    port: 9080
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/curl
    to:
    - operation:
        methods: ["GET"]
EOF
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-ztunnel
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
        - cluster.local/ns/default/sa/waypoint
EOF
# This fails with an RBAC error because you're not using a GET operation
kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage" -X DELETE
# This fails with an RBAC error because the identity of the reviews-v1 service is not allowed
kubectl exec deploy/reviews-v1 -- curl -s http://productpage:9080/productpage
# This works as you're explicitly allowing GET requests from the curl pod
kubectl exec deploy/curl -- curl -s http://productpage:9080/productpage | grep -o "<title>.*</title>"

kubectl apply -f - <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: reviews
spec:
  parentRefs:
  - group: ""
    kind: Service
    name: reviews
    port: 9080
  rules:
  - backendRefs:
    - name: reviews-v1
      port: 9080
      weight: 90
    - name: reviews-v2
      port: 9080
      weight: 10
    - name: reviews-v2
      port: 9080
      weight: 10
EOF
kubectl exec deploy/curl -- sh -c "for i in \$(seq 1 100); do curl -s http://productpage:9080/productpage | grep reviews-v.-; done"

```