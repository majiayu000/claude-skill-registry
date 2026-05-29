---
name: config-setup
description: Sets up configuration files, environment variables, and project configuration. Use when setting up project configuration, environment setup, or configuration management. Creates config files, .env examples, and configuration documentation.
---

# Config Setup Skill

## Instructions

1. Analyze configuration requirements from task
2. Identify what needs to be configured (database, API keys, environment, etc.)
3. Create configuration files
4. Set up environment variable management
5. Create .env.example file
6. Document configuration
7. Return implementation with:
   - Configuration files
   - Environment variable setup
   - .env.example file
   - Configuration documentation

## Examples

**Input:** "Set up environment configuration"
**Output:**
```javascript
// config/index.js
require('dotenv').config();

module.exports = {
    port: process.env.PORT || 3000,
    database: {
        host: process.env.DB_HOST || 'localhost',
        port: process.env.DB_PORT || 5432,
        name: process.env.DB_NAME,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD
    },
    jwt: {
        secret: process.env.JWT_SECRET,
        expiresIn: process.env.JWT_EXPIRES_IN || '24h'
    },
    nodeEnv: process.env.NODE_ENV || 'development'
};
```

```bash
# .env.example
PORT=3000
NODE_ENV=development

DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=

JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=24h
```

## Configuration Areas

- **Environment Variables**: .env files, environment setup
- **Application Config**: App configuration, feature flags
- **Database Config**: Database connection, migration config
- **API Config**: External API keys, endpoints
- **Build Config**: Build tools, bundlers, compilers
- **Deployment Config**: Deployment-specific settings
- **Development Config**: Local development setup

## Best Practices

- **No Secrets in Code**: Use environment variables for secrets
- **.env.example**: Provide example file with all required variables
- **Documentation**: Document all configuration options
- **Validation**: Validate configuration on startup
- **Defaults**: Provide sensible defaults where appropriate
- **Environment-Specific**: Different configs for dev/staging/prod
