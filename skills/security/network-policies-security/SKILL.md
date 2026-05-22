# 🔐 Skill: Network Policies & Security

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-network-policies-security` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `network-policies`, `network-security`, `kubernetes-networking`, `egress`, `ingress`, `calico`, `cilium` |
| **Referencia** | [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) |

## 🔑 Keywords para Invocación

- `network-policies`
- `network-security`
- `kubernetes-networking`
- `egress`
- `ingress`
- `calico`
- `cilium`
- `@skill:network-policies`

### Ejemplos de Prompts

```
Implementa network policies para Kubernetes security
```

```
Configura egress y ingress policies para microservicios
```

```
Setup Calico network policies y security rules
```

```
@skill:network-policies - Network security completo
```

## 📖 Descripción

Network policies controlan el tráfico de red entre pods en Kubernetes, implementando micro-segmentation y defense-in-depth. Este skill cubre network policies, egress/ingress rules, network security best practices, y herramientas como Calico y Cilium.

### ✅ Cuándo Usar Este Skill

- Kubernetes clusters
- Multi-tenant environments
- Security requirements
- Compliance requirements
- Network segmentation

### ❌ Cuándo NO Usar Este Skill

- Single-node clusters
- Development only
- No security requirements

## 🏗️ Network Security Architecture

```
External Traffic
    ↓
Ingress Controller
    ↓
Network Policy (Ingress)
    ↓
Pod
    ↓
Network Policy (Egress)
    ↓
External/Internal Services
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - **Network Policy Manager:** [`scripts/network_policy_manager.py`](scripts/network_policy_manager.py) - Gestión de network policies (Python CLI)
> 
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso completa.

### 1. Basic Network Policies

```yaml
# network-policies/default-deny-all.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  # No rules = deny all traffic
```

```yaml
# network-policies/allow-internal.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-internal
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: production
    - podSelector: {}  # Allow from pods in same namespace
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: production
  - to: []  # Allow all egress (adjust as needed)
    ports:
    - protocol: TCP
      port: 53  # DNS
    - protocol: UDP
      port: 53  # DNS
```

### 2. Service-Specific Policies

```yaml
# network-policies/user-service-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: user-service-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: user-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Allow from frontend
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 3000
  # Allow from API Gateway
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 3000
  egress:
  # Allow to database
  - to:
    - podSelector:
        matchLabels:
          app: postgresql
    ports:
    - protocol: TCP
      port: 5432
  # Allow DNS
  - to: []
    ports:
    - protocol: UDP
      port: 53
  # Allow to external APIs (controlled)
  - to: []
    ports:
    - protocol: TCP
      port: 443
```

### 3. Database Network Policy

```yaml
# network-policies/database-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: postgresql
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Only allow from application services
  - from:
    - podSelector:
        matchLabels:
          app: user-service
    ports:
    - protocol: TCP
      port: 5432
  - from:
    - podSelector:
        matchLabels:
          app: payment-service
    ports:
    - protocol: TCP
      port: 5432
  egress:
  # Allow DNS only
  - to: []
    ports:
    - protocol: UDP
      port: 53
```

### 4. Egress Policies

```yaml
# network-policies/egress-external.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-apis
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: payment-service
  policyTypes:
  - Egress
  egress:
  # Allow to specific external APIs
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
  # Specific external IPs
  - to:
    - ipBlock:
        cidr: 52.84.0.0/15  # Example external API range
    ports:
    - protocol: TCP
      port: 443
```

### 5. Calico Network Policies

```yaml
# calico/advanced-policy.yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: advanced-policy
  namespace: production
spec:
  selector: app == 'user-service'
  types:
  - Ingress
  - Egress
  ingress:
  - action: Allow
    source:
      namespaceSelector: name == 'production'
      podSelector: app == 'frontend'
    destination:
      ports:
      - 3000
  - action: Deny
    source: {}
  egress:
  - action: Allow
    destination:
      namespaceSelector: name == 'production'
      podSelector: app == 'postgresql'
      ports:
      - 5432
  - action: Log
    destination:
      nets:
      - 0.0.0.0/0
      notNets:
      - 10.0.0.0/8  # Log external traffic
```

### 6. Network Policy Management

**Script ejecutable:** [`scripts/network_policy_manager.py`](scripts/network_policy_manager.py)

Gestor de network policies para Kubernetes con validación y aplicación automática.

**Cuándo ejecutar:**
- Creación de network policies
- Aplicación de políticas por defecto
- Validación de políticas
- Gestión programática de políticas

**Uso:**
```bash
# Listar policies
python scripts/network_policy_manager.py list --namespace production

# Crear policy
python scripts/network_policy_manager.py create \
  --namespace production \
  --policy policy.json

# Aplicar default deny-all
python scripts/network_policy_manager.py apply-default --namespace production

# Validar policy
python scripts/network_policy_manager.py validate --policy policy.json
```

**Características:**
- ✅ Creación de network policies
- ✅ Listado de políticas existentes
- ✅ Validación de configuración
- ✅ Aplicación de políticas por defecto

## 🎯 Mejores Prácticas

### 1. Policy Design

✅ **DO:**
- Start with deny-all
- Allow explicitly
- Use labels consistently
- Test policies

❌ **DON'T:**
- Allow all by default
- Use IPs instead of labels
- Skip testing

### 2. Segmentation

✅ **DO:**
- Segment by namespace
- Segment by service
- Limit egress
- Monitor policy effects

❌ **DON'T:**
- Allow all egress
- Ignore namespace boundaries
- Skip monitoring

### 3. Maintenance

✅ **DO:**
- Document policies
- Review regularly
- Update with services
- Test changes

❌ **DON'T:**
- Set and forget
- Ignore policy updates
- Skip documentation

## 🚨 Troubleshooting

### Connectivity Issues

1. Check network policies
2. Verify pod labels
3. Check namespace labels
4. Test with policy disabled

### Policy Not Applied

1. Verify CNI supports policies
2. Check policy syntax
3. Review pod selectors
4. Check namespace labels

## 📚 Recursos Adicionales

- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Calico Documentation](https://docs.projectcalico.org/)
- [Cilium Documentation](https://docs.cilium.io/)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

