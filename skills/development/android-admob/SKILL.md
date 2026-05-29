---
name: android-admob
description: AdMob integration patterns for monetization - banner ads, interstitials, rewarded ads. Use when setting up ads, implementing different ad formats, or testing with test ad units.
license: MIT
version: 1.0.0
---

# Android AdMob Skill

AdMob integration patterns: banner ads, interstitials, rewarded ads.

## When to Use

- Setting up AdMob SDK
- Implementing banner ads
- Adding interstitial ads
- Integrating rewarded ads
- Testing with test ad units

## Setup

### Dependencies

```toml
[libraries]
play-services-ads = { module = "com.google.android.gms:play-services-ads", version = "24.3.0" }
```

### Initialization

```kotlin
// In Application class
MobileAds.initialize(this) { initializationStatus ->
    Timber.d("AdMob initialized: $initializationStatus")
}
```

### AndroidManifest.xml

```xml
<meta-data
    android:name="com.google.android.gms.ads.APPLICATION_ID"
    android:value="ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"/>
```

## Banner Ads

```kotlin
@Composable
fun BannerAd(modifier: Modifier = Modifier) {
    AndroidView(
        modifier = modifier.fillMaxWidth(),
        factory = { context ->
            AdView(context).apply {
                setAdSize(AdSize.BANNER)
                adUnitId = if (BuildConfig.DEBUG) {
                    "ca-app-pub-3940256099942544/6300978111" // Test ID
                } else {
                    BuildConfig.ADMOB_BANNER_ID
                }
                loadAd(AdRequest.Builder().build())
            }
        }
    )
}

// Adaptive banner (recommended)
@Composable
fun AdaptiveBannerAd(modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val windowMetrics = remember {
        WindowMetricsCalculator.getOrCreate().computeCurrentWindowMetrics(context as Activity)
    }
    val adWidth = (windowMetrics.bounds.width() / context.resources.displayMetrics.density).toInt()

    AndroidView(
        modifier = modifier.fillMaxWidth(),
        factory = { ctx ->
            AdView(ctx).apply {
                setAdSize(AdSize.getCurrentOrientationAnchoredAdaptiveBannerAdSize(ctx, adWidth))
                adUnitId = BuildConfig.ADMOB_BANNER_ID
                loadAd(AdRequest.Builder().build())
            }
        }
    )
}
```

## Interstitial Ads

```kotlin
class InterstitialAdManager(private val context: Context) {
    private var interstitialAd: InterstitialAd? = null

    fun loadAd() {
        val adRequest = AdRequest.Builder().build()
        val adUnitId = if (BuildConfig.DEBUG) {
            "ca-app-pub-3940256099942544/1033173712"
        } else {
            BuildConfig.ADMOB_INTERSTITIAL_ID
        }

        InterstitialAd.load(context, adUnitId, adRequest) { ad, error ->
            if (error != null) {
                Timber.e("Interstitial failed to load: ${error.message}")
                return@load
            }
            interstitialAd = ad
        }
    }

    fun showAd(activity: Activity, onDismissed: () -> Unit) {
        interstitialAd?.apply {
            fullScreenContentCallback = object : FullScreenContentCallback() {
                override fun onAdDismissedFullScreenContent() {
                    interstitialAd = null
                    onDismissed()
                    loadAd() // Preload next
                }
                override fun onAdFailedToShowFullScreenContent(error: AdError) {
                    interstitialAd = null
                    onDismissed()
                }
            }
            show(activity)
        } ?: onDismissed()
    }

    fun isLoaded(): Boolean = interstitialAd != null
}
```

## Rewarded Ads

```kotlin
class RewardedAdManager(private val context: Context) {
    private var rewardedAd: RewardedAd? = null

    fun loadAd() {
        val adRequest = AdRequest.Builder().build()
        val adUnitId = if (BuildConfig.DEBUG) {
            "ca-app-pub-3940256099942544/5224354917"
        } else {
            BuildConfig.ADMOB_REWARDED_ID
        }

        RewardedAd.load(context, adUnitId, adRequest) { ad, error ->
            if (error != null) {
                Timber.e("Rewarded ad failed to load: ${error.message}")
                return@load
            }
            rewardedAd = ad
        }
    }

    fun showAd(activity: Activity, onRewarded: (RewardItem) -> Unit, onDismissed: () -> Unit) {
        rewardedAd?.apply {
            fullScreenContentCallback = object : FullScreenContentCallback() {
                override fun onAdDismissedFullScreenContent() {
                    rewardedAd = null
                    onDismissed()
                    loadAd() // Preload next
                }
            }
            show(activity) { reward ->
                onRewarded(reward)
            }
        } ?: onDismissed()
    }

    fun isLoaded(): Boolean = rewardedAd != null
}
```

## Test Ad Units (Use in Debug)

| Type | Test ID |
|------|---------|
| App Open | ca-app-pub-3940256099942544/9257395921 |
| Banner | ca-app-pub-3940256099942544/6300978111 |
| Interstitial | ca-app-pub-3940256099942544/1033173712 |
| Interstitial Video | ca-app-pub-3940256099942544/8691691433 |
| Rewarded | ca-app-pub-3940256099942544/5224354917 |
| Rewarded Interstitial | ca-app-pub-3940256099942544/5354046379 |
| Native | ca-app-pub-3940256099942544/2247696110 |

## Version Compatibility

| Play Services Ads | Min SDK | Target SDK |
|-------------------|---------|------------|
| 24.x | 21 | 35 |
| 23.x | 21 | 34 |
| 22.x | 19 | 33 |

## Error Handling

```kotlin
// Ad load error handling
InterstitialAd.load(context, adUnitId, adRequest) { ad, error ->
    if (error != null) {
        when (error.code) {
            AdRequest.ERROR_CODE_NETWORK_ERROR ->
                Timber.w("Network unavailable for ads")
            AdRequest.ERROR_CODE_NO_FILL ->
                Timber.d("No ad inventory available")
            AdRequest.ERROR_CODE_INTERNAL_ERROR ->
                Timber.e("AdMob internal error")
            else -> Timber.w("Ad error: ${error.message}")
        }
        return@load
    }
    interstitialAd = ad
}

// Show ad with fallback
fun showAdOrContinue(activity: Activity, onComplete: () -> Unit) {
    if (interstitialAd != null) {
        interstitialAd?.show(activity)
    } else {
        Timber.d("Ad not ready, continuing without ad")
        onComplete()
    }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No fill | Normal - try again later, use mediation |
| Test ads only | Check ad unit ID, device registration |
| Clicks not counting | Verify no overlapping views |
| Policy violation | Review ad placement, content |

## Security Checklist

- [ ] Test IDs in BuildConfig.DEBUG
- [ ] Production IDs in BuildConfig.RELEASE
- [ ] No hardcoded ad unit IDs
- [ ] Consent management (GDPR/CCPA)
- [ ] App-ads.txt configured

## Best Practices

- Always use test IDs in debug builds
- Preload ads before showing
- Handle ad not available gracefully
- Don't show ads too frequently
- Follow AdMob policies strictly
- Implement proper error handling
- Consider user experience first

## AdMob Policies Checklist

- [ ] No accidental clicks (proper spacing)
- [ ] No incentivizing clicks
- [ ] No misleading ad placement
- [ ] Proper ad labeling
- [ ] No pop-ups or full-screen ads without user action
- [ ] Content policy compliance

## References

- [AdMob Quick Start](https://developers.google.com/admob/android/quick-start)
- [AdMob Policies](https://support.google.com/admob/answer/6128543)
- [Test Ads](https://developers.google.com/admob/android/test-ads)
- [Mediation](https://developers.google.com/admob/android/mediation)

Use this skill for ethical, effective monetization.
