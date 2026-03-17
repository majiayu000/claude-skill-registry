# Rollback Procedures

> **Skill Purpose:** Deployment failure recovery and rollback strategies

---

## Core Skill Pattern

**Objective:** Establish reliable rollback procedures to quickly recover from failed deployments and maintain service availability.

**Universal Pattern:**
1. Define rollback triggers and failure criteria
2. Create automated rollback mechanisms
3. Establish manual rollback procedures
4. Set up rollback verification and monitoring
5. Create post-rollback analysis and improvement processes

**Key Decisions (Project-Specific):**
- Rollback triggers and thresholds
- Automation vs manual rollback decisions
- Rollback speed vs verification trade-offs
- Communication and notification procedures
- Post-incident analysis requirements

---

## Project-Specific Implementation Notes

**Customize per project:**
- Rollback triggers based on application criticality
- Automation level based on team expertise and risk tolerance
- Verification procedures based on complexity and dependencies
- Communication based on stakeholder needs
- Analysis depth based on learning and improvement goals

---

## Example Implementation (Standard Deployment Rollback Pattern)

> **Note:** This is an example pattern. Adapt rollback triggers and procedures based on your specific deployment platform and risk tolerance.

### Prerequisites (Example)
- Deployment platform configured
- Monitoring and alerting in place
- Team incident response procedures defined

---

## Example: Standard Deployment Rollback Implementation

> **Framework-Specific Example:** This demonstrates the pattern using standard rollback procedures. Adapt for your deployment platform and risk requirements.

### 1. Create Rollback Configuration

Create `rollback.config.js`:

```javascript
module.exports = {
  // Rollback settings
  rollback: {
    // Maximum number of previous deployments to keep
    maxPreviousDeployments: 10,
    
    // Time window for automatic rollback (in minutes)
    autoRollbackWindow: 15,
    
    // Error rate threshold for automatic rollback
    errorRateThreshold: 0.1, // 10%
    
    // Response time threshold for automatic rollback (in ms)
    responseTimeThreshold: 5000,
    
    // Health check failures threshold
    healthCheckThreshold: 3,
    
    // Rollback strategies
    strategies: {
      'immediate': {
        description: 'Immediate rollback to previous deployment',
        conditions: ['critical_error', 'health_check_failure'],
        approval: false,
      },
      'gradual': {
        description: 'Gradual rollback with traffic shifting',
        conditions: ['high_error_rate', 'slow_response'],
        approval: true,
      },
      'manual': {
        description: 'Manual rollback with user confirmation',
        conditions: ['user_initiated', 'performance_degradation'],
        approval: true,
      },
    },
  },
  
  // Monitoring settings
  monitoring: {
    // Health check endpoints
    healthEndpoints: [
      '/health',
      '/api/health',
      '/api/status',
    ],
    
    // Metrics to monitor
    metrics: [
      'error_rate',
      'response_time',
      'throughput',
      'cpu_usage',
      'memory_usage',
    ],
    
    // Alerting thresholds
    alerts: {
      error_rate: {
        warning: 0.05, // 5%
        critical: 0.1,  // 10%
      },
      response_time: {
        warning: 2000,  // 2s
        critical: 5000, // 5s
      },
      health_check: {
        failure_threshold: 3,
      },
    },
  },
  
  // Deployment platforms
  platforms: {
    vercel: {
      rollbackCommand: 'vercel rollback',
      listCommand: 'vercel ls',
      promoteCommand: 'vercel promote',
    },
    netlify: {
      rollbackCommand: 'netlify rollback',
      listCommand: 'netlify deploys:list',
      promoteCommand: 'netlify deploys:create',
    },
    aws: {
      rollbackCommand: 'aws deploy rollback',
      listCommand: 'aws deploy list',
      promoteCommand: 'aws deploy push',
    },
  },
  
  // Notification settings
  notifications: {
    channels: ['slack', 'email', 'webhook'],
    recipients: ['dev-team@zeus-framework.dev', 'ops-team@zeus-framework.dev'],
    templates: {
      rollback_initiated: 'rollback-initiated',
      rollback_completed: 'rollback-completed',
      rollback_failed: 'rollback-failed',
    },
  },
};
```

### 2. Create Rollback Manager

Create `scripts/rollback-manager.js`:

```javascript
#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const config = require('../rollback.config');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36c',
  magenta: '\x1b[35m',
};

function colorLog(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

class RollbackManager {
  constructor() {
    this.platform = this.detectPlatform();
    this.deploymentHistory = [];
    this.currentDeployment = null;
  }

  detectPlatform() {
    // Detect deployment platform based on environment variables or config files
    if (process.env.VERCEL_ENV) {
      return 'vercel';
    } else if (fs.existsSync('netlify.toml')) {
      return 'netlify';
    } else if (fs.existsSync('aws-deploy.json')) {
      return 'aws';
    } else {
      return 'vercel'; // Default to Vercel
    }
  }

  async getDeploymentHistory() {
    colorLog('📋 Getting deployment history...', 'blue');
    
    try {
      const platformConfig = config.platforms[this.platform];
      const output = execSync(platformConfig.listCommand, { encoding: 'utf8' });
      
      // Parse deployment history based on platform
      let deployments = [];
      
      if (this.platform === 'vercel') {
        deployments = this.parseVercelDeployments(output);
      } else if (this.platform === 'netlify') {
        deployments = this.parseNetlifyDeployments(output);
      }
      
      this.deploymentHistory = deployments;
      this.currentDeployment = deployments[0];
      
      colorLog(`✅ Found ${deployments.length} deployments`, 'green');
      return deployments;
    } catch (error) {
      colorLog('❌ Failed to get deployment history', 'red');
      return [];
    }
  }

  parseVercelDeployments(output) {
    try {
      const deployments = JSON.parse(output);
      return deployments.map(dep => ({
        id: dep.id,
        url: dep.url,
        state: dep.state,
        created: dep.created,
        target: dep.target,
        isProduction: dep.target === 'production',
      }));
    } catch (error) {
      // Fallback to text parsing
      const lines = output.split('\n');
      return lines
        .filter(line => line.trim())
        .map(line => {
          const parts = line.split(/\s+/);
          return {
            id: parts[0],
            url: parts[1],
            state: parts[2],
            created: parts[3],
            target: parts[4],
            isProduction: parts[4] === 'production',
          };
        });
    }
  }

  parseNetlifyDeployments(output) {
    // Parse Netlify deployment output
    const lines = output.split('\n');
    return lines
      .filter(line => line.trim())
      .map(line => {
        const parts = line.split(/\s+/);
        return {
          id: parts[0],
          url: parts[1],
          state: parts[2],
          created: parts[3],
          target: parts[4],
          isProduction: parts[4] === 'production',
        };
      });
  }

  async checkDeploymentHealth(deployment) {
    colorLog(`🏥 Checking health of deployment: ${deployment.url}`, 'blue');
    
    const healthChecks = config.monitoring.healthEndpoints;
    const results = [];
    
    for (const endpoint of healthChecks) {
      try {
        const url = `${deployment.url}${endpoint}`;
        const response = await fetch(url, { 
          method: 'GET',
          timeout: 5000,
        });
        
        const isHealthy = response.ok;
        const responseTime = Date.now() - startTime;
        
        results.push({
          endpoint,
          healthy: isHealthy,
          responseTime,
          status: response.status,
        });
        
        if (!isHealthy) {
          colorLog(`❌ Health check failed: ${endpoint} (${response.status})`, 'red');
        } else {
          colorLog(`✅ Health check passed: ${endpoint} (${responseTime}ms)`, 'green');
        }
      } catch (error) {
        results.push({
          endpoint,
          healthy: false,
          error: error.message,
        });
        colorLog(`❌ Health check error: ${endpoint} - ${error.message}`, 'red');
      }
    }
    
    const failedChecks = results.filter(r => !r.healthy);
    const isHealthy = failedChecks.length < config.monitoring.alerts.health_check.failure_threshold;
    
    return {
      healthy: isHealthy,
      results,
      failedChecks: failedChecks.length,
    };
  }

  async getDeploymentMetrics(deployment) {
    colorLog(`📊 Getting metrics for deployment: ${deployment.url}`, 'blue');
    
    // This would typically connect to your monitoring system
    // For now, we'll simulate metrics
    const metrics = {
      error_rate: Math.random() * 0.2, // 0-20%
      response_time: Math.random() * 10000, // 0-10s
      throughput: Math.random() * 1000, // 0-1000 req/s
      cpu_usage: Math.random() * 100, // 0-100%
      memory_usage: Math.random() * 100, // 0-100%
    };
    
    colorLog('📈 Current Metrics:', 'cyan');
    colorLog(`   Error Rate: ${(metrics.error_rate * 100).toFixed(2)}%`, 'cyan');
    colorLog(`   Response Time: ${metrics.response_time.toFixed(0)}ms`, 'cyan');
    colorLog(`   Throughput: ${metrics.throughput.toFixed(0)} req/s`, 'cyan');
    
    return metrics;
  }

  shouldRollback(health, metrics) {
    const thresholds = config.rollback;
    
    // Check health check failures
    if (health.failedChecks >= thresholds.healthCheckThreshold) {
      return { shouldRollback: true, reason: 'health_check_failure', severity: 'high' };
    }
    
    // Check error rate
    if (metrics.error_rate >= thresholds.errorRateThreshold) {
      return { shouldRollback: true, reason: 'high_error_rate', severity: 'medium' };
    }
    
    // Check response time
    if (metrics.response_time >= thresholds.responseTimeThreshold) {
      return { shouldRollback: true, reason: 'slow_response', severity: 'medium' };
    }
    
    return { shouldRollback: false, reason: null, severity: null };
  }

  async executeRollback(targetDeployment, strategy = 'immediate') {
    colorLog(`🔄 Executing rollback to: ${targetDeployment.url}`, 'magenta');
    colorLog(`Strategy: ${strategy}`, 'cyan');
    
    try {
      const platformConfig = config.platforms[this.platform];
      
      switch (this.platform) {
        case 'vercel':
          return await this.executeVercelRollback(targetDeployment, platformConfig, strategy);
        case 'netlify':
          return await this.executeNetlifyRollback(targetDeployment, platformConfig, strategy);
        default:
          throw new Error(`Unsupported platform: ${this.platform}`);
      }
    } catch (error) {
      colorLog(`❌ Rollback failed: ${error.message}`, 'red');
      return { success: false, error: error.message };
    }
  }

  async executeVercelRollback(targetDeployment, platformConfig, strategy) {
    try {
      if (strategy === 'immediate') {
        // Promote previous deployment
        const command = `${platformConfig.promoteCommand} ${targetDeployment.id}`;
        colorLog(`🚀 Running: ${command}`, 'blue');
        execSync(command, { stdio: 'inherit' });
        
        colorLog('✅ Vercel rollback completed', 'green');
        return { success: true, deployment: targetDeployment };
      } else {
        // For gradual rollback, we would implement traffic shifting
        colorLog('🔄 Gradual rollback not implemented for Vercel', 'yellow');
        return await this.executeVercelRollback(targetDeployment, platformConfig, 'immediate');
      }
    } catch (error) {
      throw new Error(`Vercel rollback failed: ${error.message}`);
    }
  }

  async executeNetlifyRollback(targetDeployment, platformConfig, strategy) {
    try {
      if (strategy === 'immediate') {
        const command = `${platformConfig.rollbackCommand} ${targetDeployment.id}`;
        colorLog(`🚀 Running: ${command}`, 'blue');
        execSync(command, { stdio: 'inherit' });
        
        colorLog('✅ Netlify rollback completed', 'green');
        return { success: true, deployment: targetDeployment };
      } else {
        colorLog('🔄 Gradual rollback not implemented for Netlify', 'yellow');
        return await this.executeNetlifyRollback(targetDeployment, platformConfig, 'immediate');
      }
    } catch (error) {
      throw new Error(`Netlify rollback failed: ${error.message}`);
    }
  }

  async sendNotification(type, data) {
    colorLog(`📢 Sending notification: ${type}`, 'blue');
    
    const notification = {
      type,
      timestamp: new Date().toISOString(),
      deployment: data.deployment,
      reason: data.reason,
      platform: this.platform,
    };
    
    // Save notification to file (in real implementation, send to notification service)
    try {
      const notificationFile = `rollback-notification-${Date.now()}.json`;
      fs.writeFileSync(notificationFile, JSON.stringify(notification, null, 2));
      colorLog(`📄 Notification saved: ${notificationFile}`, 'cyan');
    } catch (error) {
      colorLog('⚠️  Failed to save notification', 'yellow');
    }
  }

  async monitorDeployment(deployment, duration = 600000) { // 10 minutes default
    colorLog(`🔍 Monitoring deployment for ${duration / 60000} minutes...`, 'blue');
    
    const startTime = Date.now();
    const checkInterval = 30000; // 30 seconds
    let rollbackTriggered = false;
    
    const monitor = async () => {
      if (Date.now() - startTime > duration || rollbackTriggered) {
        return;
      }
      
      const health = await this.checkDeploymentHealth(deployment);
      const metrics = await this.getDeploymentMetrics(deployment);
      const rollbackDecision = this.shouldRollback(health, metrics);
      
      if (rollbackDecision.shouldRollback) {
        colorLog(`🚨 Rollback triggered: ${rollbackDecision.reason}`, 'red');
        colorLog(`Severity: ${rollbackDecision.severity}`, 'yellow');
        
        await this.sendNotification('rollback_initiated', {
          deployment,
          reason: rollbackDecision.reason,
          severity: rollbackDecision.severity,
        });
        
        const previousDeployment = this.deploymentHistory.find(d => 
          d.id !== deployment.id && d.state === 'READY'
        );
        
        if (previousDeployment) {
          const strategy = rollbackDecision.severity === 'high' ? 'immediate' : 'gradual';
          await this.executeRollback(previousDeployment, strategy);
          await this.sendNotification('rollback_completed', {
            deployment: previousDeployment,
            reason: rollbackDecision.reason,
          });
        } else {
          colorLog('❌ No previous deployment available for rollback', 'red');
          await this.sendNotification('rollback_failed', {
            deployment,
            reason: 'No previous deployment available',
          });
        }
        
        rollbackTriggered = true;
        return;
      }
      
      // Continue monitoring
      setTimeout(monitor, checkInterval);
    };
    
    await monitor();
    
    if (!rollbackTriggered) {
      colorLog('✅ Monitoring completed - no rollback needed', 'green');
    }
  }

  async run() {
    const args = process.argv.slice(2);
    const command = args[0] || 'monitor';
    const deploymentId = args[1];
    
    colorLog('🔄 Rollback Manager', 'magenta');
    colorLog('==================', 'magenta');
    
    await this.getDeploymentHistory();
    
    if (this.deploymentHistory.length === 0) {
      colorLog('❌ No deployments found', 'red');
      return;
    }
    
    switch (command) {
      case 'monitor':
        const deployment = deploymentId 
          ? this.deploymentHistory.find(d => d.id === deploymentId)
          : this.currentDeployment;
        
        if (!deployment) {
          colorLog('❌ Deployment not found', 'red');
          return;
        }
        
        await this.monitorDeployment(deployment);
        break;
        
      case 'rollback':
        const targetId = deploymentId || this.deploymentHistory[1]?.id;
        const targetDeployment = this.deploymentHistory.find(d => d.id === targetId);
        
        if (!targetDeployment) {
          colorLog('❌ Target deployment not found', 'red');
          return;
        }
        
        await this.executeRollback(targetDeployment);
        break;
        
      case 'list':
        colorLog('📋 Deployment History:', 'cyan');
        this.deploymentHistory.forEach((dep, index) => {
          const status = dep.state === 'READY' ? '✅' : '⏳';
          const prod = dep.isProduction ? ' (PROD)' : '';
          colorLog(`${status} ${index + 1}. ${dep.id} - ${dep.url}${prod}`, 'cyan');
        });
        break;
        
      case 'health':
        const healthDeployment = deploymentId 
          ? this.deploymentHistory.find(d => d.id === deploymentId)
          : this.currentDeployment;
        
        if (!healthDeployment) {
          colorLog('❌ Deployment not found', 'red');
          return;
        }
        
        await this.checkDeploymentHealth(healthDeployment);
        break;
        
      default:
        colorLog('❌ Unknown command', 'red');
        colorLog('Available commands:', 'cyan');
        colorLog('  monitor [deployment-id]  - Monitor deployment health', 'cyan');
        colorLog('  rollback [deployment-id]  - Rollback to previous deployment', 'cyan');
        colorLog('  list                    - List deployment history', 'cyan');
        colorLog('  health [deployment-id]   - Check deployment health', 'cyan');
        break;
    }
  }
}

if (require.main === module) {
  const manager = new RollbackManager();
  manager.run();
}

module.exports = RollbackManager;
```

### 3. Create Automated Rollback Script

Create `scripts/auto-rollback.js`:

```javascript
#!/usr/bin/env node

const RollbackManager = require('./rollback-manager');

class AutoRollback extends RollbackManager {
  constructor() {
    super();
    this.isRunning = false;
    this.monitoringInterval = null;
  }

  async startAutoMonitoring(deploymentId, options = {}) {
    if (this.isRunning) {
      console.log('⚠️  Auto-rollback is already running');
      return;
    }

    this.isRunning = true;
    const deployment = this.deploymentHistory.find(d => d.id === deploymentId);
    
    if (!deployment) {
      console.log('❌ Deployment not found');
      return;
    }

    console.log('🤖 Starting auto-rollback monitoring...');
    console.log(`📡 Monitoring deployment: ${deployment.url}`);
    
    const checkInterval = options.interval || 30000; // 30 seconds
    const maxDuration = options.duration || 600000; // 10 minutes
    
    const startTime = Date.now();
    
    this.monitoringInterval = setInterval(async () => {
      if (Date.now() - startTime > maxDuration) {
        console.log('⏰ Auto-rollback monitoring completed');
        this.stopAutoMonitoring();
        return;
      }
      
      if (!this.isRunning) {
        return;
      }
      
      console.log(`🔍 Auto-check at ${new Date().toLocaleTimeString()}`);
      
      const health = await this.checkDeploymentHealth(deployment);
      const metrics = await this.getDeploymentMetrics(deployment);
      const rollbackDecision = this.shouldRollback(health, metrics);
      
      if (rollbackDecision.shouldRollback) {
        console.log(`🚨 Auto-rollback triggered: ${rollbackDecision.reason}`);
        
        const previousDeployment = this.deploymentHistory.find(d => 
          d.id !== deployment.id && d.state === 'READY'
        );
        
        if (previousDeployment) {
          console.log(`🔄 Auto-rolling back to: ${previousDeployment.url}`);
          await this.executeRollback(previousDeployment, 'immediate');
          this.stopAutoMonitoring();
        } else {
          console.log('❌ No previous deployment available for auto-rollback');
          this.stopAutoMonitoring();
        }
      }
    }, checkInterval);
  }

  stopAutoMonitoring() {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = null;
    }
    this.isRunning = false;
    console.log('🛑 Auto-rollback monitoring stopped');
  }

  async run() {
    const args = process.argv.slice(2);
    const command = args[0] || 'start';
    const deploymentId = args[1];
    
    switch (command) {
      case 'start':
        if (!deploymentId) {
          console.log('❌ Deployment ID required');
          console.log('Usage: npm run auto-rollback start <deployment-id>');
          return;
        }
        
        await this.getDeploymentHistory();
        await this.startAutoMonitoring(deploymentId);
        break;
        
      case 'stop':
        this.stopAutoMonitoring();
        break;
        
      case 'status':
        console.log(`🤖 Auto-rollback status: ${this.isRunning ? 'running' : 'stopped'}`);
        break;
        
      default:
        console.log('❌ Unknown command');
        console.log('Available commands:');
        console.log('  start <deployment-id>  - Start auto-rollback monitoring');
        console.log('  stop                  - Stop auto-rollback monitoring');
        console.log('  status                - Check auto-rollback status');
        break;
    }
  }
}

if (require.main === module) {
  const autoRollback = new AutoRollback();
  autoRollback.run();
}

module.exports = AutoRollback;
```

### 4. Create Rollback Recovery Script

Create `scripts/rollback-recovery.js`:

```javascript
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36c',
  magenta: '\x1b[35m',
};

function colorLog(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

class RollbackRecovery {
  constructor() {
    this.backupDir = path.join(process.cwd(), '.rollback-backups');
    this.recoveryLog = path.join(process.cwd(), 'rollback-recovery.log');
  }

  createBackup(deploymentId) {
    colorLog(`💾 Creating backup for deployment: ${deploymentId}`, 'blue');
    
    if (!fs.existsSync(this.backupDir)) {
      fs.mkdirSync(this.backupDir, { recursive: true });
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupDir = path.join(this.backupDir, `${deploymentId}-${timestamp}`);
    
    try {
      fs.mkdirSync(backupDir, { recursive: true });
      
      // Backup important files
      const filesToBackup = [
        '.next',
        'package.json',
        'package-lock.json',
        'next.config.js',
        'vercel.json',
        '.env.local',
      ];
      
      for (const file of filesToBackup) {
        const sourcePath = path.join(process.cwd(), file);
        const targetPath = path.join(backupDir, file);
        
        if (fs.existsSync(sourcePath)) {
          if (fs.statSync(sourcePath).isDirectory()) {
            this.copyDirectory(sourcePath, targetPath);
          } else {
            fs.copyFileSync(sourcePath, targetPath);
          }
          colorLog(`✅ Backed up: ${file}`, 'green');
        }
      }
      
      // Create backup metadata
      const metadata = {
        deploymentId,
        timestamp: new Date().toISOString(),
        files: filesToBackup,
        platform: this.detectPlatform(),
      };
      
      fs.writeFileSync(
        path.join(backupDir, 'backup-metadata.json'),
        JSON.stringify(metadata, null, 2)
      );
      
      colorLog(`✅ Backup created: ${backupDir}`, 'green');
      return backupDir;
    } catch (error) {
      colorLog(`❌ Backup failed: ${error.message}`, 'red');
      return null;
    }
  }

  copyDirectory(source, target) {
    if (!fs.existsSync(target)) {
      fs.mkdirSync(target, { recursive: true });
    }
    
    const files = fs.readdirSync(source);
    
    for (const file of files) {
      const sourcePath = path.join(source, file);
      const targetPath = path.join(target, file);
      
      if (fs.statSync(sourcePath).isDirectory()) {
        this.copyDirectory(sourcePath, targetPath);
      } else {
        fs.copyFileSync(sourcePath, targetPath);
      }
    }
  }

  detectPlatform() {
    if (process.env.VERCEL_ENV) return 'vercel';
    if (fs.existsSync('netlify.toml')) return 'netlify';
    return 'unknown';
  }

  listBackups() {
    colorLog('📋 Available Rollback Backups:', 'magenta');
    colorLog('=============================', 'magenta');
    
    if (!fs.existsSync(this.backupDir)) {
      colorLog('❌ No backup directory found', 'red');
      return;
    }
    
    const backups = fs.readdirSync(this.backupDir)
      .filter(dir => fs.statSync(path.join(this.backupDir, dir)).isDirectory())
      .sort((a, b) => b.localeCompare(a)); // Sort by newest first
    
    if (backups.length === 0) {
      colorLog('❌ No backups found', 'red');
      return;
    }
    
    backups.forEach((backup, index) => {
      const backupPath = path.join(this.backupDir, backup);
      const metadataPath = path.join(backupPath, 'backup-metadata.json');
      
      if (fs.existsSync(metadataPath)) {
        const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
        const date = new Date(metadata.timestamp).toLocaleString();
        
        colorLog(`${index + 1}. ${backup}`, 'cyan');
        colorLog(`   Deployment: ${metadata.deploymentId}`, 'yellow');
        colorLog(`   Platform: ${metadata.platform}`, 'yellow');
        colorLog(`   Created: ${date}`, 'yellow');
        colorLog(`   Path: ${backupPath}`, 'yellow');
        colorLog('', 'reset');
      } else {
        colorLog(`${index + 1}. ${backup} (no metadata)`, 'yellow');
      }
    });
  }

  restoreBackup(backupName) {
    colorLog(`🔄 Restoring backup: ${backupName}`, 'blue');
    
    const backupPath = path.join(this.backupDir, backupName);
    
    if (!fs.existsSync(backupPath)) {
      colorLog('❌ Backup not found', 'red');
      return false;
    }
    
    const metadataPath = path.join(backupPath, 'backup-metadata.json');
    
    if (!fs.existsSync(metadataPath)) {
      colorLog('❌ Backup metadata not found', 'red');
      return false;
    }
    
    try {
      const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
      
      // Restore files from backup
      for (const file of metadata.files) {
        const sourcePath = path.join(backupPath, file);
        const targetPath = path.join(process.cwd(), file);
        
        if (fs.existsSync(sourcePath)) {
          // Remove existing file/directory
          if (fs.existsSync(targetPath)) {
            if (fs.statSync(targetPath).isDirectory()) {
              fs.rmSync(targetPath, { recursive: true, force: true });
            } else {
              fs.unlinkSync(targetPath);
            }
          }
          
          // Copy from backup
          if (fs.statSync(sourcePath).isDirectory()) {
            this.copyDirectory(sourcePath, targetPath);
          } else {
            fs.copyFileSync(sourcePath, targetPath);
          }
          
          colorLog(`✅ Restored: ${file}`, 'green');
        }
      }
      
      colorLog('✅ Backup restored successfully', 'green');
      colorLog('📝 Next steps:', 'cyan');
      colorLog('1. Run: npm install', 'cyan');
      colorLog('2. Run: npm run build', 'cyan');
      colorLog('3. Deploy the restored version', 'cyan');
      
      return true;
    } catch (error) {
      colorLog(`❌ Restore failed: ${error.message}`, 'red');
      return false;
    }
  }

  cleanupBackups(keepCount = 5) {
    colorLog(`🧹 Cleaning up old backups (keeping ${keepCount})...`, 'blue');
    
    if (!fs.existsSync(this.backupDir)) {
      colorLog('❌ No backup directory found', 'red');
      return;
    }
    
    const backups = fs.readdirSync(this.backupDir)
      .filter(dir => fs.statSync(path.join(this.backupDir, dir)).isDirectory())
      .sort((a, b) => b.localeCompare(a)); // Sort by newest first
    
    if (backups.length <= keepCount) {
      colorLog('✅ No cleanup needed', 'green');
      return;
    }
    
    const toDelete = backups.slice(keepCount);
    
    for (const backup of toDelete) {
      const backupPath = path.join(this.backupDir, backup);
      fs.rmSync(backupPath, { recursive: true, force: true });
      colorLog(`🗑️  Deleted: ${backup}`, 'yellow');
    }
    
    colorLog(`✅ Cleaned up ${toDelete.length} old backups`, 'green');
  }

  logRecovery(action, deploymentId, success, details = '') {
    const logEntry = {
      timestamp: new Date().toISOString(),
      action,
      deploymentId,
      success,
      details,
    };
    
    const logLine = JSON.stringify(logEntry);
    
    try {
      fs.appendFileSync(this.recoveryLog, logLine + '\n');
    } catch (error) {
      colorLog('⚠️  Failed to write recovery log', 'yellow');
    }
  }

  run() {
    const args = process.argv.slice(2);
    const command = args[0] || 'list';
    const target = args[1];
    
    switch (command) {
      case 'backup':
        if (!target) {
          colorLog('❌ Deployment ID required', 'red');
          colorLog('Usage: npm run recovery:backup <deployment-id>', 'yellow');
          return;
        }
        this.createBackup(target);
        break;
        
      case 'restore':
        if (!target) {
          colorLog('❌ Backup name required', 'red');
          colorLog('Usage: npm run recovery:restore <backup-name>', 'yellow');
          return;
        }
        this.restoreBackup(target);
        break;
        
      case 'list':
        this.listBackups();
        break;
        
      case 'cleanup':
        const keepCount = parseInt(args[1]) || 5;
        this.cleanupBackups(keepCount);
        break;
        
      default:
        colorLog('❌ Unknown command', 'red');
        colorLog('Available commands:', 'cyan');
        colorLog('  backup <deployment-id>  - Create backup of current deployment', 'cyan');
        colorLog('  restore <backup-name>    - Restore from backup', 'cyan');
        colorLog('  list                   - List available backups', 'cyan');
        colorLog('  cleanup [count]         - Clean up old backups', 'cyan');
        break;
    }
  }
}

if (require.main === module) {
  const recovery = new RollbackRecovery();
  recovery.run();
}

module.exports = RollbackRecovery;
```

### 5. Update Package.json Scripts

Update `package.json` scripts:

```json
{
  "scripts": {
    "rollback": "node scripts/rollback-manager.js",
    "rollback:monitor": "node scripts/rollback-manager.js monitor",
    "rollback:execute": "node scripts/rollback-manager.js rollback",
    "rollback:list": "node scripts/rollback-manager.js list",
    "rollback:health": "node scripts/rollback-manager.js health",
    "auto-rollback": "node scripts/auto-rollback.js",
    "auto-rollback:start": "node scripts/auto-rollback.js start",
    "auto-rollback:stop": "node scripts/auto-rollback.js stop",
    "auto-rollback:status": "node scripts/auto-rollback.js status",
    "recovery:backup": "node scripts/rollback-recovery.js backup",
    "recovery:restore": "node scripts/rollback-recovery.js restore",
    "recovery:list": "node scripts/rollback-recovery.js list",
    "recovery:cleanup": "node scripts/rollback-recovery.js cleanup"
  }
}
```

---

## Code Examples

### Rollback Commands

```bash
# Monitor deployment health
npm run rollback:monitor

# Monitor specific deployment
npm run rollback:monitor <deployment-id>

# Execute rollback
npm run rollback:execute

# Rollback to specific deployment
npm run rollback:execute <deployment-id>

# List deployment history
npm run rollback:list

# Check deployment health
npm run rollback:health

# Auto-rollback monitoring
npm run auto-rollback:start <deployment-id>

# Stop auto-rollback
npm run auto-rollback:stop

# Check auto-rollback status
npm run auto-rollback:status

# Create backup before rollback
npm run recovery:backup <deployment-id>

# Restore from backup
npm run recovery:restore <backup-name>

# List available backups
npm run recovery:list

# Clean up old backups
npm run recovery:cleanup 5
```

### Rollback Configuration

```javascript
// rollback.config.js
module.exports = {
  rollback: {
    autoRollbackWindow: 15, // 15 minutes
    errorRateThreshold: 0.1, // 10%
    responseTimeThreshold: 5000, // 5 seconds
    healthCheckThreshold: 3, // 3 failed checks
  },
  monitoring: {
    healthEndpoints: ['/health', '/api/health'],
    metrics: ['error_rate', 'response_time', 'throughput'],
  },
};
```

### Custom Rollback Logic

```javascript
// Custom rollback decision logic
function shouldRollback(health, metrics, customRules) {
  // Default checks
  if (health.failedChecks >= 3) return true;
  if (metrics.error_rate >= 0.1) return true;
  
  // Custom rules
  if (customRules.businessLogic && metrics.business_errors > 10) {
    return true;
  }
  
  if (customRules.userExperience && metrics.page_load_time > 8000) {
    return true;
  }
  
  return false;
}
```

---

## Configuration Templates

### Complete rollback.config.js

```javascript
module.exports = {
  rollback: {
    maxPreviousDeployments: 10,
    autoRollbackWindow: 15,
    errorRateThreshold: 0.1,
    responseTimeThreshold: 5000,
    healthCheckThreshold: 3,
    strategies: {
      immediate: {
        description: 'Immediate rollback to previous deployment',
        conditions: ['critical_error', 'health_check_failure'],
        approval: false,
      },
      gradual: {
        description: 'Gradual rollback with traffic shifting',
        conditions: ['high_error_rate', 'slow_response'],
        approval: true,
      },
    },
  },
  monitoring: {
    healthEndpoints: ['/health', '/api/health'],
    metrics: ['error_rate', 'response_time', 'throughput'],
    alerts: {
      error_rate: { warning: 0.05, critical: 0.1 },
      response_time: { warning: 2000, critical: 5000 },
    },
  },
};
```

---

## Best Practices

1. **Monitor deployment health** - Automated health checks
2. **Set appropriate thresholds** - Balance sensitivity and stability
3. **Create backups before rollback** - Enable recovery options
4. **Use gradual rollback** - Minimize user impact
5. **Document rollback procedures** - Team knowledge sharing
6. **Test rollback procedures** - Regular drills and validation
7. **Monitor rollback success** - Verify rollback effectiveness
8. **Learn from rollbacks** - Improve deployment quality

---

## Stop Conditions

**STOP and report if:**
- Rollback execution fails
- Backup creation fails
- Health check failures
- Platform-specific errors

**Expected Outcomes:**
- Rollback procedures functional
- Automated monitoring working
- Backup system operational
- Recovery procedures working
- Notification system active

---

## Verification Checklist

- [ ] Rollback configuration created
- [ ] Rollback manager functional
- [ ] Auto-rollback system working
- [ ] Recovery procedures working
- [ ] Backup system operational
- [ ] Health checks functional
- [ ] Monitoring system active
- [ ] Package.json scripts updated
- [ ] Platform integration working
- [ ] Documentation complete

---

*Version: 1.0.0*
*Last Updated: 2026-01-31*
*Skill Category: Architecture - Deployment*
