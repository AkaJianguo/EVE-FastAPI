# EVE-FastAPI 前端开发手册

本项目基于 **RuoYi-Vue3** 修改，使用 Vue 3、Vite、Element Plus、Pinia/Vuex 等主流技术栈。通过 FastAPI 后端接口驱动。本文档旨在帮助开发者快速上手并理解项目架构。

## 1. 项目目录架构
```
src/
├── api/                 # [核心] API 接口管理 (与 views 目录一一对应)
│   ├── system/          # 系统模块接口 (用户、角色、菜单等)
│   └── monitor/         # 监控模块接口
├── assets/              # 静态资源 (图标、图片、样式)
│   ├── icons/           # SVG 图标文件
│   └── styles/          # 全局样式 (element-ui.scss, ruoyi.scss)
├── components/          # [核心] 通用组件库
│   ├── DictTag/         # 字典标签组件 (常用)
│   ├── FileUpload/      # 文件上传组件
│   ├── ImageUpload/     # 图片上传组件
│   ├── Editor/          # 富文本编辑器
│   └── SvgIcon/         # SVG 图标组件
├── directive/           # 自定义指令 (v-hasPermi 等)
├── layout/              # 页面布局 (Sidebar, Navbar, AppMain)
├── router/              # 路由配置 (包含常量路由)
├── store/               # 状态管理 (User, Permission, App)
├── utils/               # [核心] 工具类
│   ├── request.js       # Axios 封装 (这是所有请求的入口)
│   └── auth.js          # Token 读写操作
└── views/               # [核心] 页面主要组件
    ├── login.vue        # 登录页
    └── system/          # 系统管理页面
```

## 2. 核心开发流程

### 2.1 接口请求流程 (Request Flow)
前端均使用 `@/utils/request.js` 发送请求。一般流程如下：
1. **定义 API**: 在 `@/api/xxxx.js` 中导出函数。
2. **调用 API**: 在 Vue 文件中引入并调用。
3. **拦截器处理**: `request.js` 自动处理 Token 携带 (`Authorized` 头) 和 401 过期登出。

**示例代码 (api/demo.js)**:
```javascript
import request from '@/utils/request'

// 查询列表
export function listDemo(query) {
  return request({
    url: '/system/demo/list',
    method: 'get',
    params: query
  })
}
```

### 2.2 动态路由与权限
不同于传统 Vue 项目，本项目的侧边栏菜单和路由主要来自**后端动态返回**。
*   **加载入口**: `src/permission.js` 中的 `router.beforeEach`。
*   **加载过程**: 用户登录 -> 获取 Token -> 请求 `getInfo` -> 请求 `getRouters` -> 动态挂载到 Router。
*   **菜单显示**: 后端返回的路由树结构直接决定了左侧菜单栏的层级和显示。

## 3. 常用开发任务 (How-to)

### 任务一：新增一个业务模块
假设我们要开发一个“订单管理”功能：

1.  **后端准备**: 确保后端 API 已经就绪 (如 `/order/list`)。
2.  **前端 API**: 创建 `src/api/order/index.js`，定义查询、新增、修改接口。
3.  **前端页面**: 创建 `src/views/order/index.vue`。
4.  **配置菜单**: 启动项目 -> 登录 -> 系统管理 -> 菜单管理 -> 新增。
    *   **路由地址**: `order`
    *   **组件路径**: `order/index` (对应 views 下的路径)
    *   **权限字符**: `system:order:list` (用于按钮权限控制)

### 任务二：使用字典 (Dict)
数据通常以 `0/1` 存储，前端需要展示为 `正常/停用`。
```html
<script setup>
// 1. 引入字典钩子
const { sys_normal_disable } = proxy.useDict("sys_normal_disable");
</script>

<template>
  <!-- 2. 下拉框选择 -->
  <el-select v-model="form.status">
    <el-option
      v-for="dict in sys_normal_disable"
      :key="dict.value"
      :label="dict.label"
      :value="dict.value"
    />
  </el-select>

  <!-- 3. 列表回显 (自动匹配颜色和文字) -->
  <dict-tag :options="sys_normal_disable" :value="row.status"/>
</template>
```

### 任务三：权限控制
隐藏普通用户没有权限点击的按钮。
```html
<!-- 只有拥有 system:user:add 权限的用户才能看到此按钮 -->
<el-button v-hasPermi="['system:user:add']">新增用户</el-button>
```

## 4. 关键配置环境

### 4.1 代理配置 (跨域解决)
文件: `vite.config.js`
如果后端运行在 `9099` 以外的端口，请修改此处：
```javascript
server: {
  proxy: {
    '/dev-api': { // 匹配 VITE_APP_BASE_API
      target: 'http://127.0.0.1:9099', // 后端真实地址
      changeOrigin: true,
      rewrite: (p) => p.replace(/^\/dev-api/, '')
    }
  }
}
```

### 4.2 环境变量
*   `.env.development`: 开发环境配置 `VITE_APP_BASE_API = '/dev-api'`
*   `.env.production`: 生产打包配置 `VITE_APP_BASE_API = '/prod-api'`

## 5. 常用命令
```bash
# 安装依赖
pnpm install

# 启动开发服务
pnpm dev

# 构建生产环境
pnpm build:prod

# 预览构建结果
pnpm preview
```

## 6. 排错指南 (Troubleshooting)

*   **Error: connect ECONNREFUSED 127.0.0.1:9099**
    *   **原因**: Vite 试图转发请求给后端，但无法连接。
    *   **解决**: 检查 FastAPI 后端是否已启动，且端口是否为 9099。

*   **401 Unauthorized**
    *   **原因**: Token 过期或未携带。
    *   **解决**: 重新登录。检查 `request.js` 中是否正确从 Cookie/LocalStorage 获取了 Token。

*   **页面修改后不生效**
    *   Vite 极速热更新有时会失效，尝试手动刷新浏览器。
