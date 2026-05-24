---
name: config-file-generator
description: Generate configuration files for tools like ESLint, Prettier, TypeScript, and Webpack. Use when setting up project tooling or standardizing configurations.
---

# Config File Generator Skill

各種設定ファイルを生成するスキルです。

## 主な機能

- **ESLint**: .eslintrc.js
- **Prettier**: .prettierrc
- **TypeScript**: tsconfig.json
- **Jest**: jest.config.js
- **Webpack**: webpack.config.js
- **Babel**: babel.config.js
- **EditorConfig**: .editorconfig

## ESLint

```javascript
// .eslintrc.js
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'prettier'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true
    },
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  plugins: ['react', '@typescript-eslint'],
  rules: {
    'no-console': 'warn',
    '@typescript-eslint/no-unused-vars': 'error',
    'react/react-in-jsx-scope': 'off'
  }
};
```

## Prettier

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## .editorconfig

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.py]
indent_size = 4
```

## バージョン情報
- Version: 1.0.0
