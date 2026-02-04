---
name: "Meta Integration Diplomat"
description: "Especialista en OAuth Meta (Facebook, Instagram, WhatsApp Business) y gestión de activos de negocio."
trigger: "meta, facebook, instagram, whatsapp, oauth, integration, waba, pages"
scope: "INTEGRATIONS"
auto-invoke: true
---

# Meta Integration Diplomat - Platform AI Solutions

## 1. El Protocolo "Meta Diplomat"

### Concepto
La integración con Meta **NO es simple OAuth**. Es una **Vinculación de Activos de Negocio** (Business Assets) que conecta:
- **Facebook Pages** → Páginas de negocio (Graph API)
- **Instagram Accounts** → Cuentas comerciales (Graph API)
- **WhatsApp Business Accounts (WABA)** → Números de teléfono (WhatsApp Cloud API) -> *Protocolo diferente*

### Arquitectura
```
Frontend (MetaSettings.tsx)
    ↓
FB SDK Loader → FB.login() popup
    ↓
Authorization Code (efímero)
    ↓
POST /admin/meta/connect → Backend Exchange
    ↓
Long-Lived User Token (60 días)
    ↓
Auto-Discovery (Pages, IG, WABA)
    ↓
Wizard Selection → Persist Assets
```

## 2. Frontend: SDK Loader

### useFacebookSdk Hook
```typescript
// hooks/useFacebookSdk.ts
import { useEffect, useState } from 'react';

export const useFacebookSdk = (configId: string) => {
  const [sdkLoaded, setSdkLoaded] = useState(false);
  
  useEffect(() => {
    // Inyectar script de Meta
    const script = document.createElement('script');
    script.src = 'https://connect.facebook.net/en_US/sdk.js';
    script.async = true;
    script.defer = true;
    
    script.onload = () => {
      window.FB.init({
        appId: configId,
        cookie: true,
        xfbml: true,
        version: 'v18.0'
      });
      setSdkLoaded(true);
    };
    
    document.body.appendChild(script);
  }, [configId]);
  
  return sdkLoaded;
};
```

### Environment Variable
```typescript
// .env
VITE_META_CONFIG_ID=123456789012345  // Meta App Config ID
```

## 3. OAuth Flow (Popup)

### Iniciar Conexión
```typescript
const connectMeta = () => {
  if (!window.FB) {
    alert('Meta SDK not loaded. Check ad-blocker.');
    return;
  }
  
  window.FB.login((response) => {
    if (response.authResponse) {
      // Usuario autorizó
      const code = response.authResponse.code;
      handleMetaCallback(code);
    } else {
      // Usuario canceló
      console.log('User cancelled login');
    }
  }, {
    config_id: VITE_META_CONFIG_ID,
    response_type: 'code',  // CRÍTICO: queremos code, no token
    override_default_response_type: true,
    scope: 'pages_show_list,instagram_basic,whatsapp_business_messaging'
  });
};
```

### Permisos Requeridos
- `pages_show_list`: Ver páginas administradas
- `instagram_basic`: Acceso a cuentas IG Business
- `instagram_manage_messages`: Enviar/recibir mensajes IG
- `whatsapp_business_messaging`: Acceso a WABA
- `whatsapp_business_management`: Gestionar configuración WABA

## 4. Backend: Token Exchange

### Endpoint de Conexión
```python
# orchestrator_service/app/api/v1/endpoints/integrations.py

@router.post("/meta/connect")
async def connect_meta(
    payload: MetaConnectRequest,
    current_user = Depends(verify_admin_token),
    session: AsyncSession = Depends(get_session)
):
    """
    Intercambia authorization code por Long-Lived Token
    y descubre activos disponibles
    """
    tenant_id = await resolve_tenant(current_user.id)
    
    # Validar redirect_uri
    if not payload.redirect_uri.startswith(ALLOWED_ORIGINS[0]):
        raise HTTPException(
            status_code=400,
            detail="Invalid redirect_uri"
        )
    
    # Llamar a meta_service para exchange
    response = await httpx.post(
        "http://meta_service:8002/connect",
        json={
            "code": payload.code,
            "redirect_uri": payload.redirect_uri,
            "tenant_id": tenant_id
        },
        headers={"X-Internal-Secret": INTERNAL_SECRET_KEY},
        timeout=30.0
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get('detail', 'Meta connection failed')
        )
    
    data = response.json()
    
    return {
        "status": "success",
        "assets": data.get("assets", {}),
        "connected": {
            "facebook": bool(data.get("assets", {}).get("pages")),
            "instagram": bool(data.get("assets", {}).get("instagram")),
            "whatsapp": bool(data.get("assets", {}).get("whatsapp"))
        }
    }
```


    # ...

### 🛠️ Omnichannel Routing v6.1 (Triangular)
A partir de v6.1, el Orchestrator centraliza el ruteo. 
- **Meta Direct**: Prioridad si hay tokens de Meta.
- **Chatwoot**: Gateway secundario para FB/IG si IDs están presentes.
- **YCloud**: Gateway exclusivo para WhatsApp.

Toda comunicación hacia FB/IG/WA debe pasar por `unified_message_delivery` en el Orchestrator.

## 5. Meta Service: Token Exchange & Discovery


### Exchange Code por Token
```python
# meta_service/main.py

@app.post("/connect")
async def exchange_code(
    payload: ConnectRequest,
    x_internal_secret: str = Header(None)
):
    # Validar secret interno
    if x_internal_secret != INTERNAL_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Exchange code por access_token
    token_response = requests.post(
        "https://graph.facebook.com/v18.0/oauth/access_token",
        params={
            "client_id": META_APP_ID,
            "client_secret": META_APP_SECRET,
            "code": payload.code,
            "redirect_uri": payload.redirect_uri
        }
    )
    
    if token_response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Meta token exchange failed: {token_response.text}"
        )
    
    access_token = token_response.json()['access_token']
    
    # Convertir a Long-Lived Token (60 días)
    ll_response = requests.get(
        "https://graph.facebook.com/v18.0/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": META_APP_ID,
            "client_secret": META_APP_SECRET,
            "fb_exchange_token": access_token
        }
    )
    
    long_lived_token = ll_response.json()['access_token']
    
    # Auto-Discovery de activos
    assets = await discover_assets(long_lived_token)
    
    # Guardar token en Orchestrator Vault
    await save_to_vault(
        tenant_id=payload.tenant_id,
        token=long_lived_token,
        assets=assets
    )
    
    return {"status": "success", "assets": assets}
```

### Auto-Discovery
```python
async def discover_assets(access_token: str) -> dict:
    """
    Descubre automáticamente Pages, Instagram, WABA
    """
    # 1. Obtener User ID
    me_response = requests.get(
        "https://graph.facebook.com/v18.0/me",
        params={"access_token": access_token}
    )
    user_id = me_response.json()['id']
    
    # 2. Páginas administradas
    pages_response = requests.get(
        f"https://graph.facebook.com/v18.0/{user_id}/accounts",
        params={
            "access_token": access_token,
            "fields": "id,name,access_token,category"
        }
    )
    pages = pages_response.json().get('data', [])
    
    # 3. Instagram Business Accounts (vinculadas a Pages)
    instagram_accounts = []
    for page in pages:
        ig_response = requests.get(
            f"https://graph.facebook.com/v18.0/{page['id']}",
            params={
                "access_token": access_token,
                "fields": "instagram_business_account"
            }
        )
        if 'instagram_business_account' in ig_response.json():
            ig_id = ig_response.json()['instagram_business_account']['id']
            instagram_accounts.append({
                "id": ig_id,
                "page_id": page['id'],
                "page_name": page['name']
            })
    
    # 4. WhatsApp Business Accounts
    waba_response = requests.get(
        f"https://graph.facebook.com/v18.0/{user_id}/businesses",
        params={
            "access_token": access_token,
            "fields": "owned_whatsapp_business_accounts{id,name,phone_numbers}"
        }
    )
    
    whatsapp_accounts = []
    businesses = waba_response.json().get('data', [])
    for business in businesses:
        wabas = business.get('owned_whatsapp_business_accounts', {}).get('data', [])
        for waba in wabas:
            whatsapp_accounts.append({
                "id": waba['id'],
                "name": waba.get('name', 'Unknown'),
                "phone_numbers": waba.get('phone_numbers', [])
            })
    
    return {
        "pages": pages,
        "instagram": instagram_accounts,
        "whatsapp": whatsapp_accounts
    }
```

## 6. Wizard de Selección (Frontend)

### MetaOnboardingWizard Component
```tsx
interface MetaOnboardingWizardProps {
  assets: DiscoveredAssets;
  onComplete: (selected: SelectedAssets) => void;
}

const MetaOnboardingWizard: React.FC<MetaOnboardingWizardProps> = ({
  assets,
  onComplete
}) => {
  const [selectedPage, setSelectedPage] = useState<string | null>(null);
  const [selectedIG, setSelectedIG] = useState<string | null>(null);
  const [selectedWABA, setSelectedWABA] = useState<string | null>(null);
  
  const handleSave = async () => {
    // Persistir selección en backend
    await useApi({
      method: 'POST',
      url: '/admin/meta/configure',
      data: {
        page_id: selectedPage,
        instagram_account_id: selectedIG,
        waba_id: selectedWABA
      }
    });
    
    onComplete({
      page_id: selectedPage,
      instagram_id: selectedIG,
      waba_id: selectedWABA
    });
  };
  
  return (
    <div className="wizard">
      <h2>Select Your Business Assets</h2>
      
      {/* Pages */}
      <section>
        <h3>Facebook Pages</h3>
        {assets.pages.map(page => (
          <label key={page.id}>
            <input
              type="radio"
              name="page"
              value={page.id}
              onChange={() => setSelectedPage(page.id)}
            />
            {page.name}
          </label>
        ))}
      </section>
      
      {/* Similar para Instagram y WhatsApp */}
      
      <button onClick={handleSave}>Save Configuration</button>
    </div>
  );
};
```

## 7. Persistir Assets (Backend)

### Guardar en Tenants Table
```python
@router.post("/meta/configure")
async def configure_meta_assets(
    payload: MetaConfigureRequest,
    current_user = Depends(verify_admin_token),
    session: AsyncSession = Depends(get_session)
):
    tenant_id = await resolve_tenant(current_user.id)
    
    # Actualizar tenant con assets seleccionados
    stmt = update(Tenant).where(
        Tenant.id == tenant_id
    ).values(
        meta_page_id=payload.page_id,
        instagram_account_id=payload.instagram_account_id,
        whatsapp_business_account_id=payload.waba_id
    )
    
    await session.execute(stmt)
    await session.commit()
    
    return {"status": "configured"}
```

## 8. Estado "Connected" (UI)

### Verificar Conexión
```typescript
const checkMetaConnection = async () => {
  const status = await useApi<ConnectionStatus>({
    method: 'GET',
    url: '/admin/integrations/status'
  });
  
  return {
    facebook: status.meta_page_id != null,
    instagram: status.instagram_account_id != null,
    whatsapp: status.whatsapp_business_account_id != null
  };
};
```

### Indicadores Visuales
```tsx
const MetaStatus: React.FC = () => {
  const [status, setStatus] = useState<ConnectionStatus | null>(null);
  
  useEffect(() => {
    loadStatus();
  }, []);
  
  return (
    <div className="grid grid-cols-3 gap-4">
      {/* Facebook */}
      <div className={status?.facebook ? 'border-green-500' : 'border-gray-300'}>
        <Facebook size={32} />
        <span>{status?.facebook ? '✓ Connected' : '○ Not Connected'}</span>
      </div>
      
      {/* Instagram */}
      <div className={status?.instagram ? 'border-pink-500' : 'border-gray-300'}>
        <Instagram size={32} />
        <span>{status?.instagram ? '✓ Connected' : '○ Not Connected'}</span>
      </div>
      
      {/* WhatsApp */}
      <div className={status?.whatsapp ? 'border-green-500' : 'border-gray-300'}>
        <MessageCircle size={32} />
        <span>{status?.whatsapp ? '✓ Connected' : '○ Not Connected'}</span>
      </div>
    </div>
  );
};
```

## 9. Redirect URI (Critical Configuration)

### Configuración en Meta Developers
```
App Dashboard → Settings → Basic
Valid OAuth Redirect URIs:
  https://yourdomain.com/
  http://localhost:5173/ (desarrollo)
```

### Frontend Dynamic URI
```typescript
// DEBE coincidir EXACTAMENTE con lo configurado en Meta
const redirect_uri = `${window.location.origin}/`;

// Enviar al backend
await connectMeta(code, redirect_uri);
```

### Error Común
```
❌ Error: "Invalid Redirect URI"
Causa: La URI enviada no está en la whitelist de Meta

Solución:
1. Verificar en Meta Developers
2. Asegurar NO trailing slash si no está configurado
3. window.location.origin + '/' debe coincidir
```

## 10. Troubleshooting

### "App not configured" en Popup
```
Causa: VITE_META_CONFIG_ID incorrecto
Solución: Verificar en Meta Developers → App Settings
```

### "SDK is undefined" (window.FB)
```
Causa: Ad-blocker bloqueó connect.facebook.net
Solución: Desactivar ad-blocker o usar dominio whitelist
```

### "Permissions Missing" Error
```
Causa: Usuario desmarcó permisos en popup
Solución: Re-iniciar flujo y asegurar todos los permisos
```

### "OAuthException" en Backend
```
Causa: Token vencido o revocado
Solución: Re-autenticar (Long-Lived Tokens duran 60 días)
```

### "No assets found" en Wizard
```
Causa: Usuario no tiene Pages/WABA creadas
Solución: 
1. Crear Facebook Page
2. Vincular Instagram Business Account
3. Registrar WhatsApp Business Account
```

## 11. Security Best Practices

### Never Expose Tokens en Frontend
```typescript
// ❌ MAL - Token en localStorage
localStorage.setItem('meta_token', token);

// ✅ BIEN - Solo en backend vault
await saveToVault(token);
```

### Validar X-Internal-Secret
```python
# En meta_service, SIEMPRE validar
if x_internal_secret != INTERNAL_SECRET_KEY:
    raise HTTPException(status_code=403)
```

## 12. Token Refresh Strategy

### Long-Lived Token Lifecycle
- **Duración**: 60 días
- **Renovación**: No auto-refresh, re-autenticar cuando expire
- **Monitoreo**: Guardar `expires_at` en credentials metadata

```python
# Al guardar token
metadata = {
    "expires_at": (datetime.utcnow() + timedelta(days=60)).isoformat(),
    "token_type": "long_lived"
}

cred = Credential(
    tenant_id=tenant_id,
    category="meta",
    value=encrypted_token,
    metadata=metadata
)
```

## 13. Checklist de Implementación

### Frontend
- [ ] SDK Loader implementado (useFacebookSdk)
- [ ] Popup OAuth funcional (FB.login)
- [ ] Redirect URI correcto (window.location.origin + '/')
- [ ] Wizard de selección de assets
- [ ] Indicadores visuales de conexión
- [ ] Manejo de errores (ad-blocker, cancel)

### Backend (Orchestrator)
- [ ] Endpoint /meta/connect
- [ ] Validación de redirect_uri
- [ ] Comunicación con meta_service
- [ ] Persistencia de assets en tenants table
- [ ] Status endpoint (/integrations/status)

### Backend (Meta Service)
- [ ] Token exchange (code → access_token)
- [ ] Long-Lived Token conversion
- [ ] Auto-Discovery (Pages, IG, WABA)
- [ ] Vault injection
- [ ] X-Internal-Secret validation
- [ ] Error handling (Meta API failures)

---

**Tip**: Usar Meta's Graph API Explorer (developers.facebook.com/tools/explorer) para probar manualmente permisos y descubrimiento de assets.
