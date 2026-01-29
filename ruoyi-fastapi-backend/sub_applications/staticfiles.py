from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.env import UploadConfig
from utils.log_util import logger


def mount_staticfiles(app: FastAPI) -> None:
    """
    挂载静态文件
    """
    app.mount(f'{UploadConfig.UPLOAD_PREFIX}', StaticFiles(directory=f'{UploadConfig.UPLOAD_PATH}'), name='profile')
    current_path = Path(__file__).resolve()
    parents = list(current_path.parents)
    project_root = parents[2] if len(parents) > 2 else parents[-1]
    sde_static_dir = project_root / 'sde-processor' / 'output_sde'
    if sde_static_dir.exists():
        app.mount(
            '/sde-static',
            StaticFiles(directory=str(sde_static_dir)),
            name='sde_static',
        )
    else:
        logger.warning(f"SDE 静态目录不存在，跳过挂载: {sde_static_dir}")
