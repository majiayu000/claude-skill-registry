---
name: api-route
description: Create a new Next.js API route with x402 micropayment middleware
disable-model-invocation: true
argument-hint: "<path> [price]"
---

# Create API Route with x402

Create a new API route: **$ARGUMENTS**

## x402 Pricing Reference (from IMPLEMENTATION_CHECKLIST.md)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `/api/solar/irradiance` | 0.001 USDC | Real-time solar data |
| `/api/grid/carbon` | 0.002 USDC | Carbon intensity |
| `/api/buildings/area` | 0.005 USDC | Building footprints |
| `/api/geocode/search` | 0.001 USDC | Address geocoding |
| `/api/premium/analytics` | 0.01 USDC | Premium aggregated data |

## File Structure

```
src/pages/api/
├── solar/
│   └── irradiance.ts
├── grid/
│   └── carbon.ts
├── buildings/
│   └── area.ts
├── geocode/
│   └── search.ts
└── premium/
    └── analytics.ts
```

## API Route Template

```typescript
// src/pages/api/{path}.ts
import type { NextApiRequest, NextApiResponse } from "next";

// Types for this endpoint
interface ResponseData {
  // Define response shape
}

interface ErrorResponse {
  error: string;
  message: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData | ErrorResponse>
) {
  // Only allow GET requests (or POST if needed)
  if (req.method !== "GET") {
    return res.status(405).json({
      error: "Method not allowed",
      message: "Only GET requests are supported"
    });
  }

  try {
    // Extract query parameters
    const { lat, lng } = req.query;

    // Validate required parameters
    if (!lat || !lng) {
      return res.status(400).json({
        error: "Bad request",
        message: "Missing required parameters: lat, lng"
      });
    }

    // TODO: Add x402 middleware check here
    // const paymentValid = await verifyX402Payment(req);
    // if (!paymentValid) {
    //   return res.status(402).json({ error: "Payment required" });
    // }

    // Fetch from upstream API
    const data = await fetchUpstreamData(
      parseFloat(lat as string),
      parseFloat(lng as string)
    );

    // Return response with caching headers
    res.setHeader("Cache-Control", "s-maxage=300, stale-while-revalidate");
    return res.status(200).json(data);

  } catch (error) {
    console.error("API error:", error);
    return res.status(500).json({
      error: "Internal server error",
      message: "Failed to fetch data"
    });
  }
}

async function fetchUpstreamData(lat: number, lng: number): Promise<ResponseData> {
  // Implement upstream API call
  throw new Error("Not implemented");
}
```

## x402 Middleware Pattern (Future)

```typescript
// src/lib/x402/middleware.ts
import { X402_PRICING } from "./config";

export async function withX402(
  req: NextApiRequest,
  res: NextApiResponse,
  endpoint: string,
  handler: () => Promise<void>
) {
  const pricing = X402_PRICING[endpoint];

  // Check for valid payment header
  const paymentHeader = req.headers["x-402-payment"];

  if (!paymentHeader && !pricing.freeTier) {
    return res.status(402).json({
      error: "Payment required",
      price: pricing.price,
      description: pricing.description,
    });
  }

  // Verify payment signature...

  return handler();
}
```

## Upstream API Clients

Create corresponding client in `src/lib/api/`:

- `openMeteo.ts` - Solar irradiance data
- `electricityMaps.ts` - Carbon intensity
- `overpass.ts` - Building footprints (OSM)
- `nominatim.ts` - Geocoding

## Checklist

- [ ] Create API route file in correct path under `src/pages/api/`
- [ ] Define TypeScript interfaces for request/response
- [ ] Add input validation
- [ ] Add error handling with proper status codes
- [ ] Add caching headers where appropriate
- [ ] Create upstream API client in `src/lib/api/` if needed
- [ ] Document x402 pricing in config
- [ ] Test with curl/Postman
