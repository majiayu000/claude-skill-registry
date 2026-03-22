---
name: realtime
description: >-
  Implementa WebSockets com Laravel Reverb para funcionalidades em tempo real. Use quando precisar adicionar WebSockets, broadcasting, eventos em tempo real, ou notificações push.
compatibility: PHP 8.2+, Laravel 11+, Laravel Reverb
metadata:
  author: aronpc
  version: 1.0.0
  category: laravel
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# realtime

## Resumo
Implementa WebSockets com Laravel Reverb para comunicação em tempo real.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `actions` | Para broadcasting de events |
| `testing` | Para testar WebSockets |
| `mcp` | Para validar realtime no browser |
| `cicd` | Para deploy com Reverb |

## Quando usar

Use esta skill sempre que:
- Implementar WebSockets com Laravel Reverb
- Criar canais presence/private/public
- Fazer broadcasting de events
- Configurar autenticação de canais
- Integrar com frontend React
- Criar notificações em tempo real
- Debugar conexões WebSocket

## Stack Tecnológico

**Backend:** Laravel Reverb (WebSockets)

**Frontend:** React + Echo ou Browser WebSocket API

## Instalação

### Instalar Laravel Reverb

```bash
composer require laravel/reverb
php artisan reverb:install
npm install laravel-echo pusher-js
```

### Configurar Reverb

```env
# .env
REVERB_APP_ID=local-app
REVERB_APP_KEY=local-key
REVERB_APP_SECRET=local-secret
REVERB_HOST=localhost
REVERB_PORT=8081
REVERB_SCHEME=http
VITE_REVERB_APP_KEY="${REVERB_APP_KEY}"
```

## Broadcasting Events

### Criar Event

```bash
php artisan make:event OrderStatusChanged
```

```php
<?php

declare(strict_types=1);

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;

final class OrderStatusChanged implements ShouldBroadcast
{
    use Dispatchable;
    use InteractsWithSockets;

    public function __construct(
        public readonly Order $order,
        public readonly string $oldStatus,
        public readonly string $newStatus,
    ) {}

    /**
     * Canal público.
     */
    public function broadcastOn(): Channel
    {
        return new Channel('orders');
    }

    /**
     * Canal privado.
     */
    public function broadcastOn(): PrivateChannel
    {
        return new PrivateChannel('orders.' . $this->order->id);
    }

    /**
     * Canal presence.
     */
    public function broadcastOn(): PresenceChannel
    {
        return new PresenceChannel('orders.' . $this->order->id);
    }
}
```

### Dispatch Event

```php
// Em Actions ou Controllers
event(new OrderStatusChanged($order, $oldStatus, $newStatus));

// Ou com delay
event(new OrderStatusChanged($order, $oldStatus, $newStatus))->delay(now()->addSeconds(5));
```

## Tipos de Canais

### Public Channel

```php
// Event
public function broadcastOn(): Channel
{
    return new Channel('public-updates');
}

// Autorização: Nenhuma
// Frontend: Echo.channel('public-updates')
```

### Private Channel

```php
// Event
public function broadcastOn(): PrivateChannel
{
    return new PrivateChannel('orders.' . $this->order->id);
}

// Autorização: Required
// Frontend: Echo.private('orders.' . orderId)

// routes/channels.php
Broadcast::channel('orders.{order}', function ($user, Order $order) {
    return $user->tenant_id === $order->tenant_id;
});
```

### Presence Channel

```php
// Event
public function broadcastOn(): PresenceChannel
{
    return new PresenceChannel('tracking.{orderId}');
}

// Autorização: Required
// Frontend: Echo.join('tracking.' + orderId)

// routes/channels.php
Broadcast::channel('tracking.{orderId}', function ($user, $orderId) {
    $order = Order::find($orderId);
    return $order && $user->tenant_id === $order->tenant_id;
});
```

## Autenticação de Canais

### Configurar Channels

```php
<?php

// routes/channels.php
use App\Models\Order;
use App\Models\User;
use Illuminate\Support\Facades\Broadcast;

// Private channel - acesso por usuário
Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->tenant_id === $order->tenant_id;
});

// Private channel - acesso por tenant
Broadcast::channel('tenant.{tenantId}', function (User $user, int $tenantId) {
    return $user->tenant_id === $tenantId;
});

// Presence channel - tracking em tempo real
Broadcast::channel('tracking.{orderId}', function (User $user, int $orderId) {
    $order = Order::find($orderId);
    return $order && $user->tenant_id === $order->tenant_id
        && $user->can('view', $order);
});
```

### Channel Classes

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

final class OrderChannel
{
    public function join(User $user, Order $order): bool
    {
        return $user->tenant_id === $order->tenant_id
            && $user->can('view', $order);
    }
}

// routes/channels.php
Broadcast::channel('orders.{order}', OrderChannel::class);
```

## Frontend React

### Configurar Echo

```typescript
// resources/js/echo.ts
import echo from 'laravel-echo';
import pusher from 'pusher-js';

window.pusher = pusher;

window.Echo = new echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 8081,
    wssPort: import.meta.env.VITE_REVERB_PORT ?? 8081,
    forceTLS: false,
    enabledTransports: ['ws', 'wss'],
});
```

### Ouvir Eventos

```typescript
// Public channel
window.Echo.channel('public-updates')
    .listen('.OrderStatusChanged', (e: any) => {
        console.log('Order status changed:', e.order);
    });

// Private channel
window.Echo.private(`orders.${orderId}`)
    .listen('.OrderStatusChanged', (e: any) => {
        console.log('Order updated:', e.order);
        // Atualizar estado React
        setOrder(e.order);
    });

// Presence channel - tracking
window.Echo.join(`tracking.${orderId}`)
    .here((users: any[]) => {
        console.log('Users watching:', users);
    })
    .joining((user: any) => {
        console.log('User joined:', user);
        // Mostrar notificação
        toast(`${user.name} está acompanhando este pedido`);
    })
    .leaving((user: any) => {
        console.log('User left:', user);
    })
    .error((error: any) => {
        console.error('Presence error:', error);
    });

// Notification channel
window.Echo.private(`App.Models.User.${userId}`)
    .notification((notification: any) => {
        console.log('New notification:', notification);
        // Mostrar toast
        toast(notification.message);
    });
```

### React Hook

```typescript
// resources/js/hooks/useEcho.ts
import { useEffect, useState } from 'react';
import window from 'global';

interface UseEchoOptions {
    channel: string;
    event: string;
    type?: 'public' | 'private' | 'presence';
}

export function useEcho({ channel, event, type = 'public' }: UseEchoOptions) {
    const [data, setData] = useState<any>(null);

    useEffect(() => {
        const echo = (window as any).Echo;
        if (!echo) return;

        let echoChannel;
        switch (type) {
            case 'private':
                echoChannel = echo.private(channel);
                break;
            case 'presence':
                echoChannel = echo.join(channel);
                break;
            default:
                echoChannel = echo.channel(channel);
        }

        const listener = echoChannel.listen(event, (e: any) => {
            setData(e);
        });

        return () => {
            listener.stopListening(channel, event);
        };
    }, [channel, event, type]);

    return data;
}

// Uso
function OrderTracking({ orderId }: { orderId: number }) {
    const update = useEcho({
        channel: `orders.${orderId}`,
        event: '.OrderStatusChanged',
        type: 'private',
    });

    useEffect(() => {
        if (update) {
            // Atualizar UI
        }
    }, [update]);

    return <div>...</div>;
}
```

## Client Notifications

### Backend

```php
<?php

use App\Notifications\OrderUpdated;
use Illuminate\Support\Facades\Notification;

// Enviar notification em tempo real
Notification::send($users, new OrderUpdated($order));
```

### Frontend

```typescript
// Ouvir notifications do usuário atual
window.Echo.private(`App.Models.User.${userId}`)
    .notification((notification: any) => {
        console.log('Notification:', notification);
        // Mostrar toast/badge
    });
```

## Debugging WebSockets

### Verificar Conexão

```typescript
// Verificar status da conexão
window.Echo.connector.pusher.connection.bind('connected', () => {
    console.log('WebSocket connected');
});

window.Echo.connector.pusher.connection.bind('disconnected', () => {
    console.log('WebSocket disconnected');
});

window.Echo.connector.pusher.connection.bind('error', (error: any) => {
    console.error('WebSocket error:', error);
});
```

### Debug Events

```php
// config/broadcasting.php
'default' => env('BROADCAST_CONNECTION', 'reverb'),

'connections' => [
    'reverb' => [
        'driver' => 'reverb',
        'key' => env('REVERB_APP_KEY'),
        'secret' => env('REVERB_APP_SECRET'),
        'app_id' => env('REVERB_APP_ID'),
        'url' => env('REVERB_URL'),
        'host' => env('REVERB_HOST', '127.0.0.1'),
        'port' => env('REVERB_PORT', 8081),
        'scheme' => env('REVERB_SCHEME', 'http'),
        'options' => [
            'cluster' => env('REVERB_CLUSTER', 'mt1'),
            'useTLS' => env('REVERB_SCHEME', 'https') === 'https',
            'client' => env('REVERB_CLIENT', 'laravel-echo'),
            'debug' => env('REVERB_DEBUG', false), // Enable for debug
        ],
    ],
],
```

## Casos de Uso

### Rastreamento em Tempo Real

```php
// Event: TrackingUpdated
public function broadcastOn(): PresenceChannel
{
    return new PresenceChannel('tracking.' . $this->order->id);
}

// Frontend
window.Echo.join(`tracking.${orderId}`)
    .here((users) => setViewers(users))
    .joining((user) => toast(`${user.name} está observando`))
    .leaving((user) => removeViewer(user.id));
```

### Atualizações de Status

```php
// Action: UpdateOrderStatusAction
public function handle(Order $order, string $status): Order
{
    $oldStatus = $order->status;
    $order->update(['status' => $status]);

    event(new OrderStatusChanged($order, $oldStatus, $status));

    return $order;
}

// Frontend
window.Echo.private(`orders.${orderId}`)
    .listen('.OrderStatusChanged', (e) => {
        setOrderStatus(e.order.status);
        toast(__('messages.order_status_updated'));
    });
```

### Chat em Tempo Real

```php
// Event: NewMessage
public function broadcastOn(): PresenceChannel
{
    return new PresenceChannel('chat.' . $this->chat->id);
}

// Frontend
window.Echo.join(`chat.${chatId}`)
    .listen('.NewMessage', (e) => {
        addMessage(e.message);
    });
```

## Performance

### Rate Limiting

```php
// Limitar broadcasts por usuário
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('broadcast', function (Job $job) {
    return Limit::perMinute(100);
});
```

### Queue Broadcasting

```php
// Events podem ser queued
final class LargeDataEvent implements ShouldBroadcast
{
    use InteractsWithSockets;
    use SerializesModels;

    public $queue = 'broadcast'; // Fila específica
    public $connection = 'redis';

    // ...
}
```

## Segurança

### Validar Autorização

```php
// Sempre validar canais private/presence
Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    // Validar tenant ownership
    if ($user->tenant_id !== $order->tenant_id) {
        return false;
    }

    // Validar permissões
    return $user->can('view', $order);
});
```

### Sanitizar Dados

```php
// Não enviar dados sensíveis
public function broadcastWith(): array
{
    return [
        'id' => $this->order->id,
        'status' => $this->order->status,
        // Não enviar: user_id, tenant_id, etc.
    ];
}
```

## Melhores Práticas

### ✅ FAÇA

- Use canais private/presence para dados sensíveis
- Sempre validar autorização de canais
- Use filas para eventos grandes
- Sanitizar dados enviados
- Testar desconexões e reconexões
- Implementar rate limiting
- Usar presence channels para contagem de usuários
- Tratar erros de WebSocket
- Desconectar canais quando não necessário
- Log eventos para debugging

### ❌ NÃO FAÇA

- Não envie dados sensíveis via WebSocket
    - Não ignore autorização de canais
    - Não use canais públicos para dados privados
    - Não esqueça de desconectar canais
    - Não implemente lógica de negócio em frontend
    - Não abuse de broadcasts (rate limit)
    - Não envie payloads muito grandes
    - Não dependa apenas de WebSocket (fallback)

## Checklist de WebSocket

Antes de finalizar feature realtime:

- [ ] Reverb configurado e funcionando
- [ ] Canais criados (public/private/presence)
- [ ] Autorização de canais implementada
- [ ] Events com broadcasting criados
- [ ] Frontend Echo configurado
- [ ] Listeners de events criados
- [ ] Presence channels testados
- [ ] Desconexões tratadas
- [ ] Rate limiting configurado
- [ ] Testes de integração criados

## Referências Cruzadas

- **Actions**: Use com `laravel-actions-events` para dispatch events
- **Exceptions**: Trate erros de WebSocket com `laravel-exceptions`
- **i18n**: Traduza mensagens realtime com `laravel-i18n`
- **Architecture**: Integra com `laravel-architecture` para estrutura

## Referências

- [Laravel Reverb Documentation](https://laravel.com/docs/reverb) - Documentação oficial
- [Laravel Broadcasting](https://laravel.com/docs/broadcasting) - Broadcasting de events
- [Laravel Echo Documentation](https://echo.laravel.com) - Cliente frontend
