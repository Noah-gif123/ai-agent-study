# -*- coding: utf-8 -*-
"""集中配置：所有路径和常量都在这里定义"""
import os
from dotenv import load_dotenv

# 加载 .env
load_dotenv()

# ========== API 配置 ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"

# ========== 路径配置（基于本文件位置，保证在任何地方运行都正确） ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# 确保目录存在
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== Agent 行为配置 ==========
MAX_STEPS = 5              # 最大迭代轮数（Day 02）
TOKEN_LIMIT = 1500         # 触发压缩的 Token 阈值（Day 11）
KEEP_RECENT = 3            # 压缩时保留的最近消息数
MAX_RETRIES = 3            # LLM 调用最大重试次数（Day 12）