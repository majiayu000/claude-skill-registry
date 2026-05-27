---
name: cloud-app-store
description: Flow Nexus application marketplace and template management. Use for app publishing, discovery, deployment, and marketplace operations.
version: 1.0.0
category: cloud
type: skill
capabilities:
  - app_discovery
  - app_publishing
  - template_deployment
  - analytics_tracking
  - app_management
tools:
  - mcp__flow-nexus__app_search
  - mcp__flow-nexus__app_get
  - mcp__flow-nexus__app_update
  - mcp__flow-nexus__app_analytics
  - mcp__flow-nexus__app_installed
  - mcp__flow-nexus__app_store_publish_app
  - mcp__flow-nexus__app_store_list_templates
  - mcp__flow-nexus__template_list
  - mcp__flow-nexus__template_get
  - mcp__flow-nexus__template_deploy
  - mcp__flow-nexus__market_data
related_skills:
  - cloud-sandbox
  - cloud-workflow
  - cloud-payments
---

# Cloud App Store

> Manage the Flow Nexus application marketplace: discover, publish, deploy, and analyze applications and templates.

## Quick Start

```javascript
// Search for authentication apps
const apps = await mcp__flow-nexus__app_search({
  search: "authentication",
  category: "backend",
  featured: true
});

// Deploy a template
await mcp__flow-nexus__template_deploy({
  template_name: "express-api-starter",
  deployment_name: "my-api",
  variables: {
    api_key: "your_api_key",
    database_url: "postgres://..."
  }
});

// Publish your own app
await mcp__flow-nexus__app_store_publish_app({
  name: "My Auth Service",
  description: "JWT-based authentication microservice",
  category: "backend",
  source_code: sourceCode,
  tags: ["auth", "jwt", "express"]
});
```

## When to Use

- Discovering pre-built applications and templates
- Publishing applications to the marketplace
- Deploying templates for rapid project setup
- Analyzing app performance and user engagement
- Managing installed applications
- Tracking marketplace trends and statistics

## Prerequisites

- Flow Nexus account with active session
- MCP server `flow-nexus` configured
- Publishing requires verified developer status

## Core Concepts

### App Categories

| Category | Description |
|----------|-------------|
| **Web APIs** | RESTful APIs, microservices, backend frameworks |
| **Frontend** | React, Vue, Angular apps and component libraries |
| **Full-Stack** | Complete applications with frontend and backend |
| **CLI Tools** | Command-line utilities and productivity tools |
| **Data Processing** | ETL pipelines, analytics, transformation tools |
| **ML Models** | Pre-trained models, inference services |
| **Blockchain** | Web3, smart contracts, DeFi protocols |
| **Mobile** | React Native apps, mobile-first solutions |

### Template Types

- **Starter Templates**: Basic project scaffolding
- **Feature Templates**: Pre-built feature modules
- **Full Applications**: Complete, deployable apps
- **Component Libraries**: Reusable UI components

## MCP Tools Reference

### App Discovery

```javascript
// Search apps
mcp__flow-nexus__app_search({
  search: "query string",      // Search term
  category: "backend",         // Category filter
  featured: true,              // Featured apps only
  limit: 20                    // Max results (1-100)
})
// Returns: { apps: [{ id, name, description, category, rating }] }

// Get app details
mcp__flow-nexus__app_get({
  app_id: "app_id"
})
// Returns: { id, name, description, version, author, downloads, rating }

// List installed apps
mcp__flow-nexus__app_installed({
  user_id: "user_id"
})
// Returns: { installed_apps: [{ app_id, installed_at, version }] }
```

### Template Management

```javascript
// List templates
mcp__flow-nexus__template_list({
  category: "backend",
  featured: true,
  limit: 20
})

// Alternative: app store templates
mcp__flow-nexus__app_store_list_templates({
  category: "frontend",
  tags: ["react", "typescript"],
  limit: 20
})

// Get template details
mcp__flow-nexus__template_get({
  template_name: "express-api-starter"
})
// Returns: { id, name, description, variables, requirements }

// Deploy template
mcp__flow-nexus__template_deploy({
  template_id: "template_id",    // Or use template_name
  template_name: "express-api-starter",
  deployment_name: "my-project",
  variables: {
    api_key: "key",
    database_url: "postgres://..."
  },
  env_vars: {
    NODE_ENV: "production"
  }
})
// Returns: { deployment_id, url, status }
```

### App Publishing

```javascript
mcp__flow-nexus__app_store_publish_app({
  name: "App Name",
  description: "Detailed description of the app",
  category: "backend",
  source_code: "// Your source code here",
  version: "1.0.0",
  tags: ["tag1", "tag2", "tag3"],
  metadata: {
    author: "Your Name",
    repository: "https://github.com/..."
  }
})
// Returns: { app_id, status, review_pending }
```

### App Management

```javascript
// Update app
mcp__flow-nexus__app_update({
  app_id: "app_id",
  updates: {
    description: "Updated description",
    version: "1.1.0"
  }
})

// Get analytics
mcp__flow-nexus__app_analytics({
  app_id: "app_id",
  timeframe: "30d"           // 24h, 7d, 30d, 90d
})
// Returns: { downloads, active_users, rating, revenue }

// Get market data
mcp__flow-nexus__market_data()
// Returns: { total_apps, total_downloads, trending, categories }
```

## Usage Examples

### Example 1: Finding and Deploying an API Template

```javascript
// Search for API templates
const templates = await mcp__flow-nexus__template_list({
  category: "backend",
  featured: true
});

// Find the Express starter
const expressTemplate = templates.templates.find(
  t => t.name.includes("express")
);

// Get template details
const details = await mcp__flow-nexus__template_get({
  template_id: expressTemplate.id
});

console.log("Required variables:", details.variables);

// Deploy the template
const deployment = await mcp__flow-nexus__template_deploy({
  template_id: expressTemplate.id,
  deployment_name: "my-express-api",
  variables: {
    database_url: process.env.DATABASE_URL,
    jwt_secret: process.env.JWT_SECRET,
    port: "3000"
  },
  env_vars: {
    NODE_ENV: "production"
  }
});

console.log(`Deployed at: ${deployment.url}`);
```

### Example 2: Publishing a New Application

```javascript
// Prepare your application
const sourceCode = `
const express = require('express');
const jwt = require('jsonwebtoken');

const app = express();
app.use(express.json());

// JWT authentication middleware
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });

  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Routes
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  // Authentication logic
  const token = jwt.sign({ username }, process.env.JWT_SECRET);
  res.json({ token });
});

app.get('/protected', authenticate, (req, res) => {
  res.json({ message: 'Protected data', user: req.user });
});

module.exports = app;
`;

// Publish to app store
const published = await mcp__flow-nexus__app_store_publish_app({
  name: "JWT Auth Service",
  description: "A complete JWT authentication service with Express.js. Includes login, token verification, and protected route middleware.",
  category: "backend",
  source_code: sourceCode,
  version: "1.0.0",
  tags: ["authentication", "jwt", "express", "middleware", "security"],
  metadata: {
    author: "Your Name",
    license: "MIT",
    repository: "https://github.com/yourname/jwt-auth-service"
  }
});

console.log(`App published with ID: ${published.app_id}`);
```

### Example 3: Analyzing App Performance

```javascript
// Get your app's analytics
const analytics = await mcp__flow-nexus__app_analytics({
  app_id: "your_app_id",
  timeframe: "30d"
});

console.log(`
App Performance Report (Last 30 Days):
- Total Downloads: ${analytics.downloads}
- Active Users: ${analytics.active_users}
- Average Rating: ${analytics.rating}/5
- Revenue: ${analytics.revenue} rUv credits
`);

// Get market trends
const market = await mcp__flow-nexus__market_data();

console.log(`
Market Overview:
- Total Apps: ${market.total_apps}
- Total Downloads: ${market.total_downloads}
- Trending Categories: ${market.trending.categories.join(', ')}
`);
```

### Example 4: Managing Installed Apps

```javascript
// List installed apps
const installed = await mcp__flow-nexus__app_installed({
  user_id: "your_user_id"
});

for (const app of installed.installed_apps) {
  // Get details for each installed app
  const details = await mcp__flow-nexus__app_get({
    app_id: app.app_id
  });

  console.log(`${details.name} v${app.version} - Installed: ${app.installed_at}`);
}
```

## Execution Checklist

### For App Discovery
- [ ] Search with relevant keywords and filters
- [ ] Review app details and documentation
- [ ] Check ratings and reviews
- [ ] Verify category and template requirements
- [ ] Deploy with appropriate configuration

### For App Publishing
- [ ] Prepare clean, well-documented source code
- [ ] Write comprehensive description
- [ ] Add relevant tags for discoverability
- [ ] Set appropriate version number
- [ ] Include metadata (author, license, repository)
- [ ] Submit for review

## Best Practices

1. **Clear Descriptions**: Write detailed, helpful app descriptions
2. **Proper Tagging**: Use relevant tags for discoverability
3. **Version Management**: Follow semantic versioning
4. **Documentation**: Include README and usage examples
5. **Security Scanning**: Ensure code passes security checks
6. **Regular Updates**: Keep apps updated and maintained

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `app_not_found` | Invalid app_id | Use `app_search` to find valid IDs |
| `publish_failed` | Invalid source code or metadata | Verify all required fields |
| `template_deploy_failed` | Missing required variables | Check template requirements |
| `unauthorized` | Not logged in or insufficient permissions | Authenticate first |
| `duplicate_app_name` | App name already exists | Choose unique name |

## Metrics & Success Criteria

- **App Downloads**: Track total and daily downloads
- **User Rating**: Target >4.0/5 average rating
- **Active Users**: Monitor engagement over time
- **Revenue**: Track rUv credit earnings
- **Deployment Success**: >95% successful deployments

## Integration Points

### With Sandboxes

```javascript
// Deploy template to sandbox for testing
const sandbox = await mcp__flow-nexus__sandbox_create({
  template: "node"
});

await mcp__flow-nexus__template_deploy({
  template_name: "express-api-starter",
  variables: { sandbox_id: sandbox.sandbox_id }
});
```

### With Payments

```javascript
// Track app revenue
const balance = await mcp__flow-nexus__ruv_balance({
  user_id: "publisher_id"
});

// Revenue from published apps appears in balance
```

### Related Skills

- [cloud-sandbox](../cloud-sandbox/SKILL.md) - Execution environments
- [cloud-workflow](../cloud-workflow/SKILL.md) - Workflow automation
- [cloud-payments](../cloud-payments/SKILL.md) - Credit management

## References

- [Flow Nexus App Store](https://flow-nexus.ruv.io/apps)
- [Publishing Guidelines](https://flow-nexus.ruv.io/docs/publishing)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from flow-nexus-app-store agent
