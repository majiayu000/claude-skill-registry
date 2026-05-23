---
name: performance-doctor
description: |
  基于若依-vue-plus框架的系统性能优化专家技能。专注于数据库查询优化（MyBatis-Plus）、缓存策略（Redis）、异步处理及前端性能优化，系统性解决慢SQL、高并发阻塞、内存泄漏及页面卡顿问题。
  
  触发场景：
  - 系统响应缓慢，接口响应时间超过2秒
  - 数据库CPU占用率持续高于80%
  - 接口频繁超时或出现504错误
  - 页面加载时间超过5秒或出现白屏
  - Redis内存占用异常增长
  - 线程池队列堆积或线程阻塞
  
  触发词：性能优化、性能诊断、慢SQL、SQL优化、N+1问题、Redis缓存、缓存击穿、缓存雪崩、异步处理、线程池、内存溢出、接口超时、页面卡顿、虚拟滚动
---

# 性能优化规范

## 使用指南
当识别到性能相关问题时，应按以下步骤执行：
1. **问题诊断**：通过日志、监控指标或用户描述确定性能瓶颈类型
2. **定位根因**：使用Explain分析SQL、检查Redis命中率、查看线程池状态
3. **应用规范**：根据问题类型应用对应的核心规范
4. **验证效果**：通过压测或监控验证优化效果
5. **文档记录**：记录优化前后的关键指标对比

## 核心规范
### 规范1：数据库查询优化与 MyBatis-Plus 最佳实践

**适用场景**：接口响应慢、数据库CPU高、存在循环查询

**核心原则**：
1. **消除N+1查询**：严禁在循环中执行数据库查询，必须使用批量查询
2. **字段裁剪**：避免`select *`，通过`select()`方法仅查询必要字段，减少网络传输和内存占用
3. **索引优化**：对高频查询条件（WHERE）、关联字段（JOIN）、排序字段（ORDER BY）建立索引
4. **分页查询**：大数据量查询必须使用分页，避免一次性加载过多数据
5. **查询条件优化**：避免在索引字段上使用函数、类型转换或模糊匹配前缀

**性能指标**：
- 单次查询响应时间 < 100ms
- 批量查询每条记录平均时间 < 10ms
- 避免全表扫描，确保Explain显示使用索引

```java
/**
 * 批量查询与字段优化示例
 */
@Service
public class SysUserServiceImpl extends ServiceImpl<SysUserMapper, SysUser> implements ISysUserService {

    // ❌ 错误示例1：循环查询（N+1问题）
    public List<UserVO> getBadData(List<Long> ids) {
        List<UserVO> list = new ArrayList<>();
        for (Long id : ids) {
            // 问题：每次循环都执行一次SQL，100个ID就是100次查询
            // 性能影响：原本1次查询可完成的任务，变成了N次网络往返
            SysUser user = baseMapper.selectById(id);
            list.add(BeanUtil.copyProperties(user, UserVO.class));
        }
        return list;
    }

    // ❌ 错误示例2：查询所有字段
    public List<UserVO> getBadDataWithAllFields(List<Long> ids) {
        // 问题：查询了不必要的字段（如密码、盐值、个人简介等大字段）
        // 性能影响：增加网络传输量、内存占用和序列化开销
        List<SysUser> users = baseMapper.selectBatchIds(ids);
        return BeanUtil.copyToList(users, UserVO.class);
    }

    // ✅ 正确示例：批量查询 + 字段裁剪
    public List<UserVO> getGoodData(List<Long> ids) {
        if (CollUtil.isEmpty(ids)) {
            return Collections.emptyList();
        }
        
        // 方式1：批量查询（适用于需要完整对象）
        List<SysUser> users = baseMapper.selectBatchIds(ids);
        
        // 方式2：仅查询必要字段（推荐，性能更优）
        List<SysUser> users = baseMapper.selectList(
            new LambdaQueryWrapper<SysUser>()
                .select(SysUser::getUserId, SysUser::getNickName, 
                        SysUser::getAvatar, SysUser::getDeptId)
                .in(SysUser::getUserId, ids)
        );

        return BeanUtil.copyToList(users, UserVO.class);
    }
    
    // ✅ 高级示例：关联查询优化（先查主表，再批量关联）
    public List<UserWithDeptVO> getUsersWithDept(List<Long> userIds) {
        // 1. 批量查询用户信息
        List<SysUser> users = baseMapper.selectList(
            new LambdaQueryWrapper<SysUser>()
                .select(SysUser::getUserId, SysUser::getNickName, SysUser::getDeptId)
                .in(SysUser::getUserId, userIds)
        );
        
        // 2. 提取部门ID
        Set<Long> deptIds = users.stream()
            .map(SysUser::getDeptId)
            .filter(Objects::nonNull)
            .collect(Collectors.toSet());
        
        // 3. 批量查询部门信息
        Map<Long, String> deptMap = Collections.emptyMap();
        if (CollUtil.isNotEmpty(deptIds)) {
            deptMap = deptMapper.selectList(
                new LambdaQueryWrapper<SysDept>()
                    .select(SysDept::getDeptId, SysDept::getDeptName)
                    .in(SysDept::getDeptId, deptIds)
            ).stream().collect(Collectors.toMap(SysDept::getDeptId, SysDept::getDeptName));
        }
        
        // 4. 组装结果
        Map<Long, String> finalDeptMap = deptMap;
        return users.stream().map(user -> {
            UserWithDeptVO vo = BeanUtil.copyProperties(user, UserWithDeptVO.class);
            vo.setDeptName(finalDeptMap.get(user.getDeptId()));
            return vo;
        }).collect(Collectors.toList());
    }
    
    // ✅ 分页查询示例
    public TableDataInfo<UserVO> pageUsers(UserQueryDTO query) {
        Page<SysUser> page = baseMapper.selectPage(
            new Page<>(query.getPageNum(), query.getPageSize()),
            new LambdaQueryWrapper<SysUser>()
                .select(SysUser::getUserId, SysUser::getNickName, SysUser::getStatus)
                .like(StringUtils.isNotEmpty(query.getNickName()), 
                      SysUser::getNickName, query.getNickName())
                .orderByDesc(SysUser::getCreateTime)
        );
        return TableDataInfo.build(page);
    }
}
```

**索引创建示例**：
```sql
-- 为高频查询条件建立索引
CREATE INDEX idx_user_status ON sys_user(status);
CREATE INDEX idx_user_dept_id ON sys_user(dept_id);
CREATE INDEX idx_user_create_time ON sys_user(create_time);

-- 联合索引（遵循最左前缀原则）
CREATE INDEX idx_user_status_dept ON sys_user(status, dept_id);
```

### 规范2：Redis缓存策略与高可用设计

**适用场景**：热点数据查询频繁、接口响应慢、数据库压力大

**核心原则**：
1. **缓存分层**：区分热点数据（字典、配置）、会话数据（登录信息）、业务数据（查询结果）
2. **防护机制**：必须实现缓存穿透（空值缓存/布隆过滤器）、击穿（互斥锁）、雪崩（随机过期时间）防护
3. **合理TTL**：根据数据更新频率设置过期时间，避免永久缓存导致数据不一致
4. **容量控制**：大对象拆分存储，单个缓存值不超过10KB，列表类缓存不超过1000条
5. **缓存更新**：数据变更时及时删除或更新缓存，避免脏数据

**性能指标**：
- 缓存命中率 > 90%
- Redis响应时间 < 10ms
- 缓存穿透/击穿/雪崩发生率 < 0.1%

```java
@Service
public class CacheOptimizationService {

    @Autowired
    private RedisUtils redisUtils;
    
    @Autowired
    private SysDictDataMapper dictDataMapper;

    /**
     * ✅ 示例1：热点数据缓存（字典查询）
     */
    public String getDictLabel(String dictType, String dictValue) {
        String cacheKey = CacheConstants.SYS_DICT_KEY + dictType + ":" + dictValue;
        
        // 1. 先查缓存
        String label = redisUtils.getCacheObject(cacheKey);
        if (StringUtils.isNotEmpty(label)) {
            return label;
        }

        // 2. 查库
        label = dictDataMapper.selectDictLabel(dictType, dictValue);
        
        // 3. 写入缓存（设置2小时过期，防止内存泄漏）
        if (StringUtils.isNotEmpty(label)) {
            redisUtils.setCacheObject(cacheKey, label, 2, TimeUnit.HOURS);
        } else {
            // 防止缓存穿透：缓存空值，设置较短过期时间
            redisUtils.setCacheObject(cacheKey, "", 5, TimeUnit.MINUTES);
        }
        
        return label;
    }

    /**
     * ✅ 示例2：缓存击穿防护（热点数据加互斥锁）
     */
    public SysConfig getConfig(String configKey) {
        String cacheKey = CacheConstants.SYS_CONFIG_KEY + configKey;
        
        // 1. 查缓存
        SysConfig config = redisUtils.getCacheObject(cacheKey);
        if (config != null) {
            return config;
        }
        
        // 2. 使用互斥锁防止缓存击穿
        String lockKey = "lock:" + cacheKey;
        boolean locked = false;
        try {
            // 尝试获取锁（设置30秒超时）
            locked = redisUtils.setIfAbsent(lockKey, "1", 30, TimeUnit.SECONDS);
            
            if (locked) {
                // 获得锁，查询数据库
                config = configMapper.selectConfigByKey(configKey);
                if (config != null) {
                    // 随机过期时间（1-2小时），防止缓存雪崩
                    int expireTime = 3600 + RandomUtil.randomInt(3600);
                    redisUtils.setCacheObject(cacheKey, config, expireTime, TimeUnit.SECONDS);
                }
            } else {
                // 未获得锁，等待100ms后重试查询缓存
                Thread.sleep(100);
                config = redisUtils.getCacheObject(cacheKey);
                if (config == null) {
                    // 缓存仍未建立，直接查库（降级方案）
                    config = configMapper.selectConfigByKey(configKey);
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            if (locked) {
                redisUtils.deleteObject(lockKey);
            }
        }
        
        return config;
    }

    /**
     * ✅ 示例3：列表缓存优化（避免大对象）
     */
    public List<SysDictData> getDictDataList(String dictType) {
        String cacheKey = CacheConstants.SYS_DICT_KEY + dictType;
        
        // 1. 查缓存
        Collection<Object> cacheList = redisUtils.getCacheCollection(cacheKey);
        if (CollUtil.isNotEmpty(cacheList)) {
            return cacheList.stream()
                .map(obj -> (SysDictData) obj)
                .collect(Collectors.toList());
        }
        
        // 2. 查库
        List<SysDictData> dataList = dictDataMapper.selectDictDataByType(dictType);
        
        // 3. 缓存结果（仅缓存小于1000条的列表）
        if (CollUtil.isNotEmpty(dataList) && dataList.size() < 1000) {
            redisUtils.setCacheList(cacheKey, dataList);
            redisUtils.expire(cacheKey, 24, TimeUnit.HOURS);
        }
        
        return dataList;
    }

    /**
     * ✅ 示例4：布隆过滤器防止缓存穿透（适用于海量数据）
     */
    @Autowired
    private RedissonClient redissonClient;
    
    public SysUser getUserById(Long userId) {
        // 1. 布隆过滤器判断是否存在
        RBloomFilter<Long> bloomFilter = redissonClient.getBloomFilter("user:bloom");
        if (!bloomFilter.contains(userId)) {
            // 不存在，直接返回，避免查库
            return null;
        }
        
        // 2. 查缓存
        String cacheKey = CacheConstants.USER_KEY + userId;
        SysUser user = redisUtils.getCacheObject(cacheKey);
        if (user != null) {
            return user;
        }
        
        // 3. 查库
        user = userMapper.selectById(userId);
        if (user != null) {
            redisUtils.setCacheObject(cacheKey, user, 1, TimeUnit.HOURS);
        }
        
        return user;
    }

    /**
     * ✅ 示例5：缓存更新策略（数据变更时删除缓存）
     */
    @Transactional
    public int updateConfig(SysConfig config) {
        // 1. 更新数据库
        int rows = configMapper.updateConfig(config);
        
        // 2. 删除缓存（保证数据一致性）
        if (rows > 0) {
            redisUtils.deleteObject(CacheConstants.SYS_CONFIG_KEY + config.getConfigKey());
        }
        
        return rows;
    }

    /**
     * ❌ 错误示例：大对象直接缓存
     */
    public void badCacheExample(List<SysUser> users) {
        // 问题：列表过大（10000条），占用Redis内存过多，序列化/反序列化耗时
        redisUtils.setCacheObject("all:users", users);
    }

    /**
     * ❌ 错误示例：永久缓存导致数据不一致
     */
    public void badCacheNoExpire(String key, Object value) {
        // 问题：未设置过期时间，数据更新后缓存不会自动失效
        redisUtils.setCacheObject(key, value);
    }
}
```

**布隆过滤器初始化示例**：
```java
@Component
public class BloomFilterInitializer {
    
    @Autowired
    private RedissonClient redissonClient;
    
    @Autowired
    private SysUserMapper userMapper;
    
    @PostConstruct
    public void initUserBloomFilter() {
        RBloomFilter<Long> bloomFilter = redissonClient.getBloomFilter("user:bloom");
        // 预计元素数量100万，误判率0.01
        bloomFilter.tryInit(1000000L, 0.01);
        
        // 将所有用户ID加入布隆过滤器
        List<Long> userIds = userMapper.selectAllUserIds();
        userIds.forEach(bloomFilter::add);
    }
}
```

### 规范3：异步处理与线程池优化

**适用场景**：接口响应慢、非核心操作阻塞主流程、需要解耦长耗时任务

**核心原则**：
1. **异步化非核心操作**：日志记录、邮件/短信发送、统计报表、消息推送等必须异步处理
2. **线程池隔离**：不同业务使用独立线程池，避免相互影响
3. **异常处理**：异步任务异常不能影响主流程，必须捕获并记录日志
4. **上下文传递**：异步任务中无法自动获取当前登录用户、租户等信息，需显式传递
5. **任务监控**：记录任务执行时间、成功率，及时发现线程池满、任务堆积等问题

**性能指标**：
- 主流程响应时间减少50%以上
- 线程池队列使用率 < 80%
- 异步任务成功率 > 99%

```java
/**
 * ✅ 线程池配置（若依框架已内置）
 */
@Configuration
public class AsyncConfig {
    
    /**
     * 核心线程池：处理操作日志
     */
    @Bean("taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(200);
        executor.setKeepAliveSeconds(60);
        executor.setThreadNamePrefix("async-log-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
    
    /**
     * 邮件发送线程池
     */
    @Bean("mailExecutor")
    public Executor mailExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-mail-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.AbortPolicy());
        executor.initialize();
        return executor;
    }
}

@Service
@Slf4j
public class AsyncService {

    /**
     * ✅ 示例1：异步记录操作日志
     */
    @Async("taskExecutor")
    public void recordOperLogAsync(SysOperLog operLog) {
        try {
            operLogMapper.insertOperlog(operLog);
            log.info("操作日志记录成功: {}", operLog.getTitle());
        } catch (Exception e) {
            // 异步任务失败不影响主流程，仅记录错误日志
            log.error("异步记录操作日志失败: {}", operLog.getTitle(), e);
        }
    }

    /**
     * ✅ 示例2：异步发送邮件（显式传递上下文）
     */
    @Async("mailExecutor")
    public void sendEmailAsync(String to, String subject, String content, Long userId) {
        try {
            // 注意：异步任务中无法获取SecurityContextHolder，需显式传递userId
            mailService.sendHtmlMail(to, subject, content);
            log.info("邮件发送成功: {} -> {}", userId, to);
        } catch (Exception e) {
            log.error("邮件发送失败: {} -> {}", userId, to, e);
            // 可以记录到失败队列，稍后重试
            failedMailQueue.add(new MailTask(to, subject, content));
        }
    }

    /**
     * ✅ 示例3：异步更新统计数据
     */
    @Async("taskExecutor")
    public void updateStatisticsAsync(Long businessId, String businessType) {
        try {
            // 统计数据更新不影响主流程
            statisticsMapper.increaseCount(businessId, businessType);
        } catch (Exception e) {
            log.error("更新统计数据失败: businessId={}, type={}", businessId, businessType, e);
        }
    }

    /**
     * ✅ 示例4：有返回值的异步任务
     */
    @Async("taskExecutor")
    public CompletableFuture<List<String>> processDataAsync(List<Long> ids) {
        try {
            List<String> result = ids.stream()
                .map(this::processItem)
                .collect(Collectors.toList());
            return CompletableFuture.completedFuture(result);
        } catch (Exception e) {
            log.error("异步处理数据失败", e);
            return CompletableFuture.failedFuture(e);
        }
    }

    /**
     * ❌ 错误示例1：异步任务未捕获异常
     */
    @Async("taskExecutor")
    public void badAsyncNoExceptionHandle(SysOperLog operLog) {
        // 问题：如果插入失败，异常会被吞掉，无法追踪
        operLogMapper.insertOperlog(operLog);
    }

    /**
     * ❌ 错误示例2：主流程等待异步结果
     */
    public String badAsyncWait() throws Exception {
        // 问题：违背了异步设计初衷，主线程被阻塞
        CompletableFuture<String> future = processDataAsync(Arrays.asList(1L, 2L, 3L));
        return future.get(); // 阻塞等待
    }
}

/**
 * ✅ 示例5：批量异步任务协调
 */
@Service
public class BatchAsyncService {
    
    @Autowired
    private AsyncService asyncService;
    
    public void batchSendNotifications(List<Long> userIds) {
        // 拆分批次，避免线程池堆积
        int batchSize = 100;
        Lists.partition(userIds, batchSize).forEach(batch -> {
            batch.forEach(userId -> {
                // 每个用户的通知独立异步发送
                asyncService.sendNotificationAsync(userId);
            });
            
            // 批次间延迟，避免瞬时压力
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
    }
}
```

**线程池监控示例**：
```java
@Component
@Slf4j
public class ThreadPoolMonitor {
    
    @Autowired
    @Qualifier("taskExecutor")
    private ThreadPoolTaskExecutor taskExecutor;
    
    @Scheduled(cron = "0 */5 * * * ?") // 每5分钟检查一次
    public void monitorThreadPool() {
        ThreadPoolExecutor executor = taskExecutor.getThreadPoolExecutor();
        
        int activeCount = executor.getActiveCount();
        int poolSize = executor.getPoolSize();
        long completedTaskCount = executor.getCompletedTaskCount();
        int queueSize = executor.getQueue().size();
        
        log.info("线程池状态 - 活跃线程:{}/{}, 队列大小:{}, 完成任务数:{}", 
            activeCount, poolSize, queueSize, completedTaskCount);
        
        // 告警：队列超过80%
        if (queueSize > 160) {
            log.warn("线程池队列堆积严重！当前队列:{}/200", queueSize);
        }
    }
}
```

### 规范4：前端性能优化

**适用场景**：页面加载慢、表格渲染卡顿、大列表滚动不流畅

**核心原则**：
1. **虚拟滚动**：超过100条数据的列表必须使用虚拟滚动（vxe-table/vue-virtual-scroller）
2. **分页加载**：优先使用后端分页，避免前端一次性加载大量数据
3. **懒加载**：图片、组件按需加载,减少首屏加载时间
4. **防抖节流**：输入搜索、滚动事件等必须使用防抖或节流
5. **打包优化**：代码分割、Tree Shaking、Gzip压缩

**性能指标**：
- 首屏加载时间 < 3秒
- 列表渲染1000条数据 < 500ms
- 页面交互响应时间 < 100ms

```vue
<!-- ✅ 示例1：虚拟滚动表格（vxe-table） -->
<template>
  <vxe-table
    ref="tableRef"
    :data="tableData"
    :scroll-y="{enabled: true, gt: 100}"
    height="600"
    :loading="loading"
  >
    <vxe-column field="userId" title="用户ID" width="100"></vxe-column>
    <vxe-column field="userName" title="用户名" width="150"></vxe-column>
    <vxe-column field="deptName" title="部门" width="200"></vxe-column>
  </vxe-table>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const tableRef = ref()
const tableData = ref([])
const loading = ref(false)

// ✅ 正确：后端分页 + 虚拟滚动
const loadData = async (pageNum = 1, pageSize = 50) => {
  loading.value = true
  try {
    const res = await listUser({ pageNum, pageSize })
    tableData.value = res.rows
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<!-- ❌ 错误示例：一次性渲染大量数据 -->
<template>
  <el-table :data="allUsers">
    <!-- 问题：10000条数据一次性渲染，页面卡死 -->
    <el-table-column prop="userName" label="用户名"></el-table-column>
  </el-table>
</template>
```

```vue
<!-- ✅ 示例2：搜索防抖 -->
<template>
  <el-input
    v-model="queryParams.userName"
    placeholder="请输入用户名"
    @input="debounceSearch"
  />
</template>

<script setup>
import { ref } from 'vue'
import { useDebounceFn } from '@vueuse/core'

const queryParams = ref({ userName: '' })

// 防抖：300ms内多次输入只执行最后一次
const debounceSearch = useDebounceFn(() => {
  getList()
}, 300)

const getList = async () => {
  const res = await listUser(queryParams.value)
  // 处理数据...
}
</script>
```

```javascript
// ✅ 示例3：图片懒加载
// main.js
import VueLazyload from 'vue-lazyload'

app.use(VueLazyload, {
  preLoad: 1.3,
  error: 'error.png',
  loading: 'loading.gif',
  attempt: 1
})

// 组件中使用
<img v-lazy="user.avatar" alt="头像" />
```

```javascript
// ✅ 示例4：路由懒加载
// router/index.js
const routes = [
  {
    path: '/system/user',
    component: () => import('@/views/system/user/index.vue'), // 懒加载
    meta: { title: '用户管理' }
  }
]
```

```javascript
// ✅ 示例5：长列表优化（IntersectionObserver无限滚动）
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const list = ref([])
const pageNum = ref(1)
const loading = ref(false)
const noMore = ref(false)
const observerRef = ref()

const loadMore = async () => {
  if (loading.value || noMore.value) return
  
  loading.value = true
  try {
    const res = await listData({ pageNum: pageNum.value, pageSize: 20 })
    list.value.push(...res.rows)
    
    if (res.rows.length < 20) {
      noMore.value = true
    } else {
      pageNum.value++
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // 监听底部元素，触发加载更多
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      loadMore()
    }
  })
  
  observer.observe(observerRef.value)
})
</script>

<template>
  <div>
    <div v-for="item in list" :key="item.id">{{ item.name }}</div>
    <div ref="observerRef" class="loading">{{ loading ? '加载中...' : noMore ? '没有更多了' : '' }}</div>
  </div>
</template>
```

```javascript
// ✅ 示例6：打包优化配置（vite.config.js）
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // 代码分割
        manualChunks: {
          'element-plus': ['element-plus'],
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'utils': ['lodash-es', 'dayjs']
        }
      }
    },
    // 启用Gzip压缩
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
})
```

## 禁止事项

### 数据库层面
- ❌ **禁止在循环中执行SQL查询**：必须改为批量查询（`selectBatchIds`、`selectList`）
- ❌ **禁止使用`SELECT *`查询大表**：必须通过`select()`方法指定必要字段
- ❌ **禁止在索引字段上使用函数**：如`WHERE DATE(create_time) = '2023-10-01'`，会导致索引失效，应改为`WHERE create_time >= '2023-10-01 00:00:00' AND create_time < '2023-10-02 00:00:00'`
- ❌ **禁止使用前缀模糊查询**：如`WHERE name LIKE '%张三'`会导致索引失效，只能使用`LIKE '张三%'`
- ❌ **禁止在高并发表上使用`COUNT(*)`**：应使用Redis计数器或预计算
- ❌ **禁止深分页查询**：如`LIMIT 10000, 20`，应使用游标分页或`WHERE id > ?`

### 缓存层面
- ❌ **禁止缓存大对象**：单个缓存值超过10KB或列表超过1000条，会导致序列化开销大、网络传输慢
- ❌ **禁止永久缓存**：未设置TTL会导致内存泄漏和数据不一致
- ❌ **禁止忽略缓存穿透/击穿/雪崩防护**：
  - 缓存穿透：恶意查询不存在的数据，应使用空值缓存或布隆过滤器
  - 缓存击穿：热点数据过期瞬间大量请求打到数据库，应使用互斥锁
  - 缓存雪崩：大量缓存同时过期，应设置随机TTL
- ❌ **禁止在缓存中存储敏感信息**：如明文密码、身份证号等，应加密存储
- ❌ **禁止缓存未序列化的对象**：会导致类加载器问题，必须使用可序列化对象

### 异步处理层面
- ❌ **禁止在异步任务中不捕获异常**：异常会被吞掉，无法追踪，必须try-catch并记录日志
- ❌ **禁止在主流程中等待异步结果**：如`future.get()`，违背异步设计初衷
- ❌ **禁止异步任务无限堆积**：应设置队列大小限制和拒绝策略
- ❌ **禁止在异步任务中直接使用ThreadLocal**：如SecurityContextHolder，需显式传递上下文
- ❌ **禁止所有异步任务共用一个线程池**：应根据业务隔离线程池，避免相互影响

### 前端层面
- ❌ **禁止一次性渲染超过100条数据**：必须使用虚拟滚动或分页
- ❌ **禁止频繁操作DOM**：如在循环中多次`appendChild`，应使用DocumentFragment或虚拟DOM
- ❌ **禁止在输入框事件中不使用防抖**：如实时搜索，会导致请求过多
- ❌ **禁止同步加载所有路由组件**：必须使用路由懒加载
- ❌ **禁止图片不压缩直接上传**：应前端压缩后再上传，或使用CDN裁剪

## 诊断工具与方法

### SQL性能诊断
```sql
-- 1. 查看慢SQL日志（MySQL）
SHOW VARIABLES LIKE 'slow_query%';
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2; -- 超过2秒的查询记录

-- 2. 分析SQL执行计划
EXPLAIN SELECT * FROM sys_user WHERE status = '0' AND dept_id = 100;

-- 3. 查看索引使用情况
SHOW INDEX FROM sys_user;

-- 4. 分析表统计信息
ANALYZE TABLE sys_user;

-- 5. 查看当前执行的SQL
SHOW FULL PROCESSLIST;
```

### Redis性能诊断
```bash
# 1. 查看Redis内存使用
redis-cli INFO memory

# 2. 查看慢查询日志
redis-cli SLOWLOG GET 10

# 3. 查看键的内存占用
redis-cli --bigkeys

# 4. 监控实时命令
redis-cli MONITOR

# 5. 查看缓存命中率
redis-cli INFO stats | grep keyspace
```

### 应用性能诊断
```java
/**
 * ✅ 使用Spring AOP记录接口耗时
 */
@Aspect
@Component
@Slf4j
public class PerformanceAspect {
    
    @Around("@annotation(com.ruoyi.common.annotation.PerformanceLog)")
    public Object logPerformance(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();
        String methodName = joinPoint.getSignature().toShortString();
        
        try {
            Object result = joinPoint.proceed();
            long cost = System.currentTimeMillis() - startTime;
            
            if (cost > 1000) {
                log.warn("⚠️ 慢接口 [{}] 耗时: {}ms", methodName, cost);
            } else {
                log.info("接口 [{}] 耗时: {}ms", methodName, cost);
            }
            
            return result;
        } catch (Throwable e) {
            long cost = System.currentTimeMillis() - startTime;
            log.error("接口 [{}] 执行失败，耗时: {}ms", methodName, cost, e);
            throw e;
        }
    }
}
```

## 参考代码
若依框架中已包含的性能优化相关代码：
- **Redis工具类**：`ruoyi-common/src/main/java/com/ruoyi/common/utils/redis/RedisUtils.java`
- **异步配置**：`ruoyi-framework/src/main/java/com/ruoyi/framework/config/AsyncConfig.java`
- **用户服务实现**：`ruoyi-system/src/main/java/com/ruoyi/system/service/impl/SysUserServiceImpl.java`
- **MyBatis-Plus配置**：`ruoyi-framework/src/main/java/com/ruoyi/framework/config/MybatisPlusConfig.java`
- **线程池配置**：`ruoyi-framework/src/main/java/com/ruoyi/framework/config/ThreadPoolConfig.java`

## 优化效果评估标准

### 数据库优化效果
| 指标 | 优化前 | 优化后 | 提升幅度 |
|------|--------|--------|----------|
| 单次查询耗时 | 500ms | <100ms | 80%↑ |
| N+1查询次数 | 100次 | 1次 | 99%↓ |
| 数据库CPU使用率 | 90% | <50% | 44%↓ |
| 慢SQL数量 | 50条/天 | <5条/天 | 90%↓ |

### 缓存优化效果
| 指标 | 优化前 | 优化后 | 提升幅度 |
|------|--------|--------|----------|
| 接口响应时间 | 800ms | <100ms | 87%↑ |
| 缓存命中率 | 50% | >90% | 80%↑ |
| Redis内存占用 | 8GB | 2GB | 75%↓ |
| 数据库QPS | 5000 | 500 | 90%↓ |

### 异步优化效果
| 指标 | 优化前 | 优化后 | 提升幅度 |
|------|--------|--------|----------|
| 接口响应时间 | 2000ms | 200ms | 90%↑ |
| 用户体验延迟 | 明显 | 无感知 | - |
| 线程阻塞率 | 40% | <10% | 75%↓ |

### 前端优化效果
| 指标 | 优化前 | 优化后 | 提升幅度 |
|------|--------|--------|----------|
| 首屏加载时间 | 8s | <3s | 62%↑ |
| 列表渲染时间 | 3s | <500ms | 83%↑ |
| 页面交互响应 | 500ms | <100ms | 80%↑ |

## 性能优化检查清单

### 数据库查询优化
- [ ] **消除N+1查询**：是否将循环查询改为批量查询（`selectBatchIds`/`selectList`）
- [ ] **字段裁剪**：是否避免了`SELECT *`，仅查询必要字段
- [ ] **索引优化**：是否为高频查询条件（WHERE）、关联字段（JOIN）、排序字段（ORDER BY）建立索引
- [ ] **索引失效检查**：是否避免了在索引字段上使用函数、类型转换、前缀模糊查询
- [ ] **分页优化**：是否对大数据量查询使用分页，避免深分页
- [ ] **执行计划分析**：是否使用`EXPLAIN`检查SQL执行计划，确保使用索引
- [ ] **关联查询优化**：是否将多表关联查询拆分为多次批量查询

### Redis缓存优化
- [ ] **热点数据缓存**：是否对字典、配置、权限等高频数据进行缓存
- [ ] **TTL设置**：是否为所有缓存设置合理的过期时间
- [ ] **缓存穿透防护**：是否实现了空值缓存或布隆过滤器
- [ ] **缓存击穿防护**：是否对热点数据使用互斥锁防止击穿
- [ ] **缓存雪崩防护**：是否为缓存设置随机过期时间
- [ ] **容量控制**：是否避免了大对象缓存（单个值<10KB，列表<1000条）
- [ ] **缓存更新**：数据变更时是否及时删除或更新缓存
- [ ] **命中率监控**：是否监控缓存命中率并设置告警

### 异步处理优化
- [ ] **异步化非核心操作**：是否将日志、邮件、统计等耗时操作异步化
- [ ] **线程池隔离**：是否为不同业务使用独立线程池
- [ ] **异常处理**：异步任务是否捕获异常并记录日志
- [ ] **上下文传递**：是否显式传递用户、租户等上下文信息
- [ ] **队列监控**：是否监控线程池队列使用率并设置告警
- [ ] **拒绝策略**：是否设置合理的拒绝策略（CallerRunsPolicy/AbortPolicy）

### 前端性能优化
- [ ] **虚拟滚动**：是否对超过100条的列表使用虚拟滚动
- [ ] **分页加载**：是否使用后端分页，避免一次性加载大量数据
- [ ] **图片懒加载**：是否对图片使用懒加载
- [ ] **路由懒加载**：是否对路由组件使用懒加载
- [ ] **防抖节流**：是否对搜索、滚动等高频事件使用防抖或节流
- [ ] **代码分割**：是否合理配置代码分割和打包优化
- [ ] **资源压缩**：是否启用Gzip压缩和图片压缩

### 监控与告警
- [ ] **慢SQL监控**：是否开启慢SQL日志并设置告警
- [ ] **接口耗时监控**：是否监控接口响应时间并设置告警
- [ ] **Redis监控**：是否监控Redis内存、命中率、慢查询
- [ ] **线程池监控**：是否监控线程池队列、活跃线程数
- [ ] **错误日志监控**：是否监控异常日志并及时处理

## 常见性能问题诊断流程

### 问题1：接口响应慢
1. **查看日志**：确认耗时环节（数据库查询、外部接口调用、复杂计算）
2. **分析SQL**：使用`EXPLAIN`查看执行计划，检查是否使用索引
3. **检查缓存**：确认是否可以缓存，检查缓存命中率
4. **优化方案**：
   - 数据库优化：添加索引、批量查询、字段裁剪
   - 缓存优化：添加缓存、提高命中率
   - 异步优化：非核心操作异步化

### 问题2：数据库CPU高
1. **查看慢SQL**：`SHOW FULL PROCESSLIST`查看正在执行的SQL
2. **分析慢查询日志**：找出执行频繁且耗时的SQL
3. **检查索引**：确认是否有索引失效、缺失索引
4. **优化方案**：
   - 添加缺失索引
   - 优化慢SQL（减少关联表、使用覆盖索引）
   - 使用缓存减少数据库压力

### 问题3：页面卡顿
1. **检查数据量**：确认是否一次性渲染大量数据
2. **分析渲染耗时**：使用浏览器Performance工具分析
3. **检查DOM操作**：确认是否有频繁的DOM操作
4. **优化方案**：
   - 使用虚拟滚动或分页
   - 使用防抖节流减少渲染次数
   - 优化组件渲染逻辑

### 问题4：Redis内存占用高
1. **查看大键**：`redis-cli --bigkeys`找出占用内存大的键
2. **检查过期时间**：确认是否有永久缓存
3. **分析键类型**：确认是否缓存了不必要的大对象
4. **优化方案**：
   - 删除不必要的缓存
   - 设置合理的TTL
   - 拆分大对象为小对象

### 问题5：线程池队列堆积
1. **查看线程池状态**：监控活跃线程数、队列大小
2. **分析任务耗时**：确认是否有长耗时任务阻塞
3. **检查拒绝策略**：确认拒绝策略是否合理
4. **优化方案**：
   - 增加核心线程数或队列大小
   - 优化任务执行逻辑，减少耗时
   - 拆分任务，使用多个线程池隔离

## 性能优化最佳实践

### 数据库层
1. **查询优先级**：缓存 > 批量查询 > 单次查询
2. **索引设计**：联合索引遵循最左前缀原则
3. **数据分离**：冷热数据分离，历史数据归档
4. **读写分离**：读多写少场景使用主从架构

### 缓存层
1. **缓存策略**：Cache-Aside（旁路缓存）模式
2. **缓存粒度**：根据业务场景选择合适粒度（整体缓存 vs 字段缓存）
3. **多级缓存**：本地缓存（Caffeine） + 分布式缓存（Redis）
4. **缓存预热**：系统启动时预加载热点数据

### 异步层
1. **任务分类**：核心任务（同步）vs 非核心任务（异步）
2. **线程池设计**：IO密集型（线程数 = CPU核数 * 2），CPU密集型（线程数 = CPU核数 + 1）
3. **降级方案**：异步任务失败后的降级处理
4. **重试机制**：失败任务的重试策略

### 前端层
1. **首屏优化**：关键资源优先加载，非关键资源延迟加载
2. **渲染优化**：减少重排重绘，使用虚拟DOM
3. **网络优化**：HTTP/2、CDN、资源预加载
4. **体验优化**：骨架屏、Loading状态、乐观更新

## 总结
性能优化是一个持续的过程，需要：
1. **事前预防**：在开发阶段遵循性能规范，避免引入性能问题
2. **事中监控**：建立完善的监控体系，及时发现性能瓶颈
3. **事后优化**：针对性能问题进行根因分析和针对性优化
4. **持续改进**：定期Review性能指标，不断优化改进

遵循本规范，可以显著提升系统性能，改善用户体验。