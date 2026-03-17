---
name: passwordless-docs
description: Bitwarden Passwordless.dev documentation, SDKs, and React examples
version: 1.2.0
---

# passwordless-docs

Comprehensive Bitwarden Passwordless.dev documentation, SDK references, and implementation examples for passwordless authentication using FIDO2/WebAuthn.

## Description

This skill provides access to:
- **Official Documentation**: Bitwarden Passwordless.dev platform documentation
- **Node.js SDK**: Official `@passwordlessdev/passwordless-nodejs` implementation guide
- **React Example**: Complete React/Vite application demonstrating passwordless auth
- **FIDO2/WebAuthn**: Passwordless authentication standards and best practices
- **API Reference**: Complete API documentation and integration patterns

**Primary Repository:** [bitwarden/passwordless-docs](https://github.com/bitwarden/passwordless-docs)
**Node.js SDK:** [bitwarden/passwordless-nodejs](https://github.com/bitwarden/passwordless-nodejs)
**React Example:** [bitwarden/passwordless-react-example](https://github.com/bitwarden/passwordless-react-example)

## When to Use This Skill

Use this skill when you need to:
- Implement passwordless authentication with FIDO2/WebAuthn
- Integrate Bitwarden Passwordless.dev into Node.js or React applications
- Build frontend passwordless auth with React
- Look up Passwordless.dev API documentation
- Find implementation examples and working code samples
- Troubleshoot passwordless authentication issues
- Check for known issues or recent SDK updates
- Review security best practices for passwordless auth
- Understand token registration and verification flows
- Set up demo backend and frontend applications

## Quick Reference

### Documentation Repository
- **Homepage:** https://bitwarden.com/
- **Documentation Site:** https://docs.passwordless.dev/
- **Topics:** bitwarden, passwordless, FIDO2, WebAuthn
- **Open Issues:** 16
- **Last Updated:** 2025-11-28
- **Languages:** CSS (48.4%), TypeScript (25.0%), SCSS (23.6%), Vue (3.0%)

### Node.js SDK
- **Package:** `@passwordlessdev/passwordless-nodejs`
- **NPM:** https://www.npmjs.com/package/@passwordlessdev/passwordless-nodejs
- **Stars:** 16
- **License:** Apache License 2.0
- **Latest Version:** 1.0.1 (2024-10-22)
- **Open Issues:** 9
- **Languages:** TypeScript (86.8%), JavaScript (13.2%)
- **Requirements:** Node.js 10+, ES2018+

### React Example Application
- **Repository:** [bitwarden/passwordless-react-example](https://github.com/bitwarden/passwordless-react-example)
- **Stars:** 21
- **Build Tool:** Vite
- **Open Issues:** 11
- **Languages:** TypeScript (86.8%), CSS (8.2%), JavaScript (3.2%), HTML (1.6%)
- **Demo Backend:** https://demo.passwordless.dev/swagger/index.html
- **Framework:** Vanilla React (no NextJS/Remix/Gatsby)

### Key Features
- **Registration Flow**: Create passwordless registration tokens
- **Authentication**: Verify tokens and authenticate users
- **Discoverable Credentials**: Support for platform authenticators
- **Alias Management**: Device-based authentication aliases
- **Customization**: Configurable API endpoints and options
- **React Integration**: Complete frontend implementation example

## Available References

### Documentation (bitwarden/passwordless-docs)
- `references/README.md` - Complete platform documentation
- `references/file_structure.md` - Documentation site structure
- `references/issues.md` - Recent documentation issues
- `references/CHANGELOG.md` - Documentation version history
- `references/releases.md` - Documentation releases

### Node.js SDK (bitwarden/passwordless-nodejs)
- `references/sdk-nodejs/README.md` - SDK implementation guide with code examples
- `references/sdk-nodejs/file_structure.md` - SDK repository structure
- `references/sdk-nodejs/issues.md` - SDK known issues and bug reports
- `references/sdk-nodejs/releases.md` - SDK release notes and changelog

### React Example (bitwarden/passwordless-react-example)
- `references/example-react/README.md` - React implementation guide and setup
- `references/example-react/file_structure.md` - React app structure
- `references/example-react/issues.md` - Known frontend issues

## Backend SDK Quick Start

### Installation
```bash
npm i @passwordlessdev/passwordless-nodejs
```

### Basic Setup
```typescript
import { PasswordlessClient, PasswordlessOptions } from '@passwordlessdev/passwordless-nodejs';

const options: PasswordlessOptions = {
  baseUrl: 'https://v4.passwordless.dev' // Optional, this is the default
};

const client = new PasswordlessClient('your-api-secret', options);
```

### Environment Configuration
```env
PASSWORDLESS_API=https://v4.passwordless.dev
PASSWORDLESS_SECRET=demo:secret:f831e39c29e64b77aba547478a4b3ec6
```

### Registration Example
```typescript
// After creating user in your database
const registerOptions = new RegisterOptions();
registerOptions.userId = userId;
registerOptions.username = username;
registerOptions.discoverable = true;
registerOptions.aliases = [deviceName]; // Optional

const token = await client.createRegisterToken(registerOptions);
```

### Authentication Example
```typescript
const token = request.query.token;
const verifiedUser = await client.verifyToken(token);

if (verifiedUser && verifiedUser.success === true) {
  // User authenticated successfully
  // Create session, JWT, etc.
}
```

## React Frontend Quick Start

### Project Setup
```bash
# Clone the example
git clone https://github.com/bitwarden/passwordless-react-example.git
cd passwordless-react-example

# Install dependencies
npm install

# Configure environment
# Create .env file with:
VITE_BACKEND_URL=https://demo.passwordless.dev
VITE_PASSWORDLESS_API_KEY=pwdemo:public:5aec1f24f65343239bf4e1c9a852e871
VITE_PASSWORDLESS_API_URL=https://v4.passwordless.dev

# Run development server
npm run dev
```

### Key Technologies
- **React**: UI framework
- **Vite**: Build tool and dev server
- **TypeScript**: Type safety
- **Demo Backend**: Pre-configured passwordless API

### Frontend Architecture
The React example demonstrates:
- User registration with passwordless credentials
- Login flow using WebAuthn
- Session management
- API integration with Passwordless.dev
- Production-ready component structure

## Common Use Cases

### 1. Implementing Backend Passwordless Registration
Reference: `references/sdk-nodejs/README.md` - Registration section

### 2. Building React Frontend Authentication
Reference: `references/example-react/README.md` - Complete React setup

### 3. User Authentication Flow (Backend)
Reference: `references/sdk-nodejs/README.md` - Logging in section

### 4. API Documentation Lookup
Reference: `references/README.md` - Complete API reference

### 5. Troubleshooting Integration Issues
- Backend: `references/sdk-nodejs/issues.md` - SDK issues
- Frontend: `references/example-react/issues.md` - React issues

### 6. Understanding FIDO2/WebAuthn Standards
Reference: `references/README.md` - Standards documentation

### 7. Full-Stack Implementation
Combine:
- Backend: `references/sdk-nodejs/README.md`
- Frontend: `references/example-react/README.md`

## Version History

- **1.2.0** (2026-01-02): Enhanced with React example integration
  - Added React example repository (bitwarden/passwordless-react-example)
  - Included frontend implementation guide
  - Added Vite + React project setup
  - Expanded use cases for full-stack development
  - Updated frontend-specific documentation
  - Quality score improvement: 90/100 → 92/100

- **1.1.0** (2026-01-02): Enhanced with Node.js SDK integration
  - Added Node.js SDK repository content
  - Included SDK implementation examples
  - Added quick start guide for SDK
  - Expanded use cases and references
  - Updated version to reflect enhancement

- **1.0.0** (2026-01-02): Initial release
  - Core documentation repository
  - Basic reference structure
  - Initial quality score: 85/100

## Implementation Patterns

### Backend-Only Pattern
Use when building API services:
1. Install Node.js SDK
2. Configure environment variables
3. Implement registration endpoints
4. Implement verification endpoints
5. Handle session management

### Frontend-Only Pattern
Use when integrating with existing API:
1. Clone React example
2. Configure backend URL in .env
3. Customize UI components
4. Integrate with your auth flow

### Full-Stack Pattern
Use for complete implementation:
1. Set up backend with Node.js SDK
2. Use React example as frontend base
3. Connect frontend to your backend
4. Deploy both services
5. Configure production environment

## Related Resources

- **Get Started Guide**: https://docs.passwordless.dev/guide/get-started.html
- **Admin Console**: https://admin.passwordless.dev/
- **Demo Backend Swagger**: https://demo.passwordless.dev/swagger/index.html
- **Bitwarden Homepage**: https://bitwarden.com/
- **FIDO Alliance**: https://fidoalliance.org/
- **WebAuthn Guide**: https://webauthn.guide/

---

**Generated by Skill Seeker** | Enhanced with SDKs and Examples
**Quality Score**: 92/100 (Grade A)
**Status**: ✅ Production Ready
**Coverage**: Backend + Frontend + Documentation
