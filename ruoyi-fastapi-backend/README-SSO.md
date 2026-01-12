# EVE SSO 集成说明

## 流程概览
1. 前端点击 “Login with EVE SSO” 按钮，请求后端 `/auth/eve/login`（兼容旧路径 `/auth/EVElogin`）。
2. 后端生成 `state` 写入 Redis，重定向至 CCP 授权页。
3. CCP 授权后回调 `/auth/eve/callback?code=...&state=...`。
4. 后端校验 `state`，用 `code` 向 CCP 换取 access_token，解析角色信息，查库或自动注册用户，生成系统 JWT。
5. 后端重定向回前端 `FRONTEND_URL/index?token=系统JWT`，前端路由守卫拦截 URL 中的 `token`，写入 Cookie 并清理 URL，完成自动登录。

## 关键配置
- 环境变量（示例见 `.env.dev`）：
  - `FRONTEND_URL`：前端基地址，用于回调重定向，如 `http://localhost:80`。
  - `EVE_CLIENT_ID` / `EVE_CLIENT_SECRET` / `EVE_CALLBACK_URL`：CCP 应用配置。
  - `APP_ROOT_PATH`：代理前缀（默认 `/dev-api`）。
- 应用设置（[config/env.py](config/env.py#L15-L34)）：`frontend_url` 会从 env 读取，用于回调重定向。

## 前端改动
- 路由守卫：在 [src/permission.js](../ruoyi-fastapi-frontend/src/permission.js#L14-L40) 最先检查 `to.query.token`，写入 `setToken`，清空 query 并继续导航。
- 导航栏按钮：在 [src/layout/components/Navbar.vue](../ruoyi-fastapi-frontend/src/layout/components/Navbar.vue#L40-L129)，未登录时展示 “Login with EVE SSO” 按钮，点击跳转 `import.meta.env.VITE_APP_BASE_API + '/auth/eve/login'`；已登录显示头像下拉。

## 后端接口
- `GET /auth/eve/login`：生成 state，写 Redis，重定向 CCP。
- `GET /auth/EVElogin`：兼容旧路径，内部调用上面的登录入口。
- `GET /auth/eve/callback`：校验 state，用 code 换取 CCP token，解析角色，查库或自动注册，生成系统 JWT，重定向回前端 `FRONTEND_URL/index?token=...`；失败则重定向 `?error=sso_failed`。

## 核心逻辑位置
- 控制器：[module_admin/controller/login_controller.py](module_admin/controller/login_controller.py#L167-L255)
- 服务层（token 交换与用户落库）：[module_admin/service/login_service.py](module_admin/service/login_service.py#L527-L758)

## 验证步骤
1. 确保 `.env.dev`（或对应环境）中已配置 EVE SSO 参数与 `FRONTEND_URL`。
2. 后端启动：`python3 app.py --env=dev`（或 `uvicorn` 方式）。
3. 前端启动或访问已有前端：点击 “Login with EVE SSO”。
4. 授权完成后应跳回 `FRONTEND_URL/index?token=...`，URL 清除 token 后进入首页且保持登录态。
5. 若出现 `state` 校验失败或 CCP Token 获取失败，查看后端日志并确认 Redis、回调 URL、CCP 凭据是否正确。
