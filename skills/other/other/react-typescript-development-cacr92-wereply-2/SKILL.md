---
name: react-typescript-development
description: 当用户要求"开发 React 组件"、"编写前端代码"、"创建界面"、"实现状态管理"、"前端开发"、"TanStack Query"、"Ant Design"、"AI 聊天组件"、"配方管理界面"、"Hooks 优化"、"表单验证"、"响应式布局"、"类型安全"、"避免 as any"、"组件性能"、"useMemo"、"useCallback"、"React.memo"，或者提到"React开发"、"前端开发"、"组件"、"UI"、"桌面应用界面"、"TypeScript"、"类型检查"时使用此技能。用于开发 React 19 组件、TypeScript 5、Ant Design、Hooks 最佳实践、TanStack Query 状态管理、性能优化或创建 Tauri 饲料配方系统的类型安全前端界面。
version: 3.0.0
---

# React TypeScript Development Skill

Expert guidance for React 19 + TypeScript 5 + Ant Design + Tauri frontend development.

## Component Development

### Functional Component Pattern

```typescript
import React, { useState, useCallback } from 'react';
import { Button, Form, Input, message } from 'antd';
import type { FormProps } from 'antd';

interface MyComponentProps {
  initialValue?: string;
  onSave: (value: string) => Promise<void>;
}

export const MyComponent: React.FC<MyComponentProps> = ({
  initialValue,
  onSave,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = useCallback(async (values: any) => {
    try {
      setLoading(true);
      await onSave(values.name);
      message.success('保存成功');
      form.resetFields();
    } catch (error) {
      message.error(`保存失败: ${error}`);
    } finally {
      setLoading(false);
    }
  }, [onSave, form]);

  return (
    <Form
      form={form}
      onFinish={handleSubmit}
      initialValues={{ name: initialValue }}
    >
      <Form.Item
        name="name"
        label="名称"
        rules={[
          { required: true, message: '请输入名称' },
          { min: 2, max: 50, message: '名称长度为 2-50 个字符' }
        ]}
      >
        <Input placeholder="请输入名称" />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          保存
        </Button>
      </Form.Item>
    </Form>
  );
};
```

## Hooks Best Practices

### Custom Hook Pattern

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import type { Material } from '../bindings';

export function useMaterials() {
  const queryClient = useQueryClient();

  const { data: materials, isLoading } = useQuery({
    queryKey: ['materials'],
    queryFn: async () => {
      const result = await commands.getMaterials();
      if (!result.success) {
        throw new Error(result.message);
      }
      return result.data;
    },
  });

  const createMutation = useMutation({
    mutationFn: async (dto: CreateMaterialDto) => {
      const result = await commands.createMaterial(dto);
      if (!result.success) {
        throw new Error(result.message);
      }
      return result.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['materials'] });
      message.success('创建成功');
    },
    onError: (error: Error) => {
      message.error(`创建失败: ${error.message}`);
    },
  });

  return {
    materials,
    isLoading,
    createMaterial: createMutation.mutate,
  };
}
```

### Rules of Hooks Compliance

```typescript
// ❌ Bad - Hook inside condition
if (condition) {
  const [value, setValue] = useState(0);
}

// ❌ Bad - Hook inside loop
items.map((item, index) => {
  const [value, setValue] = useState(item);
  return <div key={index}>{value}</div>;
})

// ✅ Good - Hooks at top level
export const GoodComponent: React.FC = () => {
  const [value, setValue] = useState(0);
  const items = useItems();

  return items.map((item) => <Item key={item.id} item={item} />);
}
```

## State Management

### TanStack Query Patterns

```typescript
// Fetching data
const { data, isLoading, error } = useQuery({
  queryKey: ['formulas', 'list'],
  queryFn: async () => {
    const result = await commands.getFormulas();
    if (!result.success) throw new Error(result.message);
    return result.data;
  },
});

// Dependent queries
const { data: formula } = useQuery({
  queryKey: ['formula', formulaId],
  queryFn: async () => {
    const result = await commands.getFormula(formulaId);
    if (!result.success) throw new Error(result.message);
    return result.data;
  },
  enabled: !!formulaId, // Only run when formulaId exists
});

// Mutations with invalidation
const mutation = useMutation({
  mutationFn: (dto: CreateDto) => commands.createFormula(dto),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['formulas'] });
  },
});
```

### Local State vs Global State

```typescript
// ✅ Local state - Component-specific
const [isOpen, setIsOpen] = useState(false);
const [selectedId, setSelectedId] = useState<number | null>(null);

// ✅ Global state - Shared across components
const FormulasContext = createContext<FormulasContextType | undefined>(undefined);

export const useFormulas = () => {
  const context = useContext(FormulasContext);
  if (!context) {
    throw new Error('useFormulas must be used within FormulasProvider');
  }
  return context;
};
```

## Tauri Integration

### Type-Safe Commands

```typescript
// ✅ Use generated commands
import { commands } from '../bindings';
import type { Formula, Material } from '../bindings';

export async function loadFormula(id: number): Promise<Formula> {
  const result = await commands.getFormula(id);
  if (!result.success) {
    message.error(result.message);
    throw new Error(result.message);
  }
  return result.data;
}

// ❌ Don't use raw invoke
import { invoke } from '@tauri-apps/api/core';
const data = await invoke('get_formula', { id }); // Untyped!
```

### Error Handling

```typescript
import { message } from 'antd';
import { commands } from '../bindings';

export async function handleCommand<T>(
  commandFn: () => Promise<ApiResponse<T>>
): Promise<T | null> {
  try {
    const result = await commandFn();
    if (!result.success) {
      message.error(result.message);
      return null;
    }
    return result.data;
  } catch (error) {
    message.error(`操作失败: ${error}`);
    return null;
  }
}
```

## Ant Design Usage

### Message Component (No Console)

```typescript
// ❌ Bad - Console logging (desktop app!)
console.log('Data loaded', data);
console.error('Error occurred', error);

// ✅ Good - User-facing messages
import { message } from 'antd';

message.success('数据加载成功');
message.error('加载失败，请重试');
message.warning('请注意数据可能未保存');
message.info('正在处理中...');
```

### Form Validation

```typescript
const [form] = Form.useForm();

const validateFormulaName = (_: RuleObject, value: string) => {
  if (!value || value.length < 2) {
    return Promise.reject('配方名称至少2个字符');
  }
  if (value.length > 50) {
    return Promise.reject('配方名称最多50个字符');
  }
  return Promise.resolve();
};

<Form.Item
  name="name"
  label="配方名称"
  rules={[
    { required: true, message: '请输入配方名称' },
    { validator: validateFormulaName }
  ]}
>
  <Input placeholder="请输入配方名称" />
</Form.Item>
```

## Performance Optimization

### React.memo for Components

```typescript
import React, { memo } from 'react';

interface MaterialRowProps {
  material: Material;
  onSelect: (code: string) => void;
}

export const MaterialRow = memo<MaterialRowProps>(({ material, onSelect }) => {
  console.log('Rendering MaterialRow:', material.code); // For debugging
  return (
    <tr onClick={() => onSelect(material.code)}>
      <td>{material.name}</td>
      <td>{material.price}</td>
    </tr>
  );
});

MaterialRow.displayName = 'MaterialRow';
```

### useCallback and useMemo

```typescript
export const FormulaList: React.FC = () => {
  const { formulas } = useFormulas();

  // ✅ Memoize expensive calculations
  const totalCost = useMemo(() => {
    return formulas.reduce((sum, f) => sum + f.total_cost, 0);
  }, [formulas]);

  // ✅ Stable function reference
  const handleSelect = useCallback((id: number) => {
    // Handle selection
  }, []);

  return (
    <div>
      <p>Total: {totalCost}</p>
      {formulas.map(f => (
        <FormulaCard key={f.id} formula={f} onSelect={handleSelect} />
      ))}
    </div>
  );
};
```

## TypeScript Best Practices

### Type Safety (No 'as any')

```typescript
// ❌ Bad - Using 'as any'
const data = response.data as any;
const name = data.someField; // No type checking

// ✅ Good - Proper types
interface ApiResponse {
  data: {
    name: string;
    someField: string;
  };
}

const data = (response as ApiResponse).data;
const name = data.someField; // Type safe!

// ✅ Better - Type guards
function isApiResponse(data: unknown): data is ApiResponse {
  return (
    typeof data === 'object' &&
    data !== null &&
    'data' in data
  );
}
```

### Type Imports

```typescript
// ✅ Use type-only imports when possible
import type { Formula, Material } from '../bindings';
import { commands } from '../bindings'; // Value import
```

## Desktop Application Considerations

### File System Access

```typescript
import { open, save } from '@tauri-apps/plugin-dialog';
import { readTextFile, writeTextFile } from '@tauri-apps/plugin-fs';

export async function openFormulaFile() {
  const selected = await open({
    multiple: false,
    filters: [{
      name: 'Formula',
      extensions: ['json']
    }]
  });

  if (selected && typeof selected === 'string') {
    const contents = await readTextFile(selected);
    return JSON.parse(contents);
  }
}
```

### Platform-Specific Code

```typescript
import { platform } from '@tauri-apps/plugin-os';

export function getPlatformShortcut(): string {
  switch (platform()) {
    case 'darwin':
      return '⌘ + S';
    case 'windows':
      return 'Ctrl + S';
    case 'linux':
      return 'Ctrl + S';
    default:
      return 'Ctrl + S';
  }
}
```

## Common Pitfalls

### ❌ Inefficient Re-renders

```typescript
// ❌ Creating new function on every render
{items.map(item => (
  <Item key={item.id} item={item} onDelete={() => handleDelete(item.id)} />
))}

// ✅ Stable callback with useCallback
const handleDelete = useCallback((id: number) => {
  // Delete logic
}, []);

{items.map(item => (
  <Item key={item.id} item={item} onDelete={handleDelete} />
))}
```

### ❌ Missing Dependencies

```typescript
// ❌ Missing dependency
useEffect(() => {
  fetchData(category);
}, []); // Missing 'category' dependency!

// ✅ All dependencies included
useEffect(() => {
  fetchData(category);
}, [category]);
```

### ❌ Index as Key

```typescript
// ❌ Using index as key (bad for lists that change)
{items.map((item, index) => (
  <div key={index}>{item.name}</div>
))}

// ✅ Using unique ID as key
{items.map(item => (
  <div key={item.id}>{item.name}</div>
))}
```

## Testing Guidelines

### Component Testing

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FormulaForm } from './FormulaForm';

describe('FormulaForm', () => {
  it('should submit form data', async () => {
    const mockSave = vi.fn().mockResolvedValue({ success: true });
    render(<FormulaForm onSave={mockSave} />);

    fireEvent.change(screen.getByLabelText(/配方名称/), {
      target: { value: '测试配方' }
    });

    fireEvent.click(screen.getByText(/保存/));

    await waitFor(() => {
      expect(mockSave).toHaveBeenCalledWith({ name: '测试配方' });
    });
  });
});
```

## When to Use This Skill

Activate this skill when:
- Creating React components with TypeScript
- Implementing custom hooks
- Working with Ant Design components
- Handling state with TanStack Query
- Integrating with Tauri commands
- Optimizing component performance
- Writing type-safe frontend code
- Handling desktop-specific features
