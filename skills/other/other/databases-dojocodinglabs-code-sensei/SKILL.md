---
name: databases
description: >
  SQL, databases, ORMs, and data modeling. Activated when Claude works with database code,
  .sql files, Prisma schemas, or database-related npm packages.
---

# Databases — CodeSensei Teaching Module

## What is a Database?
- **Analogy:** A super-powered spreadsheet that your app can read and write to automatically. Each "table" is like a sheet, each "row" is an entry, each "column" is a field.
- **Key insight:** Without a database, your app forgets everything when it restarts. Databases make data PERMANENT.

## SQL (Structured Query Language)
- **Analogy:** SQL is the language you use to talk to the database. Like asking a librarian: "Find me all books by this author, sorted by year."
- **Essential operations:**
  - `SELECT` — "Show me data" → `SELECT * FROM users` (show all users)
  - `INSERT` — "Add new data" → `INSERT INTO users (name, email) VALUES ('Juan', 'juan@email.com')`
  - `UPDATE` — "Change existing data" → `UPDATE users SET name = 'Juan C' WHERE id = 1`
  - `DELETE` — "Remove data" → `DELETE FROM users WHERE id = 1`
  - `WHERE` — "But only the ones that match this condition"
- **Quiz:** "Which SQL word would you use to find all users who signed up today?"

## Types of Databases
- **PostgreSQL** — the reliable all-rounder. Most vibecoded apps use this. Think of it as Excel but 1000x more powerful.
- **SQLite** — a lightweight database stored in a single file. Good for small projects. Like a notepad vs a full filing system.
- **MongoDB** — stores data as flexible documents (JSON-like) instead of rigid tables. Like storing folders of papers vs a spreadsheet.

## ORMs (Object-Relational Mappers)
- **Analogy:** An ORM is a translator between your code and the database. Instead of writing SQL directly, you write code in your programming language and the ORM converts it to SQL.
- **Prisma** (most common in vibecoded projects):
  - `prisma.user.findMany()` → becomes `SELECT * FROM users`
  - `prisma.user.create({ data: { name: "Juan" } })` → becomes `INSERT INTO users...`
- **Key insight:** ORMs make databases easier to work with, but the SQL is still happening underneath.

## Schemas & Migrations
- **Schema** — the blueprint of your database. Defines what tables exist and what columns each has.
- **Migration** — a change to the blueprint. Like remodeling a room — you write instructions for the change, then apply them.
- **Analogy:** The schema is your building's floor plan. A migration is the renovation permit that says "add a new room here."

## Relationships
- **One-to-Many:** One user has many posts. Like one author writing many books.
- **Many-to-Many:** Users can have many tags, and tags can belong to many users. Like students and classes.
- **Foreign Key:** The link that connects tables. Like a reference number that says "this post belongs to user #5."
