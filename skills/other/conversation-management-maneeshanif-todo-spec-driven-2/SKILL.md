---
name: conversation-management
description: Build conversation history UI with sidebar, thread switching, and conversation CRUD operations. Implements conversation list, rename, delete, and persistence. Use when adding conversation management features for Phase 3.
allowed-tools: Bash, Write, Read, Edit, Glob
---

# Conversation Management

Quick reference for building conversation history management for the Todo AI Chatbot Phase 3.

---

## Overview

Users need to:
- **View past conversations** - List all their chat threads
- **Switch conversations** - Resume previous chats
- **Create new conversations** - Start fresh threads
- **Rename conversations** - Give meaningful titles
- **Delete conversations** - Remove unwanted history

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Next.js Frontend                          │
├──────────────────────┬──────────────────────────────────────┤
│  Conversation        │  Chat Area                           │
│  Sidebar             │                                      │
│  ┌────────────────┐  │  ┌──────────────────────────────┐   │
│  │ + New Chat     │  │  │  ChatKit / Custom Chat       │   │
│  ├────────────────┤  │  │                              │   │
│  │ Today          │  │  │  Messages...                 │   │
│  │ ├─ Chat 1     ◄├──┼──┤                              │   │
│  │ └─ Chat 2      │  │  │                              │   │
│  │ Yesterday      │  │  │                              │   │
│  │ └─ Chat 3      │  │  │                              │   │
│  └────────────────┘  │  └──────────────────────────────┘   │
└──────────────────────┴──────────────────────────────────────┘
```

---

## Backend API Endpoints

### Conversation Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/conversations` | List user's conversations |
| `POST` | `/api/conversations` | Create new conversation |
| `GET` | `/api/conversations/{id}` | Get conversation with messages |
| `PATCH` | `/api/conversations/{id}` | Rename conversation |
| `DELETE` | `/api/conversations/{id}` | Delete conversation |

---

## Backend Implementation

### Conversation Router

```python
# backend/src/routers/conversations.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, desc
from src.database import get_session
from src.middleware.auth import verify_jwt
from src.models.conversation import Conversation
from src.models.message import Message
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


class ConversationCreate(BaseModel):
    title: str | None = None


class ConversationUpdate(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    preview: str | None = None


class ConversationDetailResponse(ConversationResponse):
    messages: list[dict]


@router.get("/", response_model=list[ConversationResponse])
async def list_conversations(
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
    current_user: dict = Depends(verify_jwt),
):
    """
    List all conversations for the authenticated user.
    Ordered by most recently updated.
    """
    user_id = current_user["id"]

    # Query conversations with message count
    conversations = session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(desc(Conversation.updated_at))
        .offset(offset)
        .limit(limit)
    ).all()

    result = []
    for conv in conversations:
        # Get message count
        message_count = len(conv.messages) if conv.messages else 0

        # Get preview from last message
        preview = None
        if conv.messages:
            last_msg = sorted(conv.messages, key=lambda m: m.created_at)[-1]
            preview = last_msg.content[:100] + "..." if len(last_msg.content) > 100 else last_msg.content

        result.append(ConversationResponse(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=message_count,
            preview=preview,
        ))

    return result


@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    data: ConversationCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(verify_jwt),
):
    """Create a new conversation."""
    user_id = current_user["id"]

    conversation = Conversation(
        user_id=user_id,
        title=data.title or "New Conversation",
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=0,
    )


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(verify_jwt),
):
    """Get conversation with all messages."""
    user_id = current_user["id"]

    conversation = session.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Get messages
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()

    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=len(messages),
        messages=[
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in messages
        ],
    )


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(verify_jwt),
):
    """Rename a conversation."""
    user_id = current_user["id"]

    conversation = session.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conversation.title = data.title
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=len(conversation.messages) if conversation.messages else 0,
    )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(verify_jwt),
):
    """Delete a conversation and all its messages."""
    user_id = current_user["id"]

    conversation = session.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Delete messages first (cascade)
    session.exec(
        select(Message).where(Message.conversation_id == conversation_id)
    )
    for msg in conversation.messages:
        session.delete(msg)

    # Delete conversation
    session.delete(conversation)
    session.commit()

    return {"status": "deleted", "conversation_id": conversation_id}
```

### Register Router

```python
# backend/src/main.py
from src.routers import conversations

app.include_router(conversations.router)
```

---

## Frontend Implementation

### Conversation Store (Zustand)

```typescript
// frontend/src/stores/conversationStore.ts
import { create } from 'zustand';
import { apiClient } from '@/lib/api';

interface Conversation {
  id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
  message_count: number;
  preview?: string;
}

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

interface ConversationState {
  conversations: Conversation[];
  currentConversation: Conversation | null;
  messages: Message[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchConversations: () => Promise<void>;
  selectConversation: (id: number) => Promise<void>;
  createConversation: (title?: string) => Promise<Conversation>;
  updateConversation: (id: number, title: string) => Promise<void>;
  deleteConversation: (id: number) => Promise<void>;
  addMessage: (message: Message) => void;
  clearCurrentConversation: () => void;
}

export const useConversationStore = create<ConversationState>((set, get) => ({
  conversations: [],
  currentConversation: null,
  messages: [],
  isLoading: false,
  error: null,

  fetchConversations: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/api/conversations');
      set({ conversations: response.data, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch conversations', isLoading: false });
    }
  },

  selectConversation: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get(`/api/conversations/${id}`);
      set({
        currentConversation: response.data,
        messages: response.data.messages,
        isLoading: false,
      });
    } catch (error) {
      set({ error: 'Failed to load conversation', isLoading: false });
    }
  },

  createConversation: async (title?: string) => {
    const response = await apiClient.post('/api/conversations', { title });
    const newConv = response.data;
    set(state => ({
      conversations: [newConv, ...state.conversations],
      currentConversation: newConv,
      messages: [],
    }));
    return newConv;
  },

  updateConversation: async (id: number, title: string) => {
    const response = await apiClient.patch(`/api/conversations/${id}`, { title });
    set(state => ({
      conversations: state.conversations.map(c =>
        c.id === id ? { ...c, title } : c
      ),
      currentConversation: state.currentConversation?.id === id
        ? { ...state.currentConversation, title }
        : state.currentConversation,
    }));
  },

  deleteConversation: async (id: number) => {
    await apiClient.delete(`/api/conversations/${id}`);
    set(state => ({
      conversations: state.conversations.filter(c => c.id !== id),
      currentConversation: state.currentConversation?.id === id
        ? null
        : state.currentConversation,
      messages: state.currentConversation?.id === id ? [] : state.messages,
    }));
  },

  addMessage: (message: Message) => {
    set(state => ({
      messages: [...state.messages, message],
    }));
  },

  clearCurrentConversation: () => {
    set({ currentConversation: null, messages: [] });
  },
}));
```

### Conversation Sidebar

```tsx
// frontend/src/components/chat/ConversationSidebar.tsx
'use client';

import { useEffect, useState } from 'react';
import { useConversationStore } from '@/stores/conversationStore';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Plus, MessageSquare, MoreHorizontal, Pencil, Trash2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { formatDistanceToNow } from 'date-fns';

export function ConversationSidebar() {
  const {
    conversations,
    currentConversation,
    isLoading,
    fetchConversations,
    selectConversation,
    createConversation,
    updateConversation,
    deleteConversation,
    clearCurrentConversation,
  } = useConversationStore();

  const [renameDialog, setRenameDialog] = useState<{
    open: boolean;
    id: number;
    title: string;
  }>({ open: false, id: 0, title: '' });

  useEffect(() => {
    fetchConversations();
  }, [fetchConversations]);

  const handleNewChat = async () => {
    clearCurrentConversation();
    // Optionally create conversation immediately or wait for first message
  };

  const handleRename = async () => {
    if (renameDialog.title.trim()) {
      await updateConversation(renameDialog.id, renameDialog.title.trim());
      setRenameDialog({ open: false, id: 0, title: '' });
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Delete this conversation? This cannot be undone.')) {
      await deleteConversation(id);
    }
  };

  // Group conversations by date
  const groupedConversations = groupByDate(conversations);

  return (
    <div className="w-64 h-full border-r bg-muted/30 flex flex-col">
      {/* New Chat Button */}
      <div className="p-3 border-b">
        <Button
          onClick={handleNewChat}
          className="w-full justify-start gap-2"
          variant="outline"
        >
          <Plus className="h-4 w-4" />
          New Chat
        </Button>
      </div>

      {/* Conversation List */}
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-4">
          {Object.entries(groupedConversations).map(([group, convs]) => (
            <div key={group}>
              <h3 className="px-2 py-1 text-xs font-medium text-muted-foreground">
                {group}
              </h3>
              <div className="space-y-1">
                {convs.map(conv => (
                  <ConversationItem
                    key={conv.id}
                    conversation={conv}
                    isActive={currentConversation?.id === conv.id}
                    onSelect={() => selectConversation(conv.id)}
                    onRename={() => setRenameDialog({
                      open: true,
                      id: conv.id,
                      title: conv.title || '',
                    })}
                    onDelete={() => handleDelete(conv.id)}
                  />
                ))}
              </div>
            </div>
          ))}

          {conversations.length === 0 && !isLoading && (
            <p className="text-center text-sm text-muted-foreground py-8">
              No conversations yet
            </p>
          )}
        </div>
      </ScrollArea>

      {/* Rename Dialog */}
      <Dialog open={renameDialog.open} onOpenChange={(open) =>
        !open && setRenameDialog({ open: false, id: 0, title: '' })
      }>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Rename Conversation</DialogTitle>
          </DialogHeader>
          <Input
            value={renameDialog.title}
            onChange={(e) => setRenameDialog(prev => ({
              ...prev,
              title: e.target.value,
            }))}
            placeholder="Enter new title"
            onKeyDown={(e) => e.key === 'Enter' && handleRename()}
          />
          <DialogFooter>
            <Button variant="outline" onClick={() =>
              setRenameDialog({ open: false, id: 0, title: '' })
            }>
              Cancel
            </Button>
            <Button onClick={handleRename}>Save</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

interface ConversationItemProps {
  conversation: {
    id: number;
    title: string | null;
    preview?: string;
    updated_at: string;
  };
  isActive: boolean;
  onSelect: () => void;
  onRename: () => void;
  onDelete: () => void;
}

function ConversationItem({
  conversation,
  isActive,
  onSelect,
  onRename,
  onDelete,
}: ConversationItemProps) {
  return (
    <div
      className={cn(
        "group flex items-center gap-2 px-2 py-2 rounded-lg cursor-pointer hover:bg-muted",
        isActive && "bg-muted"
      )}
      onClick={onSelect}
    >
      <MessageSquare className="h-4 w-4 shrink-0 text-muted-foreground" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">
          {conversation.title || 'New Chat'}
        </p>
        {conversation.preview && (
          <p className="text-xs text-muted-foreground truncate">
            {conversation.preview}
          </p>
        )}
      </div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="h-6 w-6 opacity-0 group-hover:opacity-100"
            onClick={(e) => e.stopPropagation()}
          >
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem onClick={(e) => {
            e.stopPropagation();
            onRename();
          }}>
            <Pencil className="h-4 w-4 mr-2" />
            Rename
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={(e) => {
              e.stopPropagation();
              onDelete();
            }}
            className="text-destructive"
          >
            <Trash2 className="h-4 w-4 mr-2" />
            Delete
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

// Helper function to group conversations by date
function groupByDate(conversations: Array<{ updated_at: string; [key: string]: any }>) {
  const groups: Record<string, typeof conversations> = {};

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  const lastWeek = new Date(today);
  lastWeek.setDate(lastWeek.getDate() - 7);

  conversations.forEach(conv => {
    const date = new Date(conv.updated_at);
    date.setHours(0, 0, 0, 0);

    let group: string;
    if (date >= today) {
      group = 'Today';
    } else if (date >= yesterday) {
      group = 'Yesterday';
    } else if (date >= lastWeek) {
      group = 'Previous 7 Days';
    } else {
      group = 'Older';
    }

    if (!groups[group]) groups[group] = [];
    groups[group].push(conv);
  });

  return groups;
}
```

### Chat Layout with Sidebar

```tsx
// frontend/src/app/chat/layout.tsx
'use client';

import { ConversationSidebar } from '@/components/chat/ConversationSidebar';
import { useAuthStore } from '@/stores/authStore';
import { redirect } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { PanelLeftClose, PanelLeft } from 'lucide-react';

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, isLoading } = useAuthStore();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      redirect('/login');
    }
  }, [isAuthenticated, isLoading]);

  if (isLoading) {
    return <div className="h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="h-screen flex">
      {/* Sidebar */}
      {sidebarOpen && <ConversationSidebar />}

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header with toggle */}
        <div className="h-12 border-b flex items-center px-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? (
              <PanelLeftClose className="h-5 w-5" />
            ) : (
              <PanelLeft className="h-5 w-5" />
            )}
          </Button>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-hidden">
          {children}
        </div>
      </div>
    </div>
  );
}
```

---

## Project Structure

```
frontend/src/
├── app/
│   └── chat/
│       ├── layout.tsx           # Layout with sidebar
│       └── page.tsx             # Chat page with ChatKit
│
├── components/
│   └── chat/
│       ├── ConversationSidebar.tsx  # Sidebar component
│       ├── ConversationItem.tsx     # Individual conversation
│       └── ChatContainer.tsx        # Main chat area
│
├── stores/
│   └── conversationStore.ts     # Zustand store
│
└── lib/
    └── api.ts                   # API client
```

---

## Verification Checklist

**Backend:**
- [ ] Conversation CRUD endpoints implemented
- [ ] User isolation enforced
- [ ] Messages cascade delete with conversation
- [ ] Pagination support for large lists

**Frontend:**
- [ ] Conversation list fetches on mount
- [ ] Can create new conversations
- [ ] Can select and load conversation
- [ ] Can rename conversations
- [ ] Can delete conversations
- [ ] Sidebar groups by date
- [ ] Responsive on mobile (collapsible sidebar)

---

## See Also

- [chat-api-integration](../chat-api-integration/) - Chat endpoint setup
- [streaming-sse-setup](../streaming-sse-setup/) - Real-time streaming
- [openai-chatkit-setup](../openai-chatkit-setup/) - ChatKit UI
- [OpenAI ChatKit Docs](https://platform.openai.com/docs/guides/chatkit) - Official ChatKit documentation
- [Domain Allowlist](https://platform.openai.com/settings/organization/security/domain-allowlist) - Required for ChatKit production deployment
