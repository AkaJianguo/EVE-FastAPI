# 环境配置管理

> 完整的环境变量体系、配置文件、加载流程、优先级说明

## 🔄 配置体系架构

### 三层配置结构

```
┌─────────────────────────────────────────────────────────┐
│ 层 1: Docker Compose 编排层                            │
│ ─────────────────────────────────────────────────────  │
│  文件: .env.server / .env.local                         │
│  作用: 被 docker-compose up -d --env-file 读取         │
│  用途: 用于 docker-compose.yml 中的 ${VAR} 替换       │
│       同时注入到容器的环境变量                          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 层 2: 应用配置层                                        │
│ ─────────────────────────────────────────────────────  │
│  文件: .env.dockerpg (后端) / .env.docker (前端)       │
│  作用: 应用启动时读取 (python app.py --env=dockerpg)  │
│  用途: 后端 FastAPI 应用加载配置                      │
│       前端 Vite 编译时加载配置                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 层 3: 代码内置层                                        │
│ ─────────────────────────────────────────────────────  │
│  文件: config/env.py (Pydantic BaseSettings)           │
│  作用: 代码中定义的默认值                              │
│  用途: 未在 .env 文件中定义时使用默认值              │
└─────────────────────────────────────────────────────────┘
```

### 配置优先级

```
优先级（从高到低）：

1️⃣  Docker 环境变量（来自 docker-compose.yml 的 environment: 部分）
    示例：- EVE_CLIENT_ID=0f2b035a0dfa4487...
    ├─ Docker Compose 从 .env 文件中加载
    ├─ 注入到容器的环境变量
    └─ 被应用代码 os.environ 读取

2️⃣  .env.dockerpg / .env.docker 文件
    示例：EVE_CLIENT_ID = '0f2b035a0dfa4487...'
    ├─ 应用启动时加载
    ├─ python-dotenv 库读取
    └─ 覆盖后续的其他配置源

3️⃣  代码中的默认值
    示例：eve_client_id: str | None = None
    ├─ Pydantic BaseSettings 定义
    ├─ 如果环境变量和 .env 文件都未定义则使用
    └─ 最低优先级

✅ 实际加载顺序：
  1. Docker 启动容器，注入 environment: 中的变量
  2. 应用读取 os.environ（已包含 Docker 注入的变量）
  3. python-dotenv 加载 .env.dockerpg
  4. Pydantic 读取所有来源并合并
  5. 最终优先级：Docker > .env file > 默认值
```

---

## 📝 配置文件详解

### 1. `.env.server`（生产环境）

**位置**：`/opt/EVE-Project/.env.server`

**用途**：被 `docker-compose.server.yml` 读取，注入生产环境配置

```bash
# ============ 编排层 - 数据库配置 ============
DB_CONTAINER_NAME=eve_db          # 容器名称
DB_USER=eve_admin                 # 数据库用户
DB_PASSWORD=y20Vnn4FfPDPZJidY9LuiGtU  # 数据库密码
DB_NAME=eve_sde_db                # 数据库名称
DB_EXTERNAL_PORT=5432             # 外部端口映射

# ============ 编排层 - 端口映射 ============
BACKEND_EXTERNAL_PORT=19099       # 后端外部端口
FRONTEND_EXTERNAL_PORT=12580      # 前端外部端口

# ============ 编排层 - EVE SSO 配置（生产） ============
EVE_CLIENT_ID=0c7843bbd96b4c72b75eaef102aac87c        # CCP 应用 ID
EVE_CLIENT_SECRET=eat_1BhuyrlooQhrfM3vHQGXISRFut3cz2hEq_4fE3cT  # CCP 应用密钥
EVE_CALLBACK_URL=http://43.163.228.205:12580/docker-api/auth/eve/callback  # 回调地址
FRONTEND_URL=http://43.163.228.205:12580              # 前端地址

# ============ 编排层 - Docker 服务名 ============
DB_SERVICE_NAME=eve-pg            # 数据库服务名（容器间通信用）
REDIS_SERVICE_NAME=eve-redis      # Redis 服务名
BACKEND_SERVICE_NAME=eve-backend-pg  # 后端服务名
BACKEND_HOST=eve-backend-pg       # Nginx 代理目标服务名
```

### 2. `.env.local`（本地开发）

**位置**：`/opt/EVE-Project/.env.local`

**用途**：被 `docker-compose.local.yml` 读取，注入本地开发配置

```bash
# ============ 编排层 - 数据库配置 ============
DB_CONTAINER_NAME=eve_db_local    # 容器名称
DB_USER=eve_admin                  # 本地用户
DB_PASSWORD=root                  # 本地密码
DB_NAME=eve_db             # 本地数据库名
DB_EXTERNAL_PORT=15432            # 避免冲突，使用 15432

# ============ 编排层 - 端口映射 ============
BACKEND_EXTERNAL_PORT=19099       # 后端外部端口（同生产）
FRONTEND_EXTERNAL_PORT=12580      # 前端外部端口（同生产）

# ============ 编排层 - EVE SSO 配置（本地） ============
EVE_CLIENT_ID=0f2b035a0dfa4487afb4fbc80668fae4        # 本地开发 ESI ID
EVE_CLIENT_SECRET=eat_2EIXRPiDGUn355E63y69MfoS7ZgZTse8_1e0QXy  # 本地开发 ESI 密钥
EVE_CALLBACK_URL=http://localhost:12580/docker-api/auth/eve/callback  # 本地回调地址
FRONTEND_URL=http://localhost:12580                   # 本地前端地址

# ============ 编排层 - Docker 服务名 ============
DB_SERVICE_NAME=eve-pg            # 数据库服务名（与生产相同）
REDIS_SERVICE_NAME=eve-redis      # Redis 服务名（与生产相同）
BACKEND_SERVICE_NAME=eve-backend-pg  # 后端服务名（与生产相同）
BACKEND_HOST=eve-backend-pg       # Nginx 代理目标服务名（与生产相同）
```

**关键差异对比**：

| 配置项 | 生产 | 本地 |
|--------|------|------|
| `DB_EXTERNAL_PORT` | 5432 | 15432 |
| `EVE_CLIENT_ID` | 0c7843... | 0f2b035a... |
| `EVE_CALLBACK_URL` | http://43.163.228.205:... | http://localhost:... |
| `FRONTEND_URL` | http://43.163.228.205:... | http://localhost:... |

### 3. `.env.dockerpg`（后端应用配置）

**位置**：`/opt/EVE-Project/EVE-FastAPI/EVE-fastapi-backend/.env.dockerpg`

**用途**：后端容器启动时 (python app.py --env=dockerpg) 被加载

**特点**：此文件中的值会被 Docker Compose 环境变量覆盖

```bash
# -------- 应用配置 --------
APP_ENV = 'dockerpg'              # 环境标识
APP_NAME = 'RuoYi-FastAPI'        # 应用名称
APP_ROOT_PATH = '/docker-api'     # ⭐ 必须与 Nginx 一致
APP_HOST = '0.0.0.0'
APP_PORT = 9099
APP_RELOAD = false                # Docker 不启用热重载
APP_IP_LOCATION_QUERY = true      # IP 地址查询

# -------- 数据库配置 --------
# ⭐ 重要：Docker 环境变量会覆盖这些值
DB_HOST = 'eve-pg'                # 容器服务名
DB_PORT = 5432
DB_USERNAME = 'postgres'
DB_PASSWORD = 'root'              # Docker 会覆盖为真实密码
DB_DATABASE = 'ruoyi-fastapi'

# -------- Redis 配置 --------
REDIS_HOST = 'eve-redis'          # 容器服务名
REDIS_PORT = 6379
REDIS_PASSWORD = ''

# -------- EVE SSO 配置 --------
# ⭐ 重要：Docker 环境变量会覆盖这些值
EVE_CLIENT_ID = '0f2b035a0dfa4487afb4fbc80668fae4'
EVE_CLIENT_SECRET = 'eat_2EIXRPiDGUn355E63y69MfoS7ZgZTse8_1e0QXy'
EVE_CALLBACK_URL = 'http://localhost:12580/docker-api/auth/eve/callback'
FRONTEND_URL = 'http://localhost:12580'
```

### 4. `.env.docker`（前端编译配置）

**位置**：`/opt/EVE-Project/EVE-FastAPI/EVE-fastapi-frontend/.env.docker`

**用途**：前端构建时 (npm run build:docker) 被加载

```bash
# Vite 应用配置
VITE_APP_BASE_API=/docker-api     # ⭐ 必须与后端 APP_ROOT_PATH 一致
VITE_APP_TITLE=EVE Online Manager
```

**说明**：
- 前端构建时，Vite 会将 `VITE_APP_BASE_API` 替换为编译后的代码
- 所有 API 请求都会以 `/docker-api` 为前缀
- 必须与后端 `APP_ROOT_PATH = '/docker-api'` 一致

---

## 🔧 配置加载流程

### 后端配置加载 (`config/env.py`)

```python
# 步骤 1: 解析命令行参数
import sys
import argparse

if 'alembic' in sys.argv:
    # Alembic 迁移: 从 alembic.ini 读取
    env_value = ini_config['settings'].get('env')
elif 'uvicorn' in sys.argv:
    # Uvicorn 直接启动: 跳过自定义参数
    pass
else:
    # 正常启动: python app.py --env=dockerpg
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default='')
    args = parser.parse_args()
    os.environ['APP_ENV'] = args.env or 'dev'

# 步骤 2: 根据环境加载 .env 文件
from dotenv import load_dotenv

run_env = os.environ.get('APP_ENV', '')
env_file = f'.env.{run_env}' if run_env else '.env.dev'
load_dotenv(env_file)  # 加载 .env.dockerpg

# 步骤 3: 通过 Pydantic BaseSettings 读取配置
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    app_env: str = Field(default='dev', alias='APP_ENV')
    app_name: str = Field(default='RuoYi-FastAPI', alias='APP_NAME')
    app_port: int = Field(default=9099, alias='APP_PORT')
    # 优先级：环境变量 > .env 文件 > 默认值
    
    class Config:
        env_file = '.env.dockerpg'  # 指定 .env 文件路径
        case_sensitive = False

# 最终优先级：
# 1. Docker Compose 环境变量（os.environ）
# 2. .env.dockerpg 文件
# 3. 代码中的默认值
```

### 容器启动流程详解

```
docker-compose up -d 执行
    ↓
读取 --env-file .env.server 文件
├─ DB_USER=eve_admin
├─ EVE_CLIENT_ID=0c7843...
└─ ... 所有变量加载完成

创建容器（eve-backend-pg）
    ↓
Docker 注入环境变量到容器
├─ export DB_USER=eve_admin
├─ export EVE_CLIENT_ID=0c7843...
└─ ... 所有变量在容器内可访问

容器启动命令执行
├─ CMD: python app.py --env=dockerpg
    ↓
    app.py 启动
    ├─ config/env.py 解析 --env=dockerpg 参数
    ├─ load_dotenv('.env.dockerpg') 加载文件
    ├─ Pydantic 读取配置源：
    │  ① os.environ（Docker 注入的优先级最高）✅
    │  ② .env.dockerpg（python-dotenv 加载）
    │  ③ 代码默认值（最低优先级）
    └─ 合并后的配置
    
    最终值示例：
    DB_USER = 'eve_admin'         ✅ 来自 Docker 注入
    EVE_CLIENT_ID = '0c7843...'   ✅ 来自 Docker 注入
    APP_ROOT_PATH = '/docker-api' ✅ 来自 .env.dockerpg
    
    ↓
FastAPI 应用初始化 ✅
```

---

## ✅ 配置验证清单

### 启动前检查

```bash
# 1. 检查 .env.server 存在且有效
cat /opt/EVE-Project/.env.server | grep EVE_CLIENT_ID

# 2. 检查 .env.local 存在且有效
cat /opt/EVE-Project/.env.local | grep EVE_CLIENT_ID

# 3. 检查后端应用配置
grep -E "DB_HOST|APP_ROOT_PATH" /opt/EVE-Project/EVE-FastAPI/EVE-fastapi-backend/.env.dockerpg

# 4. 检查前端构建配置
grep VITE_APP_BASE_API /opt/EVE-Project/EVE-FastAPI/EVE-fastapi-frontend/.env.docker

# 5. 检查 docker-compose 文件
docker-compose -f docker-compose.server.yml config | grep -A 3 "EVE_CLIENT"
```

### 运行中检查

```bash
# 1. 检查容器内的环境变量
docker exec eve_backend env | grep EVE

# 2. 检查后端是否加载正确配置
docker logs eve_backend | grep "APP_ROOT_PATH\|EVE_CLIENT_ID"

# 3. 测试 API 连通性
curl http://localhost:19099/docker-api/docs

# 4. 测试数据库连接
docker exec eve_backend python -c "import psycopg2; psycopg2.connect('postgresql://eve_admin:pwd@eve-pg:5432/eve_sde_db')"

# 5. 测试 Nginx 代理
curl -v http://localhost:12580/docker-api/auth/login
```

---

## 🎯 常见配置错误

### 错误 1: EVE SSO 回调失败

**症状**：`EVE_CALLBACK_URL 与后台配置不一致`

**原因分析**：

```bash
# 生产环境
EVE_CALLBACK_URL=http://43.163.228.205:12580/docker-api/auth/eve/callback
# 与 CCP 后台配置必须完全一致（一个字符都不能差）

# ❌ 错误
EVE_CALLBACK_URL=http://43.163.228.205:12580/auth/eve/callback
# 缺少 /docker-api 前缀

# ❌ 错误
EVE_CALLBACK_URL=http://43.163.228.205:19099/docker-api/auth/eve/callback
# 使用了后端端口（应该用前端 Nginx 端口 12580）
```

**修复**：确保三处配置一致
1. `.env.server` 中的 `EVE_CALLBACK_URL`
2. `EVE-fastapi-backend/.env.dockerpg` 中的 `EVE_CALLBACK_URL`
3. CCP 应用管理后台中的回调 URL

### 错误 2: 数据库连接失败

**症状**：`ConnectionRefusedError: connect to eve-pg:5432 failed`

**原因分析**：

```bash
# ❌ 错误：使用了容器 ID
DB_HOST = 'abc123def456'

# ✅ 正确：使用服务名
DB_HOST = 'eve-pg'

# ❌ 错误：使用了宿主机地址
DB_HOST = 'localhost'  # 容器内 localhost 是容器本身，不是数据库

# ❌ 错误：使用了宿主机 IP
DB_HOST = '192.168.1.100'  # 容器网络隔离
```

**修复**：
```bash
# 在 .env.dockerpg 中修改
DB_HOST = 'eve-pg'  # 使用 docker-compose.yml 中定义的服务名

# 在 docker-compose 的 environment 中也要用服务名
environment:
  - DB_HOST=eve-pg  # 不要用 localhost 或 IP
```

### 错误 3: API 路由 404

**症状**：`GET /docker-api/auth/login 404 Not Found`

**原因分析**：

```bash
# ❌ 错误：路由前缀不一致
APP_ROOT_PATH = '/api'       # 后端
VITE_APP_BASE_API = '/docker-api'  # 前端
# → 前端请求 /docker-api/... 但后端期望 /api/...

# ✅ 正确：路由前缀一致
APP_ROOT_PATH = '/docker-api'
VITE_APP_BASE_API = '/docker-api'

# ❌ 错误：Nginx 代理配置不匹配
location /docker-api/ {
    proxy_pass http://eve-backend-pg:9099/docker-api/;
    # 会导致路径重复：/docker-api/docker-api/...
}

# ✅ 正确：Nginx 代理不指定路径
location /docker-api/ {
    proxy_pass http://eve-backend-pg:9099/;
    # 保持原路径：/docker-api/auth/login
}
```

**修复**：确保三处一致
1. 后端：`APP_ROOT_PATH = '/docker-api'`
2. 前端：`VITE_APP_BASE_API = '/docker-api'`
3. Nginx：`location /docker-api/ { proxy_pass http://...:9099/; }`

---

## 📊 配置总结表

| 配置项 | 类型 | 本地 | 生产 | 说明 |
|--------|------|------|------|------|
| `DB_EXTERNAL_PORT` | 编排层 | 15432 | 5432 | 宿主机端口 |
| `EVE_CLIENT_ID` | 编排层 | 0f2b035a... | 0c7843... | CCP 应用 ID |
| `EVE_CALLBACK_URL` | 编排层 | localhost:12580 | 43.163.228.205:12580 | 回调地址 |
| `DB_HOST` | 应用层 | eve-pg | eve-pg | Docker 服务名 |
| `APP_ROOT_PATH` | 应用层 | /docker-api | /docker-api | 路由前缀 |
| `VITE_APP_BASE_API` | 应用层 | /docker-api | /docker-api | 前端 API 前缀 |

---

## 📖 相关文档

- [1-PROJECT_OVERVIEW.md](1-PROJECT_OVERVIEW.md) - 项目概览
- [2-DOCKER_BUILD.md](2-DOCKER_BUILD.md) - Docker 构建与部署
- [4-DEV_GUIDE.md](4-DEV_GUIDE.md) - 开发指南
- [5-TROUBLESHOOTING.md](5-TROUBLESHOOTING.md) - 故障排除
