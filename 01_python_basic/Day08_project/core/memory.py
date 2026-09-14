# -*- coding: utf-8 -*-
"""对话压缩"""
import json
import requests
from config.settings import DEEPSEEK_API_KEY, DEEPSEEK_URL, MODEL_NAME
from prompts.templates import SUMMARY_PROMPT
from utils.logger import get_logger

logger = get_logger(__name__)

def compress_messages(messages: list, keep_recent: int = 3) -> list:
    """压缩历史对话，保留最近 N 条"""
    system_msgs = [m for m in messages if m["role"] == "system"]
    system_content = system_msgs[0]["content"] if system_msgs else "你是助手"

    # 只保留干净的 user/assistant 消息
    clean = [
        m for m in messages
        if m["role"] == "user" or (m["role"] == "assistant" and "tool_calls" not in m and m.get("content"))
    ]

    if len(clean) <= keep_recent:
        return messages

    to_compress = clean[:-keep_recent]
    recent = clean[-keep_recent:]

    # 调用 LLM 生成摘要
    try:
        resp = requests.post(
            DEEPSEEK_URL,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": SUMMARY_PROMPT.format(history=json.dumps(to_compress, ensure_ascii=False))}],
                "temperature": 0.3,
                "max_tokens": 200
            },
            timeout=30
        )
        resp.raise_for_status()
        summary = resp.json()["choices"][0]["message"]["content"].strip()
        logger.info(f"✅ 压缩完成：{summary}")

        new_system = {"role": "system", "content": f"{system_content}\n\n[历史摘要] {summary}"}
        return [new_system] + recent
    except Exception as e:
        logger.error(f"压缩失败：{e}")
        return messages