---
name: frontend-agent
description: Handles frontend/UX/route work for Unite-Hub. Fixes UI bugs, implements React components, updates layouts, ensures responsive design, and maintains shadcn/ui consistency.
---

# Frontend Agent Skill

## Overview

The Frontend Agent is responsible for all UI/UX work in the Unite-Hub Next.js application:
1. **React 19 / Next.js 16 development** with App Router
2. **shadcn/ui component implementation** and customization
3. **Tailwind CSS styling** and responsive design
4. **Route creation and breadcrumb setup**
5. **Client-side state management** (React Context, hooks)
6. **Accessibility and performance optimization**

## How to Use This Agent

### Trigger

User says: "Fix dashboard layout", "Add new contact page", "Update navigation", "Create modal component"

### What the Agent Does

#### 1. Understand the Request

**Questions to Ask**:
- Which page/component needs work?
- What's the desired behavior?
- Are there design references (screenshots, wireframes)?
- What's the priority (P0/P1/P2)?

#### 2. Analyze Current Implementation

**Step A: Locate Files**
```bash
# Find the component or page
find src/app -name "*.tsx" | grep -i "contacts"
find src/components -name "*.tsx" | grep -i "hotleads"
```

**Step B: Read Current Code**
```typescript
// Use text_editor tool
text_editor.view("src/app/dashboard/contacts/page.tsx")
```

**Step C: Identify Dependencies**
- What shadcn/ui components are used?
- What contexts are consumed (AuthContext, etc.)?
- What API routes are called?
- What database queries are made?

#### 3. Implement Changes

**Step A: Component Updates**

For existing components:
```typescript
// src/components/HotLeadsPanel.tsx
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useAuth } from "@/contexts/AuthContext";

export function HotLeadsPanel({ workspaceId }: { workspaceId: string }) {
  const { currentOrganization } = useAuth();

  // Fetch hot leads
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    async function fetchLeads() {
      const res = await fetch("/api/agents/contact-intelligence", {
        method: "POST",
        body: JSON.stringify({ action: "get_hot_leads", workspaceId }),
      });
      const data = await res.json();
      setLeads(data.leads || []);
    }
    if (workspaceId) fetchLeads();
  }, [workspaceId]);

  return (
    <Card>
      {/* UI implementation */}
    </Card>
  );
}
```

**Step B: Route Creation**

For new pages:
```typescript
// src/app/dashboard/new-page/page.tsx
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "New Page | Unite Hub",
  description: "Description of new page"
};

export default async function NewPage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold">New Page</h1>
      {/* Content */}
    </div>
  );
}
```

**Step C: shadcn/ui Components**

Install new components if needed:
```bash
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add toast
```

Use components following shadcn patterns:
```typescript
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    {/* Content */}
  </DialogContent>
</Dialog>
```

#### 4. Add Workspace Filtering (CRITICAL for V1)

**All database queries MUST filter by workspace**:

```typescript
// ❌ BAD - Shows data from all workspaces
const { data: contacts } = await supabase
  .from("contacts")
  .select("*");

// ✅ GOOD - Only shows data from user's workspace
const { data: contacts } = await supabase
  .from("contacts")
  .select("*")
  .eq("workspace_id", workspaceId);
```

**Required for these tables**:
- `contacts` - `.eq("workspace_id", workspaceId)`
- `campaigns` - `.eq("workspace_id", workspaceId)`
- `drip_campaigns` - `.eq("workspace_id", workspaceId)`
- `emails` - `.eq("workspace_id", workspaceId)`
- `generatedContent` - `.eq("workspace_id", workspaceId)`

#### 5. Handle Loading and Error States

**Loading State**:
```typescript
const [isLoading, setIsLoading] = useState(true);
const [error, setError] = useState<string | null>(null);

useEffect(() => {
  async function fetchData() {
    try {
      setIsLoading(true);
      const data = await fetch("...");
      setData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }
  fetchData();
}, []);

if (isLoading) return <Spinner />;
if (error) return <ErrorBanner message={error} />;
return <DataDisplay data={data} />;
```

#### 6. Responsive Design

**Tailwind Breakpoints**:
```typescript
<div className="
  grid grid-cols-1        // Mobile: 1 column
  md:grid-cols-2          // Tablet: 2 columns
  lg:grid-cols-3          // Desktop: 3 columns
  gap-4
">
  {/* Cards */}
</div>
```

**Mobile-First Approach**:
- Start with mobile layout (default classes)
- Add `md:` classes for tablet
- Add `lg:` and `xl:` for desktop

#### 7. Test Changes

**Step A: Visual Testing**
```bash
# Start dev server
npm run dev

# Navigate to page in browser
# Test on mobile viewport (DevTools)
# Test dark theme
```

**Step B: Accessibility**
```typescript
// Check for:
// - Proper ARIA labels
// - Keyboard navigation
// - Focus states
// - Screen reader support

<button aria-label="Close dialog">×</button>
<input aria-describedby="email-help" />
<div role="alert" aria-live="polite">{error}</div>
```

**Step C: Performance**
```typescript
// Use React.memo for expensive components
import { memo } from "react";

export const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  return <div>{/* Render */}</div>;
});

// Use dynamic imports for heavy components
import dynamic from "next/dynamic";

const HeavyChart = dynamic(() => import("@/components/HeavyChart"), {
  loading: () => <Spinner />,
  ssr: false
});
```

## Common Tasks

### Task 1: Fix Missing Workspace Filter

**Example**: Dashboard Overview page showing all contacts

**Steps**:
1. Read `src/app/dashboard/overview/page.tsx`
2. Find all Supabase queries
3. Add `.eq("workspace_id", workspaceId)` to each
4. Add null check for workspaceId before querying
5. Test with multiple workspaces

**Code**:
```typescript
// Before
const { data: contacts } = await supabase.from("contacts").select("*");

// After
if (!workspaceId) {
  return <div>No workspace selected</div>;
}

const { data: contacts, error } = await supabase
  .from("contacts")
  .select("*")
  .eq("workspace_id", workspaceId);

if (error) {
  console.error("Error fetching contacts:", error);
  return <ErrorBanner />;
}
```

### Task 2: Create New Dashboard Page

**Example**: Add "Analytics" page to dashboard

**Steps**:
1. Create `src/app/dashboard/analytics/page.tsx`
2. Add to navigation in `src/app/dashboard/layout.tsx`
3. Implement page content with shadcn/ui components
4. Add breadcrumbs
5. Test navigation

**Code**:
```typescript
// src/app/dashboard/analytics/page.tsx
import { Metadata } from "next";
import { Card } from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Analytics | Unite Hub",
};

export default async function AnalyticsPage() {
  return (
    <div className="container mx-auto py-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="text-muted-foreground">Track your campaign performance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          {/* Stat card 1 */}
        </Card>
        <Card>
          {/* Stat card 2 */}
        </Card>
        <Card>
          {/* Stat card 3 */}
        </Card>
      </div>
    </div>
  );
}
```

```typescript
// src/app/dashboard/layout.tsx - Add to navigation
const navigation = [
  { name: "Dashboard", href: "/dashboard/overview", icon: HomeIcon },
  { name: "Contacts", href: "/dashboard/contacts", icon: UsersIcon },
  { name: "Campaigns", href: "/dashboard/campaigns", icon: MailIcon },
  { name: "Analytics", href: "/dashboard/analytics", icon: ChartIcon }, // NEW
];
```

### Task 3: Implement Button Functionality

**Example**: Hot Leads panel "Send Email" button

**Steps**:
1. Read `src/components/HotLeadsPanel.tsx`
2. Find button location
3. Implement onClick handler
4. Call appropriate API endpoint
5. Show success/error toast

**Code**:
```typescript
import { useToast } from "@/components/ui/use-toast";

function HotLeadsPanel() {
  const { toast } = useToast();

  async function handleSendEmail(contactId: string) {
    try {
      const res = await fetch("/api/emails/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ contactId, templateType: "followup" }),
      });

      if (!res.ok) throw new Error("Failed to send email");

      toast({
        title: "Email sent",
        description: "Your email has been queued for sending.",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error.message,
      });
    }
  }

  return (
    <Button onClick={() => handleSendEmail(contact.id)}>
      Send Email
    </Button>
  );
}
```

## Styling Guidelines

### Tailwind CSS Best Practices

**Use Utility Classes**:
```typescript
// ✅ Good
<div className="flex items-center justify-between p-4 bg-background border rounded-lg">

// ❌ Bad (custom CSS)
<div style={{ display: "flex", padding: "16px" }}>
```

**Use CSS Variables from Theme**:
```typescript
// Defined in globals.css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --primary: 222.2 47.4% 11.2%;
  }
}

// Use in components
<div className="bg-background text-foreground">
<div className="bg-card text-card-foreground">
<div className="bg-primary text-primary-foreground">
```

**Responsive Design**:
```typescript
<div className="
  text-sm md:text-base lg:text-lg
  p-2 md:p-4 lg:p-6
  grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
">
```

## Component Library Reference

### shadcn/ui Components Available

- `accordion` - Collapsible content panels
- `alert-dialog` - Modal confirmation dialogs
- `avatar` - User profile images
- `badge` - Status badges
- `button` - Interactive buttons
- `card` - Content containers
- `checkbox` - Form checkboxes
- `dialog` - Modal dialogs
- `dropdown-menu` - Dropdown menus
- `input` - Text inputs
- `label` - Form labels
- `popover` - Floating content
- `progress` - Progress indicators
- `radio-group` - Radio buttons
- `select` - Select dropdowns
- `switch` - Toggle switches
- `tabs` - Tabbed interfaces
- `toast` - Notification toasts
- `tooltip` - Hover tooltips

**Install new components**:
```bash
npx shadcn@latest add [component-name]
```

## Error Handling Patterns

### API Errors

```typescript
try {
  const res = await fetch("/api/...");
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Something went wrong");
  }

  return data;
} catch (error) {
  console.error("API Error:", error);
  toast({
    variant: "destructive",
    title: "Error",
    description: error.message,
  });
  return null;
}
```

### Supabase Errors

```typescript
const { data, error } = await supabase.from("contacts").select("*");

if (error) {
  console.error("Supabase error:", error);
  return <ErrorBanner message="Failed to load contacts" />;
}

if (!data || data.length === 0) {
  return <EmptyState message="No contacts found" />;
}

return <ContactsList contacts={data} />;
```

## Version 1 Constraints

**What We Fix for V1**:
- ✅ Workspace filtering on ALL pages
- ✅ Hot Leads button functionality
- ✅ Contact detail page navigation
- ✅ Dashboard stat cards
- ✅ Loading and error states
- ✅ Responsive design fixes

**What We Do NOT Build for V1**:
- ❌ Advanced animations
- ❌ Custom theme builder
- ❌ Drag-and-drop interfaces
- ❌ Real-time collaboration UI
- ❌ Mobile app

## Key Points

- **Always filter by workspace** - Data isolation is critical
- **Use shadcn/ui components** - Don't reinvent the wheel
- **Follow Tailwind conventions** - Utility-first approach
- **Handle loading/error states** - Never show blank screens
- **Test responsive design** - Mobile, tablet, desktop
- **Maintain accessibility** - ARIA labels, keyboard navigation

---

## Integration with Other Agents

The Frontend Agent works with:
- **Backend Agent** - Consumes API endpoints
- **Docs Agent** - Updates component documentation
- **Orchestrator** - Receives UI fix requests
