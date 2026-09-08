import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ==========================================
# 1. API 配置
# ==========================================
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME = "deepseek-chat"

# ==========================================
# 2. 定义工具函数（真实的 Python 逻辑）
# ==========================================
def get_weather(city: str) -> str:
    """查询真实天气"""
    url = f"https://wttr.in/{city}?format=j1&days=1"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return f"⚠️ 查询失败，城市 '{city}' 可能不存在。"
        data = resp.json()
        current = data.get("current_condition", [{}])[0]
        temp = current.get("temp_C", "?")
        desc = current.get("weatherDesc", [{"value": "未知"}])[0]["value"]
        return f"🌤️ {city} 当前温度 {temp}°C，{desc}"
    except Exception as e:
        return f"❌ 请求异常：{e}"

def get_current_time() -> str:
    """获取当前时间"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"🕐 当前时间：{now}"

# ==========================================
# 3. 定义 Tools（按大模型要求的 JSON Schema 格式）
# ==========================================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的实时天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，比如：北京、上海、Tokyo"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的准确时间（年月日时分秒）",
            "parameters": {
                "type": "object",
                "properties": {}  # 不需要参数
            }
        }
    }
]

# ==========================================
# 4. 函数注册表（映射名称 -> 实际执行函数）
# ==========================================
AVAILABLE_FUNCTIONS = {
    "get_weather": get_weather,
    "get_current_time": get_current_time
}

def call_llm_with_tools(messages):
    """
    调用大模型，并自动处理工具调用
    返回：最终的回复文本
    """
    # 1. 准备请求体
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "tools": TOOLS,  # <-- 关键点：把工具定义传进去
        "tool_choice": "auto",  # 让模型自己决定是否需要调用工具
        "temperature": 0.3
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 2. 发送请求
    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    result = response.json()
    assistant_message = result["choices"][0]["message"]

    # 3. 将模型的回复追加到消息历史（先假定没有 tool_calls）
    messages.append(assistant_message)

    # 4. --- 核心逻辑：检查是否需要调用工具 ---
    # TODO 空1：如果模型返回了 tool_calls（即 assistant_message 中有 "tool_calls" 键）
    # 你就需要执行工具调用。
    if "tool_calls"in assistant_message:
        # 获取 tool_calls 列表（可能包含多个工具调用，这里我们只处理第一个）
        tool_calls = assistant_message["tool_calls"]
        tool_call = tool_calls[0]
        tool_name = tool_call["function"]["name"]
        # TODO 空2：解析 function 里的 arguments（注意它是一个 JSON 字符串）
        arguments = json.loads(tool_call["function"]["arguments"])
        
        # 5. 执行对应的函数
        function_to_call = AVAILABLE_FUNCTIONS[tool_name]
        # TODO 空3：根据工具名称决定传参方式（这里可以写通用调用，或者 if-else）
        # 如果 tool_name == "get_weather"，传入 arguments["city"]
        # 如果是 "get_current_time"，不需要传参
        if tool_name == "get_weather":
            function_response = function_to_call(arguments["city"])
        else:
            function_response = function_to_call()
        
        # 6. 将工具执行结果以 "tool" 角色发回给模型
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],  # 必须带上 id
            "content": function_response
        })
        
        # 7. 第二次调用模型，让它根据工具结果生成最终回复
        # TODO 空4：这里需要递归调用吗？为了简单，我们直接再发一次请求取最终结果。
        # 你可以直接再调用一次 API（或者重新利用上面的代码逻辑，这里我们写个简化的二次请求）
        payload_second = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.3
        }
        # 注意：第二次请求不需要再传 tools，因为我们已经拿到结果了
        resp2 = requests.post(API_URL, json=payload_second, headers=headers, timeout=30)
        final_result = resp2.json()
        final_message = final_result["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": final_message})
        return final_message

    # 如果没有 tool_calls，直接返回模型的文本回复
    return assistant_message.get("content", "我没有理解你的意思。")


def main():
    messages = [{"role": "system", "content": "你是一个智能助手，拥有查询天气和当前时间的能力。"}]
    print("🤖 支持：查天气（如：北京天气）、问时间、退出（exit）")

    while True:
        user_input = input("\n👤 用户：").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        reply = call_llm_with_tools(messages)
        print(f"🤖 Agent：{reply}")
        # 注意：messages 已经在 call_llm_with_tools 内部更新了，无需额外追加

if __name__ == "__main__":
    main()