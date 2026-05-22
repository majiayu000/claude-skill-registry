---
name: arch-scalability
cluster: se-architecture
description: "Scalability: horizontal/vertical, load balancing, caching Redis/CDN, DB replicas, queue decoupling"
tags: ["scalability","load-balancing","caching","architecture"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "scalability load balancing horizontal vertical cache redis queue replica"
---

# arch-scalability

## Purpose
This skill enables OpenClaw to design and implement scalable system architectures, focusing on handling increased loads through horizontal and vertical scaling, load balancing, caching strategies (e.g., Redis or CDN), database replicas, and queue-based decoupling to ensure applications remain performant and reliable under growth.

## When to Use
Use this skill when an application experiences traffic spikes, requires elastic resource allocation, or needs to distribute workloads to avoid bottlenecks—such as e-commerce sites during sales, real-time data processing apps, or microservices handling variable user loads. Apply it early in development for cloud-native designs or when migrating monolithic apps.

## Key Capabilities
- **Horizontal Scaling**: Add identical instances (e.g., via AWS Auto Scaling) to distribute load; use tools like Kubernetes for pod scaling.
- **Vertical Scaling**: Upgrade existing resources (e.g., increase CPU/RAM on an EC2 instance) for immediate capacity needs, but monitor limits to avoid downtime.
- **Load Balancing**: Distribute traffic across servers using NGINX or AWS ELB; supports round-robin or least-connections algorithms.
- **Caching**: Implement Redis for in-memory caching or CDN (e.g., Cloudflare) for static assets to reduce latency and database hits.
- **DB Replicas**: Set up read replicas in MySQL or PostgreSQL to handle read-heavy queries without overloading the primary database.
- **Queue Decoupling**: Use RabbitMQ or Kafka to offload tasks, preventing synchronous bottlenecks in high-throughput systems.

## Usage Patterns
To scale horizontally, configure auto-scaling groups in AWS; for vertical scaling, adjust instance types programmatically. Use caching patterns like cache-aside with Redis for frequently accessed data. For load balancing, integrate NGINX as a reverse proxy. Decouple services by routing tasks to queues, ensuring asynchronous processing. Always monitor metrics (e.g., via Prometheus) to trigger scaling events based on CPU > 80%. Pattern example: In a Node.js app, check queue length before processing and scale workers dynamically.

## Common Commands/API
Use these exact commands for scalability tasks. Set environment variables for authentication, e.g., `export REDIS_API_KEY=$SERVICE_API_KEY` for Redis connections.

- **Horizontal Scaling (AWS CLI)**: Create an auto-scaling group:  
  `aws autoscaling create-auto-scaling-group --auto-scaling-group-name my-group --launch-configuration-name my-config --min-size 1 --max-size 5 --vpc-zone-identifier subnet-123456`
  
- **Vertical Scaling (AWS EC2)**: Modify instance type:  
  `aws ec2 modify-instance-attribute --instance-id i-12345678 --instance-type "{\"Value": "t3.medium"}"`
  
- **Load Balancing (NGINX config)**: Edit `/etc/nginx/nginx.conf` and add:  
  `upstream backend { server 192.168.1.1:80; server 192.168.1.2:80; } server { listen 80; location / { proxy_pass http://backend; } }`
  
- **Caching (Redis CLI)**: Set and get cache values:  
  `redis-cli -h redis-host SET user:1 "John Doe" EX 3600`  
  `redis-cli -h redis-host GET user:1`
  
- **DB Replicas (MySQL)**: Create a replica:  
  `mysql -u root -p -e "CALL mysql.rds_create_replication_group('my-group', 'my-replica');"` (for AWS RDS)
  
- **Queue Decoupling (RabbitMQ)**: Publish a message:  
  `rabbitmqadmin publish exchange=logs routingKey=info payload="{'message': 'High load detected'}"`

API endpoints for OpenClaw integration: Use POST to `/api/scalability/scale-group` with JSON body `{ "group": "my-group", "action": "scale-out", "instances": 2 }` and include auth header `Authorization: Bearer $SERVICE_API_KEY`.

## Integration Notes
Integrate by wrapping scalability logic in your code; for example, use AWS SDK in Python to check metrics and trigger scaling: Import `boto3`, then `autoscaling = boto3.client('autoscaling')`. For Redis, connect via `redis-py` library: `import redis; r = redis.Redis(host='redis-host', password=os.environ['REDIS_API_KEY'])`. Use config files like YAML for settings:  
```yaml
scaling:
  min_instances: 1
  max_instances: 5
  threshold: 80  # CPU percent
```  
Ensure services are in the same VPC for low-latency communication. For CDN, configure Cloudflare via API: `curl -X PUT "https://api.cloudflare.com/client/v4/zones/zone-id/settings/development_mode" -H "Authorization: Bearer $CLOUDFLARE_API_KEY" -d '{"value":"on"}'`. Test integrations in staging environments first.

## Error Handling
Handle errors proactively: For Redis connections, use try-except blocks to catch `ConnectionError` and implement retries with exponential backoff (e.g., wait 2^x seconds). In load balancing, monitor for 502 errors and scale up if server health checks fail. For DB replicas, check replication lag with `SHOW SLAVE STATUS` in MySQL and fallback to primary if lag > 5 seconds. Queue errors (e.g., RabbitMQ connection failures) should trigger alerts via tools like Sentry; code snippet:  
```python
import pika
try:
    connection = pika.BlockingConnection(pika.URLParameters(os.environ['RABBITMQ_URL']))
except pika.exceptions.AMQPConnectionError as e:
    print(f"Queue error: {e}. Retrying in 5 seconds...")
    time.sleep(5)
    # Retry logic here
```  
Log all errors with timestamps and metrics for post-incident analysis.

## Concrete Usage Examples
1. **Example: Scaling a Web App with NGINX Load Balancer**  
   For a Node.js web server handling user requests, first set up NGINX: Edit config as above, then run `nginx -s reload`. In code, use AWS SDK to auto-scale:  
   ```javascript
   const AWS = require('aws-sdk'); const autoscaling = new AWS.AutoScaling(); autoscaling.setDesiredCapacity({ AutoScalingGroupName: 'my-group', DesiredCapacity: 3 }).promise();
   ```  
   This scales out to 3 instances when traffic exceeds thresholds, distributing load via NGINX.

2. **Example: Implementing Redis Caching for Database Queries**  
   In a Python Flask app, cache user data to reduce DB hits: First, connect to Redis as noted. Then:  
   ```python
   import redis r = redis.Redis(host='redis-host', password=os.environ['REDIS_API_KEY']) def get_user(id): value = r.get(f'user:{id}') if value: return value.decode() else: user = query_db(id)  # Fetch from DB r.set(f'user:{id}', user, ex=3600) return user
   ```  
   This caches results for 1 hour, improving response times during high load.

## Graph Relationships
- Related Cluster: se-architecture
- Related Tags: scalability, load-balancing, caching, architecture
- Linked Skills: arch-load-balancing (for deeper load strategies), data-caching (for advanced Redis patterns)
