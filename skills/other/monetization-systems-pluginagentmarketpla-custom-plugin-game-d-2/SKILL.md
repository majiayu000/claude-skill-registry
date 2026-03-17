---
name: monetization-systems
version: "2.0.0"
description: |
  Game monetization strategies, in-app purchases, battle passes, ads integration,
  and player retention mechanics. Ethical monetization that respects players.
sasmp_version: "1.3.0"
bonded_agent: 07-game-publishing
bond_type: PRIMARY_BOND

parameters:
  - name: model
    type: string
    required: false
    validation:
      enum: [premium, f2p, freemium, subscription, ad_supported]
  - name: platform
    type: string
    required: false
    validation:
      enum: [mobile, pc, console, web]

retry_policy:
  enabled: true
  max_attempts: 3
  backoff: exponential

observability:
  log_events: [start, complete, error, purchase, refund]
  metrics: [arpu, arppu, conversion_rate, ltv, retention]
---

# Monetization Systems

## Monetization Models

```
CHOOSING YOUR MODEL:
┌─────────────────────────────────────────────────────────────┐
│  GAME TYPE                    → RECOMMENDED MODEL           │
├─────────────────────────────────────────────────────────────┤
│  Story-driven / Single play   → PREMIUM ($10-60)           │
│  Competitive multiplayer      → F2P + Battle Pass          │
│  Mobile casual                → F2P + Ads + Light IAP      │
│  MMO / Live service           → Subscription + Cosmetics   │
│  Indie narrative              → Premium + Optional tip jar │
└─────────────────────────────────────────────────────────────┘

ETHICAL PRINCIPLES:
┌─────────────────────────────────────────────────────────────┐
│  ✅ DO:                        ❌ DON'T:                    │
│  • Cosmetics only              • Pay-to-win                 │
│  • Clear pricing               • Hidden costs               │
│  • Earnable alternatives       • Predatory targeting        │
│  • Transparent odds            • Gambling mechanics         │
│  • Respect time/money          • Exploit psychology         │
│  • Value for purchase          • Bait and switch            │
└─────────────────────────────────────────────────────────────┘
```

## IAP Implementation

```csharp
// ✅ Production-Ready: Unity IAP Manager
public class IAPManager : MonoBehaviour, IStoreListener
{
    public static IAPManager Instance { get; private set; }

    private IStoreController _storeController;
    private IExtensionProvider _extensionProvider;

    // Product IDs (match store configuration)
    public const string PRODUCT_STARTER_PACK = "com.game.starterpack";
    public const string PRODUCT_GEMS_100 = "com.game.gems100";
    public const string PRODUCT_BATTLE_PASS = "com.game.battlepass";
    public const string PRODUCT_VIP_SUB = "com.game.vip_monthly";

    public event Action<string> OnPurchaseComplete;
    public event Action<string, string> OnPurchaseFailed;

    private void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);

        InitializePurchasing();
    }

    private void InitializePurchasing()
    {
        var builder = ConfigurationBuilder.Instance(StandardPurchasingModule.Instance());

        // Consumables
        builder.AddProduct(PRODUCT_GEMS_100, ProductType.Consumable);

        // Non-consumables
        builder.AddProduct(PRODUCT_STARTER_PACK, ProductType.NonConsumable);

        // Subscriptions
        builder.AddProduct(PRODUCT_VIP_SUB, ProductType.Subscription);
        builder.AddProduct(PRODUCT_BATTLE_PASS, ProductType.Subscription);

        UnityPurchasing.Initialize(this, builder);
    }

    public void BuyProduct(string productId)
    {
        if (_storeController == null)
        {
            OnPurchaseFailed?.Invoke(productId, "Store not initialized");
            return;
        }

        var product = _storeController.products.WithID(productId);
        if (product != null && product.availableToPurchase)
        {
            _storeController.InitiatePurchase(product);
        }
        else
        {
            OnPurchaseFailed?.Invoke(productId, "Product not available");
        }
    }

    public PurchaseProcessingResult ProcessPurchase(PurchaseEventArgs args)
    {
        var productId = args.purchasedProduct.definition.id;

        // Validate receipt (server-side recommended for security)
        if (ValidateReceipt(args.purchasedProduct.receipt))
        {
            // Grant the purchase
            GrantPurchase(productId);
            OnPurchaseComplete?.Invoke(productId);
        }

        return PurchaseProcessingResult.Complete;
    }

    private void GrantPurchase(string productId)
    {
        switch (productId)
        {
            case PRODUCT_GEMS_100:
                PlayerInventory.AddGems(100);
                break;
            case PRODUCT_STARTER_PACK:
                PlayerInventory.UnlockStarterPack();
                break;
            case PRODUCT_BATTLE_PASS:
                BattlePassManager.Activate();
                break;
        }
    }

    // IStoreListener implementation...
    public void OnInitialized(IStoreController controller, IExtensionProvider extensions)
    {
        _storeController = controller;
        _extensionProvider = extensions;
    }

    public void OnInitializeFailed(InitializationFailureReason error) { }
    public void OnPurchaseFailed(Product product, PurchaseFailureReason reason) { }
}
```

## Battle Pass Design

```
BATTLE PASS STRUCTURE:
┌─────────────────────────────────────────────────────────────┐
│  SEASON LENGTH: 8-12 weeks                                   │
│  TIERS: 100 levels                                           │
│  XP PER TIER: 1000 (increases gradually)                    │
├─────────────────────────────────────────────────────────────┤
│  FREE TRACK:                                                 │
│  • Common rewards every 5 levels                            │
│  • 1-2 rare items mid-season                                │
│  • Currency to buy next pass (partial)                      │
├─────────────────────────────────────────────────────────────┤
│  PREMIUM TRACK ($10):                                        │
│  • Exclusive skin at level 1 (instant value)                │
│  • Premium rewards every level                              │
│  • Legendary items at 25, 50, 75, 100                       │
│  • Enough currency to buy next pass (with effort)           │
├─────────────────────────────────────────────────────────────┤
│  XP SOURCES:                                                 │
│  • Daily challenges: 500 XP                                 │
│  • Weekly challenges: 2000 XP each                          │
│  • Playtime: 50 XP per match                                │
│  • Special events: Bonus XP weekends                        │
└─────────────────────────────────────────────────────────────┘
```

## Economy Design

```
DUAL CURRENCY SYSTEM:
┌─────────────────────────────────────────────────────────────┐
│  SOFT CURRENCY (Gold/Coins):                                 │
│  • Earned through gameplay                                  │
│  • Used for: Upgrades, basic items, consumables             │
│  • Sink: Level-gated purchases, repair costs               │
├─────────────────────────────────────────────────────────────┤
│  HARD CURRENCY (Gems/Diamonds):                              │
│  • Purchased with real money                                │
│  • Small amounts earnable in-game                           │
│  • Used for: Premium cosmetics, time skips                  │
│  • NEVER required for core gameplay                         │
└─────────────────────────────────────────────────────────────┘

PRICING PSYCHOLOGY:
┌─────────────────────────────────────────────────────────────┐
│  $0.99  - Impulse buy, low barrier                          │
│  $4.99  - Starter pack sweet spot                           │
│  $9.99  - Battle pass standard                              │
│  $19.99 - High-value bundles                                │
│  $49.99 - Whale offering (best value/gem)                   │
│  $99.99 - Maximum purchase (regulations)                    │
└─────────────────────────────────────────────────────────────┘
```

## Key Metrics

```
MONETIZATION KPIS:
┌─────────────────────────────────────────────────────────────┐
│  CONVERSION RATE: 2-5% (F2P)                                 │
│  ARPU: $0.05-0.50/DAU (casual mobile)                       │
│  ARPPU: $5-50/paying user                                   │
│  LTV: Should exceed CPI by 1.5x+                            │
├─────────────────────────────────────────────────────────────┤
│  HEALTHY INDICATORS:                                         │
│  ✓ D1 retention > 40%                                       │
│  ✓ D7 retention > 20%                                       │
│  ✓ Conversion > 2%                                          │
│  ✓ LTV/CPI > 1.5                                            │
│  ✓ Refund rate < 5%                                         │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Low conversion rate (< 1%)                         │
├─────────────────────────────────────────────────────────────┤
│ ROOT CAUSES:                                                 │
│ • IAP offers too expensive                                  │
│ • Poor first purchase experience                            │
│ • No perceived value                                        │
│ • Wrong timing                                              │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Add high-value starter pack                               │
│ → Show IAP after engagement hook                            │
│ → A/B test price points                                     │
│ → Improve soft currency scarcity                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: High refund rate (> 10%)                           │
├─────────────────────────────────────────────────────────────┤
│ ROOT CAUSES:                                                 │
│ • Unclear what purchase provides                            │
│ • Buyers remorse (poor value)                               │
│ • Accidental purchases                                      │
│ • Technical issues                                          │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Add purchase confirmation                                 │
│ → Show exactly what user receives                           │
│ → Improve purchase value                                    │
│ → Fix any delivery bugs                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Economy inflation                                  │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Add more currency sinks                                   │
│ → Reduce faucets gradually                                  │
│ → Introduce prestige/reset systems                          │
│ → Create consumable high-end items                          │
└─────────────────────────────────────────────────────────────┘
```

## Compliance

| Region | Requirement |
|--------|-------------|
| EU | Loot box odds disclosure |
| Belgium | No loot boxes |
| China | Odds, spending limits |
| Japan | Kompu gacha banned |
| US | COPPA for under-13 |

---

**Use this skill**: When designing monetization, balancing economy, or implementing purchasing systems.
