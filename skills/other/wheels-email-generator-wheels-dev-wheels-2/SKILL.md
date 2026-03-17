---
name: Wheels Email Generator
description: Generate email functionality including mailer controllers, email templates, and configuration. Use when sending emails, creating notifications, or implementing transactional emails. Ensures proper email structure, layouts, and testing.
---

# Wheels Email Generator

## When to Use This Skill

Activate automatically when:
- User wants to send emails
- User mentions: email, mailer, sendMail, notification
- User needs password reset emails
- User wants welcome emails or transactional emails
- User asks about email templates or configuration

## Email Directory Structure

```
/app/
├── controllers/
│   └── Mailer.cfc              # Email controller
├── views/
│   └── mailer/                 # Email templates
│       ├── layouts/
│       │   ├── email.cfm       # HTML layout
│       │   └── email.txt.cfm   # Plain text layout
│       ├── welcome.cfm         # HTML version
│       ├── welcome.txt.cfm     # Text version
│       ├── resetPassword.cfm
│       └── resetPassword.txt.cfm
└── /config/
    └── settings.cfm            # Email configuration
```

## Mailer Controller Template

```cfm
component extends="Controller" {

    function config() {
        // Configure email defaults
        set(
            functionName = "sendEmail",
            from = "noreply@yourapp.com",
            layout = "email",
            detectMultipart = true
        );
    }

    /**
     * Send welcome email to new user
     */
    function welcome(required user) {
        sendEmail(
            to = arguments.user.email,
            subject = "Welcome to Our App!",
            template = "mailer/welcome",
            user = arguments.user
        );
    }

    /**
     * Send password reset email
     */
    function resetPassword(required user, required token) {
        local.resetUrl = URLFor(
            route = "passwordReset",
            token = arguments.token,
            onlyPath = false
        );

        sendEmail(
            to = arguments.user.email,
            subject = "Reset Your Password",
            template = "mailer/resetPassword",
            user = arguments.user,
            resetUrl = local.resetUrl
        );
    }

    /**
     * Send order confirmation email
     */
    function orderConfirmation(required order) {
        sendEmail(
            to = arguments.order.customerEmail,
            subject = "Order Confirmation - ##" & arguments.order.id,
            template = "mailer/orderConfirmation",
            order = arguments.order
        );
    }

    /**
     * Send notification to admin
     */
    function adminNotification(required subject, required message) {
        sendEmail(
            to = application.adminEmail,
            subject = arguments.subject,
            template = "mailer/adminNotification",
            message = arguments.message
        );
    }

}
```

## Email Layout (HTML) - views/mailer/layouts/email.cfm

```cfm
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: ##333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: ##007bff;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            background: ##f9f9f9;
            padding: 30px;
            border: 1px solid ##ddd;
        }
        .button {
            display: inline-block;
            padding: 12px 24px;
            background: ##007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin: 20px 0;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: ##666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Your App Name</h1>
    </div>

    <div class="content">
        <cfoutput>##contentForLayout()##</cfoutput>
    </div>

    <div class="footer">
        <p>&copy; #Year(Now())# Your Company. All rights reserved.</p>
        <p>
            <a href="##">Unsubscribe</a> |
            <a href="##">Privacy Policy</a> |
            <a href="##">Contact Us</a>
        </p>
    </div>
</body>
</html>
```

## Email Layout (Plain Text) - views/mailer/layouts/email.txt.cfm

```cfm
<cfoutput>
========================================
YOUR APP NAME
========================================

##contentForLayout()##

========================================
© #Year(Now())# Your Company
All rights reserved.

Unsubscribe: [URL]
Privacy: [URL]
========================================
</cfoutput>
```

## Email Template Examples

### Welcome Email (HTML) - views/mailer/welcome.cfm

```cfm
<cfparam name="user">
<cfoutput>

<h2>Welcome, ##user.firstName##!</h2>

<p>Thank you for joining our community. We're excited to have you on board.</p>

<p>Here's what you can do next:</p>

<ul>
    <li>Complete your profile</li>
    <li>Explore our features</li>
    <li>Connect with other users</li>
</ul>

<p>
    <a href="##URLFor(route='dashboard', onlyPath=false)##" class="button">
        Get Started
    </a>
</p>

<p>If you have any questions, feel free to reply to this email.</p>

<p>Best regards,<br>
The Team</p>

</cfoutput>
```

### Welcome Email (Plain Text) - views/mailer/welcome.txt.cfm

```cfm
<cfparam name="user">
<cfoutput>
Welcome, ##user.firstName##!

Thank you for joining our community. We're excited to have you on board.

Here's what you can do next:
- Complete your profile
- Explore our features
- Connect with other users

Get Started: ##URLFor(route='dashboard', onlyPath=false)##

If you have any questions, feel free to reply to this email.

Best regards,
The Team
</cfoutput>
```

### Password Reset Email - views/mailer/resetPassword.cfm

```cfm
<cfparam name="user">
<cfparam name="resetUrl">
<cfoutput>

<h2>Reset Your Password</h2>

<p>Hi ##user.firstName##,</p>

<p>We received a request to reset your password. Click the button below to create a new password:</p>

<p>
    <a href="##resetUrl##" class="button">Reset Password</a>
</p>

<p>Or copy and paste this link into your browser:</p>
<p>##resetUrl##</p>

<p><strong>This link will expire in 24 hours.</strong></p>

<p>If you didn't request a password reset, you can safely ignore this email.</p>

<p>Thanks,<br>
The Security Team</p>

</cfoutput>
```

## Email Configuration - config/settings.cfm

```cfm
<cfscript>
// Email Server Configuration
set(
    functionName = "sendEmail",
    server = "smtp.gmail.com",
    port = 587,
    username = "your-email@gmail.com",
    password = "your-app-password",
    useTLS = true,
    useSSL = false,
    from = "noreply@yourapp.com",
    type = "html",
    charset = "utf-8"
);

// Environment-Specific Email Settings
if (application.wheels.environment == "development") {
    // Log emails instead of sending
    set(functionName = "sendEmail", debug = true, deliver = false);
}

if (application.wheels.environment == "testing") {
    // Send all emails to test account
    set(functionName = "sendEmail", to = "test@yourapp.com");
}

if (application.wheels.environment == "production") {
    // Production settings
    set(
        functionName = "sendEmail",
        server = getEnv("SMTP_SERVER"),
        username = getEnv("SMTP_USERNAME"),
        password = getEnv("SMTP_PASSWORD"),
        deliver = true
    );
}
</cfscript>
```

## Using the Mailer

### In Controllers

```cfm
component extends="Controller" {

    function create() {
        user = model("User").new(params.user);

        if (user.save()) {
            // Send welcome email
            controller("Mailer").welcome(user);

            redirectTo(route="home", success="Account created! Check your email.");
        } else {
            renderView(action="new");
        }
    }

    function forgotPassword() {
        user = model("User").findOne(where="email='#params.email#'");

        if (isObject(user)) {
            // Generate reset token
            token = createUUID();
            user.update(resetToken=token, resetTokenExpiry=dateAdd("h", 24, now()));

            // Send reset email
            controller("Mailer").resetPassword(user=user, token=token);

            flashInsert(success="Password reset instructions sent to your email.");
        }

        redirectTo(action="login");
    }

}
```

### Direct Usage

```cfm
// Simple email
sendEmail(
    to = "user@example.com",
    from = "noreply@yourapp.com",
    subject = "Test Email",
    body = "This is a test email."
);

// Email with template
sendEmail(
    to = "user@example.com",
    subject = "Custom Email",
    template = "mailer/custom",
    customVariable = "value"
);

// Email with attachments
sendEmail(
    to = "user@example.com",
    subject = "Invoice",
    template = "mailer/invoice",
    file = expandPath("./uploads/invoice.pdf"),
    fileName = "invoice-##123##.pdf"
);
```

## Email with File Attachments

```cfm
function sendInvoice(required order) {
    local.pdfPath = expandPath("./temp/invoice-##arguments.order.id##.pdf");

    // Generate PDF invoice
    generateInvoicePDF(arguments.order, local.pdfPath);

    // Send email with attachment
    sendEmail(
        to = arguments.order.customerEmail,
        subject = "Your Invoice - Order ##arguments.order.id##",
        template = "mailer/invoice",
        order = arguments.order,
        file = local.pdfPath,
        fileName = "invoice-##arguments.order.id##.pdf"
    );

    // Clean up temp file
    fileDelete(local.pdfPath);
}
```

## Email with Multiple Recipients

```cfm
function sendNewsletter(required subject, required template) {
    // Get all subscribed users
    subscribers = model("User").findAll(where="subscribed=1");

    // Send to each subscriber
    for (local.subscriber in subscribers) {
        sendEmail(
            to = local.subscriber.email,
            subject = arguments.subject,
            template = arguments.template,
            user = local.subscriber
        );
    }
}
```

## Testing Emails

### Email Test

```cfm
component extends="wheels.Test" {

    function testWelcomeEmailSent() {
        // Create test user
        user = model("User").create(
            email = "test@example.com",
            firstName = "Test"
        );

        // Call mailer
        controller("Mailer").welcome(user);

        // Verify email was queued
        assert("application.wheels.emailQueue.len() > 0");
    }

    function testPasswordResetEmail() {
        user = model("User").findByKey(1);
        token = createUUID();

        controller("Mailer").resetPassword(user=user, token=token);

        // Check email contains reset link
        lastEmail = application.wheels.emailQueue[1];
        assert("findNoCase('reset', lastEmail.body) > 0");
        assert("findNoCase(token, lastEmail.body) > 0");
    }

}
```

### Manual Testing

```cfm
// Test in browser - add route
.get(name="testEmail", pattern="/test/email", to="tests##testEmail")

// Test controller
function testEmail() {
    user = model("User").findByKey(1);
    controller("Mailer").welcome(user);
    renderText("Email sent! Check server logs.");
}
```

## Email Best Practices

### ✅ DO:
- Always provide both HTML and plain text versions
- Use responsive email layouts (max-width: 600px)
- Include unsubscribe links
- Test emails across different clients
- Use descriptive subject lines
- Handle email failures gracefully
- Queue emails for bulk sending
- Use environment-specific settings

### ❌ DON'T:
- Send emails synchronously in production
- Hardcode email addresses
- Use complex CSS (limited support)
- Forget error handling
- Send without user consent
- Include sensitive data in emails
- Use JavaScript in emails

## Common Email Patterns

### 1. Transactional Emails
```cfm
// Order confirmation, password resets, account verification
- Time-sensitive
- User-triggered
- High priority
```

### 2. Notification Emails
```cfm
// Activity updates, mentions, reminders
- Event-driven
- May be batched
- User preferences apply
```

### 3. Marketing Emails
```cfm
// Newsletters, promotions
- Bulk sending
- Unsubscribe required
- Scheduled
```

## Email Queue Pattern

```cfm
// Queue email for background processing
function queueEmail(required struct emailData) {
    model("EmailQueue").create(
        recipient = arguments.emailData.to,
        subject = arguments.emailData.subject,
        template = arguments.emailData.template,
        data = serializeJSON(arguments.emailData),
        status = "pending"
    );
}

// Process queue (run via scheduled task)
function processEmailQueue() {
    pending = model("EmailQueue").findAll(
        where = "status='pending'",
        order = "createdAt",
        maxRows = 50
    );

    for (local.email in pending) {
        try {
            local.data = deserializeJSON(local.email.data);
            sendEmail(argumentCollection=local.data);
            local.email.update(status="sent", sentAt=now());
        } catch (any e) {
            local.email.update(
                status = "failed",
                errorMessage = e.message
            );
        }
    }
}
```

## SMTP Providers

### Gmail
```cfm
server = "smtp.gmail.com"
port = 587
useTLS = true
// Note: Use app password, not account password
```

### SendGrid
```cfm
server = "smtp.sendgrid.net"
port = 587
username = "apikey"
password = "YOUR_API_KEY"
useTLS = true
```

### Mailgun
```cfm
server = "smtp.mailgun.org"
port = 587
username = "postmaster@yourdomain.mailgun.org"
password = "YOUR_PASSWORD"
useTLS = true
```

### AWS SES
```cfm
server = "email-smtp.us-east-1.amazonaws.com"
port = 587
username = "YOUR_SMTP_USERNAME"
password = "YOUR_SMTP_PASSWORD"
useTLS = true
```

## Related Skills

- **wheels-controller-generator**: Create mailer controllers
- **wheels-view-generator**: Create email templates
- **wheels-auth-generator**: Password reset emails
- **wheels-test-generator**: Test email functionality

---

**Generated by:** Wheels Email Generator Skill v1.0
