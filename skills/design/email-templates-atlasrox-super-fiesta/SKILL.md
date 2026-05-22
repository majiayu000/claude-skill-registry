# Email Templates Skill

> **Generate Email Templates**: React Email templates for common scenarios.

---

## 🎯 Purpose

When user says: "Create email templates" or "Add email notifications"

Generate email templates for:
- Welcome email
- Password reset
- Order confirmation
- Invoice/Receipt
- Team invitation
- Notification digest

---

## 📁 Generated Structure

```
emails/
├── components/
│   ├── header.tsx
│   ├── footer.tsx
│   └── button.tsx
├── welcome.tsx
├── password-reset.tsx
├── order-confirmation.tsx
├── receipt.tsx
├── team-invitation.tsx
└── notification-digest.tsx
```

---

## 📧 Setup

```bash
npm install @react-email/components resend
```

---

## 🏗️ Shared Components

```tsx
// emails/components/header.tsx
import { Img, Section, Text } from "@react-email/components"

export function EmailHeader() {
  return (
    <Section style={{ textAlign: "center", marginBottom: "32px" }}>
      <Img
        src={`${process.env.NEXT_PUBLIC_APP_URL}/logo.png`}
        width="48"
        height="48"
        alt="Logo"
      />
      <Text style={{ fontSize: "24px", fontWeight: "bold", marginTop: "16px" }}>
        Your Company
      </Text>
    </Section>
  )
}

// emails/components/footer.tsx
import { Hr, Link, Section, Text } from "@react-email/components"

export function EmailFooter() {
  return (
    <Section style={{ marginTop: "32px", textAlign: "center" }}>
      <Hr style={{ borderColor: "#e5e5e5" }} />
      <Text style={{ color: "#666", fontSize: "12px" }}>
        © {new Date().getFullYear()} Your Company, Inc.
      </Text>
      <Text style={{ color: "#666", fontSize: "12px" }}>
        123 Business St, City, Country
      </Text>
      <Link href="{{unsubscribe}}" style={{ color: "#666", fontSize: "12px" }}>
        Unsubscribe
      </Link>
    </Section>
  )
}

// emails/components/button.tsx
import { Button as EmailButton } from "@react-email/components"

interface ButtonProps {
  href: string
  children: React.ReactNode
}

export function Button({ href, children }: ButtonProps) {
  return (
    <EmailButton
      href={href}
      style={{
        backgroundColor: "#2563eb",
        color: "#fff",
        padding: "12px 24px",
        borderRadius: "6px",
        fontWeight: "600",
        textDecoration: "none",
      }}
    >
      {children}
    </EmailButton>
  )
}
```

---

## 👋 Welcome Email

```tsx
// emails/welcome.tsx
import { Html, Head, Body, Container, Text, Preview } from "@react-email/components"
import { EmailHeader } from "./components/header"
import { EmailFooter } from "./components/footer"
import { Button } from "./components/button"

interface WelcomeEmailProps {
  name: string
  loginUrl: string
}

export function WelcomeEmail({ name, loginUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Welcome to Your Company - Let's get started!</Preview>
      <Body style={{ fontFamily: "Arial, sans-serif", backgroundColor: "#f9fafb" }}>
        <Container style={{ maxWidth: "600px", margin: "0 auto", padding: "40px 20px" }}>
          <EmailHeader />

          <Text style={{ fontSize: "18px", marginBottom: "16px" }}>
            Hi {name},
          </Text>

          <Text style={{ color: "#374151", lineHeight: "1.6" }}>
            Welcome to Your Company! We're excited to have you on board.
          </Text>

          <Text style={{ color: "#374151", lineHeight: "1.6" }}>
            Here's what you can do next:
          </Text>

          <ul style={{ color: "#374151", lineHeight: "1.8" }}>
            <li>Complete your profile</li>
            <li>Explore our features</li>
            <li>Connect with your team</li>
          </ul>

          <Section style={{ textAlign: "center", margin: "32px 0" }}>
            <Button href={loginUrl}>Get Started</Button>
          </Section>

          <Text style={{ color: "#374151" }}>
            If you have any questions, just reply to this email. We're here to help!
          </Text>

          <EmailFooter />
        </Container>
      </Body>
    </Html>
  )
}
```

---

## 🔑 Password Reset

```tsx
// emails/password-reset.tsx
import { Html, Head, Body, Container, Text, Preview, Section } from "@react-email/components"
import { EmailHeader } from "./components/header"
import { EmailFooter } from "./components/footer"
import { Button } from "./components/button"

interface PasswordResetEmailProps {
  name: string
  resetUrl: string
  expiresIn: string
}

export function PasswordResetEmail({ name, resetUrl, expiresIn }: PasswordResetEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Reset your password</Preview>
      <Body style={{ fontFamily: "Arial, sans-serif", backgroundColor: "#f9fafb" }}>
        <Container style={{ maxWidth: "600px", margin: "0 auto", padding: "40px 20px" }}>
          <EmailHeader />

          <Text style={{ fontSize: "18px", marginBottom: "16px" }}>
            Hi {name},
          </Text>

          <Text style={{ color: "#374151" }}>
            We received a request to reset your password. Click the button below to choose a new one:
          </Text>

          <Section style={{ textAlign: "center", margin: "32px 0" }}>
            <Button href={resetUrl}>Reset Password</Button>
          </Section>

          <Text style={{ color: "#6b7280", fontSize: "14px" }}>
            This link will expire in {expiresIn}. If you didn't request this, you can safely ignore this email.
          </Text>

          <EmailFooter />
        </Container>
      </Body>
    </Html>
  )
}
```

---

## 📦 Order Confirmation

```tsx
// emails/order-confirmation.tsx
interface OrderConfirmationEmailProps {
  orderNumber: string
  customerName: string
  items: { name: string; quantity: number; price: number }[]
  total: number
  shippingAddress: string
  trackingUrl?: string
}

export function OrderConfirmationEmail({
  orderNumber,
  customerName,
  items,
  total,
  shippingAddress,
  trackingUrl,
}: OrderConfirmationEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Order #{orderNumber} confirmed!</Preview>
      <Body style={{ fontFamily: "Arial, sans-serif", backgroundColor: "#f9fafb" }}>
        <Container style={{ maxWidth: "600px", margin: "0 auto", padding: "40px 20px" }}>
          <EmailHeader />

          <Section style={{ textAlign: "center", marginBottom: "24px" }}>
            <Text style={{ fontSize: "48px", margin: "0" }}>✓</Text>
            <Text style={{ fontSize: "24px", fontWeight: "bold" }}>Order Confirmed!</Text>
          </Section>

          <Text>Hi {customerName},</Text>
          <Text>Thank you for your order! Here's your order summary:</Text>

          <Section style={{ backgroundColor: "#f3f4f6", padding: "16px", borderRadius: "8px" }}>
            <Text style={{ fontWeight: "bold", margin: "0 0 8px" }}>Order #{orderNumber}</Text>
            
            {items.map((item, i) => (
              <Row key={i}>
                <Column>{item.name} × {item.quantity}</Column>
                <Column style={{ textAlign: "right" }}>${item.price.toFixed(2)}</Column>
              </Row>
            ))}
            
            <Hr />
            <Row>
              <Column style={{ fontWeight: "bold" }}>Total</Column>
              <Column style={{ fontWeight: "bold", textAlign: "right" }}>${total.toFixed(2)}</Column>
            </Row>
          </Section>

          <Text style={{ fontWeight: "bold" }}>Shipping to:</Text>
          <Text style={{ color: "#6b7280" }}>{shippingAddress}</Text>

          {trackingUrl && (
            <Section style={{ textAlign: "center", margin: "24px 0" }}>
              <Button href={trackingUrl}>Track Your Order</Button>
            </Section>
          )}

          <EmailFooter />
        </Container>
      </Body>
    </Html>
  )
}
```

---

## 📤 Sending Emails

```typescript
// lib/email.ts
import { Resend } from "resend"
import { WelcomeEmail } from "@/emails/welcome"
import { PasswordResetEmail } from "@/emails/password-reset"
import { OrderConfirmationEmail } from "@/emails/order-confirmation"

const resend = new Resend(process.env.RESEND_API_KEY)

export async function sendWelcomeEmail(to: string, name: string) {
  await resend.emails.send({
    from: "noreply@yourcompany.com",
    to,
    subject: "Welcome to Your Company!",
    react: WelcomeEmail({ name, loginUrl: `${process.env.APP_URL}/login` }),
  })
}

export async function sendPasswordResetEmail(to: string, name: string, token: string) {
  await resend.emails.send({
    from: "noreply@yourcompany.com",
    to,
    subject: "Reset your password",
    react: PasswordResetEmail({
      name,
      resetUrl: `${process.env.APP_URL}/reset-password?token=${token}`,
      expiresIn: "1 hour",
    }),
  })
}
```

---

**Beautiful emails in minutes!**
