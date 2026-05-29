---
name: Notifications
description: Push notifications and in-app alerts
---

# Notifications

## Setup

```typescript
import * as Notifications from 'expo-notifications';

// Configure handler
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});
```

## Request Permissions

```typescript
async function requestPermissions() {
  const { status } = await Notifications.requestPermissionsAsync();
  return status === 'granted';
}
```

## Local Notifications

```typescript
// Schedule immediate notification
await Notifications.scheduleNotificationAsync({
  content: {
    title: 'New Chapter',
    body: 'Manga X has a new chapter!',
    data: { mangaId: '123', type: 'new_chapter' },
  },
  trigger: null, // Immediate
});

// Schedule delayed notification
await Notifications.scheduleNotificationAsync({
  content: {
    title: 'Reminder',
    body: 'Continue reading...',
  },
  trigger: { seconds: 3600 }, // 1 hour
});

// Cancel all
await Notifications.cancelAllScheduledNotificationsAsync();
```

## Notification Listeners

```typescript
useEffect(() => {
  // Notification received while app is open
  const receivedSub = Notifications.addNotificationReceivedListener(
    (notification) => {
      console.log('Received:', notification);
    }
  );

  // User tapped notification
  const responseSub = Notifications.addNotificationResponseReceivedListener(
    (response) => {
      const data = response.notification.request.content.data;
      if (data.type === 'new_chapter') {
        navigation.navigate('MangaDetail', { mangaId: data.mangaId });
      }
    }
  );

  return () => {
    receivedSub.remove();
    responseSub.remove();
  };
}, []);
```

## Notification Service

```typescript
// services/notificationService.ts
import * as Notifications from 'expo-notifications';

export const notificationService = {
  async notifyNewChapter(manga: Manga, chapter: Chapter) {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: manga.title,
        body: `Chapter ${chapter.chapNum} is available`,
        data: { mangaId: manga.id, chapterId: chapter.id },
      },
      trigger: null,
    });
  },

  async notifyDownloadComplete(manga: Manga, chapterCount: number) {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: 'Download Complete',
        body: `${manga.title} - ${chapterCount} chapters`,
        data: { mangaId: manga.id, type: 'download' },
      },
      trigger: null,
    });
  },
};
```

## Progress Notifications (Android)

```typescript
// For download progress, use BackgroundService notifications
import BackgroundService from 'react-native-background-actions';

await BackgroundService.updateNotification({
  taskTitle: 'Downloading',
  taskDesc: `${current}/${total} pages`,
  progressBar: { max: total, value: current },
});
```

## Badge Count

```typescript
// Set badge
await Notifications.setBadgeCountAsync(5);

// Clear badge
await Notifications.setBadgeCountAsync(0);

// Get badge
const count = await Notifications.getBadgeCountAsync();
```

## App Config

```json
// app.json
{
  "expo": {
    "plugins": [
      [
        "expo-notifications",
        {
          "icon": "./assets/icon.png",
          "color": "#FA6432"
        }
      ]
    ]
  }
}
```
