# Docker 构建与部署指南

> 深入讲解 Dockerfile、Docker Compose 编排、容器启动流程

## ⚙️ 配置文件与环境切换

- 配置存放：后端目录下的 `EVE-fastapi-backend/esi.local.cfg`（本地）、`EVE-fastapi-backend/esi.prod.cfg`（生产），模板在项目根的 `esi.cfg.example`。
- 选择逻辑：`ENV_STATE=production` 时自动加载 `esi.prod.cfg`，否则默认 `esi.local.cfg`；可传入 `config_path` 覆盖。
- 敏感信息：`EVE_CLIENT_ID`、`EVE_CLIENT_SECRET`、`EVE_REFRESH_TOKEN` 支持环境变量优先，未设置时回落到对应 cfg。
- 连接串：本地示例 `postgresql://postgres:your-local-password@localhost:5432/eve_db`；生产示例 `postgresql://postgres:your-prod-password@localhost:5432/your-prod-db`，容器访问宿主机可将 host 改为 `172.17.0.1`。
- Git 忽略：`.gitignore` 已忽略所有非 `.cfg.example` 的 `.cfg`，请勿将真实凭证提交到仓库。

## 📦 Dockerfile 详解

### 1. 后端 Dockerfile (`EVE-fastapi-backend/Dockerfile.pg`)

```dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（PostgreSQL 客户端库等）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements-pg.txt .

# 安装 Python 依赖（使用国内镜像加速）
RUN pip install --no-cache-dir -r requirements-pg.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 9099

# 启动命令
CMD ["python", "app.py", "--env=dockerpg"]
```

**构建过程**：

```bash
# 1. 拉取基础镜像
FROM python:3.11-slim
# 下载 ~200MB 的 Python 环境

# 2. 安装系统依赖
RUN apt-get install ...
# 编译工具和 PostgreSQL 客户端库

# 3. 安装 Python 依赖
RUN pip install -r requirements-pg.txt
# asyncpg, SQLAlchemy, FastAPI, redis 等
# 第一次 ~3-5min，缓存后 <30s

# 4. 复制代码
COPY . .
# 整个项目代码 (~50MB)

# 5. 运行命令
CMD ["python", "app.py", "--env=dockerpg"]
```

**启动流程**：

```
容器启动
    ↓
执行: python app.py --env=dockerpg
    ↓
config/env.py 加载 .env.dockerpg 配置
    ↓
FastAPI 应用初始化
    ├─ 创建数据库连接池 (SQLAlchemy)
    ├─ 连接 Redis
    ├─ 初始化 APScheduler 定时任务
    └─ 启动 Uvicorn 服务器 (127.0.0.1:9099)
    ↓
应用就绪 ✅
```

**关键依赖** (`requirements-pg.txt`)：

```
fastapi==0.109.0              # Web 框架
uvicorn[standard]==0.27.0     # ASGI 服务器
sqlalchemy[asyncio]==2.0.25   # 异步 ORM
asyncpg==0.29.0               # 异步 PostgreSQL 驱动
redis==5.0.1                  # Redis 客户端
apscheduler==3.10.4           # 定时任务
pillow==10.1.0                # 图像处理
pydantic==2.5.3               # 数据验证
python-dotenv==1.0.0          # 环境变量加载
sshtunnel==0.4.0              # SSH 隧道（可选）
```

### 2. 前端 Dockerfile (多阶段构建)

```dockerfile
# === 构建阶段 ===
FROM node:20-alpine AS builder
WORKDIR /app

# 设置 npm 镜像源
RUN npm config set registry https://registry.npmmirror.com

# 复制 package.json 和锁文件
COPY package.json .
RUN npm install --no-package-lock

# 复制项目文件
COPY . .

# 使用 docker 构建模式编译
RUN npm run build:docker
# 输出: dist/ 目录 (~5MB)

# === 运行阶段 ===
FROM nginx:stable-alpine
WORKDIR /usr/share/nginx/html

# 从构建阶段复制静态文件
COPY --from=builder /app/dist ./

# 复制 Nginx 配置
COPY bin/nginx.dockerpg.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# 前台运行 Nginx（容器不会退出）
CMD ["nginx", "-g", "daemon off;"]
```

**多阶段构建优势**：

```
构建前镜像：node:20-alpine (135MB) + build dependencies (200MB) = ~335MB
    ↓
使用 --from=builder 只复制 dist/ 目录 (~5MB)
    ↓
最终镜像：nginx:stable-alpine (40MB) + dist (~5MB) = ~45MB

减少镜像体积：335MB → 45MB (约 87% 的压缩比)
```

**Nginx 反向代理配置** (`bin/nginx.dockerpg.conf`)：

```nginx
server {
    listen 80;
    server_name localhost;

    # 前端 SPA 路由支持
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
        # 所有未知路由都返回 index.html，让 Vue Router 处理
    }

    # API 代理到后端
    location /docker-api/ {
        proxy_pass http://eve-backend-pg:9099/;
        # 重要：proxy_pass 不指定路径，保持完整路径
        # 请求：http://localhost:12580/docker-api/auth/login
        # 代理到：http://eve-backend-pg:9099/docker-api/auth/login
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

**代理路径详解**：

```
请求流程：
1. 前端发送: GET http://localhost:12580/docker-api/auth/login

2. Nginx 匹配 location /docker-api/
   ├─ proxy_pass 指向: http://eve-backend-pg:9099/
   └─ 注意：没有在 proxy_pass 中指定 /docker-api
   
3. Nginx 转发到后端: http://eve-backend-pg:9099/docker-api/auth/login
   (完整路径被保留)

4. 后端 FastAPI 应用
   ├─ APP_ROOT_PATH=/docker-api 配置被加载
   ├─ 中间件自动去掉前缀 /docker-api
   └─ 最终路由到: /auth/login

5. 返回响应给前端 ✅
```

### 3. SDE 处理器 Dockerfile

```dockerfile
FROM python:3.11-slim

# 环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/app/data

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# 创建非 root 用户（安全性）
RUN mkdir -p /app/data /app/scripts && \
    useradd -m eveuser && \
    chown -R eveuser:eveuser /app

# 安装 Python 依赖
COPY --chown=eveuser:eveuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY --chown=eveuser:eveuser . .

# 切换到非 root 用户
USER eveuser

# 启动处理器
CMD ["python", "main.py"]
```

---

## 🐳 Docker Compose 编排详解

### docker-compose.local.yml（本地开发）

```yaml
version: '3.8'

services:
  # ==================== 数据库 ====================
  eve-pg:
    image: postgres:15-alpine
    container_name: eve_db
    restart: always
    
    # 环境变量（初始化参数）
    environment:
      - POSTGRES_USER=eve_admin
      - POSTGRES_PASSWORD=y20Vnn4FfPDPZJidY9LuiGtU
      - POSTGRES_DB=eve_sde_db
    
    # 端口映射
    ports:
      - "5432:5432"  # 标准 PostgreSQL 端口
    
    # 数据持久化
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    
    # 健康检查（其他服务依赖此检查）
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "eve_admin", "-d", "eve_sde_db"]
      interval: 5s
      timeout: 5s
      retries: 5
    
    networks:
      - eve-network

  # ==================== 缓存 ====================
  eve-redis:
    image: redis:7-alpine
    container_name: eve-redis
    restart: always
    networks:
      - eve-network

  # ==================== 后端 ====================
  eve-backend-pg:
    # 从 Dockerfile.pg 构建镜像
    build:
      context: ./EVE-fastapi-backend
      dockerfile: Dockerfile.pg
    
    container_name: eve_backend
    restart: always
    
    # 端口映射
    ports:
      - "19099:9099"
    
    # 环境变量（从 .env.server 加载）
    environment:
      - APP_ENV=dockerpg
      - ENV=dockerpg
      - DB_HOST=eve-pg          # 关键：使用服务名
      - DB_PORT=5432
      - DB_USERNAME=eve_admin
      - DB_PASSWORD=y20Vnn4FfPDPZJidY9LuiGtU
      - DB_DATABASE=eve_sde_db
      - REDIS_HOST=eve-redis    # 关键：使用服务名
      - REDIS_PORT=6379
      - EVE_CLIENT_ID=${EVE_CLIENT_ID}
      - EVE_CLIENT_SECRET=${EVE_CLIENT_SECRET}
      - EVE_CALLBACK_URL=${EVE_CALLBACK_URL}
      - FRONTEND_URL=${FRONTEND_URL}
    
    # 依赖关系（启动顺序）
    depends_on:
      eve-pg:
        condition: service_healthy  # 等待数据库健康检查通过
      eve-redis:
        condition: service_started
    
    networks:
      - eve-network

  # ==================== 处理器 ====================
  sde-processor:
    build:
      context: ./eve-sde-processor
      dockerfile: Dockerfile
    
    container_name: eve_sde_worker
    restart: always
    
    environment:
      - DB_HOST=eve-pg
      - DB_PORT=5432
      - DB_NAME=eve_sde_db
      - DB_USER=eve_admin
      - DB_PASSWORD=y20Vnn4FfPDPZJidY9LuiGtU
      - DATA_DIR=/app/data
    
    depends_on:
      eve-pg:
        condition: service_healthy
    
    networks:
      - eve-network

  # ==================== 前端 ====================
  frontend:
    build:
      context: ./EVE-fastapi-frontend
      dockerfile: Dockerfile
    
    container_name: eve_frontend
    restart: always
    
    ports:
      - "12580:80"
    
    volumes:
      - ./EVE-FastAPI/EVE-fastapi-frontend/bin/nginx.dockerpg.conf:/etc/nginx/conf.d/default.conf:ro
    
    depends_on:
      - eve-backend-pg
    
    networks:
      - eve-network

# ==================== 网络 ====================
networks:
  eve-network:
    driver: bridge
```

### 与生产编排的差异

```yaml
# 1. 数据库端口映射使用本地端口
eve-pg:
  ports:
    - "15432:5432"  # 避免与系统 PostgreSQL 冲突

# 2. 数据库配置使用本地凭证
environment:
  - POSTGRES_USER=postgres
  - POSTGRES_PASSWORD=root
  - POSTGRES_DB=ruoyi-fastapi

# 3. 环境变量来自 .env.local（本地 ESI）
environment:
  - EVE_CLIENT_ID=0f2b035a0dfa4487afb4fbc80668fae4  # 本地
  - EVE_CALLBACK_URL=http://localhost:12580/docker-api/auth/eve/callback

# 4. 增加 pgAdmin 工具（本地开发便利）
pgadmin:
  image: dpage/pgadmin4:latest
  container_name: eve_pgadmin
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@example.com
    PGADMIN_DEFAULT_PASSWORD: admin
  ports:
    - "5050:80"
```

---

## 🚀 启动流程详解

### 完整启动时间轴（本地）

```
命令: docker compose -f docker-compose.local.yml --env-file .env.local up -d

T+0s    Compose 读取 .env.server 文件
        ├─ 加载所有环境变量
        ├─ 验证 docker-compose.yml 语法
        └─ 创建 eve-network 网络

T+1s    启动 eve-pg 容器
        ├─ 拉取 postgres:15-alpine (~100MB，或使用本地缓存)
        ├─ 创建容器
        ├─ PostgreSQL 初始化数据库
        └─ 写入 postgres_data/ 卷

T+3s    PostgreSQL 启动完成
        ├─ 监听 0.0.0.0:5432
        ├─ 健康检查开始
        └─ pg_isready 返回成功 ✅

T+3s    启动 eve-redis 容器
        ├─ 拉取 redis:7-alpine (~50MB)
        ├─ 创建容器
        └─ Redis 启动 ✅

T+3s    eve-backend-pg 开始构建镜像
        ├─ 拉取 python:3.11-slim (~135MB)
        ├─ 执行 RUN apt-get install (~200MB)
        ├─ 执行 RUN pip install (~500MB)
        │  (asyncpg, SQLAlchemy, FastAPI 等)
        └─ 复制源代码 (~50MB)
        ⏱️ 耗时：3-5min（第一次），<30s（缓存）

T+30s   eve-backend-pg 容器启动
        ├─ FastAPI 应用初始化
        ├─ 加载 .env.dockerpg 配置
        ├─ 创建数据库连接池
        │  └─ 使用 eve-pg DNS 名称解析
        │  └─ 执行 SELECT 1 验证连接
        ├─ 连接 Redis
        └─ Uvicorn 监听 0.0.0.0:9099 ✅

T+30s   sde-processor 容器启动
        ├─ 创建数据库连接
        ├─ 连接到 eve-pg
        └─ 等待处理任务 ✅

T+35s   eve_frontend 开始构建
        ├─ 拉取 node:20-alpine (~135MB)
        ├─ npm install（安装 Vue, Vite 等）
        │  ⏱️ 耗时：2-3min（第一次），<30s（缓存）
        ├─ npm run build:docker（编译 Vue 代码）
        │  ⏱️ 耗时：1-2min
        ├─ 拉取 nginx:stable-alpine (~40MB)
        ├─ 复制 dist/ 到 Nginx 目录
        └─ Nginx 启动 ✅

T+40s   所有服务就绪
        └─ 可以开始访问应用

访问地址：
  前端: http://localhost:12580
  后端: http://localhost:19099/docker-api/docs
  数据库: localhost:5432
  Redis: 仅内部网络
  pgAdmin: http://localhost:5050 (本地仅有)
```

### 构建时间参考

| 场景 | 时间 | 说明 |
|------|------|------|
| 完全冷启动 | 8-15min | 所有镜像都需要构建 |
| 仅改代码 | <2min | 使用缓存的层 |
| 改 Python 依赖 | 3-5min | 需要重新构建后端镜像 |
| 改 Node 依赖 | 2-3min | 需要重新构建前端镜像 |
| 改配置文件 | <10s | 仅需重启容器 |

---

## 📋 常用命令

### 容器生命周期（本地）

> 本地请带上 `.env.local`（包含 DB/Redis/后端服务名变量），否则后端无法连库。

```bash
# 启动所有服务（后台）
docker compose -f docker-compose.local.yml --env-file .env.local up -d

# 启动并查看日志（前台）
docker compose -f docker-compose.local.yml --env-file .env.local up

# 停止所有服务（保留数据）
docker compose -f docker-compose.local.yml --env-file .env.local stop

# 停止并删除容器、卷等
docker compose -f docker-compose.local.yml --env-file .env.local down

# 完全清理（删除所有数据）
docker compose -f docker-compose.local.yml --env-file .env.local down -v

# 重启单个服务
docker compose -f docker-compose.local.yml --env-file .env.local restart eve-backend-pg

# 查看容器状态
docker compose -f docker-compose.local.yml --env-file .env.local ps
```

### 前端热更新（Vite Dev 容器）

```bash
# 启动后端依赖 + Vite 热更新前端
docker compose -f docker-compose.local.yml --env-file .env.local up -d eve-pg eve-redis eve-backend-pg frontend-dev

# 停止前端热更新容器
docker compose -f docker-compose.local.yml --env-file .env.local stop frontend-dev

# 查看前端热更新日志（含 HMR）
docker compose -f docker-compose.local.yml --env-file .env.local logs -f frontend-dev

# 访问地址
# 前端开发: http://localhost:5173 （HMR 端口 24678 已映射）
# 后端 API: http://localhost:19099/docker-api
```

### 镜像管理（本地）

```bash
# 构建镜像（不启动）
docker compose -f docker-compose.local.yml build

# 不使用缓存重新构建
docker compose -f docker-compose.local.yml build --no-cache

# 删除所有相关镜像
docker rmi $(docker images | grep eve | awk '{print $3}')

# 查看镜像大小
docker images | grep eve
```

### 日志查看（本地）

```bash
# 查看所有服务日志
docker compose -f docker-compose.local.yml logs

# 实时查看日志
lsof -i:5433

# 查看特定服务日志
docker compose -f docker-compose.local.yml logs eve-backend-pg

# 查看最近 100 行
docker compose -f docker-compose.local.yml logs --tail 100

# 查看某个时间之后的日志
docker compose -f docker-compose.local.yml logs --since 2h
```

---

## 🔍 诊断命令

```bash
# 查看容器详细信息
docker inspect eve_backend

# 进入容器交互式 shell
docker exec -it eve_backend /bin/bash
docker exec -it eve_db psql -U eve_admin -d eve_sde_db

# 查看容器资源占用
docker stats

# 查看网络连接
docker exec eve_backend netstat -tulpn
docker network inspect eve-project_eve-network

# 测试容器间连通性
docker exec eve_backend ping eve-pg
docker exec eve_backend nc -zv eve-pg 5432
```

---

## 相关文档

- [1-PROJECT_OVERVIEW.md](1-PROJECT_OVERVIEW.md) - 项目概览
- [3-CONFIG_ENV.md](3-CONFIG_ENV.md) - 环境配置
- [4-DEV_GUIDE.md](4-DEV_GUIDE.md) - 开发指南
- [5-TROUBLESHOOTING.md](5-TROUBLESHOOTING.md) - 故障排除
