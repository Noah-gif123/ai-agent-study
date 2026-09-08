# 场景设定：你正在开发一个助手，支持 “数学计算”、“文本翻译” 和 “单词查询” 三个功能。

# 任务目标：你的程序需要支持两种模式：

# 模拟模式：不接大模型，只通过关键词匹配调用工具（锻炼你的逻辑组织能力）。

# 智能模式：接入 DeepSeek，使用原生 Function Calling 让 AI 自主调用工具（锻炼你的 API 交互能力）。


import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

# ==========================================
# 1. 基础工具函数（所有模式共用）
# ==========================================
def calculate(expr: str) -> str:
    """计算器（安全版，仅支持四则运算）"""
    try:
        # 仅允许数字和 + - * / ( ) . 空格
        if not all(c in "0123456789+-*/(). " for c in expr):
            return "❌ 表达式包含非法字符"
        # 注意：这里为了练习，用 eval 但做了字符过滤，生产环境要用 ast
        result = eval(expr)
        return f"🧮 计算结果：{expr} = {result}"
    except Exception as e:
        return f"❌ 计算失败：{str(e)}"

def translate(text: str, target: str = "中文") -> str:
    """模拟翻译（仅用于练习，不真实调用翻译 API）"""
    # 模拟一个简易词典
    mock_dict = {
        "hello": "你好",
        "world": "世界",
        "python": "蟒蛇（编程语言）",
        "agent": "智能体"
    }
    # 简单处理：如果文本在词典里，翻译；否则模拟翻译
    if text.lower() in mock_dict:
        trans = mock_dict[text.lower()]
    else:
        trans = f"[模拟翻译] {text} -> {target}"
    return f"📝 翻译结果：{trans}"

def lookup_word(word: str) -> str:
    """查询单词释义（模拟）"""
    mock_def = {
        "python": "一种高级编程语言，以其简洁易读的语法著称。",
        "agent": "在 AI 领域，指能够自主感知环境并采取行动以实现目标的实体。",
        "api": "Application Programming Interface，应用程序编程接口。"
    }
    if word.lower() in mock_def:
        return f"📖 {word}：{mock_def[word.lower()]}"
    else:
        return f"📖 未找到 '{word}' 的定义，请确认拼写。"

def parse_rule_based(text: str) -> dict:
    """
    返回格式：{"action": "calculate"|"translate"|"lookup"|"unknown", "params": {...}}
    """
    # 1. 判断是否包含 "计算" 或 "+" 等运算符
    if any(op in text for op in ["+", "-", "*", "/"]) or "计算" in text:
        expr = text.replace("计算", "").strip()
        return {"action": "calculate", "params": {"expr": expr}}

    # 2. 判断是否包含 "翻译" 或 "translate"
    elif "翻译" in text or "translate" in text:
        trans_text = text.replace("翻译", "").strip()
        return {"action": "translate", "params": {"text": trans_text, "target": "中文"}}

    # 3. 判断是否包含 "查询" 或 "意思" 或 "definition"
    elif "查询" in text or "意思" in text or "definition" in text:
        word = text.replace("查询", "").replace("意思", "").strip()
        return {"action": "lookup", "params": {"word": word}}

    else:
        return {"action": "unknown", "params": {}}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学四则运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expr": {"type": "string", "description": "数学表达式，如 3+5*2"}
                },
                "required": ["expr"]
            }
        }
    },
    # TODO 空1：translate工具定义
    {
        "type": "function",
        "function": {
            "name": "translate",
            "description": "文本翻译工具，默认翻译成中文",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "待翻译文本"},
                    "target": {"type": "string", "description": "目标语言", "default": "中文"}
                },
                "required": ["text"]
            }
        }
    },
    # TODO 空2：lookup_word工具定义
    {
        "type": "function",
        "function": {
            "name": "lookup_word",
            "description": "查询单词释义",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {"type": "string", "description": "待查询单词"}
                },
                "required": ["word"]
            }
        }
    }
]

def call_llm_with_tools(messages: list) -> str:
    """
    调用 DeepSeek API，支持原生 Function Calling
    参数 messages: 对话历史列表
    返回：最终的文本回复
    """
    # ---------- 1. 配置 API ----------
    API_KEY = os.getenv("DEEPSEEK_API_KEY")
    API_URL = "https://api.deepseek.com/v1/chat/completions"
    MODEL_NAME = "deepseek-chat"

    # 准备请求体
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "tools": TOOLS,          # 关键！传入你定义的工具列表
        "tool_choice": "auto",   # 让模型自主决定是否调用工具
        "temperature": 0.3
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # ---------- 2. 第一次请求（让模型决定是否需要调用工具） ----------
    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    result = response.json()
    assistant_message = result["choices"][0]["message"]

    # 将模型的回复追加到消息历史
    messages.append(assistant_message)

    # ---------- 3. 检查是否有工具调用 ----------
    if "tool_calls" in assistant_message:
        # 获取第一个工具调用（可扩展处理多个）
        tool_call = assistant_message["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])  # 解析参数

        # ---------- 4. 根据工具名称执行对应的函数 ----------
        if tool_name == "calculate":
            function_response = calculate(**tool_args)
        elif tool_name == "translate":
            function_response = translate(**tool_args)
        elif tool_name == "lookup_word":
            function_response = lookup_word(**tool_args)
        else:
            function_response = f"❌ 未知工具：{tool_name}"

        # ---------- 5. 将工具执行结果以 "tool" 角色回传给模型 ----------
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],  # 必须带上 ID
            "content": function_response
        })

        # ---------- 6. 第二次请求（让模型根据工具结果生成最终回复） ----------
        # 注意：第二次请求不需要再传 tools
        payload_second = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.3
        }
        resp2 = requests.post(API_URL, json=payload_second, headers=headers, timeout=30)
        final_result = resp2.json()
        final_message = final_result["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": final_message})
        return final_message

    # 如果没有工具调用，直接返回模型的文本回复
    return assistant_message.get("content", "我没有理解你的意思。")

def main():
    print("选择模式：rule / llm / exit")
    messages = [{"role": "system", "content": "你是一个智能助手，拥有计算、翻译和查询单词的能力。"}]

    while True:
        mode = input("\n请输入模式(rule/llm/exit):").strip()
        if mode == "exit":
            print("退出程序")
            break
        if mode not in ["rule", "llm"]:
            print("模式只能输入 rule / llm / exit")
            continue

        user_text = input("请输入你的指令：").strip()
        if mode == "rule":
            intent = parse_rule_based(user_text)
            action = intent["action"]
            params = intent["params"]
            if action == "calculate":
                print(calculate(**params))
            elif action == "translate":
                print(translate(**params))
            elif action == "lookup":
                print(lookup_word(**params))
            else:
                print("⚠️ 无法识别该指令")

        elif mode == "llm":
            messages.append({"role": "user", "content": user_text})
            reply = call_llm_with_tools(messages)
            print(f"🤖 Agent：{reply}")
if __name__ == "__main__":
    main()
