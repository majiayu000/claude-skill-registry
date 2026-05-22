---
name: ionic
description: Ionic development guidelines for building cross-platform mobile applications with Angular, Cordova, and Firebase integration.
---

# Ionic Development

You are an expert in Ionic for building cross-platform mobile applications.

## Core Principles

- Write concise, technical responses with accurate Ionic examples
- Use feature-based organization for scalable applications
- Leverage Ionic's built-in components for consistent UI
- Follow Angular best practices for Ionic Angular projects

## Project Structure

### Feature-Based Organization
```
src/
├── app/
│   ├── features/
│   │   ├── auth/
│   │   ├── home/
│   │   └── settings/
│   ├── shared/
│   │   ├── components/
│   │   ├── services/
│   │   └── pipes/
│   └── core/
│       ├── guards/
│       └── interceptors/
├── assets/
└── theme/
```

## Ionic Components

### Navigation
```typescript
import { NavController } from '@ionic/angular';

constructor(private navCtrl: NavController) {}

navigateForward() {
  this.navCtrl.navigateForward('/details');
}

navigateBack() {
  this.navCtrl.back();
}
```

### UI Components
- Use `ion-header`, `ion-content`, `ion-footer` for page structure
- Leverage `ion-list`, `ion-item` for lists
- Use `ion-button`, `ion-fab` for actions
- Apply `ion-modal`, `ion-popover` for overlays

## Styling

- Use SCSS for component-specific styles
- Leverage Ionic CSS variables for theming
- Apply platform-specific styling when needed
- Use responsive utilities for different screen sizes

```scss
:host {
  --ion-background-color: var(--ion-color-light);
}

.custom-card {
  --background: var(--ion-color-primary-tint);
}
```

## Performance

### Lazy Loading
- Implement lazy loading for feature modules
- Use `loadChildren` in routing configuration
- Split code into logical chunks

### Optimization
- Use virtual scrolling for long lists
- Implement proper image loading strategies
- Minimize bundle size with tree shaking

## Native Integration

### Cordova/Capacitor Plugins
- Use Ionic Native wrappers for native functionality
- Implement web fallbacks for native features
- Handle platform differences appropriately

```typescript
import { Camera } from '@ionic-native/camera/ngx';

async takePicture() {
  const image = await this.camera.getPicture(options);
  return image;
}
```

## Firebase Integration

- Use AngularFire for Firebase services
- Implement proper Firestore transactions
- Handle real-time updates efficiently
- Use batch operations for multiple writes

## Environment Configuration

- Configure environments for development, staging, production
- Use environment files for API endpoints
- Manage secrets securely

## Testing

- Write unit tests for services and components
- Use Ionic testing utilities
- Test native plugin mocks appropriately
