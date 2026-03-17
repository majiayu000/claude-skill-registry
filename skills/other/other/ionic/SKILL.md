---
name: ionic
description: Ionic hybrid mobile framework with web technologies. Use for hybrid mobile apps.
---

# Ionic

Ionic Framework is an open-source UI toolkit for building performant, high-quality mobile and desktop apps using web technologies (HTML, CSS, JavaScript) with integrations for Angular, React, and Vue.

## When to Use

- Web developers (Angular/React/Vue) wanting to build mobile apps.
- Building a Progressive Web App (PWA) and mobile app from the exact same codebase.
- Apps with heavy data entry forms or standard UI patterns (lists, tabs).
- Enterprise apps requiring write-once-deploy-everywhere.

## Quick Start

```bash
# Install CLI
npm install -g @ionic/cli

# Start a React app with tabs
ionic start myApp tabs --type=react --capacitor
cd myApp
ionic serve
```

```tsx
// src/pages/Home.tsx (Ionic React)
import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonButton,
  IonIcon,
  IonList,
  IonItem,
  IonLabel,
} from "@ionic/react";
import { camera } from "ionicons/icons";
import { Camera, CameraResultType } from "@capacitor/camera";

const Home: React.FC = () => {
  const takePhoto = async () => {
    const image = await Camera.getPhoto({
      quality: 90,
      allowEditing: false,
      resultType: CameraResultType.Uri,
    });
    console.log("Photo URI", image.webPath);
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Ionic Camera</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <div style={{ padding: 20 }}>
          <IonButton expand="block" onClick={takePhoto}>
            <IonIcon slot="start" icon={camera} />
            Take Photo
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};
export default Home;
```

## Core Concepts

### Web Components

Ionic components (`<ion-button>`, `<ion-card>`) are Web Components. They work in any framework (or no framework) and encapsulate their styles and behavior (Shadow DOM).

### Adaptive Styling

Ionic automatically adapts the look and feel based on the platform.

- **iOS**: Uses Cupertino design standards.
- **Android**: Uses Material Design.
- No code change required.

### Capacitor Integration

Ionic uses **Capacitor** as the native bridge. It provides a Native Runtime for the web app and exposes native APIs (Camera, Geolocation, Haptics) via JavaScript plugins.

## Common Patterns

### Lazy Loading

Crucial for startup performance.

- **Angular**: Use `loadChildren` in Router.
- **React**: Use `React.lazy` and `Suspense`.

### Overlay Components

Modals, Alerts, and Action Sheets are handled via controllers or hooks (`useIonModal`), ensuring they render outside the regular DOM flow for proper z-indexing.

## Best Practices

**Do**:

- Use **Capacitor** instead of Cordova for new projects.
- Use **Virtual Scroll** (or framework equivalents) for long lists.
- Test on real devices early (Web view behavior can differ from Chrome Desktop).
- Use `ion-img` instead of `img` for efficient lazy loading within `ion-content`.

**Don't**:

- Don't block the UI thread with synchronous heavy logic (use Web Workers).
- Don't use arbitrary CSS `z-index` to fix layering (use Ionic utilities/slots).
- Don't forget to handle the **Hardware Back Button** on Android.

## Troubleshooting

| Error                   | Cause                            | Solution                                                     |
| :---------------------- | :------------------------------- | :----------------------------------------------------------- |
| `White Screen of Death` | JavaScript error during startup. | Check remote debugging console (Chrome/Safari).              |
| `CORS Error` on device  | Web View calling external API.   | Configure server CORS or use `@capacitor-community/http`.    |
| `Keyboard covers input` | Scroll view not resizing.        | Ensure `<ion-content>` is used; check `windowSoftInputMode`. |

## References

- [Ionic Framework Docs](https://ionicframework.com/docs)
- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Ionic UI Components](https://ionicframework.com/docs/components)
