# 开发指南

> 本地开发、代码修改、热重载、调试方法

## 🛠️ 本地开发环境

### 快速启动

```bash
# 1. 启动所有服务
cd /opt/EVE-Project
docker-compose -f docker-compose.local.yml --env-file .env.local up -d

# 2. 查看日志确保无错误
docker-compose -f docker-compose.local.yml logs -f

# 3. 访问应用
# 前端: http://localhost:12580
# API Docs: http://localhost:19099/docker-api/docs
# pgAdmin: http://localhost:5050
```

### 服务状态检查

```bash
# 查看容器状态
docker-compose -f docker-compose.local.yml ps

# 预期输出：
# NAME              STATUS      PORTS
# eve_db_local      Up ...      0.0.0.0:15432->5432/tcp
# eve-redis         Up ...      
# eve_backend       Up ...      0.0.0.0:19099->9099/tcp
# eve_frontend      Up ...      0.0.0.0:12580->80/tcp
# eve_pgadmin       Up ...      0.0.0.0:5050->80/tcp

# 检查所有容器就绪
docker-compose -f docker-compose.local.yml exec eve-pg pg_isready
docker-compose -f docker-compose.local.yml exec eve-redis redis-cli ping
```

---

## 💻 后端开发

### 修改代码流程

#### 场景 1: 修改 `.py` 文件（热重载）

**假设：启用了热重载** （`APP_RELOAD = true` 在 `.env.dockerpg`）

```bash
# 1. 修改 Python 文件
vim EVE-FastAPI/EVE-fastapi-backend/module_admin/controller/login_controller.py

# 2. 保存文件（自动同步到容器，因为有 Volume 挂载）
# 如果 APP_RELOAD=true，Uvicorn 会自动检测到文件变化并重启

# 3. 等待 1-2 秒，服务自动重新加载
# 无需重启容器，直接测试 API

# 4. 查看日志确认重载成功
docker logs eve_backend | tail -20
# 应该看到 "Uvicorn running on" 或类似的日志

# 5. 在浏览器中刷新测试
curl http://localhost:19099/docker-api/docs
```

**不启用热重载时** （`APP_RELOAD = false`）

```bash
# 需要手动重启容器
docker-compose -f docker-compose.local.yml restart eve-backend-pg

# 等待 ~5 秒服务重启
docker-compose -f docker-compose.local.yml logs eve-backend-pg | tail -20
```

#### 场景 2: 安装新的 Python 依赖

```bash
# 1. 修改依赖文件
vim EVE-FastAPI/EVE-fastapi-backend/requirements-pg.txt
# 添加新的包：
# numpy==1.24.0

# 2. 重新构建镜像（会重新执行 pip install）
docker-compose -f docker-compose.local.yml build eve-backend-pg
# ⏱️ 耗时 3-5 分钟

# 3. 重启服务
docker-compose -f docker-compose.local.yml up -d eve-backend-pg

# 4. 验证依赖已安装
docker exec eve_backend python -c "import numpy; print(numpy.__version__)"
```

#### 场景 3: 修改环境变量配置

```bash
# 1. 修改 .env.local
vim .env.local
# 或者修改 .env.dockerpg
vim EVE-FastAPI/EVE-fastapi-backend/.env.dockerpg

# 2. 重启容器（使新配置生效）
docker-compose -f docker-compose.local.yml restart eve-backend-pg

# 3. 验证新配置已加载
docker logs eve_backend | grep "new_config_name"
```

#### 场景 4: 修改数据库 Schema

```bash
# 使用 Alembic 迁移（推荐）

# 1. 进入容器
docker exec -it eve_backend /bin/bash

# 2. 生成迁移脚本（自动检测 Schema 变化）
alembic revision --autogenerate -m "add new_column"
# 生成: alembic/versions/xxx_add_new_column.py

# 3. 审查迁移脚本
vim alembic/versions/xxx_add_new_column.py

# 4. 执行迁移
alembic upgrade head
# 不需要重启容器

# 5. 验证迁移成功
docker exec eve_backend psql -U postgres -d ruoyi-fastapi -c "\d table_name"

# 6. 回滚（如果需要）
alembic downgrade -1
```

### 常用开发命令

```bash
# 查看后端日志（实时）
docker logs -f eve_backend

# 进入容器交互式 shell
docker exec -it eve_backend /bin/bash

# 在容器内运行命令
docker exec eve_backend python -c "print('hello')"

# 查看容器内文件
docker exec eve_backend ls -la /app

# 测试数据库连接
docker exec eve_backend python -c "
import psycopg2
conn = psycopg2.connect('postgresql://postgres:root@eve-pg:5432/ruoyi-fastapi')
print('连接成功')
conn.close()
"

# 重启容器
docker restart eve_backend

# 查看容器资源使用
docker stats eve_backend

# 删除容器（删除后可重新启动）
docker rm -f eve_backend
docker-compose -f docker-compose.local.yml up -d eve-backend-pg
```

---

## 🎨 前端开发

### 方案 A: 前端本地开发（推荐）

**优点**：支持 HMR（热模块替换），开发体验最好

```bash
# 1. 在宿主机上启动前端开发服务器
cd EVE-FastAPI/EVE-fastapi-frontend
npm install
npm run dev
# 输出：Local: http://localhost:5173

# 2. 访问本地前端
open http://localhost:5173

# 3. 修改代码后自动刷新
vim src/components/Navbar.vue
# 保存即可看到变化（HMR），无需手动刷新

# 4. 后端仍然在 Docker 中运行
# 前端自动连接到 http://localhost:19099/docker-api
```

**配置说明**：

```javascript
// vite.config.js
export default {
  server: {
    proxy: {
      '/docker-api': {
        target: 'http://localhost:19099',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/docker-api/, '/docker-api'),
      },
    },
  },
}
```

### 方案 B: Docker 容器内开发

**使用场景**：需要与其他服务完全一致的环境

```bash
# 1. 修改前端代码
vim EVE-FastAPI/EVE-fastapi-frontend/src/views/Home.vue

# 2. 重新构建镜像
docker-compose -f docker-compose.local.yml build eve_frontend
# ⏱️ 耗时：npm install (~1min) + npm build (~1min)

# 3. 重启前端容器
docker-compose -f docker-compose.local.yml up -d eve_frontend

# 4. 访问前端
open http://localhost:12580

# 5. 在浏览器中强制刷新
# macOS: Cmd + Shift + R
# Windows: Ctrl + Shift + F5
```

### 常用前端开发命令

```bash
# 本地开发
cd EVE-FastAPI/EVE-fastapi-frontend
npm install
npm run dev          # 启动本地开发服务器

# Docker 开发（构建）
npm run build:docker # 使用 .env.docker 配置编译

# 检查代码
npm run lint         # 代码检查

# 查看前端日志
docker logs eve_frontend

# 进入前端容器
docker exec -it eve_frontend /bin/sh

# 查看 Nginx 配置是否生效
docker exec eve_frontend nginx -t
docker exec eve_frontend cat /etc/nginx/conf.d/default.conf

# 重启 Nginx
docker exec eve_frontend nginx -s reload
```

---

## 🔍 调试方法

### 后端调试

#### 使用 FastAPI 内置调试工具

```bash
# 1. 访问 API 文档
open http://localhost:19099/docker-api/docs

# 2. 在 Swagger UI 中直接测试 API
# 点击 "Try it out" 按钮
# 填写参数
# 点击 "Execute" 查看响应

# 3. 查看详细日志
docker logs -f eve_backend | grep "your_endpoint_name"
```

#### 添加调试日志

```python
# 在后端代码中添加日志
import logging
logger = logging.getLogger(__name__)

@router.get('/auth/eve/login')
async def eve_login():
    logger.info('点击了 EVE SSO 登录按钮')
    logger.debug(f'生成的 state: {state}')
    logger.warning('某个警告')
    logger.error('某个错误')
    
    return {'status': 'ok'}
```

查看日志：

```bash
# 查看所有日志
docker logs eve_backend | grep "点击了 EVE"

# 搜索特定关键词
docker logs eve_backend 2>&1 | grep -i "error\|warning"

# 查看最后 200 行
docker logs --tail 200 eve_backend
```

#### 交互式调试

```bash
# 1. 进入容器 shell
docker exec -it eve_backend /bin/bash

# 2. 启动 Python REPL
python

# 3. 导入并测试代码
>>> from config.env import settings
>>> print(settings.app_root_path)
/docker-api

>>> from config.get_db import get_db
>>> # 测试数据库连接
```

### 数据库调试

#### 直接查询

```bash
# 连接到数据库
docker exec -it eve_db psql -U postgres -d ruoyi-fastapi

# psql 命令
\dt                                    # 列出所有表
\d table_name                          # 查看表结构
SELECT * FROM users LIMIT 5;           # 查询数据
INSERT INTO users VALUES (...);        # 插入数据
UPDATE users SET name='new' WHERE id=1; # 更新数据
DELETE FROM users WHERE id=1;          # 删除数据

# 查看数据库大小
SELECT pg_size_pretty(pg_database_size('ruoyi-fastapi'));

# 查看所有表大小
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

#### 使用 pgAdmin（图形化）

```bash
# 1. 访问 pgAdmin
open http://localhost:5050

# 2. 登录
# 邮箱：admin@example.com
# 密码：admin

# 3. 添加服务器
# 右键 Servers → Register → Server
# 主机名：eve-pg
# 端口：5432
# 用户：postgres
# 密码：root

# 4. 查看表、执行查询等
```

### 网络调试

```bash
# 测试容器间连通性
docker exec eve_backend ping eve-pg
docker exec eve_backend ping eve-redis

# 测试端口连接
docker exec eve_backend nc -zv eve-pg 5432
docker exec eve_backend nc -zv eve-redis 6379

# 查看 DNS 解析
docker exec eve_backend nslookup eve-pg

# 查看网络接口
docker exec eve_backend ip addr show
```

### Nginx 调试

```bash
# 查看 Nginx 配置是否有问题
docker exec eve_frontend nginx -t
# 输出：nginx: the configuration file ... is ok

# 查看 Nginx 日志
docker logs eve_frontend

# 进入 Nginx 容器
docker exec -it eve_frontend /bin/sh

# 在容器内测试后端连接
curl -v http://eve-backend-pg:9099/docker-api/docs
```

---

## 📚 常用快速参考

### 代码修改响应时间

| 修改内容 | 重启需求 | 时间 | 说明 |
|---------|---------|------|------|
| 后端 `.py` 文件 | ❌ 否 | <2s | 热重载（需启用 `APP_RELOAD=true`） |
| 前端 `.vue/.js` 文件 | ❌ 否 | <1s | HMR（本地开发模式下） |
| `.env.dockerpg` 文件 | ⚠️ 重启 | ~5s | 需要重启容器 |
| Nginx 配置 | ⚠️ 重启 | ~3s | 需要重启容器 |
| `requirements-pg.txt` | ✅ 重构 | 3-5m | 需要重新构建镜像 |
| `package.json` | ✅ 重构 | 2-3m | 需要重新构建镜像 |
| 数据库 Schema | ❌ 否 | <1s | 使用 Alembic 迁移 |

### 常用快捷命令

```bash
# 查看所有容器日志
docker-compose -f docker-compose.local.yml logs -f

# 重启所有容器
docker-compose -f docker-compose.local.yml restart

# 停止所有容器
docker-compose -f docker-compose.local.yml stop

# 启动所有容器
docker-compose -f docker-compose.local.yml start

# 删除所有容器和卷
docker-compose -f docker-compose.local.yml down -v

# 清理 Docker 系统
docker system prune -a
```

---

## 🐛 常见开发问题

### 问题 1: 热重载不工作

**检查清单**：
1. 确认 `.env.dockerpg` 中 `APP_RELOAD = true`
2. 重启容器使配置生效
3. 检查代码是否有语法错误
4. 查看日志是否有其他错误

### 问题 2: 前端连接不到后端

**调试步骤**：
```bash
# 1. 检查后端是否运行
docker ps | grep eve_backend

# 2. 检查端口映射
docker port eve_backend

# 3. 测试后端 API 可达性
curl http://localhost:19099/docker-api/docs

# 4. 检查前端构建配置
grep VITE_APP_BASE_API EVE-FastAPI/EVE-fastapi-frontend/.env.docker

# 5. 查看浏览器控制台错误
# F12 打开开发者工具
# Network 标签查看 API 请求
# Console 标签查看 JavaScript 错误
```

### 问题 3: 数据库无法连接

**调试步骤**：
```bash
# 1. 检查数据库容器是否运行
docker ps | grep eve_db

# 2. 查看数据库日志
docker logs eve_db | tail -20

# 3. 测试数据库连接
docker exec eve_backend psql -U postgres -h eve-pg -d ruoyi-fastapi -c "SELECT 1"

# 4. 检查环境变量
docker exec eve_backend env | grep DB_
```

---

## 📖 相关文档

- [1-PROJECT_OVERVIEW.md](1-PROJECT_OVERVIEW.md) - 项目概览
- [2-DOCKER_BUILD.md](2-DOCKER_BUILD.md) - Docker 构建与部署
- [3-CONFIG_ENV.md](3-CONFIG_ENV.md) - 环境配置管理
- [5-TROUBLESHOOTING.md](5-TROUBLESHOOTING.md) - 故障排除
