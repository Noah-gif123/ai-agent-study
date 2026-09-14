# -*- coding: utf-8 -*-
"""ReAct 主循环"""
import json
import tiktoken
from config.settings import MAX_STEPS, TOKEN_LIMIT, KEEP_RECENT, OUTPUT_DIR
from core.llm_client import call_llm
from core.memory import compress_messages
from tools.registry import execute_tool
from utils.logger import get_logger
import os

logger = get_logger(__name__)

# Token 计数器
try:
    ENCODING = tiktoken.encoding_for_model("gpt-3.5-turbo")
except ImportError:
    ENCODING = None

def count_tokens(messages: list) -> int:
    if ENCODING is None:
        return 0
    text = "".join(f"{m['role']}: {m.get('content', '')}\n" for m in messages)
    return len(ENCODING.encode(text))

def save_history(messages: list):
    path = os.path.join(OUTPUT_DIR, "history.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def run_agent():
    logger.info("🚀 Agent 启动")
    messages = [{"role": "system", "content": "你是智能助手"}]
    total_tokens = 0

    for step in range(1, MAX_STEPS + 1):
        user_input = input(f"\n👤 第 {step} 轮：").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # Token 检查与压缩
        current_tokens = count_tokens(messages)
        total_tokens += current_tokens
        logger.info(f"本轮 Token：{current_tokens} | 累计：{total_tokens}")

        if current_tokens > TOKEN_LIMIT:
            logger.warning(f"⚠️ Token 超限，触发压缩")
            messages = compress_messages(messages, KEEP_RECENT)

        # 调用 LLM
        parsed = call_llm(messages)
        action = parsed.get("action", "finish")
        action_input = parsed.get("action_input", {})

        if not isinstance(action_input, dict):
            action_input = {"answer": str(action_input)}

        # 执行
        if action == "finish":
            reply = action_input.get("answer", "好的。")
            messages.append({"role": "assistant", "content": reply})
        else:
            reply = execute_tool(action, action_input)
            messages.append({"role": "assistant", "content": reply})

        print(f"🤖 Agent：{reply}")

        # 每轮保存
        save_history(messages)

    logger.info("🏁 会话结束")

if __name__ == "__main__":
    run_agent()