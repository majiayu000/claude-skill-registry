---
name: react
description: React development including hooks, components, state management, and modern patterns. Activate for React components, JSX, hooks, context, and frontend development.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# React Skill

Provides comprehensive React development capabilities for modern frontend applications.

## When to Use This Skill

Activate this skill when working with:
- React component development
- Hooks implementation
- State management
- Context API usage
- Component patterns and composition

## Project Structure

\`\`\`
src/
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   └── Card.tsx
│   └── features/
│       ├── AgentList.tsx
│       └── TaskPanel.tsx
├── hooks/
│   ├── useAgent.ts
│   └── useTask.ts
├── context/
│   └── AgentContext.tsx
├── services/
│   └── api.ts
├── types/
│   └── index.ts
└── App.tsx
\`\`\`

## Component Patterns

### Functional Component
\`\`\`tsx
import { FC } from 'react';

interface AgentCardProps {
  name: string;
  type: 'claude' | 'gpt' | 'gemini';
  status: 'active' | 'idle' | 'error';
  onSelect?: () => void;
}

export const AgentCard: FC<AgentCardProps> = ({
  name,
  type,
  status,
  onSelect
}) => {
  return (
    <div
      className="agent-card"
      onClick={onSelect}
      role="button"
      tabIndex={0}
    >
      <h3>{name}</h3>
      <span className={`status status-${status}`}>{status}</span>
      <span className="type">{type}</span>
    </div>
  );
};
\`\`\`

### Custom Hooks
\`\`\`tsx
import { useState, useEffect, useCallback } from 'react';

interface Agent {
  id: string;
  name: string;
  status: string;
}

export function useAgent(agentId: string) {
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchAgent = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/agents/${agentId}`);
        const data = await response.json();
        setAgent(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchAgent();
  }, [agentId]);

  const refresh = useCallback(() => {
    // Trigger refetch
  }, [agentId]);

  return { agent, loading, error, refresh };
}
\`\`\`

### Context Provider
\`\`\`tsx
import { createContext, useContext, useReducer, ReactNode } from 'react';

interface AgentState {
  agents: Agent[];
  selectedAgent: Agent | null;
}

type AgentAction =
  | { type: 'SET_AGENTS'; payload: Agent[] }
  | { type: 'SELECT_AGENT'; payload: Agent }
  | { type: 'CLEAR_SELECTION' };

const AgentContext = createContext<{
  state: AgentState;
  dispatch: React.Dispatch<AgentAction>;
} | null>(null);

function agentReducer(state: AgentState, action: AgentAction): AgentState {
  switch (action.type) {
    case 'SET_AGENTS':
      return { ...state, agents: action.payload };
    case 'SELECT_AGENT':
      return { ...state, selectedAgent: action.payload };
    case 'CLEAR_SELECTION':
      return { ...state, selectedAgent: null };
    default:
      return state;
  }
}

export function AgentProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(agentReducer, {
    agents: [],
    selectedAgent: null
  });

  return (
    <AgentContext.Provider value={{ state, dispatch }}>
      {children}
    </AgentContext.Provider>
  );
}

export function useAgentContext() {
  const context = useContext(AgentContext);
  if (!context) {
    throw new Error('useAgentContext must be used within AgentProvider');
  }
  return context;
}
\`\`\`

## Data Fetching with React Query

\`\`\`tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useAgents() {
  return useQuery({
    queryKey: ['agents'],
    queryFn: async () => {
      const response = await fetch('/api/agents');
      return response.json();
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useCreateAgent() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (newAgent: CreateAgentInput) => {
      const response = await fetch('/api/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAgent),
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
  });
}
\`\`\`

## Form Handling

\`\`\`tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const agentSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  type: z.enum(['claude', 'gpt', 'gemini']),
  description: z.string().optional(),
});

type AgentFormData = z.infer<typeof agentSchema>;

export function AgentForm({ onSubmit }: { onSubmit: (data: AgentFormData) => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<AgentFormData>({
    resolver: zodResolver(agentSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} placeholder="Agent name" />
      {errors.name && <span>{errors.name.message}</span>}

      <select {...register('type')}>
        <option value="claude">Claude</option>
        <option value="gpt">GPT</option>
        <option value="gemini">Gemini</option>
      </select>

      <button type="submit" disabled={isSubmitting}>
        Create Agent
      </button>
    </form>
  );
}
\`\`\`

## Performance Optimization

\`\`\`tsx
import { memo, useMemo, useCallback } from 'react';

// Memoized component
export const AgentList = memo(function AgentList({ agents }: { agents: Agent[] }) {
  const sortedAgents = useMemo(
    () => [...agents].sort((a, b) => a.name.localeCompare(b.name)),
    [agents]
  );

  const handleSelect = useCallback((id: string) => {
    console.log('Selected:', id);
  }, []);

  return (
    <ul>
      {sortedAgents.map((agent) => (
        <li key={agent.id} onClick={() => handleSelect(agent.id)}>
          {agent.name}
        </li>
      ))}
    </ul>
  );
});
\`\`\`
