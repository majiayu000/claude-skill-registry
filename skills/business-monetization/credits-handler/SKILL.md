---
name: credits-handler
description: Manage the credit system (allocation, purchasing, usage). Use when adding credit types, configuring pricing, or building credit UI.
---

# Credits Handler

This skill guides you through the entire credit system, from backend configuration to frontend UI implementation.

## 1. Configuration

All credit configuration lives in `src/lib/credits/config.ts`.

### Adding a New Credit Type
1.  **Define the Type**: Add the new type to `creditTypeSchema` enum.
    ```typescript
    export const creditTypeSchema = z.enum([
      "image_generation",
      "video_generation",
      "your_new_credit_type" // Add this
    ]);
    ```

2.  **Configure Pricing & Metadata**: Add an entry to `creditsConfig`.
    ```typescript
    your_new_credit_type: {
      name: "New Credit Name",
      currency: "USD",
      minimumAmount: 10,
      // Option A: Fixed Slabs
      slabs: [
        { from: 1, to: 100, pricePerUnit: 0.10 },
        { from: 101, to: 1000, pricePerUnit: 0.08 },
      ],
      // Option B: Dynamic Calculator (e.g., based on user plan)
      priceCalculator: (amount, userPlan) => {
         // Logic here
         return amount * 0.1;
      }
    }
    ```

3.  **Plan Allocations (Optional)**: Define how many credits are given when subscribing to a plan in `onPlanChangeCredits`.

## 2. UI Implementation: Buying Credits

To let users purchase credits, use the `useBuyCredits` hook. This hook handles price calculation (factoring in plan discounts) and generating checkout URLs.

### Key Hook: `useBuyCredits`
**Location**: `src/lib/credits/useBuyCredits.ts`

#### Usage
```typescript
import useBuyCredits from "@/lib/credits/useBuyCredits";
import { PlanProvider } from "@/lib/plans/getSubscribeUrl";

const { 
  price,            // Calculated total price (number | undefined)
  isLoading,        // Price calculation in progress
  error,            // Error state
  getBuyCreditsUrl  // Function to generate payment URL
} = useBuyCredits(creditType, amount);
```

### Example: Building a Pricing Card
Here is a pattern for creating a credit purchase UI, similar to `src/components/website/website-credits-section.tsx`.

```tsx
"use client";

import { useState } from "react";
import useBuyCredits from "@/lib/credits/useBuyCredits";
import { PlanProvider } from "@/lib/plans/getSubscribeUrl";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

// 1. Define your packages
const PACKAGE = {
  credits: 100,
  name: "Starter Pack",
};

export function BuyCreditsCard({ creditType }: { creditType: "image_generation" }) {
  const [provider] = useState(PlanProvider.STRIPE); // or LEMONSQUEEZY

  // 2. Call the hook
  const { price, isLoading, error, getBuyCreditsUrl } = useBuyCredits(
    creditType,
    PACKAGE.credits
  );

  // 3. Handle Purchase
  const handleBuy = () => {
    const url = getBuyCreditsUrl(provider);
    window.location.href = url;
  };

  // 4. Render UI
  return (
    <div className="border p-4 rounded-lg">
      <h3>{PACKAGE.name}</h3>
      <div className="text-2xl font-bold">
        {isLoading ? (
          <Loader2 className="animate-spin" />
        ) : (
          `$${price?.toFixed(2) || "0.00"}`
        )}
      </div>
      
      <Button 
        onClick={handleBuy}
        disabled={isLoading || !price}
        className="w-full mt-4"
      >
        Buy {PACKAGE.credits} Credits
      </Button>
      
      {error && <p className="text-red-500 text-sm">{error.message}</p>}
    </div>
  );
}
```

## 3. UI Implementation: Displaying Credits

To show the user's current balance, use the `useCredits` hook.

### Key Hook: `useCredits`
**Location**: `src/lib/users/useCredits.ts`

#### Return Data Structure
```typescript
const { 
  credits,    // Record<string, number> | undefined
              // e.g. { "image_generation": 100, "video_generation": 50 }
  isLoading,  // boolean
  error,      // any
  mutate      // SWR mutate function to refresh data
} = useCredits();
```

#### Usage Example
```tsx
import useCredits from "@/lib/users/useCredits";

export function CreditBalance() {
  const { credits, isLoading } = useCredits();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      Image Credits: {credits?.image_generation || 0}
    </div>
  );
}
```

## 4. Core Operations (Backend)

These functions are used in API routes and webhooks.

### Allocating Credits (e.g., on Plan Change)
Use `allocatePlanCredits` to give users credits when they subscribe/upgrade.
- **File**: `src/lib/credits/allocatePlanCredits.ts`
- **Input**: `userId`, `planId`, `paymentId` (for idempotency).
- **Behavior**: Checks `onPlanChangeCredits` config and adds credits if applicable.

### Adding/Deducting Credits
To manually manipulate balances, use helpers from `src/lib/credits/recalculate.ts` (e.g., `addCredits`, `deductCredits`).
*Note: Always ensure you have a unique `paymentId` or transaction reference when adding credits to prevent duplicates.*

## 5. Checking Balance (Backend/Common)

Use `canDeductCredits` before performing an action.

```typescript
import { canDeductCredits } from "@/lib/credits/credits";

// Check if user has enough credits
const hasBalance = canDeductCredits(
  "image_generation", 
  1, 
  user // Must contain { credits: { ... } }
);

if (!hasBalance) {
  throw new Error("Insufficient credits");
}
```

## 6. Reference
For deep dives into database schema and architecture, see [reference.md](reference.md).
