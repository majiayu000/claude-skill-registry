---
name: app-store-review
description: "Prepare for App Store review and prevent rejections. Covers App Store review guidelines, app rejection reasons, PrivacyInfo.xcprivacy privacy manifest requirements, required API reason codes, in-app purchase IAP and StoreKit rules, App Store Guidelines compliance, ATT App Tracking Transparency, EU DMA Digital Markets Act, HIG compliance checklist, app submission preparation, review preparation, metadata requirements, entitlements, widgets, and Live Activities review rules. Use when preparing for App Store submission, fixing rejection reasons, auditing privacy manifests, implementing ATT consent flow, configuring StoreKit IAP, or checking HIG compliance."
---

# App Store Review Preparation

Guidance for catching App Store rejection risks before submission. Apple reviewed 7.7 million submissions in 2024 and rejected 1.9 million. Most rejections are preventable with proper preparation.

## Contents

- [Overview](#overview)
- [Top Rejection Reasons and How to Avoid Them](#top-rejection-reasons-and-how-to-avoid-them)
- [PrivacyInfo.xcprivacy -- Privacy Manifest Requirements](#privacyinfoxcprivacy-privacy-manifest-requirements)
- [Data Use, Sharing, and Privacy Policy (Guideline 5.1.2)](#data-use-sharing-and-privacy-policy-guideline-512)
- [In-App Purchase and StoreKit Rules (Guideline 3.1.1)](#in-app-purchase-and-storekit-rules-guideline-311)
- [HIG Compliance Checklist](#hig-compliance-checklist)
- [App Tracking Transparency (ATT)](#app-tracking-transparency-att)
- [EU Digital Markets Act (DMA) Considerations](#eu-digital-markets-act-dma-considerations)
- [Entitlements and Capabilities](#entitlements-and-capabilities)
- [Submission Workflow](#submission-workflow)
- [Metadata Best Practices](#metadata-best-practices)
- [Appeal Process](#appeal-process)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Overview

Use this SKILL.md for quick guidance on common rejection reasons and key policies. Use the references for detailed checklists and privacy manifest specifics.

## Top Rejection Reasons and How to Avoid Them

### Guideline 2.1 -- App Completeness

The app must be fully functional when reviewed. Apple rejects for:

- Placeholder content, lorem ipsum, or test data visible anywhere
- Broken links or empty screens
- Features behind logins without demo credentials provided in App Review notes
- Features that require hardware Apple does not have access to

**Prevention:**
- Provide demo account credentials in the App Review Information notes field in App Store Connect
- Walk through every screen and verify real content is present
- Test all flows end-to-end, including edge cases like empty states and error conditions

### Guideline 2.3 -- Accurate Metadata

- App name must match what the app actually does
- Screenshots must show the actual app UI, not marketing renders or mockups
- Description must not contain prices (they vary by region)
- No references to other platforms ("Also available on Android")
- Keywords must be relevant -- no competitor names or unrelated terms
- Category must match the app's primary function

### Guideline 4.2 -- Minimum Functionality

Apple rejects apps that are too simple or are just websites in a wrapper:

- WKWebView-only apps are rejected unless they add meaningful native functionality
- Single-feature apps may be rejected if the feature is better suited as part of another app
- Apps that duplicate built-in iOS functionality without significant improvement are rejected

### Guideline 2.5.1 -- Software Requirements

- Must use public APIs only -- private API usage is an instant rejection
- Must be built with the current Xcode GM release or later
- Must support the latest two major iOS versions (guideline, not strict rule)
- Must not download or execute code dynamically (except JavaScript in WKWebView)

## PrivacyInfo.xcprivacy -- Privacy Manifest Requirements

This is the fastest-growing rejection category (Guideline 5.1.1). A privacy manifest is **required** if your app or any of its dependencies uses certain categories of APIs.

**See:** `references/privacy-manifest.md` for the full structure, reason codes, and checklists.

### Summary

- File timestamp, system boot time, disk space, user defaults, and active keyboard APIs all require reason codes.
- Every third-party SDK must ship its own privacy manifest.
- Manifest declarations must match App Store privacy nutrition labels and actual network behavior.

## Data Use, Sharing, and Privacy Policy (Guideline 5.1.2)

- A privacy policy URL must be set in App Store Connect AND accessible within the app
- The privacy policy must accurately describe what data you collect, how you use it, and who you share it with
- App Store privacy nutrition labels must match your actual data collection practices
- Apple cross-references your privacy manifest, nutrition labels, and observed network traffic

## In-App Purchase and StoreKit Rules (Guideline 3.1.1)

IAP rules are strict and heavily enforced.

### What Requires Apple IAP

All digital content and services must use Apple's In-App Purchase system:

- Premium features or content unlocks
- Subscriptions to app functionality
- Virtual currency, coins, gems
- Ad removal
- Digital tips or donations

### What Does NOT Require IAP

- Physical products (e-commerce)
- Ride-sharing, food delivery, real-world services
- One-to-one services (tutoring, consulting booked through the app)
- Enterprise/B2B apps distributed through Apple Business Manager

### Subscription Display Requirements

- Price, duration, and auto-renewal terms must be clearly displayed before purchase
- Free trials must state what happens when they end (price, billing frequency)
- No links, buttons, or language directing users to purchase outside the app
- "Reader" apps (Netflix, Spotify) may link to external sign-up but cannot offer IAP bypass

### StoreKit Implementation Checklist

- Consumables, non-consumables, and subscriptions must be correctly categorized in App Store Connect
- Restore purchases functionality must be present and working
- Transaction verification should use StoreKit 2 `Transaction.currentEntitlements` or server-side validation
- Handle interrupted purchases, deferred transactions, and ask-to-buy gracefully

## HIG Compliance Checklist

See `references/review-checklists.md` for the full HIG checklist (navigation, modals, widgets, system feature support, launch screen, empty states). This section stays intentionally brief to keep SKILL.md concise.

## App Tracking Transparency (ATT)

### When ATT Is Required

If your app tracks users across other companies' apps or websites, you must:

1. Request permission via `ATTrackingManager.requestTrackingAuthorization` before any tracking occurs
2. Respect the user's choice -- do not track if the user denies permission
3. Not gate app functionality behind tracking consent ("Accept tracking or you cannot use this app" is rejected)
4. Provide a clear purpose string in `NSUserTrackingUsageDescription` explaining what tracking is used for

### When ATT Is NOT Required

If you do not track users across apps or websites, do not show the ATT prompt. Apple rejects unnecessary ATT prompts.

### ATT Implementation

```swift
import AppTrackingTransparency

func requestTrackingPermission() async {
    let status = await ATTrackingManager.requestTrackingAuthorization()
    switch status {
    case .authorized:
        // Enable tracking, initialize ad SDKs with tracking
        break
    case .denied, .restricted:
        // Use non-personalized ads, disable cross-app tracking
        break
    case .notDetermined:
        // Should not happen after request, handle gracefully
        break
    @unknown default:
        break
    }
}
```

**Timing:** Request ATT permission after the app has launched and the user has context for why tracking is being requested. Do not show the prompt immediately on first launch.

## EU Digital Markets Act (DMA) Considerations

For apps distributed in the EU:

- Alternative browser engines are permitted on iOS in the EU
- Alternative app marketplaces exist -- apps may be distributed outside the App Store
- External payment links may be allowed under specific conditions, with Apple's commission structure adjusted
- Notarization is required even for sideloaded apps distributed outside the App Store
- Apps using alternative distribution must still meet Apple's notarization requirements for security

## Entitlements and Capabilities

Every entitlement must be justified. Apple reviews these closely:

| Entitlement | Apple Scrutiny |
|---|---|
| Camera | Must explain purpose in `NSCameraUsageDescription` |
| Location (Always) | Must have clear, user-visible reason for background location |
| Push Notifications | Must not be used for marketing without user opt-in |
| HealthKit | Must actually use health data in a meaningful way |
| Background Modes | Each mode (audio, location, VoIP, fetch) must be justified and actively used |
| App Groups | Must explain what shared data is needed |
| Associated Domains | Universal links must actually resolve and function |

### Usage Description Strings

Usage descriptions in Info.plist must be specific about what data is accessed and why:

```xml
// REJECTED -- too vague

// APPROVED -- specific purpose
"Your location is used to show nearby restaurants on the map."

// REJECTED -- too vague
"This app needs access to your camera."

// APPROVED -- specific purpose
"The camera is used to scan barcodes for price comparison."
```

Apple rejects vague usage descriptions. Always state what the data is used for in user-facing terms.

## Submission Workflow

### Pre-Submission Steps

1. **Archive in Xcode.** Product > Archive (requires a Distribution signing identity). Verify the archive builds clean with zero warnings in Release configuration.
2. **Upload to App Store Connect.** Use the Organizer window (Distribute App > App Store Connect) or `xcodebuild -exportArchive`. Automated uploads via `altool` or Transporter also work.
3. **TestFlight internal testing.** The build is available to internal testers (your team) within minutes of processing. Walk through every screen and flow on at least two device sizes.
4. **TestFlight external testing.** External groups require a brief Beta App Review (usually < 24 hours). Use this to validate with real users before full submission.
5. **Submit for App Review.** In App Store Connect, select the build, fill in all metadata fields, attach screenshots, and click Submit for Review. Average review time is under 24 hours, but allow 48 hours.

### Expedited Review Requests

Apple grants expedited reviews for critical situations only:

- Critical bug fix affecting existing users
- Time-sensitive event (holiday launch, legal compliance deadline)
- Security vulnerability patch

Request via the Contact Us form in App Store Connect (App Review > Expedite Request). Provide a specific, factual justification. Do not request expedited review for initial launches or feature updates.

### Phased Release

After approval, you can enable phased release to gradually roll out the update:

| Day | Percentage of Users |
|-----|---------------------|
| 1   | 1%                  |
| 2   | 2%                  |
| 3   | 5%                  |
| 4   | 10%                 |
| 5   | 20%                 |
| 6   | 50%                 |
| 7   | 100%                |

Users who manually check for updates in the App Store will receive the update immediately regardless of phased release stage. You can pause, resume, or complete the rollout at any time from App Store Connect.

## Metadata Best Practices

### App Name and Subtitle

- **30 characters max** for the app name. Keep it memorable and unique.
- **30 characters max** for the subtitle. Use it for a concise value proposition.
- No generic terms that describe a category ("Photo Editor" alone is likely rejected).
- No competitor names or trademarked terms you do not own.
- No pricing information in the name or subtitle.
- Name must be unique on the App Store -- Apple rejects duplicates.

### Screenshot Requirements

- Provide screenshots for every required device size (6.9", 6.7", 6.5", 5.5" for iPhone; 13" for iPad if supporting iPad).
- Screenshots must show the **actual app UI** -- no misleading content, no features that do not exist.
- Text overlays and marketing frames are allowed but must not obscure or misrepresent the actual interface.
- Up to 10 screenshots per localization. Lead with your most compelling screen.
- Screenshots for different localizations should show localized UI.

### Keywords Optimization

- 100-character limit, comma-separated, no spaces after commas.
- Do not duplicate words already in your app name or subtitle (Apple indexes those automatically).
- Use singular or plural, not both ("game" not "game,games").
- No competitor names, trademarked terms, or irrelevant words.
- Place highest-value keywords first.
- Update keywords with each release based on Search Ads and analytics data.

### App Preview Videos

- **30 seconds max** per preview video.
- Up to 3 preview videos per localization.
- Must show the actual app running on device -- no pre-rendered animations of features that look different in practice.
- App audio is captured; narration and background music are optional.
- No device frames or hands unless showing real device interaction.
- First frame is used as the poster frame on the product page (choose carefully).

## Appeal Process

### Replying to Rejections

All rejections appear in the **Resolution Center** in App Store Connect. To respond:

1. Read the rejection message carefully -- it cites the specific guideline violated.
2. Reply directly in the Resolution Center thread with a clear, factual explanation.
3. If you made a fix, describe exactly what changed and resubmit the binary.
4. If you believe the rejection is incorrect, explain why your app complies, with references to the specific guideline text.

**Tone matters.** Be professional, specific, and concise. Provide demo credentials, screenshots, or screen recordings that demonstrate compliance. Avoid emotional language or threats.

### Escalation to App Review Board

If the Resolution Center exchange does not resolve the issue:

1. Request an appeal to the **App Review Board** via the Resolution Center or the App Store Contact form (App Review > Appeal).
2. The Board is a separate team from the original reviewer. Provide all context -- they review the full history.
3. Board decisions are final for that submission, but you can always modify the app and resubmit.

### Common Successful Appeal Strategies

- **Provide a video walkthrough** showing the feature the reviewer could not find or access.
- **Cite the specific guideline** and explain how the app satisfies each requirement.
- **Include demo credentials** if the reviewer could not log in (the most common 2.1 rejection cause).
- **Reference precedent** -- if similar apps exist on the App Store with the same pattern, note them (respectfully).
- **Offer a compromise** -- if Apple objects to a specific implementation, propose an alternative that satisfies both sides.

## Common Mistakes

1. **Missing demo credentials.** Provide App Review login credentials in App Store Connect notes. Most Guideline 2.1 rejections are from reviewers unable to test behind a login.
2. **Privacy manifest mismatch.** Declared data collection in PrivacyInfo.xcprivacy must match App Store privacy nutrition labels and actual network traffic.
3. **Unnecessary ATT prompt.** Do not show the App Tracking Transparency prompt unless you actually track users across apps or websites. Apple rejects unnecessary prompts.
4. **Vague usage descriptions.** "This app needs your location" is rejected. State the specific feature that uses the data.
5. **External payment links for digital content.** Any language or button directing users to purchase digital content outside the app is rejected.
6. **Missing concurrency annotations.** Ensure ATT request and StoreKit calls run on `@MainActor` or appropriate actor context. Mark shared state types as `Sendable` for Swift 6 concurrency safety.

## Review Checklist

Quick-check before every submission (full version in `references/review-checklists.md`):

- [ ] No placeholder/test content; all features functional; demo credentials provided
- [ ] App name matches functionality; screenshots are real; no prices in description
- [ ] PrivacyInfo.xcprivacy present with reason codes; nutrition labels match reality
- [ ] Privacy policy URL set and accessible in-app
- [ ] Digital content uses IAP; subscription terms visible; restore purchases works
- [ ] Dark Mode and Dynamic Type supported; standard navigation patterns
- [ ] Built with current Xcode GM; no private APIs; entitlements justified
- [ ] ATT prompt only if cross-app tracking occurs

## References

- Review checklists: `references/review-checklists.md`
- Privacy manifest guide: `references/privacy-manifest.md`
