---
name: java-springboot-dev
description: Java Spring Boot 开发规范和最佳实践指南。适用于企业级Java后端开发，涵盖项目架构、编码规范、安全实践、性能优化等全方位内容。
---

# Java Spring Boot 开发规范

## 技术栈

本项目基于 **Spring Boot 3.x + MyBatis-Plus + Spring Security + PostgreSQL + Redis**

## 核心原则

- **SOLID 原则**：单一职责、开闭原则、里氏替换、接口隔离、依赖倒置
- **DRY 原则**：Don't Repeat Yourself，避免代码重复
- **KISS 原则**：Keep It Simple, Stupid，保持简单
- **YAGNI 原则**：You Aren't Gonna Need It，不要过度设计
- **OWASP 安全最佳实践**：输入验证、SQL注入防护、XSS防护、CSRF防护
- **代码覆盖率**：单元测试覆盖率 ≥ 80%

## 项目架构

### 模块划分

```
project-root/
├── gyl-common/          # 通用工具模块
│   ├── util/           # 工具类
│   ├── dto/            # 通用DTO
│   ├── enums/          # 通用枚举
│   ├── result/         # 统一响应封装
│   ├── redis/          # Redis工具
│   └── exception/      # 异常定义
├── gyl-core/           # 核心业务模块
│   ├── service/        # Service层
│   ├── manager/        # Manager层
│   ├── dto/            # 业务DTO
│   ├── convert/        # DTO转换
│   └── enums/          # 业务枚举
├── gyl-gateway/        # 网关层
│   └── controller/     # Controller层
├── gyl-mapper/         # 数据持久化层
│   ├── entity/         # 实体类
│   ├── mapper/         # Mapper接口
│   └── resources/mapper/ # MyBatis XML
└── doc/                # 文档目录
    ├── sql/            # SQL文档
    └── api/            # API文档
```

## 分层架构规范

### Gateway层 (Controller)

**职责**：
- 参数校验和验证
- 请求路由和分发
- HTTP响应封装
- **禁止**编写业务逻辑

**调用规范**：
- 只能调用gyl-core下的Service方法
- 禁止直接调用Manager或Mapper
- 超过2个参数必须定义DTO

**API规范**：
- 请求方法：仅允许POST和GET
- 路径规范：
  - 后台管理: `/api/admin/`
  - 商城应用: `/api/app/`
  - 仓配系统: `/api/wms/`
- 响应格式：统一使用 `Result` 封装

**示例**：
```java
@RestController
@RequestMapping("/api/admin/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @PostMapping("/create")
    public Result<UserResponseDTO> createUser(@Valid @RequestBody UserCreateDTO dto) {
        // 仅做参数校验和路由
        UserResponseDTO response = userService.createUser(dto);
        return Result.success(response);
    }
}
```

### Service层

**职责**：
- 业务逻辑实现
- 业务规则校验
- 权限控制
- 事务管理
- 数据验证

**调用规范**：
- 必须通过Manager访问数据库和缓存
- 禁止直接操作Mapper或Redis
- 入参和返参使用DTO类型

**设计原则**：
- 一个业务领域一个Service
- 一个功能一个方法
- 避免Service之间相互调用

**示例**：
```java
@Service
public class UserService {
    
    @Autowired
    private UserManager userManager;
    
    public UserResponseDTO createUser(UserCreateDTO dto) {
        // 业务逻辑
        validateUser(dto);
        
        // 通过Manager操作数据
        UserEntity user = userManager.createUser(dto);
        
        // DTO转换
        return UserConvert.toResponseDTO(user);
    }
}
```

### Manager层

**职责**：
- 封装数据库访问
- 封装缓存操作
- 聚合多表读写
- 提供细粒度的领域方法

**调用规范**：
- 仅供Service层调用
- 禁止Gateway层或其他层直接调用
- 只能调用Mapper接口进行数据库操作
- 统一使用RedisUtil操作Redis

**设计原则**：
- 一个领域聚合一个Manager
- 可组合调用其他Manager，但应避免循环依赖
- 跨表写操作必须使用 `@Transactional(rollbackFor = Exception.class)`

**数据类型**：
- 入参：Entity、自定义DO对象、DTO
- 返回：Entity、DTO、DO对象
- **禁止**使用多个变量作为参数

**错误示例**（禁止）：
```java
// 错误：参数过多
boolean deductPoints(Integer shopId, Integer userId, Integer points, 
                      Integer changeType, String businessType, 
                      String businessId, String remark, 
                      Integer operatorId, String operatorName);
```

**正确示例**：
```java
// 正确：使用DTO
boolean deductPoints(PointDeductDTO dto);
```

**Entity赋值规范**：
- 创建或更新Entity时，**必须**为所有必填字段逐一显式赋值
- **严禁**使用 `BeanUtil.copyProperties()`
- 建议使用Builder模式或全参构造函数

### Mapper层

**职责**：
- 数据库访问
- 通用的增删改查
- 分页查询
- 多表联合查询（不超过3个表）

**技术选型**：
- 优先使用MyBatis-Plus单表CRUD
- 复杂查询使用XML
- 禁止在Mapper方法中写SQL

**接口规范**：
- 必须继承 `com.baomidou.mybatisplus.core.mapper.BaseMapper<Entity>`
- XML文件命名为 `表名+Mapper.xml`
- 存放在 `gyl-mapper/src/main/resources/mapper/`

**数据类型**：
- 入参：Entity、自定义DO对象
- 返回：Entity（整表字段）、DO对象（多表联合字段）
- **禁止**自定义Map类型

**示例**：
```java
// Mapper接口
@Mapper
public interface UserMapper extends BaseMapper<UserEntity> {
    
    // 单表查询使用MyBatis-Plus
    List<UserEntity> selectByCondition(LambdaQueryWrapper<UserEntity> wrapper);
    
    // 多表查询在XML中实现
    UserDetailDO selectUserDetailById(Long userId);
}
```

```xml
<!-- UserMapper.xml -->
<mapper namespace="com.gyl.mapper.UserMapper">
    
    <select id="selectUserDetailById" resultType="com.gyl.mapper.DO.UserDetailDO">
        SELECT u.*, p.phone
        FROM user u
        LEFT JOIN phone p ON u.id = p.user_id
        WHERE u.id = #{userId}
    </select>
    
</mapper>
```

## 通用工具使用规范

### 分页处理

- 所有分页DTO必须继承 `PageQueryDTO`
- 单表查询使用 `MyBatisPlusUtils`
- 分页返回对象使用 `ListWithPageDTO`

```java
// 分页查询DTO
public class UserPageQueryDTO extends PageQueryDTO {
    private String username;
    private Integer status;
}

// 分页返回DTO
public class UserPageResponseDTO {
    private List<UserResponseDTO> list;
    private Long total;
}

// 使用
public ListWithPageDTO<UserResponseDTO> queryUserPage(UserPageQueryDTO dto) {
    return MyBatisPlusUtils.page(
        dto, 
        UserEntity.class,
        wrapper -> wrapper.like(UserEntity::getUsername, dto.getUsername())
    );
}
```

### 金额处理

- 所有金额转换统一使用 `AmountUtil`
- 数据库存储：分为单位（Integer）
- 前端展示：元为单位（BigDecimal）
- **严禁**使用float和double进行金额计算

```java
// 前端传入：元（BigDecimal）
BigDecimal amount = new BigDecimal("99.99");

// 转为分存入数据库
Integer fen = AmountUtil.yuanToFen(amount); // 9999

// 从数据库读取：分
Integer fen = 9999;

// 转为元返回给前端
BigDecimal yuan = AmountUtil.fenToYuan(fen); // 99.99
```

### 用户信息获取

- 获取当前登录用户必须使用 `GatewayContextHolder`
- 只能在Controller层获取
- Service层和Manager层可以直接使用

```java
// Controller层获取
@GetMapping("/current")
public Result<UserResponseDTO> getCurrentUser() {
    Long userId = GatewayContextHolder.getUserId();
    String username = GatewayContextHolder.getUsername();
    
    UserResponseDTO user = userService.getUserById(userId);
    return Result.success(user);
}

// Service层直接使用
public UserResponseDTO getUserById(Long userId) {
    // 可以直接调用GatewayContextHolder
    String currentUsername = GatewayContextHolder.getUsername();
    logger.info("当前用户：{} 正在查询用户：{}", currentUsername, userId);
    
    return userManager.getUserById(userId);
}
```

### Redis缓存

- Redis操作统一使用 `RedisUtil` 工具类
- 所有Redis key维护在 `RedisKeyConsts` 中
- 缓存命名规范：`模块名_功能名_标识符`

```java
// Redis Key定义
public class RedisKeyConsts {
    public static final String USER_INFO = "user:info:%s";
    public static final String USER_TOKEN = "user:token:%s";
}

// 使用Redis
public UserEntity getUserById(Long userId) {
    String key = String.format(RedisKeyConsts.USER_INFO, userId);
    
    // 先查缓存
    UserEntity user = redisUtil.get(key, UserEntity.class);
    if (user != null) {
        return user;
    }
    
    // 查数据库
    user = userMapper.selectById(userId);
    
    // 写缓存（7天过期）
    redisUtil.set(key, user, 60 * 60 * 24 * 7);
    
    return user;
}
```

### Hutool工具库

```java
// 字符串操作
StrUtil.isEmpty(str);
StrUtil.isNotBlank(str);

// 集合操作
CollUtil.isEmpty(list);
CollUtil.isNotEmpty(list);

// 时间处理
DateUtil.now();
DateUtil.format(date, "yyyy-MM-dd HH:mm:ss");
DateUtil.parse("2025-01-16", "yyyy-MM-dd");

// UUID生成
String uuid = IdUtil.fastUUID();
```

## 数据处理规范

### DTO规范

**命名规范**：
- 功能明确命名：`AdminUserCreateDTO`、`MallUserLoginDTO`

**字段校验**：
- 使用Bean Validation注解
- `@NotBlank`、`@Size`、`@Email`、`@Pattern`等

**分类存放**：
- 按功能分包存放：`user/`、`shop/`、`goods/`等

**对象转换**：
- **禁止**使用 `BeanUtil.copyProperties()`
- 采用手动字段赋值
- DTO转换方法统一放在各模块convert包中

```java
// DTO定义
public class UserCreateDTO {
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 20, message = "用户名长度为3-20字符")
    private String username;
    
    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度为6-20字符")
    private String password;
    
    @Email(message = "邮箱格式不正确")
    @NotBlank(message = "邮箱不能为空")
    private String email;
}

// Convert类
public class UserConvert {
    
    public static UserResponseDTO toResponseDTO(UserEntity entity) {
        if (entity == null) {
            return null;
        }
        
        UserResponseDTO dto = new UserResponseDTO();
        dto.setId(entity.getId());
        dto.setUsername(entity.getUsername());
        dto.setEmail(entity.getEmail());
        dto.setCreateTime(entity.getCreateTime());
        // 手动赋值所有字段
        return dto;
    }
    
    public static UserEntity toEntity(UserCreateDTO dto) {
        UserEntity entity = new UserEntity();
        entity.setUsername(dto.getUsername());
        entity.setPassword(MD5.create().digestHex(dto.getPassword()));
        entity.setEmail(dto.getEmail());
        entity.setStatus(UserStatusEnum.ACTIVE.getCode());
        // 手动赋值所有字段
        return entity;
    }
}
```

### 枚举和状态管理

- 所有状态字段使用枚举类型
- 避免魔法数字
- 枚举定义在对应模块的enums包中
- 状态变更通过枚举方法进行校验

```java
public enum UserStatusEnum {
    
    ACTIVE(1, "正常"),
    INACTIVE(0, "禁用"),
    DELETED(-1, "已删除");
    
    private final Integer code;
    private final String desc;
    
    UserStatusEnum(Integer code, String desc) {
        this.code = code;
        this.desc = desc;
    }
    
    public Integer getCode() {
        return code;
    }
    
    public String getDesc() {
        return desc;
    }
    
    public static UserStatusEnum fromCode(Integer code) {
        for (UserStatusEnum status : values()) {
            if (status.getCode().equals(code)) {
                return status;
            }
        }
        throw new BusinessException("无效的用户状态");
    }
    
    // 状态转换校验
    public boolean canTransitionTo(UserStatusEnum target) {
        if (this == DELETED) {
            return false; // 已删除不能转换
        }
        return true;
    }
}
```

## 安全规范

### 密码安全

```java
// 密码加密（MD5）
String encryptedPassword = MD5.create().digestHex(rawPassword);

// 密码验证
boolean matches = MD5.create().digestHex(inputPassword)
    .equals(storedPassword);

// 密码重置
String newPassword = generateRandomPassword();
String encryptedNewPassword = MD5.create().digestHex(newPassword);
```

### 数据验证

- 所有外部输入必须验证
- 使用参数化查询防SQL注入
- 对输出内容进行转义防XSS

```java
// Controller参数验证
@PostMapping("/create")
public Result<Void> createUser(@Valid @RequestBody UserCreateDTO dto) {
    // Spring会自动验证@Valid注解的DTO
    userService.createUser(dto);
    return Result.success();
}

// SQL参数化查询（MyBatis-Plus自动支持）
LambdaQueryWrapper<UserEntity> wrapper = new LambdaQueryWrapper<>();
wrapper.eq(UserEntity::getUsername, username); // 自动参数化
```

### 异常处理

**异常分类**：
- `BusinessException`: 业务逻辑异常
- `ServiceException`: 服务层处理异常
- `DataAccessException`: 数据访问异常

**异常处理原则**：
- 所有异常catch必须记录详细日志
- Service层异常由统一异常处理器处理
- **事务异常**：在 `@Transactional` 函数中不要使用 `try...catch` 捕获异常

```java
// 全局异常处理器
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(BusinessException.class)
    public Result<Void> handleBusinessException(BusinessException e) {
        logger.error("业务异常：{}", e.getMessage(), e);
        return Result.fail(e.getCode(), e.getMessage());
    }
    
    @ExceptionHandler(Exception.class)
    public Result<Void> handleException(Exception e) {
        logger.error("系统异常：{}", e.getMessage(), e);
        return Result.fail(500, "系统异常，请联系管理员");
    }
}

// Service层
@Transactional(rollbackFor = Exception.class)
public void updateUser(UserUpdateDTO dto) {
    // 不要使用try...catch捕获异常
    // 让异常抛出，由事务管理器处理
    userManager.updateUser(dto);
}
```

## 性能优化规范

### 数据库操作

**避免循环查询**：
```java
// 错误示例
List<Integer> skuIds = Arrays.asList(1, 2, 3, 4, 5);
for (Integer skuId : skuIds) {
    List<GylSsu> ssuList = gylSsuManager.getSsuListBySkuId(skuId);
    ssuListMap.put(skuId, ssuList);
}

// 正确示例：批量查询
List<GylSsu> ssuList = gylSsuManager.getSsuListBySkuIds(skuIds);
```

**批量操作**：
```java
// 批量插入
void batchInsert(List<UserEntity> users) {
    users.forEach(user -> userMapper.insert(user));
}

// 批量更新
void batchUpdate(List<UserEntity> users) {
    users.forEach(user -> userMapper.updateById(user));
}
```

### 缓存策略

- 避免在事务中进行Redis操作
- 合理设置缓存过期时间
- 及时清理无效缓存

```java
// 缓存更新
@Transactional(rollbackFor = Exception.class)
public void updateUser(UserUpdateDTO dto) {
    // 1. 先更新数据库
    userManager.updateUser(dto);
    
    // 2. 事务提交后再更新缓存
    TransactionSynchronizationManager.registerSynchronization(
        new TransactionSynchronization() {
            @Override
            public void afterCommit() {
                // 更新缓存
                String key = String.format(RedisKeyConsts.USER_INFO, dto.getId());
                redisUtil.del(key);
            }
        }
    );
}
```

### 内存优化

- 及时释放大对象引用
- 避免创建不必要的临时对象

## 严格禁止事项

1. **文件修改**：禁止未经允许修改 `pom.xml` 和实体类文件
2. **对象拷贝**：禁止使用 `BeanUtil.copyProperties()`
3. **循环查询**：禁止在循环中查询数据
4. **包名调用**：不要使用完整包名调用类或方法
5. **数据库变更**：必须生成SQL文档存放在 `doc/sql/` 目录
6. **空方法**：禁止生成空方法或使用测试/默认值
7. **直接SQL**：所有SQL必须写到mapper.xml文件中

## 开发流程

### 标准开发流程

1. **需求分析**：查阅 README 确认是否有相似功能
2. **架构设计**：确定核心逻辑实现层级
3. **Mapper层**：定义数据访问接口
4. **Service层**：实现具体业务流程
5. **Controller层**：提供HTTP接口

### 代码复用原则

- 开发前必查 README 中的service说明
- 发现重复代码时，及时重构到合适层级

### 代码质量要求

- 每个方法添加Javadoc注释
- 方法行数不超过300行
- 使用描述性的变量、函数和类名
- 保持代码简洁明了，遵循KISS原则

## 最佳实践总结

### 关注点分离
- Gateway层专注请求处理
- Service层专注业务逻辑
- Mapper层专注数据访问

### 可维护性
- 使用枚举管理状态
- 使用DTO传输数据
- 手动字段赋值提高可读性
- 完善的异常处理和日志记录

### 性能优化
- 批量操作代替逐个操作
- 合理使用缓存
- 避免N+1查询问题
