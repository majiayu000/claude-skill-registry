---
name: managing-appwrite-functions
description: Handles backend logic that cannot run in the browser. Use for sensitive tasks like price calculation, cleanup, or payment verification.
---

# Appwrite Server Functions

## When to use this skill
- When logic requires an API Key that shouldn't be exposed.
- For scheduled tasks (CRON jobs like "Cancel Unpaid Bookings").
- For heavy processing that would slow down the frontend.

## Workflow
- [ ] Create a new function in the Appwrite Console.
- [ ] Set runtime to **Node.js**.
- [ ] Use `node-appwrite` SDK inside the function.
- [ ] Trigger via events (e.g., `databases.*.collections.bookings.documents.*.create`) or HTTP.

## Example (Node.js)
```javascript
const sdk = require('node-appwrite');

module.exports = async function (context) {
    const client = new sdk.Client()
        .setEndpoint(process.env.APPWRITE_FUNCTION_ENDPOINT)
        .setProject(process.env.APPWRITE_FUNCTION_PROJECT_ID)
        .setKey(context.req.headers['x-appwrite-key']);

    const databases = new sdk.Databases(client);
    
    // Logic: e.g., Confirm payment with Stripe and update DB
    context.log('Function triggered');
    return context.res.json({ success: true });
};
```

## Instructions
- **Security**: Never hardcode keys in the function code; use Appwrite Function Environment Variables.
- **Runtimes**: Prefer the latest stable Node.js runtime (e.g., 18.x or 20.x).
- **Execution**: Check "Execute" permissions to ensure only authorized users or events can run it.
