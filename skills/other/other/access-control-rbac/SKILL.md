---
name: access-control-rbac
description: Implement Role-Based Access Control (RBAC), permissions management, and authorization policies. Use when building secure access control systems with fine-grained permissions.
---

# Access Control & RBAC

## Overview

Implement comprehensive Role-Based Access Control systems with permissions management, attribute-based policies, and least privilege principles.

## When to Use

- Multi-tenant applications
- Enterprise access management
- API authorization
- Admin dashboards
- Data access controls
- Compliance requirements

## Implementation Examples

### 1. **Node.js RBAC System**

```javascript
// rbac-system.js
class Permission {
  constructor(resource, action) {
    this.resource = resource;
    this.action = action;
  }

  toString() {
    return `${this.resource}:${this.action}`;
  }
}

class Role {
  constructor(name, description) {
    this.name = name;
    this.description = description;
    this.permissions = new Set();
    this.inherits = new Set();
  }

  addPermission(permission) {
    this.permissions.add(permission.toString());
  }

  removePermission(permission) {
    this.permissions.delete(permission.toString());
  }

  inheritFrom(role) {
    this.inherits.add(role.name);
  }

  hasPermission(permission, rbac) {
    // Check direct permissions
    if (this.permissions.has(permission.toString())) {
      return true;
    }

    // Check inherited permissions
    for (const parentRoleName of this.inherits) {
      const parentRole = rbac.getRole(parentRoleName);
      if (parentRole && parentRole.hasPermission(permission, rbac)) {
        return true;
      }
    }

    return false;
  }
}

class RBACSystem {
  constructor() {
    this.roles = new Map();
    this.userRoles = new Map();
    this.initializeDefaultRoles();
  }

  initializeDefaultRoles() {
    // Admin role - full access
    const admin = new Role('admin', 'Administrator with full access');
    admin.addPermission(new Permission('*', '*'));
    this.createRole(admin);

    // Editor role
    const editor = new Role('editor', 'Can create and edit content');
    editor.addPermission(new Permission('posts', 'create'));
    editor.addPermission(new Permission('posts', 'read'));
    editor.addPermission(new Permission('posts', 'update'));
    editor.addPermission(new Permission('comments', 'read'));
    editor.addPermission(new Permission('comments', 'moderate'));
    this.createRole(editor);

    // Viewer role
    const viewer = new Role('viewer', 'Read-only access');
    viewer.addPermission(new Permission('posts', 'read'));
    viewer.addPermission(new Permission('comments', 'read'));
    this.createRole(viewer);

    // User role (inherits from viewer)
    const user = new Role('user', 'Authenticated user');
    user.inheritFrom(viewer);
    user.addPermission(new Permission('posts', 'create'));
    user.addPermission(new Permission('comments', 'create'));
    user.addPermission(new Permission('profile', 'update'));
    this.createRole(user);
  }

  createRole(role) {
    this.roles.set(role.name, role);
  }

  getRole(roleName) {
    return this.roles.get(roleName);
  }

  assignRole(userId, roleName) {
    if (!this.roles.has(roleName)) {
      throw new Error(`Role ${roleName} does not exist`);
    }

    if (!this.userRoles.has(userId)) {
      this.userRoles.set(userId, new Set());
    }

    this.userRoles.get(userId).add(roleName);
  }

  revokeRole(userId, roleName) {
    const roles = this.userRoles.get(userId);
    if (roles) {
      roles.delete(roleName);
    }
  }

  getUserRoles(userId) {
    return Array.from(this.userRoles.get(userId) || []);
  }

  can(userId, resource, action) {
    const permission = new Permission(resource, action);
    const userRoles = this.userRoles.get(userId);

    if (!userRoles) {
      return false;
    }

    // Check if user has admin role (wildcard permissions)
    if (userRoles.has('admin')) {
      return true;
    }

    // Check all user roles
    for (const roleName of userRoles) {
      const role = this.roles.get(roleName);
      if (role && role.hasPermission(permission, this)) {
        return true;
      }
    }

    return false;
  }

  // Express middleware
  authorize(resource, action) {
    return (req, res, next) => {
      const userId = req.user?.id;

      if (!userId) {
        return res.status(401).json({
          error: 'unauthorized',
          message: 'Authentication required'
        });
      }

      if (!this.can(userId, resource, action)) {
        return res.status(403).json({
          error: 'forbidden',
          message: `Permission denied: ${resource}:${action}`
        });
      }

      next();
    };
  }
}

// Usage
const rbac = new RBACSystem();

// Assign roles to users
rbac.assignRole('user-123', 'editor');
rbac.assignRole('user-456', 'viewer');
rbac.assignRole('user-789', 'admin');

// Check permissions
console.log(rbac.can('user-123', 'posts', 'update')); // true
console.log(rbac.can('user-456', 'posts', 'update')); // false
console.log(rbac.can('user-789', 'anything', 'anything')); // true

// Express route protection
const express = require('express');
const app = express();

app.post('/api/posts',
  rbac.authorize('posts', 'create'),
  (req, res) => {
    res.json({ message: 'Post created' });
  }
);

module.exports = RBACSystem;
```

### 2. **Python ABAC (Attribute-Based Access Control)**

```python
# abac_system.py
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from enum import Enum

class Effect(Enum):
    ALLOW = "allow"
    DENY = "deny"

@dataclass
class Policy:
    name: str
    effect: Effect
    resource: str
    action: str
    conditions: List[Callable[[Dict], bool]]

class ABACSystem:
    def __init__(self):
        self.policies: List[Policy] = []
        self.initialize_policies()

    def initialize_policies(self):
        """Initialize default policies"""

        # Allow users to read their own profile
        self.add_policy(Policy(
            name="read_own_profile",
            effect=Effect.ALLOW,
            resource="profile",
            action="read",
            conditions=[
                lambda ctx: ctx['user']['id'] == ctx['resource']['owner_id']
            ]
        ))

        # Allow users to update their own profile
        self.add_policy(Policy(
            name="update_own_profile",
            effect=Effect.ALLOW,
            resource="profile",
            action="update",
            conditions=[
                lambda ctx: ctx['user']['id'] == ctx['resource']['owner_id']
            ]
        ))

        # Allow admins to do anything
        self.add_policy(Policy(
            name="admin_all_access",
            effect=Effect.ALLOW,
            resource="*",
            action="*",
            conditions=[
                lambda ctx: 'admin' in ctx['user'].get('roles', [])
            ]
        ))

        # Allow managers to approve within their department
        self.add_policy(Policy(
            name="manager_department_approval",
            effect=Effect.ALLOW,
            resource="expense",
            action="approve",
            conditions=[
                lambda ctx: 'manager' in ctx['user'].get('roles', []),
                lambda ctx: ctx['user']['department'] == ctx['resource']['department']
            ]
        ))

        # Deny access during maintenance window
        self.add_policy(Policy(
            name="maintenance_block",
            effect=Effect.DENY,
            resource="*",
            action="*",
            conditions=[
                lambda ctx: ctx.get('system', {}).get('maintenance_mode', False)
            ]
        ))

        # Time-based access control
        self.add_policy(Policy(
            name="business_hours_only",
            effect=Effect.DENY,
            resource="sensitive_data",
            action="*",
            conditions=[
                lambda ctx: ctx['time']['hour'] < 9 or ctx['time']['hour'] > 17
            ]
        ))

    def add_policy(self, policy: Policy):
        """Add a new policy"""
        self.policies.append(policy)

    def evaluate(self, context: Dict[str, Any], resource: str, action: str) -> bool:
        """Evaluate access request against policies"""

        # Default deny
        decision = False

        for policy in self.policies:
            # Check if policy applies
            if not self._matches(policy.resource, resource):
                continue

            if not self._matches(policy.action, action):
                continue

            # Evaluate conditions
            try:
                conditions_met = all(
                    condition(context) for condition in policy.conditions
                )
            except Exception as e:
                print(f"Error evaluating policy {policy.name}: {e}")
                conditions_met = False

            if not conditions_met:
                continue

            # Apply policy effect
            if policy.effect == Effect.ALLOW:
                decision = True
            elif policy.effect == Effect.DENY:
                # Deny always takes precedence
                return False

        return decision

    def _matches(self, pattern: str, value: str) -> bool:
        """Check if pattern matches value (supports wildcards)"""
        if pattern == "*":
            return True
        return pattern == value

    def can(self, user: Dict, resource: str, action: str,
            resource_data: Dict = None, system_context: Dict = None) -> bool:
        """Check if user can perform action on resource"""

        from datetime import datetime

        context = {
            'user': user,
            'resource': resource_data or {},
            'system': system_context or {},
            'time': {
                'hour': datetime.now().hour,
                'weekday': datetime.now().weekday()
            }
        }

        return self.evaluate(context, resource, action)

# Usage
if __name__ == '__main__':
    abac = ABACSystem()

    # Test cases
    user1 = {
        'id': 'user-123',
        'roles': ['user'],
        'department': 'engineering'
    }

    user2 = {
        'id': 'user-456',
        'roles': ['admin']
    }

    user3 = {
        'id': 'user-789',
        'roles': ['manager'],
        'department': 'engineering'
    }

    # Own profile access
    print("User can read own profile:",
          abac.can(user1, 'profile', 'read',
                   resource_data={'owner_id': 'user-123'}))

    # Other's profile access
    print("User can read other's profile:",
          abac.can(user1, 'profile', 'read',
                   resource_data={'owner_id': 'user-999'}))

    # Admin access
    print("Admin can update any profile:",
          abac.can(user2, 'profile', 'update',
                   resource_data={'owner_id': 'user-999'}))

    # Manager approval
    expense = {'department': 'engineering', 'amount': 1000}
    print("Manager can approve dept expense:",
          abac.can(user3, 'expense', 'approve', resource_data=expense))

    # Different department
    other_expense = {'department': 'sales', 'amount': 1000}
    print("Manager can approve other dept expense:",
          abac.can(user3, 'expense', 'approve', resource_data=other_expense))
```

### 3. **Java Spring Security RBAC**

```java
// RBACConfiguration.java
package com.example.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class RBACConfiguration {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                // Public endpoints
                .requestMatchers("/api/public/**").permitAll()

                // Role-based access
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/users/**").hasAnyRole("USER", "ADMIN")

                // Permission-based access
                .requestMatchers("/api/posts/**").hasAuthority("posts:read")
                .requestMatchers("/api/posts/create").hasAuthority("posts:create")
                .requestMatchers("/api/posts/*/edit").hasAuthority("posts:update")
                .requestMatchers("/api/posts/*/delete").hasAuthority("posts:delete")

                // Default
                .anyRequest().authenticated()
            )
            .csrf().disable();

        return http.build();
    }
}

// UserController.java with method-level security
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
    public User getUser(@PathVariable String id) {
        // Users can view their own profile or admins can view any
        return userService.findById(id);
    }

    @PutMapping("/{id}")
    @PreAuthorize("@accessControl.canUpdateUser(authentication, #id)")
    public User updateUser(@PathVariable String id, @RequestBody User user) {
        return userService.update(id, user);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(@PathVariable String id) {
        userService.delete(id);
    }
}

// AccessControlService.java - Custom permission logic
@Service
public class AccessControlService {

    public boolean canUpdateUser(Authentication auth, String userId) {
        // Admins can update anyone
        if (auth.getAuthorities().stream()
            .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"))) {
            return true;
        }

        // Users can update themselves
        return auth.getPrincipal().equals(userId);
    }

    public boolean canApproveExpense(Authentication auth, Expense expense) {
        UserDetails user = (UserDetails) auth.getPrincipal();

        // Check if user is manager
        if (!auth.getAuthorities().stream()
            .anyMatch(a -> a.getAuthority().equals("ROLE_MANAGER"))) {
            return false;
        }

        // Check department match
        return user.getDepartment().equals(expense.getDepartment());
    }
}
```

## Best Practices

### ✅ DO
- Implement least privilege
- Use role hierarchies
- Audit access changes
- Regular access reviews
- Separate duties
- Document permissions
- Test access controls
- Use attribute-based policies

### ❌ DON'T
- Grant excessive permissions
- Share accounts
- Skip access reviews
- Hardcode permissions
- Ignore audit logs
- Use role explosion

## Access Control Models

- **RBAC**: Role-Based Access Control
- **ABAC**: Attribute-Based Access Control
- **MAC**: Mandatory Access Control
- **DAC**: Discretionary Access Control
- **ReBAC**: Relationship-Based Access Control

## Common Patterns

- **Owner-based**: Resource owner permissions
- **Department-based**: Organizational hierarchy
- **Time-based**: Temporal restrictions
- **Location-based**: Geographic restrictions
- **Resource-based**: Dynamic permissions

## Resources

- [NIST RBAC](https://csrc.nist.gov/projects/role-based-access-control)
- [OWASP Access Control](https://owasp.org/www-community/Access_Control)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
