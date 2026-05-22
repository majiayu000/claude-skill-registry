---
name: payment-integration
description: Payment processing integration with Stripe and PayPal for Flutter
keywords: payments, stripe, paypal, billing, subscriptions, ecommerce
---

# Skill 17: Payment Integration

## Overview

This skill provides comprehensive payment processing capabilities for Flutter applications using Stripe and PayPal. Supports one-time payments, subscriptions, and PCI-compliant payment flows.

## Features

- Stripe integration with Payment Intents
- PayPal checkout integration
- PCI DSS compliance (sensitive data never touches your server)
- Subscription management
- Apple Pay and Google Pay support
- Payment method storage
- Webhook handling

## Installation

### Dependencies

```yaml
dependencies:
  flutter_stripe: ^10.0.0
  paypal_sdk: ^1.0.0
  pay: ^1.1.2  # For Apple Pay / Google Pay
```

## Stripe Integration

### 1. Setup

```dart
import 'package:flutter_stripe/flutter_stripe.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Stripe
  Stripe.publishableKey = 'pk_test_your_key_here';
  await Stripe.instance.applySettings();

  runApp(MyApp());
}
```

### 2. Payment Service

```dart
import 'package:flutter_stripe/flutter_stripe.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PaymentService {
  final String backendUrl;

  PaymentService({required this.backendUrl});

  /// Create a payment intent on your backend
  Future<Map<String, dynamic>> createPaymentIntent(
    double amount,
    String currency,
  ) async {
    final response = await http.post(
      Uri.parse('$backendUrl/create-payment-intent'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'amount': (amount * 100).toInt(), // Stripe uses cents
        'currency': currency,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to create payment intent');
    }
  }

  /// Present payment sheet
  Future<bool> presentPaymentSheet(String clientSecret) async {
    try {
      // Initialize payment sheet
      await Stripe.instance.initPaymentSheet(
        paymentSheetParameters: SetupPaymentSheetParameters(
          paymentIntentClientSecret: clientSecret,
          merchantDisplayName: '{{PROJECT_NAME}}',
          style: ThemeMode.system,
        ),
      );

      // Display payment sheet
      await Stripe.instance.presentPaymentSheet();

      return true;
    } on StripeException catch (e) {
      if (e.error.code == FailureCode.Canceled) {
        return false; // User canceled
      }
      rethrow;
    }
  }

  /// Create and confirm payment
  Future<bool> makePayment(double amount, String currency) async {
    try {
      // 1. Create payment intent
      final paymentIntent = await createPaymentIntent(amount, currency);

      // 2. Present payment sheet
      final success = await presentPaymentSheet(paymentIntent['clientSecret']);

      return success;
    } catch (e) {
      print('Payment error: $e');
      return false;
    }
  }
}
```

### 3. Payment Provider

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

class PaymentState {
  final bool isProcessing;
  final bool paymentSuccess;
  final String? error;

  PaymentState({
    this.isProcessing = false,
    this.paymentSuccess = false,
    this.error,
  });

  PaymentState copyWith({
    bool? isProcessing,
    bool? paymentSuccess,
    String? error,
  }) {
    return PaymentState(
      isProcessing: isProcessing ?? this.isProcessing,
      paymentSuccess: paymentSuccess ?? this.paymentSuccess,
      error: error,
    );
  }
}

class PaymentNotifier extends StateNotifier<PaymentState> {
  final PaymentService _paymentService;

  PaymentNotifier(this._paymentService) : super(PaymentState());

  Future<void> processPayment(double amount, String currency) async {
    state = state.copyWith(isProcessing: true, error: null);

    try {
      final success = await _paymentService.makePayment(amount, currency);

      state = state.copyWith(
        isProcessing: false,
        paymentSuccess: success,
        error: success ? null : 'Payment was cancelled or failed',
      );
    } catch (e) {
      state = state.copyWith(
        isProcessing: false,
        paymentSuccess: false,
        error: e.toString(),
      );
    }
  }
}

final paymentProvider = StateNotifierProvider<PaymentNotifier, PaymentState>(
  (ref) => PaymentNotifier(PaymentService(backendUrl: 'https://your-api.com')),
);
```

### 4. Payment UI

```dart
class PaymentPage extends ConsumerWidget {
  const PaymentPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final paymentState = ref.watch(paymentProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Payment')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(
              'Total: \$20.00',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 32),
            if (paymentState.isProcessing)
              const CircularProgressIndicator()
            else
              ElevatedButton(
                onPressed: () {
                  ref.read(paymentProvider.notifier)
                      .processPayment(20.00, 'USD');
                },
                child: const Text('Pay Now'),
              ),
            if (paymentState.error != null)
              Text(
                paymentState.error!,
                style: const TextStyle(color: Colors.red),
              ),
            if (paymentState.paymentSuccess)
              const Text(
                'Payment successful!',
                style: TextStyle(color: Colors.green),
              ),
          ],
        ),
      ),
    );
  }
}
```

## Subscription Management

```dart
class SubscriptionService {
  final String backendUrl;

  SubscriptionService({required this.backendUrl});

  Future<Map<String, dynamic>> createSubscription(
    String customerId,
    String priceId,
  ) async {
    final response = await http.post(
      Uri.parse('$backendUrl/create-subscription'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'customerId': customerId,
        'priceId': priceId,
      }),
    );

    return jsonDecode(response.body);
  }

  Future<void> cancelSubscription(String subscriptionId) async {
    await http.post(
      Uri.parse('$backendUrl/cancel-subscription'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'subscriptionId': subscriptionId}),
    );
  }
}
```

## Apple Pay / Google Pay

```dart
import 'package:pay/pay.dart';

class DigitalWalletPayment extends StatelessWidget {
  final double amount;
  final String currency;

  const DigitalWalletPayment({
    super.key,
    required this.amount,
    required this.currency,
  });

  @override
  Widget build(BuildContext context) {
    return GooglePayButton(
      paymentConfigurationAsset: 'google_pay_config.json',
      paymentItems: [
        PaymentItem(
          label: 'Total',
          amount: amount.toStringAsFixed(2),
          status: PaymentItemStatus.final_price,
        ),
      ],
      type: GooglePayButtonType.pay,
      onPaymentResult: (result) {
        // Handle payment result
        print('Payment result: $result');
      },
    );
  }
}
```

## Security Best Practices

1. **Never store card data** - Use Stripe tokens only
2. **Backend validation** - Always verify payments on server
3. **HTTPS only** - All API calls must use HTTPS
4. **PCI Compliance** - Don't handle raw card numbers
5. **Webhook verification** - Verify Stripe signatures

## Backend Requirements

Your backend must implement:

```javascript
// Node.js/Express example
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

app.post('/create-payment-intent', async (req, res) => {
  const { amount, currency } = req.body;

  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency,
    automatic_payment_methods: { enabled: true },
  });

  res.json({ clientSecret: paymentIntent.client_secret });
});

app.post('/webhook', async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const event = stripe.webhooks.constructEvent(
    req.body,
    sig,
    process.env.STRIPE_WEBHOOK_SECRET
  );

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      // Fulfill the purchase
      break;
    case 'payment_intent.payment_failed':
      // Notify user
      break;
  }

  res.json({ received: true });
});
```

## Testing

Use Stripe test cards:
- `4242 4242 4242 4242` - Success
- `4000 0000 0000 9995` - Declined
- `4000 0000 0000 3220` - Requires 3D Secure
