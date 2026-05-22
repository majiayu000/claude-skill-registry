---
name: generate-form
description: Generate form component with validation, state management, and submit handling. Use when creating new data entry forms.
allowed-tools: Read, Write, Glob, Grep
---

# Generate Form

Generate a form component with validation and store integration.

## Usage

When user requests to create a form component, ask for:

1. **Form name** (e.g., "WaterIntakeForm", "SleepLogForm")
2. **Fields** needed (name, type, validation rules)
3. **Store action** to call on submit (e.g., "addWaterLog")
4. **Whether it includes a list** (add/remove items like MealLogForm)

## Implementation Pattern

Based on `src/components/forms/MealLogForm.tsx` pattern.

### File Structure

Create file: `src/components/forms/{FormName}.tsx`

```typescript
'use client';

import { useState } from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Trash2, Plus, Loader2 } from 'lucide-react';
import { useHealthStore } from '@/lib/store/healthStore';
import { toast } from 'sonner';

export function FormName() {
  const [field1, setField1] = useState('');
  const [field2, setField2] = useState('');
  const { addItem, isLoading } = useHealthStore();
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!field1.trim()) {
      newErrors.field1 = 'Field 1 is required';
    }

    if (!field2.trim()) {
      newErrors.field2 = 'Field 2 is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    const today = new Date().toISOString().split('T')[0];
    try {
      await addItem({
        date: today,
        field1,
        field2,
      });
      setField1('');
      setField2('');
      setErrors({});
    } catch (error: any) {
      toast.error(error.message || 'Failed to submit form');
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Form Title</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="field1">Field 1 Label</Label>
          <Input
            id="field1"
            type="text"
            placeholder="Enter value"
            value={field1}
            onChange={(e) => setField1(e.target.value)}
            disabled={isLoading}
          />
          {errors.field1 && <p className="text-xs text-red-500">{errors.field1}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="field2">Field 2 Label</Label>
          <Input
            id="field2"
            type="number"
            placeholder="0"
            value={field2}
            onChange={(e) => setField2(e.target.value)}
            disabled={isLoading}
          />
          {errors.field2 && <p className="text-xs text-red-500">{errors.field2}</p>}
        </div>
      </CardContent>
      <CardFooter>
        <Button onClick={handleSubmit} disabled={isLoading} className="w-full">
          {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Submit
        </Button>
      </CardFooter>
    </Card>
  );
}
```

### With List Management (Optional)

For forms that add/remove items from a list:

```typescript
'use client';

import { useState } from 'react';
import { Trash2, Plus } from 'lucide-react';

export function FormWithList() {
  const [items, setItems] = useState<any[]>([]);
  const [currentItem, setCurrentItem] = useState('');

  const addItem = () => {
    if (!currentItem.trim()) {
      toast.error('Item cannot be empty');
      return;
    }
    setItems([...items, { id: Date.now(), name: currentItem }]);
    setCurrentItem('');
    toast.success(`Added ${currentItem}`);
  };

  const removeItem = (index: number) => {
    const itemName = items[index].name;
    setItems(items.filter((_, i) => i !== index));
    toast.info(`Removed ${itemName}`);
  };

  return (
    <>
      <div className="flex gap-2">
        <Input
          value={currentItem}
          onChange={(e) => setCurrentItem(e.target.value)}
          placeholder="Enter item"
        />
        <Button onClick={addItem} variant="outline" size="sm">
          <Plus className="h-4 w-4" />
        </Button>
      </div>

      <div className="space-y-2 mt-4">
        {items.map((item, index) => (
          <div key={item.id} className="flex items-center justify-between bg-muted p-2 rounded">
            <span>{item.name}</span>
            <Button
              onClick={() => removeItem(index)}
              variant="ghost"
              size="sm"
            >
              <Trash2 className="h-4 w-4 text-destructive" />
            </Button>
          </div>
        ))}
      </div>
    </>
  );
}
```

## Key Conventions

- Use `'use client'` directive at top
- useState for all form fields
- useHealthStore hook for store actions
- Validation function before submit
- Try-catch-toast error handling
- Set isLoading state on button during submission
- Clear form fields after successful submit
- Use shadcn/ui components (Input, Button, Label, etc.)
- Show validation errors below each field
- Disable inputs while loading
- Use Loader2 icon for loading state
- Toast notifications for all user actions

## Steps

1. Ask user for form name, fields, store action, and list management
2. Create file: `src/components/forms/{FormName}.tsx`
3. Generate component with Card wrapper
4. Add useState for each field
5. Add useHealthStore hook integration
6. Add validation function
7. Add handleSubmit with try-catch-toast
8. Add form fields with shadcn/ui components
9. Add list management if requested
10. Format with Prettier

## Implementation Checklist

- [ ] Component exports correctly
- [ ] 'use client' directive present
- [ ] useState for all fields
- [ ] useHealthStore hook imported
- [ ] Validation function implemented
- [ ] Error state management
- [ ] handleSubmit with try-catch
- [ ] Toast notifications added
- [ ] isLoading state used
- [ ] shadcn/ui components used
- [ ] Error messages displayed
- [ ] List management (if applicable)
