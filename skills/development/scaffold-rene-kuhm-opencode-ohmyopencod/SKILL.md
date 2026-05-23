---
description: "Crear componentes, páginas, hooks y servicios con estructura enterprise. Scaffolding automático."
user-invocable: true
argument-hint: "[component|page|hook|service|api] <name> [--path src/]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# Scaffold Skill

Genera código boilerplate siguiendo las mejores prácticas y la estructura del proyecto.

## Tipos de Scaffold

### 1. Component

```bash
/scaffold component Button
/scaffold component UserCard --path src/components/features/
```

**Genera:**
```
src/components/ui/Button/
├── Button.tsx
├── Button.test.tsx
├── Button.types.ts
└── index.ts
```

**Template Component:**
```typescript
// Button.tsx
import { type ButtonProps } from './Button.types';
import { cn } from '@/lib/utils';

export function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium',
        variants[variant],
        sizes[size],
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}
```

**Template Types:**
```typescript
// Button.types.ts
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}
```

**Template Test:**
```typescript
// Button.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('should render children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should handle click events', async () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click</Button>);
    await userEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

---

### 2. Page (Next.js App Router)

```bash
/scaffold page dashboard
/scaffold page settings/profile
```

**Genera:**
```
src/app/dashboard/
├── page.tsx
├── loading.tsx
├── error.tsx
└── layout.tsx (opcional)
```

**Template Page:**
```typescript
// page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Dashboard',
  description: 'User dashboard',
};

export default async function DashboardPage() {
  return (
    <main className="container mx-auto py-8">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      {/* Content */}
    </main>
  );
}
```

---

### 3. Hook

```bash
/scaffold hook useAuth
/scaffold hook useProducts
```

**Genera:**
```
src/hooks/
├── use-auth.ts
└── use-auth.test.ts
```

**Template Hook:**
```typescript
// use-auth.ts
import { useState, useEffect, useCallback } from 'react';

interface UseAuthOptions {
  redirectTo?: string;
}

interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => Promise<void>;
}

export function useAuth(options: UseAuthOptions = {}): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check auth status on mount
    checkAuth().then(setUser).finally(() => setIsLoading(false));
  }, []);

  const login = useCallback(async (credentials: Credentials) => {
    const user = await authService.login(credentials);
    setUser(user);
  }, []);

  const logout = useCallback(async () => {
    await authService.logout();
    setUser(null);
  }, []);

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    logout,
  };
}
```

---

### 4. Service

```bash
/scaffold service user
/scaffold service payment
```

**Genera:**
```
src/services/
├── user.service.ts
└── user.service.test.ts
```

**Template Service:**
```typescript
// user.service.ts
import { prisma } from '@/lib/prisma';
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;

export class UserService {
  async findById(id: string) {
    return prisma.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string) {
    return prisma.user.findUnique({ where: { email } });
  }

  async create(input: CreateUserInput) {
    const data = CreateUserSchema.parse(input);
    return prisma.user.create({ data });
  }

  async update(id: string, input: Partial<CreateUserInput>) {
    return prisma.user.update({
      where: { id },
      data: input,
    });
  }

  async delete(id: string) {
    return prisma.user.delete({ where: { id } });
  }
}

export const userService = new UserService();
```

---

### 5. API Route

```bash
/scaffold api users
/scaffold api products/[id]
```

**Genera:**
```
src/app/api/users/
└── route.ts
```

**Template API:**
```typescript
// route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { userService } from '@/services/user.service';

const CreateSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '20');

    const users = await userService.findMany({ page, limit });
    return NextResponse.json({ data: users });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const data = CreateSchema.parse(body);
    const user = await userService.create(data);
    return NextResponse.json({ data: user }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Proceso

1. Detectar estructura del proyecto
2. Verificar si ya existe el archivo
3. Crear archivos con templates
4. Actualizar barrel exports (index.ts)
5. Mostrar archivos creados
