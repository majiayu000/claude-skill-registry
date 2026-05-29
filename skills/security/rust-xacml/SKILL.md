---
name: rust-xacml
description: "策略引擎、权限决策、RBAC、策略模式、责任链"
category: architecture
triggers: ["xacml", "permission", "rbac", "policy", "authorization", "策略引擎", "权限"]
related_skills:
  - rust-auth
  - rust-web
  - rust-performance
  - rust-cache
---

# Rust XACML - 策略引擎技能

> 本技能提供策略决策引擎的通用解决方案，包括 RBAC、责任链、策略模式等。

## 核心概念

### 1. 策略引擎架构

```
策略决策流程
┌─────────────────────────────────────────────────────────────┐
│                     请求上下文                                │
│  (主体、资源、操作、环境)                                      │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  策略决策点 (PDP)                                            │
│  ├── 策略加载                                                │
│  ├── 策略评估                                                │
│  └── 决策组合                                                │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     决策结果                                 │
│  (Permit / Deny / NotApplicable / Indeterminate)           │
└─────────────────────────────────────────────────────────────┘
```

### 2. 决策类型

| 结果 | 含义 | 处理 |
|-----|------|-----|
| **Permit** | 允许访问 | 执行操作 |
| **Deny** | 拒绝访问 | 返回 403 |
| **NotApplicable** | 无匹配策略 | 使用默认规则 |
| **Indeterminate** | 评估错误 | 返回 500 |

---

## 核心模式

### 1. 策略评估器

```rust
//! 策略评估器

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// 请求上下文
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RequestContext {
    pub subject: Subject,      // 主体
    pub resource: Resource,    // 资源
    pub action: String,        // 操作
    pub environment: HashMap<String, String>,  // 环境
}

/// 主体
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Subject {
    pub id: String,
    pub roles: Vec<String>,
    pub attributes: HashMap<String, String>,
}

/// 资源
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Resource {
    pub id: String,
    pub r#type: String,
    pub attributes: HashMap<String, String>,
}

/// 决策结果
#[derive(Debug, Clone, PartialEq)]
pub enum Decision {
    Permit,
    Deny,
    NotApplicable,
    Indeterminate(String),
}

/// 策略定义
#[derive(Debug, Clone)]
pub struct Policy {
    pub id: String,
    pub target: PolicyTarget,
    pub rules: Vec<Rule>,
    pub combining_algorithm: CombiningAlgorithm,
}

/// 策略目标（匹配条件）
#[)]
pub struct PolicyTarget {
    pubderive(Debug, Clone subjects: Vec<Vec<String>>,  // 角色组合
    pub resources: Vec<String>,
    pub actions: Vec<String>,
}

/// 访问规则
#[derive(Debug, Clone)]
pub struct Rule {
    pub id: String,
    pub effect: RuleEffect,
    pub condition: Option<Box<dyn Fn(&RequestContext) -> bool + Send>>,
}

#[derive(Debug, Clone, Copy)]
pub enum RuleEffect {
    Permit,
    Deny,
}

/// 策略组合算法
#[derive(Debug, Clone, Copy)]
pub enum CombiningAlgorithm {
    DenyOverrides,      // Deny 优先
    PermitOverrides,    // Permit 优先
    FirstApplicable,    // 首个适用
    OnlyOneApplicable,  // 仅一个适用
}

/// 策略评估器
pub struct PolicyEvaluator {
    policies: Vec<Policy>,
}

impl PolicyEvaluator {
    pub fn new(policies: Vec<Policy>) -> Self {
        Self { policies }
    }

    /// 评估请求
    pub fn evaluate(&self, context: &RequestContext) -> Decision {
        let mut applicable_policies: Vec<&Policy> = self.policies
            .iter()
            .filter(|p| self.is_target_matched(p, context))
            .collect();

        if applicable_policies.is_empty() {
            return Decision::NotApplicable;
        }

        // 根据组合算法计算最终决策
        match applicable_policies.first().map(|p| p.combining_algorithm).unwrap_or(CombiningAlgorithm::FirstApplicable) {
            CombiningAlgorithm::DenyOverrides => self.deny_overrides(&applicable_policies, context),
            CombiningAlgorithm::PermitOverrides => self.permit_overrides(&applicable_policies, context),
            CombiningAlgorithm::FirstApplicable => self.first_applicable(&applicable_policies, context),
            CombiningAlgorithm::OnlyOneApplicable => {
                if applicable_policies.len() == 1 {
                    self.evaluate_policy(applicable_policies[0], context)
                } else {
                    Decision::Indeterminate("Multiple applicable policies".to_string())
                }
            }
        }
    }

    fn is_target_matched(&self, policy: &Policy, context: &RequestContext) -> bool {
        // 检查 Subjects
        let subject_matches = policy.target.subjects.is_empty() ||
            policy.target.subjects.iter().any(|roles| {
                roles.iter().all(|r| context.subject.roles.contains(r))
            });

        // 检查 Resources
        let resource_matches = policy.target.resources.is_empty() ||
            policy.target.resources.contains(&context.resource.r#type);

        // 检查 Actions
        let action_matches = policy.target.actions.is_empty() ||
            policy.target.actions.contains(&context.action);

        subject_matches && resource_matches && action_matches
    }

    fn deny_overrides(&self, policies: &[&Policy], context: &RequestContext) -> Decision {
        let mut has_error = false;
        let mut error_msg = String::new();

        for policy in policies {
            match self.evaluate_policy(policy, context) {
                Decision::Deny => return Decision::Deny,
                Decision::Indeterminate(msg) => {
                    has_error = true;
                    error_msg = msg;
                }
                _ => {}
            }
        }

        if has_error {
            Decision::Indeterminate(error_msg)
        } else {
            Decision::Permit
        }
    }

    fn permit_overrides(&self, policies: &[&Policy], context: &RequestContext) -> Decision {
        let mut has_error = false;
        let mut error_msg = String::new();

        for policy in policies {
            match self.evaluate_policy(policy, context) {
                Decision::Permit => return Decision::Permit,
                Decision::Indeterminate(msg) => {
                    has_error = true;
                    error_msg = msg;
                }
                _ => {}
            }
        }

        if has_error {
            Decision::Indeterminate(error_msg)
        } else {
            Decision::Deny
        }
    }

    fn first_applicable(&self, policies: &[&Policy], context: &RequestContext) -> Decision {
        for policy in policies {
            let decision = self.evaluate_policy(policy, context);
            if decision != Decision::NotApplicable {
                return decision;
            }
        }
        Decision::Deny
    }

    fn evaluate_policy(&self, policy: &Policy, context: &RequestContext) -> Decision {
        for rule in &policy.rules {
            if let Some(ref condition) = rule.condition {
                if !condition(context) {
                    continue;
                }
            }
            return match rule.effect {
                RuleEffect::Permit => Decision::Permit,
                RuleEffect::Deny => Decision::Deny,
            };
        }
        Decision::NotApplicable
    }
}
```

### 2. RBAC 权限检查

```rust
//! RBAC 权限检查

use std::collections::HashMap;

/// RBAC 配置
#[derive(Debug, Clone)]
pub struct RbacConfig {
    /// 角色层级
    pub role_hierarchy: HashMap<String, Vec<String>>,
    /// 角色权限映射
    pub role_permissions: HashMap<String, Vec<String>>,
    /// 权限定义
    pub permissions: HashMap<String, PermissionDef>,
}

/// 权限定义
#[derive(Debug, Clone)]
pub struct PermissionDef {
    pub resource: String,
    pub actions: Vec<String>,
}

/// RBAC 检查器
pub struct RbacChecker {
    config: RbacConfig,
}

impl RbacChecker {
    pub fn new(config: RbacConfig) -> Self {
        Self { config }
    }

    /// 检查用户是否有权限
    pub fn check_permission(
        &self,
        user_roles: &[String],
        resource: &str,
        action: &str,
    ) -> bool {
        // 获取所有继承的角色
        let all_roles = self.expand_roles(user_roles);

        // 检查是否有权限
        for role in &all_roles {
            if let Some(perms) = self.config.role_permissions.get(role) {
                for perm_id in perms {
                    if let Some(perm) = self.config.permissions.get(perm_id) {
                        if perm.resource == resource && perm.actions.contains(&action) {
                            return true;
                        }
                    }
                }
            }
        }

        false
    }

    /// 展开角色层级
    fn expand_roles(&self, roles: &[String]) -> Vec<String> {
        let mut expanded = Vec::new();
        let mut visited = std::collections::HashSet::new();
        let mut queue = Vec::new();

        for role in roles {
            if !visited.contains(role) {
                queue.push(role.clone());
                visited.insert(role.clone());
            }
        }

        while let Some(role) = queue.pop() {
            expanded.push(role.clone());

            if let Some(parents) = self.config.role_hierarchy.get(&role) {
                for parent in parents {
                    if !visited.contains(parent) {
                        visited.insert(parent.clone());
                        queue.push(parent.clone());
                    }
                }
            }
        }

        expanded
    }

    /// 获取用户的所有权限
    pub fn get_user_permissions(&self, user_roles: &[String]) -> Vec<String> {
        let all_roles = self.expand_roles(user_roles);
        let mut permissions = std::collections::HashSet::new();

        for role in &all_roles {
            if let Some(role_perms) = self.config.role_permissions.get(role) {
                for perm in role_perms {
                    permissions.insert(perm.clone());
                }
            }
        }

        permissions.into_iter().collect()
    }
}
```

### 3. 策略缓存

```rust
//! 策略缓存

use crate::{Policy, PolicyEvaluator};
use std::sync::Arc;
use tokio::sync::RwLock;
use std::time::{Duration, Instant};

/// 缓存配置
#[derive(Debug, Clone)]
pub struct PolicyCacheConfig {
    pub ttl: Duration,
    pub max_size: usize,
}

/// 缓存条目
struct CacheEntry {
    policy: Policy,
    inserted_at: Instant,
}

/// 策略缓存
pub struct PolicyCache {
    config: PolicyCacheConfig,
    cache: Arc<RwLock<HashMap<String, CacheEntry>>>,
}

impl PolicyCache {
    pub fn new(config: PolicyCacheConfig) -> Self {
        Self {
            config,
            cache: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// 获取策略
    pub async fn get(&self, policy_id: &str) -> Option<Policy> {
        let cache = self.cache.read().await;
        cache.get(policy_id).map(|entry| entry.policy.clone())
    }

    /// 存储策略
    pub async fn set(&self, policy: Policy) {
        let mut cache = self.cache.write().await;
        
        // 清理过期条目
        let now = Instant::now();
        cache.retain(|_, v| now.duration_since(v.inserted_at) < self.config.ttl);

        // 清理超出大小的条目
        if cache.len() >= self.config.max_size {
            let to_remove = cache.len() - self.config.max_size + 1;
            let keys: Vec<String> = cache.keys().take(to_remove).cloned().collect();
            for key in keys {
                cache.remove(&key);
            }
        }

        cache.insert(policy.id.clone(), CacheEntry {
            policy,
            inserted_at: Instant::now(),
        });
    }

    /// 失效策略
    pub async fn invalidate(&self, policy_id: &str) {
        let mut cache = self.cache.write().await;
        cache.remove(policy_id);
    }

    /// 清理所有
    pub async fn clear(&self) {
        let mut cache = self.cache.write().await;
        cache.clear();
    }
}
```

---

## 最佳实践

### 1. 策略定义 DSL

```rust
//! 策略构建器

use crate::{Policy, PolicyTarget, Rule, RuleEffect, CombiningAlgorithm};

/// 策略构建器
pub struct PolicyBuilder {
    policy: Policy,
}

impl PolicyBuilder {
    pub fn new(id: &str) -> Self {
        Self {
            policy: Policy {
                id: id.to_string(),
                target: PolicyTarget {
                    subjects: Vec::new(),
                    resources: Vec::new(),
                    actions: Vec::new(),
                },
                rules: Vec::new(),
                combining_algorithm: CombiningAlgorithm::DenyOverrides,
            },
        }
    }

    pub fn with_subject_roles(mut self, roles: &[&str]) -> Self {
        self.policy.target.subjects = vec![roles.iter().map(|s| s.to_string()).collect()];
        self
    }

    pub fn with_resource(mut self, resource: &str) -> Self {
        self.policy.target.resources = vec![resource.to_string()];
        self
    }

    pub fn with_action(mut self, action: &str) -> Self {
        self.policy.target.actions = vec![action.to_string()];
        self
    }

    pub fn add_rule(
        mut self,
        id: &str,
        effect: RuleEffect,
        condition: impl Fn(&crate::RequestContext) -> bool + Send + 'static,
    ) -> Self {
        self.policy.rules.push(Rule {
            id: id.to_string(),
            effect,
            condition: Some(Box::new(condition)),
        });
        self
    }

    pub fn with_combining_algorithm(mut self, algo: CombiningAlgorithm) -> Self {
        self.policy.combining_algorithm = algo;
        self
    }

    pub fn build(self) -> Policy {
        self.policy
    }
}

/// 使用示例
fn example_policy() -> Policy {
    PolicyBuilder::new("read-policy")
        .with_subject_roles(&["user", "admin"])
        .with_resource("document")
        .with_action("read")
        .add_rule("own-document", RuleEffect::Permit, |ctx| {
            // 自己创建的文档可以读取
            ctx.resource.attributes.get("owner") == Some(&ctx.subject.id)
        })
        .add_rule("public-document", RuleEffect::Permit, |ctx| {
            // 公开文档可以读取
            ctx.resource.attributes.get("visibility") == Some(&"public".to_string())
        })
        .with_combining_algorithm(CombiningAlgorithm::DenyOverrides)
        .build()
}
```

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| 决策不一致 | 组合算法选择不当 | 根据业务选择合适的算法 |
| 性能差 | 策略过多 | 使用缓存和索引 |
| 权限绕过 | 规则顺序问题 | DenyOverrides 优先 |

---

## 关联技能

- `rust-auth` - 认证授权
- `rust-web` - Web 集成
- `rust-cache` - 策略缓存
- `rust-performance` - 性能优化

