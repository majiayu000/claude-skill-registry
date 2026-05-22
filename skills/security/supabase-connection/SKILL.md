---
name: supabase-connection
description: Manejo seguro de autenticación, RLS y conexión a base de datos y storage con Supabase.
trigger: supabase OR database OR db OR storage OR auth
scope: global
---

# Supabase Connection Skill

## Description

Estándares para conectar e interactuar con Supabase (Base de datos, Auth y Storage) tanto desde Frontend como Backend.

## Trigger

- Modificaciones en esquemas de BD (`schema.prisma` o SQL).
- Implementación de Login/Auth.
- Subida de archivos (Storage).
- Edición de políticas RLS.

## Resources

- [Supabase Docs](https://supabase.com/docs)
- [Prisma with Supabase](https://supabase.com/partners/integrations/prisma)

## Best Practices

1.  **Row Level Security (RLS) SIEMPRE:**
    - Nunca desactivar RLS en producción.
    - Definir políticas claras en SQL o mediante Prisma (si aplica).
    - Utilizar `auth.uid()` para restringir acceso a datos de usuario.

2.  **Cliente Tipado:**
    - En Frontend: Usar `createClientComponentClient` o `createServerComponentClient` (Next.js Auth Helpers) para propagar cookies de sesión automáticamente.
    - En Backend (Python): Usar `supabase-py` con la clave `SERVICE_ROLE` **SOLO** para tareas administrativas. Para acciones de usuario, pasar el JWT.

3.  **Variables de Entorno:**
    - `NEXT_PUBLIC_SUPABASE_URL`: URL pública.
    - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Clave pública (segura para navegador).
    - `SUPABASE_SERVICE_ROLE_KEY`: **PRIVADA**. Nunca exponer al cliente.

4.  **Backend (FastAPI) Auth:**
    - Validar el JWT de Supabase en cada endpoint protegido.
    - No confiar ciegamente en el frontend.

## Code Snippets

### Next.js Server Component (Fetch Data)

```typescript
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'

export default async function Page() {
  const supabase = createServerComponentClient({ cookies })
  const { data } = await supabase.from('todos').select()
  return <pre>{JSON.stringify(data, null, 2)}</pre>
}
```

### Python FastAPI (Verify JWT)

```python
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def get_current_user(token: str):
    user = supabase.auth.get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
```
