---
name: code_formatter
router_kit: FullStackKit
description: Otomatik kod formatlama, Prettier/ESLint entegrasyonu ve kod stil tutarlılığı rehberi.
metadata:
  skillport:
    category: development
    tags: [big data, cleaning, code formatter, csv, data analysis, data engineering, data science, database, etl pipelines, export, import, json, machine learning basics, migration, nosql, numpy, pandas, python data stack, query optimization, reporting, schema design, sql, statistics, transformation, visualization]      - code-style
---

# 🎨 Code Formatter

> Otomatik kod formatlama ve stil tutarlılığı rehberi.

---

## 📋 Prettier Yapılandırması

### .prettierrc
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80,
  "bracketSpacing": true,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

### Komutlar
```bash
# Format single file
npx prettier --write src/file.ts

# Format all files
npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}"

# Check without writing
npx prettier --check "src/**/*"
```

---

## 🔧 ESLint Entegrasyonu

### .eslintrc.js
```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'prettier', // Prettier çakışmalarını devre dışı bırakır
  ],
  plugins: ['@typescript-eslint', 'react'],
  rules: {
    'no-console': 'warn',
    'no-unused-vars': 'error',
  },
};
```

### Komutlar
```bash
# Lint
npx eslint src/

# Lint and fix
npx eslint src/ --fix

# Specific files
npx eslint "src/**/*.{ts,tsx}"
```

---

## 🔄 Git Hooks (Husky + lint-staged)

### package.json
```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,css,md}": [
      "prettier --write"
    ]
  }
}
```

### Setup
```bash
npx husky-init && npm install
npx husky add .husky/pre-commit "npx lint-staged"
```

---

## 📁 Ignore Files

### .prettierignore
```
node_modules/
dist/
build/
.next/
coverage/
*.min.js
```

### .eslintignore
```
node_modules/
dist/
build/
*.config.js
```

---

*Code Formatter v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Prettier Docs](https://prettier.io/docs/en/install.html)

### Aşama 1: Installation
- [ ] **Packages**: `prettier`, `eslint` ve ilgili pluginleri kur.
- [ ] **Config**: `.prettierrc` ve `.eslintrc` dosyalarını kök dizine ekle.
- [ ] **Ignore**: `.prettierignore` dosyasına `build/`, `dist/` ekle.

### Aşama 2: Automation
- [ ] **Scripts**: `package.json` içine `format` ve `lint` scriptlerini ekle.
- [ ] **VS Code**: `.vscode/settings.json` ile "Format on Save" aç.
- [ ] **Hooks**: Husky ve lint-staged ile commit öncesi kontrol ekle.

### Aşama 3: CI Integration
- [ ] **Pipeline**: CI sürecine `npm run lint` ve `prettier --check` adımlarını ekle.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | `npm run format` çalışınca dosyalar değişiyor mu? |
| 2 | Hatalı bir kod commit edilmeye çalışıldığında Husky engelliyor mu? |
| 3 | CI pipeline format hatası olduğunda fail ediyor mu? |
