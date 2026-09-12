# -*- coding: utf-8 -*-
"""
Day 07：脏数据终极防御（完整版）
核心能力：
1. safe_json_loads() 一键清洗 5 种脏数据
2. 自动重试机制（解析失败让模型重新生成）
3. 集成到 Agent 主循环中
"""

import os
import re
import json
import ast
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
        logging.FileHandler(os.path.join(LOG_DIR, "day12_dirty.log"), encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# ========== 3. 核心：safe_json_loads 脏数据清洗函数 ==========
def safe_json_loads(raw_text: str) -> dict:
    """
    从大模型返回的脏文本中安全提取 JSON 字典
    依次尝试 5 种策略，全部失败才返回 None
    """
    if not raw_text or not isinstance(raw_text, str):
        logger.warning("输入为空或非字符串")
        return None

    original = raw_text.strip()

    # ---------- 策略 1：直接解析（最干净的情况） ----------
    try:
        result = json.loads(original)
        logger.debug("✅ 策略1成功：直接解析")
        return result
    except json.JSONDecodeError:
        pass

    # ---------- 策略 2：去除 Markdown 代码块标记 ----------
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', original, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()
        try:
            result = json.loads(cleaned)
            logger.debug("✅ 策略2成功：去除 Markdown 代码块")
            return result
        except json.JSONDecodeError:
            pass

    # ---------- 策略 3：正则提取第一个 { 到最后一个 } 之间的内容 ----------
    match = re.search(r'\{.*\}', original, re.DOTALL)
    if match:
        cleaned = match.group().strip()
        try:
            result = json.loads(cleaned)
            logger.debug("✅ 策略3成功：正则提取 {} 内容")
            return result
        except json.JSONDecodeError:
            # 用 ast 兜底（处理单引号 JSON）
            try:
                result = ast.literal_eval(cleaned)
                if isinstance(result, dict):
                    logger.debug("✅ 策略3b成功：ast.literal_eval 兜底")
                    return result
            except (ValueError, SyntaxError):
                pass

    # ---------- 策略 4：截取首尾花括号之间的内容 ----------
    start = original.find("{")
    end = original.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = original[start:end + 1]
        try:
            result = json.loads(cleaned)
            logger.debug("✅ 策略4成功：截取首尾花括号内容")
            return result
        except json.JSONDecodeError:
            pass

    # ---------- 策略 5：处理单引号 JSON（Python 风格） ----------
    try:
        result = ast.literal_eval(original)
        if isinstance(result, dict):
            logger.debug("✅ 策略5成功：ast.literal_eval 解析")
            return result
    except (ValueError, SyntaxError):
        pass

    # 全部策略失败
    logger.error(f"❌ 所有清洗策略均失败，原始内容：{original[:100]}...")
    return None


# ========== 4. 单元测试 ==========
def test_safe_json_loads():
    """测试各种脏数据场景"""
    test_cases = [
        ('{"action": "finish", "action_input": {"answer": "ok"}}', "finish"),
        ('```json\n{"action": "finish", "action_input": {"answer": "ok"}}\n```', "finish"),
        ('好的，这是结果：{"action": "finish", "action_input": {"answer": "ok"}}', "finish"),
        ('{"action": "finish", "action_input": {"answer": "ok"}} 希望有帮助！', "finish"),
        ("{'action': 'finish', 'action_input': {'answer': 'ok'}}", "finish"),
        ('```\n{"action": "finish"}\n```', "finish"),
        ('完全不是 JSON 的纯文本', None),
    ]

    print("\n" + "=" * 50)
    print("🧪 测试 safe_json_loads 各种脏数据场景")
    print("=" * 50)

    passed = 0
    for idx, (raw, expected_action) in enumerate(test_cases, 1):
        result = safe_json_loads(raw)
        actual_action = result.get("action") if isinstance(result, dict) else None
        status = "✅" if actual_action == expected_action else "❌"
        if status == "✅":
            passed += 1
        print(f"{status} 用例{idx}: 期望={expected_action}, 实际={actual_action}")
        print(f"   输入：{raw[:60]}{'...' if len(raw) > 60 else ''}")

    print(f"\n📊 测试结果：{passed}/{len(test_cases)} 通过")


# ========== 5. 带重试机制的 LLM 调用 ==========
def call_llm_with_retry(messages: list, max_retries: int = 3) -> dict:
    """
    调用 DeepSeek API，如果解析失败则自动重试
    返回：解析后的字典 {"action": ..., "action_input": ...}
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    system_prompt = """你是一个智能助手。请严格按以下 JSON 格式返回，不要加任何其他文字或 Markdown 标记：

{"action": "工具名或finish", "action_input": {参数}}

可用工具：
- get_time: 获取当前时间（无需参数）

如果是普通对话，action 设为 "finish"，action_input 为 {"answer": "你的回复"}。"""

    # 构造请求消息
    filtered = [m for m in messages if m["role"] != "system"]
    request_messages = [{"role": "system", "content": system_prompt}] + filtered

    for attempt in range(1, max_retries + 1):
        logger.info(f"🔄 第 {attempt}/{max_retries} 次尝试调用 API...")

        payload = {
            "model": "deepseek-chat",
            "messages": request_messages,
            "temperature": 0.3,
            "max_tokens": 300
        }

        try:
            resp = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            ai_message = resp.json()["choices"][0]["message"]["content"]

            # 用 safe_json_loads 清洗
            parsed = safe_json_loads(ai_message)
            if parsed and "action" in parsed:
                logger.info(f"✅ 第 {attempt} 次尝试解析成功")
                return parsed
            else:
                logger.warning(f"⚠️ 第 {attempt} 次解析失败，原始返回：{ai_message[:100]}")
                # 把失败信息追加给模型，让它重试
                request_messages.append({"role": "assistant", "content": ai_message})
                request_messages.append({
                    "role": "user",
                    "content": "你上次返回的不是合法 JSON，请严格按照格式重新返回，不要加任何 Markdown 标记或解释文字。"
                })

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 第 {attempt} 次请求失败：{e}")
            time.sleep(1)  # 等待 1 秒后重试

    # 所有重试都失败
    logger.error("❌ 所有重试均失败，返回默认降级回复")
    return {"action": "finish", "action_input": {"answer": "抱歉，我暂时无法正确响应，请稍后再试。"}}


# ========== 6. 工具函数 ==========
def get_time() -> str:
    return f"🕐 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

AVAILABLE_FUNCTIONS = {"get_time": get_time}


# ========== 7. 主循环 ==========
def run_agent():
    print("🤖 Day12 脏数据防御 Agent（输入 exit 退出）")
    messages = [{"role": "system", "content": "你是助手"}]

    while True:
        user_input = input("\n👤 用户：").strip()
        if user_input.lower() == "exit":
            print("👋 退出程序")
            break
        if not user_input:
            print("⚠️ 输入为空，请重新输入")
            continue

        messages.append({"role": "user", "content": user_input})

        # 调用 LLM（带重试）
        parsed = call_llm_with_retry(messages)
        action = parsed.get("action", "finish")
        action_input = parsed.get("action_input", {})

        # 防御性处理 action_input
        if not isinstance(action_input, dict):
            action_input = {"answer": str(action_input)}

        print(f"🎯 解析结果：action={action}, input={action_input}")

        # 执行
        if action == "finish":
            reply = action_input.get("answer", "好的。")
            print(f"🤖 Agent：{reply}")
        elif action in AVAILABLE_FUNCTIONS:
            try:
                reply = AVAILABLE_FUNCTIONS[action](**action_input)
                print(f"🤖 Agent：{reply}")
            except Exception as e:
                print(f"❌ 工具执行失败：{e}")
        else:
            print(f"⚠️ 未知 action：{action}")


# ========== 入口 ==========
if __name__ == "__main__":
    # 先跑单元测试
    test_safe_json_loads()
    # 再进入交互
    print("\n" + "=" * 50)
    print("💡 交互提示：试试输入 '现在几点'、'你好'、'exit'")
    print("=" * 50)
    run_agent()