import os
import socket
import platform
from sshtunnel import SSHTunnelForwarder
from config.env import get_config
from loguru import logger

# 从配置中加载 SSH 和数据库设置
ssh_settings = get_config.get_ssh_config()
db_settings = get_config.get_database_config()

class SSHTunnelManager:
    """
    一个管理 SSH 隧道的工具类，集成到 FastAPI 的生命周期中。
    """
    def __init__(self):
        # 远程 SSH 服务器配置
        self.ssh_host = ssh_settings.ssh_host
        self.ssh_user = ssh_settings.ssh_user
        self.ssh_key_path = self._get_platform_specific_path(ssh_settings.ssh_key_path)

        # 隧道配置
        self.remote_bind_address = (db_settings.db_host, ssh_settings.remote_port)
        self.local_bind_address = ('127.0.0.1', db_settings.db_port)

        self.server: SSHTunnelForwarder | None = None
        logger.info(f"SSH 隧道管理器初始化完成。")
        logger.info(f"本地端口 {self.local_bind_address[1]} 将被转发至远程 {self.remote_bind_address[0]}:{self.remote_bind_address[1]}")


    def _get_platform_specific_path(self, path: str) -> str:
        """处理跨平台的路径，特别是 Windows 下的 '~'"""
        if path.startswith('~'):
            return os.path.expanduser(path)
        return path

    def _is_port_in_use(self) -> bool:
        """检查本地端口是否已被占用"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(self.local_bind_address)
                return False
            except socket.error:
                return True

    def start_tunnel(self):
        """启动 SSH 隧道"""
        if self._is_port_in_use():
            logger.warning(f"端口 {self.local_bind_address[1]} 已被占用，跳过启动新的 SSH 隧道。")
            return

        try:
            logger.info("正在尝试启动 SSH 隧道...")
            self.server = SSHTunnelForwarder(
                (self.ssh_host, 22),
                ssh_username=self.ssh_user,
                ssh_pkey=self.ssh_key_path,
                remote_bind_address=self.remote_bind_address,
                local_bind_address=self.local_bind_address
            )
            self.server.start()
            logger.success(f"✅ SSH 隧道已成功启动。本地 {self.server.local_bind_port} -> 远程 {self.remote_bind_address}")
        except Exception as e:
            logger.error(f"❌ 启动 SSH 隧道失败: {e}")
            raise

    def stop_tunnel(self):
        """停止 SSH 隧道"""
        if self.server and self.server.is_active:
            logger.info("正在关闭 SSH 隧道...")
            self.server.stop()
            logger.success("✅ SSH 隧道已成功关闭。")

# 创建一个单例，以便在 lifespan 中使用
ssh_tunnel_manager = SSHTunnelManager()
