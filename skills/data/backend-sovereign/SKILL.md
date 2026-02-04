---
name: "Sovereign Backend Engineer"
description: "Experto en FastAPI y gestión segura de credenciales multi-tenant para Platform AI Solutions."
trigger: "python, backend, endpoints, base de datos, credenciales, agents, tools"
scope: "BACKEND"
auto-invoke: true
---

# Sovereign Backend Engineer - Platform AI Solutions

## 1. Arquitectura de Credenciales (The Vault)

### Regla de Oro
**NUNCA** usar `os.getenv("OPENAI_API_KEY")` para lógica de agentes.

**SIEMPRE** usar el sistema de credenciales soberanas:

```python
from app.core.credentials import get_tenant_credential

# Correcto - Credenciales por tenant
api_key = await get_tenant_credential(
    tenant_id=tenant_id,
    category="openai",  # openai, google, smtp, tiendanube, whatsapp_cloud
    name="API_KEY"
)
```

###Categories:
- `openai`: GPT-5.2, gpt-5-mini
- `google`: Gemini 3 Pro, Gemini 3 Flash
- `smtp`: Email delivery (Modo Agente)
- `tiendanube`: E-commerce tokens
- `whatsapp_cloud`: Meta Business API
- `chatwoot`: Chatwoot API (v6.1 uses both CHATWOOT_API_TOKEN and CHATWOOT_BOT_TOKEN)

### 2b. Omnichannel Identity (v6.1 Patch)
Al procesar mensajes de Chatwoot, **SIEMPRE** persistir `external_chatwoot_id` e `external_account_id` en la tabla `chat_conversations`. Esto es crítico para que `unified_message_delivery` pueda responder correctamente.

### 2c. Universal Delivery Relay (v6.2.9)
**NO** llamar directamente a `meta_service` o `ycloud` para envíos desde el Orquestador.
**SIEMPRE** delegar al `whatsapp_service` usando el endpoint de Relay:
```python
# Protocolo v6.2.9
relay_payload = {
    "to": phone,
    "text": text,
    "provider": "meta_direct" | "chatwoot" | "ycloud",
    "channel_source": "instagram" | "facebook" | "whatsapp",
    "tenant_id": tenant_id
}
await client.post("/messages/relay", json=relay_payload)
```
*Beneficio*: Manejo automático de **Spacing (4s)** y **Buffer (16s)**.

## 2. Tenant Resolution Protocol (Critical)

### El Problema
- **Auth Layer**: `user.id` es UUID
- **DB Layer**: `tenant_id` es INTEGER

###Solución:
```python
# ❌ MAL - No confiar directamente en current_user.tenant_id
stmt = delete(Agent).where(Agent.tenant_id == current_user.tenant_id)

# ✅ BIEN - Resolver desde tabla users
user_row = await db.pool.fetchrow(
    "SELECT tenant_id FROM users WHERE id = $1", 
    current_user.id
)
real_tenant_int = user_row['tenant_id']
stmt = delete(Agent).where(Agent.tenant_id == real_tenant_int)
```

## 3. Query Patterns (Multi-Tenant Security)

### Filtrado Obligatorio
**TODA** query debe filtrar por `tenant_id`:

```python
# SQLAlchemy 2.0 Async
from sqlalchemy import select

stmt = select(Agent).where(
    Agent.id == agent_id,
    Agent.tenant_id == tenant_id  # CRÍTICO
)
result = await session.execute(stmt)
agent = result.scalar_one_or_none()
```

### Crear Entidades
```python
new_agent = Agent(
    name="Sales Agent",
    role="sales",
    model_provider="openai",
    model_version="gpt-5-mini",
    tenant_id=tenant_id,  # SIEMPRE incluir
    enabled_tools=["search_products", "rag_search"],
    channels=["whatsapp", "instagram"]
)
session.add(new_agent)
await session.commit()
```

## 4. RAG Híbrido (PostgreSQL + Supabase)

### Arquitectura Dual
- **PostgreSQL**: Metadata (`rag_documents` table)
- **Supabase pgvector**: Embeddings vectoriales

### Crear Documento
```python
# 1. Metadata en PostgreSQL
doc = RAGDocument(
    tenant_id=tenant_id,
    filename=filename,
    collection="General",  # General, ADN Personal, Shadow RAG
    file_path=storage_path
)
session.add(doc)
await session.flush()  # Obtener ID

# 2. Vectorizar y almacenar en Supabase
chunks = process_document(file_content)
await supabase_vector_store.add_documents(
    chunks,
    metadata={"tenant_id": tenant_id, "source_id": str(doc.id)}
)
await session.commit()
```

### Eliminar Documento (Dual Delete)
```python
# 1. Eliminar vectores de Supabase
await supabase.from_("documents").delete().eq(
    "metadata->>source_id", str(doc_id)
).execute()

# 2. Eliminar metadata de PostgreSQL
stmt = delete(RAGDocument).where(
    RAGDocument.id == doc_id,
    RAGDocument.tenant_id == tenant_id
)
await session.execute(stmt)
await session.commit()
```

## 5. Endpoints Pattern (FastAPI)

### Estructura Estándar
```python
from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import verify_admin_token

router = APIRouter()

@router.post("/agents", status_code=201)
async def create_agent(
    payload: AgentCreate,
    admin_user = Depends(verify_admin_token)
):
    # Resolver tenant
    tenant_id = await resolve_tenant(admin_user.id)
    
    # Validar credenciales existen
    has_creds = await check_credentials(tenant_id, "openai")
    if not has_creds:
        raise HTTPException(
            status_code=400,
            detail="OpenAI credentials not configured"
        )
    
    # Crear agente
    agent = Agent(**payload.dict(), tenant_id=tenant_id)
    # ...
    return agent
```

## 6. Tools Registry

### Crear Nueva Tool
```python
# app/services/tools_registry.py
from langchain.tools import tool

@tool
def search_products(query: str, tenant_id: int) -> dict:
    """Busca productos en Tienda Nube del tenant."""
    # Obtener credenciales de Tienda Nube
    tn_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube"
    )
    
    # Llamar API
    response = requests.get(
        f"https://api.tiendanube.com/v1/products/search",
        headers={"Authorization": f"Bearer {tn_token}"},
        params={"q": query}
    )
    return response.json()

@tool
async def report_assistance(type: str, score: float, reasoning: str):
    """Registra métricas de ayuda (sales/support) en la DB."""
    # Implementado en admin_routes.py (/tools/report_assistance)
    # y reflejado en el Dashboard v7.6
    pass
```

### Registro en Base de Datos
```python
tool_entry = Tool(
    tenant_id=None,  # Global tool
    name="search_products",
    type="http",
    description="Busca productos en catálogo",
    prompt_injection="Usa esta tool cuando el usuario pregunte por productos",
    config={"timeout": 10}
)
```

## 7. Agent Templates (Polymorphic Factory)

### Pre-configuraciones
- **Sales Agent**: Temperatura 0.7, tools: [search_products, check_stock]
- **Support Agent**: Temperatura 0.5, tools: [rag_search]
- **Leads Agent**: Temperatura 0.6, tools: [create_customer]

### Seed Data (Pointe Coach Legacy)
```python
DEFAULT_AGENT_TONE = """
Sos una asesora experta en danza clásica y ballet.
Usá voseo argentino. Sé cálida y profesional.
"""

SYNONYM_DICTIONARY = {
    "mallas": "leotardos",
    "can can": "medias",
    "zapatillas de punta": "puntas"
}
```

## 8. Meta Integration (The Diplomat)

### OAuth Flow
```python
# Orquestador proxy a meta_service
response = await httpx.post(
    "http://meta_service:8000/connect",
    json={
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "tenant_id": tenant_id
    },
    headers={"X-Internal-Secret": INTERNAL_SECRET_KEY}
)

# Meta service devuelve Long-Lived Token (60 días)
# Y persiste en credentials automáticamente
```

## 9. Error Handling

### HTTPException Descriptivas
```python
# ❌ MAL
raise HTTPException(status_code=400, detail="Error")

# ✅ BIEN
raise HTTPException(
    status_code=404,
    detail=f"Agent {agent_id} not found or access denied"
)
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

try:
    # Operación
    pass
except Exception as e:
    logger.error(f"Failed to create agent: {str(e)}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal error")
```

## 10. Checklist Pre-Deploy

- [ ] ¿Todas las queries filtran por `tenant_id`?
- [ ] ¿Se usa `get_tenant_credential` para API keys?
- [ ] ¿Se resuelve `tenant_id` desde tabla `users`?
- [ ] ¿Las tools están registradas en `tools_registry.py`?
- [ ] ¿Los modelos están importados en `main.py`?
- [ ] ¿RAG sincroniza PostgreSQL + Supabase?
- [ ] ¿Los errores tienen mensajes descriptivos?
