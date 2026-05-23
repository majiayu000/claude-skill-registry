---
name: ai-langchain4j
description: |
  基于若依-vue-plus框架的LangChain4j AI大模型集成标准规范。全面规范模型配置管理、类型安全服务定义、RAG（检索增强生成）实现、流式响应处理及安全性保障。
  
  触发场景：
  - 开发智能客服系统、文档问答助手、代码生成工具
  - 集成LLM大模型接口（OpenAI、智谱AI、通义千问等）
  - 实现知识库问答、文档检索、语义搜索功能
  - 开发需要流式响应的AI交互界面
  - 构建RAG（检索增强生成）应用
  
  触发词：AI集成、LangChain4j、大模型、RAG、流式输出、智谱AI、通义千问、OpenAI、向量检索、嵌入模型、Prompt工程
---

# AI 大模型集成规范

> 本规范基于LangChain4j框架，为若依-vue-plus项目定义统一的AI大模型集成标准。确保代码的可维护性、安全性和扩展性。

## 核心规范

### 规范1：模型配置与类型安全服务

**目标**：实现模型配置的集中管理和类型安全的AI服务定义。

**详细说明**：
1. **配置管理**：使用`ChatLanguageModel`构建器配置大模型，严禁在代码中硬编码API Key
2. **配置来源**：API Key必须从配置中心（如Nacos）或`application.yml`读取
3. **接口定义**：推荐使用LangChain4j的`AiServices`接口定义模式，将系统提示词（System Message）与业务逻辑解耦
4. **动态参数**：模型参数（temperature、topK、maxTokens等）应支持动态配置
5. **多模型支持**：设计时应考虑多模型切换能力（智谱AI、通义千问、OpenAI等）

**实现要点**：
- 使用`@ConfigurationProperties`绑定配置
- 通过工厂模式支持多模型动态切换
- 提供模型健康检查接口

```java
// ============ 配置属性类 ============
@Data
@Component
@ConfigurationProperties(prefix = "ai.model")
public class AiProperties {
    private String provider; // openai/zhipu/qwen
    private String baseUrl;
    private String apiKey;
    private String modelName;
    private Double temperature = 0.7;
    private Integer maxTokens = 2000;
    private Integer timeout = 60; // 秒
}

// ============ 配置类：动态初始化模型 ============
@Configuration
@EnableConfigurationProperties(AiProperties.class)
public class LangChain4jConfig {
    
    @Bean
    public ChatLanguageModel chatLanguageModel(AiProperties properties) {
        // 根据provider动态选择模型
        return switch (properties.getProvider()) {
            case "openai" -> OpenAiChatModel.builder()
                    .baseUrl(properties.getBaseUrl())
                    .apiKey(properties.getApiKey())
                    .modelName(properties.getModelName())
                    .temperature(properties.getTemperature())
                    .maxTokens(properties.getMaxTokens())
                    .timeout(Duration.ofSeconds(properties.getTimeout()))
                    .logRequests(true)
                    .logResponses(true)
                    .build();
            case "zhipu" -> ZhipuAiChatModel.builder()
                    .apiKey(properties.getApiKey())
                    .modelName(properties.getModelName())
                    .temperature(properties.getTemperature())
                    .build();
            // 其他模型...
            default -> throw new IllegalArgumentException("不支持的模型提供商: " + properties.getProvider());
        };
    }
    
    // 流式模型配置
    @Bean
    public StreamingChatLanguageModel streamingChatLanguageModel(AiProperties properties) {
        return OpenAiStreamingChatModel.builder()
                .baseUrl(properties.getBaseUrl())
                .apiKey(properties.getApiKey())
                .modelName(properties.getModelName())
                .temperature(properties.getTemperature())
                .build();
    }
}

// ============ 定义类型安全的AI服务接口 ============
public interface AiAssistant {
    
    /**
     * 通用对话接口
     * @param userMessage 用户消息
     * @return AI响应
     */
    @SystemMessage("""
        你是一个专业的若依框架助手。
        - 回答必须简洁、准确、专业
        - 使用Java代码示例时，遵循阿里巴巴Java开发规范
        - 涉及若依框架时，优先使用框架提供的工具类
        """)
    String chat(@UserMessage String userMessage);
    
    /**
     * 实体提取接口
     * @param text 待提取文本
     * @return JSON格式的实体列表
     */
    @SystemMessage("""
        提取以下文本中的关键实体（人名、地名、组织、时间等）。
        返回格式：{"entities": [{"type": "人名", "value": "张三"}]}
        """)
    String extractEntities(@UserMessage String text);
    
    /**
     * 代码审查接口
     * @param code 待审查的代码
     * @return 审查建议
     */
    @SystemMessage("""
        你是一个资深Java代码审查专家。
        审查以下代码，关注：
        1. 代码规范性
        2. 性能问题
        3. 安全隐患
        4. 可维护性
        返回格式化的审查报告。
        """)
    String reviewCode(@UserMessage String code);
}

// ============ 服务实现：通过AiServices自动生成代理 ============
@Service
public class AiAssistantService {
    
    private final AiAssistant aiAssistant;
    
    public AiAssistantService(ChatLanguageModel chatLanguageModel) {
        this.aiAssistant = AiServices.create(AiAssistant.class, chatLanguageModel);
    }
    
    public String chat(String message) {
        return aiAssistant.chat(message);
    }
}
```

### 规范2：RAG检索增强与向量化存储

**目标**：构建高效的知识库问答系统，实现精准的语义检索。

**详细说明**：
1. **向量化**：使用`EmbeddingModel`将文本转换为向量表示
2. **存储选择**：根据规模选择合适的`EmbeddingStore`（内存/Redis/Milvus）
3. **文档切分**：使用`DocumentSplitter`合理切分长文档（推荐500-1000字符/片段）
4. **检索策略**：使用`ContentRetriever`检索相关片段，支持Top-K和相似度阈值
5. **上下文构建**：将检索结果与用户问题组合成完整Prompt

**实现要点**：
- 文档预处理：去除无关字符、统一格式
- 向量索引优化：定期重建索引
- 相似度计算：余弦相似度 > 0.7为相关片段
- 缓存机制：常见问题的检索结果缓存

```java
// ============ RAG配置类 ============
@Configuration
public class RagConfig {
    
    /**
     * 嵌入模型配置
     */
    @Bean
    public EmbeddingModel embeddingModel(AiProperties properties) {
        return OpenAiEmbeddingModel.builder()
                .baseUrl(properties.getBaseUrl())
                .apiKey(properties.getApiKey())
                .modelName("text-embedding-ada-002") // 或使用国产模型
                .build();
    }
    
    /**
     * 向量存储（示例：内存存储，生产环境建议使用Redis/Milvus）
     */
    @Bean
    public EmbeddingStore<TextSegment> embeddingStore() {
        return new InMemoryEmbeddingStore<>();
    }
    
    /**
     * 文档切分器
     */
    @Bean
    public DocumentSplitter documentSplitter() {
        return DocumentSplitters.recursive(
            500,    // 每个片段最大字符数
            100,    // 片段间重叠字符数（保持上下文连贯）
            new OpenAiTokenizer() // Token计数器
        );
    }
}

// ============ RAG服务实现 ============
@Service
@Slf4j
public class AiRagService {

    private final StreamingChatLanguageModel streamingModel;
    private final EmbeddingModel embeddingModel;
    private final EmbeddingStore<TextSegment> embeddingStore;
    private final ContentRetriever contentRetriever;

    public AiRagService(StreamingChatLanguageModel streamingModel,
                        EmbeddingModel embeddingModel,
                        EmbeddingStore<TextSegment> embeddingStore) {
        this.streamingModel = streamingModel;
        this.embeddingModel = embeddingModel;
        this.embeddingStore = embeddingStore;
        
        // 构建检索器：Top-3相关片段，相似度阈值0.7
        this.contentRetriever = EmbeddingStoreContentRetriever.builder()
                .embeddingStore(embeddingStore)
                .embeddingModel(embeddingModel)
                .maxResults(3)
                .minScore(0.7)
                .build();
    }

    /**
     * 导入文档到知识库
     * @param filePath 文档路径
     */
    public void ingestDocument(String filePath) {
        try {
            // 1. 加载文档
            Document document = FileSystemDocumentLoader.loadDocument(filePath);
            
            // 2. 切分文档
            DocumentSplitter splitter = DocumentSplitters.recursive(500, 100);
            List<TextSegment> segments = splitter.split(document);
            
            // 3. 向量化并存储
            List<Embedding> embeddings = embeddingModel.embedAll(segments).content();
            embeddingStore.addAll(embeddings, segments);
            
            log.info("成功导入文档: {}, 切分为{}个片段", filePath, segments.size());
        } catch (Exception e) {
            log.error("文档导入失败: {}", filePath, e);
            throw new BusinessException("文档导入失败");
        }
    }

    /**
     * 流式问答 + RAG
     * @param query 用户问题
     * @return 流式响应
     */
    public Flux<String> streamChatWithRag(String query) {
        // 1. 检索相关上下文
        List<Content> relevantContents = contentRetriever.retrieve(Query.from(query));
        
        // 2. 构建包含上下文的Prompt
        String context = relevantContents.stream()
                .map(Content::textSegment)
                .map(TextSegment::text)
                .collect(Collectors.joining("\n\n"));
        
        String enhancedPrompt = String.format("""
            基于以下知识库内容回答用户问题：
            
            【知识库内容】
            %s
            
            【用户问题】
            %s
            
            【要求】
            - 优先使用知识库内容回答
            - 如果知识库无相关内容，明确告知用户
            - 回答要准确、简洁、专业
            """, context, query);
        
        // 3. 流式调用模型
        return Flux.create(sink -> {
            streamingModel.generate(enhancedPrompt, new StreamingResponseHandler<AiMessage>() {
                @Override
                public void onNext(String token) {
                    sink.next(token);
                }
                
                @Override
                public void onComplete(Response<AiMessage> response) {
                    sink.complete();
                    log.info("流式响应完成，Token使用: {}", response.tokenUsage());
                }
                
                @Override
                public void onError(Throwable error) {
                    log.error("流式响应错误", error);
                    sink.error(error);
                }
            });
        });
    }
    
    /**
     * 普通问答（非流式）
     */
    public String chatWithRag(String query) {
        List<Content> relevantContents = contentRetriever.retrieve(Query.from(query));
        
        String context = relevantContents.stream()
                .map(Content::textSegment)
                .map(TextSegment::text)
                .collect(Collectors.joining("\n\n"));
        
        Prompt prompt = Prompt.from(
            SystemMessage.from("你是知识库问答助手，基于提供的上下文回答问题"),
            UserMessage.from("上下文：\n" + context + "\n\n问题：" + query)
        );
        
        Response<AiMessage> response = chatLanguageModel.generate(prompt);
        return response.content().text();
    }
}

// ============ Controller层：SSE流式响应 ============
@RestController
@RequestMapping("/ai/chat")
@Slf4j
public class AiChatController {
    
    @Resource
    private AiRagService aiRagService;
    
    /**
     * 流式问答接口（SSE）
     */
    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<String>> streamChat(@RequestParam String query) {
        return aiRagService.streamChatWithRag(query)
                .map(token -> ServerSentEvent.<String>builder()
                        .data(token)
                        .build())
                .doOnComplete(() -> log.info("流式响应完成: {}", query))
                .doOnError(e -> log.error("流式响应异常", e));
    }
    
    /**
     * 普通问答接口
     */
    @PostMapping("/ask")
    public R<String> ask(@RequestBody AiChatRequest request) {
        String answer = aiRagService.chatWithRag(request.getQuery());
        return R.ok(answer);
    }
}
```

### 规范3：流式响应处理

**目标**：优化用户体验，避免长时间等待。

**详细说明**：
1. **场景判断**：超过3秒的推理请求必须使用流式响应
2. **技术选型**：Web端使用SSE（Server-Sent Events），WebSocket适用于双向通信场景
3. **错误处理**：流式过程中的异常必须优雅处理并通知前端
4. **超时控制**：设置合理的超时时间（推荐60秒）
5. **取消机制**：支持用户主动取消正在进行的流式响应

**前端对接示例**：

```javascript
// Vue3 + EventSource 接收SSE流式响应
const streamChat = async (query) => {
  const eventSource = new EventSource(`/ai/chat/stream?query=${encodeURIComponent(query)}`);
  
  let fullResponse = '';
  
  eventSource.onmessage = (event) => {
    const token = event.data;
    fullResponse += token;
    // 实时更新UI
    chatMessage.value = fullResponse;
  };
  
  eventSource.onerror = (error) => {
    console.error('流式响应错误:', error);
    eventSource.close();
    ElMessage.error('AI响应异常，请重试');
  };
  
  eventSource.addEventListener('done', () => {
    eventSource.close();
    console.log('流式响应完成');
  });
};
```

### 规范4：Prompt工程最佳实践

**目标**：提升模型输出质量和稳定性。

**详细说明**：
1. **结构化Prompt**：使用明确的分隔符（如【】、===）区分不同部分
2. **角色定义**：在SystemMessage中明确AI的身份和职责
3. **输出格式**：要求模型返回结构化数据时，提供JSON Schema示例
4. **Few-Shot**：复杂任务提供2-3个示例（输入-输出对）
5. **约束条件**：明确禁止事项和输出要求

**Prompt模板示例**：

```java
@SystemMessage("""
    【角色】你是一个资深Java后端开发专家，熟悉Spring Boot和若依框架
    
    【任务】根据用户需求生成符合规范的代码
    
    【要求】
    1. 代码必须遵循阿里巴巴Java开发规范
    2. 使用若依框架提供的BaseController、BaseEntity等基类
    3. 添加详细的中文注释
    4. 包含必要的参数校验和异常处理
    
    【禁止】
    - 不要生成硬编码的配置信息
    - 不要使用已废弃的API
    - 不要省略异常处理代码
    
    【输出格式】
    返回完整的Java类代码，包含package、import和类定义
    """)
String generateCode(@UserMessage String requirement);
```

## 禁止事项

### 安全相关
- ❌ **禁止硬编码API Key**：API Key必须从配置中心或环境变量读取，严禁写入代码或提交到Git
- ❌ **禁止发送敏感数据**：未经脱敏的个人信息、密码、密钥等敏感数据禁止注入Prompt
- ❌ **禁止盲目信任输出**：AI生成的代码、SQL、Shell命令必须人工审核或沙箱验证后才能执行
- ❌ **禁止跳过权限校验**：AI接口必须进行身份认证和权限验证
- ❌ **禁止忽略数据脱敏**：日志记录的Prompt和Response必须脱敏处理

### 性能相关
- ❌ **禁止同步阻塞调用**：超过3秒的推理请求必须使用流式或异步任务机制
- ❌ **禁止无限制并发**：必须使用线程池和限流机制（如Sentinel）控制并发数
- ❌ **禁止忽略Token限制**：前端必须进行输入长度校验，后端必须进行Token计数和截断

### 质量相关
- ❌ **禁止使用不稳定的Prompt**：Prompt必须经过测试验证，避免随意修改导致输出不稳定
- ❌ **禁止缺少错误处理**：所有AI调用必须包含try-catch和超时处理
- ❌ **禁止缺少日志记录**：必须记录请求参数、响应结果、耗时、Token消耗等关键信息
- ❌ **禁止忽略模型切换**：代码应支持多模型动态切换，不能硬绑定特定厂商

### 成本相关
- ❌ **禁止无限制调用**：必须设置用户维度的调用频率限制（如QPM、QPD）
- ❌ **禁止忽略成本监控**：必须记录Token消耗并进行成本统计和告警
- ❌ **禁止滥用高级模型**：简单任务应使用便宜的模型，复杂任务再使用高级模型

## 实施指南

### 快速开始
1. **添加依赖**（pom.xml）
```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-spring-boot-starter</artifactId>
    <version>0.35.0</version>
</dependency>
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai</artifactId>
    <version>0.35.0</version>
</dependency>
<!-- RAG相关依赖 -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-embeddings</artifactId>
    <version>0.35.0</version>
</dependency>
```

2. **配置文件**（application.yml）
```yaml
ai:
  model:
    provider: openai  # 可选：openai/zhipu/qwen
    base-url: https://api.openai.com/v1
    api-key: ${AI_API_KEY}  # 从环境变量读取
    model-name: gpt-4o-mini
    temperature: 0.7
    max-tokens: 2000
    timeout: 60
```

3. **初始化配置类**：参考"规范1"中的`LangChain4jConfig`

4. **定义AI服务接口**：参考"规范1"中的`AiAssistant`

5. **实现业务逻辑**：参考"规范2"中的`AiRagService`

### 典型应用场景

#### 场景1：智能客服机器人
- 导入产品文档、FAQ到知识库
- 使用RAG检索相关答案
- 流式输出提升用户体验

#### 场景2：代码生成助手
- 定义代码生成AI服务接口
- 提供详细的Prompt模板
- 生成符合项目规范的代码

#### 场景3：文档智能问答
- 上传PDF/Word文档
- 自动切分并向量化
- 支持自然语言查询

#### 场景4：数据分析助手
- 将数据库Schema注入Prompt
- 生成SQL查询语句
- 解释查询结果（需人工审核SQL）

## 参考代码

### 项目结构
```
ruoyi-ai/
├── config/
│   ├── LangChain4jConfig.java          # 模型配置
│   ├── RagConfig.java                   # RAG配置
│   └── AiProperties.java                # 配置属性类
├── service/
│   ├── AiAssistant.java                 # AI服务接口定义
│   ├── AiAssistantService.java          # 通用对话服务
│   ├── AiRagService.java                # RAG服务
│   └── AiCodeGeneratorService.java      # 代码生成服务
├── controller/
│   ├── AiChatController.java            # 对话接口
│   └── AiKnowledgeController.java       # 知识库管理接口
└── domain/
    ├── dto/
    │   ├── AiChatRequest.java
    │   └── AiChatResponse.java
    └── vo/
        └── TokenUsageVO.java
```

### 关键文件路径
- 核心配置：`ruoyi-ai/src/main/java/com/ruoyi/ai/config/LangChain4jConfig.java`
- RAG服务：`ruoyi-ai/src/main/java/com/ruoyi/ai/service/AiRagService.java`
- 流式接口：`ruoyi-ai/src/main/java/com/ruoyi/ai/controller/AiChatController.java`
- 前端组件：`ruoyi-ui/src/views/ai/chat/index.vue`（SSE流式接收示例）
- 配置文件：`ruoyi-ai/src/main/resources/application-ai.yml`

## 检查清单

### 开发阶段
- [ ] **配置管理**
  - [ ] API Key从配置中心或环境变量读取
  - [ ] 支持多模型动态切换（至少2个提供商）
  - [ ] 模型参数可配置（temperature、maxTokens等）
  - [ ] 配置了合理的超时时间（推荐60秒）

- [ ] **服务定义**
  - [ ] 使用AiServices接口定义模式
  - [ ] SystemMessage与业务逻辑解耦
  - [ ] Prompt结构化且经过测试验证
  - [ ] 包含清晰的角色、任务、要求、禁止项

- [ ] **RAG实现**（如果需要）
  - [ ] 正确配置EmbeddingModel
  - [ ] 选择合适的EmbeddingStore（内存/Redis/Milvus）
  - [ ] 文档切分大小合理（500-1000字符）
  - [ ] 设置了相似度阈值（推荐>0.7）
  - [ ] 实现了文档导入和更新机制

- [ ] **流式响应**
  - [ ] 超过3秒的请求使用StreamingChatLanguageModel
  - [ ] Controller正确处理Flux/SseEmitter
  - [ ] 前端正确接收SSE流式数据
  - [ ] 实现了错误处理和超时机制
  - [ ] 支持用户取消正在进行的请求

### 安全阶段
- [ ] **数据安全**
  - [ ] 敏感数据已脱敏处理
  - [ ] 日志中的Prompt和Response已脱敏
  - [ ] API Key未硬编码或提交到Git
  - [ ] 实现了接口权限校验

- [ ] **输出安全**
  - [ ] AI生成的代码/SQL需人工审核
  - [ ] 实现了输出内容过滤机制
  - [ ] 不直接执行AI生成的命令

### 性能阶段
- [ ] **并发控制**
  - [ ] 配置了线程池管理AI请求
  - [ ] 实现了限流机制（Sentinel/RateLimiter）
  - [ ] 设置了用户维度的QPM/QPD限制

- [ ] **成本控制**
  - [ ] 前端进行输入长度校验
  - [ ] 后端进行Token计数和截断
  - [ ] 记录Token消耗并统计
  - [ ] 设置了成本告警阈值

- [ ] **缓存优化**
  - [ ] 常见问题使用缓存（Redis）
  - [ ] RAG检索结果合理缓存
  - [ ] 模型响应缓存（相同问题）

### 质量阶段
- [ ] **错误处理**
  - [ ] 所有AI调用包含try-catch
  - [ ] 超时异常有明确提示
  - [ ] 流式响应错误优雅降级

- [ ] **日志记录**
  - [ ] 记录请求参数（脱敏后）
  - [ ] 记录响应结果（脱敏后）
  - [ ] 记录耗时和Token消耗
  - [ ] 记录异常堆栈信息

- [ ] **监控告警**
  - [ ] 接入APM监控（如Skywalking）
  - [ ] 配置响应时间告警
  - [ ] 配置错误率告警
  - [ ] 配置成本异常告警

### 测试阶段
- [ ] **单元测试**
  - [ ] 测试模型配置初始化
  - [ ] 测试AI服务接口调用
  - [ ] 测试RAG检索逻辑
  - [ ] 测试异常处理逻辑

- [ ] **集成测试**
  - [ ] 测试端到端流式响应
  - [ ] 测试不同模型切换
  - [ ] 测试并发场景
  - [ ] 测试超时场景

- [ ] **压力测试**
  - [ ] 测试系统最大QPS
  - [ ] 测试长连接数上限
  - [ ] 测试内存占用情况

## 常见问题

### Q1：如何选择合适的EmbeddingStore？
**A**：
- **开发/测试环境**：使用`InMemoryEmbeddingStore`（简单快速）
- **小规模生产**（<10万条）：使用`RedisEmbeddingStore`（易维护）
- **大规模生产**（>10万条）：使用`MilvusEmbeddingStore`或`PineconeEmbeddingStore`（专业向量数据库）

### Q2：如何优化RAG检索准确率？
**A**：
1. **优化文档切分**：根据文档类型调整切分大小（技术文档500字符，对话数据200字符）
2. **提升检索质量**：调整Top-K（3-5）和相似度阈值（0.7-0.8）
3. **改进Prompt**：在Prompt中明确要求"基于上下文回答，找不到则明确告知"
4. **文档预处理**：去除无关字符、统一格式、补充元数据

### Q3：流式响应如何处理超时？
**A**：
```java
// 在Flux中添加超时控制
return aiRagService.streamChatWithRag(query)
    .timeout(Duration.ofSeconds(60))
    .onErrorResume(TimeoutException.class, e -> 
        Flux.just("响应超时，请稍后重试")
    );
```

### Q4：如何实现多模型成本对比？
**A**：
1. 创建`TokenUsageRecorder`记录每次调用的Token消耗
2. 按模型维度统计总消耗
3. 根据官方定价计算成本：`成本 = (inputTokens * 输入单价 + outputTokens * 输出单价) / 1000`

### Q5：生产环境如何保证API Key安全？
**A**：
1. **本地开发**：使用`.env`文件（已加入`.gitignore`）
2. **测试环境**：使用配置中心（Nacos）加密配置
3. **生产环境**：使用密钥管理服务（如AWS KMS、阿里云KMS）
4. **权限控制**：限制只有运维人员可查看完整Key

## 扩展资源

### 官方文档
- LangChain4j官方文档：https://docs.langchain4j.dev
- Spring AI文档：https://docs.spring.io/spring-ai/reference

### 模型提供商
- OpenAI：https://platform.openai.com/docs
- 智谱AI：https://open.bigmodel.cn/dev/api
- 通义千问：https://help.aliyun.com/zh/dashscope
- Kimi（月之暗面）：https://platform.moonshot.cn/docs

### 向量数据库
- Milvus：https://milvus.io/docs
- Pinecone：https://docs.pinecone.io
- Weaviate：https://weaviate.io/developers/weaviate

---

**版本**：v1.0.0  
**最后更新**：2026-01-26  
**维护者**：AI开发团队