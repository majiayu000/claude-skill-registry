---
name: magento-module-developer
description: Creates robust, maintainable, and extensible Magento 2 modules following enterprise architecture patterns. Use when developing custom modules, implementing new functionality, creating extensions, or building Magento 2 components. Masters dependency injection, service contracts, repository patterns, and module architecture.
---

# Magento 2 Module Developer

Expert specialist in creating well-architected, maintainable, and extensible Magento 2 modules that seamlessly integrate with Magento's core framework following Adobe Commerce best practices.

## When to Use

- Creating new Magento 2 modules or extensions
- Implementing custom functionality
- Building module architecture and structure
- Setting up module dependencies and configuration
- Implementing service contracts and APIs
- Creating database schemas and data patches

## Module Development Process

### 1. Planning & Architecture
- **Requirements Analysis**: Break down functional and non-functional requirements
- **Architecture Design**: Plan module structure and integration points
- **Database Design**: Design entity relationships and data flow
- **API Design**: Define service contracts and data transfer objects
- **Performance Considerations**: Plan for scalability and optimization

### 2. Module Setup
- **Module Structure**: Create proper directory structure following Magento conventions:
  ```
  app/code/Vendor/ModuleName/
  ├── etc/
  │   ├── module.xml
  │   ├── di.xml
  │   ├── routes.xml
  │   ├── system.xml
  │   ├── acl.xml
  │   └── db_schema.xml
  ├── Model/
  ├── Block/
  ├── Controller/
  ├── Api/
  ├── view/
  └── registration.php
  ```
- **Registration**: Create `registration.php` and `composer.json`
- **Module Declaration**: Create `etc/module.xml` with proper dependencies
- **Version Control**: Set up Git with proper `.gitignore`

### 3. Core Implementation

#### Models & Entities
- Entity models extending `Magento\Framework\Model\AbstractModel`
- Resource models extending `Magento\Framework\Model\ResourceModel\Db\AbstractDb`
- Collections extending `Magento\Framework\Model\ResourceModel\Db\Collection\AbstractCollection`
- Use `db_schema.xml` for database schema definitions

#### Repositories
- Implement repository pattern for data access
- Create repository interfaces in `Api/` directory
- Implement repositories in `Model/` directory
- Use service contracts for clean API interfaces

#### Service Classes
- Business logic in service classes
- Use dependency injection for all dependencies
- Implement service contracts for extensibility

#### Controllers
- Frontend controllers extending `Magento\Framework\App\Action\Action`
- Admin controllers extending `Magento\Backend\App\Action`
- API controllers implementing service contracts

### 4. Configuration Files

#### module.xml
```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="Vendor_ModuleName" setup_version="1.0.0">
        <sequence>
            <module name="Magento_Store"/>
        </sequence>
    </module>
</config>
```

#### di.xml
- Configure dependency injection
- Define preferences, virtual types, plugins
- Use proper scope (global, frontend, adminhtml, webapi_rest, webapi_soap)

#### db_schema.xml
- Define database tables, columns, indexes
- Use proper data types and constraints
- Follow Magento naming conventions

## Design Patterns & Principles

### Service Contracts
- Create interfaces in `Api/` directory
- Implement clean API interfaces
- Use data transfer objects (DTOs) for data exchange
- Maintain backward compatibility

### Repository Pattern
- Separate data access from business logic
- Use repositories for all data operations
- Implement proper error handling
- Support transactions where needed

### Dependency Injection
- Use constructor injection only
- Avoid service locator pattern
- Leverage Magento's DI container
- Use type hints for all dependencies

### Plugin System
- Use plugins to extend functionality
- Prefer before/after plugins over around plugins
- Avoid around plugins unless necessary
- Document plugin execution order

### Event/Observer Pattern
- Dispatch events for extensibility
- Implement observers for loose coupling
- Use proper event naming conventions
- Document event data structure

## Module Components

### Backend Components
- **Models**: Entity models, resource models, collections
- **Repositories**: Data access layer implementations
- **Services**: Business logic and application services
- **Controllers**: Admin controllers and API endpoints
- **Blocks**: Admin interface building blocks
- **UI Components**: Admin grids, forms, and components

### Frontend Components
- **Controllers**: Frontend page controllers and actions
- **Blocks**: View logic and data preparation
- **Templates**: PHTML template files with proper escaping
- **Layout Files**: XML layout configurations
- **JavaScript**: Frontend interaction and AJAX functionality
- **CSS/LESS**: Styling and responsive design

### Database Components
- **db_schema.xml**: Database schema definitions
- **Data Patches**: Data migration and setup scripts
- **Schema Patches**: Database structure modifications
- **Indexers**: Custom search and filter indexers

## Advanced Features

### API Development
- Create REST endpoints with proper authentication
- Implement GraphQL resolvers and schemas
- Design clean API interfaces
- Implement rate limiting and security measures

### Event System Integration
- Dispatch custom events for extensibility
- Implement event observers
- Create before/after/around plugins
- Use virtual types for flexibility

### Caching & Performance
- Implement custom cache types and tags
- Handle cache invalidation properly
- Use lazy loading for expensive operations
- Optimize database queries and joins

### Multi-Store Support
- Handle multi-store configurations
- Implement proper configuration scopes
- Ensure proper data separation
- Support store context switching

## Best Practices

### Code Quality
- Follow PSR-12 and Magento coding standards
- Use `declare(strict_types=1);` in all PHP files
- Implement comprehensive type hinting
- Write unit and integration tests
- Maintain high code coverage

### Security
- Implement input validation
- Use proper output escaping in templates
- Implement CSRF protection
- Enforce proper access control (ACL)
- Handle sensitive data appropriately

### Performance
- Optimize database queries
- Use proper indexes
- Implement caching strategies
- Monitor memory usage
- Optimize collection loading

### Extensibility
- Provide extension points via plugins
- Dispatch events for third-party integration
- Allow configuration without code changes
- Use interface segregation
- Maintain backward compatibility

## Testing

- **Unit Tests**: Test individual classes and methods
- **Integration Tests**: Test module integration with core
- **Functional Tests**: End-to-end test scenarios
- **Static Analysis**: Use PHPStan/Psalm for code quality

## Documentation

- Technical documentation for developers
- User documentation for end users
- API documentation for all public APIs
- Installation guides
- Troubleshooting guides

## References

- [Adobe Commerce Extension Development](https://developer.adobe.com/commerce/php/development/)
- [Coding Standards](https://developer.adobe.com/commerce/php/coding-standards/)
- [Best Practices](https://developer.adobe.com/commerce/php/best-practices/)

Focus on creating modules that are maintainable, extensible, and aligned with Magento's enterprise-grade architecture principles.
