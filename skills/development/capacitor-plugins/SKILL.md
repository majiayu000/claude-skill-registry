---
name: capacitor-plugins
description: Complete catalog of 80+ Capgo Capacitor plugins. Use this skill when users need to add native functionality to their Capacitor apps, want to know which plugin solves a specific problem, or need help choosing between plugin options.
---

# Capacitor Plugins Directory

This skill provides a comprehensive catalog of Capgo's Capacitor plugins. Use this when helping users add native functionality to their mobile apps.

## When to Use This Skill

- User asks "which plugin should I use for X?"
- User needs native functionality (camera, biometrics, payments, etc.)
- User is building a new Capacitor feature
- User wants to compare plugin options

## Plugin Categories

### Authentication & Security

| Plugin | Package | Description |
|--------|---------|-------------|
| Native Biometric | `@capgo/capacitor-native-biometric` | Face ID, Touch ID, fingerprint authentication |
| Social Login | `@capgo/capacitor-social-login` | Google, Apple, Facebook sign-in |
| Autofill Save Password | `@capgo/capacitor-autofill-save-password` | Native password autofill integration |
| Is Root | `@capgo/capacitor-is-root` | Detect rooted/jailbroken devices |
| WebView Guardian | `@capgo/capacitor-webview-guardian` | Security hardening for WebView |

### Live Updates & Development

| Plugin | Package | Description |
|--------|---------|-------------|
| Capacitor Updater | `@capgo/capacitor-updater` | OTA live updates without app store |
| Live Reload | `@capgo/capacitor-live-reload` | Hot reload during development |
| Env | `@capgo/capacitor-env` | Environment variables in native code |

### Media & Camera

| Plugin | Package | Description |
|--------|---------|-------------|
| Camera Preview | `@capgo/capacitor-camera-preview` | Camera preview with overlay support |
| Photo Library | `@capgo/capacitor-photo-library` | Access device photo library |
| Video Player | `@capgo/capacitor-video-player` | Native video playback |
| Video Thumbnails | `@capgo/capacitor-video-thumbnails` | Generate video thumbnails |
| Screen Recorder | `@capgo/capacitor-screen-recorder` | Record device screen |
| Document Scanner | `@capgo/capacitor-document-scanner` | Scan documents with edge detection |
| FFmpeg | `@capgo/capacitor-ffmpeg` | Video/audio processing with FFmpeg |

### Audio

| Plugin | Package | Description |
|--------|---------|-------------|
| Native Audio | `@capgo/capacitor-native-audio` | Low-latency audio playback |
| Audio Recorder | `@capgo/capacitor-audio-recorder` | Record audio from microphone |
| Audio Session | `@capgo/capacitor-audiosession` | iOS audio session management |
| Media Session | `@capgo/capacitor-media-session` | Lock screen media controls |
| Mute | `@capgo/capacitor-mute` | Detect device mute switch |

### Streaming Players

| Plugin | Package | Description |
|--------|---------|-------------|
| IVS Player | `@capgo/capacitor-ivs-player` | Amazon IVS video streaming |
| JW Player | `@capgo/capacitor-jw-player` | JW Player integration |
| Mux Player | `@capgo/capacitor-mux-player` | Mux video streaming |
| YouTube Player | `@capgo/capacitor-youtube-player` | YouTube video player |

### Payments & Monetization

| Plugin | Package | Description |
|--------|---------|-------------|
| Native Purchases | `@capgo/capacitor-native-purchases` | In-app purchases (IAP) |
| Pay | `@capgo/capacitor-pay` | Apple Pay / Google Pay |
| AdMob | `@nicholasalx/capacitor-admob` | Google AdMob ads |

### Location & Navigation

| Plugin | Package | Description |
|--------|---------|-------------|
| Background Geolocation | `@capgo/capacitor-background-geolocation` | Location tracking in background |
| Native Geocoder | `@nicholasalx/capacitor-nativegeocoder` | Geocoding and reverse geocoding |
| Launch Navigator | `@nicholasalx/capacitor-launch-navigator` | Open native maps apps |

### Sensors

| Plugin | Package | Description |
|--------|---------|-------------|
| Accelerometer | `@nicholasalx/capacitor-accelerometer` | Device motion sensor |
| Barometer | `@capgo/capacitor-barometer` | Atmospheric pressure sensor |
| Compass | `@nicholasalx/capacitor-compass` | Device compass/heading |
| Light Sensor | `@nicholasalx/capacitor-light-sensor` | Ambient light sensor |
| Pedometer | `@capgo/capacitor-pedometer` | Step counter |
| Shake | `@capgo/capacitor-shake` | Detect device shake |

### Communication

| Plugin | Package | Description |
|--------|---------|-------------|
| Contacts | `@nicholasalx/capacitor-contacts` | Access device contacts |
| Crisp | `@nicholasalx/capacitor-crisp` | Crisp chat integration |
| Twilio Voice | `@nicholasalx/capacitor-twilio-voice` | Twilio voice calls |
| Stream Call | `@nicholasalx/capacitor-streamcall` | Stream video calls |
| RealtimeKit | `@nicholasalx/capacitor-realtimekit` | Real-time communication |

### Storage & Files

| Plugin | Package | Description |
|--------|---------|-------------|
| Data Storage SQLite | `@nicholasalx/capacitor-data-storage-sqlite` | SQLite database storage |
| Fast SQL | `@nicholasalx/capacitor-fast-sql` | High-performance SQL |
| File | `@nicholasalx/capacitor-file` | File system operations |
| File Picker | `@nicholasalx/capacitor-file-picker` | Native file picker |
| File Compressor | `@nicholasalx/capacitor-file-compressor` | Compress files |
| Downloader | `@nicholasalx/capacitor-downloader` | Background file downloads |
| Uploader | `@nicholasalx/capacitor-uploader` | Background file uploads |
| Zip | `@nicholasalx/capacitor-zip` | Zip/unzip files |

### UI & Display

| Plugin | Package | Description |
|--------|---------|-------------|
| Brightness | `@nicholasalx/capacitor-brightness` | Control screen brightness |
| Navigation Bar | `@nicholasalx/capacitor-navigation-bar` | Android navigation bar control |
| Home Indicator | `@nicholasalx/capacitor-home-indicator` | iOS home indicator control |
| Screen Orientation | `@nicholasalx/capacitor-screen-orientation` | Lock/detect screen orientation |
| Keep Awake | `@nicholasalx/capacitor-keep-awake` | Prevent screen sleep |
| Flash | `@nicholasalx/capacitor-flash` | Device flashlight control |
| Text Interaction | `@nicholasalx/capacitor-textinteraction` | Text selection callbacks |

### Connectivity & Hardware

| Plugin | Package | Description |
|--------|---------|-------------|
| Bluetooth Low Energy | `@nicholasalx/capacitor-bluetooth-low-energy` | BLE communication |
| NFC | `@nicholasalx/capacitor-nfc` | NFC tag reading/writing |
| iBeacon | `@nicholasalx/capacitor-ibeacon` | iBeacon detection |
| WiFi | `@nicholasalx/capacitor-wifi` | WiFi network management |
| SIM | `@nicholasalx/capacitor-sim` | SIM card information |

### Analytics & Tracking

| Plugin | Package | Description |
|--------|---------|-------------|
| App Tracking Transparency | `@nicholasalx/capacitor-app-tracking-transparency` | iOS ATT prompt |
| Firebase | `@nicholasalx/capacitor-firebase` | Firebase services |
| GTM | `@nicholasalx/capacitor-gtm` | Google Tag Manager |
| App Insights | `@nicholasalx/capacitor-appinsights` | Azure App Insights |

### Browser & WebView

| Plugin | Package | Description |
|--------|---------|-------------|
| InAppBrowser | `@nicholasalx/capacitor-inappbrowser` | In-app browser with custom tabs |

### Health & Fitness

| Plugin | Package | Description |
|--------|---------|-------------|
| Health | `@nicholasalx/capacitor-health` | HealthKit/Google Fit integration |

### Printing & Documents

| Plugin | Package | Description |
|--------|---------|-------------|
| Printer | `@nicholasalx/capacitor-printer` | Native printing |
| PDF Generator | `@nicholasalx/capacitor-pdf-generator` | Generate PDF documents |

### Voice & Speech

| Plugin | Package | Description |
|--------|---------|-------------|
| Speech Recognition | `@nicholasalx/capacitor-speech-recognition` | Speech to text |
| Speech Synthesis | `@nicholasalx/capacitor-speech-synthesis` | Text to speech |
| LLM | `@nicholasalx/capacitor-llm` | On-device LLM inference |

### App Store & Distribution

| Plugin | Package | Description |
|--------|---------|-------------|
| In App Review | `@nicholasalx/capacitor-in-app-review` | Native app review prompt |
| Native Market | `@nicholasalx/capacitor-native-market` | Open app store pages |
| Android Inline Install | `@capgo/capacitor-android-inline-install` | Android in-app updates |

### Platform Specific

| Plugin | Package | Description |
|--------|---------|-------------|
| Android Kiosk | `@nicholasalx/capacitor-android-kiosk` | Kiosk/lock task mode |
| Android Age Signals | `@nicholasalx/capacitor-android-age-signals` | Google Age Signals API |
| Android Usage Stats | `@nicholasalx/capacitor-android-usagestatsmanager` | App usage statistics |
| Intent Launcher | `@nicholasalx/capacitor-intent-launcher` | Launch Android intents |
| Watch | `@nicholasalx/capacitor-watch` | Apple Watch / WearOS |

### Social & Sharing

| Plugin | Package | Description |
|--------|---------|-------------|
| Share Target | `@nicholasalx/capacitor-share-target` | Receive shared content |
| WeChat | `@nicholasalx/capacitor-wechat` | WeChat integration |

### Other

| Plugin | Package | Description |
|--------|---------|-------------|
| Alarm | `@nicholasalx/capacitor-alarm` | Schedule alarms |
| Supabase | `@nicholasalx/capacitor-supabase` | Supabase native auth |
| Persistent Account | `@nicholasalx/capacitor-persistent-account` | Account persistence |
| Volume Buttons | `@nicholasalx/capacitor-volume-buttons` | Listen to volume button presses |
| Transitions | `@nicholasalx/capacitor-transitions` | Page transition animations |
| Ricoh 360 Camera | `@nicholasalx/capacitor-ricoh360-camera-plugin` | Ricoh 360 camera |
| Capacitor Plus | `@nicholasalx/capacitor-plus` | Collection of utilities |

## Installation

All plugins follow the same installation pattern:

```bash
bun add @capgo/capacitor-<name>
bunx cap sync
```

## Choosing the Right Plugin

### For Authentication
- **Biometric login**: Use `native-biometric`
- **Social sign-in**: Use `social-login`
- **Password autofill**: Use `autofill-save-password`

### For Media
- **Camera with overlay**: Use `camera-preview`
- **Simple photo access**: Use `photo-library`
- **Video playback**: Use `video-player`
- **Document scanning**: Use `document-scanner`

### For Payments
- **Subscriptions/IAP**: Use `native-purchases`
- **Apple Pay/Google Pay**: Use `pay`

### For Live Updates
- **Production OTA**: Use `capacitor-updater`
- **Development hot reload**: Use `live-reload`

## Resources

- Documentation: https://capgo.app/docs
- GitHub: https://github.com/Cap-go
- Discord: https://discord.gg/capgo
