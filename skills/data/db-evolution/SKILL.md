---
name: "DB Schema Surgeon"
description: "Gestión del esquema PostgreSQL, Auto-Healing y arquitectura RAG híbrida."
trigger: "base de datos, modelos, migraciones, tablas, RAG, schema, SQL"
scope: "DATABASE"
auto-invoke: true
---

# DB Schema Surgeon - Platform AI Solutions

## 1. Filosofía Auto-Healing (NO Alembic)

### El Protocolo
Platform AI Solutions usa **Self-Healing**: el esquema se auto-repara en cada startup.

```python
# orchestrator_service/main.py
from app.models import Base
from app.db import engine

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Crea SOLO las tablas que no existen
        await conn.run_sync(Base.metadata.create_all)
    
    # Ejecutar migraciones de esquema
    await run_migration_steps()
```

### Ventajas
- Sin historial de migraciones complejo
- Desarrollo rápido (cambios inmediatos)
- Funciona igual en local, staging y producción
- Idempotente (`create_all` solo crea lo que falta)

## 2. Crear Nuevas Tablas

### Paso 1: Definir Modelo SQLAlchemy

```python
# app/models/business_asset.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, JSONB, ForeignKey
from datetime import datetime
from .base import Base

class BusinessAsset(Base):
    __tablename__ = "business_assets"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID
    tenant_id: Mapped[str] = mapped_column(String(50), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(50))  # branding, scripts, roi
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)
```

### Paso 2: Importar en main.py

```python
# main.py
from app.models import (
    Base,
    Tenant,
    Agent,
    BusinessAsset,  # ← Agregar aquí
    Credential
)

# Esto asegura que SQLAlchemy conozca todos los modelos
```

### Paso 3: Reiniciar
Al reiniciar el servicio, `create_all` ejecutará y la tabla se creará automáticamente.

## 3. Modificar Tablas Existentes

### El Problema
`create_all` **NO** altera tablas existentes.

Para agregar columnas, cambiar tipos, o renombrar: **Migration Script**

### Solución: Migration Steps

```python
# orchestrator_service/scripts/migration_steps.py
from sqlalchemy import text

async def run_migration_steps(engine):
    """Migraciones idempotentes"""
    
    async with engine.begin() as conn:
        # Migración 1: Agregar columna
        await conn.execute(text("""
            ALTER TABLE agents 
            ADD COLUMN IF NOT EXISTS template_type VARCHAR(50) DEFAULT 'custom'
        """))
        
        # Migración 2: Crear índice
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_agents_tenant_active 
            ON agents(tenant_id, is_active)
        """))
        
        # Migración 3: Agregar columna JSONB
        await conn.execute(text("""
            ALTER TABLE tenants 
            ADD COLUMN IF NOT EXISTS tool_config JSONB DEFAULT '{}'::jsonb
        """))
```

### Invocar en Startup

```python
# main.py
from scripts.migration_steps import run_migration_steps

@app.on_event("startup")
async def startup_event():
    # 1. Crear tablas nuevas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 2. Ejecutar migraciones
    await run_migration_steps(engine)
```

## 4. Arquitectura RAG Híbrida

### Separación de Responsabilidades

| **Almacenamiento** | **Responsabilidad** | **Tecnología** |
|--------------------|---------------------|----------------|
| PostgreSQL Local   | Metadata (filename, collection, file_path) | `rag_documents` table |
| Supabase Remote    | Vectores (embeddings) | pgvector extension |

### Modelo PostgreSQL

```python
# app/models/rag_document.py
class RAGDocument(Base):
    __tablename__ = "rag_documents"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID
    tenant_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("tenants.id"),
        index=True
    )
    filename: Mapped[str] = mapped_column(String(255))
    collection: Mapped[str] = mapped_column(String(100))  # General, ADN Personal, Shadow RAG
    file_type: Mapped[str] = mapped_column(String(50))  # pdf, txt, docx
    file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

### Flujo de Creación

```python
# 1. Guardar metadata en PostgreSQL
doc = RAGDocument(
    id=str(uuid.uuid4()),
    tenant_id=tenant_id,
    filename=filename,
    collection="General",
    file_type=file_extension,
    file_path=storage_path
)
session.add(doc)
await session.flush()  # Obtener ID sin commit final

# 2. Procesar documento
chunks = process_document(file_content)

# 3. Vectorizar y guardar en Supabase
from app.services.rag.vector_store import SupabaseVectorStore

vector_store = SupabaseVectorStore(tenant_id)
await vector_store.add_documents(
    chunks,
    metadata={
        "tenant_id": tenant_id,
        "source_id": doc.id,
        "collection": collection
    }
)

# 4. Commit
await session.commit()
```

### Flujo de Eliminación (Dual Delete Protocol)

**CRÍTICO**: Mantener coherencia entre PostgreSQL y Supabase

```python
# Paso 1: Surgical Strike (Remoto) - Eliminar vectores de Supabase
await supabase.from_("documents").delete().eq(
    "metadata->>source_id", doc_id
).execute()

# Paso 2: Metadata Cleanup (Local) - Eliminar de PostgreSQL
stmt = delete(RAGDocument).where(
    RAGDocument.id == doc_id,
    RAGDocument.tenant_id == tenant_id
)
await session.execute(stmt)

# Paso 3: Physical Sweep (Disco) - Best effort
try:
    os.remove(file_path)
except FileNotFoundError:
    logger.warning(f"File {file_path} not found, skipping physical delete")

await session.commit()
```

## 5. Tablas Core (Schema Reference)

### credentials (The Vault)
```sql
CREATE TABLE IF NOT EXISTS credentials (
    id_uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id INTEGER REFERENCES tenants(id),
    name TEXT NOT NULL,
    value TEXT NOT NULL,  -- Encrypted AES-256
    category TEXT DEFAULT 'general',  -- openai, google, smtp
    scope TEXT DEFAULT 'global',  -- global o tenant
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(name, tenant_id)  -- Unicidad multi-tenant
);
```

### agents (AI Configuration)
```sql
CREATE TABLE IF NOT EXISTS agents (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    name TEXT NOT NULL,
    role TEXT DEFAULT 'sales',
    model_provider TEXT DEFAULT 'openai',
    model_version TEXT DEFAULT 'gpt-5-mini',
    temperature FLOAT DEFAULT 0.7,
    system_prompt_template TEXT NOT NULL,
    enabled_tools JSONB DEFAULT '[]',
    channels JSONB DEFAULT '["whatsapp", "instagram", "facebook", "web"]',
    config JSONB DEFAULT '{}',
    template_type VARCHAR(50) DEFAULT 'custom',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### chat_conversations (Omnichannel)
```sql
CREATE TABLE IF NOT EXISTS chat_conversations (
    id UUID PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    channel VARCHAR(32) NOT NULL,  -- whatsapp, instagram, facebook, web
    channel_source VARCHAR(32) DEFAULT 'whatsapp',
    display_name VARCHAR(255),
    meta JSONB DEFAULT '{}',
    last_message_preview TEXT,
    last_message_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### tools (Brain Extensions)
```sql
CREATE TABLE IF NOT EXISTS tools (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),  -- NULL para Global
    name VARCHAR(255) NOT NULL,
    type VARCHAR(32) NOT NULL,  -- http, internal
    description TEXT,
    prompt_injection TEXT,
    response_guide TEXT,
    config JSONB DEFAULT '{}',
    service_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, name)
);
```

## 6. Tipos de Datos Comunes

```python
from sqlalchemy import String, Integer, Boolean, DateTime, Text, JSONB, ARRAY

class ExampleModel(Base):
    __tablename__ = "example"
    
    # IDs
    id_uuid: Mapped[str] = mapped_column(String, primary_key=True)
    id_int: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Texto
    short_text: Mapped[str] = mapped_column(String(255))
    long_text: Mapped[str] = mapped_column(Text)
    
    # JSON
    metadata: Mapped[dict] = mapped_column(JSONB, default={})
    
    # Arrays
    tags: Mapped[list] = mapped_column(JSONB, default=[])
    
    # Booleanos
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

## 7. Identity Resolution (UUID vs INTEGER)

### El Problema Crítico
- **Tenants**: `id` es INTEGER
- **Users**: `id` es UUID, `tenant_id` es INTEGER
- **Agents, Tools, Credentials**: `tenant_id` es INTEGER (foreign key)

### La Solución
```python
# NUNCA asumir que current_user.tenant_id es UUID
# SIEMPRE resolver desde tabla users

user_row = await db.pool.fetchrow(
    "SELECT tenant_id FROM users WHERE id = $1",
    current_user.id  # UUID
)
real_tenant_int = user_row['tenant_id']  # INTEGER

# Usar en queries
stmt = delete(Agent).where(Agent.tenant_id == real_tenant_int)
```

## 8. Índices y Performance

### Crear Índices

```python
from sqlalchemy import Index

class Message(Base):
    __tablename__ = "messages"
    
    # ... columnas ...
    
    __table_args__ = (
        Index('idx_messages_conversation', 'conversation_id', 'created_at'),
        Index('idx_messages_tenant', 'tenant_id'),
    )
```

### Eager Loading (Evitar N+1)

```python
from sqlalchemy.orm import selectinload

# ❌ MAL - N+1 queries
conversations = await session.execute(select(Conversation))
for conv in conversations:
    messages = conv.messages  # Query adicional

# ✅ BIEN - Single query
stmt = select(Conversation).options(
    selectinload(Conversation.messages)
)
conversations = await session.execute(stmt)
```

## 9. Colecciones RAG

### Tipos de Colecciones

- **General**: Manuales técnicos, políticas (PDF/DOCX)
- **ADN Personal**: Historiales de conversación (.txt) para clonación de estilo
- **Shadow RAG**: Chats vectorizados automáticamente (memoria largo plazo)

### WhatsApp Parser (Identity Engine)

```python
# Al subir .txt a "ADN Personal", se activa parser
if collection == "ADN Personal" and file_ext == ".txt":
    from app.services.parsers import WhatsAppParser
    
    parser = WhatsAppParser(hero_name=hero_name)
    parsed = parser.parse(file_content)
    
    # Genera pares context/response para stored patterns
```

## 10. Reset Industrial (Development Only)

```sql
-- Limpiar plataforma completa
TRUNCATE TABLE 
    users, tenants, credentials, agents, tools, 
    business_assets, chat_conversations, chat_messages,
    rag_documents
RESTART IDENTITY CASCADE;
```

## 11. Checklist Pre-Deploy

- [ ] ¿El modelo está importado en `main.py`?
- [ ] ¿Las columnas tienen tipos explícitos (`Mapped[type]`)?
- [ ] ¿Las foreign keys tienen índices?
- [ ] ¿`tenant_id` está indexado?
- [ ] ¿Las migraciones usan `IF NOT EXISTS`?
- [ ] ¿En RAG, se sincroniza PostgreSQL + Supabase?
- [ ] ¿Los scripts son idempotentes?
- [ ] ¿Se resuelve UUID→INT para tenant_id?
