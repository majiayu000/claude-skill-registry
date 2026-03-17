---
name: Project Creation
description: สร้างโปรเจคใหม่ทุก Tech Stack พร้อม setup ที่สมบูรณ์
---

# Project Creation Skill

## Overview

Skill สำหรับสร้างโปรเจคใหม่ทุกประเภท พร้อม configuration และ best practices ที่เหมาะสม

## Capabilities

### Frontend Projects

#### Angular

```bash
npx -y @angular/cli new <project-name> --style=scss --routing=true --ssr=false --skip-tests=false
```

- ใช้ SCSS เป็น default
- เพิ่ม Routing module
- Setup ESLint & Prettier

#### React (Vite)

```bash
npx -y create-vite@latest <project-name> --template react-ts
```

- ใช้ TypeScript เสมอ
- เพิ่ม ESLint, Prettier, Vitest

#### Vue 3 (Vite)

```bash
npx -y create-vue@latest <project-name>
```

- เลือก TypeScript, Vue Router, Pinia
- Setup Vitest & ESLint

#### Next.js

```bash
npx -y create-next-app@latest <project-name> --typescript --tailwind --eslint --app --src-dir
```

- ใช้ App Router
- TypeScript + Tailwind CSS

---

### Backend Projects

#### Spring Boot

```bash
curl https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d language=java \
  -d bootVersion=3.4.1 \
  -d baseDir=<project-name> \
  -d groupId=com.example \
  -d artifactId=<project-name> \
  -d dependencies=web,data-jpa,postgresql,lombok,validation,security \
  -o <project-name>.zip && unzip <project-name>.zip
```

**Default Dependencies:**

- Spring Web
- Spring Data JPA
- PostgreSQL Driver
- Lombok
- Validation
- Spring Security

#### Node.js (Express + TypeScript)

```bash
mkdir <project-name> && cd <project-name>
npm init -y
npm install express cors helmet morgan dotenv
npm install -D typescript @types/node @types/express ts-node nodemon
npx tsc --init
```

**Folder Structure:**

```
src/
├── controllers/
├── services/
├── middlewares/
├── routes/
├── models/
├── utils/
└── index.ts
```

#### Python (FastAPI)

```bash
mkdir <project-name> && cd <project-name>
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

**Folder Structure:**

```
app/
├── api/
├── core/
├── models/
├── schemas/
├── services/
└── main.py
```

---

### Database Setup

#### PostgreSQL

- สร้าง Docker Compose สำหรับ PostgreSQL
- เตรียม migrations folder
- สร้าง connection configuration

#### MongoDB

- สร้าง Docker Compose สำหรับ MongoDB
- Setup connection string
- เตรียม schema/model templates

---

### DevOps Setup

เมื่อสร้างโปรเจคใหม่ ให้สร้างไฟล์เหล่านี้เสมอ:

1. **Dockerfile** - Multi-stage build
2. **docker-compose.yml** - Development environment
3. **.dockerignore** - Exclude unnecessary files
4. **.gitignore** - Proper ignore patterns
5. **.env.example** - Environment variables template
6. **README.md** - Project documentation

---

## Checklist เมื่อสร้างโปรเจคใหม่

- [ ] สร้างโปรเจคด้วย CLI ที่เหมาะสม
- [ ] ตั้งค่า TypeScript (ถ้าเป็น JS/TS project)
- [ ] เพิ่ม ESLint + Prettier
- [ ] สร้าง folder structure ที่เหมาะสม
- [ ] เพิ่ม Docker configuration
- [ ] สร้าง .gitignore และ .env.example
- [ ] Initialize Git repository
- [ ] สร้าง README.md
- [ ] ทดสอบว่า project run ได้
