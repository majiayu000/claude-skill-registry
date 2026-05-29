# 日志监控技能

## 触发条件
- 关键词：日志、监控、logging、log、告警、metrics、追踪
- 场景：当用户需要配置日志或监控系统时

## 核心规范

### 规范1：日志配置

```python
# app/core/logger.py
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime

def setup_logger(
    name: str = "app",
    level: str = "INFO",
    log_dir: str = "logs"
) -> logging.Logger:
    """配置日志器"""
    
    # 创建日志目录
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 日志格式
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（按大小轮转）
    file_handler = RotatingFileHandler(
        filename=f"{log_dir}/app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 错误日志单独文件
    error_handler = RotatingFileHandler(
        filename=f"{log_dir}/error.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger

# 使用
logger = setup_logger()
```

### 规范2：结构化日志

```python
import json
import logging
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """JSON 格式日志"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # 添加额外字段
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)
        
        # 添加异常信息
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)

# 带上下文的日志
class ContextLogger:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.context: Dict[str, Any] = {}
    
    def bind(self, **kwargs) -> 'ContextLogger':
        """绑定上下文"""
        new_logger = ContextLogger(self.logger)
        new_logger.context = {**self.context, **kwargs}
        return new_logger
    
    def _log(self, level: int, msg: str, **kwargs):
        extra = {'extra_data': {**self.context, **kwargs}}
        self.logger.log(level, msg, extra=extra)
    
    def info(self, msg: str, **kwargs):
        self._log(logging.INFO, msg, **kwargs)
    
    def error(self, msg: str, **kwargs):
        self._log(logging.ERROR, msg, **kwargs)

# 使用
logger = ContextLogger(logging.getLogger("app"))
request_logger = logger.bind(request_id="abc123", user_id=1)
request_logger.info("处理请求", action="create_user")
```

### 规范3：请求日志中间件

```python
# app/middleware/logging.py
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 生成请求 ID
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        
        # 记录请求开始
        start_time = time.time()
        
        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host,
        )
        
        # 处理请求
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                "Request failed",
                request_id=request_id,
                error=str(e),
                exc_info=True
            )
            raise
        
        # 记录请求结束
        duration = time.time() - start_time
        logger.info(
            "Request completed",
            request_id=request_id,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2)
        )
        
        # 添加响应头
        response.headers["X-Request-ID"] = request_id
        
        return response
```

### 规范4：Prometheus 指标

```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response

# 定义指标
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

ACTIVE_REQUESTS = Gauge(
    'http_active_requests',
    'Active HTTP requests'
)

# 中间件
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ACTIVE_REQUESTS.inc()
        
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        ACTIVE_REQUESTS.dec()
        
        return response

# 暴露指标端点
@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
```

### 规范5：告警配置

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://localhost:8080/webhook'
  
  - name: 'critical-alerts'
    webhook_configs:
      - url: 'http://localhost:8080/webhook'
        send_resolved: true

# prometheus rules
groups:
  - name: api-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} requests/second"
      
      - alert: SlowResponse
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow response time"
          description: "95th percentile latency is {{ $value }}s"
```

### 规范6：日志级别使用规范

| 级别 | 使用场景 | 示例 |
|------|---------|------|
| **DEBUG** | 调试信息，生产环境关闭 | 变量值、SQL语句 |
| **INFO** | 正常业务流程 | 请求处理、任务完成 |
| **WARNING** | 潜在问题，不影响功能 | 配置缺失、重试 |
| **ERROR** | 错误，影响单个请求 | 接口调用失败 |
| **CRITICAL** | 严重错误，影响系统 | 数据库连接失败 |

```python
# 正确使用示例
logger.debug(f"查询参数: {params}")
logger.info(f"用户 {user_id} 登录成功")
logger.warning(f"配置项 {key} 未设置，使用默认值")
logger.error(f"调用支付接口失败: {error}", exc_info=True)
logger.critical(f"数据库连接失败: {error}")
```

### 规范7：ELK 日志收集

```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - es-data:/usr/share/elasticsearch/data

  logstash:
    image: logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

  filebeat:
    image: elastic/filebeat:8.11.0
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml
      - ./logs:/var/log/app
    depends_on:
      - logstash

volumes:
  es-data:
```

## 禁止事项
- ❌ 在日志中输出敏感信息（密码、Token）
- ❌ 生产环境开启 DEBUG 级别
- ❌ 不记录异常堆栈
- ❌ 日志文件无轮转策略
- ❌ 忽略告警通知

## 检查清单
- [ ] 是否配置了日志轮转
- [ ] 是否有结构化日志格式
- [ ] 是否记录了请求 ID
- [ ] 是否配置了监控指标
- [ ] 是否配置了告警规则
- [ ] 是否有日志收集方案
