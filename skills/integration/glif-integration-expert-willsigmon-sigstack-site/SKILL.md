---
name: glif-integration-expert
description: Integrate Glif into apps, Discord bots, and web projects. Use when building Glif-powered features.
allowed-tools: Read, Edit, Bash
---

# Glif Integration Expert

Embed Glif AI workflows into applications and services.

## Integration Options

### 1. Direct API (Server-side)

**Node.js/TypeScript:**
```typescript
async function runGlif(glifId: string, inputs: string[]) {
  const res = await fetch('https://simple-api.glif.app', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.GLIF_API_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: glifId, inputs })
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error);
  return data.output;
}
```

**Python:**
```python
import requests

def run_glif(glif_id: str, inputs: list[str]) -> str:
    res = requests.post(
        'https://simple-api.glif.app',
        headers={'Authorization': f'Bearer {GLIF_API_TOKEN}'},
        json={'id': glif_id, 'inputs': inputs}
    )
    data = res.json()
    if 'error' in data:
        raise Exception(data['error'])
    return data['output']
```

### 2. Cloudflare Worker (Serverless)

```javascript
export default {
  async fetch(request, env) {
    const { glifId, inputs } = await request.json();

    const res = await fetch('https://simple-api.glif.app', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.GLIF_API_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id: glifId, inputs })
    });

    return new Response(await res.text(), {
      headers: { 'Access-Control-Allow-Origin': '*' }
    });
  }
};
```

### 3. Next.js API Route

```typescript
// app/api/glif/route.ts
export async function POST(request: Request) {
  const { glifId, inputs } = await request.json();

  const res = await fetch('https://simple-api.glif.app', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.GLIF_API_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: glifId, inputs })
  });

  return Response.json(await res.json());
}
```

### 4. Discord Bot

```javascript
client.on('messageCreate', async (message) => {
  if (message.content.startsWith('!generate ')) {
    const prompt = message.content.slice(10);
    await message.reply('Generating...');

    const result = await runGlif('YOUR_GLIF_ID', [prompt]);
    await message.reply(result); // Image URL or text
  }
});
```

## Embedding Options

### Iframe Embed
```html
<iframe
  src="https://glif.app/glifs/GLIF_ID/embed"
  width="400"
  height="600"
  frameborder="0">
</iframe>
```

### Custom Player
Use Glif's embed SDK for custom styling and callbacks.

## n8n Integration

**HTTP Request Node:**
- Method: POST
- URL: `https://simple-api.glif.app`
- Headers: `Authorization: Bearer {{$credentials.glifApi.token}}`
- Body: `{"id": "GLIF_ID", "inputs": ["{{$json.prompt}}"]}`

## Best Practices

1. **Store tokens in env vars** - Never commit API tokens
2. **Handle async properly** - Glif calls can take 10-60s
3. **Cache results** - Same inputs = same outputs
4. **Show loading states** - Users need feedback
5. **Rate limit client-side** - Prevent credit drain
6. **Validate inputs** - Check before sending to API

## Error Handling

```typescript
const data = await res.json();

if (data.error) {
  // Glif-level error (bad inputs, model failure)
  console.error('Glif error:', data.error);
}

if (data.price === 0 && !data.output) {
  // Likely auth or quota issue
  console.error('Possible auth/quota issue');
}
```

## Useful Glif IDs

Find popular glifs at https://glif.app/explore
Copy ID from URL: `glif.app/glifs/{THIS_PART}`
