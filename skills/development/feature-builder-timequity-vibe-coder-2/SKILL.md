---
name: feature-builder
description: |
  Add features by description. User says WHAT, AI figures out HOW.
  Use when: user wants to add functionality to existing app.
  Triggers: "add auth", "add payments", "add search", "добавь",
  "integrate", "connect".
---

# Feature Builder

Add complete features from simple descriptions.

## Feature Patterns

### Authentication
"Add login" / "Add auth" / "Users should sign in"

Generates:
- Login/register pages
- Auth context/hooks
- Protected routes
- Session management

### Payments
"Add payments" / "Accept money" / "Stripe"

Generates:
- Pricing page
- Checkout flow
- Stripe integration
- Webhook handlers

### Search
"Add search" / "Find things"

Generates:
- Search input component
- Search API endpoint
- Results display
- Filters (if applicable)

### CRUD
"Manage [items]" / "Add/edit/delete [things]"

Generates:
- List view
- Create/edit forms
- Delete confirmation
- API endpoints

## Process

1. **Parse request**
   - Identify feature type
   - Extract specifics (e.g., "Google auth")

2. **Plan implementation**
   - Required components
   - API endpoints
   - Database changes

3. **Generate with TDD**
   - Write tests first
   - Implement each part
   - Verify all tests pass

4. **Integrate**
   - Add to existing routes
   - Update navigation
   - Connect to data layer

5. **Report**
   - "✅ Added [feature]"
   - Show preview

## User Experience

User: "Add Google login"
    ↓
"Adding Google authentication..."
    ↓
[Generate OAuth flow, buttons, callbacks]
    ↓
"✅ Google login added. Try it in preview."
