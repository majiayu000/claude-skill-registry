# Landing Page Skill

> **Generate Marketing Landing Page**: Hero, features, pricing, testimonials.

---

## 🎯 Purpose

When user says: "Create a landing page" or "Add marketing page"

Generate a complete landing page with:
- Hero section
- Features
- Pricing
- Testimonials
- CTA sections
- Footer

---

## 📁 Generated Structure

```
src/
├── app/
│   └── (marketing)/
│       ├── layout.tsx
│       ├── page.tsx
│       └── pricing/
│           └── page.tsx
└── components/
    └── marketing/
        ├── hero.tsx
        ├── features.tsx
        ├── pricing-cards.tsx
        ├── testimonials.tsx
        ├── cta.tsx
        ├── navbar.tsx
        └── footer.tsx
```

---

## 🦸 Hero Section

```tsx
// components/marketing/hero.tsx
import Link from "next/link"
import { Button } from "@/components/ui/button"

export function Hero() {
  return (
    <section className="relative py-20 lg:py-32 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-100 -z-10" />
      
      <div className="container mx-auto px-4 text-center">
        <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-700 rounded-full px-4 py-1.5 text-sm font-medium mb-6">
          ✨ New: AI-powered features now available
        </div>

        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6">
          Build faster with
          <span className="text-blue-600"> modern tools</span>
        </h1>

        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          The all-in-one platform for building, deploying, and scaling your 
          applications. Start free, scale as you grow.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" asChild>
            <Link href="/signup">Start for Free</Link>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <Link href="/demo">Watch Demo</Link>
          </Button>
        </div>

        <p className="mt-4 text-sm text-gray-500">
          No credit card required • 14-day free trial
        </p>
      </div>
    </section>
  )
}
```

---

## ✨ Features Section

```tsx
// components/marketing/features.tsx
const features = [
  {
    icon: "⚡",
    title: "Lightning Fast",
    description: "Built on edge infrastructure for sub-100ms response times globally.",
  },
  {
    icon: "🔒",
    title: "Secure by Default",
    description: "Enterprise-grade security with SOC 2 compliance and encryption.",
  },
  {
    icon: "🔄",
    title: "Auto Scaling",
    description: "Automatically scales from zero to millions of requests.",
  },
  {
    icon: "🎯",
    title: "Analytics",
    description: "Built-in analytics to understand your users and optimize.",
  },
  {
    icon: "🤖",
    title: "AI Powered",
    description: "Integrated AI features to automate and enhance your workflows.",
  },
  {
    icon: "🔗",
    title: "Integrations",
    description: "Connect with 100+ tools and services you already use.",
  },
]

export function Features() {
  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Everything you need to ship fast
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Powerful features that help you build, deploy, and scale.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature) => (
            <div key={feature.title} className="p-6 rounded-xl border hover:shadow-lg transition">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

## 💰 Pricing Cards

```tsx
// components/marketing/pricing-cards.tsx
const plans = [
  {
    name: "Free",
    price: "$0",
    description: "Perfect for side projects",
    features: ["5 projects", "10GB storage", "Community support", "Basic analytics"],
    cta: "Start Free",
    popular: false,
  },
  {
    name: "Pro",
    price: "$19",
    period: "/month",
    description: "For growing teams",
    features: [
      "Unlimited projects",
      "100GB storage",
      "Priority support",
      "Advanced analytics",
      "Custom domains",
      "Team collaboration",
    ],
    cta: "Start Trial",
    popular: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    description: "For large organizations",
    features: [
      "Everything in Pro",
      "Unlimited storage",
      "24/7 support",
      "SSO/SAML",
      "SLA guarantee",
      "Dedicated account manager",
    ],
    cta: "Contact Sales",
    popular: false,
  },
]

export function PricingCards() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Simple, transparent pricing</h2>
          <p className="text-xl text-gray-600">No hidden fees. Cancel anytime.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={cn(
                "p-8 rounded-2xl bg-white border-2",
                plan.popular ? "border-blue-600 shadow-xl" : "border-gray-200"
              )}
            >
              {plan.popular && (
                <div className="bg-blue-600 text-white text-sm font-medium px-3 py-1 rounded-full inline-block mb-4">
                  Most Popular
                </div>
              )}
              <h3 className="text-2xl font-bold">{plan.name}</h3>
              <div className="mt-4 flex items-baseline">
                <span className="text-4xl font-bold">{plan.price}</span>
                {plan.period && <span className="text-gray-500">{plan.period}</span>}
              </div>
              <p className="mt-2 text-gray-600">{plan.description}</p>

              <ul className="mt-6 space-y-3">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-2">
                    <span className="text-green-500">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>

              <Button
                className="w-full mt-8"
                variant={plan.popular ? "default" : "outline"}
              >
                {plan.cta}
              </Button>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

## 💬 Testimonials

```tsx
// components/marketing/testimonials.tsx
const testimonials = [
  {
    quote: "This platform has transformed how we build products. We shipped 3x faster.",
    author: "Sarah Chen",
    role: "CTO, TechStart",
    avatar: "/avatars/sarah.jpg",
  },
  {
    quote: "The best developer experience I've ever had. Highly recommended.",
    author: "Mike Johnson",
    role: "Lead Developer, Acme Inc",
    avatar: "/avatars/mike.jpg",
  },
  {
    quote: "Migrated from our old stack in a weekend. Game changer.",
    author: "Emily Rodriguez",
    role: "Founder, StartupXYZ",
    avatar: "/avatars/emily.jpg",
  },
]

export function Testimonials() {
  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
          Loved by developers worldwide
        </h2>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((t) => (
            <div key={t.author} className="p-6 rounded-xl bg-gray-50">
              <p className="text-lg mb-6">&ldquo;{t.quote}&rdquo;</p>
              <div className="flex items-center gap-3">
                <img src={t.avatar} alt={t.author} className="w-12 h-12 rounded-full" />
                <div>
                  <p className="font-semibold">{t.author}</p>
                  <p className="text-sm text-gray-600">{t.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

**Landing page in minutes!**
