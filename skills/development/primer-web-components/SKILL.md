---
name: primer-web-components
description: Build checkout and payment experiences using Primer's web components. Use this skill when implementing payment flows, checkout pages, card forms, or integrating Primer SDK into React, Next.js, or vanilla JavaScript applications. Covers component usage, React integration patterns, stable object references, event handling, SSR support, and CSS theming.
---

# Primer Web Components

## Overview

This skill provides comprehensive guidance for building checkout and payment experiences using Primer's web component library (`@primer-io/primer-js`). Primer components are framework-agnostic custom elements that work with React, Next.js, Vue, Svelte, or vanilla JavaScript.

Use this skill when:

- Implementing checkout pages or payment flows
- Integrating Primer payment methods (cards, PayPal, BLIK, Apple Pay, Google Pay, etc.)
- Building custom card forms with validation
- Working with React and need to handle web component integration properly
- Customizing payment UI with themes and CSS custom properties
- Implementing vault for saved payment methods
- Handling payment lifecycle events and callbacks

## 🚨 Breaking Changes in v0.7.0

**Critical API Changes:**

Starting in v0.7.0, the callback and event APIs have been updated for clearer separation of success and failure handling:

- **Callbacks**: `onPaymentComplete` replaced with `onPaymentSuccess` and `onPaymentFailure`
- **State Fields**: `error` → `primerJsError`, `failure` → `paymentFailure`
- **Event Names**: `primer:payment-methods-updated` → use `primer:methods-update`

**New in v0.7.0:**

- Payment lifecycle events: `primer:payment-start`, `primer:payment-success`, `primer:payment-failure`
- Vault events: `primer:vault:methods-update`
- Vault callback: `onVaultedMethodsUpdate`
- PII-filtered payment data in success payloads

All examples in this skill use the v0.7.0+ API. If using older SDK versions, refer to legacy documentation.

## Quick Start Guide

### Installation

```bash
npm install @primer-io/primer-js
```

### Basic HTML Setup

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Primer Checkout</title>
  </head>
  <body>
    <primer-checkout client-token="your-client-token"></primer-checkout>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

### Vanilla JavaScript Initialization

```typescript
import { loadPrimer } from '@primer-io/primer-js';
import { fetchClientToken } from './fetchClientToken';

(async function () {
  await loadPrimer();

  const checkout = document.querySelector('primer-checkout')!;
  const response = await fetchClientToken('order-id');

  if (response.success) {
    checkout.setAttribute('client-token', response.clientToken);
  }

  // Handle payment success and failure
  checkout.addEventListener('primer:ready', (event) => {
    const primer = event.detail;

    primer.onPaymentSuccess = ({ paymentSummary, paymentMethodType }) => {
      console.log('✅ Payment successful!', paymentSummary.id);
      window.location.href = `/confirmation?orderId=${paymentSummary.orderId}`;
    };

    primer.onPaymentFailure = ({ error }) => {
      console.error('❌ Payment failed:', error.message);
      // Show error to user
    };
  });
})();
```

### React 19 Setup (Recommended)

**TypeScript Configuration:**

```typescript
import type { CheckoutElement } from '@primer-io/primer-js';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'primer-checkout': CheckoutElement;
    }
  }
}
```

**Component:**

```typescript
import { useEffect } from 'react';
import { loadPrimer } from '@primer-io/primer-js';

// ✅ Define options outside component for stable reference
const SDK_OPTIONS = {
  locale: 'en-GB',
  enabledPaymentMethods: [PaymentMethodType.PAYMENT_CARD],
};

function CheckoutPage({ clientToken }: { clientToken: string }) {
  useEffect(() => {
    loadPrimer();
  }, []);

  return (
    <primer-checkout client-token={clientToken} options={SDK_OPTIONS} />
  );
}
```

## Component Architecture

### Core Component Hierarchy

```
primer-checkout (root)
├── primer-main (layout container)
│   ├── slot="payments" (payment method selection)
│   ├── slot="checkout-complete" (success state)
│   └── slot="checkout-failure" (error state)
├── primer-payment-method (individual payment type)
├── primer-payment-method-container (declarative filtering)
├── primer-billing-address (billing information, SDK Core only)
├── primer-error-message-container (payment failure display)
└── primer-card-form (card payment inputs)
    ├── primer-input-card-number
    ├── primer-input-card-expiry
    ├── primer-input-cvv
    ├── primer-input-card-holder-name
    ├── primer-card-form-submit
    └── Custom fields using base components:
        ├── primer-input-wrapper
        ├── primer-input-label
        └── primer-input
```

## SDK Modes: Core vs Legacy

### SDK Core (Default since v0.4.0)

The new payment engine with enhanced features. **This is the default and recommended for new integrations.**

```javascript
// SDK Core is enabled by default
checkout.options = {
  sdkCore: true, // Default, no need to specify
};
```

**Currently Supported Payment Methods:**

- `PAYMENT_CARD` - Full card payment forms
- `PAYPAL` - PayPal button integration
- `ADYEN_BLIK` - Polish payment method (OTP verification)

New payment methods are added regularly. Check release notes for updates.

**Benefits:**

- Modern payment processing engine
- Enhanced performance and reliability
- New payment methods support
- Better error handling and diagnostics

### Legacy SDK

Enable with `sdkCore: false`. Provides access to 50+ payment methods via Web Headless API.

```javascript
checkout.options = {
  sdkCore: false, // Opt into legacy SDK
};
```

**When to use:**

- Need payment methods not yet in SDK Core
- Existing integration using legacy patterns
- Require specific processor-specific methods

**Important:** Payment method availability depends on:

1. Primer Dashboard configuration
2. Payment processor Web Headless support
3. Regional availability

Not all payment methods support Web Headless. Check the [Primer Payment Methods catalog](https://primer.io/docs/connections/payment-methods/available-payment-methods) for "Web Headless" column.

## SDK Options Reference

### Core Options

Configure SDK behavior through the `options` property:

```javascript
checkout.options = {
  // Core configuration
  sdkCore: true, // Default: true (SDK Core enabled)
  locale: 'en-US', // Force UI locale
  merchantDomain: 'merchant.example.com', // For Apple Pay validation
  disabledPayments: false, // Disable all payment methods
  enabledPaymentMethods: [PaymentMethodType.PAYMENT_CARD, PaymentMethodType.PAYPAL],
};
```

**Core Options:**

| Option                  | Type                  | Default                            | Description                          |
| ----------------------- | --------------------- | ---------------------------------- | ------------------------------------ |
| `sdkCore`               | `boolean`             | `true`                             | Enable SDK Core engine               |
| `locale`                | `string`              | Browser's locale                   | Force UI locale (e.g., "en-GB")      |
| `merchantDomain`        | `string`              | `window.location.hostname`         | Domain for Apple Pay validation      |
| `disabledPayments`      | `boolean`             | `false`                            | Disable all payment methods globally |
| `enabledPaymentMethods` | `PaymentMethodType[]` | `[PaymentMethodType.PAYMENT_CARD]` | Which payment methods to display     |

### Card Options

Configure card payment form behavior:

```javascript
checkout.options = {
  card: {
    cardholderName: {
      required: true, // Whether cardholder name is required
      visible: true, // Whether cardholder name field is visible
    },
  },
};
```

**Card Options:**

| Option                         | Type      | Default | Description                |
| ------------------------------ | --------- | ------- | -------------------------- |
| `card.cardholderName.required` | `boolean` | `false` | Require cardholder name    |
| `card.cardholderName.visible`  | `boolean` | `true`  | Show cardholder name field |

### Apple Pay Options

Configure Apple Pay button appearance and data collection:

```javascript
checkout.options = {
  applePay: {
    buttonType: 'buy', // 'plain' | 'buy' | 'set-up' | 'donate' | 'check-out' | 'book' | 'subscribe'
    buttonStyle: 'black', // 'white' | 'white-outline' | 'black'
    billingOptions: {
      requiredBillingContactFields: ['postalAddress', 'emailAddress'],
    },
    shippingOptions: {
      requiredShippingContactFields: ['postalAddress', 'name'],
      requireShippingMethod: false,
    },
  },
};
```

### Google Pay Options

Configure Google Pay button appearance and data collection:

```javascript
checkout.options = {
  googlePay: {
    buttonType: 'long', // 'long' | 'short' | 'book' | 'buy' | 'checkout' | 'donate' | 'order' | 'pay' | 'plain' | 'subscribe'
    buttonColor: 'black', // 'default' | 'black' | 'white'
    buttonSizeMode: 'fill', // 'fill' | 'static'
    captureBillingAddress: true,
    emailRequired: false,
    requireShippingMethod: false,
  },
};
```

### Klarna Options

Configure Klarna payment behavior:

```javascript
checkout.options = {
  klarna: {
    paymentFlow: 'DEFAULT', // 'DEFAULT' | 'PREFER_VAULT'
    allowedPaymentCategories: ['pay_now', 'pay_later', 'pay_over_time'],
    buttonOptions: {
      text: 'Pay with Klarna',
    },
  },
};
```

### Vault Options

Configure payment method vaulting (saving for future use):

```javascript
checkout.options = {
  vault: {
    enabled: true, // Enable vaulting
    showEmptyState: true, // Show message when no vaulted methods exist
  },
};
```

### Stripe Options

Configure Stripe-specific payment options:

```javascript
checkout.options = {
  stripe: {
    mandateData: {
      fullMandateText: 'By providing your payment information...',
      merchantName: 'Your Business Name',
    },
    publishableKey: 'pk_test_...',
  },
};
```

### Submit Button Options

Configure submit button behavior:

```javascript
checkout.options = {
  submitButton: {
    amountVisible: true, // Show amount on button (e.g., "Pay $12.34")
    useBuiltInButton: true, // Default: true, set false for external buttons
  },
};
```

**Using External Submit Buttons:**

```javascript
// Hide built-in button
checkout.options = {
  submitButton: {
    useBuiltInButton: false,
  },
};

// Dispatch event to submit from external button
document.getElementById('my-button').addEventListener('click', () => {
  document.dispatchEvent(
    new CustomEvent('primer:card-submit', {
      bubbles: true,
      composed: true,
      detail: { source: 'external-button' },
    }),
  );
});
```

## PayPal Integration

PayPal integration requires SDK Core (`sdkCore: true`, which is the default).

### Basic Configuration

```javascript
import { PaymentMethodType } from '@primer-io/primer-js';

checkout.options = {
  sdkCore: true, // Default, required for PayPal
  enabledPaymentMethods: [PaymentMethodType.PAYMENT_CARD, PaymentMethodType.PAYPAL],
  paypal: {
    style: {
      layout: 'vertical',
      color: 'gold',
      shape: 'rect',
      height: 45,
      label: 'checkout',
    },
  },
};
```

### Button Styling Options

Customize PayPal button appearance:

| Option            | Type                                                                   | Default      | Description                           |
| ----------------- | ---------------------------------------------------------------------- | ------------ | ------------------------------------- |
| `layout`          | `'vertical'` \| `'horizontal'`                                         | `'vertical'` | Button layout orientation             |
| `color`           | `'gold'` \| `'blue'` \| `'silver'` \| `'white'` \| `'black'`           | `'gold'`     | Button color theme                    |
| `shape`           | `'rect'` \| `'pill'`                                                   | `'rect'`     | Button border shape                   |
| `height`          | `number` (25-55)                                                       | `40`         | Button height in pixels               |
| `label`           | `'paypal'` \| `'checkout'` \| `'buynow'` \| `'pay'` \| `'installment'` | `'paypal'`   | Button label text                     |
| `tagline`         | `boolean`                                                              | `false`      | Show tagline (horizontal layout only) |
| `borderRadius`    | `number` (0-55)                                                        | `4`          | Button corner radius in pixels        |
| `disableMaxWidth` | `boolean`                                                              | `false`      | Disable maximum width constraint      |

**Styling Examples:**

```javascript
// Horizontal blue pill buttons
paypal: {
  style: {
    layout: 'horizontal',
    color: 'blue',
    shape: 'pill',
    height: 45,
    label: 'checkout',
    tagline: false,
  }
}

// Vertical silver buttons with custom border radius
paypal: {
  style: {
    layout: 'vertical',
    color: 'silver',
    shape: 'rect',
    height: 50,
    borderRadius: 8,
    disableMaxWidth: true,
  }
}
```

### Funding Source Control

Control which PayPal funding sources are available:

```javascript
paypal: {
  disableFunding: ['credit', 'paylater', 'card'], // Hide these options
  enableFunding: ['venmo'], // Explicitly enable Venmo
}
```

**Available Funding Sources:**

- `card` - Guest card payments (credit/debit without PayPal account)
- `credit` - PayPal Credit (US, UK)
- `paylater` - PayPal Pay Later
- `venmo` - Venmo (US)

**Funding Control Examples:**

```javascript
// Only PayPal balance and bank account
paypal: {
  disableFunding: ['card', 'credit', 'paylater', 'venmo'],
}

// PayPal with Venmo only
paypal: {
  disableFunding: ['card', 'credit', 'paylater'],
  enableFunding: ['venmo'],
}
```

**Important:** `disableFunding` takes precedence over `enableFunding`. If a source appears in both arrays, it will be disabled.

### PayPal Vaulting

Enable vaulting to allow customers to save their PayPal account:

```javascript
paypal: {
  vault: true, // Enable vaulting in SDK
}
```

**Requirements:**

Vaulting requires **both** SDK configuration and server-side setup:

1. **SDK Configuration**: Set `vault: true` in PayPal options
2. **Client Session**: Configure `vaultOnSuccess: true` in your client session creation request

**Legacy SDK**: For `sdkCore: false`, use:

```javascript
paypal: {
  paymentFlow: 'PREFER_VAULT',
}
```

### Complete PayPal Example

```javascript
checkout.options = {
  sdkCore: true,
  enabledPaymentMethods: [PaymentMethodType.PAYMENT_CARD, PaymentMethodType.PAYPAL],
  paypal: {
    // Button styling
    style: {
      layout: 'vertical',
      color: 'gold',
      shape: 'pill',
      height: 45,
      label: 'checkout',
      borderRadius: 6,
    },

    // Funding control
    disableFunding: ['credit', 'card'],
    enableFunding: ['venmo'],

    // Vaulting
    vault: true,
  },
};
```

## Events & Callbacks

Primer Checkout uses an event-driven architecture with custom DOM events and callbacks. Events bubble up through the DOM, and callbacks provide direct handling of payment lifecycle.

### Core Events

#### `primer:ready`

Dispatched when the Primer SDK is fully initialized and ready for use.

**Event Detail:** Contains the PrimerJS instance with methods and callbacks.

**Usage:**

```javascript
const checkout = document.querySelector('primer-checkout');

checkout.addEventListener('primer:ready', (event) => {
  const primer = event.detail;
  console.log('✅ Primer SDK ready');

  // Configure payment success handler
  primer.onPaymentSuccess = ({ paymentSummary, paymentMethodType }) => {
    console.log('✅ Payment successful', paymentSummary.id);
    console.log('💳 Method:', paymentMethodType);

    // Access available payment data (PII-filtered)
    if (paymentSummary.paymentMethodData?.last4Digits) {
      console.log('Last 4:', paymentSummary.paymentMethodData.last4Digits);
    }

    // Redirect to confirmation page
    window.location.href = `/order/confirmation?id=${paymentSummary.orderId}`;
  };

  // Configure payment failure handler
  primer.onPaymentFailure = ({ error, paymentMethodType }) => {
    console.error('❌ Payment failed', error.message);
    console.error('Error code:', error.code);

    // Log diagnostics ID for support
    if (error.diagnosticsId) {
      console.error('Diagnostics ID:', error.diagnosticsId);
    }

    // Show error message and allow retry
    showErrorMessage(error.message);
  };

  // Configure vaulted methods update handler
  primer.onVaultedMethodsUpdate = ({ vaultedPayments }) => {
    console.log('Vault updated:', vaultedPayments.size(), 'methods');
    updateVaultUI(vaultedPayments.toArray());
  };
});
```

#### `primer:state-change`

Dispatched whenever the checkout state changes (processing, success, error, etc.).

**Event Detail:** Contains `isProcessing`, `isSuccessful`, `isLoading`, `primerJsError`, `paymentFailure`.

**Usage:**

```javascript
checkout.addEventListener('primer:state-change', (event) => {
  const { isProcessing, isSuccessful, primerJsError, paymentFailure } = event.detail;

  if (isProcessing) {
    console.log('⏳ Processing payment...');
    showLoadingSpinner();
  } else if (isSuccessful) {
    console.log('✅ Payment successful!');
    hideLoadingSpinner();
  } else if (primerJsError || paymentFailure) {
    const errorMessage = primerJsError?.message || paymentFailure?.message || 'An error occurred';
    console.error('❌ Payment failed:', errorMessage);

    // Log error code for debugging
    if (paymentFailure?.code) {
      console.error('Error code:', paymentFailure.code);
    }

    hideLoadingSpinner();
    showErrorMessage(errorMessage);
  }
});
```

**State Field Changes in v0.7.0:**

- `error` → `primerJsError` (SDK-level errors)
- `failure` → `paymentFailure` (payment-level failures)

#### `primer:methods-update`

Dispatched when available payment methods are loaded and ready.

**Event Detail:** Contains `InitializedPayments` instance with `toArray()` and `size()` methods.

**Usage:**

```javascript
checkout.addEventListener('primer:methods-update', (event) => {
  const paymentMethods = event.detail.toArray();

  console.log('Available payment methods:', paymentMethods);
  console.log('Total methods:', paymentMethods.length);

  // Access individual method details
  paymentMethods.forEach((method) => {
    console.log('Method type:', method.type);
  });
});
```

**Tip:** For most layout and filtering use cases, the `primer-payment-method-container` component provides a simpler declarative approach without requiring event listeners.

### Payment Lifecycle Events (New in v0.7.0)

Payment lifecycle events provide granular tracking of payment processing stages with detailed data payloads.

#### `primer:payment-start`

Dispatched when payment processing begins, immediately after the user initiates a payment.

**Event Detail:** `undefined` (use as trigger signal only)

**Usage:**

```javascript
document.addEventListener('primer:payment-start', () => {
  console.log('💳 Payment processing started');

  // Show loading indicators
  showPaymentLoadingSpinner();

  // Disable form inputs to prevent duplicate submissions
  disableFormInputs();

  // Track payment initiation
  analytics.track('Payment Started');
});
```

#### `primer:payment-success`

Dispatched when a payment completes successfully.

**Event Detail:**

```typescript
{
  paymentSummary: PaymentSummary; // PII-filtered payment data
  paymentMethodType: string; // e.g., 'PAYMENT_CARD', 'PAYPAL'
  timestamp: number; // Unix timestamp of success
}
```

**PaymentSummary Structure:**

Available fields (PII-filtered):

- `id`: Payment ID
- `orderId`: Merchant order ID
- `paymentMethodType`: Type of payment method used
- `paymentMethodData`: Object containing non-sensitive card data
  - `last4Digits`: Last 4 digits of card number (if applicable)
  - `network`: Card network (Visa, Mastercard, etc.)
  - `paymentMethodType`: Payment method type

Filtered fields (not available):

- `cardholderName`: Filtered for PII protection

**Usage:**

```javascript
document.addEventListener('primer:payment-success', (event) => {
  const { paymentSummary, paymentMethodType, timestamp } = event.detail;

  console.log('✅ Payment successful!');
  console.log('Payment ID:', paymentSummary.id);
  console.log('Order ID:', paymentSummary.orderId);
  console.log('Method:', paymentMethodType);
  console.log('Timestamp:', new Date(timestamp));

  // Access available payment method data
  if (paymentSummary.paymentMethodData?.last4Digits) {
    console.log('Last 4 digits:', paymentSummary.paymentMethodData.last4Digits);
    console.log('Network:', paymentSummary.paymentMethodData.network);
  }

  // Track successful payment in analytics
  analytics.track('Payment Successful', {
    paymentId: paymentSummary.id,
    orderId: paymentSummary.orderId,
    method: paymentMethodType,
    last4: paymentSummary.paymentMethodData?.last4Digits,
  });

  // Redirect to confirmation page
  window.location.href = `/order/confirmation?id=${paymentSummary.orderId}`;
});
```

**Important:** The `PaymentSummary` object filters sensitive information like cardholder names. Only use the provided non-sensitive fields for display and analytics.

#### `primer:payment-failure`

Dispatched when a payment fails or encounters an error.

**Event Detail:**

```typescript
{
  error: {
    code: string;           // Error code (e.g., 'CARD_DECLINED')
    message: string;        // User-friendly error message
    diagnosticsId?: string; // Optional diagnostics ID for support
    data?: any;            // Optional additional error data
  };
  paymentSummary?: PaymentSummary;  // Optional, may be undefined
  paymentMethodType: string;
  timestamp: number;
}
```

**Usage:**

```javascript
document.addEventListener('primer:payment-failure', (event) => {
  const { error, paymentSummary, paymentMethodType, timestamp } = event.detail;

  console.error('❌ Payment failed');
  console.error('Error code:', error.code);
  console.error('Error message:', error.message);

  if (error.diagnosticsId) {
    console.error('Diagnostics ID:', error.diagnosticsId);
  }

  // Display error message to user
  showErrorMessage(error.message);

  // Track payment failure in analytics
  analytics.track('Payment Failed', {
    errorCode: error.code,
    errorMessage: error.message,
    diagnosticsId: error.diagnosticsId,
    method: paymentMethodType,
    timestamp: new Date(timestamp),
  });

  // Send to error tracking service
  if (error.diagnosticsId) {
    errorTracker.capturePaymentFailure({
      diagnosticsId: error.diagnosticsId,
      code: error.code,
      paymentMethodType,
    });
  }
});
```

### Vault Events (New in v0.7.0)

#### `primer:vault:methods-update`

Dispatched when vaulted payment methods are loaded, updated, or when the vault state changes.

**Event Detail:**

```typescript
{
  vaultedPayments: InitializedVaultedPayments; // Vault API instance
  timestamp: number; // Unix timestamp
}
```

**InitializedVaultedPayments API:**

- `toArray()`: Returns array of `VaultedPaymentMethodSummary` objects
- `get(id: string)`: Gets a specific vaulted payment method by ID
- `size()`: Returns the number of saved payment methods

**VaultedPaymentMethodSummary Structure:**

- `id`: Unique identifier for the vaulted payment method
- `analyticsId`: Analytics tracking identifier
- `paymentMethodType`: Type of payment method (e.g., 'PAYMENT_CARD', 'ADYEN_STRIPE_ACH')
- `paymentInstrumentType`: Instrument type
- `paymentInstrumentData`: Object with PII-filtered payment instrument details
  - `last4Digits`: Last 4 digits of card (cards only)
  - `network`: Card network like VISA, MASTERCARD (cards only)
  - `accountNumberLastFourDigits`: Last 4 of account number (ACH only)
  - `bankName`: Bank name (ACH only)
  - `accountType`: CHECKING or SAVINGS (ACH only)
  - `email`: Email address (wallet methods like PayPal)
- `userDescription`: Optional user-provided description

**Important:** Sensitive fields like cardholder names, expiration dates, and full account numbers are filtered out for security.

**Usage:**

```javascript
document.addEventListener('primer:vault:methods-update', (event) => {
  const { vaultedPayments, timestamp } = event.detail;

  console.log('💳 Vault methods updated');
  console.log('Total saved methods:', vaultedPayments.size());

  // Get all saved payment methods
  const methods = vaultedPayments.toArray();

  methods.forEach((method) => {
    console.log('Method ID:', method.id);
    console.log('Type:', method.paymentMethodType);

    if (method.paymentInstrumentData) {
      console.log('Last 4:', method.paymentInstrumentData.last4Digits);
      console.log('Network:', method.paymentInstrumentData.network);
    }
  });

  // Update UI with saved methods
  updateVaultDisplay(methods);

  // Track vault updates in analytics
  analytics.track('Vault Methods Updated', {
    count: methods.length,
    timestamp,
  });
});
```

### Card Events

Card events are specific to card payment form interactions and validation.

#### `primer:card-success`

Dispatched when a card form is successfully validated and submitted.

**Event Detail:** Contains `result` object with payment submission data.

**Usage:**

```javascript
checkout.addEventListener('primer:card-success', (event) => {
  const result = event.detail.result;
  console.log('✅ Card form submitted successfully', result);

  // Disable form to prevent duplicate submissions
  disableCardForm();

  // Show intermediate success message
  showMessage('Processing your payment...');
});
```

#### `primer:card-error`

Dispatched when card validation fails or submission encounters an error.

**Event Detail:** Contains `errors` array with validation error objects.

**Usage:**

```javascript
checkout.addEventListener('primer:card-error', (event) => {
  const errors = event.detail.errors;
  console.error('❌ Card validation errors:', errors);

  // Log each error
  errors.forEach((error) => {
    console.error(`${error.field}: ${error.error}`);
  });

  // Display custom error UI
  displayValidationErrors(errors);
});
```

#### `primer:card-network-change`

Dispatched when the card network (Visa, Mastercard, etc.) is detected or changes based on the card number input.

**Event Detail:** Contains `detectedCardNetwork`, `selectableCardNetworks`, and `isLoading`.

**Usage:**

```javascript
checkout.addEventListener('primer:card-network-change', (event) => {
  const { detectedCardNetwork, selectableCardNetworks, isLoading } = event.detail;

  if (isLoading) {
    console.log('🔍 Detecting card network...');
    return;
  }

  if (detectedCardNetwork) {
    const network = detectedCardNetwork.network;
    console.log('💳 Card network detected:', network);

    // Show card brand logo
    updateCardBrandLogo(network);

    // Track card network detection
    analytics.track('Card Network Detected', { network });
  }
});
```

### Triggerable Events

Triggerable events are events that YOU dispatch to control SDK behavior.

#### `primer:card-submit`

Trigger card form submission programmatically from anywhere in your application.

**Event Detail:** Optional `source` property to identify the trigger source.

**Usage:**

The checkout component listens for this event at the document level, so you can dispatch it from anywhere without referencing the card form element directly.

```javascript
// Trigger card form submission from anywhere
document.dispatchEvent(
  new CustomEvent('primer:card-submit', {
    bubbles: true,
    composed: true,
    detail: { source: 'custom-button' },
  }),
);
```

**Complete Example: External Submit Button**

```html
<primer-checkout client-token="your-client-token">
  <primer-main slot="main">
    <div slot="payments">
      <primer-card-form>
        <div slot="card-form-content">
          <primer-input-card-number></primer-input-card-number>
          <primer-input-card-expiry></primer-input-card-expiry>
          <primer-input-cvv></primer-input-cvv>
          <!-- No submit button inside the form -->
        </div>
      </primer-card-form>

      <!-- External submit button outside the card form -->
      <button id="external-submit" class="custom-pay-button">Pay Now</button>
    </div>
  </primer-main>
</primer-checkout>

<script>
  // Set up external button
  document.getElementById('external-submit').addEventListener('click', () => {
    // Dispatch event to document - checkout listens at document level
    document.dispatchEvent(
      new CustomEvent('primer:card-submit', {
        bubbles: true,
        composed: true,
        detail: { source: 'external-button' },
      }),
    );
  });

  // Listen for submission results
  const checkout = document.querySelector('primer-checkout');

  checkout.addEventListener('primer:card-success', (event) => {
    console.log('✅ Card form submitted successfully');
  });

  checkout.addEventListener('primer:card-error', (event) => {
    console.log('❌ Validation errors:', event.detail.errors);
  });
</script>
```

**Important:**

- The `bubbles: true` and `composed: true` properties are required
- Always include a meaningful `source` parameter for debugging
- The checkout component handles the event at document level and forwards it internally

## Vault Integration

Vault allows customers to save payment methods for future use.

### Configuration

```javascript
checkout.options = {
  vault: {
    enabled: true, // Enable vaulting
    showEmptyState: true, // Show empty state message when no saved methods
  },
};
```

### Vault Events

Use the `primer:vault:methods-update` event to respond to vault changes:

```javascript
document.addEventListener('primer:vault:methods-update', (event) => {
  const { vaultedPayments, timestamp } = event.detail;

  console.log('Total saved methods:', vaultedPayments.size());

  // Get all methods
  const methods = vaultedPayments.toArray();
  methods.forEach((method) => {
    console.log(`${method.network} ending in ${method.last4Digits}`);
  });

  // Get specific method
  const method = vaultedPayments.get('payment-method-id');
  if (method) {
    console.log('Found method:', method);
  }
});
```

### Vault Callback

Use the callback for direct vault handling in the `primer:ready` event:

```javascript
checkout.addEventListener('primer:ready', (event) => {
  const primer = event.detail;

  primer.onVaultedMethodsUpdate = ({ vaultedPayments }) => {
    console.log('Vault updated:', vaultedPayments.size(), 'methods');
    updateVaultUI(vaultedPayments.toArray());
  };
});
```

### Complete Vault Example

```html
<primer-checkout client-token="your-client-token">
  <primer-main slot="main">
    <div slot="payments">
      <!-- Vaulted methods will appear here automatically -->
      <primer-payment-method-container></primer-payment-method-container>
    </div>
  </primer-main>
</primer-checkout>

<script>
  const checkout = document.querySelector('primer-checkout');

  // Configure vault
  checkout.options = {
    vault: {
      enabled: true,
      showEmptyState: true,
    },
  };

  // Handle vault updates
  checkout.addEventListener('primer:ready', (event) => {
    const primer = event.detail;

    primer.onVaultedMethodsUpdate = ({ vaultedPayments }) => {
      const methods = vaultedPayments.toArray();
      console.log(`Loaded ${methods.length} vaulted payment methods`);

      // Display saved methods
      methods.forEach((method) => {
        if (method.paymentInstrumentData) {
          console.log(
            `${method.paymentInstrumentData.network} ending in ${method.paymentInstrumentData.last4Digits}`,
          );
        }
      });
    };
  });
</script>
```

## React Integration Patterns

### Critical: Stable Object References

**THE MOST COMMON MISTAKE** with Primer in React is creating new object references on every render, causing component re-initialization and loss of user input.

This applies to **BOTH React 18 AND React 19**.

### React 18 vs React 19 Comparison

React 19 introduced improved support for web components, but the need for stable references remains critical.

| Aspect                        | React 18                              | React 19              |
| ----------------------------- | ------------------------------------- | --------------------- |
| **How objects passed**        | ref + useEffect                       | JSX props             |
| **Attribute conversion**      | Converts objects to `[object Object]` | Assigns as properties |
| **Code pattern**              | Imperative                            | Declarative           |
| **Lines of code**             | ~15 lines                             | ~5 lines              |
| **Stable references needed?** | ✅ Yes (always)                       | ✅ Yes (always)       |
| **Can inline objects?**       | ❌ No (doesn't work)                  | ❌ No (causes issues) |

### ALL Three Stable Reference Patterns

#### Pattern 1: Constant Outside Component (For Static Options)

```typescript
// ✅ Created once at module load, same reference forever
const SDK_OPTIONS = {
  locale: 'en-GB',
  card: {
    cardholderName: {
      required: true,
      visible: true,
    },
  },
};

function CheckoutPage({ clientToken }: { clientToken: string }) {
  // React 19 example
  return <primer-checkout client-token={clientToken} options={SDK_OPTIONS} />;
}
```

**When to use:** Options are static and don't depend on props, state, or user input

**Benefits:**

- ✅ Zero re-render overhead
- ✅ Simplest pattern
- ✅ No React hooks needed

#### Pattern 2: useMemo for Dynamic Options

```typescript
import { useMemo } from 'react';

function CheckoutPage({ clientToken, userLocale, merchantName }: Props) {
  // ✅ Creates new object ONLY when dependencies change
  const sdkOptions = useMemo(
    () => ({
      locale: userLocale,
      applePay: {
        merchantName: merchantName,
        merchantCountryCode: 'GB',
      },
    }),
    [userLocale, merchantName] // Only recreate when these change
  );

  // React 19 example
  return <primer-checkout client-token={clientToken} options={sdkOptions} />;
}
```

**When to use:** Options depend on props, state, or context that can change

**Benefits:**

- ✅ Stable reference until dependencies change
- ✅ Only re-initializes when necessary
- ✅ Prevents unnecessary re-renders

#### Pattern 3: Common Mistakes to Avoid

```typescript
// ❌ WRONG: Inline object in JSX
function CheckoutPage() {
  // New object on every render
  return <primer-checkout options={{ locale: 'en-GB' }} />;
}

// ❌ WRONG: Object in component body
function CheckoutPage() {
  // New object on every render
  const options = { locale: 'en-GB' };
  return <primer-checkout options={options} />;
}

// ✅ CORRECT: Use constant or useMemo
const SDK_OPTIONS = { locale: 'en-GB' };

function CheckoutPage() {
  // Same object reference every render
  return <primer-checkout options={SDK_OPTIONS} />;
}

// ✅ CORRECT: Use useMemo for empty deps
function CheckoutPage() {
  const options = useMemo(() => ({ locale: 'en-GB' }), []);
  return <primer-checkout options={options} />;
}
```

### TypeScript Setup

Show both patterns:

**Pattern 1: CheckoutElement**

```typescript
import type { CheckoutElement } from '@primer-io/primer-js';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'primer-checkout': CheckoutElement;
    }
  }
}
```

**Pattern 2: SDK Options Type**

```typescript
import type { PrimerCheckoutOptions } from '@primer-io/primer-js';

const options: PrimerCheckoutOptions = {
  locale: 'en-GB',
  enabledPaymentMethods: [PaymentMethodType.PAYMENT_CARD],
};
```

### React 18 Pattern (For Legacy Apps)

For React 18, you must use refs and useEffect:

```typescript
import { useRef, useEffect } from 'react';

// ✅ Define options outside component or use useMemo
const SDK_OPTIONS = { locale: 'en-GB' };

function CheckoutPage({ clientToken }: { clientToken: string }) {
  const checkoutRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const checkout = checkoutRef.current;
    if (!checkout) return;

    // Imperative property assignment
    checkout.options = SDK_OPTIONS;

    // Set up event listeners
    const handleReady = () => console.log('✅ SDK ready');
    checkout.addEventListener('primer:ready', handleReady);

    return () => {
      checkout.removeEventListener('primer:ready', handleReady);
    };
  }, []); // Empty deps - runs once

  return <primer-checkout ref={checkoutRef} client-token={clientToken} />;
}
```

### React 19 Pattern (Recommended)

React 19 allows direct JSX property assignment:

```typescript
// ✅ Define options outside component or use useMemo
const SDK_OPTIONS = { locale: 'en-GB' };

function CheckoutPage({ clientToken }: { clientToken: string }) {
  return <primer-checkout client-token={clientToken} options={SDK_OPTIONS} />;
}
```

**Critical:** Keep the constant! React 19 doesn't eliminate the need for stable references.

## Server-Side Rendering (SSR)

Primer Checkout requires browser APIs (Web Components, DOM) and must load client-side only.

### Why SSR Requires Special Handling

The SDK depends on:

- Web Components API (`customElements.define()`)
- DOM APIs for component rendering
- Browser context for iframes and payment processing
- `window` object

These don't exist in Node.js (server) environment.

### Next.js

#### App Router (Next.js 13+)

```typescript
'use client';

import { useEffect } from 'react';
import { loadPrimer } from '@primer-io/primer-js';

export default function CheckoutPage() {
  useEffect(() => {
    if (typeof window !== 'undefined') {
      loadPrimer().catch(console.error);
    }
  }, []);

  return <primer-checkout client-token="your-token" />;
}
```

The `'use client'` directive marks this component as client-side only.

#### Pages Router (Legacy)

```typescript
import { useEffect } from 'react';
import { loadPrimer } from '@primer-io/primer-js';

function CheckoutPage() {
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const initializePrimer = async () => {
        try {
          await loadPrimer();
          console.log('✅ Primer loaded');
        } catch (error) {
          console.error('❌ Failed to load Primer:', error);
        }
      };

      initializePrimer();
    }
  }, []);

  return <primer-checkout client-token="your-token" />;
}

export default CheckoutPage;
```

### Nuxt.js 3

```vue
<template>
  <primer-checkout client-token="your-token" />
</template>

<script setup>
import { onMounted } from 'vue';

onMounted(async () => {
  if (import.meta.client) {
    try {
      const { loadPrimer } = await import('@primer-io/primer-js');
      loadPrimer();
      console.log('✅ Primer loaded');
    } catch (error) {
      console.error('❌ Failed to load Primer:', error);
    }
  }
});
</script>
```

**Note:** Use `import.meta.client` (modern Nuxt 3) instead of `process.client` (legacy Nuxt 2).

### SvelteKit

```svelte
<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  onMount(async () => {
    if (browser) {
      try {
        const { loadPrimer } = await import('@primer-io/primer-js');
        loadPrimer();
        console.log('✅ Primer loaded');
      } catch (error) {
        console.error('❌ Failed to load Primer:', error);
      }
    }
  });
</script>

<primer-checkout client-token="your-token" />
```

### Best Practices

1. **Always use framework lifecycle methods** (useEffect, onMounted, onMount)
2. **Include environment checks** (`typeof window`, `import.meta.client`, `browser`)
3. **Use dynamic imports** to prevent server bundling
4. **Wrap in try-catch** for error handling
5. **Use stable references** for options objects (apply to all frameworks)

## Error Handling

### Payment Failure vs Validation Errors

**Validation Errors:**

- Handled by input components themselves
- Prevent form submission until fixed
- Displayed inline by card inputs
- No action needed from you

**Payment Failures:**

- Occur after form submission
- Displayed via `<primer-error-message-container>` or custom handling
- Require user action (retry, change payment method)

### Using Error Message Container

```html
<primer-checkout client-token="your-token">
  <primer-main slot="main">
    <div slot="payments">
      <primer-payment-method type="PAYMENT_CARD"></primer-payment-method>

      <!-- Shows payment failures automatically -->
      <primer-error-message-container></primer-error-message-container>
    </div>
  </primer-main>
</primer-checkout>
```

**Placement Guidelines:**

1. Prominently visible after payment attempt
2. Where users naturally look for feedback
3. Within same visual context as payment method

### Custom Error Handling

**Using Callbacks:**

```javascript
checkout.addEventListener('primer:ready', (event) => {
  const primer = event.detail;

  primer.onPaymentFailure = ({ error, paymentMethodType }) => {
    // Display custom error UI
    showErrorNotification({
      title: 'Payment Failed',
      message: error.message,
      allowRetry: true,
    });

    // Log for debugging
    console.error('Payment failed:', {
      code: error.code,
      message: error.message,
      diagnosticsId: error.diagnosticsId, // For support
      method: paymentMethodType,
    });

    // Send to error tracking
    errorTracker.capture({
      errorCode: error.code,
      diagnosticsId: error.diagnosticsId,
    });
  };
});
```

**Using State Change Event:**

```javascript
checkout.addEventListener('primer:state-change', (event) => {
  const { primerJsError, paymentFailure } = event.detail;

  if (primerJsError || paymentFailure) {
    const message = primerJsError?.message || paymentFailure?.message;
    showErrorMessage(message);

    // Log diagnostics ID for support
    if (paymentFailure?.diagnosticsId) {
      console.error('Diagnostics ID:', paymentFailure.diagnosticsId);
    }
  }
});
```

**Using Payment Failure Event:**

```javascript
document.addEventListener('primer:payment-failure', (event) => {
  const { error, paymentMethodType } = event.detail;

  // Show user-friendly error
  showErrorMessage(error.message);

  // Track in analytics
  analytics.track('Payment Failed', {
    errorCode: error.code,
    method: paymentMethodType,
  });

  // Log for debugging
  if (error.diagnosticsId) {
    console.error('Diagnostics ID for support:', error.diagnosticsId);
  }
});
```

## Component Properties vs SDK Options

### Why the Distinction Exists

Component properties use Lit's attribute system which monitors DOM attribute changes. Direct property assignment bypasses this system, causing values to be ignored. The `options` property is the ONLY exception - it's designed to accept direct property assignment.

### Component Properties (use `setAttribute()`)

These are HTML attributes set via `setAttribute()`:

- `client-token` - JWT from backend (REQUIRED)
- `custom-styles` - JSON string of CSS variables
- `loader-disabled` - Boolean to disable loader

```javascript
checkout.setAttribute('client-token', 'your-token');
checkout.setAttribute('loader-disabled', 'true');
checkout.setAttribute('custom-styles', JSON.stringify({ primerColorBrand: '#4a6cf7' }));
```

### SDK Options (use property assignment)

Everything else goes in the `options` object:

- Locale, payment methods, vault configuration, etc.

```javascript
checkout.options = {
  locale: 'en-GB',
  enabledPaymentMethods: [PaymentMethodType.PAYMENT_CARD],
  vault: { enabled: true },
};
```

### Debugging Tip

```javascript
// Check if using correctly
checkout.getAttribute('client-token'); // Should return token
checkout.options; // Should return options object

// Common mistake
checkout.getAttribute('locale'); // Returns null (locale is in options!)
```

**Remember:** Never mix these up. Component properties use `setAttribute()`, SDK options use direct property assignment.

## Preventing Flash of Undefined Components (FOUC)

Web components register via JavaScript. Before registration, custom elements may flash as undefined.

### CSS Solution (Simple)

```css
primer-checkout:has(:not(:defined)) {
  visibility: hidden;
}
```

Use `visibility: hidden` (not `display: none`) to preserve layout space.

### JavaScript Solution (More Control)

```javascript
Promise.allSettled([
  customElements.whenDefined('primer-checkout'),
  customElements.whenDefined('primer-payment-method'),
]).then(() => {
  document.querySelector('.checkout-container').classList.add('ready');
});
```

```css
.checkout-container {
  visibility: hidden;
}

.checkout-container.ready {
  visibility: visible;
}
```

## CSS Theming

### Custom Properties

Apply via CSS:

```css
:root {
  --primer-color-brand: #2f98ff;
  --primer-radius-base: 8px;
  --primer-typography-brand: 'Inter, sans-serif';
  --primer-space-base: 4px;
}

/* Or scope to specific checkout */
primer-checkout {
  --primer-color-brand: #4a6cf7;
}
```

Or via `custom-styles` attribute:

```html
<primer-checkout
  custom-styles='{"primerColorBrand":"#2f98ff","primerRadiusBase":"8px"}'
></primer-checkout>
```

### Dark Theme

```css
primer-checkout.primer-dark-theme {
  --primer-color-text-primary: var(--primer-color-gray-100);
  --primer-color-background-outlined-default: var(--primer-color-gray-800);
}
```

```javascript
// Apply theme
const checkout = document.querySelector('primer-checkout');
checkout.classList.add('primer-dark-theme');
```

## Common Use Cases

### 1. Default Checkout (Simplest)

```html
<primer-checkout client-token="your-token"></primer-checkout>
```

This provides a complete checkout experience with all available payment methods.

### 2. Custom Payment Method Layout

```html
<primer-checkout client-token="your-token">
  <primer-main slot="main">
    <div slot="payments">
      <h2>Choose Payment Method</h2>

      <!-- Individual methods -->
      <primer-payment-method type="PAYMENT_CARD"></primer-payment-method>
      <primer-payment-method type="PAYPAL"></primer-payment-method>

      <!-- Error display -->
      <primer-error-message-container></primer-error-message-container>
    </div>

    <div slot="checkout-complete">
      <h2>Thank you for your order!</h2>
    </div>
  </primer-main>
</primer-checkout>
```

### 3. Declarative Payment Filtering

```html
<div slot="payments">
  <!-- Show only digital wallets -->
  <primer-payment-method-container include="APPLE_PAY,GOOGLE_PAY">
  </primer-payment-method-container>

  <!-- Show everything except cards -->
  <primer-payment-method-container exclude="PAYMENT_CARD"> </primer-payment-method-container>
</div>
```

### 4. Custom Card Form

```html
<primer-card-form>
  <div slot="card-form-content">
    <primer-input-card-number></primer-input-card-number>

    <div style="display: flex; gap: 8px;">
      <primer-input-card-expiry></primer-input-card-expiry>
      <primer-input-cvv></primer-input-cvv>
    </div>

    <primer-input-card-holder-name></primer-input-card-holder-name>

    <!-- Custom field using base components -->
    <primer-input-wrapper>
      <primer-input-label slot="label">Billing Zip</primer-input-label>
      <primer-input slot="input" type="text" name="zip"></primer-input>
    </primer-input-wrapper>

    <primer-card-form-submit></primer-card-form-submit>
  </div>
</primer-card-form>
```

## Best Practices

1. **Always use stable object references** in React (module-level constants or `useMemo`)
2. **Set component properties via `setAttribute()`**, SDK options via property assignment
3. **Clean up event listeners** in React `useEffect` cleanup functions
4. **Use declarative containers** (`primer-payment-method-container`) instead of manual filtering
5. **Include error handling** with `primer-error-message-container` or custom callbacks
6. **Load Primer in `useEffect`** (or equivalent) for SSR frameworks
7. **Use TypeScript declarations** for proper JSX support
8. **Keep SDK options simple** - only configure what you need
9. **Use v0.7.0+ callbacks** (`onPaymentSuccess`, `onPaymentFailure`) for clearer error handling
10. **Track diagnosticsId** in payment failures for support inquiries

## Common Troubleshooting

### Component re-initializing on every render?

→ Check object reference stability. Use module-level constants or `useMemo`.
→ In React 19, ensure options object has stable reference.
→ Applies to BOTH React 18 AND React 19.

### TypeScript errors with JSX?

→ Add TypeScript declarations: `import type { CheckoutElement } from '@primer-io/primer-js'`
→ Declare in global JSX namespace or use `CustomElements` type

### SSR errors ("customElements is not defined", "window is not defined")?

→ Load Primer in client-side lifecycle: `useEffect`, `onMounted`, `onMount`
→ Use `'use client'` directive in Next.js App Router
→ Add environment checks: `typeof window !== 'undefined'`
→ Use dynamic imports: `await import('@primer-io/primer-js')`

### Event not firing?

→ Ensure component is mounted before adding listener
→ Use `useEffect` in React, wait for `primer:ready`
→ Check event name (v0.7.0 renamed some events)

### Payment methods not showing?

→ Check client token is valid
→ Check `enabledPaymentMethods` configuration
→ Wait for `primer:ready` event before accessing SDK
→ Verify methods are configured in Primer Dashboard
→ Check SDK Core vs Legacy mode compatibility

### Options not applying?

→ Check you're using `checkout.options = {...}`, not `setAttribute`
→ Verify object has stable reference in React
→ Check SDK Core vs Legacy mode compatibility
→ Never set `client-token` in options (it's a component property)

### Styling not applying?

→ CSS custom properties pierce Shadow DOM
→ Use `--primer-*` variables
→ Check specificity and scoping
→ Apply to `primer-checkout` element or `:root`

### Infinite re-renders in React?

→ Inline object in JSX: `options={{ locale: 'en-GB' }}` - use constant or useMemo
→ Object in component body without useMemo
→ Dependencies missing in useMemo array
→ This happens in BOTH React 18 AND React 19

### "Cannot set property options of HTMLElement"?

→ Component not yet registered, wait for `primer:ready`
→ Or ensure `loadPrimer()` was called
→ Use `customElements.whenDefined('primer-checkout')` to wait

### Payment failures not displaying?

→ Include `<primer-error-message-container>` in your layout
→ Or implement custom error handling with `onPaymentFailure` callback
→ Or listen to `primer:payment-failure` event
→ Check `primerJsError` and `paymentFailure` in state change events

### Vaulted methods not appearing?

→ Check `vault.enabled: true` in options
→ Verify client session has `vaultOnSuccess: true`
→ Listen to `primer:vault:methods-update` event
→ Use `onVaultedMethodsUpdate` callback for updates

### PayPal button not showing?

→ Check `sdkCore: true` (required for PayPal)
→ Include `PaymentMethodType.PAYPAL` in `enabledPaymentMethods`
→ Verify PayPal is configured in Primer Dashboard
→ Check browser console for PayPal SDK errors

## Resources

For always up-to-date documentation, this skill references the Primer Checkout documentation covering:

- Component APIs and properties
- SDK options and configuration
- Event payloads and callbacks
- Payment lifecycle handling
- Vault integration patterns
- React integration patterns (React 18 & 19)
- SSR framework patterns (Next.js, Nuxt, SvelteKit)
- CSS theming and customization
- TypeScript type definitions

For the latest component APIs, patterns, and examples, use Context7 MCP server:

```typescript
// Resolve library
const library = await resolveLibraryId('primer checkout components');
// Returns: /primer-io/examples

// Fetch documentation
const docs = await getLibraryDocs('/primer-io/examples', {
  topic: 'payment lifecycle events',
  tokens: 10000,
});
```

This ensures access to the most current component APIs, v0.7.0+ features, and integration patterns.
