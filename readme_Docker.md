这是一份为您目前的 **EVE Online Web 项目**定制的 Docker 开发环境 README 文档。它记录了我们在 Intel Mac (macOS 12) 上解决的所有关键配置和填过的“坑”。

---

# EVE Online Web Project - Docker 开发环境指南

本项目是基于 RuoYi-FastAPI 架构开发的 EVE Online 工具型 Web 产品。为了适配 **macOS 12 (Intel)** 环境，我们使用了特定的 Docker 版本和网络代理配置。

## 🛠 环境要求

* **操作系统**: macOS Monterey (12.x) - Intel Chip
* **Docker Desktop**: [v4.28.0](https://www.google.com/search?q=https://docs.docker.com/desktop/release-notes/4.28/) (推荐此版本以保证在旧版 macOS 上的稳定性)
* **本地数据库端口**: `15432` (避免与本地 5432 端口冲突)
* **前端访问端口**: `12580`

---

## 🏗 服务架构

本环境采用 Docker Compose 进行编排，包含以下四个核心容器：

| 容器名称 | 服务类型 | 内部端口 | 宿主机端口 | 说明 |
| --- | --- | --- | --- | --- |
| `ruoyi-pg` | PostgreSQL 15 | 5432 | **15432** | 存储 EVE SDE (raw) 与业务数据 |
| `ruoyi-redis` | Redis | 6379 | 16379 | 缓存与 Session 管理 |
| `ruoyi-backend-pg` | FastAPI (Python) | 9099 | **19099** | 后端逻辑处理 + EVE SSO |
| `ruoyi-frontend` | Nginx + Vue3 | 80 | **12580** | 前端管理界面 + API 代理 |

---

## 🚀 快速启动

1. **构建并启动所有服务**：
```zsh
docker compose up -d --build

```


2. **检查容器状态**：
```zsh
docker ps

```



---

## 💾 数据库初始化 (EVE SDE 数据灌入)

由于 EVE 的静态数据导出 (SDE) 文件较大（约 2GB），建议使用以下“物理拷贝”方式进行初始化，以防网络流中断：

1. **拷贝备份文件到容器**：
```zsh
docker cp eve_online.dump ruoyi-pg:/tmp/eve_online.dump

```


2. **执行恢复指令** (忽略 `already exists` 或 `role` 相关的 warning)：
```zsh
docker exec -it ruoyi-pg pg_restore -U postgres -d ruoyi-fastapi --no-owner /tmp/eve_online.dump

```


3. **验证数据量**：
```zsh
docker exec -it ruoyi-pg psql -U postgres -d ruoyi-fastapi -c "SELECT count(*) FROM raw.types;"

```



---

## � 开发模式：代码修改与容器重启

### 后端代码修改（Python）

**✅ 无需重启容器**（已配置热重载）

后端通过 Volume 挂载实现了代码同步：
```yaml
volumes:
  - ./ruoyi-fastapi-backend:/app
```

**修改后自动生效的情况**：
- ✓ `.py` Python 代码文件
- ✓ 业务逻辑、路由、服务层代码
- ✗ **依赖库变更**（`requirements-pg.txt`）
- ✗ **环境变量配置**（`.env.dockerpg`）

**启用热重载**：
```bash
# 修改 .env.dockerpg，将 APP_RELOAD 改为 true
APP_RELOAD = true

# 重启容器使配置生效
docker-compose restart ruoyi-backend-pg
```

**需要重启的情况**：
```bash
# 1. 安装了新的 Python 包
docker-compose build ruoyi-backend-pg
docker-compose up -d ruoyi-backend-pg

# 2. 修改了环境变量（.env.dockerpg 或 docker-compose.yml）
docker-compose restart ruoyi-backend-pg

# 3. 修改了 Dockerfile.pg
docker-compose build --no-cache ruoyi-backend-pg
docker-compose up -d ruoyi-backend-pg
```

### 前端代码修改（Vue3）

**❌ 需要重新构建镜像**

前端使用 Nginx 部署**已构建的静态文件**，不支持热重载：

```bash
# 修改前端代码后执行
cd ruoyi-fastapi-frontend
docker-compose build ruoyi-frontend
docker-compose up -d ruoyi-frontend
```

**快速验证更新**：
```bash
# 查看前端构建时间
docker exec ruoyi-frontend ls -lh /usr/share/nginx/html/index.html

# 强制刷新浏览器缓存
# macOS: Cmd + Shift + R
# 或直接清空浏览器缓存
```

### Nginx 配置修改

**✅ 仅需重启容器**（已挂载配置文件）

```yaml
volumes:
  - ./ruoyi-fastapi-frontend/bin/nginx.dockerpg.conf:/etc/nginx/conf.d/default.conf
```

**修改后重启**：
```bash
# 修改 nginx.dockerpg.conf 后
docker-compose restart ruoyi-frontend

# 验证配置是否生效
docker exec ruoyi-frontend nginx -t
```

### 数据库 Schema 修改

**✅ 使用 Alembic 迁移**（无需重启容器）

```bash
# 1. 生成迁移脚本
docker exec -it ruoyi-backend-pg alembic revision --autogenerate -m "描述"

# 2. 执行迁移
docker exec -it ruoyi-backend-pg alembic upgrade head

# 3. 回滚（如果需要）
docker exec -it ruoyi-backend-pg alembic downgrade -1
```

### 快速参考表

| 修改内容 | 是否需要重启 | 操作命令 |
| --- | --- | --- |
| 后端 `.py` 文件（热重载开启） | ❌ 否 | 自动生效，等待 1-2 秒 |
| 后端 `.py` 文件（热重载关闭） | ⚠️ 重启 | `docker-compose restart ruoyi-backend-pg` |
| 后端依赖 `requirements-pg.txt` | ✅ 重新构建 | `docker-compose build ruoyi-backend-pg` |
| 后端环境变量 `.env.dockerpg` | ⚠️ 重启 | `docker-compose restart ruoyi-backend-pg` |
| 前端 Vue 代码 | ✅ 重新构建 | `docker-compose build ruoyi-frontend` |
| Nginx 配置 | ⚠️ 重启 | `docker-compose restart ruoyi-frontend` |
| 数据库结构 | ❌ 否 | 使用 Alembic 迁移 |
| Docker Compose 配置 | ✅ 重新启动 | `docker-compose down && docker-compose up -d` |

### 开发效率优化建议

**1. 后端开发建议开启热重载**：
```bash
# .env.dockerpg 中设置
APP_RELOAD = true
```

**2. 前端本地开发模式**（推荐）：
```bash
# 在宿主机运行前端开发服务器，享受 HMR（热模块替换）
cd ruoyi-fastapi-frontend
npm run dev
# 访问 http://localhost:80，自动连接 Docker 后端
```

**3. 监控容器日志**：
```bash
# 实时查看后端日志
docker logs -f ruoyi-backend-pg

# 查看所有服务日志
docker-compose logs -f
```

---

## �🔧 关键配置说明

### 前端 Nginx 代理配置 (`nginx.dockerpg.conf`)

**Docker 环境下使用 Nginx 作为反向代理**，将前端请求转发到后端 FastAPI 服务：

```nginx
location /docker-api/ {
    # ✓ 关键：proxy_pass 不指定路径
    # 这样 Nginx 会保留客户端请求的完整路径 /docker-api/...
    # 转发给后端: http://ruoyi-backend-pg:9099/docker-api/...
    proxy_pass http://ruoyi-backend-pg:9099/;
    
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**为什么这样配置**：
- 前端请求: `http://localhost:12580/docker-api/auth/eve/login`
- Nginx 转发: `http://ruoyi-backend-pg:9099/docker-api/auth/eve/login`
- 后端预认证中间件识别 `APP_ROOT_PATH=/docker-api`，去掉前缀后路由到 `/auth/eve/login`

**常见错误**（已修正）：
```nginx
# ✗ 错误配置 - 导致路径重复
proxy_pass http://ruoyi-backend-pg:9099/docker-api/;
# 会变成: /docker-api/docker-api/auth/eve/login (404)

# ✓ 正确配置 - 保持路径原样
proxy_pass http://ruoyi-backend-pg:9099/;
```

**关键点**：
* **前端访问路径**: `http://localhost:12580/docker-api/*`
* **后端路由前缀**: `APP_ROOT_PATH=/docker-api`（需要在 `.env.dockerpg` 中配置）
* **Nginx 配置文件**: `ruoyi-fastapi-frontend/bin/nginx.dockerpg.conf`（需要重启容器才能生效）

### EVE SSO 单点登录配置

项目支持通过 EVE Online SSO 进行用户认证。**这是最重要的配置之一，任何漏项都会导致登录失败。**

#### 必需环境变量配置

在 **两个位置** 都必须配置这些变量：

**1. `.env.dockerpg` (后端环境文件)**:
```bash
# EVE SSO 相关配置
FRONTEND_URL=http://localhost:12580
EVE_CLIENT_ID=0f2b035a0dfa4487afb4fbc80668fae4
EVE_CLIENT_SECRET=eat_2EIXRPiDGUn355E63y69MfoS7ZgZTse8_1e0QXy
EVE_CALLBACK_URL=http://localhost:12580/docker-api/auth/eve/callback
APP_ROOT_PATH=/docker-api
```

**2. `docker-compose.yml` (environment 节点)**:
```yaml
environment:
  - FRONTEND_URL=http://localhost:12580
  - EVE_CLIENT_ID=0f2b035a0dfa4487afb4fbc80668fae4
  - EVE_CLIENT_SECRET=eat_2EIXRPiDGUn355E63y69MfoS7ZgZTse8_1e0QXy
  - EVE_CALLBACK_URL=http://localhost:12580/docker-api/auth/eve/callback
  - APP_ROOT_PATH=/docker-api
```

**验证配置已生效**：
```bash
# 检查环境变量是否被容器读取
docker exec ruoyi-backend-pg env | grep -E "EVE_|FRONTEND_URL|APP_ROOT_PATH"
# 应输出以上所有变量
```

#### 前端构建环境配置

**重要**：前端必须使用 Docker 环境配置，不能使用 production 配置！

`.env.docker` (已正确设置):
```dotenv
VITE_APP_BASE_API=/docker-api
```

Dockerfile 构建命令 (已修正):
```dockerfile
RUN npm run build:docker  # ✓ 正确：使用 --mode docker 加载 .env.docker
# 而不是: RUN npm run build:prod  # ✗ 错误：会使用默认配置
```

#### Nginx 代理配置

**关键**：proxy_pass 路径配置决定了请求能否正确到达后端

`nginx.dockerpg.conf` (已修正):
```nginx
location /docker-api/ {
    proxy_pass http://ruoyi-backend-pg:9099/;
    # ✓ 不指定路径，让 Nginx 保留 /docker-api/ 前缀传给后端
    # ✗ 错误示例: proxy_pass http://ruoyi-backend-pg:9099/docker-api/; (会导致路径重复)
    
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**为什么这样配置**：后端有 `pre_auth` 中间件会自动识别并去掉 `APP_ROOT_PATH` 前缀，因此 Nginx 只需转发完整路径。

#### 完整 EVE SSO 登录流程

```
┌─────────────────────────────────────────────────────────────┐
│ 用户点击 "Login with EVE SSO" 按钮                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 前端跳转: http://localhost:12580/docker-api/auth/eve/login  │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
    ┌─────────────┐        ┌────────────────┐
    │  Nginx 代理  │        │  路径检查      │
    │ 接收请求    │        │ /docker-api/   │
    └──────┬──────┘        └────────┬───────┘
           │                        │
           └────────────┬───────────┘
                        ▼
        ┌───────────────────────────────┐
        │ 转发: http://backend:9099/     │
        │       docker-api/auth/eve/... │
        └──────────────┬────────────────┘
                       ▼
        ┌───────────────────────────────┐
        │ 后端 pre_auth 中间件           │
        │ 识别 APP_ROOT_PATH = /docker-api
        │ 去掉前缀，路由到 /auth/eve/... │
        └──────────────┬────────────────┘
                       ▼
        ┌───────────────────────────────┐
        │ /auth/eve/login 处理           │
        │ 1. 生成 state 保存到 Redis     │
        │ 2. 生成 EVE OAuth URL         │
        │ 3. 307 重定向                 │
        └──────────────┬────────────────┘
                       ▼
        ┌───────────────────────────────────────┐
        │ 跳转: https://login.eveonline.com/... │
        │ scope: publicData                     │
        └───────────────┬─────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────┐
        │ 用户在 EVE CCP 页面授权         │
        │ 返回 code 和 state              │
        └───────────────┬────────────────┘
                        ▼
        ┌──────────────────────────────────────┐
        │ CCP 重定向: /docker-api/auth/eve/    │
        │            callback?code=...&state=  │
        └───────────────┬────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
    ┌──────────┐              ┌──────────────┐
    │Nginx代理 │              │路径检查      │
    └────┬─────┘              └────┬─────────┘
         │                         │
         └──────────┬──────────────┘
                    ▼
        ┌────────────────────────────┐
        │ 转发: http://backend:9099/ │
        │       docker-api/auth/...  │
        └────────────┬───────────────┘
                     ▼
        ┌────────────────────────────┐
        │ /auth/eve/callback 处理     │
        │ 1. 验证 state（Redis检查）  │
        │ 2. 交换 code 获取 token    │
        │ 3. 查询用户信息            │
        │ 4. 创建/更新用户           │
        │ 5. 生成系统 JWT            │
        │ 6. 307 重定向              │
        └────────────┬───────────────┘
                     ▼
        ┌────────────────────────────────────┐
        │ 重定向: http://localhost:12580/    │
        │         ?token=eyJ...              │
        │ （token 包含用户信息和权限）        │
        └────────────┬─────────────────────┘
                     ▼
        ┌──────────────────────────────┐
        │ 前端路由守卫捕获 URL 中的 token │
        └────────────┬─────────────────┘
                     ▼
        ┌────────────────────────────────┐
        │ 保存 token 到 localStorage      │
        │ 清除 URL 中的 query 参数       │
        │ 跳转到首页 (/)                 │
        └────────────┬───────────────────┘
                     ▼
        ┌─────────────────────────────┐
        │ ✅ 登陆成功！                 │
        │ 用户进入管理系统             │
        └─────────────────────────────┘
```

#### 调试 SSO 问题

如果 SSO 登录失败，按以下顺序排查：

1. **检查配置是否完整**：
   ```bash
   # 后端环境变量
   docker exec ruoyi-backend-pg env | grep EVE_
   docker exec ruoyi-backend-pg env | grep FRONTEND_URL
   docker exec ruoyi-backend-pg env | grep APP_ROOT_PATH
   
   # 前端构建配置
   docker exec ruoyi-frontend grep "docker-api" /usr/share/nginx/html/static/js/*.js | head -1
   ```

2. **测试 API 端点**：
   ```bash
   # 测试登录端点是否可访问
   curl -v http://localhost:12580/docker-api/auth/eve/login
   # 应返回: HTTP/1.1 307 Temporary Redirect
   # Location: https://login.eveonline.com/v2/oauth/authorize/?...
   ```

3. **查看后端日志**：
   ```bash
   # 监控 EVE SSO 相关日志
   docker logs -f ruoyi-backend-pg | grep -i "eve\|sso\|oauth"
   ```

4. **验证 Redis 连接**：
   ```bash
   # state 保存在 Redis 中，检查 Redis 是否可用
   docker exec ruoyi-backend-pg redis-cli -h ruoyi-redis ping
   # 应返回: PONG
   ```

### 后端数据库连接

本地 Python 开发环境直连 Docker 数据库时，请使用以下配置：

* **HOST**: `127.0.0.1`
* **PORT**: `15432`
* **USER/PASS**: `postgres` / `root`
## 🧪 功能测试

### 验证 API 服务可用性

```bash
# 测试 Swagger 文档访问
curl -s http://localhost:12580/docker-api/docs | grep -o "title" | head -1

# 测试后端健康状态
curl http://localhost:12580/docker-api/getInfo
# 应返回: {"code":401,"msg":"未授权，请先登录",...}
```

### 测试 EVE SSO 登录

1. **浏览器访问**: `http://localhost:12580`
2. **点击右上角**: "Login with EVE SSO" 按钮
3. **验证跳转**: 应跳转至 `https://login.eveonline.com/...`
4. **授权后**: 自动返回系统并完成登录

**查看 SSO 日志**：
```bash
docker logs ruoyi-backend-pg --tail 50 | grep -i "eve\|sso"
```

## ⚠️ 常见问题排查 (Troubleshooting)

### 1. 点击登录按钮后提示"请先登录"

**可能原因**：
- A. 前端 API 基础 URL 配置错误
- B. Nginx 代理配置错误
- C. 后端环境变量未正确加载
- D. 前端构建使用了错误的环境配置

**排查步骤**：

```bash
# 1️⃣ 验证前端使用的是 Docker 配置（/docker-api）
docker exec ruoyi-frontend grep -o "docker-api" /usr/share/nginx/html/static/js/*.js | wc -l
# 应该返回多个匹配（表示 /docker-api 被构建进了前端代码）

# 2️⃣ 检查 Nginx 配置
docker exec ruoyi-frontend cat /etc/nginx/conf.d/default.conf | grep -A 5 "location /docker-api"
# 应该看到: proxy_pass http://ruoyi-backend-pg:9099/;

# 3️⃣ 验证后端环境变量
docker exec ruoyi-backend-pg env | grep -E "APP_ROOT_PATH|EVE_|FRONTEND_URL"
# 应显示所有 EVE SSO 和路径配置

# 4️⃣ 测试 API 路径是否可访问
curl -I http://localhost:12580/docker-api/auth/eve/login
# 应返回: HTTP/1.1 307 Temporary Redirect
```

**解决方案**：
- 如果步骤 1 失败：重新构建前端镜像（`docker-compose build --no-cache ruoyi-frontend`）
- 如果步骤 2 失败：修改 `nginx.dockerpg.conf`，重启容器（`docker-compose restart ruoyi-frontend`）
- 如果步骤 3 失败：检查 `.env.dockerpg` 和 `docker-compose.yml`，重启后端（`docker-compose restart ruoyi-backend-pg`）
- 如果步骤 4 失败：检查网络连接或 Nginx 配置

### 2. EVE SSO 回调失败（授权后无反应或跳转错误）

**症状**：
- 授权后返回 404 或 500 错误页面
- 无限重定向
- "请先登录" 提示

**排查步骤**：

```bash
# 1️⃣ 验证 EVE_CALLBACK_URL 配置
docker exec ruoyi-backend-pg env | grep EVE_CALLBACK_URL
# 应输出: EVE_CALLBACK_URL=http://localhost:12580/docker-api/auth/eve/callback

# 2️⃣ 检查 Redis 连接（state 和 session 保存在 Redis）
docker exec ruoyi-backend-pg redis-cli -h ruoyi-redis ping
# 应返回: PONG

# 3️⃣ 查看后端日志，搜索 EVE 相关的错误
docker logs ruoyi-backend-pg --tail 100 | grep -i "eve\|sso\|callback\|error"

# 4️⃣ 测试回调路由是否存在
curl -I http://localhost:12580/docker-api/auth/eve/callback?code=test&state=test
# 应返回 400（缺少有效 code/state）而不是 404（路由不存在）
```

**常见原因及解决**：
- **404 Not Found**: Nginx 代理配置错误（见问题 1 的步骤 2）
- **Redis 连接失败**: 检查 `ruoyi-redis` 容器是否运行（`docker ps | grep redis`）
- **State 验证失败**: 清除浏览器 Cookie 和本地存储，重新尝试登录
- **Token 生成失败**: 检查后端日志中是否有数据库错误

### 3. 404 Not Found 错误

**根本原因**：Nginx 代理路径与后端路由路径不匹配

**检查清单**：
```bash
# ✓ 前端配置
grep "VITE_APP_BASE_API" ruoyi-fastapi-frontend/.env.docker
# 应输出: VITE_APP_BASE_API=/docker-api

# ✓ 后端配置
grep "APP_ROOT_PATH" ruoyi-fastapi-backend/.env.dockerpg
# 应输出: APP_ROOT_PATH=/docker-api

# ✓ Nginx 配置
docker exec ruoyi-frontend cat /etc/nginx/conf.d/default.conf | grep -A 2 "location /docker-api"
# proxy_pass 应该是: http://ruoyi-backend-pg:9099/;

# ✓ 验证路径是否一致
# 前端: /docker-api ✓
# 后端: /docker-api ✓
# Nginx: 保留路径 ✓
```

**修复步骤**（按顺序）：
1. 修改 Nginx 配置文件 `nginx.dockerpg.conf`
2. 重启前端容器：`docker-compose restart ruoyi-frontend`
3. 检查 `.env.dockerpg` 中的 `APP_ROOT_PATH=/docker-api`
4. 重启后端容器：`docker-compose restart ruoyi-backend-pg`
5. 强制刷新前端：`Cmd+Shift+R`（清除浏览器缓存）

### 4. 前端显示"400 Bad Request"或"未授权，请先登录"

**原因**：API 请求路径正确，但缺少有效的 JWT token

**验证步骤**：
```bash
# 检查浏览器 localStorage 中是否有 token
# 打开浏览器开发者工具 (F12) → Application → Local Storage → http://localhost:12580
# 查找 "Authorization" 或 "token" 字段

# 如果没有 token，说明登录流程未完成
# 检查登录过程中是否有错误消息
docker logs ruoyi-backend-pg --tail 50 | grep -i "login\|auth"
```

**解决方案**：
- 清除浏览器 Cookie 和 Local Storage
- 清除 Redis 中的过期 session：`docker exec ruoyi-redis redis-cli FLUSHDB`
- 重新开始登录流程

### 5. Docker Pull 失败（拉取镜像超时）

**原因**：网络连接问题或官方源速度慢

**解决方案**：在 Docker Desktop 设置中配置国内镜像加速器：
```json
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
```

然后重试：
```bash
docker-compose pull
docker-compose build --no-cache
```

### 6. Intel Mac 性能问题（数据库查询缓慢）

**症状**：
- 登录响应缓慢（>5 秒）
- 数据库查询超时
- CPU 占用率高

**解决方案**：调整 Docker Desktop 资源配置：
- **Preferences** → **Resources**
- **Memory**: 增加至 4GB 以上
- **CPU**: 分配 2-4 核心
- **Disk Image Size**: 至少保留 20GB 可用空间

```bash
# 验证配置是否生效
docker stats --no-stream

# 查看数据库性能
docker exec -it ruoyi-pg psql -U postgres -d ruoyi-fastapi -c "SELECT version();"
```

### 7. 找不到 `nginx.dockerpg.conf` 文件

**错误示例**：
```
ERROR: Service 'ruoyi-frontend' failed to build: COPY failed: file not found in build context
```

**原因**：Dockerfile 中的 COPY 路径错误或文件不在预期位置

**解决方案**：
```bash
# 验证文件路径
ls -la ruoyi-fastapi-frontend/bin/nginx.dockerpg.conf

# 确保在项目根目录执行 docker-compose 命令
pwd
# 应输出包含 docker-compose.yml 的目录

# 重新构建
docker-compose build --no-cache ruoyi-frontend
```

## 📊 容器状态监控

```bash
# 查看所有容器状态
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 查看资源占用
docker stats --no-stream

# 查看网络连接
docker network inspect ruoyi-network
```

## 🔐 安全注意事项

**生产环境部署时务必修改**：
- [ ] 修改数据库密码 (当前: `postgres/root`)
- [ ] 更新 JWT 密钥 (`JWT_SECRET_KEY`)
- [ ] 配置 HTTPS 证书
- [ ] 限制数据库外部访问 (移除端口映射 `15432:5432`)
- [ ] 使用环境变量或密钥管理服务存储 `EVE_CLIENT_SECRET`

## 📚 相关文档

- [EVE SSO 集成说明](ruoyi-fastapi-backend/README-SSO.md)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Docker Compose 参考](https://docs.docker.com/compose/)

---

**文档更新日期**: 2026年1月16日  
**适用版本**: Docker Desktop 4.28.0 / macOS 12 Intel


* **进入数据库命令行**：
```zsh
docker exec -it ruoyi-pg psql -U postgres -d ruoyi-fastapi

```


* **完全重置前端** (当遇到 `npm` 缓存或 `matches` 报错时)：
```zsh
# 在 frontend 目录下执行
rm -rf node_modules package-lock.json
docker compose build --no-cache ruoyi-frontend

```



---

## ⚠️ 常见问题排查 (Troubleshooting)

* **404 Not Found**: 检查 `vite.config.js` 中的 `proxy` 是否为 `/docker-api`，并确保 `VITE_APP_BASE_API` 在 `.env.docker` 中正确对齐。
* **Docker Pull 失败**: 请在 Docker Desktop 设置中配置国内镜像加速器 (如 `daocloud.io` 或 `unidock.top`)。
* **Intel Mac 性能限制**: 如果数据库查询缓慢，请在 Docker Resources 设置中将内存分配增加至 **4GB** 以上。

---

## 📝 关键修复历史（2026年1月16日）

本文档在成功实现 EVE SSO 登陆流程后进行了重大更新。以下是修复过程中发现和解决的关键问题：

### 问题 1：Nginx 路径重复（404 Not Found）
**症状**：请求变成 `/docker-api/docker-api/auth/eve/callback`

**根本原因**：`proxy_pass http://ruoyi-backend-pg:9099/docker-api/;` 指定了路径

**修复**：改为 `proxy_pass http://ruoyi-backend-pg:9099/;` 让 Nginx 保留完整路径

### 问题 2：SSO 回调重定向错误（405 Method Not Allowed）
**症状**：EVE SSO 授权后重定向到 `/index?token=...` 返回 405 错误

**根本原因**：前端是 SPA（单页应用），访问 `/index` 实际是 HTTP 请求，而非路由

**修复**：改为重定向到 `/?token=...`，让前端路由处理

### 问题 3：前端 API 路径错误（API 基础 URL 不匹配）
**症状**：`import.meta.env.VITE_APP_BASE_API` 在构建时设为 `/index` 而不是 `/docker-api`

**根本原因**：Dockerfile 使用 `npm run build:prod` 而不是 `npm run build:docker`

**修复**：改为 `RUN npm run build:docker` 加载 `.env.docker` 配置

### 问题 4：本地开发 Vite 代理配置（本地前端连接 Docker 后端）
**症状**：Vite 代理指向 `http://ruoyi-backend-pg:8080`（Docker DNS 和错误的端口）

**根本原因**：
- 使用了 Docker 容器内部的 DNS 名称，在 macOS 主机上无法解析
- 后端实际运行在 9099 端口，不是 8080

**修复**：改为 `http://127.0.0.1:19099`（localhost 和正确的宿主机端口）

### 问题 5：缺少 EVE SSO 环境变量
**症状**：后端没有收到 EVE OAuth 凭证

**根本原因**：`.env.dockerpg` 没有配置 EVE SSO 相关的环境变量

**修复**：添加 `EVE_CLIENT_ID`, `EVE_CLIENT_SECRET`, `EVE_CALLBACK_URL`, `FRONTEND_URL` 到：
- `.env.dockerpg`（后端环境文件）
- `docker-compose.yml` environment 节点

### 总结
**最关键的三个配置点**：
1. **前端**：必须使用 Docker 环境配置（`npm run build:docker`），不能用 production
2. **后端**：必须在 `.env.dockerpg` 和 `docker-compose.yml` 中都配置 EVE SSO 和路径变量
3. **Nginx**：`proxy_pass` 不能指定路径，让后端的预认证中间件处理路径前缀

---

**文档更新日期**: 2026年1月16日  
**适用版本**: Docker Desktop 4.28.0 / macOS 12 Intel / EVE FastAPI v1.0  
**最后验证**: ✅ EVE SSO 登陆流程完全正常