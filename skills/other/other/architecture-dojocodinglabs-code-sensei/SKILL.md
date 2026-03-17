---
name: architecture
description: >
  Software architecture, design patterns, and system design concepts. Activated for
  Blue Belt and above when Claude makes significant architectural decisions.
---

# Architecture — CodeSensei Teaching Module

## What is Architecture?
- **Analogy:** Architecture is the floor plan of your application. Just like a building needs a plan before construction, your app needs a structure that determines how all the pieces connect.
- **Key insight:** Bad architecture doesn't break your app today — it makes it painful to change tomorrow. Good architecture makes change easy.

## Client-Server Architecture
- **The pattern:** Frontend (client) ↔ API ↔ Backend (server) ↔ Database
- **Why this split:** Separation of concerns. The frontend handles display, the backend handles logic and data. They can change independently.
- **When to teach:** First time Claude creates both a frontend and backend file in the same project.

## Monolith vs Microservices
- **Monolith:** Everything in one codebase. Like a single restaurant where the kitchen, dining room, and bar are all one business.
- **Microservices:** Each feature is its own mini-app. Like a food court where each stall is independent.
- **Key insight for vibecoders:** Start monolith. Always. Microservices are for when you have scaling problems, not before.

## MVC Pattern
- **Model** — the data layer (what your app knows)
- **View** — the display layer (what the user sees)
- **Controller** — the logic layer (what happens when the user does something)
- **Analogy:** A restaurant. The menu (model) has the dishes. The table presentation (view) is what the customer sees. The waiter (controller) takes orders and coordinates between kitchen and table.

## State Management
- **The problem:** As your app grows, keeping track of data that multiple components need becomes messy.
- **Analogy:** In a small office, everyone shouts across the room. In a big company, you need an organized messaging system (Slack, email).
- **Solutions:** React Context, Redux, Zustand — all solve the same problem differently.

## Caching
- **Analogy:** Instead of cooking every meal from scratch, you prep common ingredients in advance. Caching stores frequently-used data closer to where it's needed so you don't have to fetch it every time.

## Authentication vs Authorization
- **Authentication:** "Who are you?" (login)
- **Authorization:** "What are you allowed to do?" (permissions)
- **Analogy:** Authentication is the bouncer checking your ID. Authorization is the VIP list determining which areas you can access.

## When to Teach Architecture
- Only for Blue Belt and above — beginners should focus on making things work before worrying about structure
- Introduce naturally when Claude makes an architectural choice the user might wonder about
