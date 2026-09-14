# -*- coding: utf-8 -*-
"""LLM 调用封装"""
import time
import requests
from config.settings import DEEPSEEK_API_KEY, DEEPSEEK_URL, MODEL_NAME, MAX_RETRIES
from prompts.templates import AGENT_SYSTEM_PROMPT
from tools.registry import get_tools_schema
from utils.json_cleaner import safe_json_loads
from utils.logger import get_logger

logger = get_logger(__name__)

def call_llm(messages: list) -> dict:
    """调用 LLM 并自动重试，返回解析后的字典"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    # 构造请求消息（把 system prompt 放在最前面）
    filtered = [m for m in messages if m["role"] != "system"]
    request_messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}] + filtered

    for attempt in range(1, MAX_RETRIES + 1):
        logger.info(f"🔄 第 {attempt}/{MAX_RETRIES} 次调用 LLM")

        payload = {
            "model": MODEL_NAME,
            "messages": request_messages,
            "tools": get_tools_schema(),
            "tool_choice": "auto",
            "temperature": 0.3,
            "max_tokens": 300
        }

        try:
            resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            assistant_msg = result["choices"][0]["message"]

            # 情况 1：模型返回工具调用
            if "tool_calls" in assistant_msg:
                tool_call = assistant_msg["tool_calls"][0]
                return {
                    "action": tool_call["function"]["name"],
                    "action_input": __import__("json").loads(tool_call["function"]["arguments"]),
                    "_raw": assistant_msg
                }

            # 情况 2：模型返回普通文本，尝试解析为 JSON
            content = assistant_msg.get("content", "")
            parsed = safe_json_loads(content)
            if parsed and "action" in parsed:
                return parsed
            else:
                return {"action": "finish", "action_input": {"answer": content}}

        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败：{e}")
            time.sleep(1)

    return {"action": "finish", "action_input": {"answer": "服务暂时不可用，请稍后重试。"}}