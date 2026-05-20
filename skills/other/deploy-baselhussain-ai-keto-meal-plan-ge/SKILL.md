---
description: Deploy frontend and backend to Vercel with migration and health verification
handoffs:
  - label: Fix Deployment Issues
    agent: backend-engineer
    prompt: Fix the deployment issues identified
    send: false
---

## User Input

```text
$ARGUMENTS
```

Options: `production`, `staging`, `preview`, or empty (defaults to staging)

## Task

Deploy the keto meal plan application to Vercel with proper migrations and health checks.

### Steps

1. **Parse Arguments**:
   - `production`: Deploy to production environment
   - `staging`: Deploy to staging environment (default)
   - `preview`: Create preview deployment

2. **Pre-Deployment Checks**:
   ```bash
   # Ensure we're on correct branch
   git branch --show-current

   # Check for uncommitted changes
   git status --porcelain

   # Run tests
   cd backend && pytest tests/unit/ -v

   # Build frontend locally to catch errors
   cd frontend && npm run build
   ```

3. **Push to Git** (if needed):
   ```bash
   git add .
   git commit -m "Deploy: [production|staging|preview]"
   git push origin $(git branch --show-current)
   ```

4. **Deploy Frontend to Vercel**:
   ```bash
   cd frontend

   # Production deployment
   vercel --prod

   # Or staging/preview
   vercel
   ```

5. **Deploy Backend to Render**:
   ```bash
   # Backend deploys automatically via GitHub integration
   # Or trigger manual deploy via Render dashboard
   # Or use Render CLI:

   cd backend

   # If using Render CLI
   render deploy --service backend-service

   # Check deploy status
   render services list
   ```

6. **Run Database Migrations**:
   ```bash
   # Set DATABASE_URL to production/staging database
   export DATABASE_URL="[production-database-url]"

   cd backend
   alembic upgrade head

   # Verify migration
   alembic current
   ```

7. **Verify Deployment Health**:
   ```bash
   # Frontend health (Vercel)
   curl https://keto-meal-plan.vercel.app/

   # Backend health (Render)
   curl https://keto-meal-plan-api.onrender.com/health

   # Database connection
   curl https://keto-meal-plan-api.onrender.com/internal/db-health

   # Redis connection
   curl https://keto-meal-plan-api.onrender.com/internal/redis-health
   ```

8. **Test Critical Endpoints**:
   ```bash
   # Quiz submission endpoint
   curl -X POST https://keto-meal-plan-api.onrender.com/v1/quiz/submit \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","step_1":"male"}'

   # Webhook endpoint (should return 401 without signature)
   curl -X POST https://keto-meal-plan-api.onrender.com/webhooks/paddle
   ```

9. **Configure Environment Variables** (if first deploy):

   **Backend (Render Dashboard)**:
   - DATABASE_URL
   - REDIS_URL
   - OPENAI_API_KEY
   - GEMINI_API_KEY
   - PADDLE_API_KEY
   - PADDLE_WEBHOOK_SECRET
   - BLOB_READ_WRITE_TOKEN
   - RESEND_API_KEY
   - RESEND_FROM_EMAIL
   - SENTRY_DSN
   - JWT_SECRET
   - APP_URL

   **Frontend (Vercel Dashboard)**:
   ```bash
   vercel env add NEXT_PUBLIC_API_URL production
   vercel env add NEXT_PUBLIC_PADDLE_VENDOR_ID production
   vercel env add NEXT_PUBLIC_PADDLE_ENVIRONMENT production
   ```

10. **Output Summary**:
    ```
    ✅ Deployment Summary
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Environment: production
    Branch: main

    Frontend (Vercel):
    ✅ Deployed to: https://keto-meal-plan.vercel.app
    ✅ Build successful
    ✅ Health check: PASS

    Backend (Render):
    ✅ Deployed to: https://keto-meal-plan-api.onrender.com
    ✅ Migrations applied: 5 pending → all applied
    ✅ Health check: PASS
    ✅ Database: Connected
    ✅ Redis: Connected

    Post-Deployment:
    ⚠️ Update Paddle webhook URL to:
       https://keto-meal-plan-api.onrender.com/webhooks/paddle

    ⚠️ Update NEXT_PUBLIC_API_URL in Vercel to:
       https://keto-meal-plan-api.onrender.com/v1

    ⚠️ Test full payment flow in production (test mode):
       1. Complete quiz
       2. Test payment with Paddle test card
       3. Verify email delivery
       4. Check PDF download
    ```

## Example Usage

```bash
/deploy                  # Deploy to staging
/deploy staging          # Deploy to staging
/deploy production       # Deploy to production
/deploy preview          # Create preview deployment
```

## Exit Criteria

- Both frontend and backend deployed successfully
- Database migrations applied
- Health checks pass
- Critical endpoints respond correctly
- Deployment URLs logged

## Post-Deployment Checklist

- [ ] Update Paddle webhook URL in Paddle dashboard
- [ ] Test quiz submission in production
- [ ] Test payment flow with Paddle test card
- [ ] Verify email delivery
- [ ] Check Sentry for errors
- [ ] Monitor Vercel Analytics for traffic
- [ ] Verify cron jobs scheduled correctly
