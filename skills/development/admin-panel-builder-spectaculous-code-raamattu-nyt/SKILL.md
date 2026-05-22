---
name: admin-panel-builder
description: Expert assistant for creating and maintaining admin panel pages in the KR92 Bible Voice project. Use when creating admin pages, building admin components, integrating with admin navigation, or adding admin features.
---

# Admin Panel Builder

## Current Architecture (2026)

### Layout Pattern
All admin pages now use the **SidebarProvider + AppSidebar + AdminHeader** pattern:

```typescript
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import AdminHeader from "@/components/admin/AdminHeader";

return (
  <SidebarProvider>
    <div className="min-h-screen flex w-full bg-background">
      <AppSidebar onNavigateToContinueAudio={() => {}} onNavigateToContinueText={() => {}} />
      <main className="flex-1 overflow-auto">
        <AdminHeader
          title="Page Title"
          icon={<Icon className="h-6 w-6 text-primary" />}
          showBackButton={true}
        />
        <div className="p-6">
          {/* Content */}
        </div>
      </main>
    </div>
  </SidebarProvider>
);
```

### Authentication Pattern
Use `@shared-auth/hooks/useUserRole` from the shared package:

```typescript
import { useUserRole } from "@shared-auth/hooks/useUserRole";

const { isAdmin } = useUserRole();

if (!isAdmin) {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <p className="text-muted-foreground">Sinulla ei ole oikeuksia tähän sivuun.</p>
    </div>
  );
}
```

### Import Patterns
```typescript
// UI components from @ui aliases
import { Button } from "@ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@ui/tabs";

// Shared auth from @shared-auth
import { useUserRole } from "@shared-auth/hooks/useUserRole";

// Local imports with @/
import AdminHeader from "@/components/admin/AdminHeader";
import { supabase } from "@/integrations/supabase/client";
```

## Existing Admin Pages Structure

### Dashboard (`AdminDashboardPage.tsx`)
- Central hub with overview cards
- Grid layout with clickable admin cards
- Stats overview widget with quick metrics
- Uses lucide-react icons (Bot, Users, Video, etc.)
- Each card has: title, description, icon, path, stats, isLoading

### Specialized Admin Pages
- `AdminAIPage.tsx` - AI management with tabs (usage, prompts, features, pricing)
- `AdminAudioPage.tsx` - Audio/TTS management
- `AdminAuthTokensPage.tsx` - Authentication and API tokens
- `AdminTopicsPage.tsx` - Topic management and translations
- `AdminUsersPage.tsx` - User and role management
- `AdminTranslationsPage.tsx` - Term translation cache
- `AdminVideoPage.tsx` - Video series and clips
- `AdminWidgetAnalyticsPage.tsx` - Widget usage statistics

## Creating New Admin Pages

### Step 1: Create Page Component

```typescript
// apps/raamattu-nyt/src/pages/AdminExamplePage.tsx

import { useUserRole } from "@shared-auth/hooks/useUserRole";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@ui/tabs";
import { Database, Loader2 } from "lucide-react";
import { AppSidebar } from "@/components/AppSidebar";
import AdminHeader from "@/components/admin/AdminHeader";
import { SidebarProvider } from "@/components/ui/sidebar";
import { supabase } from "@/integrations/supabase/client";
import { useQuery } from "@tanstack/react-query";
import { toast } from "sonner"; // Use sonner for toast notifications

const AdminExamplePage = () => {
  const { isAdmin } = useUserRole();

  // Access control
  if (!isAdmin) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-muted-foreground">Sinulla ei ole oikeuksia tähän sivuun.</p>
      </div>
    );
  }

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-background">
        <AppSidebar onNavigateToContinueAudio={() => {}} onNavigateToContinueText={() => {}} />
        <main className="flex-1 overflow-auto">
          <AdminHeader
            title="Example Management"
            description="Manage example resources"
            icon={<Database className="h-6 w-6 text-primary" />}
            showBackButton={true}
          />

          <div className="p-6">
            <div className="max-w-6xl mx-auto space-y-6">
              <Tabs defaultValue="list" className="space-y-4">
                <TabsList>
                  <TabsTrigger value="list">List</TabsTrigger>
                  <TabsTrigger value="create">Create</TabsTrigger>
                  <TabsTrigger value="settings">Settings</TabsTrigger>
                </TabsList>

                <TabsContent value="list">
                  <Card>
                    <CardHeader>
                      <CardTitle>Items</CardTitle>
                      <CardDescription>View and manage items</CardDescription>
                    </CardHeader>
                    <CardContent>
                      {/* Component content */}
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="create">
                  <Card>
                    <CardHeader>
                      <CardTitle>Create Item</CardTitle>
                      <CardDescription>Add a new item</CardDescription>
                    </CardHeader>
                    <CardContent>
                      {/* Form content */}
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default AdminExamplePage;
```

### Step 2: Add Route to App.tsx

```typescript
// apps/raamattu-nyt/src/App.tsx

import AdminExamplePage from "./pages/AdminExamplePage";

// In Routes:
<Route path="/admin/example" element={<AdminExamplePage />} />
```

### Step 3: Add Card to Admin Dashboard

```typescript
// In AdminDashboardPage.tsx adminCards array:

{
  title: "Example Management",
  description: "Manage example resources",
  icon: Database,
  path: "/admin/example",
  stats: [{ label: "items", value: itemCount || 0 }],
  isLoading: itemsLoading,
},
```

## Creating Admin Components

### Data Table Pattern

```typescript
// apps/raamattu-nyt/src/components/admin/ExampleTable.tsx

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@ui/button";
import { Badge } from "@ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@ui/table";
import { Trash2, Edit, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { supabase } from "@/integrations/supabase/client";

export const ExampleTable = () => {
  const queryClient = useQueryClient();

  // Fetch data
  const { data: items, isLoading } = useQuery({
    queryKey: ["admin-examples"],
    queryFn: async () => {
      const { data, error } = await supabase
        .from("examples")
        .select("*")
        .order("created_at", { ascending: false });

      if (error) throw error;
      return data;
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const { error } = await supabase
        .from("examples")
        .delete()
        .eq("id", id);

      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin-examples"] });
      toast.success("Item deleted successfully");
    },
    onError: (error: Error) => {
      toast.error(`Error: ${error.message}`);
    },
  });

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Created</TableHead>
          <TableHead className="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {items?.map((item) => (
          <TableRow key={item.id}>
            <TableCell className="font-medium">{item.name}</TableCell>
            <TableCell>
              <Badge variant={item.is_active ? "default" : "secondary"}>
                {item.is_active ? "Active" : "Inactive"}
              </Badge>
            </TableCell>
            <TableCell>{new Date(item.created_at).toLocaleDateString()}</TableCell>
            <TableCell className="text-right space-x-2">
              <Button variant="outline" size="sm">
                <Edit className="h-4 w-4" />
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => deleteMutation.mutate(item.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
```

### Form Component Pattern

```typescript
// apps/raamattu-nyt/src/components/admin/ExampleForm.tsx

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@ui/button";
import { Input } from "@ui/input";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@ui/form";
import { Switch } from "@ui/switch";
import { toast } from "sonner";
import { supabase } from "@/integrations/supabase/client";

const formSchema = z.object({
  name: z.string().min(3, "Name must be at least 3 characters"),
  description: z.string().optional(),
  is_active: z.boolean().default(true),
});

type FormData = z.infer<typeof formSchema>;

export const ExampleForm = () => {
  const queryClient = useQueryClient();

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      description: "",
      is_active: true,
    },
  });

  const createMutation = useMutation({
    mutationFn: async (values: FormData) => {
      const { error } = await supabase
        .from("examples")
        .insert([values]);

      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin-examples"] });
      toast.success("Item created successfully");
      form.reset();
    },
    onError: (error: Error) => {
      toast.error(`Error: ${error.message}`);
    },
  });

  const onSubmit = (values: FormData) => {
    createMutation.mutate(values);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter name" {...field} />
              </FormControl>
              <FormDescription>The name of the item</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Input placeholder="Enter description" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="is_active"
          render={({ field }) => (
            <FormItem className="flex items-center justify-between rounded-lg border p-4">
              <div className="space-y-0.5">
                <FormLabel className="text-base">Active</FormLabel>
                <FormDescription>Enable this item</FormDescription>
              </div>
              <FormControl>
                <Switch
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
            </FormItem>
          )}
        />

        <Button type="submit" disabled={createMutation.isPending}>
          {createMutation.isPending ? "Creating..." : "Create Item"}
        </Button>
      </form>
    </Form>
  );
};
```

## Best Practices

### 1. Access Control
✅ Always check `isAdmin` from `useUserRole()`
✅ Show user-friendly Finnish message: "Sinulla ei ole oikeuksia tähän sivuun."
✅ No loading spinner needed (handled by hook)

### 2. Toast Notifications
✅ Use `toast` from "sonner" (not useToast hook)
✅ `toast.success()` for success messages
✅ `toast.error()` for errors
✅ Keep messages concise and actionable

### 3. Data Fetching
✅ Use React Query (`useQuery`, `useMutation`)
✅ Always invalidate queries after mutations
✅ Handle loading states with Loader2 spinner
✅ Show empty states when no data

### 4. Layout & Styling
✅ Use SidebarProvider + AppSidebar + AdminHeader pattern
✅ Wrap content in `<div className="p-6">`
✅ Use `max-w-6xl mx-auto` for centered content
✅ Use `space-y-6` for vertical spacing
✅ Cards for section containers
✅ Tabs for multi-section pages

### 5. Icons
✅ Import from lucide-react
✅ Use consistent size: `h-4 w-4` for buttons, `h-6 w-6` for headers
✅ Add text-primary to header icons

### 6. Finnish UI Text
✅ Page titles and descriptions in Finnish when user-facing
✅ Error messages in Finnish
✅ Admin navigation in Finnish
✅ Code/technical terms can be in English

## Common UI Components

| Component | Import Path | Use For |
|-----------|-------------|---------|
| Card | @ui/card | Section containers |
| Tabs | @ui/tabs | Multi-section pages |
| Table | @ui/table | Data lists |
| Form | @ui/form | Input forms with validation |
| Button | @ui/button | Actions |
| Badge | @ui/badge | Status indicators |
| Input | @ui/input | Text inputs |
| Switch | @ui/switch | Boolean toggles |
| Select | @ui/select | Dropdowns |
| Dialog | @ui/dialog | Modals |
| AlertDialog | @ui/alert-dialog | Confirmations |
| Alert | @ui/alert | Notices and warnings |

## AdminHeader Props

```typescript
interface AdminHeaderProps {
  title: string;              // Page title (Finnish)
  description?: string;       // Optional subtitle
  icon?: React.ReactNode;    // Optional icon element
  showBackButton?: boolean;  // Show back to admin (default: true)
  showSidebarTrigger?: boolean; // Show sidebar toggle (default: true)
}
```

## Dashboard Card Props

```typescript
interface AdminCardProps {
  title: string;             // Card title (Finnish)
  description: string;       // Card description (Finnish)
  icon: React.ElementType;  // Lucide icon component
  path: string;             // Navigation path
  stats?: Array<{           // Optional statistics
    label: string;
    value: string | number;
  }>;
  isLoading?: boolean;      // Show skeleton for stats
  isExternal?: boolean;     // Open in new window
}
```

## Token Management

### Important Admin Features
- **Authentication Tokens**: Manage Supabase keys, Turnstile tokens
- **OAuth Providers**: Google, Apple (planned)
- **Integration Tokens**: OpenAI, ElevenLabs API keys
- **Direct Dashboard Links**: Quick access to external services
- **Copy-to-clipboard**: Environment variable names
- **Regeneration Guidelines**: When and how to rotate keys
- **Security Warnings**: Sensitive key indicators

### Token Card Pattern
```typescript
<Card>
  <CardHeader>
    <CardTitle className="flex items-center gap-2">
      {token.name}
      {token.isSensitive && (
        <Badge variant="outline" className="bg-red-500/10">
          <Shield className="h-3 w-3 mr-1" />
          Sensitive
        </Badge>
      )}
    </CardTitle>
  </CardHeader>
  <CardContent className="space-y-4">
    {/* Environment variable with copy button */}
    {/* Location info */}
    {/* Usage badges */}
    {/* Dashboard links */}
    {/* Regeneration info */}
  </CardContent>
</Card>
```

## Related Files

### Key Admin Files
- `apps/raamattu-nyt/src/pages/AdminDashboardPage.tsx` - Dashboard hub
- `apps/raamattu-nyt/src/pages/AdminAuthTokensPage.tsx` - Token management example
- `apps/raamattu-nyt/src/components/admin/AdminHeader.tsx` - Header component
- `apps/raamattu-nyt/src/App.tsx` - Route definitions

### Documentation
- `Docs/07-ADMIN-GUIDE.md` - Admin features overview
- `Docs/12-AUTHENTICATION.md` - Auth system details
- `Docs/context/supabase-map.md` - Database schema reference

## Common Patterns

### Stats Query Pattern
```typescript
const { data: itemCount, isLoading } = useQuery({
  queryKey: ["admin-item-count"],
  queryFn: async () => {
    const { count } = await supabase
      .from("items")
      .select("*", { count: "exact", head: true });
    return count || 0;
  },
  enabled: isAdmin, // Only fetch if admin
});
```

### RPC Call Pattern
```typescript
const { data } = await supabase.rpc("get_admin_stats", {
  p_limit: 1000,
});
```

### Conditional Rendering
```typescript
{stats && stats.length > 0 && (
  <CardContent>
    <div className="flex gap-3">
      {isLoading ? (
        <Skeleton className="h-4 w-20" />
      ) : (
        stats.map((stat, i) => (
          <div key={i}>
            <span className="font-semibold">{stat.value}</span>
            <span className="text-muted-foreground ml-1">{stat.label}</span>
          </div>
        ))
      )}
    </div>
  </CardContent>
)}
```

## Tips

1. **Keep components focused**: One component per file, single responsibility
2. **Extract complex logic**: Move business logic to separate functions/hooks
3. **Type everything**: Use TypeScript interfaces for all data structures
4. **Test queries first**: Verify Supabase queries in SQL editor before implementing
5. **Handle empty states**: Always show something when data is empty
6. **Loading states matter**: Use skeletons for stats, spinners for content
7. **Error boundaries**: Wrap risky operations in try-catch
8. **Invalidate smartly**: Only invalidate affected queries after mutations
9. **Consistent naming**: Use Finnish for UI, English for code
10. **Document complex logic**: Add comments for non-obvious implementations
