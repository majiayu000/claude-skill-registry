---
name: crud-development
description: 定义若依（RuoYi / RuoYi-Vue-Plus 生态）在数据持久层（Mapper）与业务层（Service）的 CRUD 开发规范。要求 Mapper 统一继承 `BaseMapperPlus<Entity,Vo>`、Service 统一实现 `IService<Entity>` 并采用标准实现基类；查询/更新条件强制使用 `LambdaQueryWrapper` / `LambdaUpdateWrapper` 构建类型安全条件；分页统一使用 `PageQuery` + `TableDataInfo<T>` 返回。严禁循环执行 SQL、严禁直接返回 Entity 给前端、严禁 `SELECT *`，写操作强制采用批量 API 与 VO/DTO 封装，提升代码一致性、可维护性与性能。
---

# CRUD 开发技能

## 触发条件
- **关键词**：CRUD、MyBatis-Plus、Mapper、Service、分页、事务、LambdaQueryWrapper、BaseMapperPlus、IService、若依
- **触发场景**：
  - 用户请求创建、修改、删除或查询数据接口
  - 实现列表查询、分页展示、数据导出功能
  - 进行批量数据处理、多表关联查询
  - 需要实现带权限控制或数据范围过滤的查询
  - 编写若依（RuoYi / RuoYi-Vue-Plus）框架的持久层或业务层代码
- **不适用场景**：
  - 非若依框架项目（可能缺少 BaseMapperPlus、PageQuery 等基础设施）
  - 纯展示型接口无需数据库操作
  - 简单的静态配置读取

## 核心规范
### 规范1：继承标准基类
所有 Mapper 接口**必须**继承 `BaseMapperPlus<Entity,Vo>`，所有 Service 实现类**禁止**使用标准实现基类（如 `ServiceImpl<Mapper, Entity>` 或框架提供的其他基类），必须实现IService。

- **目标**：统一代码结构、减少样板代码、避免"Mapper/Service 风格不一致"导致的维护成本。
- **强制约束**：
  - Mapper **仅负责**"数据访问层"职责（SQL查询、数据映射），**严禁**在 Mapper 中编写业务逻辑、事务编排或复杂计算。
  - Service **负责**业务编排、事务管理、权限校验、数据校验、VO/DTO 转换。
  - Controller **严禁**直接调用 Mapper，**必须**通过 Service 暴露的方法访问数据层。
  - 对外返回对象**必须**使用 VO/DTO（而不是 Entity），**严禁**将数据库实体类直接暴露给前端或外部调用方。
- **泛型参数说明**：
  - `BaseMapperPlus<Entity, Vo>`：第一个泛型为数据库实体类，第二个泛型为返回给调用方的视图对象。
  - `IService<Entity>`：泛型为数据库实体类。
```java
// Mapper：Entity + VO（返回给前端/调用方的对象）
public interface SysUserMapper extends BaseMapperPlus<SysUser, SysUserVo> {
    // 复杂/多表查询建议在 Mapper 增补自定义方法，返回 Vo/DTO
    // Page<SysUserVo> selectPageUserList(@Param("page") Page<?> page, @Param("ew") Wrapper<SysUser> wrapper);
}

// Service 接口：继承 IService<Entity>
public interface ISysUserService{
    // 业务方法定义
    TableDataInfo<SysUserVo> selectPageUserList(SysUserBo user, PageQuery pageQuery);
}

// Service 实现类：继承 ServiceImpl 并实现接口
@Service
public class SysUserServiceImpl implements ISysUserService {
    // baseMapper 由 ServiceImpl 自动注入，类型为 SysUserMapper
    @Override
    public TableDataInfo<SysUserVo> selectPageUserList(SysUserBo user, PageQuery pageQuery) {
        Page<SysUserVo> page = baseMapper.selectPageUserList(pageQuery.build(), this.buildQueryWrapper(user));
        return TableDataInfo.build(page);
    }
}
```

### 规范2：使用 Lambda 构造查询条件
**必须**使用 `LambdaQueryWrapper` 或 `LambdaUpdateWrapper` 来构建查询/更新条件，**严禁**使用 `QueryWrapper` 或 `UpdateWrapper` 通过字符串硬编码字段名（如 `"user_id"`），避免重构困难、列名拼接错误以及潜在的 SQL 注入风险。

- **推荐写法**：
  - 条件拼装集中封装到独立的 `buildQueryWrapper(Bo/Dto)` 方法，便于复用、测试与维护。
  - 所有可选条件都使用带 `condition` 参数的重载（如 `eq(condition, field, value)`），避免空值条件污染 SQL。
  - 排序优先使用 `orderByAsc/Desc(Entity::getXxx)`；若排序字段来自前端，**必须**进行白名单校验后再使用（防止 order by 注入）。
- **安全注意事项**：
  - `like` 默认会产生全表扫描风险，能使用 `eq` 就**不要**使用 `like`；必要时建立索引并限制查询范围。
  - `and/or` 组合条件使用 `and(w -> ...)` / `or(w -> ...)` / `nested(w -> ...)`，避免括号错误导致条件失效。
  - 更新场景优先使用 `LambdaUpdateWrapper` 做"按条件更新"，但**必须**确保 where 条件完备，**严禁**无条件更新（如 wrapper 无任何 where 条件、或条件恒为 true）。
  - 所有动态条件**必须**验证非空/非null后再添加，避免错误的全表操作。
```java
    /**
     * 构建查询条件（集中管理，便于测试和维护）
     */
    private Wrapper<SysUser> buildQueryWrapper(SysUserBo user) {
        Map<String, Object> params = user.getParams();
        LambdaQueryWrapper<SysUser> wrapper = Wrappers.lambdaQuery();
        wrapper.eq(SysUser::getDelFlag, SystemConstants.NORMAL)
            .eq(ObjectUtil.isNotNull(user.getUserId()), SysUser::getUserId, user.getUserId())
            .in(StringUtils.isNotBlank(user.getUserIds()), SysUser::getUserId, StringUtils.splitTo(user.getUserIds(), Convert::toLong))
            .like(StringUtils.isNotBlank(user.getUserName()), SysUser::getUserName, user.getUserName())
            .like(StringUtils.isNotBlank(user.getNickName()), SysUser::getNickName, user.getNickName())
            .eq(StringUtils.isNotBlank(user.getStatus()), SysUser::getStatus, user.getStatus())
            .like(StringUtils.isNotBlank(user.getPhonenumber()), SysUser::getPhonenumber, user.getPhonenumber())
            .between(params.get("beginTime") != null && params.get("endTime") != null,
                SysUser::getCreateTime, params.get("beginTime"), params.get("endTime"))
            .and(ObjectUtil.isNotNull(user.getDeptId()), w -> {
                // 嵌套查询：部门及其子部门
                List<Long> ids = deptMapper.selectDeptAndChildById(user.getDeptId());
                w.in(SysUser::getDeptId, ids);
            })
            .orderByAsc(SysUser::getUserId);
        // 排除用户ID列表
        if (StringUtils.isNotBlank(user.getExcludeUserIds())) {
            wrapper.notIn(SysUser::getUserId, StringUtils.splitTo(user.getExcludeUserIds(), Convert::toLong));
        }
        return wrapper;
    }
```

### 规范3：分页查询标准写法
分页查询**必须**使用 `PageQuery` 统一构建 `Page<?>`，并**必须**使用 `TableDataInfo<T>` 作为 Controller 返回对象，保证前端列表组件协议一致、避免各模块分页字段不统一。

- **目标**：标准化分页入参/出参，减少重复代码，确保分页字段（total/rows/page/pageSize 等）一致。
- **职责划分**：
  - Controller **仅负责**权限校验与参数透传，**不做**任何分页拼装逻辑。
  - Service **负责**：`PageQuery.build()` + 构建 wrapper + Mapper 查询 + `TableDataInfo.build(page)` 封装结果。
  - Mapper **负责**：执行分页查询，返回 `Page<Vo>` 对象。
- **建议**：
  - 多表/自定义分页查询优先返回 VO（`Page<Vo>`），**严禁** Entity 直接外泄。
  - 分页参数（pageNum、pageSize）的校验和默认值设置在 `PageQuery` 中统一处理，Service/Controller 不重复校验。
```java
// Controller 层
    @SaCheckPermission("system:user:list")
    @GetMapping("/list")
    public TableDataInfo<SysUserVo> list(SysUserBo user, PageQuery pageQuery) {
        return userService.selectPageUserList(user, pageQuery);
    }

// Service 层实现
    @Override
    public TableDataInfo<SysUserVo> selectPageUserList(SysUserBo user, PageQuery pageQuery) {
        // 1. 构建分页对象
        Page<SysUserVo> page = pageQuery.build();
        // 2. 构建查询条件
        Wrapper<SysUser> wrapper = this.buildQueryWrapper(user);
        // 3. 执行分页查询
        page = baseMapper.selectPageUserList(page, wrapper);
        // 4. 封装返回结果
        return TableDataInfo.build(page);
    }
```

### 规范4：事务管理规范
所有涉及多步骤写操作（多次 insert/update/delete）的业务方法**必须**在 Service 层添加 `@Transactional` 注解，确保数据一致性。

- **强制要求**：
  - 事务注解**必须**添加 `rollbackFor = Exception.class`，确保所有异常都回滚（默认只回滚 RuntimeException）。
  - **严禁**在 Controller 层添加 `@Transactional`，事务边界**必须**在 Service 层。
  - 对于只读操作（纯查询），使用 `@Transactional(readOnly = true)` 可提升性能（可选）。
- **注意事项**：
  - 避免在事务方法中调用外部 HTTP 接口、发送 MQ 消息等耗时操作，防止长事务锁表。
  - 事务方法内**严禁**捕获异常后不抛出，否则事务不会回滚。
  - 批量操作失败时，整个事务会回滚，需在业务层面考虑是否需要部分成功的场景（如需要，应拆分事务或使用补偿机制）。
```java
    @Override
    @Transactional(rollbackFor = Exception.class)
    public boolean insertUser(SysUserBo user) {
        SysUser entity = BeanUtil.toBean(user, SysUser.class);
        // 1. 插入用户
        boolean result = this.save(entity);
        // 2. 插入用户角色关联
        if (result && CollUtil.isNotEmpty(user.getRoleIds())) {
            insertUserRole(entity.getUserId(), user.getRoleIds());
        }
        // 3. 插入用户岗位关联
        if (result && CollUtil.isNotEmpty(user.getPostIds())) {
            insertUserPost(entity.getUserId(), user.getPostIds());
        }
        return result;
    }
```

### 规范5：批量操作优化
涉及多条记录的插入、更新或删除操作**必须**使用批量 API，**严禁**在循环中执行单条 SQL。

- **批量插入**：使用 `saveBatch(List<Entity>)` 或 `saveBatch(List<Entity>, batchSize)`。
- **批量更新**：使用 `updateBatchById(List<Entity>)` 或 `updateBatchById(List<Entity>, batchSize)`。
- **批量删除**：使用 `removeBatchByIds(Collection<?>)` 或 `remove(Wrapper<Entity>)`。
- **性能建议**：
  - 默认批量大小为 1000，大数据量操作建议手动指定 batchSize（如 500-1000）。
  - 批量操作前**必须**校验列表非空（`CollUtil.isNotEmpty(list)`），避免空列表导致的 SQL 异常。
  - 对于超大数据量（10万+），建议分批处理并考虑异步执行。
```java
    // ❌ 错误示例：循环执行单条 SQL
    for (SysUser user : userList) {
        userMapper.insert(user);
    }

    // ✅ 正确示例：批量插入
    if (CollUtil.isNotEmpty(userList)) {
        this.saveBatch(userList, 1000);
    }
```

## 禁止事项
### 数据库操作禁止
- ❌ **禁止在循环中执行单条 SQL**：必须使用 `saveBatch`、`updateBatchById`、`removeBatchByIds` 进行批量操作
- ❌ **禁止使用 `SELECT *`**：应明确指定所需列（使用 `select(Entity::getField1, Entity::getField2)`），尤其是列表接口和导出接口
- ❌ **禁止无条件更新/删除**：wrapper 必须包含明确的 where 条件，严禁条件恒为 true 或缺少条件的全表操作
- ❌ **禁止 N+1 查询**：先查列表再循环查详情/关联的场景，应改为批量查询（`in`）或 join/一次性查询
- ❌ **禁止在 Mapper 中编写业务逻辑**：Mapper 只负责数据访问，业务编排必须在 Service 完成

### 查询条件禁止
- ❌ **禁止使用 `QueryWrapper` 字符串硬编码字段名**：统一使用 `LambdaQueryWrapper` 防止重构遗漏（如 `new QueryWrapper<>().eq("user_id", id)`）
- ❌ **禁止前端传入的排序字段直接使用**：必须进行白名单校验，防止 order by 注入与越权字段读取
- ❌ **禁止在动态条件中未判空**：所有动态条件必须使用 `condition` 参数或提前判空，避免空值导致全表操作

### 数据安全禁止
- ❌ **禁止直接返回数据库实体类（Entity）给前端**：必须使用 VO（View Object）或 DTO 进行数据封装与脱敏
- ❌ **禁止将敏感字段暴露给前端**：密码、盐、身份证号、手机号全量、API密钥等必须脱敏或不返回
- ❌ **禁止在日志中输出敏感信息**：避免将用户密码、token、身份证号等敏感数据打印到日志

### 架构层次禁止
- ❌ **禁止 Controller 直接调用 Mapper**：必须通过 Service 访问数据层，保持分层清晰
- ❌ **禁止在 Controller 里做批量业务编排/事务性多步骤写入**：事务边界必须落在 Service
- ❌ **禁止在 Service 中硬编码 SQL**：复杂逻辑优先使用 MyBatis-Plus 构造器，特殊场景在 Mapper XML 或注解中编写

### 事务管理禁止
- ❌ **禁止在 Controller 层添加 `@Transactional`**：事务边界必须在 Service 层
- ❌ **禁止 `@Transactional` 不指定 `rollbackFor`**：必须显式指定 `rollbackFor = Exception.class`
- ❌ **禁止在事务方法中捕获异常后不抛出**：会导致事务不回滚
- ❌ **禁止在事务中调用长耗时外部服务**：如 HTTP 调用、MQ 发送等，防止长事务锁表

### 性能与规范禁止
- ❌ **禁止在生产环境使用 `System.out.println` 调试**：必须使用日志框架（slf4j、logback）
- ❌ **禁止在循环中频繁调用数据库**：应一次性查询后在内存中处理
- ❌ **禁止在列表接口返回大字段**：如富文本、大 JSON、文件内容等，应在详情接口返回

## 参考代码
- 文件路径：`ruoyi-system/src/main/java/org/dromara/system/mapper/SysUserMapper.java`
- 文件路径：`ruoyi-system/src/main/java/org/dromara/system/service/ISysUserService.java`
- 文件路径：`ruoyi-system/src/main/java/org/dromara/system/service/impl/SysUserServiceImpl.java`
- 文件路径：`ruoyi-admin/src/main/java/org/dromara/web/controller/system/SysUserController.java`
- 文件路径：`ruoyi-ui/src/views/system/user/index.vue`

## 检查清单
在完成 CRUD 相关代码后，请按以下清单逐项检查：

### 基础规范检查
- [ ] Mapper 是否继承 `BaseMapperPlus<Entity, Vo>`
- [ ] Service 接口是否继承 `IService<Entity>`
- [ ] Service 实现类是否继承 `ServiceImpl<Mapper, Entity>` 并实现接口
- [ ] Controller 是否直接调用 Mapper（必须通过 Service）

### 查询条件检查
- [ ] 是否使用 `LambdaQueryWrapper` / `LambdaUpdateWrapper` 构建查询条件
- [ ] 是否避免使用 `QueryWrapper` 硬编码字段名
- [ ] 动态条件是否使用 `condition` 参数判空
- [ ] 排序字段是否进行白名单校验（来自前端的情况）
- [ ] 更新操作是否确保 where 条件完备

### 分页与返回检查
- [ ] 分页查询是否使用 `PageQuery.build()` + `TableDataInfo.build(page)`
- [ ] 是否正确处理了分页参数
- [ ] 是否使用 VO 对象封装返回数据（严禁直接返回 Entity）
- [ ] 是否对敏感字段进行脱敏或不返回

### 性能优化检查
- [ ] 是否避免 `SELECT *` 并显式选择必要字段（尤其是列表接口）
- [ ] 是否避免 N+1 查询并对关联数据采用批量/一次性查询方案
- [ ] 是否使用批量操作（`saveBatch`/`updateBatchById`/`removeBatchByIds`）而非循环单条操作
- [ ] 批量操作是否判空并指定合理的 batchSize

### 事务与安全检查
- [ ] 多步骤写操作是否将事务边界放在 Service（使用 `@Transactional(rollbackFor = Exception.class)`）
- [ ] 事务方法是否避免调用长耗时外部服务
- [ ] 事务方法是否正确抛出异常（不吞异常）
- [ ] 是否对导出字段做了白名单校验（避免注入与越权字段读取）

### 代码质量检查
- [ ] 是否将查询条件封装到独立的 `buildQueryWrapper` 方法
- [ ] 是否避免在生产环境使用 `System.out.println`（使用日志框架）
- [ ] 是否在列表接口中避免返回大字段（富文本、大JSON等）
- [ ] 代码是否符合团队命名规范和注释规范
