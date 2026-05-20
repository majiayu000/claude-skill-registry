---
name: backend
description: >
  Servers, routes, APIs, and backend architecture. Activated when Claude creates server-side
  code, API routes, or Express/Fastify/Next.js API handlers.
---

# Backend Development — CodeSensei Teaching Module

## What is a Backend?
- **Analogy:** If your website is a restaurant, the frontend is the dining room (what customers see) and the backend is the kitchen (where the real work happens). The backend stores data, processes requests, handles logins, and talks to databases.
- **Key insight:** The backend runs on a SERVER (a computer somewhere in the cloud), not in the user's browser.

## Servers
- **Analogy:** A server is like a receptionist. It sits there waiting for requests ("I want to see the homepage" or "save this form data"), then responds appropriately.
- **Express.js** is the most common server framework in vibecoded projects. It's like a template for building that receptionist — you tell it "when someone asks for X, do Y."

## Routes / Endpoints
- **Analogy:** Routes are like departments in a company. `/api/users` is the Users department. `/api/products` is Products. Each one handles specific requests.
- **HTTP Methods (the verbs):**
  - `GET` — "Give me data" (reading)
  - `POST` — "Here's new data, save it" (creating)
  - `PUT`/`PATCH` — "Update this existing data" (editing)
  - `DELETE` — "Remove this data" (deleting)
- **Quiz:** "If someone fills out a signup form, which HTTP method sends their data to the server?"

## APIs (Application Programming Interfaces)
- **Analogy:** An API is a menu at a restaurant. It lists what you can order (available requests), what you need to provide (required data), and what you'll get back (the response). You don't need to know HOW the kitchen cooks it — you just order from the menu.
- **REST API** — the most common style. Uses URLs as addresses and HTTP methods as actions.
- **Key insight:** APIs are how different programs talk to each other. Your frontend talks to your backend via an API. Your backend might talk to Stripe's API for payments or Google's API for maps.

## Request & Response Cycle
```
User clicks "Submit"
    ↓
Frontend sends HTTP request to backend
    ↓
Backend receives request, processes it
    ↓
Backend talks to database if needed
    ↓
Backend sends response back
    ↓
Frontend displays the result
```

## Middleware
- **Analogy:** Security checkpoints before entering a building. Before a request reaches its destination (route), it passes through middleware that can check if you're logged in, log the visit, parse the data, etc.
- **Common middleware:** Authentication check, request body parser, error handler, CORS

## Environment & Security
- **API Keys** — passwords for using external services. NEVER put them in your code directly.
- **`.env` files** — where secrets live, read by the server but never sent to users
- **CORS** — browser security that prevents random websites from accessing your API
