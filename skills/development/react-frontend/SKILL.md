---
name: react-frontend
description: React components for Chat, Evaluation, Report, Admin with TypeScript, Tailwind, hooks
---

# React Frontend — CEI-001

## Project Structure

```
src/
├── components/
│   ├── chat/
│   │   ├── ChatWindow.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── ChatInput.tsx
│   │   └── useChat.ts (custom hook)
│   ├── evaluation/
│   │   ├── EvaluationWizard.tsx
│   │   ├── QuestionCard.tsx
│   │   ├── ProgressBar.tsx
│   │   └── useEvaluation.ts
│   ├── report/
│   │   ├── ReportDashboard.tsx
│   │   ├── ScoreCard.tsx
│   │   ├── RadarChart.tsx
│   │   └── useReport.ts
│   ├── admin/
│   │   ├── DocumentList.tsx
│   │   ├── DocumentUpload.tsx
│   │   ├── PipelineStatus.tsx
│   │   └── useDocuments.ts
│   └── shared/
│       ├── Navbar.tsx
│       ├── Footer.tsx
│       ├── Button.tsx
│       └── Card.tsx
├── pages/
│   ├── HomePage.tsx
│   ├── ChatPage.tsx
│   ├── EvaluationPage.tsx
│   ├── ReportPage.tsx
│   ├── AdminPage.tsx
│   └── LoginPage.tsx
├── services/
│   ├── api.ts (axios client with auth)
│   ├── chatService.ts
│   ├── evaluationService.ts
│   ├── reportService.ts
│   └── adminService.ts
├── hooks/
│   ├── useAuth.ts
│   ├── useAPI.ts
│   └── useLocalStorage.ts
├── store/
│   ├── authStore.ts (Zustand)
│   ├── evaluationStore.ts
│   └── chatStore.ts
├── types/
│   ├── api.ts
│   ├── evaluation.ts
│   ├── chat.ts
│   └── admin.ts
├── styles/
│   └── tailwind.css
└── App.tsx
```

## Component Pattern with TypeScript

### Basic Component
```typescript
import React, { FC } from 'react';

interface EvaluationHeaderProps {
  title: string;
  progress: number;
  onBack: () => void;
}

export const EvaluationHeader: FC<EvaluationHeaderProps> = ({
  title,
  progress,
  onBack
}) => {
  return (
    <div className="bg-white border-b">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <button
          onClick={onBack}
          className="text-gray-600 hover:text-gray-900"
        >
          ← Retour
        </button>
        <div className="flex-1 mx-4">
          <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
```

### Chat Component with Streaming
```typescript
import React, { useState, useRef, useEffect } from 'react';
import { chatService } from '@/services/chatService';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{ title: string; excerpt: string }>;
  timestamp: Date;
}

export const ChatWindow: FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Stream assistant response
      let assistantContent = '';
      let sources: ChatMessage['sources'] = [];

      const stream = await chatService.sendMessage({
        conversation_id: 'current', // From context
        content: inputValue
      });

      for await (const chunk of stream) {
        if (chunk.type === 'content') {
          assistantContent += chunk.data;
          
          // Update last message in real-time
          setMessages(prev => {
            const newMessages = [...prev];
            if (newMessages[newMessages.length - 1]?.role === 'assistant') {
              newMessages[newMessages.length - 1].content = assistantContent;
            }
            return newMessages;
          });
        } else if (chunk.type === 'sources') {
          sources = chunk.data;
        }
      }

      // Add assistant message
      const assistantMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'assistant',
        content: assistantContent,
        sources,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Erreur: Impossible de générer une réponse.',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(msg => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isLoading && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t bg-white p-4">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Posez votre question..."
            disabled={isLoading}
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            Envoyer
          </button>
        </form>
      </div>
    </div>
  );
};
```

### Form with Validation (Evaluation)
```typescript
import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const questionSchema = z.object({
  answer: z.enum(['oui', 'non', 'partiellement']),
  comment: z.string().optional()
});

type QuestionFormData = z.infer<typeof questionSchema>;

interface QuestionCardProps {
  question: {
    id: string;
    text: string;
    category: string;
    type: 'yesno' | 'scale' | 'multiple';
  };
  onSubmit: (answer: QuestionFormData) => void;
}

export const QuestionCard: FC<QuestionCardProps> = ({ question, onSubmit }) => {
  const { control, handleSubmit, formState: { errors } } = useForm<QuestionFormData>({
    resolver: zodResolver(questionSchema)
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">{question.text}</h3>

      <div className="space-y-3 mb-6">
        {['oui', 'non', 'partiellement'].map(option => (
          <label key={option} className="flex items-center">
            <Controller
              name="answer"
              control={control}
              render={({ field }) => (
                <input
                  {...field}
                  type="radio"
                  value={option}
                  className="w-4 h-4 text-blue-600"
                />
              )}
            />
            <span className="ml-3 capitalize">{option}</span>
          </label>
        ))}
      </div>

      {errors.answer && (
        <p className="text-red-600 text-sm mb-4">{errors.answer.message}</p>
      )}

      <Controller
        name="comment"
        control={control}
        render={({ field }) => (
          <textarea
            {...field}
            placeholder="Commentaires optionnels..."
            rows={3}
            className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )}
      />

      <button
        type="submit"
        className="mt-4 w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Suivant
      </button>
    </form>
  );
};
```

## Custom Hooks

```typescript
// hooks/useChat.ts
import { useState, useCallback } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { chatService } from '@/services/chatService';

export const useChat = (conversationId: string) => {
  const [messages, setMessages] = useState([]);

  const { data: history, isLoading } = useQuery({
    queryKey: ['chat', conversationId],
    queryFn: () => chatService.getHistory(conversationId)
  });

  const sendMutation = useMutation({
    mutationFn: (content: string) =>
      chatService.sendMessage({ conversation_id: conversationId, content }),
    onSuccess: (response) => {
      setMessages(prev => [...prev, response]);
    }
  });

  return {
    messages: history || [],
    isLoading,
    sendMessage: sendMutation.mutate,
    isLoading: sendMutation.isPending
  };
};
```

## Auth & API Client

```typescript
// services/api.ts
import axios from 'axios';
import { useAuthStore } from '@/store/authStore';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000'
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

export default api;
```

## State Management (Zustand)

```typescript
// store/authStore.ts
import { create } from 'zustand';

interface AuthStore {
  user: any | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    const { access_token, user } = response.data;
    localStorage.setItem('token', access_token);
    set({ token: access_token, user });
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, user: null });
  }
}));
```

## Types

```typescript
// types/api.ts
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{ title: string; excerpt: string }>;
  timestamp: string;
}

export interface Evaluation {
  id: string;
  userId: string;
  status: 'in_progress' | 'completed';
  answers: Record<string, string>;
  score: number;
  createdAt: string;
  completedAt?: string;
}

export interface EvaluationQuestion {
  id: string;
  moduleId: string;
  text: string;
  type: 'yesno' | 'scale' | 'multiple';
  weight: number;
}
```

## Tailwind Classes

- Spacing: `px-4`, `py-2`, `mx-4`, `gap-2`
- Colors: `bg-blue-600`, `text-gray-900`, `border-gray-200`
- Layout: `flex`, `grid`, `container mx-auto`
- Responsive: `md:`, `lg:`
- States: `hover:`, `focus:`, `disabled:`, `dark:`

## Conventions

- Files: PascalCase for components, camelCase for hooks/services
- Props interfaces end with `Props`
- Type everything (no `any`)
- Hooks use `use` prefix
- Components use FC type or function syntax
- Import order: react, third-party, local
- Error boundaries for error handling
- Accessible: alt text, labels, semantic HTML
- No hardcoded strings (use constants/i18n)
