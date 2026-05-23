---
description: Send test email via Resend to verify template and delivery
---

## User Input

```text
$ARGUMENTS
```

Format: email address (defaults to test@resend.dev)

## Task

Send a test email using the meal plan delivery template to verify email service and rendering.

### Steps

1. **Parse Email Address**:
   ```bash
   TO_EMAIL="${ARGUMENTS:-test@resend.dev}"
   echo "Sending test email to: ${TO_EMAIL}"
   ```

2. **Generate Test PDF** (optional):
   ```bash
   cd backend

   # Use existing test PDF or generate one
   if [ ! -f "tests/fixtures/test_meal_plan.pdf" ]; then
       python -c "
       from src.services.pdf_generator import generate_pdf
       import json

       with open('tests/fixtures/test_meal_plan_weight_loss.json') as f:
           meal_plan = json.load(f)

       generate_pdf(meal_plan, 'tests/fixtures/test_meal_plan.pdf')
       "
   fi
   ```

3. **Send Email via Resend**:
   ```bash
   python -c "
   from src.services.email_service import send_delivery_email
   import asyncio

   async def test():
       result = await send_delivery_email(
           to_email='${TO_EMAIL}',
           pdf_path='tests/fixtures/test_meal_plan.pdf',
           blob_url='https://blob.vercel-storage.com/test.pdf',
           customer_email='${TO_EMAIL}'
       )
       return result

   result = asyncio.run(test())

   if result['success']:
       print('✅ Email sent successfully')
       print(f'   Message ID: {result[\"message_id\"]}')
   else:
       print(f'❌ Email failed: {result[\"error\"]}')
   "
   ```

4. **Alternative: Direct Resend API Test**:
   ```bash
   curl -X POST "https://api.resend.com/emails" \
     -H "Authorization: Bearer ${RESEND_API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{
       "from": "'"${RESEND_FROM_EMAIL}"'",
       "to": ["'"${TO_EMAIL}"'"],
       "subject": "Test: Your Keto Meal Plan",
       "html": "<h1>Test Email</h1><p>This is a test email from the keto meal plan system.</p>"
     }'
   ```

5. **Check Email Delivery** (Resend Dashboard):
   ```bash
   echo "Check email delivery status at:"
   echo "https://resend.com/emails"
   ```

6. **Output Summary**:
   ```
   ✅ Test Email Sent
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Recipient: test@resend.dev
   From: noreply@ketomealplan.com
   Subject: Your Personalized Keto Meal Plan

   Content:
   ✅ HTML template rendered
   ✅ PDF attachment included (487 KB)
   ✅ Recovery instructions included
   ✅ Green theme applied

   Delivery:
   ✅ Sent via Resend
   📧 Message ID: abc-123-def
   ⏱️  Delivery time: 0.8s

   Check your inbox:
   📬 ${TO_EMAIL}

   If using test@resend.dev, check:
   https://resend.com/emails
   ```

## Example Usage

```bash
/test-email                      # Send to test@resend.dev
/test-email user@example.com     # Send to specific address
```

## Exit Criteria

- Test email sent successfully
- Message ID received from Resend
- Email visible in Resend dashboard
- Template rendered correctly
- PDF attachment included

## Testing Notes

- **Resend Test Mode**: Emails to `test@resend.dev` are captured in Resend dashboard
- **Real Emails**: Test with your own email to verify deliverability
- **Template Validation**: Open email to verify green theme, layout, recovery link
