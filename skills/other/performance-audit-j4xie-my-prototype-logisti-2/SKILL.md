---
name: performance-audit
description: 分析后端性能问题，检测 N+1 查询、无分页查询、全表扫描、AI 服务超时等。使用此 Skill 来评估系统性能瓶颈、检测数据库查询问题、或优化 API 响应时间。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# 后端性能审计 Skill

## 性能问题分类

| 问题类型 | 严重程度 | 影响 |
|----------|----------|------|
| N+1 查询 | 高 | 100 用户 = 101 次 DB 查询 |
| 无分页 findAll() | 高 | 全表加载，内存溢出 |
| LIKE %keyword% | 中 | 无法使用索引 |
| AI 服务同步阻塞 | 高 | 线程池耗尽 |

## 已知问题位置

### N+1 查询
| 文件 | 行号 | 问题 |
|------|------|------|
| MobileServiceImpl.java | 990-995 | 人员统计循环查询 |
| MobileServiceImpl.java | 1061-1064 | 工时排行循环查询 |
| MobileServiceImpl.java | 1141-1142 | 加班统计循环查询 |
| MobileServiceImpl.java | 1228-1231 | 人员绩效循环查询 |

### 无分页 findAll()
| 文件 | 行号 |
|------|------|
| PlatformServiceImpl | 50-52 |
| AIReportScheduler | 61-63 |
| FactoryServiceImpl | 38-40 |

### LIKE 全表扫描
| 文件 | 行号 |
|------|------|
| CustomerRepository | 49 |
| SupplierRepository | 49 |
| MaterialBatchRepository | 126 |
| UserRepository | 73-75 |

## 检测命令

```bash
cd /Users/jietaoxie/my-prototype-logistics/backend-java

# 1. N+1 查询 - for 循环中的 repository 调用
grep -rn "for.*{" src/main/java/com/cretas/aims/service/ -A10 | \
  grep -B5 "repository\|Repository" | head -50

# 2. 无分页 findAll()
grep -rn "\.findAll()" src/main/java/ --include="*.java" | grep -v "Pageable"

# 3. 左模糊 LIKE (无法使用索引)
grep -rn "LIKE %:" src/main/java/ --include="*.java"

# 4. RestTemplate 超时配置
grep -rn "RestTemplate" src/main/java/ --include="*.java" -A5 | head -30

# 5. 巨型类 (>500行)
wc -l src/main/java/com/cretas/aims/service/impl/*.java | awk '$1 > 500'

# 6. 缓存/异步使用
grep -rn "@Cacheable\|@Async" src/main/java/ --include="*.java"
```

## 修复要点

| 问题 | 修复方案 |
|------|----------|
| N+1 查询 | 批量查询 `findByUserIdIn(userIds)` + groupingBy |
| 无分页 | `findAll(PageRequest.of(0, 100))` |
| 左模糊 | 改为右模糊 `LIKE CONCAT(:keyword, '%')` |
| AI 超时 | `setConnectTimeout(5000)` + `@Async` |

## 参考

- 完整审计报告: `backend-java/BACKEND_AUDIT_REPORT.md`
