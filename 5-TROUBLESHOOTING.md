# 故障排除与快速参考

> 常见问题诊断、修复方案、命令速查表

## 🔴 常见问题速查

### 问题 1: 数据库连接失败

**错误信息**：
```
FATAL: database "eve_sde_db" does not exist
Failed to establish a new connection
psycopg2.OperationalError: could not translate host name "eve-pg" to address
```

**根本原因**：
- ❌ 数据库容器未启动
- ❌ 使用了错误的服务名或主机名
- ❌ 网络连接问题
- ❌ 环境变量配置错误

**诊断步骤**：

```bash
# 1. 检查数据库容器是否运行
docker ps | grep eve_db
# 如果没有输出，说明容器未运行

# 2. 查看容器日志
docker logs eve_db | tail -50

# 3. 检查环境变量
docker exec eve_backend env | grep DB_

# 4. 测试 DNS 解析
docker exec eve_backend nslookup eve-pg
# 应该返回 IP 地址

# 5. 测试端口连接
docker exec eve_backend nc -zv eve-pg 5432
# 应该输出 "Connection succeeded"

# 6. 直接连接测试
docker exec eve_backend psql -U postgres -h eve-pg -d ruoyi-fastapi -c "SELECT 1"
```

**修复方案**：

```bash
# 方案 1: 重启数据库容器
docker-compose -f docker-compose.local.yml restart eve-pg

# 方案 2: 查看具体错误
docker logs eve_db | grep -i error

# 方案 3: 清理旧数据重新启动
docker-compose -f docker-compose.local.yml down
sudo rm -rf postgres_data/
docker-compose -f docker-compose.local.yml up -d eve-pg

# 方案 4: 检查网络连通性
docker network inspect eve-project_eve-network
```

---

### 问题 2: 前端 API 请求 404

**错误信息**：
```
GET /docker-api/auth/login 404 Not Found
GET http://localhost:12580/docker-api/system/user/info 404
```

**根本原因**：
- ❌ 后端 API 服务未启动
- ❌ 路由前缀不匹配
- ❌ Nginx 代理配置错误
- ❌ 请求路径拼写错误

**诊断步骤**：

```bash
# 1. 检查后端容器状态
docker ps | grep eve_backend
docker logs eve_backend | tail -20

# 2. 测试后端 API 直连
curl -v http://localhost:19099/docker-api/docs
# 应该返回 200 OK

# 3. 检查路由前缀配置
grep APP_ROOT_PATH EVE-FastAPI/EVE-fastapi-backend/.env.dockerpg
docker exec eve_backend env | grep APP_ROOT_PATH

# 4. 检查前端构建配置
grep VITE_APP_BASE_API EVE-FastAPI/EVE-fastapi-frontend/.env.docker

# 5. 检查 Nginx 配置
docker exec eve_frontend cat /etc/nginx/conf.d/default.conf | grep docker-api

# 6. 测试 Nginx 代理
curl -v http://localhost:12580/docker-api/docs
# 应该能访问后端 docs
```

**修复方案**：

```bash
# 确保三处配置一致
# 1. 后端
grep APP_ROOT_PATH EVE-FastAPI/EVE-fastapi-backend/.env.dockerpg
# 应该是: APP_ROOT_PATH = '/docker-api'

# 2. 前端
grep VITE_APP_BASE_API EVE-FastAPI/EVE-fastapi-frontend/.env.docker
# 应该是: VITE_APP_BASE_API=/docker-api

# 3. Nginx
grep "location /docker-api" EVE-FastAPI/EVE-fastapi-frontend/bin/nginx.dockerpg.conf
# 应该是: location /docker-api/ { proxy_pass http://eve-backend-pg:9099/; }

# 修复后重启服务
docker-compose -f docker-compose.local.yml restart
```

---

### 问题 3: 容器启动后立即退出

**错误信息**：
```
docker ps -a 中容器状态为 Exited
docker logs 显示错误信息
```

**根本原因**：
- ❌ 依赖服务未就绪
- ❌ 配置文件语法错误
- ❌ 端口被占用
- ❌ 缺少必要的环境变量

**诊断步骤**：

```bash
# 1. 查看容器状态
docker ps -a | grep eve

# 2. 查看完整日志
docker logs eve_backend
docker logs eve_db

# 3. 检查依赖
docker logs eve_backend | grep -i "error\|fatal\|connection"

# 4. 查看启动命令
docker inspect eve_backend | grep -A 5 "Cmd"

# 5. 检查配置文件
docker exec eve_backend cat .env.dockerpg | head -20
```

**修复方案**：

```bash
# 检查依赖启动顺序
docker ps -a | grep -E "eve_db|eve_backend"
# eve_db 应该先启动，且状态为 Up

# 等待数据库完全启动
docker exec eve_db pg_isready
# 返回 "accepting connections" 表示就绪

# 手动启动后端
docker-compose -f docker-compose.local.yml up eve-backend-pg
# 不加 -d，可以看到详细输出
```

---

### 问题 4: EVE SSO 登录失败

**错误信息**：
```
state 校验失败
CCP token 获取失败
重定向到 error=sso_failed
```

**根本原因**：
- ❌ EVE_CLIENT_ID / EVE_CLIENT_SECRET 不正确或过期
- ❌ EVE_CALLBACK_URL 与 CCP 后台配置不一致
- ❌ Redis 无法访问（state 存储失败）
- ❌ 时钟不同步

**诊断步骤**：

```bash
# 1. 检查 ESI 凭证
docker exec eve_backend env | grep EVE_

# 2. 检查回调 URL
docker exec eve_backend env | grep EVE_CALLBACK_URL
# 应该与 CCP 后台完全一致

# 3. 检查 Redis 连接
docker exec eve_backend redis-cli -h eve-redis ping
# 应该返回 PONG

# 4. 查看登录日志
docker logs eve_backend | grep -i "sso\|auth\|eve"

# 5. 检查时钟同步
docker exec eve_backend date
# 应该与宿主机时间一致
```

**修复方案**：

```bash
# 1. 更新 ESI 凭证
# 在 .env.server 或 .env.local 中修改
EVE_CLIENT_ID=...
EVE_CLIENT_SECRET=...

# 2. 修复回调 URL
# 确保与 CCP 后台完全一致（一个字符都不能差）
EVE_CALLBACK_URL=http://localhost:12580/docker-api/auth/eve/callback

# 3. 重启服务加载新配置
docker-compose -f docker-compose.local.yml restart eve-backend-pg

# 4. 同步时钟（如果系统时钟不对）
# 宿主机：ntpdate -s time.nist.gov
# Docker：docker run --rm --privileged --tty ubuntu:latest timedatectl set-time "2026-01-24 10:00:00"
```

---

### 问题 5: 端口冲突

**错误信息**：
```
Error starting userland proxy: listen tcp 0.0.0.0:5432: bind: address already in use
```

**根本原因**：
- ❌ 端口已被其他应用使用
- ❌ 旧容器仍在占用
- ❌ Docker 残留进程

**诊断步骤**：

```bash
# 1. 查看端口占用情况
lsof -i :5432
netstat -tulpn | grep 5432

# 2. 查看 Docker 端口映射
docker-compose -f docker-compose.local.yml ps
docker port eve_db

# 3. 查看旧容器
docker ps -a | grep eve_db
```

**修复方案**：

```bash
# 方案 1: 清理旧容器
docker-compose -f docker-compose.local.yml down
docker ps -a | grep eve | awk '{print $1}' | xargs docker rm -f

# 方案 2: 修改端口映射
# 在 .env.local 中修改
DB_EXTERNAL_PORT=25432  # 改为其他端口

# 方案 3: 杀死占用进程
lsof -i :5432 | grep LISTEN | awk '{print $2}' | xargs kill -9

# 然后重新启动
docker-compose -f docker-compose.local.yml up -d
```

---

## 🧹 完全重置环境

**适用场景**：多次修复无效、配置混乱、需要全新环境

```bash
cd /opt/EVE-Project

# 步骤 1: 停止并删除所有容器和卷
docker-compose -f docker-compose.local.yml down -v

# 步骤 2: 删除所有相关镜像
docker rmi $(docker images | grep eve | awk '{print $3}')

# 步骤 3: 删除持久化数据
sudo rm -rf postgres_data/

# 步骤 4: 清理 Docker 系统（可选，慎用）
docker system prune -a --volumes

# 步骤 5: 验证配置文件
cat .env.local
cat EVE-FastAPI/EVE-fastapi-backend/.env.dockerpg
cat EVE-FastAPI/EVE-fastapi-frontend/.env.docker

# 步骤 6: 重新构建和启动
docker-compose -f docker-compose.local.yml build --no-cache
docker-compose -f docker-compose.local.yml up -d

# 步骤 7: 监控启动过程
docker-compose -f docker-compose.local.yml logs -f

# 步骤 8: 验证服务就绪
docker-compose -f docker-compose.local.yml ps
curl http://localhost:12580
curl http://localhost:19099/docker-api/docs
```

---

## 📋 诊断命令速查

### 容器与镜像

```bash
# 列出正在运行的容器
docker ps

# 列出所有容器（包含已停止）
docker ps -a

# 查看镜像列表
docker images

# 查看容器详细信息
docker inspect eve_backend

# 查看容器资源使用
docker stats

# 查看容器进程
docker top eve_backend

# 查看容器启动命令
docker inspect eve_backend | grep -A 5 '"Cmd"'
```

### 日志管理

```bash
# 查看所有服务日志
docker-compose -f docker-compose.local.yml logs

# 实时查看特定服务日志
docker logs -f eve_backend

# 查看最近 N 行
docker logs --tail 100 eve_backend

# 查看某个时间段的日志
docker logs --since 1h eve_backend

# 搜索特定关键词
docker logs eve_backend 2>&1 | grep -i "error\|fatal"
```

### 网络诊断

```bash
# 列出所有网络
docker network ls

# 查看网络详情
docker network inspect eve-project_eve-network

# 测试容器间连通性
docker exec eve_backend ping eve-pg

# 测试端口连接
docker exec eve_backend nc -zv eve-pg 5432

# 查看 DNS 解析
docker exec eve_backend nslookup eve-pg

# 查看容器网络接口
docker exec eve_backend ip addr show

# 查看容器路由
docker exec eve_backend route -n
```

### 数据库诊断

```bash
# 连接数据库
docker exec -it eve_db psql -U postgres -d ruoyi-fastapi

# psql 常用命令（在 psql 提示符下）
\l                          # 列出数据库
\dt                         # 列出表
\d table_name              # 查看表结构
SELECT * FROM users;       # 查询数据

# 从外部执行 SQL
docker exec eve_db psql -U postgres -d ruoyi-fastapi -c "SELECT count(*) FROM users;"

# 备份数据库
docker exec eve_db pg_dump -U postgres ruoyi-fastapi > backup.sql

# 恢复数据库
docker exec -i eve_db psql -U postgres ruoyi-fastapi < backup.sql
```

### Nginx 诊断

```bash
# 检查 Nginx 配置语法
docker exec eve_frontend nginx -t

# 查看 Nginx 进程
docker exec eve_frontend ps aux | grep nginx

# 查看 Nginx 配置文件
docker exec eve_frontend cat /etc/nginx/conf.d/default.conf

# 重载 Nginx 配置（不重启）
docker exec eve_frontend nginx -s reload

# 查看 Nginx 日志
docker logs eve_frontend

# 在容器内测试后端连接
docker exec eve_frontend curl -v http://eve-backend-pg:9099/docker-api/docs
```

### Redis 诊断

```bash
# 连接 Redis 并 ping
docker exec eve_redis redis-cli ping

# 查看 Redis 信息
docker exec eve_redis redis-cli info

# 查看所有 key
docker exec eve_redis redis-cli keys "*"

# 查看特定 key 的值
docker exec eve_redis redis-cli get "key_name"

# 删除特定 key
docker exec eve_redis redis-cli del "key_name"
```

---

## ⚡ 常用命令速查表

### 容器生命周期

```bash
# 启动
docker-compose -f docker-compose.local.yml up -d

# 停止
docker-compose -f docker-compose.local.yml stop

# 重启
docker-compose -f docker-compose.local.yml restart

# 停止并删除
docker-compose -f docker-compose.local.yml down

# 删除卷
docker-compose -f docker-compose.local.yml down -v

# 查看状态
docker-compose -f docker-compose.local.yml ps
```

### 镜像操作

```bash
# 构建
docker-compose -f docker-compose.local.yml build

# 不使用缓存重新构建
docker-compose -f docker-compose.local.yml build --no-cache

# 删除镜像
docker rmi image_id

# 删除所有未使用的镜像
docker image prune -a
```

### 容器操作

```bash
# 进入容器 shell
docker exec -it container_name /bin/bash

# 运行命令
docker exec container_name command

# 查看日志
docker logs container_name

# 查看统计
docker stats container_name

# 复制文件（容器→宿主机）
docker cp container_name:/path/to/file ./local/path

# 复制文件（宿主机→容器）
docker cp ./local/path container_name:/path/to/file
```

---

## 📞 获取帮助

### 检查列表

- [ ] 所有容器状态为 `Up`
- [ ] 数据库能正常连接
- [ ] 后端 API 文档可访问
- [ ] 前端页面能加载
- [ ] ESI 登录能成功

### 信息收集

```bash
# 生成诊断报告
cat > diagnostic_report.txt << 'EOF'
# 诊断报告 - $(date)

## 容器状态
$(docker-compose -f docker-compose.local.yml ps)

## 镜像列表
$(docker images | grep eve)

## 日志信息
$(docker-compose -f docker-compose.local.yml logs --tail 50)

## 网络诊断
$(docker network inspect eve-project_eve-network)

## 数据库检查
$(docker exec eve_db psql -U postgres -d ruoyi-fastapi -c "SELECT 1")
EOF

cat diagnostic_report.txt
```

---

## 清理缓存与重建

```bash
# 查看当前可回收空间
docker system df

# 清空所有缓存（镜像、容器、卷、构建缓存）
docker system prune -a --volumes -f

# 服务器环境：无缓存重建并启动
cd /opt/EVE-Project
mkdir -p postgres_data
docker compose -f docker-compose.server.yml --env-file .env.server build --no-cache
docker compose -f docker-compose.server.yml --env-file .env.server up -d

# 本地开发（可选）：无缓存重建并启动
cd /opt/EVE-Project
mkdir -p postgres_data
docker compose -f EVE-FastAPI/docker-compose.local.yml --env-file .env.local build --no-cache
docker compose -f EVE-FastAPI/docker-compose.local.yml --env-file .env.local up -d
```

---

## 📖 相关文档

- [1-PROJECT_OVERVIEW.md](1-PROJECT_OVERVIEW.md) - 项目概览
- [2-DOCKER_BUILD.md](2-DOCKER_BUILD.md) - Docker 构建与部署
- [3-CONFIG_ENV.md](3-CONFIG_ENV.md) - 环境配置管理
- [4-DEV_GUIDE.md](4-DEV_GUIDE.md) - 开发指南

---

## 💡 经验技巧

### 快速调试技巧

```bash
# 1. 使用 alias 简化命令
alias dc-local='docker-compose -f docker-compose.local.yml'
alias dc-logs='docker-compose -f docker-compose.local.yml logs -f'

# 2. 一键重启
dc-local down && dc-local up -d && dc-logs

# 3. 快速进入容器
docker exec -it eve_backend bash

# 4. 查看最近的错误
docker logs eve_backend | tail -100 | grep -i error
```

### 性能优化

```bash
# 减小镜像体积：使用 .dockerignore
echo "node_modules" > .dockerignore
echo ".git" >> .dockerignore

# 加快构建速度：使用镜像缓存
docker-compose -f docker-compose.local.yml build  # 使用缓存
docker-compose -f docker-compose.local.yml build --no-cache  # 跳过缓存

# 监控资源使用
docker stats --no-stream  # 单次输出
```

### 安全建议

```bash
# 不要提交包含密码的 .env 文件
echo ".env*" >> .gitignore

# 定期备份数据库
docker exec eve_db pg_dump -U postgres ruoyi-fastapi > backup_$(date +%Y%m%d_%H%M%S).sql

# 使用强密码
# 生成随机密码：openssl rand -base64 32
```
