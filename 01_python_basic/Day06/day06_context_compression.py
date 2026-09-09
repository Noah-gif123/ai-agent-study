# -*- coding: utf-8 -*-
"""
Day 06：对话压缩器（最终修复版）
修复：彻底过滤掉 tool_calls 相关消息，确保压缩后的消息列表干净合规
"""

import os
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
import requests

# ========== 1. 加载环境 ==========
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("请在 .env 中设置 DEEPSEEK_API_KEY")

# ========== 2. 日志配置 ==========
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "compression.log"), encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# ========== 3. Token 计数器 ==========
try:
    import tiktoken
    ENCODING = tiktoken.encoding_for_model("gpt-3.5-turbo")
    logger.info("✅ tiktoken 加载成功")
except ImportError:
    logger.warning("⚠️ tiktoken 未安装，Token 统计返回 0")
    ENCODING = None

def count_tokens(messages: list) -> int:
    if ENCODING is None:
        return 0
    text = ""
    for msg in messages:
        # 只统计 role 和 content，忽略其他字段
        content = msg.get("content", "")
        if content:
            text += f"{msg['role']}: {content}\n"
    return len(ENCODING.encode(text))

# ========== 4. 压缩函数（最终修复版） ==========
def compress_conversation(messages: list, keep_recent: int = 3) -> list:
    """
    压缩对话历史：只保留 user 和干净的 assistant（无 tool_calls）消息，
    将较早的部分压缩成摘要，合并到 system prompt 中。
    """
    # 1. 提取 system 内容
    system_msgs = [msg for msg in messages if msg["role"] == "system"]
    system_content = system_msgs[0]["content"] if system_msgs else "你是一个智能助手。"

    # 2. 提取干净的非 system 消息（只保留 user 和 不含 tool_calls 且有内容的 assistant）
    clean_msgs = []
    for msg in messages:
        if msg["role"] == "user":
            clean_msgs.append(msg)
        elif msg["role"] == "assistant" and "tool_calls" not in msg and msg.get("content"):
            clean_msgs.append(msg)
        # 忽略 tool 角色和带 tool_calls 的 assistant

    # 如果干净消息数太少，无需压缩
    if len(clean_msgs) <= keep_recent:
        logger.info("干净消息数较少，跳过压缩")
        return messages

    # 3. 分割：待压缩部分和最近保留部分
    to_compress = clean_msgs[:-keep_recent]
    recent = clean_msgs[-keep_recent:]

    # 4. 构造摘要 prompt
    summary_prompt = f"""请将以下对话历史压缩成一段简洁的摘要（50字以内），保留关键信息：

{json.dumps(to_compress, ensure_ascii=False, indent=2)}

只输出摘要文本，不要其他内容。"""

    try:
        logger.info(f"📝 正在压缩 {len(to_compress)} 条历史消息...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": summary_prompt}],
                "temperature": 0.3,
                "max_tokens": 200
            },
            timeout=30
        )
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"].strip()
        logger.info(f"✅ 压缩完成，摘要：{summary}")

        # 5. 构造新消息列表：system + 摘要（并入 system） + 最近干净消息
        new_system_content = system_content + f"\n\n[历史摘要] {summary}"
        new_messages = [{"role": "system", "content": new_system_content}] + recent

        # 6. Token 对比
        old_tokens = count_tokens(messages)
        new_tokens = count_tokens(new_messages)
        logger.info(f"📊 压缩前 Token：{old_tokens}，压缩后：{new_tokens}，节省：{old_tokens - new_tokens}")

        return new_messages

    except Exception as e:
        logger.error(f"压缩失败：{e}，将跳过压缩")
        return messages

# ========== 5. 工具定义（世界之最） ==========
WORLD_RECORDS = {
    "山": "世界最高峰是珠穆朗玛峰（海拔 8848.86 米）",
    "海": "世界最大的海是珊瑚海（面积 479.1 万平方公里）",
    "河": "世界最长的河流是尼罗河（全长 6670 公里）",
    "湖": "世界最大的淡水湖是苏必利尔湖（面积 8.21 万平方公里）",
    "岛": "世界最大的岛屿是格陵兰岛（面积 216.6 万平方公里）"
}

def query_world_record(category: str) -> str:
    for key in WORLD_RECORDS:
        if key in category:
            return WORLD_RECORDS[key]
    return f"未找到“{category}”的记录"

TOOLS = [{
    "type": "function",
    "function": {
        "name": "query_world_record",
        "description": "查询世界之最",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "类别（山/海/河/湖/岛）"}
            },
            "required": ["category"]
        }
    }
}]

# ========== 6. 调用 DeepSeek（含工具调用） ==========
def call_deepseek_with_tools(messages: list) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto",
        "temperature": 0.3
    }
    try:
        resp = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        assistant_msg = result["choices"][0]["message"]
        messages.append(assistant_msg)  # 可能包含 tool_calls

        if "tool_calls" in assistant_msg:
            tool_call = assistant_msg["tool_calls"][0]
            args = json.loads(tool_call["function"]["arguments"])
            tool_result = query_world_record(args.get("category", ""))
            messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": tool_result})

            payload2 = {
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.3
            }
            resp2 = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload2, headers=headers, timeout=30)
            resp2.raise_for_status()
            final = resp2.json()["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": final})
            return final
        return assistant_msg.get("content", "")
    except requests.exceptions.RequestException as e:
        logger.error(f"API 调用失败: {e}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"响应内容: {e.response.text[:200]}")
        return f"❌ 请求失败：{e}"

# ========== 7. 主循环 ==========
def run_agent():
    TOKEN_LIMIT = 800   # 为了演示压缩，设低一点
    KEEP_RECENT = 3

    messages = [{"role": "system", "content": "你是一个知识助手，可以查询世界之最。"}]
    total_tokens = 0
    round_count = 0

    print("🌍 世界之最查询器（支持压缩，输入 exit 退出）")
    logger.info("🚀 Agent 启动，Token 阈值：{}".format(TOKEN_LIMIT))

    while True:
        user_input = input("\n👤 用户：").strip()
        if user_input.lower() == "exit":
            logger.info("用户退出")
            break
        if not user_input:
            continue

        round_count += 1
        messages.append({"role": "user", "content": user_input})

        # Token 检查
        current_tokens = count_tokens(messages)
        total_tokens += current_tokens
        logger.info(f"第 {round_count} 轮 | 当前 token：{current_tokens} | 累计：{total_tokens}")

        if current_tokens > TOKEN_LIMIT:
            logger.warning(f"⚠️ Token 超限（{current_tokens} > {TOKEN_LIMIT}），触发压缩...")
            messages = compress_conversation(messages, keep_recent=KEEP_RECENT)
            current_tokens = count_tokens(messages)
            logger.info(f"压缩后 Token：{current_tokens}")

        # 调用模型
        try:
            reply = call_deepseek_with_tools(messages)
            print(f"🤖 Agent：{reply}")
        except Exception as e:
            logger.error(f"调用失败：{e}")
            print(f"❌ 发生错误：{e}")

# ========== 入口 ==========
if __name__ == "__main__":
    run_agent()