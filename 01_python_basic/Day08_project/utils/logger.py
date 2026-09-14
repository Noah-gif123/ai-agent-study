# -*- coding: utf-8 -*-
"""统一的日志配置"""
import os
import logging
from config.settings import LOG_DIR

def get_logger(name: str) -> logging.Logger:
    """获取一个配置好的 logger"""
    logger = logging.getLogger(name)
    if logger.handlers:  # 避免重复添加 handler
        return logger

    logger.setLevel(logging.DEBUG)

    # 控制台 handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # 文件 handler
    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, "agent.log"),
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    # 统一格式
    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    console.setFormatter(fmt)
    file_handler.setFormatter(fmt)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger