---
name: "Omnichannel Chat Operator"
description: "Especialista en gestión de conversaciones multi-canal (WhatsApp, Instagram, Facebook) para Platform AI Solutions."
trigger: "chats, conversaciones, mensajes, whatsapp, instagram, facebook, human override, templates"
scope: "CHATS"
auto-invoke: true
---

# Omnichannel Chat Operator - Platform AI Solutions

## 1. Arquitectura de Comunicación

### Canales Soportados
- **WhatsApp**: Via Meta Cloud API o YCloud
- **Instagram**: Via Meta Graph API
- **Facebook Messenger**: Via Meta Graph API
- **Web Widget**: Canal directo (Chatwoot optional)

### Flujo Híbrido de Sincronización
```
Frontend (Chats.tsx)
    ↓
Polling (10s) → GET /admin/chats/summary
    ↓
Chat Selected → Loop (3s) → GET /admin/chats/{id}/messages
    ↓
Delta Sync (solo nuevos mensajes)
```

## 2. Gestión de Conversaciones

### Cargar Lista de Chats
```typescript
// Polling cada 10 segundos
const loadChats = async () => {
  const response = await useApi<Contact[]>({
    method: 'GET',
    url: '/admin/chats/summary',
    params: {
      human_filter: 'all',  // 'all', 'human_only', 'bot_only'
      channel: 'whatsapp',  // Filtro opcional
      limit: 20
    }
  });
};

// Response structure
interface Contact {
  id: string;  // UUID
  customer_phone: string;
  display_name: string;
  last_message: string;
  timestamp: string;
  channel_source: 'whatsapp' | 'instagram' | 'facebook' | 'web';
  unread_count: number;
  is_locked: boolean;  // Human override activo
  platform_origin: string;  // Cuenta específica de Meta
}
```

### Cargar Mensajes de Conversación
```typescript
// Loop de 3 segundos cuando chat está seleccionado
const loadMessages = async (chatId: string) => {
  const messages = await useApi<Message[]>({
    method: 'GET',
    url: `/admin/chats/${chatId}/messages`
  });
  
  // Ordenar por timestamp (puede venir desordenado)
  messages.sort((a, b) => 
    new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );
};

// Message structure
interface Message {
  id: number;
  conversation_id: string;
  sender: 'user' | 'agent';
  content: string;
  timestamp: string;
  attachments?: Attachment[];  // Multimedia
  correlation_id?: string;  // Link con logs de IA
}

interface Attachment {
  type: 'image' | 'video' | 'audio' | 'document';
  url: string;
  filename?: string;
}
```

## 3. Envío de Mensajes (Unified Outbox)

### Send Tunnel
```typescript
const sendMessage = async (
  conversationId: string,
  message: string,
  channelSource: string
) => {
  await useApi({
    method: 'POST',
    url: '/admin/whatsapp/send',
    data: {
      conversation_id: conversationId,
      message: message,
      channel_source: channelSource  // CRÍTICO para routing
    }
  });
};
```

### Backend Routing (Orchestrator v6.2.9)
```python
# orchestrator_service/app/api/v1/endpoints/chats.py

@router.post("/whatsapp/send")
async def send_message(
    payload: SendMessageRequest,
    current_user = Depends(verify_admin_token)
):
    # 1. Resolver tenant e ID de conversación
    tenant_id = await resolve_tenant(current_user.id)
    
    # 2. Delegar al Universal Delivery Relay (v6.2.9)
    # Se centraliza en whatsapp_service para aplicar Spacing (4s) y Auth Dinámica.
    relay_payload = {
        "to": payload.to_number,
        "text": payload.message,
        "provider": resolve_provider(payload.channel_source),
        "channel_source": payload.channel_source,
        "tenant_id": tenant_id,
        "conversation_id": payload.conversation_id
    }
    
    await delivery_relay.post("/messages/relay", json=relay_payload)
    
    # 3. Guardar en DB para auditoría
    # ... persistencia ...
    
    return {"status": "sent"}
```

## 4. Human Override (Intervención Humana)

### Activar Chat Lock
```typescript
const toggleHumanOverride = async (
  chatId: string,
  locked: boolean
) => {
  await useApi({
    method: 'POST',
    url: `/admin/conversations/${chatId}/human-override`,
    data: { locked }
  });
};
```

### Backend Implementation
```python
@router.post("/conversations/{conversation_id}/human-override")
async def set_human_override(
    conversation_id: str,
    payload: HumanOverrideRequest,
    session: AsyncSession = Depends(get_session)
):
    # Actualizar flag
    stmt = update(ChatConversation).where(
        ChatConversation.id == conversation_id
    ).values(is_locked=payload.locked)
    
    await session.execute(stmt)
    await session.commit()
    
    # El bot dejará de responder automáticamente
    # hasta que is_locked = false
    
    return {"locked": payload.locked}

### Detección Automática de Ecos (Chatwoot Dash)
Si un humano responde directamente desde la interfaz de Chatwoot, el `whatsapp_service` captura el evento `message_created` (outgoing) y lo marca como `is_echo = True`. Al llegar al Orchestrator, este activa el bloqueo de IA automáticamente para ese chat.
```

## 5. Templates HSM (Meta 24h Window)

### Regla de Meta
- **Ventana de 24h**: Después de la última interacción del usuario, solo puedes responder con texto libre durante 24 horas
- **Re-enganche**: Pasadas 24h, debes usar plantillas HSM pre-aprobadas por Meta

### UI Template Selector
```typescript
interface Template {
  id: string;
  name: string;
  language: string;
  status: 'APPROVED' | 'PENDING' | 'REJECTED';
  category: 'MARKETING' | 'UTILITY' | 'AUTHENTICATION';
  components: TemplateComponent[];
}

const sendTemplate = async (
  conversationId: string,
  templateId: string,
  parameters: string[]
) => {
  await useApi({
    method: 'POST',
    url: '/admin/templates/send',
    data: {
      conversation_id: conversationId,
      template_id: templateId,
      parameters: parameters
    }
  });
};
```

### Sincronizar Templates
```python
# Sync con Meta para obtener status actualizado
@router.post("/templates/sync")
async def sync_templates(tenant_id: int):
    # Obtener credenciales de Meta
    waba_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="whatsapp_cloud"
    )
    
    # Llamar a Meta Graph API
    response = requests.get(
        f"https://graph.facebook.com/v18.0/{waba_id}/message_templates",
        headers={"Authorization": f"Bearer {waba_token}"}
    )
    
    templates = response.json()['data']
    
    # Actualizar DB local
    for template in templates:
        # Upsert en tabla templates
        pass
    
    return {"synced": len(templates)}
```

## 6. Multimedia (Attachments)

### Renderizar Adjuntos
```tsx
const renderAttachment = (attachment: Attachment) => {
  switch (attachment.type) {
    case 'image':
      return <img src={attachment.url} alt="Attachment" />;
    case 'video':
      return <video src={attachment.url} controls />;
    case 'audio':
      return <audio src={attachment.url} controls />;
    case 'document':
      return <a href={attachment.url} download>{attachment.filename}</a>;
  }
};
```

### Backend Storage
```python
# Attachments se guardan como JSONB en chat_messages.attachments
attachments = [
    {
        "type": "image",
        "url": "https://cdn.whatsapp.net/...",
        "mime_type": "image/jpeg"
    }
]

msg = ChatMessage(
    conversation_id=conv_id,
    sender='user',
    content='[Image]',
    attachments=attachments  # JSONB column
)
```

## 7. Indicadores Visuales (UI)

### Estado Online
```typescript
const isOnline = (lastInteraction: string): boolean => {
  const diff = Date.now() - new Date(lastInteraction).getTime();
  return diff < 5 * 60 * 1000;  // < 5 minutos = online
};
```

### Borde de Color por Canal
```tsx
const getBorderColor = (channel: string) => {
  switch (channel) {
    case 'whatsapp': return 'border-green-500';
    case 'instagram': return 'border-pink-500';
    case 'facebook': return 'border-blue-500';
    case 'web': return 'border-purple-500';
  }
};
```

## 8. Traceability (Correlation ID)

### Link con AI Logs
```python
# Al crear mensaje del agente
correlation_id = str(uuid.uuid4())

msg = ChatMessage(
    conversation_id=conv_id,
    sender='agent',
    content=response,
    correlation_id=correlation_id
)

# En logs del agent_service
logger.info(
    f"AI Response",
    extra={
        "correlation_id": correlation_id,
        "reasoning": reasoning_steps,
        "tools_used": tool_calls
    }
)
```

### Frontend Debugging
```tsx
// Ver logs de razonamiento del agente
const viewAIReasoning = async (correlationId: string) => {
  const logs = await useApi({
    method: 'GET',
    url: `/admin/logs/ai/${correlationId}`
  });
  // Mostrar en modal
};
```

## 9. Paginación y Scroll Infinito

### Implementación
```tsx
const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
  const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
  
  // Detectar bottom
  if (scrollHeight - scrollTop === clientHeight) {
    if (!loading && hasMore) {
      loadMoreChats();
    }
  }
};

const loadMoreChats = async () => {
  const newChats = await useApi({
    method: 'GET',
    url: '/admin/chats/summary',
    params: {
      offset: contacts.length,
      limit: 20
    }
  });
  
  setContacts([...contacts, ...newChats]);
};
```

## 10. Troubleshooting

### "El bot no responde"
```python
# Checklist de diagnóstico
1. Verificar is_locked = false en chat_conversations
2. Verificar tenant_id del mensaje entrante coincide con agent.tenant_id
3. Verificar credenciales OpenAI válidas para el tenant
4. Revisar logs: docker logs orchestrator_service --tail 100
```

### "Error sending message"
```python
# Causas comunes:
- Falta channel_source en payload
- Token de Meta expirado
- 24h window expirada (usar template)
- Número no registrado en WABA
```

### "Mensajes desordenados"
```typescript
// SIEMPRE ordenar en frontend
messages.sort((a, b) => 
  new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
);
```

## 11. Multi-Tenant Security

### Filtrado Obligatorio
```python
# Backend SIEMPRE debe filtrar por tenant
stmt = select(ChatConversation).where(
    ChatConversation.tenant_id == tenant_id
)

# El usuario del tenant 1 NUNCA debe ver chats del tenant 2
```

## 12. Checklist de Features

### Vista Chats.tsx
- [ ] Polling de conversaciones activo
- [ ] Loop de mensajes cuando chat seleccionado
- [ ] Envío de mensajes con channel_source correcto
- [ ] Toggle human override funcional
- [ ] Renderizado de multimedia (attachments)
- [ ] Paginación con scroll infinito
- [ ] Indicadores visuales (online, canal)
- [ ] Filtros (human_filter, channel)

### Backend
- [ ] Routing multi-canal (WhatsApp/IG/FB)
- [ ] Human override persistence
- [ ] Template management
- [ ] Attachment storage (JSONB)
- [ ] Correlation ID logging
- [ ] Multi-tenant isolation
- [ ] Delta sync optimization

---

**Tip**: Para debugging en producción, usar `correlation_id` para trazar el flujo completo desde el mensaje del usuario → razonamiento del agente → respuesta final.
