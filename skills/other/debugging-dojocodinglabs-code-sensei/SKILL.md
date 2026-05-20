---
name: debugging
description: >
  Reading errors, troubleshooting, and fixing bugs. Activated when Claude encounters errors
  or when the user is debugging. Teaches the most valuable skill: understanding what went wrong.
---

# Debugging — CodeSensei Teaching Module

## What is Debugging?
- **Analogy:** Debugging is detective work. Something isn't working, and you need to find out why. Every error message is a clue.
- **Key insight:** Errors are NOT failures. They're the computer telling you exactly what went wrong and where. Learning to read errors is the single most valuable programming skill.

## How to Read Error Messages
Teach users to look for these three things in EVERY error:

1. **What happened** — the error type (TypeError, SyntaxError, 404, etc.)
2. **Where it happened** — the file name and line number
3. **Why it happened** — the description message

Example:
```
TypeError: Cannot read property 'name' of undefined
    at UserCard (src/components/UserCard.jsx:12)
```
Translation: "On line 12 of UserCard.jsx, you tried to get `.name` from something that doesn't exist yet."

## Common Error Types (teach as encountered)

### Frontend Errors
- **"Cannot read property X of undefined"** — you're trying to use data that hasn't loaded yet. Like trying to read a book that hasn't been delivered.
- **"X is not defined"** — you're using a variable/function that doesn't exist. Likely a typo or missing import.
- **"X is not a function"** — you're trying to call something as a function, but it's not one.
- **White screen of death** — usually a component crashed during rendering. Check the browser console.

### Backend Errors
- **404 Not Found** — the URL/route doesn't exist. Like going to a room number that doesn't exist in the building.
- **500 Internal Server Error** — something broke on the server. Check the server logs.
- **401 Unauthorized** — you're not logged in (or your token expired).
- **403 Forbidden** — you're logged in but don't have permission.
- **CORS error** — your frontend is trying to talk to a backend that doesn't trust it. Like calling a secure building and not being on the approved list.

### Database Errors
- **"relation X does not exist"** — the table hasn't been created yet. Run your migrations.
- **"unique constraint violation"** — you're trying to add a duplicate entry (like two users with the same email).
- **"null value in column X violates not-null constraint"** — you forgot to include a required field.

## The Debugging Mindset
1. **Don't panic** — errors are normal. Every developer sees them constantly.
2. **Read the error** — the answer is usually right there in the message.
3. **Google the error** — copy the exact error message. Someone has had this problem before.
4. **Check what changed** — what did you (or Claude) do right before it broke?
5. **Isolate the problem** — narrow down which part is broken.

## Teaching Opportunity
Every error is a learning moment. When Claude fixes an error, explain:
- What the error meant
- Why it happened
- How it was fixed
- How to prevent it next time

This is where real engineering intuition is built.
