---
name: database-ops
description: 定义了RuoYi-Vue-Plus框架下的数据库结构设计标准，规范了数据库初始化、版本升级DDL变更及Schema准备流程。核心要求包括强制包含标准审计字段、遵循小写下划线命名与InnoDB存储规范、禁止使用物理外键以提升性能，以及根据配置文件动态适配MySQL或Oracle数据库的SQL生成策略。
---

# Database-Ops 数据库设计

## 技能说明
本技能专为 **RuoYi-Vue-Plus** 框架的数据库设计场景定制，确保所有数据库操作符合框架规范，保证系统的可维护性、可扩展性和性能最优。

## 触发条件
### 必须触发的场景（强制）
- **关键词触发**：用户提及 DDL、CREATE TABLE、ALTER TABLE、DROP TABLE、建表、删表、改表、Schema、数据库设计、表结构设计
- **行为触发**：
  - 需要创建新的业务表或系统表时
  - 需要修改现有表结构（添加/删除/修改字段）时
  - 准备数据库初始化脚本时
  - 版本升级需要执行 DDL 变更时
  - 使用代码生成器前需要准备表结构时

### 应主动触发的场景（建议）
- 用户描述业务需求但未明确提及数据库时，应主动询问是否需要设计数据表
- 发现用户提供的 SQL 语句不符合框架规范时，应主动应用本技能进行修正

## 执行流程
1. **配置文件读取**：首先读取 `ruoyi-admin/src/main/resources/application-dev.yml` 确定数据库类型
2. **数据库类型判断**：
   - 如果配置中只有一个数据源，自动使用对应数据库的 SQL 语法
   - 如果配置中有多个数据源，**必须**询问用户在哪个数据库中执行操作
3. **系统表检查**（规范5）：检查系统表是否已初始化
4. **表结构设计**：按照核心规范1-4设计表结构
5. **生成 SQL 脚本**：输出符合目标数据库语法的 DDL 语句
6. **检查清单验证**：对照检查清单进行最终验证

## 核心规范
### 规范1：强制包含标准审计字段 [MANDATORY]
**适用范围**：所有业务表（bus_*）和系统表（sys_*），字典表和配置表除外

**必须包含的字段**（顺序不可更改，必须放在业务字段之后、主键定义之前）：
1. `create_by` varchar(64) DEFAULT '' COMMENT '创建者'
2. `create_time` datetime DEFAULT NULL COMMENT '创建时间'
3. `update_by` varchar(64) DEFAULT '' COMMENT '更新者'
4. `update_time` datetime DEFAULT NULL COMMENT '更新时间'
5. `remark` varchar(500) DEFAULT NULL COMMENT '备注'
6. `del_flag` char(1) DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）'

**技术原因**：
- 这些字段对应 `BaseEntity` 基类，框架会自动填充创建/更新信息
- `del_flag` 支持 MyBatis-Plus 的逻辑删除功能，避免物理删除数据
- 缺少任何一个字段都会导致框架的自动审计功能失效
**示例代码**：
```sql
CREATE TABLE `sys_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `user_name` varchar(30) NOT NULL COMMENT '用户账号',
  `nick_name` varchar(30) NOT NULL COMMENT '用户昵称',
  `dept_id` bigint(20) DEFAULT NULL COMMENT '部门ID',
  -- ========== 标准审计字段 Start（必须严格按此顺序） ==========
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  -- ========== 标准审计字段 End ==========
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户信息表';
```

### 规范2：遵循命名与存储规范 [MANDATORY]
**命名规范**（严格执行）：
- **表名**：必须使用小写字母 + 下划线（snake_case），格式为 `前缀_业务名`
  - 系统表前缀：`sys_`（如 sys_user、sys_role）
  - 业务表前缀：`bus_`（如 bus_order、bus_product）
  - 临时表前缀：`tmp_`（如 tmp_import_data）
- **字段名**：必须使用小写字母 + 下划线，禁止使用驼峰命名
  - ✅ 正确：`user_name`, `order_id`, `create_time`
  - ❌ 错误：`userName`, `orderId`, `createTime`
- **主键命名**：必须为 `表名单数_id`（如 user_id、order_id）
- **索引命名**：
  - 普通索引：`idx_字段名`（如 idx_user_name）
  - 唯一索引：`uk_字段名`（如 uk_order_sn）
  - 联合索引：`idx_字段1_字段2`（如 idx_dept_id_status）

**存储规范**（强制）：
- **存储引擎**：必须使用 `InnoDB`（支持事务、行级锁、外键约束）
- **字符集**：必须使用 `utf8mb4`（支持完整的 Unicode 字符，包括 emoji）
- **排序规则**：必须使用 `utf8mb4_general_ci`（不区分大小写）
- **主键类型**：必须使用 `bigint(20) NOT NULL AUTO_INCREMENT`
- **自增起始值**：系统表从 100 开始，业务表从 1 开始
**示例代码**：
```sql
-- ✅ 正确示例：完全符合规范
CREATE TABLE `bus_order` (
  `order_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_sn` varchar(64) NOT NULL COMMENT '订单编号',
  `order_amount` decimal(10,2) NOT NULL COMMENT '订单金额',
  `pay_status` char(1) DEFAULT '0' COMMENT '支付状态（0未支付 1已支付）',
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `uk_order_sn` (`order_sn`),
  KEY `idx_pay_status` (`pay_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='业务订单表';
```

### 规范3：禁止使用物理外键 [MANDATORY]
**核心原则**：严禁在表级别建立物理外键约束（FOREIGN KEY）

**技术原因**：
- **性能问题**：物理外键会在 INSERT/UPDATE/DELETE 操作时触发额外的约束检查，降低并发性能
- **锁表风险**：级联更新/删除可能导致大范围锁表，影响系统可用性
- **分库分表限制**：物理外键无法跨库使用，限制了水平扩展能力
- **灵活性降低**：业务逻辑变更时需要先删除外键约束，增加维护成本

**正确做法**：
1. 使用普通索引（KEY）代替外键约束，仅用于加速关联查询
2. 在业务代码层面通过 Service 层保证数据一致性
3. 使用 MyBatis-Plus 的 `@TableField` 注解配置逻辑关联
**示例对比**：
```sql
-- ❌ 错误示例：使用了物理外键约束
CREATE TABLE `bus_order` (
  `order_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '下单用户ID',
  PRIMARY KEY (`order_id`),
  CONSTRAINT `fk_order_user` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ✅ 正确示例：仅创建普通索引
CREATE TABLE `bus_order` (
  `order_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `user_id` bigint(20) DEFAULT NULL COMMENT '下单用户ID',
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  PRIMARY KEY (`order_id`),
  KEY `idx_user_id` (`user_id`) -- 仅创建索引以加速查询，不建立外键约束
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='业务订单表';
```

### 规范4：根据数据库类型生成对应 SQL [MANDATORY]
**配置文件读取**：
- **路径**：`ruoyi-admin/src/main/resources/application-dev.yml`
- **关键配置**：`spring.datasource.dynamic.datasource`

**判断逻辑**：
1. **单数据源场景**：
   - 如果只配置了 MySQL，自动生成 MySQL 语法的 SQL
   - 如果只配置了 Oracle，自动生成 Oracle 语法的 SQL
   - 如果只配置了 PostgreSQL，自动生成 PostgreSQL 语法的 SQL

2. **多数据源场景**：
   - **必须**询问用户："检测到多个数据源（MySQL、Oracle），请问要在哪个数据库中创建此表？"
   - 等待用户明确回复后再生成对应语法的 SQL

**数据类型映射差异**：

| 通用类型 | MySQL | Oracle | PostgreSQL |
|---------|-------|--------|------------|
| 主键 | bigint(20) AUTO_INCREMENT | NUMBER(20) + SEQUENCE | bigserial |
| 长文本 | varchar(255) | VARCHAR2(255) | varchar(255) |
| 日期时间 | datetime | DATE | timestamp |
| 小数 | decimal(10,2) | NUMBER(10,2) | numeric(10,2) |
| 布尔 | char(1) | CHAR(1) | char(1) |

**示例**：
```sql
-- MySQL 语法
CREATE TABLE `bus_order` (
  `order_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_time` datetime DEFAULT NULL COMMENT '下单时间',
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Oracle 语法
CREATE TABLE bus_order (
  order_id NUMBER(20) NOT NULL,
  order_time DATE DEFAULT NULL,
  PRIMARY KEY (order_id)
);
CREATE SEQUENCE seq_bus_order START WITH 1 INCREMENT BY 1;
COMMENT ON TABLE bus_order IS '订单表';
COMMENT ON COLUMN bus_order.order_id IS '订单ID';
COMMENT ON COLUMN bus_order.order_time IS '下单时间';
```

### 规范5：系统表初始化检查 [MANDATORY]
**执行时机**：在创建任何业务表之前，必须先确保系统表已初始化

**检查流程**：
1. **读取配置文件**：`ruoyi-admin/src/main/resources/application-dev.yml`
2. **确定数据库类型**：
   - 如果是 MySQL，检查 `script/sql/mysql/` 目录
   - 如果是 Oracle，检查 `script/sql/oracle/` 目录
   - 如果是 PostgreSQL，检查 `script/sql/postgresql/` 目录
3. **验证系统表**：
   - 读取对应数据库目录下的 SQL 初始化脚本
   - 检查以下核心系统表是否已存在：
     - `sys_user`（用户表）
     - `sys_role`（角色表）
     - `sys_menu`（菜单表）
     - `sys_dept`（部门表）
     - `sys_dict_type`（字典类型表）
     - `sys_dict_data`（字典数据表）
4. **执行初始化**：
   - 如果系统表不存在，**必须**先提示用户："检测到系统表未初始化，需要先执行 `script/sql/mysql/ry-vue-plus.sql` 初始化系统表，是否继续？"
   - 等待用户确认后，提供完整的初始化 SQL 脚本路径

**重要提示**：
- 系统表必须在业务表之前创建，否则可能导致权限、字典等功能异常
- 不同数据库的初始化脚本语法不同，必须使用对应数据库的脚本

## 禁止事项 [CRITICAL]
### 数据库设计层面
- ❌ **禁止省略 COMMENT 注释**：所有表和字段必须有中文注释说明业务含义，方便团队协作
- ❌ **禁止使用物理外键**：严禁使用 `FOREIGN KEY` 约束，必须通过业务层维护关联
- ❌ **禁止省略审计字段**：所有业务表必须包含完整的 6 个标准审计字段（create_by、create_time、update_by、update_time、remark、del_flag）
- ❌ **禁止使用驼峰命名**：表名和字段名必须使用 snake_case，不能使用 camelCase
- ❌ **禁止使用 MyISAM 引擎**：必须使用 InnoDB 引擎以支持事务和行级锁
- ❌ **禁止使用 utf8 字符集**：必须使用 utf8mb4 以支持完整 Unicode（包括 emoji）
- ❌ **禁止使用 SELECT * 视图**：视图定义必须明确列出所有字段

### 字段定义层面
- ❌ **禁止使用 TEXT/BLOB 类型**：应使用 varchar 并指定合理长度，便于索引优化
- ❌ **禁止不指定字段长度**：varchar 和 char 必须明确指定长度（如 varchar(255)）
- ❌ **禁止使用 NULL 作为默认值（特殊情况除外）**：优先使用空字符串 '' 或 0 作为默认值
- ❌ **禁止主键使用 int 类型**：必须使用 bigint(20) 以避免 ID 溢出
- ❌ **禁止金额字段使用 float/double**：必须使用 decimal(10,2) 避免精度丢失

### 索引设计层面
- ❌ **禁止在低基数字段上建索引**：如性别（只有男/女）不适合建索引
- ❌ **禁止过多索引**：单表索引数量不超过 5 个，避免影响写入性能
- ❌ **禁止联合索引字段顺序错误**：必须按照查询频率和区分度排序（最常用且区分度高的在前）

### 操作流程层面
- ❌ **禁止跳过配置文件读取**：必须先读取 application-dev.yml 确定数据库类型
- ❌ **禁止在多数据源场景下擅自决定**：检测到多数据源时必须询问用户选择哪个数据库
- ❌ **禁止在系统表未初始化时创建业务表**：必须先确保系统表已存在
- ❌ **禁止直接修改系统表结构**：系统表（sys_*）结构由框架维护，除非有充分理由
- ❌ **禁止在生产环境直接执行 DDL**：必须先在开发/测试环境验证后再发布

### 安全与性能层面
- ❌ **禁止存储明文密码**：密码字段必须使用加密存储
- ❌ **禁止在 SQL 中硬编码敏感信息**：如数据库连接字符串、密钥等
- ❌ **禁止创建无主键表**：所有表必须有主键
- ❌ **禁止使用保留关键字作为表名或字段名**：如 order、user、group 等（应加前缀如 bus_order）

## 参考代码资源
### 框架核心文件
- **系统表初始化脚本**（MySQL）：`script/sql/mysql/ry-vue-plus.sql`
- **系统表初始化脚本**（Oracle）：`script/sql/oracle/ry-vue-plus.sql`
- **基础实体类**：`ruoyi-common/src/main/java/org/dromara/common/core/domain/BaseEntity.java`
  - 作用：定义标准审计字段的 Java 映射
- **用户实体示例**：`ruoyi-system/src/main/java/org/dromara/system/domain/SysUser.java`
  - 作用：参考如何继承 BaseEntity 并定义业务字段
- **配置文件**：`ruoyi-admin/src/main/resources/application-dev.yml`
  - 作用：读取数据源配置，确定目标数据库类型

### 数据类型参考
#### MySQL 常用类型
- 主键：`bigint(20) NOT NULL AUTO_INCREMENT`
- 字符串（短）：`varchar(64)` / `varchar(255)`
- 字符串（长）：`varchar(500)` / `varchar(2000)`
- 状态标识：`char(1)` 
- 金额：`decimal(10,2)`
- 日期时间：`datetime`
- 整数：`int(11)` / `bigint(20)`

#### Oracle 常用类型
- 主键：`NUMBER(20)` + `SEQUENCE`
- 字符串：`VARCHAR2(64)` / `VARCHAR2(255)`
- 状态标识：`CHAR(1)`
- 金额：`NUMBER(10,2)`
- 日期时间：`DATE`
- 整数：`NUMBER(11)` / `NUMBER(20)`

## 检查清单（执行前必查）
### 结构完整性检查
- [ ] 是否包含所有 6 个标准审计字段（create_by, create_time, update_by, update_time, remark, del_flag）
- [ ] 审计字段顺序是否正确（必须在业务字段之后、主键定义之前）
- [ ] 是否定义了主键，且主键类型为 `bigint(20) NOT NULL AUTO_INCREMENT`

### 命名规范检查
- [ ] 表名是否使用 snake_case 且有正确前缀（sys_/bus_/tmp_）
- [ ] 字段名是否全部使用 snake_case（无驼峰命名）
- [ ] 索引命名是否符合规范（idx_* 或 uk_*）

### 存储配置检查
- [ ] 引擎是否为 `InnoDB`
- [ ] 字符集是否为 `utf8mb4`
- [ ] 排序规则是否为 `utf8mb4_general_ci`

### 约束与索引检查
- [ ] 是否存在物理外键约束（如有必须删除，改用普通索引 + 业务层维护）
- [ ] 关联字段是否创建了普通索引（KEY）以加速查询
- [ ] 唯一性约束是否使用 UNIQUE KEY

### 字段类型检查
- [ ] 所有 varchar 和 char 字段是否指定了合理的长度
- [ ] 金额字段是否使用 decimal 而非 float/double
- [ ] 日期时间字段是否使用 datetime 而非 timestamp

### 注释完整性检查
- [ ] 表是否有 COMMENT 注释说明业务含义
- [ ] 所有字段是否都有 COMMENT 注释（必须是中文描述）
- [ ] 状态字段的注释是否说明了枚举值含义（如：0未支付 1已支付）

### 环境适配检查
- [ ] 是否已读取 application-dev.yml 确定数据库类型
- [ ] 多数据源场景是否已询问用户选择目标数据库
- [ ] 生成的 SQL 语法是否匹配目标数据库（MySQL/Oracle/PostgreSQL）
- [ ] 是否已检查系统表初始化状态

## 常见问题与解决方案
### Q1：为什么必须使用 bigint(20) 而不是 int？
**A**：int 最大值约 21 亿，在高并发系统中容易溢出。bigint 最大值约 922 亿亿，足够使用。

### Q2：为什么禁止使用物理外键？
**A**：物理外键会严重影响并发性能，且在分库分表场景下无法使用。建议通过业务层 Service 保证数据一致性。

### Q3：如何处理已存在的表需要新增字段的情况？
**A**：使用 ALTER TABLE 语句，新增字段必须放在标准审计字段之前：
```sql
ALTER TABLE `bus_order` 
ADD COLUMN `discount_amount` decimal(10,2) DEFAULT 0.00 COMMENT '优惠金额' AFTER `order_amount`;
```

### Q4：如何处理多租户场景的表设计？
**A**：在业务表中添加 `tenant_id` 字段，并创建索引：
```sql
`tenant_id` varchar(20) DEFAULT '000000' COMMENT '租户编号',
KEY `idx_tenant_id` (`tenant_id`)
```

### Q5：表名超过 MySQL 64 字符限制怎么办？
**A**：使用缩写或重新设计表名，确保表名简洁且有意义。例如：
- ❌ `bus_user_order_delivery_address_history` (太长)
- ✅ `bus_delivery_addr_history` (简洁明了)

## 输出格式要求（⭐ 关键）

### 核心原则：必须输出完整可执行的 SQL 脚本文件

**强制要求**：
1. 所有 SQL 语句必须整合为一个完整的脚本文件格式
2. 脚本必须包含文件头注释、数据库选择、表创建等完整内容
3. 脚本必须可以直接复制粘贴到数据库管理工具中一键执行
4. 多个表的情况下，必须统一在一个脚本中按逻辑顺序排列

### 标准 SQL 脚本文件格式（MySQL）

```sql
-- ====================================================
-- RuoYi-Vue-Plus 业务表 DDL 脚本
-- ====================================================
-- 功能模块：订单管理模块
-- 创建时间：2026-01-26
-- 数据库类型：MySQL 5.7+
-- 执行说明：在开发环境执行前请先备份数据库
-- ====================================================

-- 切换到目标数据库（根据实际情况修改数据库名）
USE `ry-vue-plus`;

-- ====================================================
-- 表1：bus_order (业务订单表)
-- 说明：存储用户订单信息，支持逻辑删除
-- ====================================================

DROP TABLE IF EXISTS `bus_order`;

CREATE TABLE `bus_order` (
  -- 业务主键
  `order_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  
  -- 业务字段
  `order_sn` varchar(64) NOT NULL COMMENT '订单编号',
  `user_id` bigint(20) NOT NULL COMMENT '下单用户ID',
  `order_amount` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '订单金额',
  `pay_status` char(1) DEFAULT '0' COMMENT '支付状态（0未支付 1已支付 2已退款）',
  
  -- 标准审计字段
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  
  -- 主键与索引
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `uk_order_sn` (`order_sn`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_pay_status` (`pay_status`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='业务订单表';

-- ====================================================
-- 表2：bus_order_item (订单明细表)
-- 说明：存储订单商品明细信息
-- ====================================================

DROP TABLE IF EXISTS `bus_order_item`;

CREATE TABLE `bus_order_item` (
  -- 业务主键
  `item_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '明细ID',
  
  -- 业务字段
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
  `product_name` varchar(255) NOT NULL COMMENT '商品名称',
  `quantity` int(11) NOT NULL DEFAULT 1 COMMENT '购买数量',
  `price` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '商品单价',
  
  -- 标准审计字段
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  
  -- 主键与索引
  PRIMARY KEY (`item_id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='订单明细表';

-- ====================================================
-- 脚本执行完成提示
-- ====================================================
-- 执行成功后，请验证表结构：
-- DESC bus_order;
-- DESC bus_order_item;
-- ====================================================
```

### 标准 SQL 脚本文件格式（Oracle）

```sql
-- ====================================================
-- RuoYi-Vue-Plus 业务表 DDL 脚本
-- ====================================================
-- 功能模块：订单管理模块
-- 创建时间：2026-01-26
-- 数据库类型：Oracle 11g+
-- 执行说明：在开发环境执行前请先备份数据库
-- ====================================================

-- 删除已存在的表（如果存在）
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE bus_order CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE seq_bus_order';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

-- ====================================================
-- 表1：bus_order (业务订单表)
-- 说明：存储用户订单信息，支持逻辑删除
-- ====================================================

CREATE TABLE bus_order (
  order_id NUMBER(20) NOT NULL,
  order_sn VARCHAR2(64) NOT NULL,
  user_id NUMBER(20) NOT NULL,
  order_amount NUMBER(10,2) DEFAULT 0.00 NOT NULL,
  pay_status CHAR(1) DEFAULT '0',
  create_by VARCHAR2(64) DEFAULT '',
  create_time DATE DEFAULT NULL,
  update_by VARCHAR2(64) DEFAULT '',
  update_time DATE DEFAULT NULL,
  remark VARCHAR2(500) DEFAULT NULL,
  del_flag CHAR(1) DEFAULT '0',
  PRIMARY KEY (order_id)
);

-- 创建序列
CREATE SEQUENCE seq_bus_order START WITH 1 INCREMENT BY 1 NOCACHE;

-- 添加表注释
COMMENT ON TABLE bus_order IS '业务订单表';
COMMENT ON COLUMN bus_order.order_id IS '订单ID';
COMMENT ON COLUMN bus_order.order_sn IS '订单编号';
COMMENT ON COLUMN bus_order.user_id IS '下单用户ID';
COMMENT ON COLUMN bus_order.order_amount IS '订单金额';
COMMENT ON COLUMN bus_order.pay_status IS '支付状态（0未支付 1已支付 2已退款）';
COMMENT ON COLUMN bus_order.create_by IS '创建者';
COMMENT ON COLUMN bus_order.create_time IS '创建时间';
COMMENT ON COLUMN bus_order.update_by IS '更新者';
COMMENT ON COLUMN bus_order.update_time IS '更新时间';
COMMENT ON COLUMN bus_order.remark IS '备注';
COMMENT ON COLUMN bus_order.del_flag IS '删除标志（0代表存在 2代表删除）';

-- 创建索引
CREATE UNIQUE INDEX uk_order_sn ON bus_order(order_sn);
CREATE INDEX idx_user_id ON bus_order(user_id);
CREATE INDEX idx_pay_status ON bus_order(pay_status);

-- ====================================================
-- 脚本执行完成
-- ====================================================
```

### 输出要求总结

**必须包含的部分**（按顺序）：
1. ✅ **脚本文件头注释**（功能模块、创建时间、数据库类型、执行说明）
2. ✅ **数据库选择语句**（MySQL: USE 语句；Oracle: 连接到对应schema）
3. ✅ **每个表的完整 DDL**：
   - 表头注释（表名、说明）
   - DROP TABLE IF EXISTS 语句
   - CREATE TABLE 语句（含所有字段、约束、索引）
   - Oracle 需额外包含 SEQUENCE 和 COMMENT 语句
4. ✅ **脚本执行完成提示**（验证命令、注意事项）

**输出规范**：
- 所有 SQL 必须在同一个代码块中（```sql ... ```）
- 脚本必须可以一键复制粘贴执行
- 多表创建时，按照依赖关系排序（主表在前，从表在后）
- 必须包含完整的注释说明，便于后续维护

## 执行后的反馈模板

完成 SQL 脚本生成后，必须向用户提供以下完整反馈：

---
✅ **SQL 脚本生成完成**

**脚本信息**：
- 功能模块：订单管理模块
- 包含表数：2 个表（bus_order、bus_order_item）
- 数据库类型：MySQL 5.7+
- 脚本行数：约 80 行

**表结构统计**：

| 表名 | 中文名 | 字段数 | 索引数 |
|------|--------|--------|--------|
| bus_order | 业务订单表 | 10 个业务字段 + 6 个审计字段 | 1 主键 + 1 唯一 + 2 普通 |
| bus_order_item | 订单明细表 | 8 个业务字段 + 6 个审计字段 | 1 主键 + 2 普通 |

**脚本文件建议路径**：
```
项目根目录/script/sql/business/order_management_ddl.sql
```

**下一步操作指南**：

**步骤1：保存脚本文件**
```bash
# 创建业务 SQL 目录（如果不存在）
mkdir -p script/sql/business

# 将上述 SQL 保存为文件
vim script/sql/business/order_management_ddl.sql
```

**步骤2：在开发环境执行脚本**
- 方式1（命令行）：
  ```bash
  mysql -u root -p ry-vue-plus < script/sql/business/order_management_ddl.sql
  ```
- 方式2（Navicat/DBeaver）：
  1. 打开 SQL 文件
  2. 选中全部内容
  3. 点击"运行"按钮执行

**步骤3：验证表结构**
```sql
-- 验证表是否创建成功
SHOW TABLES LIKE 'bus_order%';

-- 查看表结构
DESC bus_order;
DESC bus_order_item;

-- 验证索引是否正确
SHOW INDEX FROM bus_order;
```

**步骤4：使用代码生成器（可选）**
1. 访问代码生成器页面：`http://localhost:8080/tool/gen`
2. 导入 `bus_order` 和 `bus_order_item` 表
3. 配置生成选项后，生成对应的 Java 代码

**注意事项**：
- ⚠️ **请勿在生产环境直接执行**，必须先在开发/测试环境验证
- ⚠️ 如果表已存在，`DROP TABLE` 语句会删除原表数据，请提前备份
- ⚠️ 执行前确认数据库名称是否正确（脚本中的 `USE ry-vue-plus`）
- ⚠️ 执行后建议提交 SQL 脚本到版本控制系统（Git）

**版本控制建议**：
```bash
# 将 SQL 脚本纳入 Git 管理
git add script/sql/business/order_management_ddl.sql
git commit -m "feat: 添加订单管理模块数据库表结构"
```

---