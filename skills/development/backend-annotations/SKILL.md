---
name: backend-annotations
description: |
  基于若依-vue-plus框架的后端Java注解标准使用规范。涵盖实体映射（Lombok、MyBatis-Plus）、接口安全（Sa-Token权限）、
  日志审计（操作日志）、数据校验（JSR-303）、数据导入导出（Excel注解）、防重复提交、接口限流等全方位注解使用标准。
  触发场景：
  - 编写Entity实体类并映射数据库表结构
  - 开发Controller RESTful接口并配置安全权限
  - 实现Service业务逻辑并管理事务
  - 配置数据导入导出功能（Excel/Word/PDF）
  - 添加接口防护机制（防重、限流、脱敏）
  - 进行参数校验和异常处理
  触发词：注解规范、实体注解、权限注解、日志注解、参数校验、数据导出、事务管理、接口防护
---

# 后端注解使用规范

## 核心规范

### 规范1：实体类与数据库映射注解
**适用场景**：定义Domain实体类、BO业务对象、VO视图对象时

**核心要求**：
1. **Lombok注解**：使用`@Data`（包含getter/setter）、`@EqualsAndHashCode`（equals和hashCode方法）简化POJO代码
2. **MyBatis-Plus注解**：
   - `@TableName("表名")`：指定数据库表名（支持动态表名）
   - `@TableId(type = IdType.AUTO)`：标识主键及生成策略（AUTO自增、ASSIGN_ID雪花算法）
   - `@TableField(exist = false)`：标记非数据库字段（如关联查询的扩展属性）
   - `@TableLogic`：逻辑删除字段标记（如`del_flag`）
3. **导出注解**：需要Excel导出的字段必须使用`@Excel(name = "列名")`，支持字典转换`readConverterExp`
4. **继承基类**：实体类应继承`BaseEntity`获得公共字段（createTime、updateTime、createBy等）

**字段命名规范**：
- 数据库字段使用下划线命名（user_name）
- Java属性使用驼峰命名（userName）
- MyBatis-Plus自动完成映射转换

```java
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("sys_user")
public class SysUser extends BaseEntity {
    
    /** 主键ID - 自增策略 */
    @TableId(type = IdType.AUTO)
    private Long userId;

    /** 用户账号 - 支持Excel导出 */
    @Excel(name = "用户账号")
    private String userName;

    /** 用户性别 - 字典转换导出 */
    @Excel(name = "用户性别", readConverterExp = "0=男,1=女,2=未知")
    private String sex;

    /** 用户状态 - 字典类型 */
    @Excel(name = "用户状态", dictType = "sys_normal_disable")
    private String status;

    /** 部门名称 - 非数据库字段，用于关联查询展示 */
    @TableField(exist = false)
    private String deptName;

    /** 角色列表 - 非数据库字段，用于业务处理 */
    @TableField(exist = false)
    private List<SysRole> roles;

    /** 逻辑删除字段 */
    @TableLogic
    private String delFlag;
}
```

### 规范2：Controller层安全与操作日志注解
**适用场景**：开发RESTful API接口，特别是涉及增删改查、数据导出、敏感操作的接口

**核心要求**：
1. **权限校验注解**（必须）：
   - `@SaCheckPermission("权限标识")`：基于Sa-Token的权限验证
   - 权限标识格式：`模块:功能:操作`（如`system:user:add`）
   - 公开接口（登录、注册、验证码）除外

2. **操作日志注解**（增删改必须）：
   - `@Log(title = "模块名称", businessType = BusinessType.XXX)`
   - 业务类型：INSERT新增、UPDATE修改、DELETE删除、EXPORT导出、IMPORT导入、GRANT授权、CLEAN清空

3. **接口防护注解**（重要接口建议）：
   - `@RepeatSubmit(interval = 5000, message = "请勿重复提交")`：防止表单重复提交（默认5秒内）
   - `@RateLimiter(count = 10, time = 60)`：接口限流（60秒内最多10次请求）
   
4. **参数校验注解**（必须）：
   - 方法参数使用`@Validated`或`@Valid`激活校验
   - BO/DTO类中使用JSR-303注解（@NotNull、@NotBlank、@Size等）

5. **数据权限注解**（可选）：
   - `@DataScope(deptAlias = "d", userAlias = "u")`：自动过滤数据权限范围

**注解顺序规范**：
```
@SaCheckPermission        // 权限校验
@Log                      // 操作日志
@RepeatSubmit             // 防重复提交
@RateLimiter             // 接口限流
@PostMapping/GetMapping  // 请求映射
public R<Void> method(@Validated @RequestBody Bo bo) { ... }
```

```java
@RestController
@RequestMapping("/system/user")
public class SysUserController extends BaseController {

    /**
     * 新增用户
     * 完整注解配置示例：权限+日志+防重+校验
     */
    @SaCheckPermission("system:user:add")
    @Log(title = "用户管理", businessType = BusinessType.INSERT)
    @RepeatSubmit()
    @PostMapping
    public R<Void> add(@Validated @RequestBody SysUserBo user) {
        // 数据权限校验
        deptService.checkDeptDataScope(user.getDeptId());
        
        // 业务唯一性校验
        if (!userService.checkUserNameUnique(user)) {
            return R.fail("新增用户'" + user.getUserName() + "'失败，登录账号已存在");
        } else if (StringUtils.isNotEmpty(user.getPhonenumber()) && !userService.checkPhoneUnique(user)) {
            return R.fail("新增用户'" + user.getUserName() + "'失败，手机号码已存在");
        } else if (StringUtils.isNotEmpty(user.getEmail()) && !userService.checkEmailUnique(user)) {
            return R.fail("新增用户'" + user.getUserName() + "'失败，邮箱账号已存在");
        }
        
        // 多租户场景校验
        if (TenantHelper.isEnable()) {
            if (!tenantService.checkAccountBalance(TenantHelper.getTenantId())) {
                return R.fail("当前租户下用户名额不足，请联系管理员");
            }
        }
        
        // 密码加密处理
        user.setPassword(BCrypt.hashpw(user.getPassword()));
        return toAjax(userService.insertUser(user));
    }

    /**
     * 导出用户数据
     * 导出操作必须记录日志并校验权限
     */
    @Log(title = "用户管理", businessType = BusinessType.EXPORT)
    @SaCheckPermission("system:user:export")
    @PostMapping("/export")
    public void export(SysUserBo user, HttpServletResponse response) {
        List<SysUserExportVo> list = userService.selectUserExportList(user);
        ExcelUtil.exportExcel(list, "用户数据", SysUserExportVo.class, response);
    }

    /**
     * 查询用户列表（带数据权限过滤）
     */
    @SaCheckPermission("system:user:list")
    @GetMapping("/list")
    @DataScope(deptAlias = "d", userAlias = "u")
    public TableDataInfo<SysUserVo> list(SysUserBo user) {
        return userService.selectPageUserList(user);
    }

    /**
     * 删除用户（支持批量删除）
     */
    @SaCheckPermission("system:user:remove")
    @Log(title = "用户管理", businessType = BusinessType.DELETE)
    @DeleteMapping("/{userIds}")
    public R<Void> remove(@PathVariable Long[] userIds) {
        if (ArrayUtil.contains(userIds, getUserId())) {
            return R.fail("当前用户不能删除");
        }
        return toAjax(userService.deleteUserByIds(userIds));
    }

    /**
     * 重置密码
     * 敏感操作需要防重复提交
     */
    @SaCheckPermission("system:user:resetPwd")
    @Log(title = "用户管理", businessType = BusinessType.UPDATE)
    @RepeatSubmit()
    @PutMapping("/resetPwd")
    public R<Void> resetPwd(@Validated @RequestBody SysUserBo user) {
        userService.checkUserAllowed(user.getUserId());
        user.setPassword(BCrypt.hashpw(user.getPassword()));
        return toAjax(userService.resetUserPwd(user.getUserId(), user.getPassword()));
    }

    /**
     * 获取验证码（公开接口，无需权限校验）
     * 但需要限流防止接口滥用
     */
    @RateLimiter(count = 5, time = 60)
    @GetMapping("/captchaImage")
    public R<CaptchaVo> getCaptchaImage() {
        return R.ok(captchaService.createCaptcha());
    }
}
```

### 规范3：Service层事务管理注解
**适用场景**：涉及多表操作、数据一致性要求高的业务逻辑

**核心要求**：
1. **事务注解位置**：必须在Service实现类的public方法上使用`@Transactional`
2. **事务传播行为**：
   - `REQUIRED`（默认）：有事务加入，无事务新建
   - `REQUIRES_NEW`：始终开启新事务（用于独立日志记录）
   - `NESTED`：嵌套事务（用于部分回滚场景）
3. **异常回滚策略**：默认RuntimeException回滚，checked异常需手动指定`rollbackFor = Exception.class`
4. **只读优化**：查询方法使用`@Transactional(readOnly = true)`提升性能

```java
@Service
public class SysUserServiceImpl implements ISysUserService {

    /** 新增用户 - 涉及用户表+用户角色关联表，需要事务 */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public int insertUser(SysUserBo user) {
        // 插入用户基本信息
        SysUser sysUser = MapstructUtils.convert(user, SysUser.class);
        int rows = baseMapper.insert(sysUser);
        user.setUserId(sysUser.getUserId());
        // 新增用户与角色关联
        insertUserRole(user);
        // 新增用户与岗位关联
        insertUserPost(user);
        return rows;
    }

    /** 查询方法 - 使用只读事务优化 */
    @Override
    @Transactional(readOnly = true)
    public SysUserVo selectUserById(Long userId) {
        return baseMapper.selectVoById(userId);
    }

    /** 删除用户 - 级联删除多表数据 */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public int deleteUserByIds(Long[] userIds) {
        for (Long userId : userIds) {
            checkUserAllowed(userId);
            checkUserDataScope(userId);
        }
        // 删除用户与角色关联
        userRoleMapper.delete(new LambdaQueryWrapper<SysUserRole>()
            .in(SysUserRole::getUserId, Arrays.asList(userIds)));
        // 删除用户与岗位关联
        userPostMapper.delete(new LambdaQueryWrapper<SysUserPost>()
            .in(SysUserPost::getUserId, Arrays.asList(userIds)));
        // 删除用户
        return baseMapper.deleteBatchIds(Arrays.asList(userIds));
    }
}
```

### 规范4：参数校验注解（JSR-303）
**适用场景**：BO业务对象、DTO数据传输对象的字段校验

**常用校验注解**：
- `@NotNull`：不能为null（可以为空字符串）
- `@NotBlank`：不能为null且trim后长度>0（字符串专用）
- `@NotEmpty`：不能为null且size>0（集合/数组/字符串）
- `@Size(min=2, max=30)`：字符串/集合长度范围
- `@Pattern(regexp="正则")`：正则表达式校验
- `@Email`：邮箱格式校验
- `@Min`/`@Max`：数值范围校验

**分组校验**：使用`@Validated`的groups属性实现新增/编辑不同校验规则

```java
public class SysUserBo extends BaseEntity {

    /** 用户ID - 编辑时必填，新增时不填 */
    @NotNull(message = "用户ID不能为空", groups = { EditGroup.class })
    private Long userId;

    /** 用户账号 - 新增和编辑都必填 */
    @NotBlank(message = "用户账号不能为空", groups = { AddGroup.class, EditGroup.class })
    @Size(min = 0, max = 30, message = "用户账号长度不能超过{max}个字符")
    private String userName;

    /** 用户昵称 */
    @NotBlank(message = "用户昵称不能为空")
    @Size(min = 0, max = 30, message = "用户昵称长度不能超过{max}个字符")
    private String nickName;

    /** 用户邮箱 */
    @Email(message = "邮箱格式不正确")
    @Size(min = 0, max = 50, message = "邮箱长度不能超过{max}个字符")
    private String email;

    /** 手机号码 */
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phonenumber;

    /** 用户密码 - 新增时必填 */
    @NotBlank(message = "用户密码不能为空", groups = { AddGroup.class })
    @Size(min = 5, max = 20, message = "用户密码长度必须在{min}到{max}个字符之间")
    private String password;

    /** 角色ID数组 - 至少选择一个角色 */
    @NotEmpty(message = "用户角色不能为空")
    private Long[] roleIds;
}

// Controller中使用分组校验
@PostMapping
public R<Void> add(@Validated(AddGroup.class) @RequestBody SysUserBo user) { ... }

@PutMapping
public R<Void> edit(@Validated(EditGroup.class) @RequestBody SysUserBo user) { ... }
```

### 规范5：数据脱敏注解
**适用场景**：敏感数据（手机号、身份证、邮箱等）在日志、接口返回时需要脱敏

```java
public class SysUserVo {

    /** 手机号脱敏 - 显示为 138****5678 */
    @Sensitive(strategy = SensitiveStrategy.PHONE)
    private String phonenumber;

    /** 身份证脱敏 - 显示前6后4位 */
    @Sensitive(strategy = SensitiveStrategy.ID_CARD)
    private String idCard;

    /** 邮箱脱敏 - 用户名部分脱敏 */
    @Sensitive(strategy = SensitiveStrategy.EMAIL)
    private String email;

    /** 银行卡脱敏 - 显示前4后4位 */
    @Sensitive(strategy = SensitiveStrategy.BANK_CARD)
    private String bankCard;
}
```

## 禁止事项

### 严重错误（会导致系统故障）
- ❌ **禁止在Mapper层使用`@Transactional`**：事务管理必须在Service层，Mapper层仅负责数据访问
- ❌ **禁止遗漏`@Validated`/@Valid触发校验**：仅在BO中定义校验注解不会生效，必须在Controller参数上激活
- ❌ **禁止对外暴露接口缺少`@SaCheckPermission`**：除公开接口（登录/注册/验证码）外，所有接口必须权限校验
- ❌ **禁止事务方法为非public**：`@Transactional`仅对public方法生效，protected/private方法无效
- ❌ **禁止在同类中直接调用事务方法**：会导致事务失效，需通过注入的Service调用

### 性能与安全问题
- ❌ **禁止查询接口使用写事务**：查询方法应使用`@Transactional(readOnly = true)`优化性能
- ❌ **禁止在Controller中处理事务**：违反分层架构原则，事务逻辑必须在Service层
- ❌ **禁止敏感操作缺少`@RepeatSubmit`**：新增/修改/删除/支付等操作必须防重复提交
- ❌ **禁止公开接口缺少`@RateLimiter`**：验证码、登录、注册等接口必须限流防止暴力破解

### 数据一致性问题
- ❌ **禁止实体类字段名与`@Excel(name="")`不一致**：会导致Excel导出列名错误或数据丢失
- ❌ **禁止非数据库字段缺少`@TableField(exist = false)`**：会导致MyBatis-Plus插入/更新时报错字段不存在
- ❌ **禁止主键字段缺少`@TableId`注解**：会导致主键生成策略失效，可能产生重复主键
- ❌ **禁止逻辑删除字段缺少`@TableLogic`**：会导致逻辑删除功能失效，误删数据无法恢复

### 代码规范问题
- ❌ **禁止使用`@Autowired`字段注入**：推荐使用构造器注入或`@Resource`，避免循环依赖
- ❌ **禁止实体类缺少Lombok注解**：必须使用`@Data`简化getter/setter，使用`@EqualsAndHashCode(callSuper = true)`处理继承
- ❌ **禁止在BO中使用`required = true`**：应使用`@NotNull`/@NotBlank等校验注解，语义更清晰
- ❌ **禁止增删改操作缺少`@Log`注解**：违反审计要求，关键操作必须记录日志

### 多租户场景特殊禁止
- ❌ **禁止多租户表缺少`@TenantIgnore`标记**：全局配置表（字典/参数）必须忽略租户隔离
- ❌ **禁止租户隔离字段手动赋值**：`tenant_id`由框架自动注入，手动设置可能破坏数据隔离

## 参考代码

### 实体类示例
- **用户实体**：`ruoyi-system/src/main/java/com/ruoyi/system/domain/SysUser.java`
- **角色实体**：`ruoyi-system/src/main/java/com/ruoyi/system/domain/SysRole.java`
- **字典实体**：`ruoyi-system/src/main/java/com/ruoyi/system/domain/SysDictData.java`

### Controller层示例
- **用户控制器**：`ruoyi-admin/src/main/java/com/ruoyi/web/controller/system/SysUserController.java`
- **角色控制器**：`ruoyi-admin/src/main/java/com/ruoyi/web/controller/system/SysRoleController.java`
- **部门控制器**：`ruoyi-admin/src/main/java/com/ruoyi/web/controller/system/SysDeptController.java`

### Service层示例
- **用户服务**：`ruoyi-system/src/main/java/com/ruoyi/system/service/impl/SysUserServiceImpl.java`
- **角色服务**：`ruoyi-system/src/main/java/com/ruoyi/system/service/impl/SysRoleServiceImpl.java`

### 注解定义
- **Excel注解**：`ruoyi-common/ruoyi-common-excel/src/main/java/com/ruoyi/common/excel/annotation/Excel.java`
- **Log注解**：`ruoyi-common/ruoyi-common-log/src/main/java/com/ruoyi/common/log/annotation/Log.java`
- **RepeatSubmit注解**：`ruoyi-common/ruoyi-common-web/src/main/java/com/ruoyi/common/web/annotation/RepeatSubmit.java`
- **RateLimiter注解**：`ruoyi-common/ruoyi-common-redis/src/main/java/com/ruoyi/common/redis/annotation/RateLimiter.java`

## 检查清单

### 实体类检查（Entity/Domain）
- [ ] 是否使用`@Data`和`@EqualsAndHashCode(callSuper = true)`简化代码
- [ ] 是否使用`@TableName`指定数据库表名
- [ ] 主键字段是否使用`@TableId(type = IdType.AUTO)`或其他策略
- [ ] 非数据库字段是否标记`@TableField(exist = false)`
- [ ] 需要导出的字段是否配置`@Excel(name = "列名")`
- [ ] 字典字段是否配置`dictType`或`readConverterExp`进行转换
- [ ] 逻辑删除字段是否标记`@TableLogic`
- [ ] 是否继承`BaseEntity`获取公共字段

### Controller层检查
- [ ] 增删改查接口是否配置`@SaCheckPermission`权限校验
- [ ] 增删改操作是否配置`@Log`记录操作日志
- [ ] 新增/修改/删除/支付等敏感操作是否使用`@RepeatSubmit`防重
- [ ] 公开接口（验证码/登录/注册）是否配置`@RateLimiter`限流
- [ ] 接口参数是否使用`@Validated`/@Valid激活校验
- [ ] 导出接口是否记录`BusinessType.EXPORT`日志
- [ ] 数据权限控制是否使用`@DataScope`注解
- [ ] 返回值是否使用统一`R<T>`包装

### Service层检查
- [ ] 涉及多表操作的方法是否使用`@Transactional(rollbackFor = Exception.class)`
- [ ] 查询方法是否使用`@Transactional(readOnly = true)`优化性能
- [ ] 事务方法是否为public访问权限
- [ ] 是否避免在同类中直接调用事务方法（导致事务失效）
- [ ] 是否正确处理异常回滚策略（checked异常需手动指定）

### BO/DTO校验检查
- [ ] 必填字段是否使用`@NotNull`/`@NotBlank`/`@NotEmpty`
- [ ] 字符串长度是否使用`@Size(min, max)`限制
- [ ] 邮箱字段是否使用`@Email`校验
- [ ] 手机号是否使用`@Pattern`正则校验
- [ ] 是否根据新增/编辑场景使用分组校验（AddGroup/EditGroup）
- [ ] 校验注解是否配置清晰的`message`提示信息

### 数据安全检查
- [ ] 敏感字段（手机/身份证/邮箱）是否使用`@Sensitive`脱敏
- [ ] 密码字段是否使用BCrypt加密存储
- [ ] 接口是否进行数据权限范围校验（部门/用户范围）
- [ ] 是否校验业务唯一性约束（用户名/手机号/邮箱重复）

### 多租户场景检查（如启用）
- [ ] 全局配置表是否标记`@TenantIgnore`忽略租户隔离
- [ ] 是否避免手动设置`tenant_id`字段（由框架自动注入）
- [ ] 跨租户查询是否正确处理租户上下文

### 性能优化检查
- [ ] 是否合理使用只读事务`readOnly = true`
- [ ] 接口是否配置合理的限流阈值`@RateLimiter(count, time)`
- [ ] 是否避免在事务中执行耗时操作（远程调用/文件IO）
- [ ] 批量操作是否使用`deleteBatchIds`/`updateBatchById`提升效率

## 快速决策树

```
开始开发
  ├─ 定义实体类？
  │   ├─ 添加 @Data + @TableName + @TableId
  │   ├─ 需要导出？添加 @Excel
  │   ├─ 有非DB字段？添加 @TableField(exist = false)
  │   └─ 逻辑删除？添加 @TableLogic
  │
  ├─ 开发Controller接口？
  │   ├─ 公开接口（登录/验证码）？仅添加 @RateLimiter
  │   ├─ 查询接口？添加 @SaCheckPermission
  │   ├─ 增删改接口？添加 @SaCheckPermission + @Log + @RepeatSubmit
  │   ├─ 导出接口？添加 @SaCheckPermission + @Log(EXPORT)
  │   └─ 参数校验？添加 @Validated + BO中定义校验规则
  │
  ├─ 编写Service业务逻辑？
  │   ├─ 纯查询？添加 @Transactional(readOnly = true)
  │   ├─ 涉及多表操作？添加 @Transactional(rollbackFor = Exception.class)
  │   └─ 单表简单操作？可不加事务注解
  │
  └─ 定义BO/DTO？
      ├─ 必填字段？添加 @NotNull / @NotBlank / @NotEmpty
      ├─ 字符串长度限制？添加 @Size(min, max)
      ├─ 邮箱/手机号？添加 @Email / @Pattern
      └─ 新增/编辑规则不同？使用分组校验 AddGroup/EditGroup
```

## 常见问题FAQ

### Q1：为什么事务不生效？
**可能原因**：
1. 方法不是public（Spring AOP仅代理public方法）
2. 在同类中直接调用事务方法（未走代理）
3. 异常被捕获未抛出（事务默认仅回滚RuntimeException）
4. 数据库引擎不支持事务（如MyISAM）

**解决方案**：
- 确保方法为public
- 通过注入的Service调用事务方法
- 使用`rollbackFor = Exception.class`覆盖所有异常
- 检查数据库引擎是否为InnoDB

### Q2：参数校验为什么不生效？
**可能原因**：
1. Controller参数未添加`@Validated`或`@Valid`
2. BO类中校验注解配置错误
3. 分组校验未指定groups

**解决方案**：
```java
// 错误写法
public R<Void> add(@RequestBody SysUserBo user) { ... }

// 正确写法
public R<Void> add(@Validated @RequestBody SysUserBo user) { ... }
```

### Q3：Excel导出字段为空或错误？
**可能原因**：
1. VO类字段缺少`@Excel`注解
2. `@Excel(name="")`名称与字段名不匹配
3. 字典字段未配置`dictType`或`readConverterExp`

**解决方案**：
```java
// 正确配置
@Excel(name = "用户性别", dictType = "sys_user_sex")
private String sex;

// 或使用readConverterExp
@Excel(name = "用户性别", readConverterExp = "0=男,1=女,2=未知")
private String sex;
```

### Q4：权限校验失败但代码看起来正确？
**可能原因**：
1. 权限标识拼写错误（如system:user:add写成system:user:insert）
2. 用户角色未分配对应权限
3. Redis中权限缓存未更新

**解决方案**：
- 检查菜单管理中的权限标识是否与代码一致
- 确认角色已分配该权限
- 清除Redis缓存或重新登录刷新权限

### Q5：多租户场景下数据错乱？
**可能原因**：
1. 全局配置表未标记`@TenantIgnore`
2. 手动设置了`tenant_id`覆盖框架注入
3. 租户上下文在异步线程中丢失

**解决方案**：
```java
// 全局配置表忽略租户
@TableName(value = "sys_dict_data", excludeProperty = "tenantId")
public class SysDictData extends BaseEntity { ... }

// 异步任务传递租户上下文
String tenantId = TenantHelper.getTenantId();
CompletableFuture.runAsync(() -> {
    TenantHelper.setTenantId(tenantId);
    // 业务逻辑
});
```

## 最佳实践建议

### 1. 注解顺序约定
遵循统一的注解顺序提升代码可读性：
```java
// Controller方法注解顺序
@SaCheckPermission("权限标识")      // 1. 权限校验
@Log(title = "模块", businessType)  // 2. 操作日志
@RepeatSubmit()                     // 3. 防重复提交
@RateLimiter(count, time)          // 4. 接口限流
@PostMapping("/path")               // 5. 请求映射
public R<Vo> method(@Validated @RequestBody Bo bo) { ... }
```

### 2. 日志记录规范
- 新增操作：`BusinessType.INSERT`
- 修改操作：`BusinessType.UPDATE`
- 删除操作：`BusinessType.DELETE`
- 导出操作：`BusinessType.EXPORT`
- 导入操作：`BusinessType.IMPORT`
- 授权操作：`BusinessType.GRANT`
- 强退操作：`BusinessType.FORCE`
- 清空操作：`BusinessType.CLEAN`

### 3. 权限标识命名规范
格式：`模块:功能:操作`
```
system:user:list    // 用户列表查询
system:user:add     // 新增用户
system:user:edit    // 编辑用户
system:user:remove  // 删除用户
system:user:export  // 导出用户
system:user:import  // 导入用户
system:user:resetPwd // 重置密码
```

### 4. 分层职责清晰
- **Controller层**：参数校验、权限校验、日志记录、返回值包装
- **Service层**：业务逻辑、事务管理、数据权限过滤
- **Mapper层**：数据访问、SQL映射，不处理业务逻辑

### 5. 异常处理统一
```java
// Service层抛出业务异常
throw new ServiceException("用户名已存在");

// 全局异常处理器自动捕获并返回统一格式
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ServiceException.class)
    public R<Void> handleServiceException(ServiceException e) {
        return R.fail(e.getMessage());
    }
}
```