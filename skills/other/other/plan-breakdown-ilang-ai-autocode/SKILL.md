---
name: plan-breakdown
description: Break large tasks into small, concrete steps. Each step should take 2-5 minutes.
---

# Task Breakdown

When building anything medium or large:
1. Break into 5-15 concrete steps
2. Each step has a clear deliverable ("完成登录页面", "数据库建好了")
3. Steps are ordered by dependency — can't build login before database
4. Show the plan to the user in plain language: "我分这几步来做：第一步...第二步..."
5. Each step, when completed, should produce something visible or testable
6. Never have a step longer than 5 minutes of work

Format for user:
```
我来分几步做：
1. 先把基础框架搭好（2分钟）
2. 做用户注册页面（5分钟）
3. 做登录功能（5分钟）
4. 连接数据库存用户信息（3分钟）
5. 测试确保都能跑（3分钟）
大概20分钟搞定。
```
