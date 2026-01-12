# 当前阻塞项

## 目标
自动化启动 FastAPI 开发服务器（python3 app.py --env=dev），使其通过 SSH 隧道连接远程 PostgreSQL 实例，而不再依赖手动执行 ssh -L。

## 现象
- sshtunnel 管理器会尝试启动，但检测本地端口 5433 已被占用，因此跳过隧道启动。
- 紧接着 async SQLAlchemy/asyncpg 引擎访问 127.0.0.1:5433 时抛出 ConnectionRefusedError，为了避免不确定状态，应用会直接退出启动流程。

## 关键配置点
- 现在 SSH 参数通过 SshSettings 数据类提供，它在 .env 完全加载后读取以 SSH_* 为前缀的环境变量（参见 [config/env.py](config/env.py#L101-L117)）。
- 与 FastAPI 生命周期绑定的 SSHTunnelManager 依赖这些 SSH 配置加上统一的数据库配置来完成远端端口的转发，因此它的单例在 server.py 运行前必须获得一个未被占用的 db_port（参见 [config/ssh_tunnel.py](config/ssh_tunnel.py#L12-L75)）。

## 已完成的诊断步骤
1. 将 sshtunnel 添加到 requirements-pg.txt 并执行 python3 -m pip install -r requirements-pg.txt，以确保依赖在环境中可用。
2. 在隧道管理器里记录生命周期日志，确认其启动逻辑在数据库引擎创建前执行，由此排除了 ConnectionRefusedError 是由于时间错误导致的可能。
3. 将 .env.dev 中的 DB_PORT 设置为 5433，以保证被转发的流量与 async 引擎期望的本地绑定端口一致。

## 推荐下一步
1. 找出当前监听 127.0.0.1:5433 的进程并停止，或将隧道（及 .env.dev）改成另一个未被占用的端口。
2. 在端口冲突解决后重新运行 python3 app.py --env=dev，确认 ssh_tunnel_manager.start_tunnel() 没有再输出“端口已占用”的日志。
3. 一旦隧道成功启动，确认 SQL 引擎能建立连接、创建必要表，并让 FastAPI 正常完成生命周期启动。
4. 如果端口依然不可用，可在环境中调整 db_port 与 remote_port 的映射，并同步更新 SshSettings 以避免与其它服务冲突。

## 验证手段
- 日志中应包含来自 [config/ssh_tunnel.py](config/ssh_tunnel.py#L12-L75) 的“✅ SSH 隧道已成功启动”，并紧接着数据库初始化没有 ConnectionRefusedError。
- 只要隧道健康运行，config/database.py 中的 init_create_table() 不应再触发 SystemExit。

## 备注
本文件记录当前阻塞的核心问题。一旦隧道真正转发流量，后续的 async 数据库启动流程会因为致命错误而提前退出，所以只要没有出现原先那些错误日志，就说明问题已得到缓解。