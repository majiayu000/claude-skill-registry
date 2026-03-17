---
description: Capacitor and Ionic expert for web-to-mobile development. Capacitor 6+ architecture, Ionic Framework with Angular/React/Vue, native API access, custom plugins, live reload, Appflow, PWA support. Use for Capacitor projects, Ionic apps, Cordova migration, or web-to-native decisions. Activates for: Capacitor, Ionic, Cordova, web-to-mobile, hybrid app, Appflow, Ionic Framework, Capacitor plugin, native bridge, web-to-native.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# Capacitor / Ionic Expert

Comprehensive expertise in **Capacitor 6+** and **Ionic Framework** for building cross-platform mobile applications from web technologies. Covers architecture, native API access, custom plugin development, deployment, and when to choose Capacitor over React Native or Flutter.

## Fetching Current Documentation

**Before providing version-specific guidance, verify current versions.** Capacitor releases frequently, and plugin APIs evolve. Always verify current APIs before recommending specific patterns.

For library documentation, use WebSearch or install Context7 manually: `claude plugin install context7@claude-plugins-official`

## Capacitor 6+ Architecture

### How Capacitor Works

```
┌──────────────────────────────────────────────────┐
│                  Your Web App                     │
│          (Angular / React / Vue / Vanilla)        │
├──────────────────────────────────────────────────┤
│              Capacitor Bridge                     │
│    (Message passing between JS and Native)        │
├─────────────────────┬────────────────────────────┤
│   iOS (WKWebView)   │   Android (WebView)        │
│   Swift / ObjC      │   Kotlin / Java            │
│   Native APIs       │   Native APIs              │
└─────────────────────┴────────────────────────────┘
```

**Key architectural principles:**
- Your web app runs in a native WebView (WKWebView on iOS, Android WebView)
- Capacitor provides a bridge to call native APIs from JavaScript
- Native code is a first-class citizen -- you own the Xcode and Android Studio projects
- Plugins provide the abstraction layer between JS and native

### Project Structure

```
my-app/
├── src/                     # Web app source (Angular/React/Vue)
├── ios/                     # Native iOS project (Xcode)
│   └── App/
│       ├── App/
│       │   ├── AppDelegate.swift
│       │   ├── capacitor.config.json
│       │   └── public/      # Built web assets copied here
│       └── App.xcworkspace
├── android/                 # Native Android project
│   └── app/
│       ├── src/main/
│       │   ├── java/.../MainActivity.java
│       │   └── assets/public/  # Built web assets copied here
│       └── build.gradle.kts
├── capacitor.config.ts      # Capacitor configuration
├── package.json
└── ionic.config.json        # If using Ionic CLI
```

### Capacitor Configuration

```typescript
// capacitor.config.ts
import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.example.myapp',
  appName: 'My App',
  webDir: 'dist',  // or 'www' for Angular
  server: {
    androidScheme: 'https',  // Required for cookies, secure context
    iosScheme: 'capacitor',
    hostname: 'app.example.com',
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      launchAutoHide: true,
      backgroundColor: '#ffffff',
      androidSplashResourceName: 'splash',
      showSpinner: false,
    },
    PushNotifications: {
      presentationOptions: ['badge', 'sound', 'alert'],
    },
    Keyboard: {
      resize: 'body',
      resizeOnFullScreen: true,
    },
  },
  ios: {
    contentInset: 'automatic',
    preferredContentMode: 'mobile',
  },
  android: {
    allowMixedContent: false,
    captureInput: true,
    webContentsDebuggingEnabled: false,  // Set true for debug builds
  },
};

export default config;
```

### Project Setup

```bash
# New Ionic + Capacitor project
npm install -g @ionic/cli
ionic start myApp tabs --type=angular --capacitor

# Add Capacitor to existing web project
npm install @capacitor/core @capacitor/cli
npx cap init "My App" com.example.myapp --web-dir dist

# Add platforms
npx cap add ios
npx cap add android

# Build and sync
npm run build
npx cap sync  # Copies web assets + updates native dependencies

# Open native IDE
npx cap open ios
npx cap open android
```

## Ionic Framework Integration

### Angular Integration

```typescript
// app.module.ts
import { IonicModule } from '@ionic/angular';

@NgModule({
  imports: [
    BrowserModule,
    IonicModule.forRoot({
      mode: 'ios',  // Force iOS styling everywhere, or 'md' for Material
      animated: true,
      rippleEffect: true,
    }),
    AppRoutingModule,
  ],
})
export class AppModule {}
```

```html
<!-- home.page.html -->
<ion-header>
  <ion-toolbar>
    <ion-title>Products</ion-title>
    <ion-buttons slot="end">
      <ion-button (click)="openCart()">
        <ion-icon name="cart-outline" slot="icon-only"></ion-icon>
        <ion-badge *ngIf="cartCount > 0">{{ cartCount }}</ion-badge>
      </ion-button>
    </ion-buttons>
  </ion-toolbar>
</ion-header>

<ion-content>
  <ion-refresher slot="fixed" (ionRefresh)="refresh($event)">
    <ion-refresher-content></ion-refresher-content>
  </ion-refresher>

  <ion-list>
    <ion-item *ngFor="let product of products" (click)="viewProduct(product)">
      <ion-thumbnail slot="start">
        <img [src]="product.image" [alt]="product.name" />
      </ion-thumbnail>
      <ion-label>
        <h2>{{ product.name }}</h2>
        <p>{{ product.price | currency }}</p>
      </ion-label>
      <ion-button slot="end" fill="clear" (click)="addToCart(product, $event)">
        <ion-icon name="add-circle-outline" slot="icon-only"></ion-icon>
      </ion-button>
    </ion-item>
  </ion-list>

  <ion-infinite-scroll (ionInfinite)="loadMore($event)">
    <ion-infinite-scroll-content loadingSpinner="dots"></ion-infinite-scroll-content>
  </ion-infinite-scroll>
</ion-content>
```

### React Integration

```tsx
// App.tsx
import { IonApp, IonRouterOutlet, setupIonicReact } from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';

setupIonicReact({ mode: 'ios' });

const App: React.FC = () => (
  <IonApp>
    <IonReactRouter>
      <IonRouterOutlet>
        <Route exact path="/home" component={Home} />
        <Route exact path="/product/:id" component={ProductDetail} />
        <Redirect exact from="/" to="/home" />
      </IonRouterOutlet>
    </IonReactRouter>
  </IonApp>
);
```

```tsx
// ProductList.tsx
import {
  IonContent, IonHeader, IonList, IonItem, IonLabel,
  IonRefresher, IonRefresherContent, IonSearchbar,
} from '@ionic/react';

const ProductList: React.FC = () => {
  const [searchText, setSearchText] = useState('');
  const [products, setProducts] = useState<Product[]>([]);

  const handleRefresh = async (event: CustomEvent) => {
    await fetchProducts();
    event.detail.complete();
  };

  return (
    <IonContent>
      <IonSearchbar
        value={searchText}
        onIonInput={(e) => setSearchText(e.detail.value!)}
        debounce={300}
      />
      <IonRefresher slot="fixed" onIonRefresh={handleRefresh}>
        <IonRefresherContent />
      </IonRefresher>
      <IonList>
        {products.map((product) => (
          <IonItem key={product.id} routerLink={`/product/${product.id}`}>
            <IonLabel>
              <h2>{product.name}</h2>
              <p>${product.price}</p>
            </IonLabel>
          </IonItem>
        ))}
      </IonList>
    </IonContent>
  );
};
```

### Vue Integration

```vue
<!-- ProductList.vue -->
<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Products</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list>
        <ion-item v-for="product in products" :key="product.id"
                  @click="router.push(`/product/${product.id}`)">
          <ion-label>
            <h2>{{ product.name }}</h2>
            <p>{{ formatPrice(product.price) }}</p>
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useIonRouter } from '@ionic/vue';

const router = useIonRouter();
const products = ref<Product[]>([]);

onMounted(async () => {
  products.value = await fetchProducts();
});
</script>
```

## Native API Access

### Core Capacitor Plugins

```typescript
// Camera
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';

async function takePhoto() {
  const image = await Camera.getPhoto({
    quality: 90,
    allowEditing: true,
    resultType: CameraResultType.Uri,
    source: CameraSource.Camera,
  });
  return image.webPath;
}

// Geolocation
import { Geolocation } from '@capacitor/geolocation';

async function getCurrentPosition() {
  const position = await Geolocation.getCurrentPosition({
    enableHighAccuracy: true,
    timeout: 10000,
  });
  return {
    lat: position.coords.latitude,
    lng: position.coords.longitude,
  };
}

// Filesystem
import { Filesystem, Directory, Encoding } from '@capacitor/filesystem';

async function writeFile(filename: string, data: string) {
  await Filesystem.writeFile({
    path: filename,
    data,
    directory: Directory.Documents,
    encoding: Encoding.UTF8,
  });
}

async function readFile(filename: string) {
  const result = await Filesystem.readFile({
    path: filename,
    directory: Directory.Documents,
    encoding: Encoding.UTF8,
  });
  return result.data;
}

// Haptics
import { Haptics, ImpactStyle } from '@capacitor/haptics';

async function vibrate() {
  await Haptics.impact({ style: ImpactStyle.Medium });
}

// Share
import { Share } from '@capacitor/share';

async function shareContent() {
  await Share.share({
    title: 'Check this out',
    text: 'Great product on My App',
    url: 'https://example.com/product/123',
    dialogTitle: 'Share with friends',
  });
}
```

### Platform Detection

```typescript
import { Capacitor } from '@capacitor/core';

// Check if running natively
if (Capacitor.isNativePlatform()) {
  // Use native APIs
} else {
  // Fallback for web
}

// Get platform
const platform = Capacitor.getPlatform(); // 'ios' | 'android' | 'web'

// Check if plugin is available
if (Capacitor.isPluginAvailable('Camera')) {
  const photo = await Camera.getPhoto({ ... });
} else {
  // Fallback: use file input
}
```

## Custom Capacitor Plugin Development

### Plugin Structure

```bash
# Generate plugin scaffold
npm init @capacitor/plugin my-custom-plugin
```

```
my-custom-plugin/
├── src/
│   ├── definitions.ts    # TypeScript interface
│   ├── index.ts          # Plugin registration
│   └── web.ts            # Web implementation
├── ios/
│   └── Sources/
│       └── MyCustomPlugin/
│           └── MyCustomPlugin.swift
├── android/
│   └── src/main/java/com/example/
│       └── MyCustomPlugin.java
└── package.json
```

### TypeScript Definition

```typescript
// src/definitions.ts
export interface MyCustomPlugin {
  echo(options: { value: string }): Promise<{ value: string }>;
  getDeviceInfo(): Promise<DeviceInfo>;
  startBackgroundTask(options: { interval: number }): Promise<void>;
  addListener(
    eventName: 'taskCompleted',
    listenerFunc: (event: { result: string }) => void,
  ): Promise<PluginListenerHandle>;
}

export interface DeviceInfo {
  model: string;
  osVersion: string;
  batteryLevel: number;
}
```

### iOS Implementation (Swift)

```swift
import Capacitor

@objc(MyCustomPlugin)
public class MyCustomPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "MyCustomPlugin"
    public let jsName = "MyCustomPlugin"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "echo", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "getDeviceInfo", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "startBackgroundTask", returnType: CAPPluginReturnPromise),
    ]

    @objc func echo(_ call: CAPPluginCall) {
        let value = call.getString("value") ?? ""
        call.resolve(["value": value])
    }

    @objc func getDeviceInfo(_ call: CAPPluginCall) {
        let device = UIDevice.current
        call.resolve([
            "model": device.model,
            "osVersion": device.systemVersion,
            "batteryLevel": device.batteryLevel,
        ])
    }

    @objc func startBackgroundTask(_ call: CAPPluginCall) {
        let interval = call.getInt("interval") ?? 60

        DispatchQueue.global().asyncAfter(deadline: .now() + .seconds(interval)) {
            self.notifyListeners("taskCompleted", data: ["result": "done"])
        }

        call.resolve()
    }
}
```

### Android Implementation (Kotlin)

```kotlin
@CapacitorPlugin(name = "MyCustomPlugin")
class MyCustomPlugin : Plugin() {

    @PluginMethod
    fun echo(call: PluginCall) {
        val value = call.getString("value") ?: ""
        val result = JSObject()
        result.put("value", value)
        call.resolve(result)
    }

    @PluginMethod
    fun getDeviceInfo(call: PluginCall) {
        val result = JSObject()
        result.put("model", Build.MODEL)
        result.put("osVersion", Build.VERSION.RELEASE)
        result.put("batteryLevel", getBatteryLevel())
        call.resolve(result)
    }

    private fun getBatteryLevel(): Float {
        val batteryManager = context.getSystemService(Context.BATTERY_SERVICE) as BatteryManager
        return batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY).toFloat() / 100
    }
}
```

## Live Reload and Development Workflow

```bash
# Start dev server with live reload on device
ionic cap run ios --livereload --external
ionic cap run android --livereload --external

# Or configure manually in capacitor.config.ts
const config: CapacitorConfig = {
  server: {
    url: 'http://192.168.1.100:5173',  // Your dev server
    cleartext: true,  // Allow HTTP for dev
  },
};

# Build and sync workflow
npm run build && npx cap sync

# Copy web assets only (faster, no native dep update)
npx cap copy
```

## Capacitor vs Cordova Migration

### Key Differences

| Feature | Cordova | Capacitor |
|---------|---------|-----------|
| Native project | Generated, gitignored | Owned, committed to git |
| Plugin system | XML config | Native code + npm |
| WebView | UIWebView (deprecated) | WKWebView / Modern WebView |
| CLI | cordova build | npx cap sync + Xcode/AS |
| Live reload | cordova run --livereload | cap run --livereload |
| PWA support | Separate build | Same codebase |

### Migration Steps

```bash
# 1. Install Capacitor
npm install @capacitor/core @capacitor/cli

# 2. Initialize
npx cap init "My App" com.example.myapp --web-dir www

# 3. Add platforms
npx cap add ios
npx cap add android

# 4. Replace Cordova plugins with Capacitor equivalents
npm uninstall cordova-plugin-camera
npm install @capacitor/camera

# 5. Update plugin usage in code
// Before (Cordova):
// navigator.camera.getPicture(success, error, options);

// After (Capacitor):
import { Camera, CameraResultType } from '@capacitor/camera';
const photo = await Camera.getPhoto({ resultType: CameraResultType.Uri });

# 6. Build and test
npm run build && npx cap sync
npx cap open ios
```

### Cordova Plugin Compatibility

```bash
# Many Cordova plugins still work in Capacitor
npm install cordova-plugin-inappbrowser
npx cap sync

# Check compatibility
npx cap doctor
```

## Ionic UI Components and Theming

### Custom Theming

```css
/* theme/variables.css */
:root {
  --ion-color-primary: #3880ff;
  --ion-color-primary-rgb: 56, 128, 255;
  --ion-color-primary-contrast: #ffffff;
  --ion-color-primary-shade: #3171e0;
  --ion-color-primary-tint: #4c8dff;

  --ion-color-secondary: #3dc2ff;
  --ion-color-success: #2dd36f;
  --ion-color-warning: #ffc409;
  --ion-color-danger: #eb445a;

  --ion-font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --ion-background-color: #ffffff;
  --ion-text-color: #1a1a1a;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --ion-background-color: #121212;
    --ion-text-color: #e0e0e0;
    --ion-card-background: #1e1e1e;
    --ion-toolbar-background: #1a1a1a;
  }
}
```

## PWA Support Alongside Native

Capacitor apps work as PWAs with zero extra configuration.

```typescript
// Service worker registration (same build, web + native)
if ('serviceWorker' in navigator && !Capacitor.isNativePlatform()) {
  navigator.serviceWorker.register('/sw.js');
}

// Adaptive behavior
function getStorageProvider() {
  if (Capacitor.isNativePlatform()) {
    return new CapacitorStorageProvider(); // Uses @capacitor/preferences
  }
  return new IndexedDBStorageProvider(); // Web fallback
}
```

## Performance Optimization

### WebView Performance

```typescript
// capacitor.config.ts
const config: CapacitorConfig = {
  android: {
    // Enable hardware acceleration
    allowMixedContent: false,
    // Use Chrome Custom Tabs for external links
    appendUserAgent: 'MyApp/1.0',
  },
  ios: {
    preferredContentMode: 'mobile',
    // Limiter for WKWebView
    limitsNavigationsToAppBoundDomains: true,
  },
};
```

### Image and Asset Optimization

```typescript
// Lazy load images with Ionic
<ion-img [src]="product.image" alt="Product"></ion-img>

// Use responsive images
<picture>
  <source srcset="image-400.webp 400w, image-800.webp 800w" type="image/webp" />
  <img src="image-800.jpg" loading="lazy" alt="Product" />
</picture>
```

### Virtual Scrolling for Large Lists

```html
<!-- Angular + Ionic virtual scroll -->
<ion-content>
  <cdk-virtual-scroll-viewport itemSize="72" class="ion-content-scroll-host">
    <ion-item *cdkVirtualFor="let item of items">
      <ion-label>{{ item.name }}</ion-label>
    </ion-item>
  </cdk-virtual-scroll-viewport>
</ion-content>
```

## Appflow (CI/CD) and Live Updates

```bash
# Install Appflow SDK
npm install @ionic/cloud

# Deploy live update
ionic deploy add --app-id YOUR_APP_ID --channel-name production

# Configure in capacitor.config.ts
plugins: {
  LiveUpdates: {
    appId: 'YOUR_APP_ID',
    channel: 'production',
    autoUpdateMethod: 'background',
    maxVersions: 2,
  },
}
```

## Testing Strategies

### Unit Testing (Angular Example)

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';
import { ProductListPage } from './product-list.page';

describe('ProductListPage', () => {
  let component: ProductListPage;
  let fixture: ComponentFixture<ProductListPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ProductListPage],
      imports: [IonicModule.forRoot()],
      providers: [{ provide: ProductService, useClass: MockProductService }],
    }).compileComponents();

    fixture = TestBed.createComponent(ProductListPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('displays products after loading', async () => {
    await component.ionViewDidEnter();
    fixture.detectChanges();
    const items = fixture.nativeElement.querySelectorAll('ion-item');
    expect(items.length).toBeGreaterThan(0);
  });
});
```

### E2E with Cypress or Playwright

```typescript
// Cypress test for Ionic app
describe('Product List', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.get('ion-content').should('be.visible');
  });

  it('loads and displays products', () => {
    cy.get('ion-item').should('have.length.greaterThan', 0);
  });

  it('navigates to product detail', () => {
    cy.get('ion-item').first().click();
    cy.url().should('include', '/product/');
    cy.get('ion-back-button').should('be.visible');
  });
});
```

## When to Use Capacitor vs React Native vs Flutter

| Factor | Capacitor/Ionic | React Native | Flutter |
|--------|----------------|--------------|---------|
| **Best for** | Web teams going mobile | Mobile-first with web skills | High-performance custom UI |
| **UI rendering** | Native WebView | Native components | Custom Skia rendering |
| **Performance** | Good (web perf) | Great | Excellent |
| **Code sharing** | 95%+ with web app | 70-85% iOS/Android | 80-95% iOS/Android |
| **Team skills** | HTML/CSS/JS | React + some native | Dart + some native |
| **Existing web app** | Reuse directly | Rewrite UI layer | Full rewrite |
| **Native feel** | Good with Ionic UI | Excellent | Excellent |
| **Plugin ecosystem** | Cordova + Capacitor | Large | Growing |
| **Startup speed** | Slower (WebView init) | Fast | Fast |

**Choose Capacitor when:**
- You have an existing web application to mobilize
- Your team is primarily web developers
- You need a single codebase for web + iOS + Android
- Performance requirements are standard (not gaming or heavy animation)
- You want to ship quickly with familiar tools

**Choose React Native when:**
- You need native UI feel and performance
- Your team knows React
- You need deep native integration
- You are building a mobile-first product

**Choose Flutter when:**
- You need pixel-perfect custom UI across platforms
- Performance is critical (animations, transitions)
- You want the tightest cross-platform consistency
- You are starting from scratch with no web codebase

## Related Skills

- `appstore` - **Recommended**: App Store Connect automation via `asc` CLI (TestFlight, submissions, metadata, signing)
- `expo` - Expo/React Native for comparison
- `react-native-expert` - Architecture and RN/Expo expertise
- `mobile-testing` - Testing Ionic/Capacitor apps
- `deep-linking-push` - Deep linking and push in Capacitor
