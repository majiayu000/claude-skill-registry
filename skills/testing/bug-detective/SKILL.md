---
name: bug-detective
description: |
  基于若依-vue-plus框架的Bug排查与调试标准流程。提供系统化的问题诊断方法论，涵盖：
  1. 日志链路追踪与TraceId全链路分析
  2. 全局异常处理器的堆栈解析方法
  3. 框架级常见陷阱（Long精度丢失、逻辑删除、缓存不一致、权限拦截）
  4. MyBatis-Plus与Redis的排查技巧
  5. 分布式环境下的事务与并发问题定位
  
  触发场景：
  - 系统报错（500/403/404等HTTP错误码）
  - 接口返回异常数据或格式错误
  - 前端显示数据与数据库不一致
  - 查询结果为空或数据缺失
  - 事务回滚或数据不一致
  - 缓存穿透、雪崩或击穿
  - 性能问题（慢查询、高CPU、OOM）
  
  触发词：Bug排查、异常定位、日志分析、TraceId追踪、精度丢失、逻辑删除、缓存不一致、权限403、事务失效、慢查询、N+1问题
---

# Bug 排查与调试规范

> **核心理念**：遵循"日志→异常→数据→配置→代码"的五层排查法，优先使用框架提供的诊断工具，避免盲目猜测和改动代码。

## 核心规范

### 规范1：日志链路追踪与全局异常解析

**详细说明**：
生产环境排查必须依赖`TraceId`进行全链路日志追踪。若依框架通过MDC（Mapped Diagnostic Context）自动为每个请求生成唯一TraceId，贯穿Controller→Service→Mapper全流程。

**排查步骤**：
1. **获取TraceId**：从日志文件或响应头`X-Trace-Id`中提取
2. **过滤完整链路**：使用`grep "TraceId=xxxxx" application.log`查看完整调用链
3. **定位异常层级**：优先查看`GlobalExceptionHandler`捕获的堆栈信息，不要仅关注Controller层
4. **解析业务异常**：若依框架异常通常封装在`ServiceException`中，需仔细阅读`code`和`message`字段
5. **检查嵌套异常**：使用`e.getCause()`追踪底层异常（如SQL异常、Redis连接异常）

**关键配置**：
```yaml
# application.yml 日志配置示例
logging:
  level:
    com.ruoyi: INFO
    com.ruoyi.system.mapper: DEBUG  # 仅对Mapper开启SQL日志
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] [%X{traceId}] %-5level %logger{36} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%X{traceId}] %-5level %logger{50} - %msg%n"
```

```java
/**
 * 全局异常处理器 (若依标准配置)
 */
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    /**
     * 业务异常
     */
    @ExceptionHandler(ServiceException.class)
    public R<Void> handleServiceException(ServiceException e, HttpServletRequest request) {
        String traceId = MDC.get("traceId");
        log.error("业务异常发生 [TraceId:{}] [URI:{}] [错误码:{}] [消息:{}]", 
                  traceId, request.getRequestURI(), e.getCode(), e.getMessage());
        // 必须返回错误码和具体错误信息，而非直接暴露堆栈
        return R.fail(e.getCode(), e.getMessage());
    }

    /**
     * 系统异常
     */
    @ExceptionHandler(Exception.class)
    public R<Void> handleException(Exception e, HttpServletRequest request) {
        String traceId = MDC.get("traceId");
        log.error("系统异常发生 [TraceId:{}] [URI:{}]", traceId, request.getRequestURI(), e);
        // 生产环境不暴露详细堆栈，记录traceId供后续排查
        return R.fail("系统内部错误，请联系管理员（TraceId:" + traceId + "）");
    }
    
    /**
     * 数据库异常（常见于SQL语法错误、字段不存在）
     */
    @ExceptionHandler(SQLException.class)
    public R<Void> handleSQLException(SQLException e, HttpServletRequest request) {
        String traceId = MDC.get("traceId");
        log.error("数据库异常 [TraceId:{}] [SQLState:{}] [ErrorCode:{}]", 
                  traceId, e.getSQLState(), e.getErrorCode(), e);
        return R.fail("数据操作失败（TraceId:" + traceId + "）");
    }
}
```

### 规范2：常见框架级Bug模式识别

**详细说明**：
若依框架基于MyBatis-Plus和SpringBoot构建，存在几类高频Bug模式。排查数据异常时，需按以下优先级检查：

#### 2.1 Long精度丢失问题
**现象**：前端显示的ID末尾变为00，导致根据ID查询失败  
**原因**：JavaScript的`Number`类型最大安全整数为`2^53-1`（16位），Java的`Long`为64位  
**解决方案**：

```java
// 方案1：全局配置（推荐）
@Configuration
public class JacksonConfig {
    @Bean
    public Jackson2ObjectMapperBuilderCustomizer customizer() {
        return builder -> {
            // 所有Long类型自动转为String
            builder.serializerByType(Long.class, ToStringSerializer.instance);
            builder.serializerByType(Long.TYPE, ToStringSerializer.instance);
        };
    }
}

// 方案2：实体类单独标注
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.ToStringSerializer;

public class SysUser extends BaseEntity {
    
    @JsonSerialize(using = ToStringSerializer.class)
    private Long userId;
    
    @JsonSerialize(using = ToStringSerializer.class)
    private Long deptId;
}
```

**排查命令**：
```javascript
// 浏览器控制台验证
console.log(Number.MAX_SAFE_INTEGER);  // 9007199254740991
console.log(userId > Number.MAX_SAFE_INTEGER);  // true则必定丢失精度
```

#### 2.2 逻辑删除陷阱
**现象**：数据库有数据，但查询结果为空  
**原因**：若依默认使用`@TableLogic`实现软删除，MyBatis-Plus会自动在SQL添加`WHERE del_flag = 0`  
**解决方案**：

```java
// 排查逻辑删除配置
@TableName(value = "sys_user")
public class SysUser {
    
    // 若依默认逻辑删除字段：0未删除 2已删除
    // 如果查询结果为空，检查数据库该字段值是否被意外置为2
    @TableLogic(value = "0", delval = "2")
    private String delFlag;
}
```

**排查步骤**：
1. 检查实体类是否有`@TableLogic`注解
2. 查询数据库原始数据：`SELECT * FROM sys_user WHERE user_id = ? -- 不经过MyBatis-Plus`
3. 检查`del_flag`字段值：若为2则表示已逻辑删除
4. 确认业务逻辑：是否应该查询已删除数据（需使用`includedDeleted()`）

```java
// 需要查询已删除数据的场景
List<SysUser> users = userMapper.selectList(
    Wrappers.<SysUser>lambdaQuery()
        .eq(SysUser::getUserName, "admin")
        // 包含已删除数据
        .apply("1=1") // 绕过逻辑删除（不推荐）
);

// 推荐方式：使用原生SQL
@Select("SELECT * FROM sys_user WHERE user_name = #{userName}")
List<SysUser> selectIncludingDeleted(@Param("userName") String userName);
```

#### 2.3 权限拦截403问题
**现象**：接口返回403 Forbidden，但用户已登录  
**原因**：若依的`@PreAuthorize`权限注解校验失败  
**解决方案**：

```java
// 排查权限配置
@RestController
@RequestMapping("/system/user")
public class SysUserController {
    
    // 检查权限标识是否与菜单配置一致
    @PreAuthorize("@ss.hasPermi('system:user:query')")
    @GetMapping("/list")
    public R<List<SysUser>> list() {
        // ...
    }
}
```

**排查步骤**：
1. 检查用户是否拥有该权限：`SELECT * FROM sys_role_menu WHERE role_id = ? AND menu_id = ?`
2. 检查菜单权限标识：`SELECT perms FROM sys_menu WHERE menu_id = ?`
3. 对比代码中的`@PreAuthorize`值与数据库`perms`字段是否一致
4. 检查Redis缓存：`GET login_tokens:{token}` 确认用户权限列表

#### 2.4 缓存不一致问题
**现象**：修改数据后，查询仍返回旧数据  
**原因**：Redis缓存未及时更新或删除  
**解决方案**：

```java
// 正确的缓存更新模式
@Service
public class SysUserServiceImpl implements ISysUserService {
    
    @Autowired
    private RedisCache redisCache;
    
    private static final String USER_CACHE_KEY = "user:info:";
    
    @Override
    @Transactional
    public int updateUser(SysUser user) {
        int rows = userMapper.updateById(user);
        if (rows > 0) {
            // 先更新数据库，后删除缓存（Cache-Aside模式）
            redisCache.deleteObject(USER_CACHE_KEY + user.getUserId());
        }
        return rows;
    }
    
    @Override
    public SysUser selectUserById(Long userId) {
        // 先查缓存，缓存未命中再查数据库
        String cacheKey = USER_CACHE_KEY + userId;
        SysUser user = redisCache.getCacheObject(cacheKey);
        if (user == null) {
            user = userMapper.selectById(userId);
            if (user != null) {
                // 设置缓存过期时间，防止永久占用内存
                redisCache.setCacheObject(cacheKey, user, 30, TimeUnit.MINUTES);
            }
        }
        return user;
    }
}
```

**排查命令**：
```bash
# Redis CLI 检查缓存
redis-cli
> KEYS user:info:*
> GET user:info:1
> TTL user:info:1  # 检查过期时间
> DEL user:info:1  # 手动删除测试
```

### 规范3：数据库慢查询与N+1问题

**详细说明**：
性能问题往往源于低效的SQL查询，特别是循环中的单条查询（N+1问题）。

**排查步骤**：

1. **开启SQL日志**：
```yaml
# application-dev.yml
mybatis-plus:
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

2. **识别N+1问题**：
```java
// ❌ 错误示例：N+1查询
List<SysUser> users = userMapper.selectList(null);
for (SysUser user : users) {
    // 每次循环都查询一次数据库！
    SysDept dept = deptMapper.selectById(user.getDeptId());
    user.setDept(dept);
}

// ✅ 正确示例：批量查询或关联查询
List<SysUser> users = userMapper.selectUserListWithDept();
// 或使用MyBatis-Plus的批量查询
List<Long> deptIds = users.stream()
    .map(SysUser::getDeptId)
    .distinct()
    .collect(Collectors.toList());
List<SysDept> depts = deptMapper.selectBatchIds(deptIds);
Map<Long, SysDept> deptMap = depts.stream()
    .collect(Collectors.toMap(SysDept::getDeptId, dept -> dept));
users.forEach(user -> user.setDept(deptMap.get(user.getDeptId())));
```

3. **使用MyBatis-Plus关联查询**：
```xml
<!-- SysUserMapper.xml -->
<select id="selectUserListWithDept" resultType="SysUser">
    SELECT u.*, d.dept_name
    FROM sys_user u
    LEFT JOIN sys_dept d ON u.dept_id = d.dept_id
    WHERE u.del_flag = '0'
</select>
```

### 规范4：事务失效问题

**详细说明**：
`@Transactional`注解失效是常见Bug，导致数据不一致。

**失效场景与解决方案**：

#### 4.1 非public方法
```java
// ❌ 事务不生效
@Transactional
private void updateUser(SysUser user) { }

// ✅ 必须是public方法
@Transactional
public void updateUser(SysUser user) { }
```

#### 4.2 同类方法调用
```java
@Service
public class UserService {
    
    // ❌ 事务不生效（自调用问题）
    public void outerMethod() {
        this.innerMethod();  // 直接调用，未经过代理
    }
    
    @Transactional
    public void innerMethod() {
        // 事务失效
    }
    
    // ✅ 解决方案1：拆分到不同类
    @Autowired
    private UserTransactionService transactionService;
    
    public void outerMethod() {
        transactionService.innerMethod();  // 经过Spring代理
    }
    
    // ✅ 解决方案2：注入自身代理
    @Autowired
    @Lazy
    private UserService self;
    
    public void outerMethod() {
        self.innerMethod();
    }
}
```

#### 4.3 异常被捕获
```java
// ❌ 事务不回滚
@Transactional
public void updateUser(SysUser user) {
    try {
        userMapper.updateById(user);
        int i = 1 / 0;  // 触发异常
    } catch (Exception e) {
        log.error("更新失败", e);
        // 异常被吞掉，事务不回滚！
    }
}

// ✅ 解决方案1：重新抛出异常
@Transactional
public void updateUser(SysUser user) {
    try {
        userMapper.updateById(user);
        int i = 1 / 0;
    } catch (Exception e) {
        log.error("更新失败", e);
        throw new ServiceException("用户更新失败");
    }
}

// ✅ 解决方案2：手动回滚
@Transactional
public void updateUser(SysUser user) {
    try {
        userMapper.updateById(user);
        int i = 1 / 0;
    } catch (Exception e) {
        log.error("更新失败", e);
        TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
        return;
    }
}
```

#### 4.4 错误的异常类型
```java
// ❌ 检查异常不回滚
@Transactional
public void updateUser(SysUser user) throws Exception {
    userMapper.updateById(user);
    throw new Exception("检查异常");  // 事务不回滚！
}

// ✅ 指定回滚异常类型
@Transactional(rollbackFor = Exception.class)
public void updateUser(SysUser user) throws Exception {
    userMapper.updateById(user);
    throw new Exception("检查异常");
}
```

### 规范5：前后端数据交互问题

**详细说明**：
前后端数据格式不一致、时间时区偏差、空值处理等问题的排查。

#### 5.1 日期时间格式问题
**现象**：前端显示时间与数据库相差8小时  
**原因**：时区配置不一致或序列化格式错误  
**解决方案**：

```java
// 全局配置时区和日期格式
@Configuration
public class JacksonConfig {
    @Bean
    public Jackson2ObjectMapperBuilderCustomizer customizer() {
        return builder -> {
            // 设置时区为东八区
            builder.timeZone(TimeZone.getTimeZone("GMT+8"));
            // 设置日期格式
            builder.simpleDateFormat("yyyy-MM-dd HH:mm:ss");
        };
    }
}

// 实体类单独配置
public class SysUser extends BaseEntity {
    
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
    private Date createTime;
}
```

```yaml
# application.yml 配置
spring:
  jackson:
    time-zone: GMT+8
    date-format: yyyy-MM-dd HH:mm:ss
```

#### 5.2 空值处理问题
**现象**：前端收到`null`字段，导致解析错误  
**原因**：后端未配置空值序列化策略  
**解决方案**：

```java
// 全局配置空值处理
@Configuration
public class JacksonConfig {
    @Bean
    public Jackson2ObjectMapperBuilderCustomizer customizer() {
        return builder -> {
            // null值不返回
            builder.serializationInclusion(JsonInclude.Include.NON_NULL);
            // 或将null转为空字符串/空数组
            // builder.serializationInclusion(JsonInclude.Include.ALWAYS);
        };
    }
}

// 实体类单独配置
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SysUser extends BaseEntity {
    private String nickName;
}
```

### 规范6：分页查询问题

**详细说明**：
MyBatis-Plus分页插件配置错误、分页参数传递问题。

**常见问题与解决方案**：

```java
// ❌ 错误示例：分页插件未生效
@GetMapping("/list")
public R<List<SysUser>> list(PageQuery pageQuery) {
    // 直接查询，无分页效果
    List<SysUser> users = userMapper.selectList(null);
    return R.ok(users);
}

// ✅ 正确示例1：使用PageHelper（若依默认）
@GetMapping("/list")
public TableDataInfo<SysUser> list(SysUser user, PageQuery pageQuery) {
    // PageHelper会自动拦截下一条查询并添加分页
    startPage();
    List<SysUser> list = userService.selectUserList(user);
    return getDataTable(list);
}

// ✅ 正确示例2：使用MyBatis-Plus分页
@GetMapping("/list")
public R<Page<SysUser>> list(PageQuery pageQuery) {
    Page<SysUser> page = new Page<>(pageQuery.getPageNum(), pageQuery.getPageSize());
    Page<SysUser> result = userMapper.selectPage(page, null);
    return R.ok(result);
}
```

**分页插件配置**：
```java
@Configuration
public class MybatisPlusConfig {
    
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        // 添加分页插件
        PaginationInnerInterceptor paginationInnerInterceptor = new PaginationInnerInterceptor();
        // 设置数据库类型
        paginationInnerInterceptor.setDbType(DbType.MYSQL);
        // 设置单页最大限制数量
        paginationInnerInterceptor.setMaxLimit(500L);
        interceptor.addInnerInterceptor(paginationInnerInterceptor);
        return interceptor;
    }
}
```

## 禁止事项

### 代码层面
- ❌ **禁止吞掉异常**：`try { ... } catch (Exception e) {}`不记录日志，导致问题无法追溯
- ❌ **禁止循环查询数据库**：在`for`循环中单条执行数据库查询或更新（N+1问题），这是性能Bug的根源
- ❌ **禁止不指定事务回滚异常类型**：`@Transactional`默认只回滚`RuntimeException`，检查异常需手动指定`rollbackFor`
- ❌ **禁止直接返回敏感异常信息**：生产环境不能将SQL异常、堆栈信息直接暴露给前端
- ❌ **禁止在事务方法中捕获异常不抛出**：会导致事务不回滚，数据不一致

### 配置层面
- ❌ **禁止生产环境开启DEBUG日志**：将`logging.level.root`设置为`DEBUG`，会产生海量日志导致IO阻塞和磁盘爆满
- ❌ **禁止关闭SQL注入防护**：不要在Mapper中使用`${}`拼接参数，必须使用`#{}`预编译
- ❌ **禁止缓存无过期时间**：Redis缓存必须设置合理的过期时间，防止内存泄漏
- ❌ **禁止忽略逻辑删除注解**：直接使用原生SQL绕过`@TableLogic`可能导致查询到已删除数据

### 排查层面
- ❌ **禁止没有TraceId就开始排查**：生产问题必须先定位TraceId，获取完整调用链
- ❌ **禁止仅看Controller层日志**：异常可能在Service或Mapper层抛出，需全链路排查
- ❌ **禁止随意修改配置**：排查问题时不要轻易修改`application.yml`配置，应先分析日志
- ❌ **禁止直连生产数据库修改数据**：排查时只能SELECT查询，修改数据需走正规变更流程

### 数据库层面
- ❌ **禁止SELECT ***：查询时应明确指定字段，特别是有大字段（TEXT、BLOB）时
- ❌ **禁止在WHERE条件中使用函数**：如`WHERE DATE_FORMAT(create_time, '%Y-%m-%d') = '2026-01-26'`会导致索引失效
- ❌ **禁止使用!=或<>**：这两个操作符无法使用索引，应改为`NOT IN`或拆分为`>`和`<`
- ❌ **禁止JOIN过多表**：超过3个表的JOIN会导致性能急剧下降，考虑拆分查询或冗余设计

## 参考代码路径

若依框架核心配置与工具类文件路径：

### 异常处理相关
- `ruoyi-framework/src/main/java/com/ruoyi/framework/web/exception/GlobalExceptionHandler.java`
- `ruoyi-common/src/main/java/com/ruoyi/common/exception/ServiceException.java`
- `ruoyi-common/src/main/java/com/ruoyi/common/exception/base/BaseException.java`

### 序列化配置相关
- `ruoyi-common/src/main/java/com/ruoyi/common/config/JacksonConfig.java`
- `ruoyi-framework/src/main/java/com/ruoyi/framework/config/FastJson2JsonRedisSerializer.java`

### 实体类相关
- `ruoyi-system/src/main/java/com/ruoyi/system/domain/SysUser.java`
- `ruoyi-common/src/main/java/com/ruoyi/common/core/domain/BaseEntity.java`

### MyBatis-Plus配置
- `ruoyi-framework/src/main/java/com/ruoyi/framework/config/MybatisPlusConfig.java`
- `ruoyi-framework/src/main/java/com/ruoyi/framework/config/MybatisPlusMetaObjectHandler.java`

### Redis缓存相关
- `ruoyi-common/src/main/java/com/ruoyi/common/utils/redis/RedisCache.java`
- `ruoyi-framework/src/main/java/com/ruoyi/framework/config/RedisConfig.java`

### 权限校验相关
- `ruoyi-framework/src/main/java/com/ruoyi/framework/web/service/PermissionService.java`
- `ruoyi-framework/src/main/java/com/ruoyi/framework/config/SecurityConfig.java`

## 检查清单（Bug排查必查项）

### 第一层：日志排查
- [ ] 是否获取了TraceId并过滤出完整调用链日志
- [ ] 是否查看了`GlobalExceptionHandler`的异常堆栈
- [ ] 是否检查了日志中的SQL语句（开启MyBatis日志）
- [ ] 是否确认了异常发生的具体层级（Controller/Service/Mapper）
- [ ] 是否检查了嵌套异常的底层原因（`e.getCause()`）

### 第二层：异常排查
- [ ] 是否确认了异常类型（业务异常/系统异常/数据库异常）
- [ ] 是否检查了异常的错误码和错误信息
- [ ] 是否排查了异常是否被捕获后未重新抛出
- [ ] 是否确认了异常是否触发了事务回滚
- [ ] 是否检查了异常是否与权限拦截有关（403错误）

### 第三层：数据排查
- [ ] 是否排查了Long类型的序列化配置（精度丢失）
- [ ] 是否检查了逻辑删除字段状态（`del_flag`）
- [ ] 是否确认了数据库原始数据是否存在（直接SELECT查询）
- [ ] 是否检查了缓存与数据库的数据一致性
- [ ] 是否排查了日期时间的时区和格式问题
- [ ] 是否检查了空值处理配置（null序列化）

### 第四层：配置排查
- [ ] 是否检查了`application.yml`的数据库连接配置
- [ ] 是否确认了Redis连接配置和缓存过期时间
- [ ] 是否检查了MyBatis-Plus的全局配置（逻辑删除、分页插件）
- [ ] 是否确认了Jackson的序列化配置（时区、日期格式、Long转String）
- [ ] 是否检查了权限配置（`@PreAuthorize`与数据库`perms`字段）

### 第五层：代码排查
- [ ] 是否确认了事务注解`@Transactional`是否生效
- [ ] 是否排查了N+1查询问题（循环中的单条查询）
- [ ] 是否检查了分页插件是否正确配置和使用
- [ ] 是否确认了SQL语句的索引使用情况（EXPLAIN分析）
- [ ] 是否检查了并发问题（乐观锁/悲观锁/分布式锁）

### 性能问题专项排查
- [ ] 是否使用`EXPLAIN`分析了慢SQL的执行计划
- [ ] 是否检查了是否存在全表扫描（type=ALL）
- [ ] 是否确认了索引是否失效（未使用index）
- [ ] 是否排查了是否存在JOIN过多表的情况
- [ ] 是否检查了Redis缓存命中率（`INFO stats`）
- [ ] 是否使用JVM工具排查了内存泄漏（jmap、MAT）

## 快速诊断命令

### 日志排查命令
```bash
# 根据TraceId过滤日志
grep "TraceId=xxxxx" application.log

# 查看最近的错误日志
tail -f application.log | grep "ERROR"

# 统计某个异常的出现次数
grep "ServiceException" application.log | wc -l
```

### 数据库排查命令
```sql
-- 检查逻辑删除状态
SELECT user_id, user_name, del_flag FROM sys_user WHERE user_id = ?;

-- 分析SQL执行计划
EXPLAIN SELECT * FROM sys_user WHERE user_name = 'admin';

-- 查看慢查询日志
SHOW VARIABLES LIKE 'slow_query%';
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;
```

### Redis排查命令
```bash
# 连接Redis
redis-cli

# 查看所有key
KEYS *

# 查看某个key的值和过期时间
GET user:info:1
TTL user:info:1

# 查看缓存命中率
INFO stats

# 清空某个前缀的key
redis-cli --scan --pattern "user:info:*" | xargs redis-cli DEL
```

### 权限排查SQL
```sql
-- 查询用户的所有角色
SELECT r.* FROM sys_role r
INNER JOIN sys_user_role ur ON r.role_id = ur.role_id
WHERE ur.user_id = ?;

-- 查询角色的所有权限
SELECT m.perms FROM sys_menu m
INNER JOIN sys_role_menu rm ON m.menu_id = rm.menu_id
WHERE rm.role_id = ?;

-- 查询用户的所有权限（完整链路）
SELECT DISTINCT m.perms FROM sys_menu m
INNER JOIN sys_role_menu rm ON m.menu_id = rm.menu_id
INNER JOIN sys_user_role ur ON rm.role_id = ur.role_id
WHERE ur.user_id = ? AND m.perms IS NOT NULL;
```

## 高级排查技巧

### 1. 使用Arthas诊断JVM问题
```bash
# 下载并启动Arthas
curl -O https://arthas.aliyun.com/arthas-boot.jar
java -jar arthas-boot.jar

# 监控方法执行耗时
trace com.ruoyi.system.service.impl.SysUserServiceImpl selectUserList

# 查看方法参数和返回值
watch com.ruoyi.system.service.impl.SysUserServiceImpl selectUserList "{params,returnObj}" -x 2

# 反编译类文件
jad com.ruoyi.system.service.impl.SysUserServiceImpl
```

### 2. 使用MyBatis日志插件
```xml
<!-- pom.xml 添加依赖 -->
<dependency>
    <groupId>p6spy</groupId>
    <artifactId>p6spy</artifactId>
    <version>3.9.1</version>
</dependency>
```

```yaml
# application.yml 配置
spring:
  datasource:
    driver-class-name: com.p6spy.engine.spy.P6SpyDriver
    url: jdbc:p6spy:mysql://localhost:3306/ry-vue
```

### 3. 开启SQL性能分析
```java
@Configuration
public class MybatisPlusConfig {
    
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        
        // 添加性能分析插件（仅开发环境）
        if (environment.acceptsProfiles(Profiles.of("dev"))) {
            PerformanceInterceptor performanceInterceptor = new PerformanceInterceptor();
            performanceInterceptor.setMaxTime(1000); // 超过1秒的SQL输出
            performanceInterceptor.setFormat(true);  // 格式化SQL
            // 注意：MyBatis-Plus 3.x 已移除此插件，建议使用p6spy
        }
        
        return interceptor;
    }
}
```

## 总结

遵循本规范的五层排查法：

1. **日志层**：获取TraceId，过滤完整调用链
2. **异常层**：分析异常类型、错误码、堆栈信息
3. **数据层**：检查数据库原始数据、缓存数据、逻辑删除状态
4. **配置层**：确认框架配置、序列化配置、权限配置
5. **代码层**：排查事务、N+1查询、索引使用

**核心原则**：先看日志，再查数据，后改代码；优先使用框架工具，避免盲目猜测。
