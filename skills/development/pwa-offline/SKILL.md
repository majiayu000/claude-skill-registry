---
name: pwa-offline
description: Modo offline / PWA para áreas sem internet
---

Estratégias para Progressive Web App com suporte offline, essencial para os 12 milhões de domicílios sem internet estável.

## Contexto

- 12 milhões de domicílios sem internet no Brasil
- 12,1% da zona rural sem cobertura alguma
- Muitos usuários têm dados móveis limitados (pré-pago)
- PWA permite instalar o app sem passar pela Play Store

## Configuração PWA

### manifest.json
```json
{
  "name": "Tá na Mão - Seus Benefícios",
  "short_name": "Tá na Mão",
  "description": "Descubra seus benefícios sociais",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#F99500",
  "orientation": "portrait",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

### Service Worker - Estratégias de Cache
```typescript
// frontend/src/sw.ts
import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { BackgroundSyncPlugin } from 'workbox-background-sync';

// 1. Pre-cache: shell da aplicação (HTML, CSS, JS)
precacheAndRoute(self.__WB_MANIFEST);
cleanupOutdatedCaches();

// 2. Cache-First: catálogo de benefícios (muda pouco)
registerRoute(
  ({ url }) => url.pathname.startsWith('/data/benefits/'),
  new CacheFirst({
    cacheName: 'beneficios-cache',
    plugins: [
      new ExpirationPlugin({ maxAgeSeconds: 7 * 24 * 60 * 60 }), // 7 dias
    ],
  })
);

// 3. Network-First: API de elegibilidade (precisa de dados frescos)
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    plugins: [
      new ExpirationPlugin({ maxAgeSeconds: 24 * 60 * 60 }), // 1 dia
    ],
    networkTimeoutSeconds: 5, // fallback para cache após 5s
  })
);

// 4. Stale-While-Revalidate: imagens e ícones
registerRoute(
  ({ request }) => request.destination === 'image',
  new StaleWhileRevalidate({
    cacheName: 'images-cache',
    plugins: [
      new ExpirationPlugin({ maxEntries: 60 }),
    ],
  })
);
```

### Background Sync - Formulários Offline
```typescript
// 5. Background Sync: formulários preenchidos offline
const bgSyncPlugin = new BackgroundSyncPlugin('formularios-pendentes', {
  maxRetentionTime: 7 * 24 * 60, // 7 dias em minutos
  onSync: async ({ queue }) => {
    let entry;
    while ((entry = await queue.shiftRequest())) {
      try {
        await fetch(entry.request);
      } catch (error) {
        await queue.unshiftRequest(entry);
        throw error;
      }
    }
  },
});

registerRoute(
  ({ url }) => url.pathname.startsWith('/api/v2/benefits/eligibility/'),
  new NetworkFirst({
    plugins: [bgSyncPlugin],
  }),
  'POST'
);
```

## IndexedDB - Armazenamento Local

### Schema
```typescript
// frontend/src/db/offline-db.ts
import Dexie from 'dexie';

class TaNaMaoDB extends Dexie {
  beneficios!: Dexie.Table<Beneficio, string>;
  resultados!: Dexie.Table<ResultadoElegibilidade, string>;
  formulariosPendentes!: Dexie.Table<FormularioPendente, string>;
  crasProximos!: Dexie.Table<CrasInfo, string>;

  constructor() {
    super('TaNaMaoDB');
    this.version(1).stores({
      beneficios: 'id, scope, state, category, status',
      resultados: 'id, cpfHash, timestamp',
      formulariosPendentes: 'id, tipo, timestamp, sincronizado',
      crasProximos: 'id, municipio, lat, lng',
    });
  }
}

export const db = new TaNaMaoDB();
```

### Sincronização
```typescript
// frontend/src/services/sync-service.ts
export class SyncService {
  /**
   * Baixa catálogo de benefícios para uso offline.
   * Chamar quando usuário tiver conexão.
   */
  async sincronizarBeneficios(): Promise<void> {
    const response = await fetch('/api/v2/benefits/');
    const beneficios = await response.json();
    await db.beneficios.bulkPut(beneficios.data);
    localStorage.setItem('ultimaSync', new Date().toISOString());
  }

  /**
   * Salva resultado de elegibilidade localmente.
   */
  async salvarResultado(resultado: ResultadoElegibilidade): Promise<void> {
    await db.resultados.put({
      ...resultado,
      timestamp: Date.now(),
    });
  }

  /**
   * Envia formulários pendentes quando voltar online.
   */
  async enviarPendentes(): Promise<number> {
    const pendentes = await db.formulariosPendentes
      .where('sincronizado').equals(0)
      .toArray();

    let enviados = 0;
    for (const form of pendentes) {
      try {
        await fetch(form.endpoint, {
          method: 'POST',
          body: JSON.stringify(form.dados),
          headers: { 'Content-Type': 'application/json' },
        });
        await db.formulariosPendentes.update(form.id!, { sincronizado: 1 });
        enviados++;
      } catch {
        break; // parar se perder conexão novamente
      }
    }
    return enviados;
  }
}
```

## Detecção de Conectividade

```typescript
// frontend/src/hooks/useOnlineStatus.ts
import { useState, useEffect } from 'react';

export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [wasOffline, setWasOffline] = useState(false);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      if (wasOffline) {
        // Disparar sincronização
        syncService.enviarPendentes();
        setWasOffline(false);
      }
    };
    const handleOffline = () => {
      setIsOnline(false);
      setWasOffline(true);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [wasOffline]);

  return { isOnline, wasOffline };
}
```

## Banner Offline
```tsx
// frontend/src/components/OfflineBanner.tsx
export function OfflineBanner() {
  const { isOnline } = useOnlineStatus();

  if (isOnline) return null;

  return (
    <div className="bg-yellow-600 text-white text-center py-2 text-sm">
      Você está sem internet. Algumas coisas ainda funcionam.
    </div>
  );
}
```

## O que Funciona Offline
| Funcionalidade | Offline | Observação |
|---------------|---------|------------|
| Catálogo de benefícios | Sim | Cache local (7 dias) |
| Wizard de elegibilidade | Parcial | Formulário salvo, resultado ao voltar online |
| Checklist de documentos | Sim | Cache local |
| Telefones de emergência | Sim | Dados estáticos |
| Consulta por CPF | Não | Requer API |
| Buscar CRAS no mapa | Não | Requer Google Maps |
| Chat com agente | Não | Requer Gemini |

## Otimização de Banda
```typescript
// Compressão de assets
// vite.config.ts
import viteCompression from 'vite-plugin-compression';

export default defineConfig({
  plugins: [
    viteCompression({ algorithm: 'brotli' }),  // ~70% menor que gzip
    viteCompression({ algorithm: 'gzip' }),
  ],
});
```

## Arquivos Relacionados
- `frontend/src/sw.ts` - Service Worker
- `frontend/src/db/offline-db.ts` - IndexedDB schema
- `frontend/src/services/sync-service.ts` - Sincronização
- `frontend/src/hooks/useOnlineStatus.ts` - Hook de conectividade
- `frontend/public/manifest.json` - Manifesto PWA
- `frontend/vite.config.ts` - Configuração de build

## Testes
```bash
# Simular offline no Chrome DevTools
# Network tab → Offline checkbox

# Lighthouse PWA audit
npx lighthouse http://localhost:5173 --only-categories=pwa

# Verificar service worker
chrome://serviceworker-internals/
```

## Checklist PWA
- [ ] manifest.json com ícones corretos
- [ ] Service Worker registrado
- [ ] Cache de shell da aplicação
- [ ] Cache de catálogo de benefícios
- [ ] IndexedDB para dados offline
- [ ] Background Sync para formulários
- [ ] Banner de status offline
- [ ] Lighthouse PWA score > 90
- [ ] Testado em 3G lento (Chrome DevTools)
