---
name: push-notifications
description: Firebase Cloud Messaging and Apple Push Notification Service setup.
---

# Push Notifications

## Expo Notifications

```bash
npx expo install expo-notifications expo-device
```

```typescript
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';

// Configure
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

// Request permission
async function registerForPushNotifications() {
  if (!Device.isDevice) return null;

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') return null;

  const token = await Notifications.getExpoPushTokenAsync({
    projectId: 'your-project-id',
  });

  return token.data;
}
```

## Handle Notifications

```typescript
// Foreground
useEffect(() => {
  const subscription = Notifications.addNotificationReceivedListener(
    (notification) => {
      console.log('Received:', notification);
    }
  );

  return () => subscription.remove();
}, []);

// Tap response
useEffect(() => {
  const subscription = Notifications.addNotificationResponseReceivedListener(
    (response) => {
      const data = response.notification.request.content.data;
      // Navigate based on data
      navigation.navigate(data.screen, data.params);
    }
  );

  return () => subscription.remove();
}, []);
```

## Backend Integration

```typescript
// Send from server
await fetch('https://exp.host/--/api/v2/push/send', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    to: expoPushToken,
    title: 'New message',
    body: 'You have a new message',
    data: { screen: 'Chat', chatId: '123' },
  }),
});
```

## Firebase (bare workflow)

```typescript
import messaging from '@react-native-firebase/messaging';

// Get FCM token
const fcmToken = await messaging().getToken();

// Background handler
messaging().setBackgroundMessageHandler(async (message) => {
  console.log('Background message:', message);
});
```
