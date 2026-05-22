---
name: radtools
description: RadTools UI component API. Use when building interfaces with Button, Card, Tabs, Dialog, and other design system components. Quick reference with copy-paste examples.
---

# RadTools Components

Import from `@/components/ui`. All components follow retro OS aesthetics.

## Design Principles

- **Colors**: cream (#FEF8E2), sun-yellow (#FCE184), black (#0F0E0C)
- **Typography**: `font-joystix` (headings), `font-mondwest` (body)
- **Shadows**: 2px for buttons, 4px for cards
- **Disabled**: 50% opacity + cursor-not-allowed

---

## Button

```tsx
import { Button } from '@/components/ui';

// Variants
<Button variant="primary">Primary</Button>   // yellow bg
<Button variant="secondary">Secondary</Button> // black bg
<Button variant="outline">Outline</Button>   // border only
<Button variant="ghost">Ghost</Button>       // minimal

// With icon
<Button iconName="download">Download</Button>
<Button iconOnly iconName="close" aria-label="Close" />

// States
<Button loading>Saving...</Button>
<Button disabled>Disabled</Button>
<Button fullWidth>Full Width</Button>

// As link
<Button href="/about">Learn More</Button>
```

**Props**: `variant`, `size` (sm/md/lg), `iconName`, `iconOnly`, `loading`, `disabled`, `fullWidth`, `href`

---

## Card

```tsx
import { Card, CardHeader, CardBody, CardFooter } from '@/components/ui';

// Basic
<Card>Content</Card>

// Variants
<Card variant="dark">Dark card</Card>
<Card variant="raised">With shadow</Card>

// With structure
<Card noPadding>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
  <CardFooter><Button>Action</Button></CardFooter>
</Card>
```

**Props**: `variant` (default/dark/raised), `noPadding`

---

## Tabs

```tsx
import { Tabs, TabList, TabTrigger, TabContent } from '@/components/ui';

<Tabs defaultValue="tab1">
  <TabList>
    <TabTrigger value="tab1">Tab 1</TabTrigger>
    <TabTrigger value="tab2" iconName="settings">Tab 2</TabTrigger>
  </TabList>
  <TabContent value="tab1">Content 1</TabContent>
  <TabContent value="tab2">Content 2</TabContent>
</Tabs>

// Controlled
const [tab, setTab] = useState('tab1');
<Tabs value={tab} onValueChange={setTab}>...</Tabs>
```

**Props**: `defaultValue`, `value`, `onValueChange`, `variant` (pill/line)

---

## Dialog

```tsx
import {
  Dialog, DialogTrigger, DialogContent,
  DialogHeader, DialogTitle, DialogDescription,
  DialogBody, DialogFooter, DialogClose
} from '@/components/ui';

<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    <DialogBody>Content</DialogBody>
    <DialogFooter>
      <DialogClose asChild><Button variant="outline">Cancel</Button></DialogClose>
      <Button>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

---

## Form Components

```tsx
import { Input, TextArea, Label, Select, Checkbox, Radio, Switch, Slider } from '@/components/ui';

// Input
<Label htmlFor="name">Name</Label>
<Input id="name" placeholder="Enter name" />
<TextArea rows={4} placeholder="Description" />

// Select
<Select>
  <option value="">Choose...</option>
  <option value="a">Option A</option>
</Select>

// Controls
<Checkbox id="agree" /> <label htmlFor="agree">Agree</label>
<Radio name="size" value="sm" /> Small
<Switch checked={enabled} onCheckedChange={setEnabled} />
<Slider value={50} onValueChange={setValue} min={0} max={100} />
```

---

## Feedback Components

```tsx
import { Badge, Alert, Progress, Spinner, Tooltip, Toast, useToast } from '@/components/ui';

// Badge
<Badge>Default</Badge>
<Badge variant="success">Success</Badge>
<Badge variant="error">Error</Badge>

// Alert
<Alert>Info message</Alert>
<Alert variant="error">Error message</Alert>

// Loading
<Progress value={65} />
<Spinner size={24} />

// Tooltip
<Tooltip content="Helpful info">
  <Button>Hover me</Button>
</Tooltip>

// Toast (requires ToastProvider)
const { toast } = useToast();
toast({ title: 'Saved!', variant: 'success' });
```

---

## Overlay Components

```tsx
// Sheet (slide-out panel)
import { Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle } from '@/components/ui';

<Sheet>
  <SheetTrigger asChild><Button>Open</Button></SheetTrigger>
  <SheetContent side="right">
    <SheetHeader><SheetTitle>Panel</SheetTitle></SheetHeader>
    Content here
  </SheetContent>
</Sheet>

// DropdownMenu
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui';

<DropdownMenu>
  <DropdownMenuTrigger asChild><Button iconOnly iconName="more" /></DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem onSelect={() => {}}>Edit</DropdownMenuItem>
    <DropdownMenuItem onSelect={() => {}}>Delete</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>

// Popover
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui';

<Popover>
  <PopoverTrigger asChild><Button>Info</Button></PopoverTrigger>
  <PopoverContent>Details here</PopoverContent>
</Popover>
```

---

## Navigation Components

```tsx
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui';
import { Breadcrumbs, Divider } from '@/components/ui';

// Accordion
<Accordion type="single" collapsible>
  <AccordionItem value="1">
    <AccordionTrigger>Section 1</AccordionTrigger>
    <AccordionContent>Content</AccordionContent>
  </AccordionItem>
</Accordion>

// Breadcrumbs
<Breadcrumbs items={[
  { label: 'Home', href: '/' },
  { label: 'Current' }
]} />

// Divider
<Divider />
<Divider orientation="vertical" className="h-6" />
```

---

## Common Patterns

### Loading State
```tsx
if (isLoading) {
  return (
    <div className="flex items-center justify-center p-8">
      <Spinner />
      <span className="ml-2 font-joystix text-pixel-sm">LOADING...</span>
    </div>
  );
}
```

### Form with Validation
```tsx
<Card>
  <form onSubmit={handleSubmit}>
    <Label htmlFor="email">Email</Label>
    <Input id="email" className={error ? 'border-sun-red' : ''} />
    {error && <p className="text-sun-red text-xs mt-1">{error}</p>}
    <Button type="submit" fullWidth>Submit</Button>
  </form>
</Card>
```

### Confirm Dialog
```tsx
<Dialog>
  <DialogTrigger asChild><Button variant="outline">Delete</Button></DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm Delete</DialogTitle>
      <DialogDescription>This cannot be undone.</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <DialogClose asChild><Button variant="outline">Cancel</Button></DialogClose>
      <Button onClick={onDelete}>Delete</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

