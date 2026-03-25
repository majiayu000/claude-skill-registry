---
name: webmcp-commerce-tools
description: Implement commerce-specific WebMCP tools — product search, cart management, checkout, returns, subscriptions, and support. Use when building agentic shopping experiences on e-commerce websites.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WebMCP Commerce Tools

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.chrome.com/blog/webmcp` for commerce-related examples and guidance
2. Web-search `webmcp agentic commerce e-commerce tools examples` for community implementations
3. Web-search `webmcp shopping agent checkout cart tools` for commerce workflow patterns
4. Web-search `site:github.com webmcp commerce` for open-source commerce tool implementations

## Conceptual Architecture

### Agentic Shopping Flow

A typical agent-driven shopping session using WebMCP:

```
User: "Find me wireless headphones under $100"
  → Agent navigates to retailer site
  → Site registers tools: [searchProducts, viewDetails, addToCart, checkout]
  → Agent calls searchProducts(query="wireless headphones", maxPrice=100)
  → Site returns structured product list
  → Agent presents results to user
  → User: "Add the Sony ones to my cart"
  → Agent calls addToCart(productId="sony-wh-1000", quantity=1)
  → Agent: "Added! Proceed to checkout?"
  → User: "Yes, use my saved card"
  → Agent calls checkout(useSavedPayment=true)
  → Site: requestUserInteraction → User confirms → Order placed
  → Agent: "Order #1234 confirmed!"
```

### Core Commerce Tool Set

Every e-commerce site should consider these tool categories:

#### 1. Product Discovery
- `searchProducts(query, filters)` — Catalog search with optional filters
- `getCategories()` — List product categories
- `viewProductDetails(productId)` — Full product info, images, reviews
- `compareProducts(productIds)` — Side-by-side comparison

#### 2. Cart Management
- `addToCart(productId, quantity, variant)` — Add item to cart
- `removeFromCart(itemId)` — Remove item from cart
- `updateCartQuantity(itemId, quantity)` — Change quantity
- `getCartContents()` — View current cart
- `applyCoupon(code)` — Apply a discount code

#### 3. Checkout
- `getShippingOptions(address)` — Available shipping methods and costs
- `checkout(paymentMethod, shippingOption)` — Complete purchase
- `getOrderSummary()` — Pre-checkout order review

#### 4. Order Management
- `getOrderHistory(filters)` — Past orders with optional date/status filters
- `getOrderStatus(orderId)` — Track a specific order
- `initiateReturn(orderId, items, reason)` — Start a return
- `cancelOrder(orderId)` — Cancel a pending order

#### 5. Account & Subscriptions
- `manageSubscription(action, planId)` — Upgrade, downgrade, cancel subscriptions
- `getSubscriptionDetails()` — Current subscription info
- `updateShippingAddress(address)` — Update default address

#### 6. Support
- `createSupportTicket(type, description)` — Open a support case
- `checkTicketStatus(ticketId)` — Check on existing ticket

### Tool Design Principles for Commerce

1. **Mirror existing APIs** — Tool execute callbacks should call your existing REST/GraphQL APIs
2. **Reuse session** — Tools run in the user's authenticated browser session; no extra auth needed
3. **Structured returns** — Return JSON with consistent structure (items array, totals, status)
4. **Progressive disclosure** — Start with search and browse tools; add checkout only for authenticated users
5. **Confirmation gates** — Require user interaction for anything involving money

### Multi-Site Agent Workflows

Agents can navigate across multiple retailer sites:
1. Search on Site A using WebMCP → get results
2. Search on Site B using WebMCP → get results
3. Compare across sites at the agent level
4. Purchase from the best option using that site's checkout tool

Each site maintains its own tools; the agent coordinates across them.

### Integration with Backend Protocols

WebMCP tools can delegate to backend protocols:
- **UCP endpoint** — `searchProducts` tool calls a UCP product discovery API
- **Stripe Checkout** — `checkout` tool creates a Stripe session server-side
- **Inventory service** — Tools check real-time stock via internal APIs

### Best Practices

- Expose tools progressively: read-only tools for all visitors, transactional tools for logged-in users
- Return pagination info for list results (total, page, hasMore)
- Include product images/thumbnails in results as URLs (agents can display them)
- Handle out-of-stock gracefully — return clear status, not errors
- Test the full purchase flow with an AI agent end-to-end
- Consider mobile/responsive — tools should work regardless of viewport

Fetch the latest WebMCP examples and commerce community patterns before building your tool set.
