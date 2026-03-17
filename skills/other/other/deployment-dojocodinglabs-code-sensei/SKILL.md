---
name: deployment
description: >
  Hosting, deployment, CI/CD, and going live. Activated when Claude works with deployment
  configs, Dockerfiles, Vercel/Netlify configs, or deployment-related commands.
---

# Deployment — CodeSensei Teaching Module

## What is Deployment?
- **Analogy:** Deployment is moving from rehearsal to opening night. Your app works on your computer (localhost), and deployment puts it on a server so the whole world can use it.
- **Key insight:** When you run `npm start` on your computer, only YOU can see the app. Deployment puts it on someone else's computer (a server) that's always on and connected to the internet.

## Localhost vs Production
- **localhost** — your computer, only you can access it. The rehearsal stage.
- **Production** — a server in the cloud, anyone with the URL can access it. Opening night.
- **Staging** — a test server that mimics production. The dress rehearsal.

## Common Deployment Platforms
- **Vercel** — one-click deployment for Next.js/React apps. Push to GitHub, it deploys automatically.
- **Netlify** — similar to Vercel, great for static sites and simple apps.
- **Railway / Render** — for backend apps with databases.
- **AWS / GCP / Azure** — the industrial-grade options. More complex but more powerful.
- **Key insight:** For most vibecoded projects, Vercel or Railway is all you need.

## Domains & DNS
- **Analogy:** A domain name (like myapp.com) is a nickname for your server's actual address (an IP like 192.168.1.1). DNS is the phone book that translates names to addresses.
- **Teaching flow:** User types myapp.com → DNS looks up the address → Browser connects to the server → Server sends the app

## Environment Variables in Production
- **Key insight:** Your .env file doesn't get uploaded. You set environment variables SEPARATELY in your hosting platform's dashboard.
- **Why:** Security. Your code is often public (on GitHub), but your secrets shouldn't be.

## CI/CD (Continuous Integration / Continuous Deployment)
- **Analogy:** An automatic assembly line. Every time you push code to GitHub, the system automatically tests it, builds it, and deploys it — without you clicking anything.
- **Key insight:** This is why developers "push to main" to deploy. The pipeline handles the rest.

## Docker (if encountered)
- **Analogy:** A shipping container for your app. It packages your code AND everything it needs to run (right version of Node, right libraries, right settings) into one portable box. That box runs the same everywhere.
- **Dockerfile** — the recipe for building the container
- **Key insight:** Docker solves "it works on my machine" — by shipping the machine too.
