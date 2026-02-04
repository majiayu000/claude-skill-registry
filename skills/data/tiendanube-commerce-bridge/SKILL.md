---
name: "TiendaNube Commerce Bridge"
description: "Especialista en integración con Tienda Nube: OAuth, sincronización de catálogo, órdenes y gestión de productos."
trigger: "tiendanube, tienda nube, e-commerce, products, orders, oauth, catalog, store"
scope: "ECOMMERCE"
auto-invoke: true
---

# TiendaNube Commerce Bridge - Platform AI Solutions

## 1. Concepto: E-Commerce Integration

### Filosofía
Tienda Nube es la **fuente de verdad** para:
- **Catálogo de productos** (name, price, stock, variants)
- **Órdenes de cliente** (orders, fulfillment)
- **Información de tienda** (store name, currency, timezone)

### Flujo de Integración
```
Frontend → Redirect to TiendaNube OAuth
    ↓
TiendaNube Authorization
    ↓
Callback with code → Backend Exchange
    ↓
Access Token + User ID → Vault
    ↓
API Calls (Products, Orders)
```

## 2. OAuth Flow (Redirect-Based)

### App Configuration (Partners Dashboard)
```
App Name: Nexus AI Assistant
Redirect URI: https://yourdomain.com/auth/callback
Scopes: read_products, read_orders, write_products
```

### Frontend: Iniciar OAuth
```tsx
const TiendaNubeConnect: React.FC = () => {
  const handleConnect = () => {
    // Obtener tenant_id actual
    const tenantId = localStorage.getItem('tenant_id');
    
    // Construir URL de autorización
    const clientId = import.meta.env.VITE_TIENDANUBE_CLIENT_ID;
    const redirectUri = `${window.location.origin}/auth/callback`;
    
    const authUrl = new URL('https://www.tiendanube.com/apps/authorize/token');
    authUrl.searchParams.set('client_id', clientId);
    authUrl.searchParams.set('redirect_uri', redirectUri);
    authUrl.searchParams.set('state', tenantId);  // Para identificar tenant
    
    // Redirigir a TiendaNube
    window.location.href = authUrl.toString();
  };
  
  return (
    <button onClick={handleConnect} className="tn-connect-btn">
      Conectar Tienda Nube
    </button>
  );
};
```

### Frontend: Callback Handler
```tsx
// Route: /auth/callback
const TiendaNubeCallback: React.FC = () => {
  const [status, setStatus] = useState('processing');
  
  useEffect(() => {
    handleCallback();
  }, []);
  
  const handleCallback = async () => {
    // Extraer parámetros de URL
    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');
    const tenantId = params.get('state');
    
    if (!code) {
      setStatus('error');
      return;
    }
    
    try {
      // Enviar code al backend
      await useApi({
        method: 'POST',
        url: '/auth/tiendanube/exchange',
        data: {
          code,
          tenant_id: tenantId,
          redirect_uri: `${window.location.origin}/auth/callback`
        }
      });
      
      setStatus('success');
      
      // Redirigir a dashboard
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
      
    } catch (error) {
      setStatus('error');
    }
  };
  
  return (
    <div className="callback-handler">
      {status === 'processing' && <p>Conectando con Tienda Nube...</p>}
      {status === 'success' && <p>✅ Conexión exitosa!</p>}
      {status === 'error' && <p>❌ Error en la conexión</p>}
    </div>
  );
};
```

## 3. Backend: Token Exchange

### Exchange Endpoint
```python
# orchestrator_service/app/api/v1/endpoints/auth.py

@router.post("/auth/tiendanube/exchange")
async def exchange_tiendanube_code(
    payload: TiendaNubeExchange,
    session: AsyncSession = Depends(get_session)
):
    """
    Intercambia authorization code por access_token
    """
    # Validar redirect_uri
    if not payload.redirect_uri.startswith(ALLOWED_ORIGINS[0]):
        raise HTTPException(
            status_code=400,
            detail="Invalid redirect_uri"
        )
    
    # Exchange code por token
    response = requests.post(
        "https://www.tiendanube.com/apps/authorize/token",
        data={
            "client_id": TIENDANUBE_CLIENT_ID,
            "client_secret": TIENDANUBE_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": payload.code
        }
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"TiendaNube token exchange failed: {response.text}"
        )
    
    data = response.json()
    access_token = data['access_token']
    user_id = data['user_id']  # Store ID
    
    # Guardar en Vault
    await save_credential(
        tenant_id=payload.tenant_id,
        category="tiendanube",
        name="access_token",
        value=access_token,
        scope="tenant"
    )
    
    await save_credential(
        tenant_id=payload.tenant_id,
        category="tiendanube",
        name="user_id",
        value=str(user_id),
        scope="tenant"
    )
    
    # Actualizar tenant con store info
    await update_tenant_store_info(
        tenant_id=payload.tenant_id,
        user_id=user_id,
        access_token=access_token
    )
    
    return {
        "status": "connected",
        "store_id": user_id
    }
```

## 4. Sincronización de Catálogo

### Obtener Productos
```python
async def get_tiendanube_products(
    tenant_id: int,
    page: int = 1,
    per_page: int = 50
) -> List[dict]:
    """
    Obtiene productos de Tienda Nube
    """
    # Obtener credenciales
    access_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="access_token"
    )
    
    user_id = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="user_id"
    )
    
    if not access_token or not user_id:
        raise HTTPException(
            status_code=400,
            detail="TiendaNube not connected"
        )
    
    # Llamar API
    response = requests.get(
        f"https://api.tiendanube.com/v1/{user_id}/products",
        headers={
            "Authentication": f"bearer {access_token}",
            "User-Agent": "Nexus AI (contact@nexus.com)"
        },
        params={
            "page": page,
            "per_page": per_page,
            "published": "true"  # Solo productos publicados
        }
    )
    
    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="TiendaNube token expired. Reconnect your store."
        )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"TiendaNube API error: {response.text}"
        )
    
    products = response.json()
    
    return products
```

### Endpoint de Productos
```python
# orchestrator_service/app/api/v1/endpoints/products.py

@router.get("/admin/products")
async def list_products(
    current_user = Depends(verify_admin_token),
    page: int = 1,
    per_page: int = 50
):
    tenant_id = await resolve_tenant(current_user.id)
    
    # Obtener de TiendaNube
    products = await get_tiendanube_products(
        tenant_id=tenant_id,
        page=page,
        per_page=per_page
    )
    
    # Normalizar estructura
    normalized = [
        {
            "id": p['id'],
            "name": p['name']['es'],  # o idioma configurado
            "price": p['variants'][0]['price'] if p['variants'] else 0,
            "stock": sum(v.get('stock', 0) for v in p['variants']),
            "image_url": p['images'][0]['src'] if p['images'] else None,
            "category": p.get('categories', [{}])[0].get('name', {}).get('es'),
            "variants": [
                {
                    "id": v['id'],
                    "name": v.get('values', [{}])[0].get('es', 'Default'),
                    "price": v['price'],
                    "stock": v.get('stock', 0)
                }
                for v in p.get('variants', [])
            ]
        }
        for p in products
    ]
    
    return normalized
```

## 5. Búsqueda de Productos (Agent Tool)

### search_products Tool
```python
# agent_service/main.py

from langchain.tools import tool

@tool
async def search_products(
    query: str,
    tenant_id: int,
    category: Optional[str] = None
) -> dict:
    """
    Busca productos en el catálogo de Tienda Nube.
    Usa este tool cuando el usuario pregunte por un producto específico.
    
    Args:
        query: Término de búsqueda (ej: "zapatillas rojas")
        tenant_id: ID del tenant
        category: Filtro opcional de categoría
    
    Returns:
        Lista de productos encontrados con precio y stock
    """
    # Obtener credenciales
    access_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="access_token"
    )
    
    user_id = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="user_id"
    )
    
    # Llamar API de búsqueda
    response = await httpx.get(
        f"https://api.tiendanube.com/v1/{user_id}/products",
        headers={"Authentication": f"bearer {access_token}"},
        params={
            "q": query,
            "per_page": 10,
            "published": "true"
        }
    )
    
    products = response.json()
    
    # Formatear para el agente
    results = []
    for p in products:
        results.append({
            "id": p['id'],
            "name": p['name']['es'],
            "price": f"${p['variants'][0]['price']}",
            "stock": "Disponible" if sum(v.get('stock', 0) for v in p['variants']) > 0 else "Sin stock",
            "url": p['permalink']
        })
    
    return {
        "found": len(results),
        "products": results
    }
```

## 6. Gestión de Órdenes

### Obtener Órdenes
```python
@router.get("/admin/orders")
async def list_orders(
    current_user = Depends(verify_admin_token),
    status: Optional[str] = None,  # 'open', 'closed', 'cancelled'
    page: int = 1
):
    tenant_id = await resolve_tenant(current_user.id)
    
    # Credenciales
    access_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="access_token"
    )
    
    user_id = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="user_id"
    )
    
    # Llamar API
    params = {"page": page, "per_page": 20}
    if status:
        params['status'] = status
    
    response = requests.get(
        f"https://api.tiendanube.com/v1/{user_id}/orders",
        headers={"Authentication": f"bearer {access_token}"},
        params=params
    )
    
    orders = response.json()
    
    # Normalizar
    return [
        {
            "id": o['id'],
            "number": o['number'],
            "status": o['status'],
            "total": o['total'],
            "currency": o['currency'],
            "customer_name": o['customer']['name'],
            "created_at": o['created_at'],
            "products": [
                {
                    "name": item['name'],
                    "quantity": item['quantity'],
                    "price": item['price']
                }
                for item in o['products']
            ]
        }
        for o in orders
    ]
```

## 7. Crear Producto (Write Permission)

### create_product Endpoint
```python
@router.post("/admin/products", status_code=201)
async def create_product(
    payload: ProductCreate,
    current_user = Depends(verify_admin_token)
):
    tenant_id = await resolve_tenant(current_user.id)
    
    # Credenciales
    access_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="access_token"
    )
    
    user_id = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="user_id"
    )
    
    # Construir payload de TiendaNube
    tn_payload = {
        "name": {"es": payload.name},
        "description": {"es": payload.description},
        "published": True,
        "variants": [
            {
                "price": str(payload.price),
                "stock": payload.stock
            }
        ]
    }
    
    # Crear en TiendaNube
    response = requests.post(
        f"https://api.tiendanube.com/v1/{user_id}/products",
        headers={
            "Authentication": f"bearer {access_token}",
            "Content-Type": "application/json"
        },
        json=tn_payload
    )
    
    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to create product: {response.text}"
        )
    
    created_product = response.json()
    
    return {
        "id": created_product['id'],
        "name": created_product['name']['es'],
        "permalink": created_product['permalink']
    }
```

## 8. Webhooks (Opcional)

### Configurar Webhook
```python
async def setup_tiendanube_webhook(
    tenant_id: int,
    event: str  # 'order/created', 'product/updated'
):
    """
    Registra webhook para recibir eventos de TiendaNube
    """
    access_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="access_token"
    )
    
    user_id = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="user_id"
    )
    
    # URL del webhook
    webhook_url = f"{BASE_URL}/webhooks/tiendanube/{tenant_id}"
    
    # Crear webhook
    response = requests.post(
        f"https://api.tiendanube.com/v1/{user_id}/webhooks",
        headers={"Authentication": f"bearer {access_token}"},
        json={
            "url": webhook_url,
            "event": event
        }
    )
    
    return response.json()
```

### Recibir Webhook
```python
@router.post("/webhooks/tiendanube/{tenant_id}")
async def handle_tiendanube_webhook(
    tenant_id: int,
    payload: dict = Body(...)
):
    """
    Procesa eventos de TiendaNube
    """
    event = payload.get('event')
    
    if event == 'order/created':
        # Notificar al equipo
        await notify_new_order(tenant_id, payload['object'])
    
    elif event == 'product/updated':
        # Sincronizar catálogo
        await sync_product(tenant_id, payload['object'])
    
    return {"status": "received"}
```

## 9. Store Information

### Obtener Info de Tienda
```python
@router.get("/admin/store/info")
async def get_store_info(
    current_user = Depends(verify_admin_token)
):
    tenant_id = await resolve_tenant(current_user.id)
    
    access_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="access_token"
    )
    
    user_id = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="user_id"
    )
    
    # Llamar API de Store
    response = requests.get(
        f"https://api.tiendanube.com/v1/{user_id}/store",
        headers={"Authentication": f"bearer {access_token}"}
    )
    
    store = response.json()
    
    return {
        "name": store['name']['es'],
        "url": store['url'],
        "currency": store['currency'],
        "language": store['language'],
        "country": store['country']
    }
```

## 10. Rate Limiting

### TiendaNube Limits
- **2 requests/second** por app
- **10,000 requests/day** por store

### Implementar Throttling
```python
import asyncio
from collections import deque

class TiendaNubeRateLimiter:
    def __init__(self):
        self.requests = deque()
        self.max_per_second = 2
    
    async def wait_if_needed(self):
        now = time.time()
        
        # Limpiar requests antiguos (> 1 segundo)
        while self.requests and self.requests[0] < now - 1:
            self.requests.popleft()
        
        # Si alcanzamos el límite, esperar
        if len(self.requests) >= self.max_per_second:
            sleep_time = 1 - (now - self.requests[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        # Registrar request
        self.requests.append(time.time())

limiter = TiendaNubeRateLimiter()

# Uso
await limiter.wait_if_needed()
response = requests.get(...)
```

## 11. Troubleshooting

### "404 No encontramos lo que estás buscando"
```
Causa: Redirect URI no coincide exactamente
Solución: Verificar en Partners Dashboard → Redirect URI
```

### "401 Unauthorized"
```
Causa: Token expirado o revocado
Solución: Re-autenticar (TiendaNube tokens no expiran, pero pueden ser revocados)
```

### "Products API returns empty"
```
Causa: Tienda no tiene productos publicados
Solución: Verificar en Tienda Nube que productos estén published=true
```

### "Rate limit exceeded"
```
Causa: > 2 req/s
Solución: Implementar rate limiter (ver sección 10)
```

## 12. Checklist de Implementación

### Frontend
- [ ] Botón "Conectar Tienda Nube"
- [ ] Callback handler en /auth/callback
- [ ] Estado de conexión visible
- [ ] Lista de productos con paginación
- [ ] Búsqueda de productos

### Backend
- [ ] OAuth exchange implementado
- [ ] Credenciales guardadas en Vault
- [ ] Endpoint /admin/products
- [ ] Endpoint /admin/orders
- [ ] search_products tool para agentes
- [ ] Rate limiter implementado
- [ ] Error handling (401, 404, 429)

### Configuración
- [ ] TIENDANUBE_CLIENT_ID en .env
- [ ] TIENDANUBE_CLIENT_SECRET en .env
- [ ] Redirect URI configurado en Partners
- [ ] Scopes correctos (read_products, read_orders)

---

**Tip**: Para debugging, usar TiendaNube API Explorer: https://tiendanube.github.io/api-documentation/
