---
name: heroui-components
description: Add or customize HeroUI components in the web application. Use when implementing new UI features with HeroUI design system or updating component styling.
allowed-tools: Read, Edit, Write, mcp__heroui-react__list_components, mcp__heroui-react__get_component_info, mcp__heroui-react__get_component_examples
---

# HeroUI Components Skill

This skill helps you work with HeroUI (Hero UI / NextUI v3) components in `apps/web/`.

## When to Use This Skill

- Adding new HeroUI components to pages
- Customizing HeroUI component variants
- Implementing forms with HeroUI inputs
- Creating modal dialogs and drawers
- Building navigation with HeroUI components
- Debugging HeroUI styling issues

## HeroUI Overview

HeroUI is a modern React UI library built on Tailwind CSS and React Aria, providing accessible components.

## Discovery and Research

### List Available Components

```typescript
// Use MCP tool to discover components
mcp__heroui-react__list_components()
```

### Get Component Information

```typescript
// Get details about a specific component
mcp__heroui-react__get_component_info({ component: "Button" })
mcp__heroui-react__get_component_info({ component: "Input" })
```

### Get Usage Examples

```typescript
// Get examples for a component
mcp__heroui-react__get_component_examples({ component: "Modal" })
```

## Installation and Setup

HeroUI is already installed in the web app. Import from `@heroui/react`:

```typescript
import { Button, Input, Card } from "@heroui/react";
```

## Common Components

### 1. Button Component

```typescript
import { Button } from "@heroui/react";

export function ActionButton() {
  return (
    <>
      {/* Basic button */}
      <Button>Click me</Button>

      {/* Color variants */}
      <Button color="primary">Primary</Button>
      <Button color="secondary">Secondary</Button>
      <Button color="success">Success</Button>
      <Button color="warning">Warning</Button>
      <Button color="danger">Danger</Button>

      {/* Size variants */}
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>

      {/* Variants */}
      <Button variant="solid">Solid</Button>
      <Button variant="bordered">Bordered</Button>
      <Button variant="light">Light</Button>
      <Button variant="flat">Flat</Button>
      <Button variant="faded">Faded</Button>
      <Button variant="shadow">Shadow</Button>
      <Button variant="ghost">Ghost</Button>

      {/* With icon */}
      <Button startContent={<SearchIcon />}>Search</Button>
      <Button endContent={<ArrowIcon />}>Next</Button>

      {/* Loading state */}
      <Button isLoading>Loading...</Button>

      {/* Disabled */}
      <Button isDisabled>Disabled</Button>
    </>
  );
}
```

### 2. Input Component

```typescript
import { Input } from "@heroui/react";

export function SearchForm() {
  return (
    <>
      {/* Basic input */}
      <Input
        type="text"
        label="Search"
        placeholder="Enter search term"
      />

      {/* With validation */}
      <Input
        type="email"
        label="Email"
        placeholder="you@example.com"
        isRequired
        errorMessage="Please enter a valid email"
      />

      {/* With start/end content */}
      <Input
        type="text"
        label="Price"
        placeholder="0.00"
        startContent={<span>$</span>}
        endContent={<span>SGD</span>}
      />

      {/* Variants */}
      <Input variant="flat" />
      <Input variant="bordered" />
      <Input variant="faded" />
      <Input variant="underlined" />

      {/* Colors */}
      <Input color="primary" />
      <Input color="success" />
      <Input color="danger" />
    </>
  );
}
```

### 3. Card Component

```typescript
import { Card, CardHeader, CardBody, CardFooter, Button } from "@heroui/react";

export function CarCard({ car }: { car: Car }) {
  return (
    <Card className="max-w-md">
      <CardHeader className="flex gap-3">
        <div className="flex flex-col">
          <p className="text-md font-bold">{car.make}</p>
          <p className="text-small text-default-500">{car.model}</p>
        </div>
      </CardHeader>

      <CardBody>
        <p>Year: {car.year}</p>
        <p>Price: ${car.price?.toLocaleString()}</p>
      </CardBody>

      <CardFooter>
        <Button color="primary" variant="flat">
          View Details
        </Button>
      </CardFooter>
    </Card>
  );
}
```

### 4. Modal Component

```typescript
"use client";

import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
} from "@heroui/react";

export function CarDetailsModal({ car }: { car: Car }) {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  return (
    <>
      <Button onPress={onOpen}>View Details</Button>

      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                {car.make} {car.model}
              </ModalHeader>

              <ModalBody>
                <p>Year: {car.year}</p>
                <p>Registration: {car.registrationDate}</p>
                <p>Fuel Type: {car.fuelType}</p>
              </ModalBody>

              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Close
                </Button>
                <Button color="primary" onPress={onClose}>
                  Save
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
}
```

### 5. Table Component

```typescript
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
} from "@heroui/react";

export function CarTable({ cars }: { cars: Car[] }) {
  return (
    <Table aria-label="Car registrations table">
      <TableHeader>
        <TableColumn>MAKE</TableColumn>
        <TableColumn>MODEL</TableColumn>
        <TableColumn>YEAR</TableColumn>
        <TableColumn>PRICE</TableColumn>
      </TableHeader>

      <TableBody>
        {cars.map((car) => (
          <TableRow key={car.id}>
            <TableCell>{car.make}</TableCell>
            <TableCell>{car.model}</TableCell>
            <TableCell>{car.year}</TableCell>
            <TableCell>${car.price?.toLocaleString()}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
```

### 6. Tabs Component

```typescript
import { Tabs, Tab } from "@heroui/react";

export function DataTabs() {
  return (
    <Tabs aria-label="Data options">
      <Tab key="cars" title="Car Registrations">
        <CarRegistrationData />
      </Tab>
      <Tab key="coe" title="COE Results">
        <COEBiddingData />
      </Tab>
      <Tab key="pqp" title="PQP Data">
        <PQPData />
      </Tab>
    </Tabs>
  );
}
```

### 7. Select Component

```typescript
import { Select, SelectItem } from "@heroui/react";

export function CarMakeSelector() {
  const makes = ["Toyota", "Honda", "BMW", "Mercedes"];

  return (
    <Select
      label="Select car make"
      placeholder="Choose a make"
      className="max-w-xs"
    >
      {makes.map((make) => (
        <SelectItem key={make} value={make}>
          {make}
        </SelectItem>
      ))}
    </Select>
  );
}
```

### 8. Dropdown Component

```typescript
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Button,
} from "@heroui/react";

export function ActionsDropdown() {
  return (
    <Dropdown>
      <DropdownTrigger>
        <Button variant="bordered">Actions</Button>
      </DropdownTrigger>

      <DropdownMenu aria-label="Actions">
        <DropdownItem key="view">View</DropdownItem>
        <DropdownItem key="edit">Edit</DropdownItem>
        <DropdownItem key="delete" className="text-danger" color="danger">
          Delete
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
}
```

## Form Handling

### Complete Form Example

```typescript
"use client";

import { useState } from "react";
import { Input, Button, Textarea } from "@heroui/react";
import { createBlogPost } from "@/actions/blog";

export function CreatePostForm() {
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setIsLoading(true);

    const formData = new FormData(e.currentTarget);
    const result = await createBlogPost(formData);

    setIsLoading(false);

    if (result.success) {
      // Handle success
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        name="title"
        label="Post Title"
        placeholder="Enter post title"
        isRequired
      />

      <Textarea
        name="content"
        label="Content"
        placeholder="Enter post content"
        minRows={5}
        isRequired
      />

      <Input
        name="tags"
        label="Tags"
        placeholder="Enter tags separated by commas"
      />

      <Button
        type="submit"
        color="primary"
        isLoading={isLoading}
        className="w-full"
      >
        Create Post
      </Button>
    </form>
  );
}
```

## Theming and Customization

### Theme Provider Setup

```typescript
// app/providers.tsx
"use client";

import { HeroUIProvider } from "@heroui/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <HeroUIProvider>
      {children}
    </HeroUIProvider>
  );
}

// app/layout.tsx
import { Providers } from "./providers";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### Custom Colors via Tailwind

```typescript
// tailwind.config.ts
import { heroui } from "@heroui/react";

export default {
  plugins: [
    heroui({
      themes: {
        light: {
          colors: {
            primary: {
              DEFAULT: "#0070F3",
              foreground: "#FFFFFF",
            },
            focus: "#0070F3",
          },
        },
      },
    }),
  ],
};
```

### Component-Level Customization

```typescript
import { Button } from "@heroui/react";

export function CustomButton() {
  return (
    <Button
      className="bg-gradient-to-r from-blue-500 to-purple-500"
      variant="shadow"
    >
      Custom Styled Button
    </Button>
  );
}
```

## Accessibility

HeroUI components are built on React Aria for accessibility:

```typescript
import { Button } from "@heroui/react";

export function AccessibleButton() {
  return (
    <Button
      aria-label="Close dialog"
      aria-describedby="close-description"
    >
      Close
    </Button>
  );
}
```

## Responsive Design

```typescript
import { Button } from "@heroui/react";

export function ResponsiveButton() {
  return (
    <Button
      size={{
        initial: "sm",    // Mobile
        sm: "md",         // Tablet
        lg: "lg",         // Desktop
      }}
      className="w-full sm:w-auto"
    >
      Responsive Button
    </Button>
  );
}
```

## Common Patterns

### Loading States

```typescript
"use client";

import { useState } from "react";
import { Button } from "@heroui/react";

export function SubmitButton() {
  const [isLoading, setIsLoading] = useState(false);

  async function handleClick() {
    setIsLoading(true);
    await performAction();
    setIsLoading(false);
  }

  return (
    <Button
      onPress={handleClick}
      isLoading={isLoading}
      color="primary"
    >
      {isLoading ? "Processing..." : "Submit"}
    </Button>
  );
}
```

### Controlled Inputs

```typescript
"use client";

import { useState } from "react";
import { Input } from "@heroui/react";

export function ControlledInput() {
  const [value, setValue] = useState("");

  return (
    <Input
      value={value}
      onValueChange={setValue}
      label="Search"
      placeholder="Type to search..."
    />
  );
}
```

## Testing HeroUI Components

```typescript
// __tests__/components/car-card.test.tsx
import { render, screen } from "@testing-library/react";
import { HeroUIProvider } from "@heroui/react";
import CarCard from "../car-card";

function renderWithProvider(component: React.ReactElement) {
  return render(
    <HeroUIProvider>{component}</HeroUIProvider>
  );
}

describe("CarCard", () => {
  it("renders car information", () => {
    const car = { make: "Toyota", model: "Camry", year: 2024 };

    renderWithProvider(<CarCard car={car} />);

    expect(screen.getByText("Toyota")).toBeInTheDocument();
    expect(screen.getByText("Camry")).toBeInTheDocument();
  });
});
```

## Debugging Tips

1. **Missing Provider**: Ensure HeroUIProvider wraps your app
2. **Styling Issues**: Check Tailwind CSS configuration includes HeroUI plugin
3. **Type Errors**: Import types from `@heroui/react`
4. **SSR Issues**: Mark client components with `"use client"`

## References

- HeroUI Documentation: Use MCP tools for component info
- Related files:
  - `apps/web/src/components/` - React components
  - `apps/web/src/app/` - Pages using HeroUI
  - `apps/web/tailwind.config.ts` - Tailwind configuration
  - `apps/web/CLAUDE.md` - Web app documentation

## Best Practices

1. **Use MCP Tools**: Query component info before implementing
2. **Consistent Variants**: Use same variant across similar components
3. **Accessibility**: Always add aria labels for icon-only buttons
4. **Responsive**: Test components on mobile, tablet, desktop
5. **Provider**: Ensure HeroUIProvider at root level
6. **TypeScript**: Leverage TypeScript types for props
7. **Testing**: Wrap tests in HeroUIProvider
8. **Performance**: Use client components only when needed
9. **Size Utility**: Use `size-*` instead of `h-* w-*` for equal dimensions (Tailwind v3.4+)

### Size Utility Convention

When styling HeroUI components with equal height and width, use the `size-*` utility:

```tsx
// ✅ Good - Use size-* for equal dimensions
<Button isIconOnly className="size-10">
  <Icon className="size-4" />
</Button>

// ❌ Avoid - Redundant h-* and w-*
<Button isIconOnly className="h-10 w-10">
  <Icon className="h-4 w-4" />
</Button>
```
