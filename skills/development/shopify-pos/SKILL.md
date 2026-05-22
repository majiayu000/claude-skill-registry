---
name: shopify-pos
description: Guide for building Shopify POS (Point of Sale) UI extensions that integrate custom functionality into Shopify's retail interface. Use this skill when the user needs to create POS tiles, modals, blocks, or actions for the smart grid, cart, customer details, order details, product details, or post-purchase screens. Covers targets, components, APIs, and development workflow for POS app extensions.
---

# Shopify POS UI Extensions (2026)

Build custom extensions that integrate directly into Shopify's Point of Sale interface on iOS and Android devices.

## Official References

- [POS UI Extensions API](https://shopify.dev/docs/api/pos-ui-extensions/latest)
- [Building for POS](https://shopify.dev/docs/apps/build/pos)
- [POS Extension Targets](https://shopify.dev/docs/api/pos-ui-extensions/latest/targets)

## Prerequisites

- Shopify CLI (latest)
- Shopify App with POS enabled
- Development store with POS Pro subscription

**Enable POS embedding**: In Partner Dashboard > App > Configuration, set "Embed app in Shopify POS" to **True**.

## Extension Architecture

POS UI extensions have three interconnected parts:

1. **Targets** - Where your extension appears (tile, modal, block, menu item)
2. **Target APIs** - Data and functionality access (Cart, Customer, Session, etc.)
3. **Components** - Native UI building blocks (Button, Screen, List, etc.)

## Creating a POS Extension

```bash
shopify app generate extension --template pos_ui --name "my-pos-extension"
```

### Configuration (shopify.extension.toml)

```toml
api_version = "2025-10"

[[extensions]]
type = "ui_extension"
name = "my-pos-extension"
handle = "my-pos-extension"

[[extensions.targeting]]
module = "./src/Tile.tsx"
target = "pos.home.tile.render"

[[extensions.targeting]]
module = "./src/Modal.tsx"
target = "pos.home.modal.render"
```

## Targets Reference

See [references/targets.md](references/targets.md) for all available targets.

### Target Types

| Type | Purpose | Example |
|------|---------|---------|
| **Tile** | Smart grid button on home screen | `pos.home.tile.render` |
| **Modal** | Full-screen interface | `pos.home.modal.render` |
| **Block** | Inline content section | `pos.product-details.block.render` |
| **Menu Item** | Action menu button | `pos.customer-details.action.menu-item.render` |

### Common Target Patterns

**Home Screen (Smart Grid)**
```tsx
// Tile.tsx - Entry point on POS home
import { Tile, reactExtension } from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.home.tile.render', () => <TileComponent />);

function TileComponent() {
  return <Tile title="My App" subtitle="Tap to open" enabled={true} />;
}
```

**Modal (Full Screen)**
```tsx
// Modal.tsx - Launches when tile is tapped
import { Screen, Navigator, Text, Button, useApi, reactExtension } from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.home.modal.render', () => <ModalComponent />);

function ModalComponent() {
  const api = useApi<'pos.home.modal.render'>();

  return (
    <Navigator>
      <Screen name="Main" title="My Extension">
        <Text>Welcome to my POS extension</Text>
        <Button title="Close" onPress={() => api.navigation.dismiss()} />
      </Screen>
    </Navigator>
  );
}
```

**Block (Inline Content)**
```tsx
// ProductBlock.tsx
import { Section, Text, reactExtension, useApi } from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.product-details.block.render', () => <ProductBlock />);

function ProductBlock() {
  const { product } = useApi<'pos.product-details.block.render'>();
  const productData = product.getProduct();

  return (
    <Section title="Custom Info">
      <Text>Product ID: {productData?.id}</Text>
    </Section>
  );
}
```

## Components Reference

See [references/components.md](references/components.md) for all available components.

### Key Components

**Layout & Structure**
- `Screen` - Navigation screen with title, loading state, actions
- `Navigator` - Screen navigation container
- `ScrollView` - Scrollable content container
- `Section` - Card-like grouping container
- `Stack` - Horizontal/vertical layout
- `List` - Structured data rows

**Actions**
- `Button` - Tappable action button
- `Tile` - Smart grid tile (home screen only)
- `Selectable` - Make components tappable

**Forms**
- `TextField`, `TextArea` - Text input
- `NumberField` - Numeric input
- `EmailField` - Email with validation
- `DateField`, `DatePicker` - Date selection
- `RadioButtonList` - Single selection
- `Stepper` - Increment/decrement control
- `PinPad` - Secure PIN entry

**Feedback**
- `Banner` - Important messages
- `Dialog` - Confirmation prompts
- `Badge` - Status indicators

**Media**
- `Icon` - POS icon catalog
- `Image` - Visual content
- `CameraScanner` - Barcode/QR scanning

## APIs Reference

See [references/apis.md](references/apis.md) for all available APIs.

### Accessing APIs

```tsx
import { useApi } from '@shopify/ui-extensions-react/point-of-sale';

function MyComponent() {
  const api = useApi<'pos.home.modal.render'>();

  // Access various APIs based on target
  const { cart, customer, session, navigation, toast } = api;
}
```

### Core APIs

**Cart API** - Modify cart contents
```tsx
const { cart } = useApi<'pos.home.modal.render'>();

// Add item
await cart.addLineItem({ variantId: 'gid://shopify/ProductVariant/123', quantity: 1 });

// Apply discount
await cart.applyCartDiscount({ type: 'percentage', value: 10, title: '10% Off' });

// Get cart
const currentCart = cart.getCart();
```

**Session API** - Authentication and session data
```tsx
const { session } = useApi<'pos.home.modal.render'>();

// Get session token for backend auth
const token = await session.getSessionToken();

// Get current staff member
const staff = session.currentSession;
```

**Customer API** - Customer data access
```tsx
const { customer } = useApi<'pos.customer-details.block.render'>();
const customerData = customer.getCustomer();
```

**Toast API** - Show notifications
```tsx
const { toast } = useApi<'pos.home.modal.render'>();
toast.show('Item added successfully');
```

**Navigation API** - Screen navigation
```tsx
const { navigation } = useApi<'pos.home.modal.render'>();
navigation.dismiss();  // Close modal
navigation.navigate('ScreenName');  // Navigate to screen
```

**Scanner API** - Barcode scanning
```tsx
const { scanner } = useApi<'pos.home.modal.render'>();
const result = await scanner.scanBarcode();
```

**Print API** - Receipt printing
```tsx
const { print } = useApi<'pos.home.modal.render'>();
await print.printDocument(documentContent);
```

### Direct GraphQL API Access

Available for extensions targeting `2025-07` or later (requires POS 10.6.0+).

```tsx
const response = await fetch('shopify:admin/api/graphql.json', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: `
      query GetProduct($id: ID!) {
        product(id: $id) {
          title
          variants(first: 10) {
            nodes { id title inventoryQuantity }
          }
        }
      }
    `,
    variables: { id: 'gid://shopify/Product/123' }
  })
});
```

Declare required scopes in `shopify.app.toml`:
```toml
[access_scopes]
scopes = "read_products,write_products,read_customers"
```

## Development Workflow

### Local Development

```bash
shopify app dev
```

Open the Shopify POS app on your device and connect to the development store.

### Testing

1. Install app on development store
2. Open Shopify POS app
3. Navigate to smart grid (home) to see tiles
4. Tap tiles to test modals
5. Navigate to relevant screens (products, customers, orders) for block/action targets

### Deployment

```bash
shopify app deploy
```

## Best Practices

1. **Performance First** - Extensions run in critical merchant workflows; minimize API calls and computations
2. **Offline Consideration** - Use Storage API for data that should persist offline
3. **Native Feel** - Use provided components to match POS design system
4. **Error Handling** - Always handle API failures gracefully with user feedback
5. **Loading States** - Show loading indicators during async operations

### Storage API for Offline Data

```tsx
const { storage } = useApi<'pos.home.modal.render'>();

// Store data
await storage.setItem('key', JSON.stringify(data));

// Retrieve data
const stored = await storage.getItem('key');
const data = stored ? JSON.parse(stored) : null;
```

## Complete Example: Loyalty Points Extension

```tsx
// Tile.tsx
import { Tile, reactExtension } from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.home.tile.render', () => (
  <Tile title="Loyalty Points" subtitle="Check & redeem" enabled={true} />
));

// Modal.tsx
import {
  Screen, Navigator, Text, Button, Section, Stack,
  useApi, reactExtension
} from '@shopify/ui-extensions-react/point-of-sale';
import { useState, useEffect } from 'react';

export default reactExtension('pos.home.modal.render', () => <LoyaltyModal />);

function LoyaltyModal() {
  const { cart, session, navigation, toast } = useApi<'pos.home.modal.render'>();
  const [points, setPoints] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPoints();
  }, []);

  async function fetchPoints() {
    const token = await session.getSessionToken();
    const currentCart = cart.getCart();
    const customerId = currentCart?.customer?.id;

    if (!customerId) {
      setLoading(false);
      return;
    }

    const res = await fetch('https://your-backend.com/api/points', {
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ customerId })
    });
    const data = await res.json();
    setPoints(data.points);
    setLoading(false);
  }

  async function redeemPoints() {
    await cart.applyCartDiscount({
      type: 'fixedAmount',
      value: points / 100,
      title: 'Loyalty Redemption'
    });
    toast.show('Points redeemed!');
    navigation.dismiss();
  }

  return (
    <Navigator>
      <Screen name="Main" title="Loyalty Points" isLoading={loading}>
        <Section title="Current Balance">
          <Stack direction="vertical" spacing={2}>
            <Text variant="headingLarge">{points} points</Text>
            <Text>Worth ${(points / 100).toFixed(2)}</Text>
          </Stack>
        </Section>
        <Button
          title="Redeem All Points"
          type="primary"
          onPress={redeemPoints}
          disabled={points === 0}
        />
        <Button title="Close" onPress={() => navigation.dismiss()} />
      </Screen>
    </Navigator>
  );
}
```
