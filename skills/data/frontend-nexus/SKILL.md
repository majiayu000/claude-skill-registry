---
name: "Nexus UI Developer"
description: "Especialista en React 18, TypeScript, Tailwind CSS y conexión con API multi-tenant."
trigger: "frontend, react, tsx, componentes, UI, vistas, hooks"
scope: "FRONTEND"
auto-invoke: true
---

# Nexus UI Developer - Platform AI Solutions

## 1. Core Architecture

### Tech Stack
- **React 18** + TypeScript + Vite
- **TailwindCSS** + Vanilla CSS (`index.css` para Glassmorphism)
- **Lucide Icons** para iconografía
- **React Router** para navegación

### Estructura de Proyecto
```
frontend_react/
├── src/
│   ├── views/              # Páginas completas (rutas)
│   │   ├── Chats.tsx       # Omnichannel HUD
│   │   ├── Agents.tsx      # Configuración de IA
│   │   ├── Knowledge.tsx   # RAG/Sovereign Library
│   │   ├── Settings.tsx    # Configuración
│   │   │   └── Credentials.tsx  # The Vault UI
│   │   │   └── Integrations.tsx # Meta/TiendaNube
│   │   └── MagicOnboarding.tsx  # SSE 7-agent wizard
│   ├── components/         # Reutilizables
│   ├── hooks/              
│   │   └── useApi.ts       # ¡CRÍTICO! Hook universal
│   ├── services/
│   └── types/
```

## 2. The Sovereign API Hook (useApi)

### **REGLA DE ORO**: SIEMPRE usar `useApi` para llamadas al backend

```tsx
import { useApi } from '../hooks/useApi';

interface Agent {
  id: number;
  name: string;
  model_provider: string;
  tenant_id: number;
}

export const AgentsList: React.FC = () => {
  const { data, isLoading, error, execute } = useApi<Agent[]>();

  useEffect(() => {
    execute({
      method: 'GET',
      url: '/admin/agents'
    });
  }, []);

  if (isLoading) return <Spinner />;
  if (error) return <ErrorAlert message={error} />;

  return (
    <div>
      {data?.map(agent => (
        <AgentCard key={agent.id} agent={agent} />
      ))}
    </div>
  );
};
```

### ¿Por qué useApi?
1. **Auto-inyecta** `X-Admin-Token` header
2. **Maneja** loading/error states
3. **Centraliza** lógica de autenticación
4. **Garantiza** multi-tenant isolation

### POST/PUT/DELETE
```tsx
const { execute, isLoading } = useApi<Agent>();

const createAgent = async () => {
  await execute({
    method: 'POST',
    url: '/admin/agents',
    data: {
      name: 'Sales Agent',
      role: 'sales',
      model_provider: 'openai',
      model_version: 'gpt- 5-mini'
    }
  });
};
```

## 3. TypeScript Strict Typing

### Interfaces Obligatorias
```tsx
// types/agent.ts
export interface Agent {
  id: number;
  tenant_id: number;
  name: string;
  role: 'sales' | 'support' | 'leads';
  model_provider: 'openai' | 'google';
  model_version: string;
  temperature: number;
  enabled_tools: string[];
  channels: Array<'whatsapp' | 'instagram' | 'facebook' | 'web'>;
  config: AgentConfig;
  is_active: boolean;
}

export interface AgentConfig {
  reasoning_effort?: 'none' | 'low' | 'medium' | 'high';
  text_verbosity?: 'concise' | 'detailed' | 'bullet_points';
  agent_tone?: string;
}

export interface AgentCreate {
  name: string;
  role: string;
  model_provider: string;
  model_version: string;
  // ...
}
```

### **PROHIBIDO**: `any`
```tsx
// ❌ MAL
const handleClick = (data: any) => {}

// ✅ BIEN
const handleClick = (data: Agent) => {}
```

## 4. Components Pattern

### Functional Components
```tsx
interface ChatMessageProps {
  content: string;
  role: 'user' | 'agent';
  timestamp: Date;
  onDelete?: () => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  content,
  role,
  timestamp,
  onDelete
}) => {
  return (
    <div className={`message ${role}`}>
      <p>{content}</p>
      <span className="text-xs text-gray-500">
        {timestamp.toLocaleTimeString()}
      </span>
      {onDelete && (
        <button onClick={onDelete} className="text-red-500">
          <Trash2 size={16} />
        </button>
      )}
    </div>
  );
};
```

## 5. Credential Security (Masked Values)

### **NUNCA** mostrar API keys en plain text

```tsx
import { Eye, EyeOff } from 'lucide-react';

interface MaskedCredentialProps {
  value: string;  // "sk-proj...1a2b" (masked por backend)
}

export const MaskedCredential: React.FC<MaskedCredentialProps> = ({ value }) => {
  const [revealed, setRevealed] = useState(false);

  // Backend devuelve máscara, NO valor real
  const displayValue = revealed ? value : '•'.repeat(20);

  return (
    <div className="flex items-center gap-2">
      <input
        type="text"
        value={displayValue}
        readOnly
        className="font-mono bg-gray-100 px-3 py-2 rounded w-full"
      />
      <button
        onClick={() => setRevealed(!revealed)}
        className="text-blue-500"
      >
        {revealed ? <EyeOff size={18} /> : <Eye size={18} />}
      </button>
    </div>
  );
};
```

## 6. Key Views (Sovereign Hub)

### Credentials.tsx (The Vault UI)
```tsx
// Categorías de credenciales
const CATEGORIES = ['openai', 'google', 'smtp', 'tiendanube', 'whatsapp_cloud'];

// Crear credencial
const createCredential = async () => {
  await execute({
    method: 'POST',
    url: '/admin/credentials',
    data: {
      name: 'OPENAI_API_KEY',
      value: apiKeyInput,
      category: 'openai',
      scope: 'tenant'  // 'global' o 'tenant'
    }
  });
};
```

### Knowledge.tsx (RAG Management)
```tsx
// Upload documento
const handleUpload = async (file: File, collection: string) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('collection', collection);  // General, ADN Personal, Shadow RAG

  await execute({
    method: 'POST',
    url: '/admin/knowledge/upload',
    data: formData
  });
};

// Eliminar documento (Hard Delete)
const handleDelete = async (docId: string) => {
  if (confirm('¿Eliminar documento?')) {
    await execute({
      method: 'DELETE',
      url: `/admin/knowledge/${docId}`
    });
  }
};
```

### MagicOnboarding.tsx (SSE Protocol Omega)
```tsx
// Server-Sent Events para streaming
const [events, setEvents] = useState<string[]>([]);

useEffect(() => {
  const eventSource = new EventSource('/admin/onboarding/stream');
  
  eventSource.onmessage = (event) => {
    setEvents(prev => [...prev, event.data]);
  };

  eventSource.onerror = () => {
    eventSource.close();
  };

  return () => eventSource.close();
}, []);
```

## 7. Tailwind CSS Standards

### Glassmorphism (index.css)
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### Responsive Design
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {agents.map(agent => (
    <AgentCard key={agent.id} {...agent} />
  ))}
</div>
```

### Conditional Classes
```tsx
const buttonClasses = `
  px-4 py-2 rounded font-medium transition
  ${variant === 'primary' ? 'bg-blue-500 text-white' : 'bg-gray-200'}
  ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-80'}
`;
```

## 8. Forms & Validation

### Controlled Inputs
```tsx
const [formData, setFormData] = useState<AgentCreate>({
  name: '',
  role: 'sales',
  model_provider: 'openai',
  model_version: 'gpt-5-mini'
});

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setFormData({
    ...formData,
    [e.target.name]: e.target.value
  });
};

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  await createAgent(formData);
};
```

## 9. Error Handling (Protocol Omega)

### Error Display
```tsx
if (error) {
  return (
    <div className="bg-red-50 border border-red-200 rounded p-4">
      <h3 className="text-red-800 font-bold">Error</h3>
      <p className="text-red-600">{error}</p>
    </div>
  );
}
```

### Toast Notifications
```tsx
import { toast } from 'react-hot-toast';

const handleSave = async () => {
  try {
    await execute({ method: 'POST', url: '/admin/agents', data });
    toast.success('Agent created successfully');
  } catch (err) {
    toast.error('Failed to create agent');
  }
};
```

## 10. Omnichannel Components

### Channel Selector
```tsx
const CHANNELS = ['whatsapp', 'instagram', 'facebook', 'web'];

<div className="flex gap-2">
  {CHANNELS.map(channel => (
    <label key={channel} className="flex items-center gap-2">
      <input
        type="checkbox"
        checked={selectedChannels.includes(channel)}
        onChange={() => toggleChannel(channel)}
      />
      <span className="capitalize">{channel}</span>
    </label>
  ))}
</div>
```

## 11. Icons (Lucide React)

```tsx
import { 
  MessageSquare,  // Chats
  Settings,       // Configuración
  Database,       // Knowledge
  ShoppingCart,   // Tienda Nube
  Zap,            // Agentes
  Key,            // Credentials
  Trash2,         // Delete
  Upload          // Upload
} from 'lucide-react';

<button className="flex items-center gap-2">
  <MessageSquare size={20} />
  <span>Chats</span>
</button>
```

## 12. Performance

### React.memo
```tsx
export const AgentCard = React.memo<AgentCardProps>(({ agent }) => {
  return <div>{agent.name}</div>;
});
```

### useMemo / useCallback
```tsx
const filteredAgents = useMemo(() => {
  return agents.filter(a => a.is_active);
}, [agents]);

const handleDelete = useCallback((id: number) => {
  // ...
}, []);
```

## 13. Checklist Pre-Commit

- [ ] ¿Se usa `useApi` para todas las llamadas API?
- [ ] ¿Las interfaces TypeScript están definidas?
- [ ] ¿No hay `any` en el código?
- [ ] ¿Las credenciales se muestran enmascaradas?
- [ ] ¿Los loading states tienen feedback visual?
- [ ] ¿Los errores se muestran al usuario?
- [ ] ¿Las clases Tailwind son responsive?
- [ ] ¿Los formularios usan `e.preventDefault()`?
- [ ] ¿Las listas tienen `key` único?
- [ ] ¿No hay `console.log` en producción?
