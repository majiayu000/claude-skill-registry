---
name: apache
description: Apache HTTP Server 配置
version: 1.0.0
author: terminal-skills
tags: [server, apache, httpd, web, vhost]
---

# Apache 配置

## 概述
Apache HTTP Server 配置、虚拟主机、模块管理等技能。

## 基础管理

### 服务控制
```bash
# CentOS/RHEL
systemctl start httpd
systemctl stop httpd
systemctl restart httpd
systemctl reload httpd

# Ubuntu/Debian
systemctl start apache2
systemctl stop apache2
systemctl restart apache2
systemctl reload apache2

# 配置测试
apachectl configtest
httpd -t
```

### 配置文件
```bash
# CentOS/RHEL
/etc/httpd/conf/httpd.conf
/etc/httpd/conf.d/*.conf

# Ubuntu/Debian
/etc/apache2/apache2.conf
/etc/apache2/sites-available/
/etc/apache2/sites-enabled/

# 日志
/var/log/httpd/                     # CentOS
/var/log/apache2/                   # Ubuntu
```

### 模块管理
```bash
# Ubuntu/Debian
a2enmod rewrite                     # 启用模块
a2dismod rewrite                    # 禁用模块
a2ensite example.conf               # 启用站点
a2dissite example.conf              # 禁用站点

# CentOS/RHEL
# 编辑 /etc/httpd/conf.modules.d/
httpd -M                            # 列出已加载模块
```

## 虚拟主机

### 基于域名
```apache
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    DocumentRoot /var/www/example
    
    <Directory /var/www/example>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/example-error.log
    CustomLog ${APACHE_LOG_DIR}/example-access.log combined
</VirtualHost>
```

### HTTPS 配置
```apache
<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/example
    
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/example.crt
    SSLCertificateKeyFile /etc/ssl/private/example.key
    SSLCertificateChainFile /etc/ssl/certs/chain.crt
    
    # SSL 优化
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    SSLHonorCipherOrder off
    
    Header always set Strict-Transport-Security "max-age=31536000"
</VirtualHost>

# HTTP 重定向
<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / https://example.com/
</VirtualHost>
```

## 反向代理

### 基础代理
```apache
# 启用模块
# a2enmod proxy proxy_http

<VirtualHost *:80>
    ServerName api.example.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:3000/
    ProxyPassReverse / http://127.0.0.1:3000/
    
    # 超时设置
    ProxyTimeout 300
</VirtualHost>
```

### 负载均衡
```apache
# 启用模块
# a2enmod proxy_balancer lbmethod_byrequests

<Proxy "balancer://mycluster">
    BalancerMember http://192.168.1.10:8080
    BalancerMember http://192.168.1.11:8080
    ProxySet lbmethod=byrequests
</Proxy>

<VirtualHost *:80>
    ServerName app.example.com
    ProxyPass / balancer://mycluster/
    ProxyPassReverse / balancer://mycluster/
</VirtualHost>
```

## URL 重写

### 基础重写
```apache
# 启用模块
# a2enmod rewrite

<Directory /var/www/html>
    RewriteEngine On
    
    # 强制 HTTPS
    RewriteCond %{HTTPS} off
    RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
    
    # 去除 www
    RewriteCond %{HTTP_HOST} ^www\.(.+)$ [NC]
    RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
    
    # 前端路由（SPA）
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^ index.html [L]
</Directory>
```

### .htaccess
```apache
# /var/www/html/.htaccess
RewriteEngine On

# 隐藏 .php 扩展名
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.php -f
RewriteRule ^(.*)$ $1.php [L]

# 防盗链
RewriteCond %{HTTP_REFERER} !^$
RewriteCond %{HTTP_REFERER} !^https?://(www\.)?example\.com [NC]
RewriteRule \.(jpg|jpeg|png|gif)$ - [F]
```

## 安全配置

### 基础安全
```apache
# 隐藏版本信息
ServerTokens Prod
ServerSignature Off

# 禁用目录列表
<Directory /var/www>
    Options -Indexes
</Directory>

# 安全头
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-XSS-Protection "1; mode=block"
```

### 访问控制
```apache
# IP 限制
<Directory /var/www/admin>
    Require ip 192.168.1.0/24
</Directory>

# 基础认证
<Directory /var/www/private>
    AuthType Basic
    AuthName "Restricted Area"
    AuthUserFile /etc/apache2/.htpasswd
    Require valid-user
</Directory>

# 创建密码文件
# htpasswd -c /etc/apache2/.htpasswd username
```

## 常见场景

### 场景 1：PHP 配置
```apache
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/html
    
    <FilesMatch \.php$>
        SetHandler "proxy:unix:/var/run/php/php-fpm.sock|fcgi://localhost"
    </FilesMatch>
    
    <Directory /var/www/html>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

### 场景 2：限流
```apache
# 启用模块
# a2enmod ratelimit

<Location /api>
    SetOutputFilter RATE_LIMIT
    SetEnv rate-limit 400
</Location>
```

### 场景 3：日志格式
```apache
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %D" combined_time
CustomLog ${APACHE_LOG_DIR}/access.log combined_time
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 配置错误 | `apachectl configtest` |
| 403 Forbidden | 检查目录权限、SELinux |
| 500 Internal Error | 查看 error.log |
| 模块未加载 | `httpd -M` 检查模块 |
| 性能问题 | 检查 MPM 配置、连接数 |
