# 🔧 Environment Setup Skill

---
name: env-setup
description: Setup and configure development environments for various tech stacks
---

## 🎯 Purpose

ตั้งค่า development environment สำหรับ tech stacks ต่างๆ อย่างถูกต้องและครบถ้วน

## 📋 When to Use

- Start new project
- Onboard new developer
- Setup CI/CD
- Configure new machine
- Troubleshoot env issues

## 🔧 Environment Components

### 1. Package Managers
```bash
# Node.js
nvm install 20
nvm use 20
npm install -g pnpm

# Python
pyenv install 3.11
pyenv local 3.11
pip install pipenv
```

### 2. Editor Config
```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true
```

### 3. Environment Variables
```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/db
API_KEY=your-api-key
NODE_ENV=development
```

### 4. Git Hooks
```bash
# Setup husky
npx husky-init && npm install
npx husky add .husky/pre-commit "npm run lint"
npx husky add .husky/commit-msg "npx commitlint --edit $1"
```

## 📝 Project Setup Templates

### React/Vite
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

### Next.js
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint
cd my-app
npm run dev
```

### Python/FastAPI
```bash
mkdir my-api && cd my-api
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
```

## 📋 Environment Checklist

### Development
- [ ] Node.js version correct
- [ ] Package manager installed
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Editor extensions installed
- [ ] Git hooks configured
- [ ] Database running
- [ ] Dev server works

### Production
- [ ] Build succeeds
- [ ] Env vars configured
- [ ] Database migrated
- [ ] SSL configured
- [ ] Logs configured
- [ ] Health checks work

## 🔧 Common Issues

| Issue | Solution |
|-------|----------|
| Node version wrong | Use nvm |
| Deps not installing | Clear cache, reinstall |
| Env vars undefined | Check .env, restart |
| Port in use | Kill process or change port |

## ✅ Setup Verification

```bash
# Check versions
node --version
npm --version
python --version

# Check env
echo $DATABASE_URL

# Test build
npm run build

# Run tests
npm test
```

## 🔗 Related Skills

- `project-setup` - Full project setup
- `containerization` - Docker setup
- `ci-cd-pipeline` - CI/CD setup
