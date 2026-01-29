# EVE-FastAPI 配置审计摘要

> 生成日期：2026-01-30

## 数据库初始化逻辑

- **初始化文件**：`ruoyi-fastapi-backend/config/database.py`
- **Engine/Session**：
  - `create_async_engine(db_settings.database_url, ...)`
  - `AsyncSessionLocal = async_sessionmaker(bind=engine, ...)`
- **多数据库绑定（Binds）实现**：
  - 未发现 SQLAlchemy `binds` 或多 engine 绑定。
  - 通过**单一 engine** + 两个 Base 区分 schema：
    - `Base`（public schema）
    - `SdeBase`（`metadata = MetaData(schema="raw")`）
  - `get_db()` / `get_sde_db()` 只读/读写策略不同，不属于 binds。

## 环境变量与端口

- **`.env.dev`**：`ruoyi-fastapi-backend/.env.dev` 在工作区未找到。
- **PostgreSQL（由 `docker-compose.local.yml` + `.env.local` 组合推导）**：
  - `POSTGRES_USER` ← `.env.local` 中 `DB_USER=eve_admin`
  - `POSTGRES_DB` ← `.env.local` 中 `DB_NAME=eve_db`
  - `POSTGRES_PASSWORD` ← `.env.local` 中 `DB_PASSWORD=root`
  - **端口映射**：`${DB_EXTERNAL_PORT}:5432` → `15432:5432`

## SDE 输出 SQLite 文件

- **配置文件**：`sde-processor/config.json`
- **输出目录（路径变量）**：`paths.db_output = "./output_sde/db"`
- **输出文件名**：`item_db_{lang}.sqlite`
  - 语言：`en`、`zh`
  - 结果文件：
    - **`./output_sde/db/item_db_en.sqlite`**
    - **`./output_sde/db/item_db_zh.sqlite`**

## 静态文件服务配置

- **挂载入口**：`ruoyi-fastapi-backend/sub_applications/staticfiles.py`
- **挂载方式**：
  - `app.mount(UploadConfig.UPLOAD_PREFIX, StaticFiles(directory=UploadConfig.UPLOAD_PATH), ...)`
- **路径变量（物理路径）**：
  - `UPLOAD_PREFIX = "/profile"`
  - **`UPLOAD_PATH = "vf_admin/upload_path"`**
  - `DOWNLOAD_PATH = "vf_admin/download_path"`

## 前端代理配置（Vite）

- **配置文件**：`ruoyi-fastapi-frontend/vite.config.js`
- **代理规则**：
  - 仅配置 `/dev-api` → `backendTarget`
  - `rewrite: p.replace(/^\/dev-api/, "")`
- **/dev-api 之外的资源**：
  - 未配置额外代理；静态资源由 Vite 本地/构建输出处理（`base`、`build.assetsDir`）。
