---
name: component-hierarchy
description: Guide component selection in ResRequest Vue projects. Ensures correct usage of ShadCN-Vue vs custom components, proper imports, and design system compliance. Activates when creating or modifying Vue components.
---

# Component Hierarchy

Follow this selection order when choosing components for ResRequest projects.

## Selection Priority

### 1. ShadCN-Vue Components (First Choice)
Located at `@/components/ui/`

Always check ShadCN-Vue first. These are the base UI components.

**NEVER modify files in `@/components/ui/`** - these are managed by ShadCN.

### 2. Custom Components (Second Choice)
Located at `@/components/custom/`

Project-specific wrappers and extensions of ShadCN components.

### 3. Feature Components (Third Choice)
Located at `@/components/[feature]/`

Domain-specific components for features like email-threads, comments, bookings.

## ShadCN-Vue Component Reference

### Buttons
```typescript
import { Button } from '@/components/ui/button'

<Button>Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Cancel</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button disabled>Disabled</Button>
```

### Form Inputs
```typescript
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Checkbox } from '@/components/ui/checkbox'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Switch } from '@/components/ui/switch'

// Basic input
<div class="space-y-2">
    <Label for="email">Email</Label>
    <Input id="email" type="email" v-model="email" />
</div>
```

### Select/Dropdown
```typescript
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'

<Select v-model="selected">
    <SelectTrigger>
        <SelectValue placeholder="Select option" />
    </SelectTrigger>
    <SelectContent>
        <SelectItem value="option1">Option 1</SelectItem>
        <SelectItem value="option2">Option 2</SelectItem>
    </SelectContent>
</Select>
```

### Cards
```typescript
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'

<Card>
    <CardHeader>
        <CardTitle>Card Title</CardTitle>
        <CardDescription>Card description</CardDescription>
    </CardHeader>
    <CardContent>
        <p>Card content</p>
    </CardContent>
    <CardFooter>
        <Button>Action</Button>
    </CardFooter>
</Card>
```

### Dialogs/Modals
```typescript
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog'

<Dialog v-model:open="isOpen">
    <DialogTrigger as-child>
        <Button>Open Dialog</Button>
    </DialogTrigger>
    <DialogContent>
        <DialogHeader>
            <DialogTitle>Dialog Title</DialogTitle>
            <DialogDescription>Dialog description</DialogDescription>
        </DialogHeader>
        <div>Content here</div>
        <DialogFooter>
            <Button variant="outline" @click="isOpen = false">Cancel</Button>
            <Button @click="save">Save</Button>
        </DialogFooter>
    </DialogContent>
</Dialog>
```

### Tables
```typescript
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'

<Table>
    <TableHeader>
        <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Actions</TableHead>
        </TableRow>
    </TableHeader>
    <TableBody>
        <TableRow v-for="user in users" :key="user.id">
            <TableCell>{{ user.name }}</TableCell>
            <TableCell>{{ user.email }}</TableCell>
            <TableCell>
                <Button size="sm" variant="ghost">Edit</Button>
            </TableCell>
        </TableRow>
    </TableBody>
</Table>
```

### Badges
```typescript
import { Badge } from '@/components/ui/badge'

<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
```

### Alerts
```typescript
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

<Alert>
    <AlertTitle>Heads up!</AlertTitle>
    <AlertDescription>This is an alert message.</AlertDescription>
</Alert>

<Alert variant="destructive">
    <AlertTitle>Error</AlertTitle>
    <AlertDescription>Something went wrong.</AlertDescription>
</Alert>
```

### Tabs
```typescript
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

<Tabs default-value="tab1">
    <TabsList>
        <TabsTrigger value="tab1">Tab 1</TabsTrigger>
        <TabsTrigger value="tab2">Tab 2</TabsTrigger>
    </TabsList>
    <TabsContent value="tab1">Content 1</TabsContent>
    <TabsContent value="tab2">Content 2</TabsContent>
</Tabs>
```

## Custom Components

### FloatingLabelInput (ALWAYS use for form fields)
```typescript
import FloatingLabelInput from '@/components/custom/FloatingLabelInput.vue'

<FloatingLabelInput
    v-model="form.name"
    label="Name"
    :error="form.errors.name"
    required
/>

<FloatingLabelInput
    v-model="form.email"
    label="Email"
    type="email"
    :error="form.errors.email"
/>
```

### RRIcon (Custom icons)
```typescript
import RRIcon from '@/components/custom/icon/RRIcon.vue'

<RRIcon name="calendar" />
<RRIcon name="user" class="h-5 w-5" />
```

## Component Rules

### 1. Never Modify ShadCN Files
```
@/components/ui/ is READ-ONLY

To customise ShadCN components:
1. Create wrapper in @/components/custom/
2. Import and extend the base component
3. Add custom props/styles in wrapper
```

### 2. Always Use FloatingLabelInput for Forms
```vue
<!-- WRONG: Raw Input -->
<Input v-model="name" />

<!-- CORRECT: FloatingLabelInput -->
<FloatingLabelInput v-model="name" label="Name" />
```

### 3. Use Tailwind Utilities Only
```vue
<!-- WRONG: Custom CSS -->
<style scoped>
.custom-button {
    background-color: blue;
}
</style>

<!-- CORRECT: Tailwind classes -->
<Button class="bg-blue-500 hover:bg-blue-600">
    Custom Button
</Button>
```

### 4. Check ShadCN Examples
Before creating a custom component, check if ShadCN already provides it:
- View examples at `/page/admin/shadcn-components` in the app
- Check ShadCN-Vue documentation

### 5. Component Composition
Compose complex UIs from ShadCN primitives:

```vue
<Card>
    <CardHeader>
        <div class="flex items-center justify-between">
            <CardTitle>{{ title }}</CardTitle>
            <Badge :variant="statusVariant">{{ status }}</Badge>
        </div>
    </CardHeader>
    <CardContent>
        <Table>
            <!-- Table content -->
        </Table>
    </CardContent>
    <CardFooter class="flex justify-end gap-2">
        <Button variant="outline">Cancel</Button>
        <Button>Save</Button>
    </CardFooter>
</Card>
```

## Import Patterns

### Correct Imports
```typescript
// ShadCN components - destructured import
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader } from '@/components/ui/card'

// Custom components - default import
import FloatingLabelInput from '@/components/custom/FloatingLabelInput.vue'
import RRIcon from '@/components/custom/icon/RRIcon.vue'

// Feature components - default import
import CommentThread from '@/components/comments/CommentThread.vue'
```

### Import Organisation
```typescript
// 1. Vue core
import { ref, computed, watch } from 'vue'

// 2. Inertia
import { useForm, router, Link } from '@inertiajs/vue3'

// 3. ShadCN UI components
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

// 4. Custom components
import FloatingLabelInput from '@/components/custom/FloatingLabelInput.vue'

// 5. Composables
import { useBookings } from '@/composables/useBookings'

// 6. Types
import type { Booking, Property } from '@/types'
```
