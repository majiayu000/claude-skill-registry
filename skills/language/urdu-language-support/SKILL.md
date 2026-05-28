---
name: urdu-language-support
description: Implement Urdu language support with RTL layout, translations, and AI responses in Urdu. Bonus feature (+100 points) for Phase 5. (project)
allowed-tools: Bash, Write, Read, Glob, Edit, Grep
---

# Urdu Language Support Skill

## Quick Start

1. **Read Phase 5 Constitution** - `constitution-prompt-phase-5.md`
2. **Set up i18n** - next-intl or react-intl
3. **Create Urdu translations** - JSON translation files
4. **Configure RTL support** - Tailwind RTL plugin
5. **Update AI agent** - Urdu response capability
6. **Add language switcher** - UI component

## Bonus Points: +100

This is a **bonus feature** for Phase 5 that adds 100 points to the hackathon score.

## i18n Setup with next-intl

### Installation

```bash
cd frontend
npm install next-intl
```

### Next.js Configuration

```typescript
// frontend/next.config.ts
import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin();

const nextConfig = {
  // ... other config
};

export default withNextIntl(nextConfig);
```

### i18n Configuration

```typescript
// frontend/i18n.ts
import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`./messages/${locale}.json`)).default
}));
```

### Middleware for Locale Detection

```typescript
// frontend/middleware.ts
import createMiddleware from 'next-intl/middleware';

export default createMiddleware({
  locales: ['en', 'ur'],
  defaultLocale: 'en',
  localePrefix: 'as-needed'
});

export const config = {
  matcher: ['/((?!api|_next|.*\\..*).*)']
};
```

## Translation Files

### English Translations

```json
// frontend/messages/en.json
{
  "common": {
    "appName": "Evolution Todo",
    "loading": "Loading...",
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "search": "Search",
    "filter": "Filter",
    "sort": "Sort"
  },
  "auth": {
    "login": "Login",
    "signup": "Sign Up",
    "logout": "Logout",
    "email": "Email",
    "password": "Password",
    "forgotPassword": "Forgot Password?"
  },
  "tasks": {
    "title": "Tasks",
    "newTask": "New Task",
    "addTask": "Add Task",
    "editTask": "Edit Task",
    "deleteTask": "Delete Task",
    "taskTitle": "Task Title",
    "description": "Description",
    "priority": "Priority",
    "dueDate": "Due Date",
    "status": "Status",
    "tags": "Tags",
    "reminder": "Reminder",
    "priorities": {
      "low": "Low",
      "medium": "Medium",
      "high": "High"
    },
    "statuses": {
      "pending": "Pending",
      "inProgress": "In Progress",
      "completed": "Completed"
    },
    "noTasks": "No tasks found",
    "completedTasks": "Completed Tasks"
  },
  "chat": {
    "title": "AI Assistant",
    "placeholder": "Ask me anything about your tasks...",
    "send": "Send",
    "thinking": "Thinking...",
    "newConversation": "New Conversation"
  },
  "settings": {
    "title": "Settings",
    "language": "Language",
    "theme": "Theme",
    "notifications": "Notifications"
  }
}
```

### Urdu Translations

```json
// frontend/messages/ur.json
{
  "common": {
    "appName": "ایوولیوشن ٹوڈو",
    "loading": "لوڈ ہو رہا ہے...",
    "save": "محفوظ کریں",
    "cancel": "منسوخ کریں",
    "delete": "حذف کریں",
    "edit": "ترمیم کریں",
    "search": "تلاش کریں",
    "filter": "فلٹر",
    "sort": "ترتیب دیں"
  },
  "auth": {
    "login": "لاگ ان",
    "signup": "سائن اپ",
    "logout": "لاگ آؤٹ",
    "email": "ای میل",
    "password": "پاس ورڈ",
    "forgotPassword": "پاس ورڈ بھول گئے؟"
  },
  "tasks": {
    "title": "کام",
    "newTask": "نیا کام",
    "addTask": "کام شامل کریں",
    "editTask": "کام میں ترمیم کریں",
    "deleteTask": "کام حذف کریں",
    "taskTitle": "کام کا عنوان",
    "description": "تفصیل",
    "priority": "ترجیح",
    "dueDate": "آخری تاریخ",
    "status": "حیثیت",
    "tags": "ٹیگز",
    "reminder": "یاد دہانی",
    "priorities": {
      "low": "کم",
      "medium": "درمیانی",
      "high": "زیادہ"
    },
    "statuses": {
      "pending": "زیر التواء",
      "inProgress": "جاری",
      "completed": "مکمل"
    },
    "noTasks": "کوئی کام نہیں ملا",
    "completedTasks": "مکمل شدہ کام"
  },
  "chat": {
    "title": "AI معاون",
    "placeholder": "اپنے کاموں کے بارے میں کچھ بھی پوچھیں...",
    "send": "بھیجیں",
    "thinking": "سوچ رہا ہوں...",
    "newConversation": "نئی گفتگو"
  },
  "settings": {
    "title": "ترتیبات",
    "language": "زبان",
    "theme": "تھیم",
    "notifications": "اطلاعات"
  }
}
```

## RTL Support with Tailwind

### Tailwind RTL Plugin

```bash
npm install tailwindcss-rtl
```

### Tailwind Configuration

```typescript
// frontend/tailwind.config.ts
import type { Config } from "tailwindcss";
import rtl from "tailwindcss-rtl";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [rtl],
};

export default config;
```

### RTL Layout Component

```tsx
// frontend/components/layout/rtl-provider.tsx
"use client";

import { useLocale } from "next-intl";
import { useEffect } from "react";

export function RTLProvider({ children }: { children: React.ReactNode }) {
  const locale = useLocale();
  const isRTL = locale === "ur";

  useEffect(() => {
    document.documentElement.dir = isRTL ? "rtl" : "ltr";
    document.documentElement.lang = locale;
  }, [locale, isRTL]);

  return <>{children}</>;
}
```

### RTL-Aware Components

```tsx
// frontend/components/ui/rtl-text.tsx
import { cn } from "@/lib/utils";
import { useLocale } from "next-intl";

interface RTLTextProps {
  children: React.ReactNode;
  className?: string;
}

export function RTLText({ children, className }: RTLTextProps) {
  const locale = useLocale();
  const isRTL = locale === "ur";

  return (
    <span className={cn(
      isRTL && "font-urdu",  // Custom Urdu font
      className
    )}>
      {children}
    </span>
  );
}
```

## Language Switcher Component

```tsx
// frontend/components/language-switcher.tsx
"use client";

import { useLocale, useTranslations } from "next-intl";
import { useRouter, usePathname } from "next/navigation";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Globe } from "lucide-react";

const languages = [
  { code: "en", name: "English", nativeName: "English" },
  { code: "ur", name: "Urdu", nativeName: "اردو" },
];

export function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();
  const t = useTranslations("settings");

  const handleChange = (newLocale: string) => {
    // Remove current locale prefix and add new one
    const newPath = pathname.replace(`/${locale}`, `/${newLocale}`);
    router.push(newPath);
  };

  return (
    <Select value={locale} onValueChange={handleChange}>
      <SelectTrigger className="w-[140px]">
        <Globe className="h-4 w-4 me-2" />
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {languages.map((lang) => (
          <SelectItem key={lang.code} value={lang.code}>
            {lang.nativeName}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
```

## AI Agent Urdu Support

### Update Agent Prompt

```python
# backend/src/agents/prompts.py

SYSTEM_PROMPT_URDU = """
آپ ایک مددگار AI اسسٹنٹ ہیں جو صارفین کو ان کے کاموں کا انتظام کرنے میں مدد کرتا ہے۔

آپ یہ کر سکتے ہیں:
- نئے کام بنائیں
- کاموں کی فہرست دیکھیں
- کام مکمل کریں
- کام حذف کریں
- کاموں میں ترمیم کریں
- یاد دہانیاں مقرر کریں

ہمیشہ اردو میں جواب دیں اور شائستہ رہیں۔
"""

def get_system_prompt(language: str = "en") -> str:
    """Get system prompt based on language."""
    if language == "ur":
        return SYSTEM_PROMPT_URDU
    return SYSTEM_PROMPT_EN
```

### Language Detection

```python
# backend/src/agents/language.py
import langdetect

def detect_language(text: str) -> str:
    """Detect language of input text."""
    try:
        lang = langdetect.detect(text)
        return "ur" if lang == "ur" else "en"
    except:
        return "en"

def should_respond_in_urdu(user_message: str) -> bool:
    """Check if response should be in Urdu."""
    return detect_language(user_message) == "ur"
```

### Updated Agent

```python
# backend/src/agents/todo_agent.py
from .language import should_respond_in_urdu, get_system_prompt

async def run_agent(user_message: str, user_id: str):
    """Run AI agent with language support."""

    # Detect language
    use_urdu = should_respond_in_urdu(user_message)
    system_prompt = get_system_prompt("ur" if use_urdu else "en")

    # Create agent with appropriate prompt
    agent = Agent(
        name="todo_assistant",
        instructions=system_prompt,
        model="gemini/gemini-2.0-flash",
        tools=[...],
    )

    # Run and return response
    response = await Runner.run(agent, user_message)
    return response
```

## Urdu Font Configuration

### Google Fonts Setup

```tsx
// frontend/app/layout.tsx
import { Noto_Nastaliq_Urdu, Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const urduFont = Noto_Nastaliq_Urdu({
  subsets: ["arabic"],
  variable: "--font-urdu",
  weight: ["400", "700"],
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body className={`${inter.variable} ${urduFont.variable}`}>
        {children}
      </body>
    </html>
  );
}
```

### Tailwind Font Configuration

```typescript
// frontend/tailwind.config.ts
const config: Config = {
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)", "sans-serif"],
        urdu: ["var(--font-urdu)", "serif"],
      },
    },
  },
};
```

## Usage in Components

```tsx
// frontend/components/tasks/task-card.tsx
"use client";

import { useTranslations } from "next-intl";
import { PriorityBadge } from "./priority-badge";

export function TaskCard({ task }: { task: Task }) {
  const t = useTranslations("tasks");

  return (
    <div className="p-4 border rounded-lg">
      <h3 className="font-bold">{task.title}</h3>
      <p className="text-muted-foreground">{task.description}</p>
      <div className="flex items-center gap-2 mt-2">
        <span className="text-sm">{t("priority")}:</span>
        <PriorityBadge priority={task.priority} />
      </div>
      <div className="flex items-center gap-2 mt-1">
        <span className="text-sm">{t("status")}:</span>
        <span>{t(`statuses.${task.status}`)}</span>
      </div>
    </div>
  );
}
```

## Verification Checklist

- [ ] next-intl installed and configured
- [ ] English translations complete
- [ ] Urdu translations complete
- [ ] RTL support working
- [ ] Language switcher component created
- [ ] Urdu font loaded (Noto Nastaliq)
- [ ] AI agent responds in Urdu
- [ ] All UI text is translatable
- [ ] Direction changes correctly on language switch
- [ ] No layout breaks in RTL mode

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Font not loading | Missing import | Add Noto Nastaliq to layout |
| RTL not working | Missing dir attribute | Set in RTLProvider |
| Translation missing | Key not in JSON | Add to messages file |
| AI responds in English | No language detection | Add langdetect check |
| Text overflow | RTL text handling | Use `text-start`/`text-end` |

## References

- [next-intl Documentation](https://next-intl-docs.vercel.app/)
- [Tailwind CSS RTL](https://tailwindcss.com/docs/hover-focus-and-other-states#rtl-support)
- [Google Fonts - Urdu](https://fonts.google.com/noto/specimen/Noto+Nastaliq+Urdu)
- [Phase 5 Constitution](../../../constitution-prompt-phase-5.md)
