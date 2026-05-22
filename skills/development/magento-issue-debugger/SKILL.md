---
name: magento-issue-debugger
description: Systematically investigates, diagnoses, and resolves complex Magento 2 technical problems. Use when debugging issues, investigating bugs, analyzing performance problems, resolving errors, or troubleshooting system failures. Masters log analysis, performance profiling, and root cause analysis.
---

# Magento 2 Issue Debugger

Expert specialist in systematically investigating, diagnosing, and resolving complex technical problems across all layers of the Magento stack.

## When to Use

- Debugging production issues
- Investigating bugs and errors
- Analyzing performance problems
- Resolving system failures
- Troubleshooting integration issues
- Diagnosing cache or indexing problems

## Debugging Methodologies

### Systematic Investigation
- **Problem Assessment**: Establish consistent steps to reproduce the problem
- **Environment Documentation**: Catalog system configuration and environment details
- **Impact Analysis**: Determine scope, frequency, and business impact
- **Timeline Analysis**: Establish when the issue started and what changed
- **Isolation Testing**: Disable modules and features to isolate the issue

### Root Cause Analysis
- **Hypothesis Testing**: Form and test theories methodically
- **Data Collection**: Gather logs, configuration, and performance metrics
- **Code Analysis**: Review recent code changes and related modules
- **Database Investigation**: Check for data corruption or migration issues
- **Deep Dive**: Dig deep to find underlying causes rather than treating symptoms

## Issue Investigation Process

### 1. Problem Assessment
- **Issue Reproduction**: Establish consistent steps to reproduce
- **Environment Documentation**: Catalog system configuration
- **Impact Analysis**: Determine scope and business impact
- **Timeline Analysis**: Establish when issue started
- **User Impact**: Understand how issue affects different user types

### 2. Data Collection
- **Log Gathering**: Collect relevant logs from all system components
  - Magento logs: `var/log/`
  - PHP error logs
  - Web server logs (Apache/Nginx)
  - Database slow query logs
- **Configuration Review**: Examine module configurations and system settings
- **Code Analysis**: Review recent code changes and related modules
- **Database Investigation**: Check for data corruption or migration issues
- **Performance Metrics**: Gather timing and resource usage data

### 3. Systematic Debugging
- **Debug Mode**: Enable Magento debug mode for detailed error reporting
  ```bash
  bin/magento deploy:mode:set developer
  ```
- **Xdebug Integration**: Use step-through debugging for complex logic issues
- **Profiling Tools**: Use Blackfire, XHProf, or similar tools for performance issues
- **Database Debugging**: Enable query logging and analyze database interactions
- **Isolation Testing**: Disable modules to isolate the issue

### 4. Resolution Implementation
- **Fix Development**: Implement appropriate fixes based on root cause analysis
- **Testing Strategy**: Develop comprehensive test plans for verification
- **Rollback Planning**: Prepare rollback procedures for production fixes
- **Documentation**: Document findings, solutions, and prevention strategies
- **Monitoring Setup**: Implement monitoring to prevent issue recurrence

## Common Issue Categories

### Performance Issues
- **Slow Page Loading**: Identify bottlenecks in frontend and backend processing
- **Database Performance**: Optimize queries, indexes, and database configuration
- **Memory Issues**: Debug memory leaks and high memory usage
- **Cache Problems**: Resolve cache invalidation and cache warming issues
- **Frontend Performance**: Debug JavaScript errors and CSS rendering issues

### Functional Bugs
- **Checkout Issues**: Debug payment processing, shipping, and order placement
- **Product Display**: Resolve catalog, search, and product page problems
- **Admin Panel Issues**: Fix backend functionality and configuration problems
- **Extension Conflicts**: Identify and resolve module compatibility issues
- **API Problems**: Debug REST and GraphQL API endpoints

### System-Level Issues
- **Installation Problems**: Resolve setup and upgrade issues
- **Configuration Errors**: Fix system and module configuration problems
- **File Permission Issues**: Resolve file system and directory permission problems
- **Cron Job Failures**: Debug scheduled task execution problems
- **Email Issues**: Resolve email sending and template problems

### Security Issues
- **Access Control**: Debug permission and ACL issues
- **Authentication Problems**: Resolve login and session issues
- **CSRF Failures**: Debug form key validation problems
- **SQL Injection**: Identify and fix vulnerable queries
- **XSS Vulnerabilities**: Fix output escaping issues

## Debugging Tools & Techniques

### Log Analysis
- **Magento Logs**: `var/log/exception.log`, `var/log/system.log`
- **PHP Error Logs**: Check PHP-FPM or Apache error logs
- **Web Server Logs**: Analyze Apache/Nginx access and error logs
- **Database Logs**: Review slow query logs and database errors
- **Custom Logging**: Implement custom logging for specific issues

### Performance Profiling
- **Blackfire**: Performance profiling and optimization
- **XHProf**: PHP profiling tool
- **New Relic**: APM monitoring
- **Database Profiling**: Enable query logging
- **Frontend Profiling**: Browser DevTools performance analysis

### Debugging Commands
```bash
# Enable developer mode
bin/magento deploy:mode:set developer

# Clear cache
bin/magento cache:clean
bin/magento cache:flush

# Reindex
bin/magento indexer:reindex

# Check compilation
bin/magento setup:di:compile

# Check static content
bin/magento setup:static-content:deploy

# Check database
bin/magento setup:db:status
```

### Code Debugging
- **Xdebug**: Step-through debugging
- **var_dump/die**: Quick debugging (remove before production)
- **Magento Logger**: Use `\Psr\Log\LoggerInterface` for logging
- **Exception Handling**: Proper exception catching and logging
- **Error Reporting**: Configure error reporting levels

## Best Practices

### Prevention
- **Comprehensive Testing**: Write unit, integration, and functional tests
- **Code Reviews**: Regular code reviews to catch issues early
- **Monitoring**: Implement monitoring and alerting
- **Logging**: Comprehensive logging strategy
- **Documentation**: Maintain clear documentation

### Resolution
- **Root Cause**: Always fix root cause, not symptoms
- **Testing**: Test fixes thoroughly before deployment
- **Documentation**: Document the issue and resolution
- **Communication**: Communicate with stakeholders
- **Monitoring**: Monitor after fix deployment

## References

- [Adobe Commerce Troubleshooting](https://developer.adobe.com/commerce/php/development/)
- [Performance Best Practices](https://developer.adobe.com/commerce/php/best-practices/performance/)
- [Logging](https://developer.adobe.com/commerce/php/development/components/logging/)

Focus on systematic investigation to identify root causes and implement lasting solutions.
