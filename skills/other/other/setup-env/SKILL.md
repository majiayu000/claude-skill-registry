---
description: Environment setup and validation - verify all required environment variables and API connections
handoffs:
  - label: Configure Missing Variables
    agent: backend-engineer
    prompt: Help configure the missing environment variables
    send: false
---

## User Input

```text
$ARGUMENTS
```

Options: `check` (validate only), `create` (create .env from example), empty (validate and report)

## Task

Validate environment setup for the keto meal plan project and test all external API connections.

### Steps

1. **Parse Arguments**:
   - Empty or `check`: Validate all environment variables and connections
   - `create`: Create `.env` files from `.env.example` templates

2. **Check Required Environment Variables**:

   **Backend (.env)**:
   ```bash
   cd backend

   # Required variables
   ENV
   DATABASE_URL
   REDIS_URL
   OPENAI_API_KEY
   GEMINI_API_KEY
   PADDLE_API_KEY
   PADDLE_WEBHOOK_SECRET
   BLOB_READ_WRITE_TOKEN
   RESEND_API_KEY
   RESEND_FROM_EMAIL
   SENTRY_DSN
   JWT_SECRET
   APP_URL
   ```

   **Frontend (.env.local)**:
   ```bash
   cd frontend

   # Required variables
   NEXT_PUBLIC_API_URL
   NEXT_PUBLIC_PADDLE_VENDOR_ID
   NEXT_PUBLIC_PADDLE_ENVIRONMENT
   NEXT_PUBLIC_ENABLE_MID_QUIZ_AUTH
   ```

3. **Validate Each Variable**:
   - Check if variable exists
   - Check if value is not empty
   - Check format (URLs, keys, etc.)

4. **Test API Connections** (if `check` or empty):

   **Database (Neon DB)**:
   ```bash
   cd backend
   python -c "from src.lib.database import engine; engine.connect(); print('✅ Database connection successful')"
   ```

   **Redis**:
   ```bash
   python -c "from src.lib.redis_client import redis_client; redis_client.ping(); print('✅ Redis connection successful')"
   ```

   **OpenAI API**:
   ```bash
   python -c "import openai; openai.api_key='${OPENAI_API_KEY}'; openai.models.list(); print('✅ OpenAI API key valid')"
   ```

   **Vercel Blob**:
   ```bash
   # Test blob upload
   curl -X PUT "https://blob.vercel-storage.com/test.txt" \
     -H "authorization: Bearer ${BLOB_READ_WRITE_TOKEN}" \
     -H "x-content-type: text/plain" \
     -d "test" | grep -q "url" && echo "✅ Vercel Blob token valid"
   ```

   **Resend**:
   ```bash
   curl -X GET "https://api.resend.com/domains" \
     -H "Authorization: Bearer ${RESEND_API_KEY}" | grep -q "object" && echo "✅ Resend API key valid"
   ```

5. **Generate Report**:
   ```
   ✅ Environment Setup Report
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Backend Environment Variables:
   ✅ ENV: development
   ✅ DATABASE_URL: postgresql+asyncpg://...
   ✅ REDIS_URL: redis://localhost:6379/0
   ❌ OPENAI_API_KEY: Not set
   ✅ GEMINI_API_KEY: AIza...
   ...

   Frontend Environment Variables:
   ✅ NEXT_PUBLIC_API_URL: http://localhost:8000/v1
   ❌ NEXT_PUBLIC_PADDLE_VENDOR_ID: Not set
   ...

   API Connection Tests:
   ✅ Database (Neon DB): Connected
   ✅ Redis: Connected
   ❌ OpenAI API: Failed (invalid key)
   ✅ Vercel Blob: Connected
   ✅ Resend: Connected

   Missing Variables: 2
   Failed Connections: 1
   ```

6. **Recommendations**:
   - List missing variables with instructions to set them
   - Suggest running `/setup-env create` to create `.env` files
   - Provide links to service signup pages (Paddle, Vercel Blob, Resend, etc.)

## Example Usage

```bash
/setup-env               # Validate all environment variables and connections
/setup-env check         # Same as above
/setup-env create        # Create .env files from .env.example templates
```

## Exit Criteria

- All required environment variables checked
- API connections tested (if not in create mode)
- Report generated with clear status
- Instructions provided for missing setup

## Notes

- **Sensitive Data**: Never log full API keys or secrets
- **Local Development**: Use `.env.local` for frontend (not committed to git)
- **Production**: All variables must be set in Vercel dashboard
