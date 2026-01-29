# 使用稳定的 LTS 版本
FROM node:20-alpine AS builder

WORKDIR /app

# 1. 直接设置国内镜像源（去掉报错的 unsafe-perm）
RUN npm config set registry https://registry.npmmirror.com

# 2. 复制依赖描述文件
COPY package.json ./

# 3. 安装依赖
# 建议加上 --no-package-lock，可以有效避免之前遇到的 'matches' 报错
RUN npm install --no-package-lock

# 4. 复制源码并执行构建
COPY . .
# 使用 Docker 环境配置（VITE_APP_BASE_API = '/docker-api'）
RUN npm run build:docker

# --- 运行阶段 ---
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]