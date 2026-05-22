---
name: api-fetch-with-auth
description: Create authenticated API fetch function in Next.js. Use for frontend API calls.
---
# APIFetchWithAuth Instructions
Input: Endpoint, method, body.
Output: Fetch function.
Steps:
1. Import getSession from better-auth/nextjs.
2. Attach Bearer token.
Example Code:
import { getSession } from 'better-auth/nextjs';
async function apiFetch(url: string, method: string, body?: any) {
  const session = await getSession();
  const token = session?.token;
  return fetch(url, {
    method,
    headers: { Authorization: `Bearer ${token}` },
    body: body ? JSON.stringify(body) : undefined,
  });
}