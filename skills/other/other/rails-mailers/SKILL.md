---
name: rails-mailers
description: Use when sending emails - ActionMailer with async delivery via SolidQueue, templates, previews, and testing
---

# Email with ActionMailer

Send transactional and notification emails using ActionMailer, integrated with SolidQueue for async delivery. Create HTML and text templates, preview emails in development, and test thoroughly.

<when-to-use>
- Sending transactional emails (password resets, confirmations, receipts)
- Sending notification emails (updates, alerts, digests)
- Delivering emails asynchronously via background jobs
- Creating email templates with HTML and text versions
- Testing email delivery and content
</when-to-use>

<benefits>
- **Async Delivery** - ActionMailer integrates with SolidQueue for non-blocking email sending
- **Template Support** - ERB templates for HTML and text email versions
- **Preview in Development** - See emails without sending via /rails/mailers
- **Testing Support** - Full test suite for delivery and content
- **Layouts** - Shared layouts for consistent email branding
- **Attachments** - Send files (PDFs, images) with emails
</benefits>

<verification-checklist>
Before completing mailer work:
- ✅ Async delivery used (deliver_later, not deliver_now)
- ✅ Both HTML and text templates provided
- ✅ URL helpers used (not path helpers)
- ✅ Email previews created for development
- ✅ Mailer tests passing (delivery and content)
- ✅ SolidQueue configured for background delivery
</verification-checklist>

<standards>
- ALWAYS deliver emails asynchronously with deliver_later (NOT deliver_now)
- Provide both HTML and text email templates
- Use *_url helpers (NOT *_path) for links in emails
- Set default 'from' address in ApplicationMailer
- Create email previews for development (/rails/mailers)
- Configure default_url_options for each environment
- Use inline CSS for email styling (email clients strip external styles)
- Test email delivery and content
- Use parameterized mailers (.with()) for cleaner syntax
</standards>

---

## ActionMailer Setup

<pattern name="actionmailer-basic-setup">
<description>Configure ActionMailer for email delivery</description>

**Mailer Class:**

```ruby
# app/mailers/application_mailer.rb
class ApplicationMailer < ActionMailer::Base
  default from: "noreply@example.com"
  layout "mailer"
end

# app/mailers/notification_mailer.rb
class NotificationMailer < ApplicationMailer
  def welcome_email(user)
    @user = user
    @login_url = login_url
    mail(to: user.email, subject: "Welcome to Our App")
  end

  def password_reset(user)
    @user = user
    @reset_url = password_reset_url(user.reset_token)
    mail(to: user.email, subject: "Password Reset Instructions")
  end
end
```

**HTML Template:**

```erb
<%# app/views/notification_mailer/welcome_email.html.erb %>
<h1>Welcome, <%= @user.name %>!</h1>
<p>Thanks for signing up. Get started by logging in:</p>
<%= link_to "Login Now", @login_url, class: "button" %>
```

**Text Template:**

```erb
<%# app/views/notification_mailer/welcome_email.text.erb %>
Welcome, <%= @user.name %>!

Thanks for signing up. Get started by logging in:
<%= @login_url %>
```

**Usage (Async with SolidQueue):**

```ruby
# In controller or service
NotificationMailer.welcome_email(@user).deliver_later
NotificationMailer.password_reset(@user).deliver_later(queue: :mailers)
```

**Why:** ActionMailer integrates seamlessly with SolidQueue for async delivery. Always use deliver_later to avoid blocking requests. Provide both HTML and text versions for compatibility.
</pattern>

<antipattern>
<description>Using deliver_now in production (blocks HTTP request)</description>
<bad-example>

```ruby
# ❌ WRONG - Blocks HTTP request thread
def create
  @user = User.create!(user_params)
  NotificationMailer.welcome_email(@user).deliver_now  # Blocks!
  redirect_to @user
end
```

</bad-example>
<good-example>

```ruby
# ✅ CORRECT - Async delivery via SolidQueue
def create
  @user = User.create!(user_params)
  NotificationMailer.welcome_email(@user).deliver_later  # Non-blocking
  redirect_to @user
end
```

</good-example>

**Why bad:** deliver_now blocks the HTTP request until SMTP completes, creating slow response times and poor user experience. deliver_later uses SolidQueue to send email in background.
</antipattern>

<pattern name="parameterized-mailers">
<description>Use .with() to pass parameters cleanly to mailers</description>

```ruby
class NotificationMailer < ApplicationMailer
  def custom_notification
    @user = params[:user]
    @message = params[:message]
    mail(to: @user.email, subject: params[:subject])
  end
end

# Usage
NotificationMailer.with(
  user: user,
  message: "Update available",
  subject: "System Alert"
).custom_notification.deliver_later
```

**Why:** Cleaner syntax, easier to read and modify, and works seamlessly with background jobs.
</pattern>

---

## Email Templates

<pattern name="email-layouts">
<description>Shared layouts for consistent email branding</description>

**HTML Layout:**

```erb
<%# app/views/layouts/mailer.html.erb %>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      body {
        font-family: Arial, sans-serif;
        max-width: 600px;
        margin: 0 auto;
        color: #333;
      }
      .header {
        background-color: #4F46E5;
        color: white;
        padding: 20px;
        text-align: center;
      }
      .content {
        padding: 20px;
      }
      .button {
        display: inline-block;
        padding: 12px 24px;
        background-color: #4F46E5;
        color: white;
        text-decoration: none;
        border-radius: 4px;
      }
      .footer {
        padding: 20px;
        text-align: center;
        font-size: 12px;
        color: #666;
      }
    </style>
  </head>
  <body>
    <div class="header">
      <h1>Your App</h1>
    </div>
    <div class="content">
      <%= yield %>
    </div>
    <div class="footer">
      <p>&copy; 2025 Your Company. All rights reserved.</p>
    </div>
  </body>
</html>
```

**Text Layout:**

```erb
<%# app/views/layouts/mailer.text.erb %>
================================================================================
YOUR APP
================================================================================

<%= yield %>

--------------------------------------------------------------------------------
© 2025 Your Company. All rights reserved.
```

**Why:** Consistent branding across all emails. Inline CSS ensures styling works across email clients.
</pattern>

<pattern name="email-attachments">
<description>Attach files to emails (PDFs, CSVs, images)</description>

```ruby
class ReportMailer < ApplicationMailer
  def monthly_report(user, data)
    @user = user

    # Regular attachment
    attachments["report.pdf"] = {
      mime_type: "application/pdf",
      content: generate_pdf(data)
    }

    # Inline attachment (for embedding in email body)
    attachments.inline["logo.png"] = File.read(
      Rails.root.join("app/assets/images/logo.png")
    )

    mail(to: user.email, subject: "Monthly Report")
  end
end
```

**In template:**

```erb
<%# Reference inline attachment %>
<%= image_tag attachments["logo.png"].url %>
```

**Why:** Attach reports, exports, or inline images. Inline attachments can be referenced in email body with image_tag.
</pattern>

<antipattern>
<description>Using *_path helpers instead of *_url in emails (broken links)</description>
<bad-example>

```ruby
# ❌ WRONG - Relative path doesn't work in emails
def welcome_email(user)
  @user = user
  @login_url = login_path  # => "/login" (relative path)
  mail(to: user.email, subject: "Welcome")
end
```

</bad-example>
<good-example>

```ruby
# ✅ CORRECT - Full URL works in emails
def welcome_email(user)
  @user = user
  @login_url = login_url  # => "https://example.com/login" (absolute URL)
  mail(to: user.email, subject: "Welcome")
end

# Required configuration
# config/environments/production.rb
config.action_mailer.default_url_options = { host: "example.com", protocol: "https" }
```

</good-example>

**Why bad:** Emails are viewed outside your application context, so relative paths don't work. Always use *_url helpers to generate absolute URLs.
</antipattern>

---

## Email Testing

<pattern name="letter-opener-setup">
<description>Preview emails in browser during development without sending</description>

**Configuration:**

```ruby
# Gemfile
group :development do
  gem "letter_opener"
end

# config/environments/development.rb
config.action_mailer.delivery_method = :letter_opener
config.action_mailer.default_url_options = { host: "localhost", port: 3000 }

# config/environments/production.rb
config.action_mailer.delivery_method = :smtp
config.action_mailer.smtp_settings = {
  address: "smtp.sendgrid.net",
  port: 587,
  user_name: Rails.application.credentials.dig(:smtp, :username),
  password: Rails.application.credentials.dig(:smtp, :password),
  authentication: :plain,
  enable_starttls_auto: true
}
config.action_mailer.default_url_options = { host: "example.com", protocol: "https" }
```

**Why:** letter_opener opens emails in browser during development - no SMTP setup needed. Test email appearance without actually sending.
</pattern>

<pattern name="mailer-previews">
<description>Preview all email variations at /rails/mailers</description>

```ruby
# test/mailers/previews/notification_mailer_preview.rb
class NotificationMailerPreview < ActionMailer::Preview
  # Preview at http://localhost:3000/rails/mailers/notification_mailer/welcome_email
  def welcome_email
    user = User.first || User.new(name: "Test User", email: "test@example.com")
    NotificationMailer.welcome_email(user)
  end

  def password_reset
    user = User.first || User.new(name: "Test User", email: "test@example.com")
    user.reset_token = "sample_token_123"
    NotificationMailer.password_reset(user)
  end

  # Preview with different data
  def welcome_email_long_name
    user = User.new(name: "Christopher Alexander Montgomery III", email: "long@example.com")
    NotificationMailer.welcome_email(user)
  end
end
```

**Why:** Mailer previews at /rails/mailers let you see all email variations without sending. Test different edge cases (long names, missing data, etc.).
</pattern>

<pattern name="mailer-testing">
<description>Test email delivery and content with ActionMailer::TestCase</description>

```ruby
# test/mailers/notification_mailer_test.rb
class NotificationMailerTest < ActionMailer::TestCase
  test "welcome_email sends with correct attributes" do
    user = users(:alice)
    email = NotificationMailer.welcome_email(user)

    # Test delivery
    assert_emails 1 do
      email.deliver_now
    end

    # Test attributes
    assert_equal [user.email], email.to
    assert_equal ["noreply@example.com"], email.from
    assert_equal "Welcome to Our App", email.subject

    # Test content
    assert_includes email.html_part.body.to_s, user.name
    assert_includes email.text_part.body.to_s, user.name
    assert_includes email.html_part.body.to_s, "Login Now"
  end

  test "delivers via background job" do
    user = users(:alice)

    assert_enqueued_with(job: ActionMailer::MailDeliveryJob, queue: "mailers") do
      NotificationMailer.welcome_email(user).deliver_later(queue: :mailers)
    end
  end

  test "password_reset includes reset link" do
    user = users(:alice)
    user.update!(reset_token: "test_token_123")
    email = NotificationMailer.password_reset(user)

    assert_includes email.html_part.body.to_s, "test_token_123"
    assert_includes email.html_part.body.to_s, "password_reset"
  end
end
```

**Why:** Test email delivery, content, and background job enqueuing. Verify recipients, subjects, and that emails are queued properly.
</pattern>

---

## Email Configuration

<pattern name="environment-configuration">
<description>Configure ActionMailer for each environment</description>

**Development:**

```ruby
# config/environments/development.rb
config.action_mailer.delivery_method = :letter_opener
config.action_mailer.perform_deliveries = true
config.action_mailer.raise_delivery_errors = true
config.action_mailer.default_url_options = { host: "localhost", port: 3000 }
```

**Test:**

```ruby
# config/environments/test.rb
config.action_mailer.delivery_method = :test
config.action_mailer.default_url_options = { host: "example.com" }
```

**Production:**

```ruby
# config/environments/production.rb
config.action_mailer.delivery_method = :smtp
config.action_mailer.perform_deliveries = true
config.action_mailer.raise_delivery_errors = false
config.action_mailer.default_url_options = {
  host: ENV["APP_HOST"],
  protocol: "https"
}

config.action_mailer.smtp_settings = {
  address: ENV["SMTP_ADDRESS"],
  port: ENV["SMTP_PORT"],
  user_name: Rails.application.credentials.dig(:smtp, :username),
  password: Rails.application.credentials.dig(:smtp, :password),
  authentication: :plain,
  enable_starttls_auto: true
}
```

**Why:** Different configurations per environment. Development previews in browser, test stores emails in memory, production sends via SMTP.
</pattern>

---

<testing>

```ruby
# test/mailers/notification_mailer_test.rb
class NotificationMailerTest < ActionMailer::TestCase
  setup do
    @user = users(:alice)
  end

  test "welcome_email" do
    email = NotificationMailer.welcome_email(@user)

    assert_emails 1 { email.deliver_now }
    assert_equal [@user.email], email.to
    assert_equal ["noreply@example.com"], email.from
    assert_match @user.name, email.html_part.body.to_s
    assert_match @user.name, email.text_part.body.to_s
  end

  test "enqueues for async delivery" do
    assert_enqueued_with(job: ActionMailer::MailDeliveryJob) do
      NotificationMailer.welcome_email(@user).deliver_later
    end
  end

  test "uses correct queue" do
    assert_enqueued_with(job: ActionMailer::MailDeliveryJob, queue: "mailers") do
      NotificationMailer.welcome_email(@user).deliver_later(queue: :mailers)
    end
  end
end

# test/system/email_delivery_test.rb
class EmailDeliveryTest < ApplicationSystemTestCase
  test "sends welcome email after signup" do
    visit signup_path
    fill_in "Email", with: "new@example.com"
    fill_in "Password", with: "password"
    click_button "Sign Up"

    assert_enqueued_emails 1
    perform_enqueued_jobs

    email = ActionMailer::Base.deliveries.last
    assert_equal ["new@example.com"], email.to
    assert_match "Welcome", email.subject
  end
end
```

</testing>

---

<related-skills>
- rails-ai:jobs - Background job processing with SolidQueue
- rails-ai:views - Email templates and layouts
- rails-ai:testing - Testing email delivery
- rails-ai:project-setup - Environment-specific email configuration
</related-skills>

<resources>

**Official Documentation:**
- [Rails Guides - Action Mailer Basics](https://guides.rubyonrails.org/action_mailer_basics.html)

**Gems & Libraries:**
- [letter_opener](https://github.com/ryanb/letter_opener) - Preview emails in browser during development

**Tools:**
- [Email on Acid](https://www.emailonacid.com/) - Email testing across clients

**Email Service Providers:**
- [SendGrid Rails Guide](https://docs.sendgrid.com/for-developers/sending-email/rubyonrails)

</resources>
