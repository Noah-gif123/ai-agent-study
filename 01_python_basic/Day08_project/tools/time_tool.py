# -*- coding: utf-8 -*-
"""时间工具"""
from datetime import datetime

def get_time() -> str:
    return f"🕐 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# 工具元信息（供注册表使用）
TOOL_DEFINITION = {
    "name": "get_time",
    "description": "获取当前的准确时间",
    "parameters": {"type": "object", "properties": {}, "required": []},
    "func": get_time
}