---
name: nextjs-chatkit
description: Integrate OpenAI ChatKit in Next.js 15 App Router with domain allowlist, authentication, and API connections. Use when building chat interfaces or ChatKit integration.
---

# Next.js ChatKit Integration

## Environment Setup
```env
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_domain_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Chat Page (app/chat/page.tsx)
```typescript
'use client';

import { ChatKit } from '@openai/chatkit';
import { useAuth } from '@/lib/auth';

export default function ChatPage() {
  const { user, token } = useAuth();

  const handleMessage = async (message: string, conversationId?: number) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/chat`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ conversation_id: conversationId, message }),
      }
    );
    const data = await response.json();
    return data.response;
  };

  return (
    <ChatKit
      domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY!}
      onMessage={handleMessage}
      placeholder="Ask me to manage your tasks..."
    />
  );
}
```

## Domain Allowlist Setup
1. Deploy frontend to get URL (e.g., https://app.vercel.app)
2. Add domain at: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Copy generated domain key
4. Set NEXT_PUBLIC_OPENAI_DOMAIN_KEY in Vercel env vars