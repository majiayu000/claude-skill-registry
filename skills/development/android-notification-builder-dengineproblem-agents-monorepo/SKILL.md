---
name: android-notification-builder
description: Эксперт Android notifications. Используй для push notifications, channels и notification patterns.
---

# Android Notification Builder Expert

Эксперт по реализации уведомлений Android с использованием NotificationCompat.Builder и notification channels.

## Notification Channels (API 26+)

```kotlin
class NotificationHelper(private val context: Context) {
    companion object {
        const val CHANNEL_ID_MESSAGES = "messages"
        const val CHANNEL_ID_UPDATES = "updates"
        const val CHANNEL_ID_PROMOTIONS = "promotions"
    }

    fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val messagesChannel = NotificationChannel(
                CHANNEL_ID_MESSAGES,
                "Сообщения",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Уведомления о новых сообщениях"
                enableLights(true)
                lightColor = Color.BLUE
                enableVibration(true)
                vibrationPattern = longArrayOf(0, 250, 250, 250)
            }

            val updatesChannel = NotificationChannel(
                CHANNEL_ID_UPDATES,
                "Обновления",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Системные обновления"
            }

            val notificationManager = context.getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannels(
                listOf(messagesChannel, updatesChannel)
            )
        }
    }
}
```

## Базовое уведомление

```kotlin
fun showBasicNotification(title: String, message: String) {
    val intent = Intent(context, MainActivity::class.java).apply {
        flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
    }

    val pendingIntent = PendingIntent.getActivity(
        context, 0, intent,
        PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
    )

    val notification = NotificationCompat.Builder(context, CHANNEL_ID_MESSAGES)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle(title)
        .setContentText(message)
        .setPriority(NotificationCompat.PRIORITY_HIGH)
        .setContentIntent(pendingIntent)
        .setAutoCancel(true)
        .build()

    NotificationManagerCompat.from(context).notify(NOTIFICATION_ID, notification)
}
```

## Расширяемые уведомления

### Big Text Style
```kotlin
fun showExpandableTextNotification(title: String, shortText: String, longText: String) {
    val bigTextStyle = NotificationCompat.BigTextStyle()
        .bigText(longText)
        .setBigContentTitle(title)
        .setSummaryText("Подробности")

    val notification = NotificationCompat.Builder(context, CHANNEL_ID_MESSAGES)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle(title)
        .setContentText(shortText)
        .setStyle(bigTextStyle)
        .setPriority(NotificationCompat.PRIORITY_DEFAULT)
        .build()

    NotificationManagerCompat.from(context).notify(NOTIFICATION_ID, notification)
}
```

### Big Picture Style
```kotlin
fun showImageNotification(title: String, message: String, bitmap: Bitmap) {
    val bigPictureStyle = NotificationCompat.BigPictureStyle()
        .bigPicture(bitmap)
        .bigLargeIcon(null as Bitmap?)
        .setBigContentTitle(title)
        .setSummaryText(message)

    val notification = NotificationCompat.Builder(context, CHANNEL_ID_MESSAGES)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle(title)
        .setContentText(message)
        .setLargeIcon(bitmap)
        .setStyle(bigPictureStyle)
        .build()

    NotificationManagerCompat.from(context).notify(NOTIFICATION_ID, notification)
}
```

### Inbox Style
```kotlin
fun showInboxNotification(title: String, messages: List<String>) {
    val inboxStyle = NotificationCompat.InboxStyle()
        .setBigContentTitle(title)
        .setSummaryText("${messages.size} новых сообщений")

    messages.take(5).forEach { message ->
        inboxStyle.addLine(message)
    }

    val notification = NotificationCompat.Builder(context, CHANNEL_ID_MESSAGES)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle(title)
        .setContentText("${messages.size} новых сообщений")
        .setStyle(inboxStyle)
        .setNumber(messages.size)
        .build()

    NotificationManagerCompat.from(context).notify(NOTIFICATION_ID, notification)
}
```

## Интерактивные уведомления

### Action Buttons
```kotlin
fun showNotificationWithActions(title: String, message: String) {
    // Reply action
    val replyIntent = Intent(context, ReplyReceiver::class.java)
    val replyPendingIntent = PendingIntent.getBroadcast(
        context, 0, replyIntent,
        PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
    )

    val remoteInput = RemoteInput.Builder("key_text_reply")
        .setLabel("Ответить")
        .build()

    val replyAction = NotificationCompat.Action.Builder(
        R.drawable.ic_reply,
        "Ответить",
        replyPendingIntent
    ).addRemoteInput(remoteInput).build()

    // Archive action
    val archiveIntent = Intent(context, ArchiveReceiver::class.java)
    val archivePendingIntent = PendingIntent.getBroadcast(
        context, 1, archiveIntent,
        PendingIntent.FLAG_IMMUTABLE
    )

    val archiveAction = NotificationCompat.Action.Builder(
        R.drawable.ic_archive,
        "Архивировать",
        archivePendingIntent
    ).build()

    val notification = NotificationCompat.Builder(context, CHANNEL_ID_MESSAGES)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle(title)
        .setContentText(message)
        .addAction(replyAction)
        .addAction(archiveAction)
        .build()

    NotificationManagerCompat.from(context).notify(NOTIFICATION_ID, notification)
}
```

## Progress Notification

```kotlin
fun showProgressNotification(title: String, maxProgress: Int, currentProgress: Int) {
    val notification = NotificationCompat.Builder(context, CHANNEL_ID_UPDATES)
        .setSmallIcon(R.drawable.ic_download)
        .setContentTitle(title)
        .setContentText("Загрузка: $currentProgress%")
        .setProgress(maxProgress, currentProgress, false)
        .setOngoing(true)
        .build()

    NotificationManagerCompat.from(context).notify(PROGRESS_NOTIFICATION_ID, notification)
}

fun showIndeterminateProgress(title: String) {
    val notification = NotificationCompat.Builder(context, CHANNEL_ID_UPDATES)
        .setSmallIcon(R.drawable.ic_sync)
        .setContentTitle(title)
        .setContentText("Синхронизация...")
        .setProgress(0, 0, true)
        .setOngoing(true)
        .build()

    NotificationManagerCompat.from(context).notify(PROGRESS_NOTIFICATION_ID, notification)
}

fun completeProgressNotification(title: String) {
    val notification = NotificationCompat.Builder(context, CHANNEL_ID_UPDATES)
        .setSmallIcon(R.drawable.ic_done)
        .setContentTitle(title)
        .setContentText("Загрузка завершена")
        .setProgress(0, 0, false)
        .build()

    NotificationManagerCompat.from(context).notify(PROGRESS_NOTIFICATION_ID, notification)
}
```

## Grouped Notifications

```kotlin
fun showGroupedNotifications(messages: List<Message>) {
    val GROUP_KEY = "com.example.MESSAGE_GROUP"

    // Individual notifications
    messages.forEachIndexed { index, message ->
        val notification = NotificationCompat.Builder(context, CHANNEL_ID_MESSAGES)
            .setSmallIcon(R.drawable.ic_message)
            .setContentTitle(message.sender)
            .setContentText(message.text)
            .setGroup(GROUP_KEY)
            .build()

        NotificationManagerCompat.from(context).notify(index, notification)
    }

    // Summary notification
    val summaryNotification = NotificationCompat.Builder(context, CHANNEL_ID_MESSAGES)
        .setSmallIcon(R.drawable.ic_message)
        .setContentTitle("${messages.size} новых сообщений")
        .setStyle(NotificationCompat.InboxStyle()
            .setBigContentTitle("${messages.size} новых сообщений")
            .setSummaryText("Сообщения"))
        .setGroup(GROUP_KEY)
        .setGroupSummary(true)
        .build()

    NotificationManagerCompat.from(context).notify(SUMMARY_ID, summaryNotification)
}
```

## FCM Integration

```kotlin
class MyFirebaseMessagingService : FirebaseMessagingService() {

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        remoteMessage.notification?.let { notification ->
            showNotification(
                notification.title ?: "Уведомление",
                notification.body ?: ""
            )
        }

        remoteMessage.data.isNotEmpty().let {
            handleDataMessage(remoteMessage.data)
        }
    }

    override fun onNewToken(token: String) {
        sendTokenToServer(token)
    }

    private fun showNotification(title: String, body: String) {
        val notification = NotificationCompat.Builder(this, CHANNEL_ID_MESSAGES)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(body)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        NotificationManagerCompat.from(this).notify(
            System.currentTimeMillis().toInt(),
            notification
        )
    }
}
```

## Лучшие практики

### Безопасность
```kotlin
// Скрытие контента на lock screen
.setVisibility(NotificationCompat.VISIBILITY_PRIVATE)
.setPublicVersion(publicNotification)

// Безопасные PendingIntent
PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
```

### Производительность
```kotlin
// Оптимизация bitmap
fun scaleBitmap(bitmap: Bitmap, maxSize: Int = 256): Bitmap {
    val ratio = minOf(
        maxSize.toFloat() / bitmap.width,
        maxSize.toFloat() / bitmap.height
    )
    return Bitmap.createScaledBitmap(
        bitmap,
        (bitmap.width * ratio).toInt(),
        (bitmap.height * ratio).toInt(),
        true
    )
}
```

### Пользовательский опыт
- Используйте соответствующие importance levels
- Группируйте связанные уведомления
- Добавляйте действия для быстрого реагирования
- Обеспечьте accessibility через content descriptions
- Тестируйте на разных версиях Android
