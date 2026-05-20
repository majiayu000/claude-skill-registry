---
name: passkit-wallet
description: "Integrate Apple Pay payments and Wallet passes using PassKit. Use when adding Apple Pay buttons, creating payment requests, handling payment authorization, adding passes to Wallet, configuring merchant capabilities, managing shipping and contact fields, or working with PKPaymentRequest, PKPaymentAuthorizationController, PKPaymentButton, PKPass, PKAddPassesViewController, PKPassLibrary, or Apple Pay checkout flows."
---

# PassKit — Apple Pay & Wallet

Accept Apple Pay payments for physical goods and services, and add passes to
the user's Wallet. Covers payment buttons, payment requests, authorization,
Wallet passes, and merchant configuration. Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [Displaying the Apple Pay Button](#displaying-the-apple-pay-button)
- [Creating a Payment Request](#creating-a-payment-request)
- [Presenting the Payment Sheet](#presenting-the-payment-sheet)
- [Handling Payment Authorization](#handling-payment-authorization)
- [Wallet Passes](#wallet-passes)
- [Checking Pass Library](#checking-pass-library)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Project Configuration

1. Enable the **Apple Pay** capability in Xcode
2. Create a Merchant ID in the Apple Developer portal (format: `merchant.com.example.app`)
3. Generate and install a Payment Processing Certificate for your merchant ID
4. Add the merchant ID to your entitlements

### Availability Check

Always verify the device can make payments before showing Apple Pay UI.

```swift
import PassKit

func canMakePayments() -> Bool {
    // Check device supports Apple Pay at all
    guard PKPaymentAuthorizationController.canMakePayments() else {
        return false
    }
    // Check user has cards for the networks you support
    return PKPaymentAuthorizationController.canMakePayments(
        usingNetworks: [.visa, .masterCard, .amex, .discover],
        capabilities: .threeDSecure
    )
}
```

## Displaying the Apple Pay Button

### SwiftUI

Use the built-in `PayWithApplePayButton` view in SwiftUI.

```swift
import SwiftUI
import PassKit

struct CheckoutView: View {
    var body: some View {
        PayWithApplePayButton(.buy) {
            startPayment()
        }
        .payWithApplePayButtonStyle(.black)
        .frame(height: 48)
        .padding()
    }
}
```

### UIKit

Use `PKPaymentButton` for UIKit-based interfaces.

```swift
let button = PKPaymentButton(
    paymentButtonType: .buy,
    paymentButtonStyle: .black
)
button.cornerRadius = 12
button.addTarget(self, action: #selector(startPayment), for: .touchUpInside)
```

**Button types:** `.buy`, `.setUp`, `.inStore`, `.donate`, `.checkout`, `.book`, `.subscribe`, `.reload`, `.addMoney`, `.topUp`, `.order`, `.rent`, `.support`, `.contribute`, `.tip`

## Creating a Payment Request

Build a `PKPaymentRequest` with your merchant details and the items being purchased.

```swift
func createPaymentRequest() -> PKPaymentRequest {
    let request = PKPaymentRequest()
    request.merchantIdentifier = "merchant.com.example.app"
    request.countryCode = "US"
    request.currencyCode = "USD"
    request.supportedNetworks = [.visa, .masterCard, .amex, .discover]
    request.merchantCapabilities = .threeDSecure

    request.paymentSummaryItems = [
        PKPaymentSummaryItem(label: "Widget", amount: 9.99),
        PKPaymentSummaryItem(label: "Shipping", amount: 4.99),
        PKPaymentSummaryItem(label: "My Store", amount: 14.98) // Total (last item)
    ]

    return request
}
```

The **last item** in `paymentSummaryItems` is treated as the total and its label appears as the merchant name on the payment sheet.

### Requesting Shipping and Contact Info

```swift
request.requiredShippingContactFields = [.postalAddress, .emailAddress, .name]
request.requiredBillingContactFields = [.postalAddress]

request.shippingMethods = [
    PKShippingMethod(label: "Standard", amount: 4.99),
    PKShippingMethod(label: "Express", amount: 9.99),
]
request.shippingMethods?[0].identifier = "standard"
request.shippingMethods?[0].detail = "5-7 business days"
request.shippingMethods?[1].identifier = "express"
request.shippingMethods?[1].detail = "1-2 business days"

request.shippingType = .shipping // .delivery, .storePickup, .servicePickup
```

### Supported Networks

| Network | Constant |
|---|---|
| Visa | `.visa` |
| Mastercard | `.masterCard` |
| American Express | `.amex` |
| Discover | `.discover` |
| China UnionPay | `.chinaUnionPay` |
| JCB | `.JCB` |
| Maestro | `.maestro` |
| Electron | `.electron` |
| Interac | `.interac` |

Query available networks at runtime with `PKPaymentRequest.availableNetworks()`.

## Presenting the Payment Sheet

Use `PKPaymentAuthorizationController` (works in both SwiftUI and UIKit, no view controller needed).

```swift
@MainActor
func startPayment() {
    let request = createPaymentRequest()
    let controller = PKPaymentAuthorizationController(paymentRequest: request)
    controller.delegate = self
    controller.present()
}
```

## Handling Payment Authorization

Implement `PKPaymentAuthorizationControllerDelegate` to process the payment token.

```swift
extension CheckoutCoordinator: PKPaymentAuthorizationControllerDelegate {
    func paymentAuthorizationController(
        _ controller: PKPaymentAuthorizationController,
        didAuthorizePayment payment: PKPayment,
        handler completion: @escaping (PKPaymentAuthorizationResult) -> Void
    ) {
        // Send payment.token.paymentData to your payment processor
        Task {
            do {
                try await paymentService.process(payment.token)
                completion(PKPaymentAuthorizationResult(status: .success, errors: nil))
            } catch {
                completion(PKPaymentAuthorizationResult(status: .failure, errors: [error]))
            }
        }
    }

    func paymentAuthorizationControllerDidFinish(
        _ controller: PKPaymentAuthorizationController
    ) {
        controller.dismiss()
    }
}
```

### Handling Shipping Changes

```swift
func paymentAuthorizationController(
    _ controller: PKPaymentAuthorizationController,
    didSelectShippingMethod shippingMethod: PKShippingMethod,
    handler completion: @escaping (PKPaymentRequestShippingMethodUpdate) -> Void
) {
    let updatedItems = recalculateItems(with: shippingMethod)
    let update = PKPaymentRequestShippingMethodUpdate(paymentSummaryItems: updatedItems)
    completion(update)
}
```

## Wallet Passes

### Adding a Pass to Wallet

Load a `.pkpass` file and present `PKAddPassesViewController`.

```swift
func addPassToWallet(data: Data) {
    guard let pass = try? PKPass(data: data) else { return }

    if let addController = PKAddPassesViewController(pass: pass) {
        addController.delegate = self
        present(addController, animated: true)
    }
}
```

### SwiftUI Wallet Button

```swift
import PassKit
import SwiftUI

struct AddPassButton: View {
    let passData: Data

    var body: some View {
        Button("Add to Wallet") {
            addPass()
        }
    }

    func addPass() {
        guard let pass = try? PKPass(data: passData) else { return }
        let library = PKPassLibrary()
        library.addPasses([pass]) { status in
            switch status {
            case .shouldReviewPasses:
                // Present review UI
                break
            case .didAddPasses:
                // Passes added successfully
                break
            case .didCancelAddPasses:
                break
            @unknown default:
                break
            }
        }
    }
}
```

## Checking Pass Library

Use `PKPassLibrary` to inspect and manage passes the user already has.

```swift
let library = PKPassLibrary()

// Check if a specific pass is already in Wallet
let hasPass = library.containsPass(pass)

// Retrieve passes your app can access
let passes = library.passes()

// Check if pass library is available
guard PKPassLibrary.isPassLibraryAvailable() else { return }
```

## Common Mistakes

### DON'T: Use StoreKit for physical goods

Apple Pay (PassKit) is for **physical goods and services**. StoreKit is for digital
content, subscriptions, and in-app purchases. Using the wrong framework leads to
App Review rejection.

```swift
// WRONG: Using StoreKit to sell a physical product
let product = try await Product.products(for: ["com.example.tshirt"])

// CORRECT: Use Apple Pay for physical goods
let request = PKPaymentRequest()
request.paymentSummaryItems = [
    PKPaymentSummaryItem(label: "T-Shirt", amount: 29.99),
    PKPaymentSummaryItem(label: "My Store", amount: 29.99)
]
```

### DON'T: Hardcode merchant ID in multiple places

```swift
// WRONG: Merchant ID scattered across the codebase
let request1 = PKPaymentRequest()
request1.merchantIdentifier = "merchant.com.example.app"
// ...elsewhere:
let request2 = PKPaymentRequest()
request2.merchantIdentifier = "merchant.com.example.app" // easy to get out of sync

// CORRECT: Centralize configuration
enum PaymentConfig {
    static let merchantIdentifier = "merchant.com.example.app"
    static let countryCode = "US"
    static let currencyCode = "USD"
    static let supportedNetworks: [PKPaymentNetwork] = [.visa, .masterCard, .amex]
}
```

### DON'T: Forget the total line item

The last item in `paymentSummaryItems` is the total row. If you omit it, the
payment sheet shows no merchant name or total.

```swift
// WRONG: No total item
request.paymentSummaryItems = [
    PKPaymentSummaryItem(label: "Widget", amount: 9.99)
]

// CORRECT: Last item is the total with your merchant name
request.paymentSummaryItems = [
    PKPaymentSummaryItem(label: "Widget", amount: 9.99),
    PKPaymentSummaryItem(label: "My Store", amount: 9.99) // Total
]
```

### DON'T: Skip the canMakePayments check

```swift
// WRONG: Show Apple Pay button without checking
PayWithApplePayButton(.buy) { startPayment() }

// CORRECT: Only show when available
if PKPaymentAuthorizationController.canMakePayments(
    usingNetworks: PaymentConfig.supportedNetworks
) {
    PayWithApplePayButton(.buy) { startPayment() }
} else {
    // Show alternative checkout or setup button
    Button("Set Up Apple Pay") { /* guide user */ }
}
```

### DON'T: Dismiss the controller before completing authorization

```swift
// WRONG: Dismissing inside didAuthorizePayment
func paymentAuthorizationController(
    _ controller: PKPaymentAuthorizationController,
    didAuthorizePayment payment: PKPayment,
    handler completion: @escaping (PKPaymentAuthorizationResult) -> Void
) {
    controller.dismiss() // Too early -- causes blank sheet
    completion(.init(status: .success, errors: nil))
}

// CORRECT: Dismiss only in paymentAuthorizationControllerDidFinish
func paymentAuthorizationControllerDidFinish(
    _ controller: PKPaymentAuthorizationController
) {
    controller.dismiss()
}
```

## Review Checklist

- [ ] Apple Pay capability enabled and merchant ID configured in Developer portal
- [ ] Payment Processing Certificate generated and installed
- [ ] `canMakePayments(usingNetworks:)` checked before showing Apple Pay button
- [ ] Last item in `paymentSummaryItems` is the total with merchant display name
- [ ] Payment token sent to server for processing (never decoded client-side)
- [ ] `paymentAuthorizationControllerDidFinish` dismisses the controller
- [ ] Shipping method changes recalculate totals via delegate callback
- [ ] StoreKit used for digital goods; Apple Pay used for physical goods
- [ ] Wallet passes loaded from signed `.pkpass` bundles
- [ ] `PKPassLibrary.isPassLibraryAvailable()` checked before pass operations
- [ ] Apple Pay button uses system-provided `PKPaymentButton` or `PayWithApplePayButton`
- [ ] Error states handled in authorization result (network failures, declined cards)

## References

- Extended patterns (recurring payments, coupon codes, multi-merchant): `references/wallet-passes.md`
- [PassKit framework](https://sosumi.ai/documentation/passkit)
- [PKPaymentRequest](https://sosumi.ai/documentation/passkit/pkpaymentrequest)
- [PKPaymentAuthorizationController](https://sosumi.ai/documentation/passkit/pkpaymentauthorizationcontroller)
- [PKPaymentButton](https://sosumi.ai/documentation/passkit/pkpaymentbutton)
- [PKPass](https://sosumi.ai/documentation/passkit/pkpass)
- [PKAddPassesViewController](https://sosumi.ai/documentation/passkit/pkaddpassesviewcontroller)
- [PKPassLibrary](https://sosumi.ai/documentation/passkit/pkpasslibrary)
- [PKPaymentNetwork](https://sosumi.ai/documentation/passkit/pkpaymentnetwork)
