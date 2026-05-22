---
name: "Credential Vault Specialist"
description: "Especialista en gestión segura de credenciales multi-tenant: encriptación, scope, categorías y The Vault."
trigger: "credentials, credenciales, vault, api keys, tokens, encriptación, settings, sovereign"
scope: "SECURITY"
auto-invoke: true
---

# Credential Vault Specialist - Platform AI Solutions

## 1. Concepto: The Sovereign Vault

### Filosofía
**NO usar variables de entorno para secretos de tenant**. Cada tienda (tenant) proporciona sus propias credenciales API, garantizando:
- **Soberanía de Datos**: El tenant controla sus propias keys
- **Aislamiento Total**: Las credenciales de Tenant 1 son invisibles para Tenant 2
- **Rotación Independiente**: Cada tenant puede rotar sus keys sin afectar a otros

### The Vault Architecture
```
Frontend (Credentials View)
    ↓
POST /admin/credentials (HTTPS)
    ↓
Backend → AES-256 Encryption (Fernet)
    ↓
PostgreSQL credentials table (encrypted value)
    ↓
Runtime → Decrypt on-demand (get_tenant_credential)
    ↓
API Calls (OpenAI, Meta, Google, SMTP)
```

## 2. Modelo de Datos

### credentials Table
```sql
CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    category VARCHAR(100) NOT NULL,  -- 'openai', 'google', 'smtp', 'tiendanube', 'whatsapp_cloud'
    name VARCHAR(100) NOT NULL,      -- 'API_KEY', 'user_id', 'host'
    value TEXT NOT NULL,              -- Encrypted con AES-256
    scope VARCHAR(50) DEFAULT 'tenant',  -- 'global', 'tenant'
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, category, name)
);

-- Index for fast lookups
CREATE INDEX idx_credentials_tenant_category 
ON credentials(tenant_id, category);
```

### Categorías Soportadas
```python
SUPPORTED_CATEGORIES = {
    "openai": {
        "fields": ["API_KEY"],
        "masked_display": True
    },
    "google": {
        "fields": ["API_KEY"],
        "masked_display": True
    },
    "smtp": {
        "fields": ["host", "port", "user", "pass"],
        "special_handling": "json_stringify"
    },
    "tiendanube": {
        "fields": ["access_token", "user_id"],
        "oauth": True
    },
    "whatsapp_cloud": {
        "fields": ["access_token", "phone_number_id", "waba_id"],
        "oauth": True
    },
    "meta": {
        "fields": ["long_lived_token"],
        "oauth": True,
        "expires": True
    }
}
```

## 3. Encriptación (AES-256 with Fernet)

### Master Key (Environment Variable)
```python
# orchestrator_service/.env
INTERNAL_SECRET_KEY=base64_encoded_32_byte_key_here
```

### Encryption Module
```python
# app/core/encryption.py

from cryptography.fernet import Fernet
import base64
import os

class CredentialEncryption:
    def __init__(self):
        # Derivar key desde INTERNAL_SECRET_KEY
        secret = os.getenv('INTERNAL_SECRET_KEY')
        if not secret:
            raise ValueError("INTERNAL_SECRET_KEY not set")
        
        # Asegurar 32 bytes (URL-safe base64)
        key = base64.urlsafe_b64encode(secret.encode()[:32].ljust(32))
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encripta valor y retorna string base64
        """
        encrypted_bytes = self.cipher.encrypt(plaintext.encode())
        return encrypted_bytes.decode('utf-8')
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Desencripta valor desde string base64
        """
        decrypted_bytes = self.cipher.decrypt(ciphertext.encode())
        return decrypted_bytes.decode('utf-8')

# Singleton
encryptor = CredentialEncryption()
```

## 4. Guardar Credencial (Frontend → Backend)

### Frontend: Credentials View
```tsx
const CredentialsView: React.FC = () => {
  const [category, setCategory] = useState('openai');
  const [apiKey, setApiKey] = useState('');
  
  const handleSave = async () => {
    await useApi({
      method: 'POST',
      url: '/admin/credentials',
      data: {
        category: category,
        name: 'API_KEY',
        value: apiKey,
        scope: 'tenant'  // o 'global'
      }
    });
    
    // Limpiar input
    setApiKey('');
    alert('Credential saved securely');
  };
  
  return (
    <div className="vault-interface">
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="openai">OpenAI</option>
        <option value="google">Google</option>
        <option value="smtp">SMTP</option>
      </select>
      
      <input
        type="password"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        placeholder="Enter API Key"
      />
      
      <button onClick={handleSave}>Save to Vault</button>
    </div>
  );
};
```

### Backend: Save Endpoint
```python
# orchestrator_service/app/api/v1/endpoints/credentials.py

from app.core.encryption import encryptor

@router.post("/credentials", status_code=201)
async def save_credential(
    payload: CredentialCreate,
    current_user = Depends(verify_admin_token),
    session: AsyncSession = Depends(get_session)
):
    # Resolver tenant
    tenant_id = await resolve_tenant(current_user.id)
    
    # Validar scope
    if payload.scope == 'global' and not current_user.is_superadmin:
        raise HTTPException(
            status_code=403,
            detail="Only superadmins can set global credentials"
        )
    
    # Asignar tenant_id
    if payload.scope == 'tenant':
        final_tenant_id = tenant_id
    else:
        final_tenant_id = None  # Global credentials
    
    # Encriptar valor
    encrypted_value = encryptor.encrypt(payload.value)
    
    # Upsert (insert or update)
    stmt = select(Credential).where(
        Credential.tenant_id == final_tenant_id,
        Credential.category == payload.category,
        Credential.name == payload.name
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        # Actualizar
        existing.value = encrypted_value
        existing.updated_at = datetime.utcnow()
    else:
        # Crear nuevo
        cred = Credential(
            tenant_id=final_tenant_id,
            category=payload.category,
            name=payload.name,
            value=encrypted_value,
            scope=payload.scope,
            metadata=payload.metadata or {}
        )
        session.add(cred)
    
    await session.commit()
    
    return {"status": "saved"}
```

## 5. Obtener Credencial (Runtime)

### get_tenant_credential Function
```python
# app/core/credentials.py

async def get_tenant_credential(
    tenant_id: int,
    category: str,
    name: str = "API_KEY",
    session: AsyncSession = None
) -> str | None:
    """
    Busca credencial con fallback a global
    
    Priority:
    1. Tenant-specific credential
    2. Global credential (if exists)
    3. None
    """
    # 1. Buscar credencial específica del tenant
    stmt = select(Credential).where(
        Credential.tenant_id == tenant_id,
        Credential.category == category,
        Credential.name == name
    )
    result = await session.execute(stmt)
    cred = result.scalar_one_or_none()
    
    if cred:
        # Desencriptar y retornar
        return encryptor.decrypt(cred.value)
    
    # 2. Fallback: buscar credencial global
    stmt_global = select(Credential).where(
        Credential.tenant_id == None,
        Credential.category == category,
        Credential.name == name,
        Credential.scope == 'global'
    )
    result_global = await session.execute(stmt_global)
    cred_global = result_global.scalar_one_or_none()
    
    if cred_global:
        return encryptor.decrypt(cred_global.value)
    
    # 3. No encontrado
    return None
```

### Uso en Servicios
```python
# Ejemplo: Llamar a OpenAI
async def call_openai_api(tenant_id: int, prompt: str):
    # Obtener API key del tenant
    api_key = await get_tenant_credential(
        tenant_id=tenant_id,
        category="openai",
        name="API_KEY"
    )
    
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="OpenAI API key not configured for this tenant"
        )
    
    # Usar key
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

## 6. Caso Especial: SMTP (JSON Stringified)

### SMTP Configuration
```python
# SMTP requiere múltiples campos, se guarda como JSON string

smtp_config = {
    "host": "smtp.gmail.com",
    "port": "587",
    "user": "noreply@tienda.com",
    "pass": "app_specific_password"
}

# Guardar como string JSON
await save_credential(
    tenant_id=tenant_id,
    category="smtp",
    name="config",
    value=json.dumps(smtp_config)
)

# Recuperar y parsear
smtp_json = await get_tenant_credential(
    tenant_id=tenant_id,
    category="smtp",
    name="config"
)

smtp_dict = json.loads(smtp_json)
```

### Frontend SMTP Form
```tsx
const SMTPForm: React.FC = () => {
  const [host, setHost] = useState('');
  const [port, setPort] = useState('587');
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  
  const handleSave = async () => {
    const config = {
      host,
      port,
      user,
      pass
    };
    
    await useApi({
      method: 'POST',
      url: '/admin/credentials',
      data: {
        category: 'smtp',
        name: 'config',
        value: JSON.stringify(config),
        scope: 'tenant'
      }
    });
  };
  
  return (
    <form>
      <input
        value={host}
        onChange={(e) => setHost(e.target.value)}
        placeholder="SMTP Host (e.g., smtp.gmail.com)"
      />
      <input
        value={port}
        onChange={(e) => setPort(e.target.value)}
        placeholder="Port (587 for TLS)"
      />
      <input
        value={user}
        onChange={(e) => setUser(e.target.value)}
        placeholder="Username / Email"
      />
      <input
        type="password"
        value={pass}
        onChange={(e) => setPass(e.target.value)}
        placeholder="Password / App-Specific Password"
      />
      <button onClick={handleSave}>Save SMTP Config</button>
    </form>
  );
};
```

## 7. Listar Credenciales (Masked)

### Frontend: Credential List
```tsx
interface CredentialDisplay {
  id: number;
  category: string;
  name: string;
  masked_value: string;
  scope: string;
  created_at: string;
}

const CredentialsList: React.FC = () => {
  const [credentials, setCredentials] = useState<CredentialDisplay[]>([]);
  
  useEffect(() => {
    loadCredentials();
  }, []);
  
  const loadCredentials = async () => {
    const data = await useApi({
      method: 'GET',
      url: '/admin/credentials'
    });
    setCredentials(data);
  };
  
  const handleDelete = async (id: number) => {
    if (confirm('Delete this credential?')) {
      await useApi({
        method: 'DELETE',
        url: `/admin/credentials/${id}`
      });
      loadCredentials();
    }
  };
  
  return (
    <div className="credentials-list">
      {credentials.map(cred => (
        <div key={cred.id} className="credential-card">
          <div>
            <strong>{cred.category}</strong> / {cred.name}
          </div>
          <div className="masked-value">
            {cred.masked_value}
          </div>
          <div className="scope-badge">
            {cred.scope === 'global' ? '🌍 Global' : '🔒 Tenant'}
          </div>
          <button onClick={() => handleDelete(cred.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
};
```

### Backend: List Endpoint (Masked)
```python
@router.get("/credentials")
async def list_credentials(
    current_user = Depends(verify_admin_token),
    session: AsyncSession = Depends(get_session)
):
    tenant_id = await resolve_tenant(current_user.id)
    
    # Obtener credenciales del tenant
    stmt = select(Credential).where(
        Credential.tenant_id == tenant_id
    )
    result = await session.execute(stmt)
    credentials = result.scalars().all()
    
    # Si es superadmin, mostrar también globals
    if current_user.is_superadmin:
        stmt_global = select(Credential).where(
            Credential.scope == 'global'
        )
        result_global = await session.execute(stmt_global)
        credentials.extend(result_global.scalars().all())
    
    # Maskear valores
    return [
        {
            "id": cred.id,
            "category": cred.category,
            "name": cred.name,
            "masked_value": mask_value(cred.value),
            "scope": cred.scope,
            "created_at": cred.created_at.isoformat()
        }
        for cred in credentials
    ]

def mask_value(encrypted_value: str) -> str:
    """
    Devuelve valor mascarado (ej: sk-...xyz)
    """
    try:
        # Desencriptar
        decrypted = encryptor.decrypt(encrypted_value)
        
        # Maskear (mostrar primeros 3 y últimos 3 caracteres)
        if len(decrypted) > 10:
            return f"{decrypted[:3]}...{decrypted[-3:]}"
        else:
            return "***"
    except:
        return "*** (error decrypting)"
```

## 8. Rotación de Credenciales

### Frontend: Rotate Key
```tsx
const rotateKey = async (credentialId: number) => {
  const newKey = prompt('Enter new API key:');
  
  if (!newKey) return;
  
  await useApi({
    method: 'PUT',
    url: `/admin/credentials/${credentialId}`,
    data: {
      value: newKey
    }
  });
  
  alert('Key rotated successfully');
};
```

### Backend: Update Endpoint
```python
@router.put("/credentials/{credential_id}")
async def update_credential(
    credential_id: int,
    payload: CredentialUpdate,
    current_user = Depends(verify_admin_token),
    session: AsyncSession = Depends(get_session)
):
    tenant_id = await resolve_tenant(current_user.id)
    
    # Obtener credencial
    cred = await session.get(Credential, credential_id)
    
    if not cred:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    # Validar ownership
    if cred.tenant_id != tenant_id and not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Encriptar nuevo valor
    cred.value = encryptor.encrypt(payload.value)
    cred.updated_at = datetime.utcnow()
    
    await session.commit()
    
    return {"status": "updated"}
```

## 9. Scope: Global vs Tenant

### Global Credentials (Fallback)
```python
# Usar para credenciales compartidas (ej: SMTP del sistema)
# Solo superadmins pueden crear/editar

await save_credential(
    tenant_id=None,  # NULL = global
    category="smtp",
    name="config",
    value=json.dumps(smtp_config),
    scope="global"
)
```

### Tenant-Specific (Preferred)
```python
# Cada tenant provee sus propias keys
await save_credential(
    tenant_id=tenant_id,
    category="openai",
    name="API_KEY",
    value="sk-proj-...",
    scope="tenant"
)
```

### Resolution Logic
1. **Buscar tenant-specific** → Si existe, usar
2. **Fallback a global** → Si no existe tenant-specific
3. **Return None** → Si no existe ninguna

## 10. Metadata (Expiration Tracking)

### Guardar con Metadata
```python
# Para tokens con expiración (ej: Meta Long-Lived Token)
metadata = {
    "expires_at": (datetime.utcnow() + timedelta(days=60)).isoformat(),
    "token_type": "long_lived",
    "auto_refresh": False
}

await save_credential(
    tenant_id=tenant_id,
    category="meta",
    name="long_lived_token",
    value=token,
    metadata=metadata
)
```

### Verificar Expiración
```python
async def check_token_expiration(tenant_id: int) -> bool:
    """
    Retorna True si token está por expirar (< 7 días)
    """
    stmt = select(Credential).where(
        Credential.tenant_id == tenant_id,
        Credential.category == "meta"
    )
    result = await session.execute(stmt)
    cred = result.scalar_one_or_none()
    
    if not cred:
        return False
    
    expires_at_str = cred.metadata.get('expires_at')
    if not expires_at_str:
        return False
    
    expires_at = datetime.fromisoformat(expires_at_str)
    days_remaining = (expires_at - datetime.utcnow()).days
    
    return days_remaining < 7
```

## 11. Troubleshooting

### "Decryption Error"
```
Causa: INTERNAL_SECRET_KEY cambió después de encriptar
Solución: NUNCA cambiar INTERNAL_SECRET_KEY en producción
```

### "Credential not found"
```
Causa: tenant_id incorrecto (UUID vs Integer)
Solución: Usar resolve_tenant(current_user.id) siempre
```

### "403 Forbidden on global credential"
```
Causa: Usuario no es superadmin
Solución: Solo superadmins pueden gestionar scope='global'
```

## 12. Security Best Practices

### ✅ DO
- Usar HTTPS siempre
- Encriptar valores antes de guardar
- Validar ownership antes de editar/borrar
- Maskear valores en listados
- Rotar keys periódicamente

### ❌ DON'T
- Enviar valores sin encriptar
- Guardar en localStorage (frontend)
- Exponer valores completos en logs
- Permitir edición cross-tenant
- Hardcodear keys en código

## 13. Checklist de Implementación

### Frontend
- [ ] Formularios por categoría (OpenAI, Google, SMTP)
- [ ] Input type="password" para keys
- [ ] Lista de credenciales con valores masked
- [ ] Botón de rotación funcional
- [ ] Indicador de scope (global vs tenant)
- [ ] Delete con confirmación

### Backend
- [ ] Encriptación AES-256 implementada
- [ ] get_tenant_credential con fallback
- [ ] Upsert logic (insert or update)
- [ ] Validación de ownership
- [ ] Endpoint de listado masked
- [ ] Metadata para expiración

---

**Tip**: Nunca loggear valores desencriptados. Usar `logger.info(f"Using credential for {category}")` sin exponer el valor.
