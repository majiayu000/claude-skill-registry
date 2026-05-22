---
name: orchardcore-notifications
description: Skill for managing Orchard Core notifications. Covers INotificationService, notification providers, notification events, push notifications, notification workflow activities, and custom notification handlers.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Notifications - Prompt Templates

## Create and Manage Notifications

You are an Orchard Core expert. Generate notification implementations, custom providers, and notification handling for Orchard Core.

### Guidelines

- Enable the `OrchardCore.Notifications` feature before using the notification system.
- Use `INotificationService` to send notifications programmatically to specific users.
- Notifications support multiple delivery methods: in-app, email, and push.
- Implement `INotificationProvider` to create custom notification sources.
- Use `INotificationEvents` to hook into the notification lifecycle.
- Notifications appear in the admin dashboard notification center.
- Each notification has a summary, body, and optional URL for navigation.
- Target notifications to individual users or groups using permissions.
- Notifications can be marked as read, dismissed, or left unread.
- Workflow activities can send notifications as part of automated processes.

### Enabling Notifications

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Notifications",
        "OrchardCore.Notifications.Email"
      ],
      "disable": []
    }
  ]
}
```

### Notification Model

A notification contains the following key properties:

- `NotificationId` - Unique identifier for the notification.
- `Summary` - Short text displayed in the notification list.
- `Body` - Detailed content of the notification (supports HTML).
- `UserId` - The target user who receives the notification.
- `CreatedUtc` - Timestamp when the notification was created.
- `ReadAtUtc` - Timestamp when the notification was read (null if unread).
- `IsRead` - Indicates whether the notification has been read.

### Sending Notifications with INotificationService

```csharp
using OrchardCore.Notifications;

public sealed class ContentApprovalHandler
{
    private readonly INotificationService _notificationService;
    private readonly IStringLocalizer S;

    public ContentApprovalHandler(
        INotificationService notificationService,
        IStringLocalizer<ContentApprovalHandler> stringLocalizer)
    {
        _notificationService = notificationService;
        S = stringLocalizer;
    }

    public async Task NotifyAuthorAsync(IUser user, string contentItemId)
    {
        var message = new Notification
        {
            Summary = S["Your content has been approved"],
            Body = S["The content item you submitted has been reviewed and approved."],
        };

        await _notificationService.SendAsync(user, message);
    }
}
```

### Sending Notifications to Multiple Users

```csharp
using OrchardCore.Notifications;
using OrchardCore.Users.Services;

public sealed class BulkNotificationSender
{
    private readonly INotificationService _notificationService;
    private readonly IUserService _userService;
    private readonly IStringLocalizer S;

    public BulkNotificationSender(
        INotificationService notificationService,
        IUserService userService,
        IStringLocalizer<BulkNotificationSender> stringLocalizer)
    {
        _notificationService = notificationService;
        _userService = userService;
        S = stringLocalizer;
    }

    public async Task NotifyEditorsAsync(string contentItemDisplayText)
    {
        var message = new Notification
        {
            Summary = S["New content requires review: {0}", contentItemDisplayText],
            Body = S["A new content item has been submitted and requires editorial review."],
        };

        var editors = await _userService.GetUsersInRoleAsync("Editor");

        foreach (var editor in editors)
        {
            await _notificationService.SendAsync(editor, message);
        }
    }
}
```

### Implementing a Custom Notification Provider

Implement `INotificationProvider` to define a custom source of notifications.

```csharp
using OrchardCore.Notifications;

public sealed class SystemAlertNotificationProvider : INotificationProvider
{
    private readonly ISession _session;
    private readonly IStringLocalizer S;

    public SystemAlertNotificationProvider(
        ISession session,
        IStringLocalizer<SystemAlertNotificationProvider> stringLocalizer)
    {
        _session = session;
        S = stringLocalizer;
    }

    public async Task<IEnumerable<Notification>> GetNotificationsAsync(
        string userId,
        NotificationQueryContext context)
    {
        // Return custom notifications for the given user.
        var alerts = await _session.Query<SystemAlert>()
            .Where(a => a.IsActive)
            .ListAsync();

        return alerts.Select(alert => new Notification
        {
            Summary = alert.Title,
            Body = alert.Message,
            CreatedUtc = alert.CreatedUtc,
        });
    }
}
```

### Handling Notification Events

Use `INotificationEvents` to react to notification lifecycle changes.

```csharp
using OrchardCore.Notifications;

public sealed class NotificationEventHandler : NotificationEventsBase
{
    private readonly ILogger _logger;

    public NotificationEventHandler(ILogger<NotificationEventHandler> logger)
    {
        _logger = logger;
    }

    public override Task SentAsync(NotificationContext context)
    {
        _logger.LogInformation(
            "Notification '{Summary}' sent to user '{UserId}'.",
            context.Notification.Summary,
            context.NotifyUserId);

        return Task.CompletedTask;
    }

    public override Task ReadAsync(NotificationContext context)
    {
        _logger.LogInformation(
            "Notification '{NotificationId}' marked as read.",
            context.Notification.NotificationId);

        return Task.CompletedTask;
    }
}
```

### Registering Notification Services

```csharp
using OrchardCore.Modules;
using OrchardCore.Notifications;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<INotificationEvents, NotificationEventHandler>();
        services.AddScoped<INotificationProvider, SystemAlertNotificationProvider>();
    }
}
```

### Creating a Custom Notification Handler

Handle specific notification types by implementing `INotificationMethodProvider`.

```csharp
using OrchardCore.Notifications;

public sealed class SmsNotificationMethodProvider : INotificationMethodProvider
{
    private readonly ISmsService _smsService;

    public SmsNotificationMethodProvider(ISmsService smsService)
    {
        _smsService = smsService;
    }

    public string Method => "Sms";

    public LocalizedString Name => new("SMS");

    public async Task<bool> TrySendAsync(
        IUser user,
        Notification notification,
        bool isRead,
        CancellationToken cancellationToken = default)
    {
        var phoneNumber = await GetPhoneNumberAsync(user);

        if (string.IsNullOrEmpty(phoneNumber))
        {
            return false;
        }

        await _smsService.SendAsync(phoneNumber, notification.Summary);

        return true;
    }

    private Task<string> GetPhoneNumberAsync(IUser user)
    {
        // Retrieve the phone number from user claims or profile.
        return Task.FromResult(string.Empty);
    }
}
```

### Notification Permissions

Notifications use permissions to control access:

- `ManageNotifications` - Allows managing all notifications.
- `ViewOwnNotifications` - Allows a user to view their own notifications.

```csharp
using OrchardCore.Notifications;
using OrchardCore.Security.Permissions;

public sealed class NotificationPermissionHandler : AuthorizationHandler<PermissionRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        PermissionRequirement requirement)
    {
        if (requirement.Permission.Name == NotificationPermissions.ManageNotifications.Name)
        {
            if (context.User.IsInRole("Administrator"))
            {
                context.Succeed(requirement);
            }
        }

        return Task.CompletedTask;
    }
}
```

### Push Notifications Configuration

Enable push notifications by configuring the `OrchardCore.Notifications` settings:

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Notifications",
        "OrchardCore.Notifications.Push"
      ],
      "disable": []
    }
  ]
}
```

Configure push notification options in `appsettings.json`:

```json
{
  "OrchardCore": {
    "OrchardCore_Notifications": {
      "TotalUnreadNotifications": 10,
      "AbsoluteExpirationSeconds": 600,
      "DisableNotificationCenter": false
    }
  }
}
```

### Notification Workflow Activities

The notifications module provides workflow activities for automation:

- `NotifyUserTask` - Sends a notification to a specific user within a workflow.

```csharp
using OrchardCore.Notifications.Activities;
using OrchardCore.Workflows.Activities;
using OrchardCore.Workflows.Abstractions.Models;
using OrchardCore.Workflows.Models;

public sealed class CustomNotifyTask : TaskActivity
{
    private readonly INotificationService _notificationService;
    private readonly IUserService _userService;

    public CustomNotifyTask(
        INotificationService notificationService,
        IUserService userService,
        IStringLocalizer<CustomNotifyTask> localizer)
    {
        _notificationService = notificationService;
        _userService = userService;
        S = localizer;
    }

    private IStringLocalizer S { get; }

    public override string Name => "CustomNotifyTask";

    public override LocalizedString DisplayText => S["Custom Notify Task"];

    public override LocalizedString Category => S["Notifications"];

    public string UserName { get; set; }

    public string NotificationSummary { get; set; }

    public override IEnumerable<Outcome> GetPossibleOutcomes(
        WorkflowExecutionContext workflowContext,
        ActivityContext activityContext)
    {
        return Outcomes(S["Notified"], S["Failed"]);
    }

    public override async Task<ActivityExecutionResult> ExecuteAsync(
        WorkflowExecutionContext workflowContext,
        ActivityContext activityContext)
    {
        var user = await _userService.GetUserByNameAsync(UserName);

        if (user == null)
        {
            return Outcomes("Failed");
        }

        var message = new Notification
        {
            Summary = NotificationSummary,
        };

        await _notificationService.SendAsync(user, message);

        return Outcomes("Notified");
    }
}
```

### Reading and Managing Notifications

```csharp
using OrchardCore.Notifications;

public sealed class NotificationManager
{
    private readonly INotificationService _notificationService;

    public NotificationManager(INotificationService notificationService)
    {
        _notificationService = notificationService;
    }

    public async Task<IEnumerable<Notification>> GetUnreadNotificationsAsync(string userId)
    {
        return await _notificationService.GetNotificationsAsync(
            userId,
            isRead: false);
    }

    public async Task MarkAsReadAsync(string notificationId)
    {
        await _notificationService.ReadAsync(notificationId);
    }

    public async Task DismissNotificationAsync(string notificationId)
    {
        await _notificationService.DeleteAsync(notificationId);
    }

    public async Task<int> GetUnreadCountAsync(string userId)
    {
        return await _notificationService.GetUnreadCountAsync(userId);
    }
}
```

### Admin Notification Center

Notifications appear in the Orchard Core admin dashboard. The notification center is accessible from the top navigation bar and displays:

- A bell icon with a badge showing the unread notification count.
- A dropdown list of recent notifications sorted by date.
- Options to mark individual notifications as read or dismiss them.
- A link to the full notifications list page.

Customize the notification center behavior in the admin settings under **Configuration > Notifications**.
