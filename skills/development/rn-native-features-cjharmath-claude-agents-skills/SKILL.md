---
name: rn-native-features
description: Native iOS features in Expo React Native apps. Use when implementing camera, push notifications, haptics, permissions, device sensors, or other native APIs in Expo.
---

# Native Features (Expo)

## Permissions Pattern

Always request permissions before using native features:

```typescript
import * as Camera from 'expo-camera';

async function requestCameraPermission() {
  const { status } = await Camera.requestCameraPermissionsAsync();
  
  if (status !== 'granted') {
    // Guide user to settings if denied
    Alert.alert(
      'Camera Access Required',
      'Please enable camera access in Settings to take photos.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Open Settings', onPress: () => Linking.openSettings() },
      ]
    );
    return false;
  }
  return true;
}
```

### Check permission status first

```typescript
import * as Camera from 'expo-camera';

function usePermission() {
  const [permission, requestPermission] = Camera.useCameraPermissions();
  
  // permission.granted - boolean
  // permission.canAskAgain - false if user selected "Don't ask again"
  // permission.status - 'granted' | 'denied' | 'undetermined'
  
  return { permission, requestPermission };
}
```

## Camera

### Basic Camera with Photo Capture

```typescript
import { CameraView, useCameraPermissions } from 'expo-camera';
import { useRef, useState } from 'react';

export function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [facing, setFacing] = useState<'front' | 'back'>('back');
  const cameraRef = useRef<CameraView>(null);

  if (!permission) return <View />;
  
  if (!permission.granted) {
    return (
      <View>
        <Text>Camera access is required</Text>
        <Button title="Grant Permission" onPress={requestPermission} />
      </View>
    );
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.8,
        base64: false,
        exif: false,
      });
      console.log('Photo URI:', photo.uri);
      // photo.uri is a local file path
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <CameraView 
        ref={cameraRef}
        style={{ flex: 1 }} 
        facing={facing}
      >
        <View style={styles.controls}>
          <Button title="Flip" onPress={() => setFacing(f => f === 'back' ? 'front' : 'back')} />
          <Button title="Take Photo" onPress={takePicture} />
        </View>
      </CameraView>
    </View>
  );
}
```

### Image Picker (Gallery + Camera)

Often simpler than full camera UI:

```typescript
import * as ImagePicker from 'expo-image-picker';

async function pickImage() {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    aspect: [1, 1],
    quality: 0.8,
  });

  if (!result.canceled) {
    return result.assets[0].uri;
  }
}

async function takePhoto() {
  const permission = await ImagePicker.requestCameraPermissionsAsync();
  if (!permission.granted) return;
  
  const result = await ImagePicker.launchCameraAsync({
    allowsEditing: true,
    aspect: [1, 1],
    quality: 0.8,
  });

  if (!result.canceled) {
    return result.assets[0].uri;
  }
}
```

## Push Notifications

### Setup with expo-notifications

```typescript
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';

// Configure how notifications appear when app is foregrounded
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

async function registerForPushNotifications() {
  if (!Device.isDevice) {
    console.log('Push notifications require a physical device');
    return null;
  }

  // Check existing permission
  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  // Request if not determined
  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    console.log('Push notification permission denied');
    return null;
  }

  // Get Expo push token
  const token = await Notifications.getExpoPushTokenAsync({
    projectId: 'your-expo-project-id', // From app.json
  });

  return token.data; // "ExponentPushToken[xxxx]"
}
```

### Handle incoming notifications

```typescript
import { useEffect, useRef } from 'react';
import * as Notifications from 'expo-notifications';

export function useNotificationHandler() {
  const notificationListener = useRef<Notifications.Subscription>();
  const responseListener = useRef<Notifications.Subscription>();

  useEffect(() => {
    // Notification received while app is foregrounded
    notificationListener.current = Notifications.addNotificationReceivedListener(
      (notification) => {
        console.log('Received:', notification.request.content);
      }
    );

    // User tapped on notification
    responseListener.current = Notifications.addNotificationResponseReceivedListener(
      (response) => {
        const data = response.notification.request.content.data;
        // Navigate based on notification data
        if (data.screen) {
          router.push(data.screen);
        }
      }
    );

    return () => {
      notificationListener.current?.remove();
      responseListener.current?.remove();
    };
  }, []);
}
```

### Send test notification locally

```typescript
async function sendTestNotification() {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: "Match Reminder",
      body: "Your match starts in 30 minutes!",
      data: { screen: '/match/123' },
    },
    trigger: { seconds: 5 },
  });
}
```

### Send from backend (Expo Push API)

```python
# FastAPI example
import httpx

async def send_push_notification(
    expo_push_token: str, 
    title: str, 
    body: str, 
    data: dict = None
):
    message = {
        "to": expo_push_token,
        "title": title,
        "body": body,
        "data": data or {},
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://exp.host/--/api/v2/push/send",
            json=message,
            headers={"Content-Type": "application/json"},
        )
        return response.json()
```

## Haptic Feedback

```typescript
import * as Haptics from 'expo-haptics';

// Light tap - for UI interactions
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);

// Medium - for confirmations
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);

// Heavy - for significant actions
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);

// Success/Error/Warning - semantic feedback
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);

// Selection - for picker/scroll
Haptics.selectionAsync();
```

### Good haptic patterns

```typescript
// Button press
<Pressable 
  onPress={() => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    handlePress();
  }}
/>

// Form submission success
await submitForm();
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

// Error state
if (error) {
  Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
}

// Picker/Scroll selection
<Picker 
  onValueChange={(value) => {
    Haptics.selectionAsync();
    setValue(value);
  }}
/>
```

## Location

```typescript
import * as Location from 'expo-location';

async function getCurrentLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') {
    return null;
  }

  const location = await Location.getCurrentPositionAsync({
    accuracy: Location.Accuracy.Balanced,
  });
  
  return {
    latitude: location.coords.latitude,
    longitude: location.coords.longitude,
  };
}

// Watch location changes
function useLocationTracking() {
  const [location, setLocation] = useState(null);

  useEffect(() => {
    let subscription: Location.LocationSubscription;
    
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') return;
      
      subscription = await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.High,
          distanceInterval: 10, // meters
        },
        (loc) => setLocation(loc.coords)
      );
    })();
    
    return () => subscription?.remove();
  }, []);
  
  return location;
}
```

## Local Storage

### AsyncStorage (simple key-value)

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Store
await AsyncStorage.setItem('user_preferences', JSON.stringify(prefs));

// Retrieve
const prefs = JSON.parse(await AsyncStorage.getItem('user_preferences') || '{}');

// Remove
await AsyncStorage.removeItem('user_preferences');
```

### SecureStore (sensitive data)

```typescript
import * as SecureStore from 'expo-secure-store';

// For tokens, credentials - encrypted storage
await SecureStore.setItemAsync('auth_token', token);
const token = await SecureStore.getItemAsync('auth_token');
await SecureStore.deleteItemAsync('auth_token');
```

## App State & Lifecycle

```typescript
import { useEffect } from 'react';
import { AppState, AppStateStatus } from 'react-native';

function useAppState(callback: (state: AppStateStatus) => void) {
  useEffect(() => {
    const subscription = AppState.addEventListener('change', callback);
    return () => subscription.remove();
  }, [callback]);
}

// Usage
useAppState((state) => {
  if (state === 'active') {
    // App came to foreground - refresh data
    refreshData();
  } else if (state === 'background') {
    // App going to background - save state
    saveState();
  }
});
```

## Keyboard Handling

```typescript
import { KeyboardAvoidingView, Platform } from 'react-native';

// Wrap forms to avoid keyboard
<KeyboardAvoidingView 
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  style={{ flex: 1 }}
>
  <YourForm />
</KeyboardAvoidingView>

// Dismiss keyboard
import { Keyboard } from 'react-native';
Keyboard.dismiss();

// Listen to keyboard events
import { useEffect } from 'react';
import { Keyboard } from 'react-native';

function useKeyboardVisible() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const showSub = Keyboard.addListener('keyboardDidShow', () => setVisible(true));
    const hideSub = Keyboard.addListener('keyboardDidHide', () => setVisible(false));
    return () => {
      showSub.remove();
      hideSub.remove();
    };
  }, []);

  return visible;
}
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Camera black screen | Check permissions, ensure CameraView has explicit dimensions |
| Notifications not received | Verify physical device, check push token registration |
| Location inaccurate | Use `Accuracy.High`, check device location services enabled |
| Haptics not working | Only works on physical device, not simulator |
| SecureStore size limit | Max ~2KB per item, use for tokens not large data |
