---
name: "Magic Onboarding Orchestrator"
description: "Especialista en el proceso 'Hacer Magia': orquestación de agentes IA, SSE streaming y generación de assets de negocio."
trigger: "magia, magic, onboarding, hacer magia, wizard, sse, stream, assets, branding"
scope: "MAGIC"
auto-invoke: true
---

# Magic Onboarding Orchestrator - Platform AI Solutions

## 1. Concepto: "Hacer Magia" (The Ignition)

### Filosofía
**"Hacer Magia"** es el proceso de **Onboarding Automatizado** que transforma una tienda conectada en una operación lista para vender en minutos.

### Lo que hace:
1. **Analiza catálogo** de Tienda Nube
2. **Extrae Brand DNA** (misión, visión, tono)
3. **Vectoriza conocimiento** para RAG
4. **Genera scripts de venta** (AIDA, PAS)
5. **Calcula proyecciones ROI**
6. **Crea visuales publicitarios** (Google Imagen 3)

### Arquitectura
```
Frontend (MagicOnboarding.tsx)
    ↓
POST /admin/onboarding/magic → Background Task (202 Accepted)
    ↓
SSE Stream (/engine/stream/v2/{tenant_id})
    ↓
Orchestrator → 7 Agent Pipeline
    ↓
Business Assets (DB) + RAG Vectors (Supabase)
```

## 2. Los 7 Agentes Especializados

### Protocolo Omega (Sequential Pipeline)

```python
# agent_service/app/core/magic_orchestrator.py

MAGIC_PIPELINE = [
    {
        "name": "Catalog Analyzer",
        "role": "Analizar productos y categorías",
        "output": "product_catalog.json"
    },
    {
        "name": "Brand DNA Extractor",
        "role": "Identificar identidad de marca",
        "output": "branding.json"
    },
    {
        "name": "Knowledge Vectorizer",
        "role": "Crear embeddings para RAG",
        "output": "rag_vectors (Supabase)"
    },
    {
        "name": "Sales Script Generator",
        "role": "Crear copys de venta (AIDA, PAS)",
        "output": "scripts.json"
    },
    {
        "name": "ROI Projector",
        "role": "Proyecciones financieras",
        "output": "roi.json"
    },
    {
        "name": "Visual Artist",
        "role": "Generar imágenes publicitarias",
        "output": "visuals.json"
    },
    {
        "name": "Compliance Guardian",
        "role": "Validar coherencia y legalidad",
        "output": "validation_report.json"
    }
]
```

## 3. Frontend: Iniciar Magia

### MagicOnboarding Component
```tsx
const MagicOnboarding: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [progress, setProgress] = useState(0);
  
  const handleIgnite = async () => {
    setLoading(true);
    
    // Iniciar proceso (background task)
    const response = await useApi({
      method: 'POST',
      url: '/admin/onboarding/magic',
      data: {
        mode: 'full',  // 'full', 'catalog_only', 'branding_only'
        options: {
          generate_visuals: true,
          vectorize_catalog: true
        }
      }
    });
    
    if (response.status === 'started') {
      // Conectar a SSE stream
      listenToStream(response.tenant_id);
    }
  };
  
  const listenToStream = (tenantId: number) => {
    const eventSource = new EventSource(
      `/api/admin/engine/stream/v2/${tenantId}`
    );
    
    eventSource.addEventListener('log', (e) => {
      const data = JSON.parse(e.data);
      setLogs(prev => [...prev, data.message]);
    });
    
    eventSource.addEventListener('progress', (e) => {
      const data = JSON.parse(e.data);
      setProgress(data.percentage);
    });
    
    eventSource.addEventListener('asset_generated', (e) => {
      const data = JSON.parse(e.data);
      console.log('Asset generated:', data.type, data.id);
    });
    
    eventSource.addEventListener('done', (e) => {
      eventSource.close();
      setLoading(false);
      // Redirigir a Business Forge
      navigate('/forge');
    });
    
    eventSource.addEventListener('error', (e) => {
      console.error('SSE Error:', e);
      eventSource.close();
      setLoading(false);
    });
  };
  
  return (
    <div className="magic-container">
      <button
        onClick={handleIgnite}
        disabled={loading}
        className="ignite-button"
      >
        {loading ? 'Creando Magia...' : 'Hacer Magia ✨'}
      </button>
      
      {/* Progress bar */}
      <div className="progress-bar">
        <div style={{ width: `${progress}%` }} />
      </div>
      
      {/* Live logs */}
      <div className="log-console">
        {logs.map((log, i) => (
          <div key={i}>{log}</div>
        ))}
      </div>
    </div>
  );
};
```

## 4. Backend: Orchestrator

### Endpoint de Inicio
```python
# orchestrator_service/app/api/v1/endpoints/magic.py

@router.post("/onboarding/magic", status_code=202)
async def start_magic_onboarding(
    payload: MagicOnboardingRequest,
    current_user = Depends(verify_admin_token),
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
    """
    Inicia el proceso de Hacer Magia en background
    """
    tenant_id = await resolve_tenant(current_user.id)
    
    # Validar credenciales necesarias
    await validate_prerequisites(tenant_id, session)
    
    # Crear task en background
    background_tasks.add_task(
        execute_magic_pipeline,
        tenant_id=tenant_id,
        mode=payload.mode,
        options=payload.options
    )
    
    return {
        "status": "started",
        "tenant_id": tenant_id,
        "stream_url": f"/api/admin/engine/stream/v2/{tenant_id}"
    }
```

### Validación de Prerequisites
```python
async def validate_prerequisites(
    tenant_id: int,
    session: AsyncSession
):
    """
    Verifica que estén configuradas las credenciales necesarias
    """
    # 1. Tienda Nube conectada
    tn_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube"
    )
    if not tn_token:
        raise HTTPException(
            status_code=400,
            detail="Tienda Nube not connected. Connect your store first."
        )
    
    # 2. OpenAI API Key
    openai_key = await get_tenant_credential(
        tenant_id=tenant_id,
        category="openai"
    )
    if not openai_key:
        raise HTTPException(
            status_code=400,
            detail="OpenAI API key not configured"
        )
    
    # 3. Google API Key (para imágenes)
    google_key = await get_tenant_credential(
        tenant_id=tenant_id,
        category="google"
    )
    if not google_key:
        raise HTTPException(
            status_code=400,
            detail="Google API key not configured (required for visuals)"
        )
```

## 5. SSE Stream (Server-Sent Events)

### Endpoint SSE
```python
# orchestrator_service/app/api/v1/endpoints/sse.py

from sse_starlette.sse import EventSourceResponse

@router.get("/engine/stream/v2/{tenant_id}")
async def stream_magic_progress(
    tenant_id: int,
    current_user = Depends(verify_admin_token)
):
    """
    Stream de eventos en tiempo real del proceso de Magia
    """
    async def event_generator():
        # Suscribirse a Redis channel
        pubsub = redis_client.pubsub()
        channel = f"magic_progress:{tenant_id}"
        await pubsub.subscribe(channel)
        
        try:
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    
                    # Enviar evento al frontend
                    yield {
                        "event": data.get('event', 'log'),
                        "data": json.dumps(data)
                    }
                    
                    # Si terminó, cerrar stream
                    if data.get('event') == 'done':
                        break
        finally:
            await pubsub.unsubscribe(channel)
    
    return EventSourceResponse(event_generator())
```

### Redis Broadcast (desde Pipeline)
```python
async def broadcast_progress(
    tenant_id: int,
    event: str,
    data: dict
):
    """
    Envía evento a todos los clientes suscritos
    """
    channel = f"magic_progress:{tenant_id}"
    
    payload = {
        "event": event,
        **data
    }
    
    await redis_client.publish(
        channel,
        json.dumps(payload)
    )
```

## 6. Ejecución del Pipeline

### execute_magic_pipeline (Background Task)
```python
async def execute_magic_pipeline(
    tenant_id: int,
    mode: str,
    options: dict
):
    """
    Ejecuta los 7 agentes secuencialmente
    """
    try:
        # 1. Catalog Analyzer
        await broadcast_progress(
            tenant_id,
            "log",
            {"message": "📦 Analizando catálogo de productos..."}
        )
        
        catalog = await analyze_catalog(tenant_id)
        
        await broadcast_progress(
            tenant_id,
            "progress",
            {"percentage": 14, "step": "catalog"}
        )
        
        # 2. Brand DNA Extractor
        await broadcast_progress(
            tenant_id,
            "log",
            {"message": "🧬 Extrayendo ADN de marca..."}
        )
        
        branding = await extract_brand_dna(tenant_id, catalog)
        
        await save_asset(
            tenant_id=tenant_id,
            type="branding",
            content=branding
        )
        
        await broadcast_progress(
            tenant_id,
            "asset_generated",
            {"type": "branding", "id": branding_asset.id}
        )
        
        await broadcast_progress(
            tenant_id,
            "progress",
            {"percentage": 28, "step": "branding"}
        )
        
        # 3. Knowledge Vectorizer
        if options.get('vectorize_catalog', True):
            await broadcast_progress(
                tenant_id,
                "log",
                {"message": "🧠 Vectorizando conocimiento para RAG..."}
            )
            
            await vectorize_catalog(tenant_id, catalog)
            
            await broadcast_progress(
                tenant_id,
                "progress",
                {"percentage": 42, "step": "vectorization"}
            )
        
        # 4. Sales Script Generator
        await broadcast_progress(
            tenant_id,
            "log",
            {"message": "📝 Generando scripts de venta..."}
        )
        
        scripts = await generate_sales_scripts(
            tenant_id,
            catalog,
            branding
        )
        
        await save_asset(
            tenant_id=tenant_id,
            type="scripts",
            content=scripts
        )
        
        await broadcast_progress(
            tenant_id,
            "progress",
            {"percentage": 56, "step": "scripts"}
        )
        
        # 5. ROI Projector
        await broadcast_progress(
            tenant_id,
            "log",
            {"message": "💰 Calculando proyecciones ROI..."}
        )
        
        roi = await calculate_roi(tenant_id, catalog)
        
        await save_asset(
            tenant_id=tenant_id,
            type="roi",
            content=roi
        )
        
        await broadcast_progress(
            tenant_id,
            "progress",
            {"percentage": 70, "step": "roi"}
        )
        
        # 6. Visual Artist
        if options.get('generate_visuals', True):
            await broadcast_progress(
                tenant_id,
                "log",
                {"message": "🎨 Generando visuales publicitarios..."}
            )
            
            visuals = await generate_visuals(
                tenant_id,
                catalog,
                branding
            )
            
            await save_asset(
                tenant_id=tenant_id,
                type="visuals",
                content=visuals
            )
            
            await broadcast_progress(
                tenant_id,
                "progress",
                {"percentage": 85, "step": "visuals"}
            )
        
        # 7. Compliance Guardian
        await broadcast_progress(
            tenant_id,
            "log",
            {"message": "✅ Validando coherencia..."}
        )
        
        validation = await validate_compliance(tenant_id)
        
        await broadcast_progress(
            tenant_id,
            "progress",
            {"percentage": 100, "step": "validation"}
        )
        
        # Finalizar
        await broadcast_progress(
            tenant_id,
            "done",
            {"message": "🎉 Magia completada!"}
        )
        
    except Exception as e:
        await broadcast_progress(
            tenant_id,
            "error",
            {"message": f"Error: {str(e)}"}
        )
        raise
```

## 7. Agentes Específicos

### Catalog Analyzer
```python
async def analyze_catalog(tenant_id: int) -> dict:
    """
    Descarga y analiza catálogo de Tienda Nube
    """
    # Obtener credenciales
    tn_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube"
    )
    
    tn_user_id = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube",
        name="user_id"
    )
    
    # Llamar API de Tienda Nube
    response = await httpx.get(
        f"https://api.tiendanube.com/v1/{tn_user_id}/products",
        headers={"Authorization": f"Bearer {tn_token}"},
        params={"per_page": 200}
    )
    
    products = response.json()
    
    # Análisis estructural
    categories = extract_categories(products)
    price_range = calculate_price_range(products)
    top_products = identify_top_products(products)
    
    return {
        "products": products,
        "categories": categories,
        "price_range": price_range,
        "top_products": top_products,
        "total_products": len(products)
    }
```

### Brand DNA Extractor
```python
async def extract_brand_dna(
    tenant_id: int,
    catalog: dict
) -> dict:
    """
    Usa IA para analizar la identidad de marca
    """
    # Llamar a agent_service
    response = await httpx.post(
        "http://agent_service:8004/analyze-brand",
        json={
            "tenant_id": tenant_id,
            "catalog": catalog,
            "prompt": """
Analiza este catálogo de productos y extrae:
1. MISIÓN: ¿Qué problema resuelve esta tienda?
2. VISIÓN: ¿Qué aspiración tiene?
3. VOZ: ¿Cómo habla la marca? (formal, casual, técnica)
4. VALORES: ¿Qué principios transmite?

Formato JSON.
"""
        }
    )
    
    brand_dna = response.json()
    
    return {
        "mission": brand_dna.get('mission'),
        "vision": brand_dna.get('vision'),
        "voice": brand_dna.get('voice'),
        "values": brand_dna.get('values'),
        "color_palette": brand_dna.get('color_palette'),
        "typography_vibe": brand_dna.get('typography_vibe')
    }
```

### Visual Artist
```python
async def generate_visuals(
    tenant_id: int,
    catalog: dict,
    branding: dict
) -> dict:
    """
    Genera imágenes publicitarias con Google Imagen 3
    """
    google_key = await get_tenant_credential(
        tenant_id=tenant_id,
        category="google"
    )
    
    # Seleccionar top 3 productos
    top_products = catalog['top_products'][:3]
    
    visuals = []
    
    for product in top_products:
        # Construir prompt
        prompt = f"""
Professional advertising photography of {product['name']}.
Brand vibe: {branding['voice']}.
Colors: {branding['color_palette']}.
High-end commercial lighting, cinematic composition.
"""
        
        # Llamar a Google Imagen API
        response = await httpx.post(
            "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0:generate",
            headers={"Authorization": f"Bearer {google_key}"},
            json={
                "prompt": prompt,
                "num_images": 1,
                "aspect_ratio": "1:1"
            }
        )
        
        image_url = response.json()['images'][0]['url']
        
        visuals.append({
            "product_id": product['id'],
            "product_name": product['name'],
            "image_url": image_url,
            "prompt_used": prompt
        })
    
    return {
        "social_posts": visuals,
        "generated_at": datetime.utcnow().isoformat()
    }
```

## 8. Persistencia de Assets

### business_assets Table
```sql
CREATE TABLE business_assets (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    type VARCHAR(50) NOT NULL,  -- 'branding', 'scripts', 'roi', 'visuals'
    content JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Guardar Asset
```python
async def save_asset(
    tenant_id: int,
    type: str,
    content: dict
) -> BusinessAsset:
    """
    Persiste asset generado en DB
    """
    asset = BusinessAsset(
        tenant_id=tenant_id,
        type=type,
        content=content
    )
    
    session.add(asset)
    await session.commit()
    await session.refresh(asset)
    
    return asset
```

## 9. Troubleshooting

### "Stream se desconecta"
```
Causa: Timeout de SSE (servidor cierra conexión)
Solución: Enviar "heartbeat" cada 15 segundos desde backend
```

### "Error: Tienda Nube API 401"
```
Causa: Token expirado o inválido
Solución: Re-autenticar Tienda Nube en Settings
```

### "No se generan imágenes"
```
Causa: Google API key faltante o quota excedida
Solución: Configurar credencial 'google' en Vault
```

### "RAG vectorization falla"
```
Causa: Supabase URL incorrecta o pgvector no habilitado
Solución: Verificar SUPABASE_DB_URL y extensión pgvector
```

## 10. Checklist de Implementación

### Frontend
- [ ] Botón "Hacer Magia" funcional
- [ ] SSE listener conectado
- [ ] Progress bar actualizada en tiempo real
- [ ] Log console visible
- [ ] Redirección a Forge al completar
- [ ] Error handling (stream disconnect)

### Backend
- [ ] Background task ejecutándose
- [ ] SSE endpoint con Redis pubsub
- [ ] 7 agentes implementados
- [ ] Assets guardados en business_assets
- [ ] Validación de prerequisites
- [ ] Broadcast de eventos correcto

### Credenciales Requeridas
- [ ] Tienda Nube (access_token + user_id)
- [ ] OpenAI (API key)
- [ ] Google (API key para Imagen 3)
- [ ] Supabase (DB URL para RAG)

---

**Tip**: Para debugging, usar Redis CLI para monitorear mensajes: `SUBSCRIBE magic_progress:*`
