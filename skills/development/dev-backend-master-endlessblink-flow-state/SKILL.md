---
name: Backend Master
description: Master skill for Backend Integration (Supabase) and API handling. Covers database schema, authentication, and SQL.
triggers:
  - fix supabase
  - database migration
  - api integration
  - auth issue
---

# Backend Master Skill

## 🎯 **Capabilities**
- **Supabase**: Client initialization, RLS policies, Types generation.
- **Database**: Postgres SQL, Migrations, Schema design.
- **Auth**: User management, Session handling (`useAuthStore`).
- **Data Sync**: Offline-first patterns (if applicable), Real-time subscriptions.

## 🛠️ **Best Practices**
- **Types**: Always generate types from Supabase schema.
- **RLS**: Never leave tables public unless intended.
- **Security**: Use `useSupabase` composable, never raw client in components.

## 🔄 **Workflow**
1.  **Schema**: Design table in SQL Editor or migration file.
2.  **Types**: Run `npm run update-types` (or equivalent).
3.  **Store**: Update Pinia store to fetch/cache data.
4.  **UI**: Bind clean data to Vue components.
