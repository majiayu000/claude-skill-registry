---
name: react-modal
description: Create modal dialogs in the frontend using a custom Modal component built on top of Radix UI Dialog. Use this skill whenever the user asks to create, add, or modify a modal, dialog, popup, or confirmation prompt in the React application.
---

This skill defines the standard approach for creating modal dialogs in this project. All modals MUST use the custom `Modal` component located at `src/components/ui/Modal.tsx`, which wraps Radix UI Dialog primitives.

## Prerequisites

Before creating any modal, ensure `@radix-ui/react-dialog` is installed:

```bash
npm list @radix-ui/react-dialog || npm install @radix-ui/react-dialog
```

## The Modal Component

The base `Modal` component lives at `src/components/ui/Modal.tsx`. If it does not exist yet, create it with the following implementation:

```tsx
import * as React from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { cn } from "../../lib/utils";

const Modal = DialogPrimitive.Root;

const ModalTrigger = DialogPrimitive.Trigger;

const ModalPortal = DialogPrimitive.Portal;

const ModalClose = DialogPrimitive.Close;

const ModalOverlay = React.forwardRef<
  React.ComponentRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/60 backdrop-blur-sm",
      "data-[state=open]:animate-in data-[state=open]:fade-in-0",
      "data-[state=closed]:animate-out data-[state=closed]:fade-out-0",
      className
    )}
    {...props}
  />
));
ModalOverlay.displayName = "ModalOverlay";

const ModalContent = React.forwardRef<
  React.ComponentRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <ModalPortal>
    <ModalOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-1/2 top-1/2 z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2",
        "bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700",
        "p-6 duration-200",
        "data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95 data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]",
        "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%]",
        className
      )}
      {...props}
    >
      {children}
    </DialogPrimitive.Content>
  </ModalPortal>
));
ModalContent.displayName = "ModalContent";

const ModalHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-1.5 mb-4", className)} {...props} />
);
ModalHeader.displayName = "ModalHeader";

const ModalFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn("flex justify-end gap-3 mt-6", className)}
    {...props}
  />
);
ModalFooter.displayName = "ModalFooter";

const ModalTitle = React.forwardRef<
  React.ComponentRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold text-gray-900 dark:text-white", className)}
    {...props}
  />
));
ModalTitle.displayName = "ModalTitle";

const ModalDescription = React.forwardRef<
  React.ComponentRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-gray-600 dark:text-gray-400", className)}
    {...props}
  />
));
ModalDescription.displayName = "ModalDescription";

export {
  Modal,
  ModalPortal,
  ModalOverlay,
  ModalTrigger,
  ModalClose,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalTitle,
  ModalDescription,
};
```

## The ConfirmModal Component

The `ConfirmModal` is a specialized, ready-to-use confirmation dialog that lives at `src/components/ui/ConfirmModal.tsx`. It replaces all uses of `window.confirm()`. If it does not exist yet, create it with the following implementation:

```tsx
import * as React from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalTitle,
  ModalDescription,
  ModalClose,
} from "./Modal";
import { cn } from "../../lib/utils";

type ConfirmVariant = "danger" | "warning" | "default";

interface ConfirmModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onConfirm: () => void | Promise<void>;
  title: string;
  description?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  variant?: ConfirmVariant;
  loading?: boolean;
}

const variantStyles: Record<ConfirmVariant, string> = {
  danger:
    "bg-red-600 hover:bg-red-700 text-white focus:ring-red-500",
  warning:
    "bg-yellow-500 hover:bg-yellow-600 text-white focus:ring-yellow-400",
  default:
    "bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500",
};

export function ConfirmModal({
  open,
  onOpenChange,
  onConfirm,
  title,
  description,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  variant = "default",
  loading = false,
}: ConfirmModalProps) {
  const handleConfirm = async () => {
    await onConfirm();
    onOpenChange(false);
  };

  return (
    <Modal open={open} onOpenChange={onOpenChange}>
      <ModalContent className="max-w-md">
        <ModalHeader>
          <ModalTitle>{title}</ModalTitle>
          {description && (
            <ModalDescription>{description}</ModalDescription>
          )}
        </ModalHeader>
        <ModalFooter>
          <ModalClose asChild>
            <button
              type="button"
              disabled={loading}
              className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 hover:bg-gray-200 text-gray-700 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2"
            >
              {cancelLabel}
            </button>
          </ModalClose>
          <button
            type="button"
            onClick={handleConfirm}
            disabled={loading}
            className={cn(
              "px-4 py-2 rounded-lg text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed",
              variantStyles[variant]
            )}
          >
            {loading ? "Loading..." : confirmLabel}
          </button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
```

## Usage Rules

1. **Always use the `Modal` component** from `src/components/ui/Modal.tsx` for any modal, dialog, or popup — unless the user explicitly requests an exception.
2. **Always use `ConfirmModal`** from `src/components/ui/ConfirmModal.tsx` for any confirmation prompt (e.g., "Are you sure you want to delete?"). Never build confirmation dialogs manually from `Modal` primitives.
3. **Never use raw Radix UI Dialog primitives directly** in page or feature components. Always go through the `Modal` or `ConfirmModal` wrappers.
4. **Never use `window.alert()`, `window.confirm()`, or `window.prompt()`** — use `ConfirmModal` for confirmations, the `Modal` component for other dialogs, and `toast` from `sonner` for alerts.
5. **Never create a custom modal from scratch** with manual overlay/backdrop logic. The Modal component already handles overlay, backdrop blur, animations, focus trapping, and accessibility.

## Usage Patterns

### ConfirmModal — Confirmation prompt (replaces `window.confirm()`)

This is the standard way to ask the user to confirm a destructive or important action:

```tsx
import * as React from "react";
import { ConfirmModal } from "@/components/ui/ConfirmModal";
import { toast } from "sonner";

function DeleteUserButton({ userId }: { userId: string }) {
  const [open, setOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  const handleDelete = async () => {
    setLoading(true);
    try {
      await deleteUser(userId);
      toast.success("User deleted successfully!");
    } catch (error) {
      toast.error("Failed to delete user.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button onClick={() => setOpen(true)}>Delete User</button>
      <ConfirmModal
        open={open}
        onOpenChange={setOpen}
        onConfirm={handleDelete}
        title="Delete User"
        description="Are you sure you want to delete this user? This action cannot be undone."
        confirmLabel="Delete"
        cancelLabel="Cancel"
        variant="danger"
        loading={loading}
      />
    </>
  );
}
```

**ConfirmModal variants:**
- `variant="danger"` — Red button. Use for destructive actions (delete, remove, revoke).
- `variant="warning"` — Yellow button. Use for risky but reversible actions.
- `variant="default"` — Blue button. Use for neutral confirmations.

### General Modal — Custom content dialogs

For modals with custom content (forms, detail views, etc.):

```tsx
import {
  Modal,
  ModalTrigger,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalTitle,
  ModalDescription,
  ModalClose,
} from "@/components/ui/Modal";

function Example() {
  return (
    <Modal>
      <ModalTrigger asChild>
        <button>Open Modal</button>
      </ModalTrigger>
      <ModalContent>
        <ModalHeader>
          <ModalTitle>Modal Title</ModalTitle>
          <ModalDescription>
            A brief description of what this modal does.
          </ModalDescription>
        </ModalHeader>

        {/* Modal body content goes here */}
        <div>Your content here</div>

        <ModalFooter>
          <ModalClose asChild>
            <button>Cancel</button>
          </ModalClose>
          <button>Confirm</button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
```

### Controlled Modal (programmatic open/close)

When you need to control the modal state programmatically (e.g., close after an async action):

```tsx
function ControlledExample() {
  const [open, setOpen] = React.useState(false);

  const handleConfirm = async () => {
    await someAsyncAction();
    setOpen(false);
  };

  return (
    <Modal open={open} onOpenChange={setOpen}>
      <ModalTrigger asChild>
        <button>Open</button>
      </ModalTrigger>
      <ModalContent>
        <ModalHeader>
          <ModalTitle>Confirm Action</ModalTitle>
        </ModalHeader>
        <ModalFooter>
          <ModalClose asChild>
            <button>Cancel</button>
          </ModalClose>
          <button onClick={handleConfirm}>Confirm</button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
```

### When to use which

| Scenario | Component |
|---|---|
| "Are you sure you want to delete?" | `ConfirmModal` |
| "Discard unsaved changes?" | `ConfirmModal` |
| Edit form in a dialog | `Modal` |
| Detail/preview popup | `Modal` |
| Alert/notification message | `toast` from `sonner` (not a modal) |

## Styling

- The Modal component follows the same styling conventions as other `src/components/ui/` components (Tailwind CSS, `cn()` utility, dark mode support via `dark:` variants).
- Override styles by passing `className` to any Modal sub-component.
- The default width is `max-w-lg`. Pass a different `className` to `ModalContent` to change it (e.g., `className="max-w-2xl"` for wider modals).

## Accessibility

The Radix UI Dialog primitive already provides:
- Focus trapping within the modal
- `Escape` key to close
- Click outside (overlay) to close
- Proper `aria-` attributes via `ModalTitle` and `ModalDescription`

Always include a `ModalTitle` for accessibility. If the title should be visually hidden, use `sr-only` class.
