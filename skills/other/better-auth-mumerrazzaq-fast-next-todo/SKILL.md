---
name: better-auth
description: A comprehensive skill for integrating the `better-auth` authentication framework into modern web applications. Use this skill for tasks involving user authentication, including setup, configuration, database integration, and implementing various auth methods like email/password, social logins, magic links, and passkeys, especially within a Next.js environment.
---

# Comprehensive `better-auth` Integration Skill

## Overview

This skill provides a complete guide and reusable assets for integrating the `better-auth` authentication framework into modern web applications, with a focus on Next.js.

`better-auth` is a powerful, framework-agnostic authentication library for TypeScript. It supports a wide range of authentication strategies and is highly extensible through its plugin and adapter ecosystem.

## Quick Start: Installation

To get started with `better-auth` in a Next.js project, you need to install a few key packages.

```bash
npm install better-auth better-auth/next-js @daveyplate/better-auth-ui
```

### What do these packages do?

-   `better-auth`: This is the core library that provides all the main authentication logic. It is framework-agnostic.
-   `better-auth/next-js`: This package is the adapter that makes `better-auth` work seamlessly with Next.js. It provides helpers for API routes and middleware.
-   `@daveyplate/better-auth-ui`: This is the official React component library, built with `shadcn/ui`, which gives you pre-built components like sign-in forms and user buttons.

After installation, you can proceed with the detailed `Integration Workflow` below.

## Integration Workflow

To add `better-auth` to your project, follow this step-by-step workflow. Each step links to a detailed reference guide with code examples and explanations.

### Step 1: Installation & Core Setup

Begin by installing the necessary packages and creating the main configuration file for `better-auth`. This is the foundation of your authentication system.

- **For detailed instructions, see: [references/01-installation-and-setup.md](./references/01-installation-and-setup.md)**

### Step 2: Next.js Integration

Next, integrate `better-auth` with your Next.js application by setting up the required API route handler and creating a middleware to protect your pages.

- **For detailed instructions, see: [references/02-nextjs-integration.md](./references/02-nextjs-integration.md)**

### Step 3: Database Integration

`better-auth` requires a database to store user and session information. This guide shows you how to connect to a PostgreSQL database using the Prisma adapter.

The recommended workflow uses the `@better-auth/cli` to automatically generate your database schema, ensuring it's always accurate.

- **For detailed instructions, see: [references/03-database-adapters.md](./references/03-database-adapters.md)**

### Step 4: Configure Authentication Methods

Choose and configure one or more authentication methods for your users.

- **Email & Password**: The most common authentication method.
  - See: [references/04-auth-methods-email-password.md](./references/04-auth-methods-email-password.md)
- **Social Logins**: Allow users to sign in with providers like Google, GitHub, etc.
  - See: [references/05-auth-methods-social-logins.md](./references/05-auth-methods-social-logins.md)
- **Magic Links**: Passwordless authentication via email.
  - See: [references/06-auth-methods-magic-links.md](./references/06-auth-methods-magic-links.md)
- **Passkeys**: Secure, passwordless authentication using WebAuthn.
  - See: [references/07-auth-methods-passkeys.md](./references/07-auth-methods-passkeys.md)

### Step 5: Email Integration

Many auth features require sending transactional emails. This step covers integrating an email service provider.

- **For detailed instructions, see: [references/11-integration-email-service.md](./references/11-integration-email-service.md)**

### Step 6: Common Features

Implement common user account features.

- **Password Reset**: Allow users to reset their forgotten passwords.
  - See: [references/10-feature-password-reset.md](./references/10-feature-password-reset.md)

### Step 7: Advanced Features (Optional)

Enhance your application's security with advanced features.

- **Two-Factor Authentication (2FA)**: Add an extra layer of security to user accounts.
  - See: [references/08-advanced-2fa.md](./references/08-advanced-2fa.md)

### Step 8: UI Component Integration

Integrate the official `@daveyplate/better-auth-ui` library to add pre-built React components for sign-in forms, user buttons, and more.

- **For detailed instructions, see: [references/09-ui-components.md](./references/09-ui-components.md)**

## Resources

This skill bundles the following resources to accelerate development.

### references/

This directory contains detailed markdown guides for each step of the integration process. They are filled with code snippets and best practices derived from the official `better-auth` documentation.

### assets/

This directory contains boilerplate code templates that can be copied into your project.

- **`assets/templates/better-auth-nextjs-template/`**: A starter kit for a Next.js application with `better-auth` pre-configured.

### scripts/

This directory contains helper scripts. The example script has been removed as it is not needed for this skill.
