---
name: in-app-purchases
description: '| ID | flutter-iap |'
---

# 💰 Skill: In-App Purchases (IAP)

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-iap` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `in-app-purchases`, `iap`, `subscriptions`, `revenue-cat`, `app-store`, `play-billing` |
| **Referencia** | [in_app_purchase Plugin](https://pub.dev/packages/in_app_purchase) |

## 🔑 Keywords para Invocación

- `in-app-purchases`
- `iap`
- `subscriptions`
- `revenue-cat`
- `revenuecat`
- `billing`
- `@skill:iap`

### Ejemplos de Prompts

```
Implementa in-app-purchases con subscriptions
```

```
Setup revenue-cat para gestionar suscripciones
```

```
Configura billing para App Store y Play Store
```

```
@skill:iap - Sistema completo de compras y suscripciones
```

## 📖 Descripción

Este skill cubre la implementación de In-App Purchases (IAP) y subscriptions usando el plugin `in_app_purchase` y RevenueCat. Incluye productos consumibles, no consumibles, subscriptions, restore purchases, y receipt validation.

### ✅ Cuándo Usar Este Skill

- Apps con modelo freemium
- Subscriptions (mensual/anual)
- Premium features
- Virtual goods/currency
- Remove ads
- Content unlocking
- SaaS apps

### ❌ Cuándo NO Usar Este Skill

- Apps completamente gratuitas
- Monetización solo con ads
- Servicios externos (no permitido por Apple/Google)

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── services/
│   │   └── purchases/
│   │       ├── iap_service.dart
│   │       ├── purchase_models.dart
│   │       └── subscription_service.dart
│   │
│   └── main.dart
│
├── android/
│   └── app/
│       └── src/main/
│           └── AndroidManifest.xml
│
└── ios/
    └── Runner/
        └── Info.plist
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

  # In-App Purchase
  in_app_purchase: ^3.1.11

  # RevenueCat (alternative)
  purchases_flutter: ^6.16.0

dev_dependencies:
  flutter_test:
    sdk: flutter
```

## 💻 Implementación

### 1. Product Models

```dart
// lib/services/purchases/purchase_models.dart
enum ProductType {
  consumable,      // Can be purchased multiple times (coins, lives)
  nonConsumable,   // One-time purchase (premium upgrade)
  subscription,    // Recurring (monthly/yearly)
}

class AppProduct {
  final String id;
  final ProductType type;
  final String title;
  final String description;
  final String price;
  final double rawPrice;
  final String currencyCode;

  AppProduct({
    required this.id,
    required this.type,
    required this.title,
    required this.description,
    required this.price,
    required this.rawPrice,
    required this.currencyCode,
  });
}

class ProductIds {
  // Consumables
  static const String coins100 = 'coins_100';
  static const String coins500 = 'coins_500';
  static const String coins1000 = 'coins_1000';

  // Non-consumables
  static const String premiumUpgrade = 'premium_upgrade';
  static const String removeAds = 'remove_ads';

  // Subscriptions
  static const String monthlySubscription = 'monthly_subscription';
  static const String yearlySubscription = 'yearly_subscription';

  static Set<String> get allProductIds => {
        coins100,
        coins500,
        coins1000,
        premiumUpgrade,
        removeAds,
        monthlySubscription,
        yearlySubscription,
      };
}
```

### 2. IAP Service

```dart
// lib/services/purchases/iap_service.dart
import 'dart:async';
import 'dart:io';
import 'package:in_app_purchase/in_app_purchase.dart';
import 'package:in_app_purchase_android/in_app_purchase_android.dart';
import 'package:in_app_purchase_storekit/in_app_purchase_storekit.dart';
import 'package:flutter/services.dart';
import 'purchase_models.dart';

class IAPService {
  static final InAppPurchase _iap = InAppPurchase.instance;
  static StreamSubscription<List<PurchaseDetails>>? _subscription;

  static bool _isAvailable = false;
  static List<ProductDetails> _products = [];
  static List<PurchaseDetails> _purchases = [];

  static bool get isAvailable => _isAvailable;
  static List<ProductDetails> get products => _products;
  static List<PurchaseDetails> get purchases => _purchases;

  // Initialize IAP
  static Future<void> initialize() async {
    // Check if IAP is available
    _isAvailable = await _iap.isAvailable();

    if (!_isAvailable) {
      print('❌ In-App Purchases not available');
      return;
    }

    // Setup purchase updates listener
    _subscription = _iap.purchaseStream.listen(
      _onPurchaseUpdate,
      onError: (error) {
        print('❌ Purchase error: $error');
      },
    );

    // Load products
    await loadProducts();

    // Restore purchases
    await restorePurchases();

    print('✅ IAP initialized');
  }

  // Load products from stores
  static Future<void> loadProducts() async {
    if (!_isAvailable) return;

    try {
      final ProductDetailsResponse response = await _iap.queryProductDetails(
        ProductIds.allProductIds,
      );

      if (response.error != null) {
        print('❌ Error loading products: ${response.error}');
        return;
      }

      if (response.productDetails.isEmpty) {
        print('⚠️ No products found');
        return;
      }

      _products = response.productDetails;
      print('✅ Loaded ${_products.length} products');
    } catch (e) {
      print('❌ Exception loading products: $e');
    }
  }

  // Purchase product
  static Future<bool> purchaseProduct(ProductDetails product) async {
    if (!_isAvailable) return false;

    try {
      final PurchaseParam purchaseParam = PurchaseParam(
        productDetails: product,
      );

      // Determine purchase type
      if (product.id == ProductIds.coins100 ||
          product.id == ProductIds.coins500 ||
          product.id == ProductIds.coins1000) {
        // Consumable
        return await _iap.buyConsumable(purchaseParam: purchaseParam);
      } else {
        // Non-consumable or subscription
        return await _iap.buyNonConsumable(purchaseParam: purchaseParam);
      }
    } catch (e) {
      print('❌ Purchase error: $e');
      return false;
    }
  }

  // Handle purchase updates
  static Future<void> _onPurchaseUpdate(
    List<PurchaseDetails> purchaseDetailsList,
  ) async {
    for (final PurchaseDetails purchase in purchaseDetailsList) {
      print('📱 Purchase update: ${purchase.productID} - ${purchase.status}');

      switch (purchase.status) {
        case PurchaseStatus.pending:
          _handlePending(purchase);
          break;

        case PurchaseStatus.purchased:
          await _handlePurchased(purchase);
          break;

        case PurchaseStatus.error:
          _handleError(purchase);
          break;

        case PurchaseStatus.restored:
          await _handleRestored(purchase);
          break;

        case PurchaseStatus.canceled:
          _handleCanceled(purchase);
          break;

        default:
          break;
      }

      // Complete purchase
      if (purchase.pendingCompletePurchase) {
        await _iap.completePurchase(purchase);
      }
    }
  }

  static void _handlePending(PurchaseDetails purchase) {
    print('⏳ Purchase pending: ${purchase.productID}');
    // Show loading indicator
  }

  static Future<void> _handlePurchased(PurchaseDetails purchase) async {
    print('✅ Purchase successful: ${purchase.productID}');

    // Verify purchase with server
    final isValid = await _verifyPurchase(purchase);

    if (isValid) {
      // Deliver content
      await _deliverProduct(purchase);

      // Track revenue
      AnalyticsService.trackEvent('purchase_completed', properties: {
        'product_id': purchase.productID,
        'transaction_id': purchase.purchaseID,
      });
    } else {
      print('❌ Purchase verification failed');
    }
  }

  static void _handleError(PurchaseDetails purchase) {
    print('❌ Purchase error: ${purchase.error}');

    // Show error to user
    // Track failed purchase
    AnalyticsService.trackEvent('purchase_failed', properties: {
      'product_id': purchase.productID,
      'error': purchase.error?.message,
    });
  }

  static Future<void> _handleRestored(PurchaseDetails purchase) async {
    print('🔄 Purchase restored: ${purchase.productID}');
    await _deliverProduct(purchase);
  }

  static void _handleCanceled(PurchaseDetails purchase) {
    print('❌ Purchase canceled: ${purchase.productID}');

    AnalyticsService.trackEvent('purchase_canceled', properties: {
      'product_id': purchase.productID,
    });
  }

  // Verify purchase with server
  static Future<bool> _verifyPurchase(PurchaseDetails purchase) async {
    try {
      // TODO: Implement server-side verification
      // Send receipt to your server for validation

      if (Platform.isAndroid) {
        // Android: Send purchase token
        final androidPurchase = purchase as GooglePlayPurchaseDetails;
        // await api.verifyAndroidPurchase(
        //   productId: purchase.productID,
        //   purchaseToken: androidPurchase.billingClientPurchase.purchaseToken,
        // );
      } else if (Platform.isIOS) {
        // iOS: Send receipt data
        final iosPurchase = purchase as AppStorePurchaseDetails;
        // await api.verifyIOSPurchase(
        //   productId: purchase.productID,
        //   receiptData: iosPurchase.verificationData.serverVerificationData,
        // );
      }

      return true;
    } catch (e) {
      print('❌ Verification error: $e');
      return false;
    }
  }

  // Deliver product to user
  static Future<void> _deliverProduct(PurchaseDetails purchase) async {
    final productId = purchase.productID;

    // Consumables
    if (productId == ProductIds.coins100) {
      await _addCoins(100);
    } else if (productId == ProductIds.coins500) {
      await _addCoins(500);
    } else if (productId == ProductIds.coins1000) {
      await _addCoins(1000);
    }
    // Non-consumables
    else if (productId == ProductIds.premiumUpgrade) {
      await _unlockPremium();
    } else if (productId == ProductIds.removeAds) {
      await _removeAds();
    }
    // Subscriptions
    else if (productId == ProductIds.monthlySubscription ||
        productId == ProductIds.yearlySubscription) {
      await _activateSubscription(productId);
    }

    _purchases.add(purchase);
  }

  static Future<void> _addCoins(int amount) async {
    // TODO: Implement coin addition logic
    print('💰 Added $amount coins');
  }

  static Future<void> _unlockPremium() async {
    // TODO: Implement premium unlock logic
    print('⭐ Premium unlocked');
  }

  static Future<void> _removeAds() async {
    // TODO: Implement ad removal logic
    print('🚫 Ads removed');
  }

  static Future<void> _activateSubscription(String productId) async {
    // TODO: Implement subscription activation
    print('📅 Subscription activated: $productId');
  }

  // Restore purchases
  static Future<void> restorePurchases() async {
    if (!_isAvailable) return;

    try {
      await _iap.restorePurchases();
      print('✅ Purchases restored');
    } catch (e) {
      print('❌ Restore error: $e');
    }
  }

  // Check if product is purchased
  static bool isPurchased(String productId) {
    return _purchases.any((purchase) => purchase.productID == productId);
  }

  // Get product by ID
  static ProductDetails? getProductById(String productId) {
    try {
      return _products.firstWhere((product) => product.id == productId);
    } catch (e) {
      return null;
    }
  }

  // Dispose
  static Future<void> dispose() async {
    await _subscription?.cancel();
  }
}
```

### 3. Subscription Service

```dart
// lib/services/purchases/subscription_service.dart
import 'iap_service.dart';
import 'purchase_models.dart';

enum SubscriptionStatus {
  none,
  active,
  expired,
  canceled,
}

class SubscriptionService {
  static SubscriptionStatus _status = SubscriptionStatus.none;
  static DateTime? _expirationDate;

  static SubscriptionStatus get status => _status;
  static DateTime? get expirationDate => _expirationDate;
  static bool get isActive => _status == SubscriptionStatus.active;

  // Check subscription status
  static Future<void> checkSubscriptionStatus() async {
    final hasMonthly = IAPService.isPurchased(ProductIds.monthlySubscription);
    final hasYearly = IAPService.isPurchased(ProductIds.yearlySubscription);

    if (hasMonthly || hasYearly) {
      // TODO: Verify with server if subscription is still active
      // This should check expiration date from server
      _status = SubscriptionStatus.active;
    } else {
      _status = SubscriptionStatus.none;
    }
  }

  // Subscribe
  static Future<bool> subscribe(String productId) async {
    final product = IAPService.getProductById(productId);

    if (product == null) {
      print('❌ Product not found: $productId');
      return false;
    }

    final success = await IAPService.purchaseProduct(product);

    if (success) {
      await checkSubscriptionStatus();
    }

    return success;
  }

  // Cancel subscription (opens store management)
  static Future<void> manageSubscription() async {
    // iOS: Opens subscription management in App Store
    // Android: Opens subscription management in Play Store

    if (Platform.isIOS) {
      // Open iOS subscription management
      await canLaunchUrl(Uri.parse('https://apps.apple.com/account/subscriptions'));
    } else if (Platform.isAndroid) {
      // Open Android subscription management
      await canLaunchUrl(Uri.parse('https://play.google.com/store/account/subscriptions'));
    }
  }
}
```

### 4. Usage Example

```dart
// lib/screens/store_screen.dart
import 'package:flutter/material.dart';

class StoreScreen extends StatefulWidget {
  @override
  State<StoreScreen> createState() => _StoreScreenState();
}

class _StoreScreenState extends State<StoreScreen> {
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadProducts();
  }

  Future<void> _loadProducts() async {
    await IAPService.loadProducts();
    setState(() {
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final products = IAPService.products;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Store'),
        actions: [
          TextButton(
            onPressed: () async {
              await IAPService.restorePurchases();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Purchases restored')),
              );
            },
            child: const Text('Restore'),
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) {
          final product = products[index];

          return Card(
            margin: const EdgeInsets.all(8),
            child: ListTile(
              title: Text(product.title),
              subtitle: Text(product.description),
              trailing: ElevatedButton(
                onPressed: () => _purchase(product),
                child: Text(product.price),
              ),
            ),
          );
        },
      ),
    );
  }

  Future<void> _purchase(ProductDetails product) async {
    final success = await IAPService.purchaseProduct(product);

    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Purchasing ${product.title}...')),
      );
    }
  }
}
```

### 5. iOS Configuration

```xml
<!-- ios/Runner/Info.plist -->
<key>SKAdNetworkItems</key>
<array>
    <!-- Add your SKAdNetwork IDs here -->
</array>
```

### 6. Android Configuration

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<manifest>
    <uses-permission android:name="com.android.vending.BILLING" />
</manifest>
```

## 🎯 Mejores Prácticas

### 1. Server-Side Validation

✅ **DO:** Siempre valida compras en tu servidor
```dart
// Never trust client-side only validation
final isValid = await api.verifyPurchase(receipt);
```

### 2. Restore Purchases

✅ **DO:** Implementa restore
```dart
// Required for non-consumables and subscriptions
await IAPService.restorePurchases();
```

### 3. Subscription Management

✅ **DO:** Link a subscription management
```dart
// Let users manage subscriptions in store
ElevatedButton(
  onPressed: () => SubscriptionService.manageSubscription(),
  child: const Text('Manage Subscription'),
);
```

## 🚨 Troubleshooting

### Products Not Loading

```dart
// Verify product IDs match exactly in stores
// iOS: App Store Connect
// Android: Google Play Console
```

### Purchase Not Completing

```dart
// Always call completePurchase
if (purchase.pendingCompletePurchase) {
  await InAppPurchase.instance.completePurchase(purchase);
}
```

### Sandbox Testing

```dart
// iOS: Use sandbox account
// Android: Use test tracks or license testers
```

## 📚 Recursos

- [in_app_purchase Plugin](https://pub.dev/packages/in_app_purchase)
- [RevenueCat](https://www.revenuecat.com/)
- [App Store Guidelines](https://developer.apple.com/app-store/review/guidelines/#in-app-purchase)
- [Google Play Billing](https://developer.android.com/google/play/billing)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
