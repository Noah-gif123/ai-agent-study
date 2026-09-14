# -*- coding: utf-8 -*-
"""脏数据清洗工具"""
import re
import json
import ast
from utils.logger import get_logger

logger = get_logger(__name__)

def safe_json_loads(raw_text: str) -> dict:
    """从脏文本中安全提取 JSON（5 层策略）"""
    if not raw_text or not isinstance(raw_text, str):
        return None

    original = raw_text.strip()

    # 策略 1：直接解析
    try:
        return json.loads(original)
    except json.JSONDecodeError:
        pass

    # 策略 2：去除 Markdown 代码块
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', original, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 策略 3：正则提取 {...}
    match = re.search(r'\{.*\}', original, re.DOTALL)
    if match:
        cleaned = match.group().strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            try:
                result = ast.literal_eval(cleaned)
                if isinstance(result, dict):
                    return result
            except (ValueError, SyntaxError):
                pass

    # 策略 4：截取首尾花括号
    start, end = original.find("{"), original.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(original[start:end + 1])
        except json.JSONDecodeError:
            pass

    # 策略 5：ast 兜底
    try:
        result = ast.literal_eval(original)
        if isinstance(result, dict):
            return result
    except (ValueError, SyntaxError):
        pass

    logger.error(f"所有清洗策略失败：{original[:80]}...")
    return None