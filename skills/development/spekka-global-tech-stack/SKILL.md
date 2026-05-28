---
name: Global Tech Stack
description: Defines the complete technical stack for the Cawpile video generation service. Use this when making technology choices, adding dependencies, configuring build tools, or setting up infrastructure. Applies to package.json, tsconfig.json, Dockerfile, and architecture decisions.
---

# Global Tech Stack

This Skill provides Claude Code with specific guidance on how it should handle global tech stack.

## When to use this skill:

- Adding new npm dependencies or updating package.json
- Configuring TypeScript compiler options in tsconfig.json
- Working with Docker configuration or deployment setup
- Setting up AWS S3 integration or credential management
- Choosing libraries or frameworks for new features
- Making architectural decisions about service design

## Instructions

Define your technical stack below. This serves as a reference for all team members and helps maintain consistency across the project.

### Framework & Runtime
- **Application Framework:** Express 4.21
- **Language/Runtime:** TypeScript 5.6 on Node.js
- **Package Manager:** npm

### Video Generation
- **Video Engine:** Remotion 4.0
- **Component Framework:** React 18.3 (for Remotion compositions)
- **Video Format:** H.264 codec, 1080x1920 @ 30fps (9:16 TikTok format)
- **Animation System:** Frame-based timing (30fps)

### Storage & Infrastructure
- **Object Storage:** AWS S3 (rendered video storage)
- **Containerization:** Docker with Noto Color Emoji font
- **Credential Management:** Docker Secrets

### Testing & Quality
- **Test Framework:** Vitest (unit and integration tests)
- **Linting:** ESLint with TypeScript rules
- **Path Aliases:** `@/*` maps to `src/*`

### Architecture Patterns
- **Service Model:** Microservice (server-to-server backend for Cawpile.org)
- **Progress Updates:** Server-Sent Events (SSE) for render progress
- **API Design:** RESTful endpoints with Express middleware
