import os
import json
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

# ==========================================
# 0. 加载环境变量
# ==========================================
load_dotenv()

# ==========================================
# 1. 配置大模型 API（二选一，注释掉不用的那个）
# ==========================================

# ---------- 方案一：DeepSeek API（推荐） ----------
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

API_KEY = DEEPSEEK_API_KEY
API_URL = DEEPSEEK_URL
MODEL_NAME = "deepseek-chat"

# ==========================================
# 2. Pydantic 模型（工具参数校验）
# ==========================================

class WeatherParams(BaseModel):
    city: str = Field(..., description="城市名")
    days: int = Field(default=1, ge=1, le=3, description="查询天数 1~3")


# ==========================================
# 3. 工具函数
# ==========================================

def get_weather(params: WeatherParams) -> str:
    """查询天气（复用 Day 06 的代码）"""
    url = f"https://wttr.in/{params.city}?format=j1&days={params.days}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return f"⚠️ 查询失败，城市 '{params.city}' 可能不存在。"
        
        data = resp.json()
        weather_list = data.get("weather", [])
        actual_days = min(len(weather_list), params.days)
        
        if actual_days == 0:
            return "❌ 未获取到天气数据。"
        
        summaries = []
        for i in range(actual_days):
            day = weather_list[i]
            temp_max = day.get("maxtempC", "?")
            temp_min = day.get("mintempC", "?")
            desc = day.get("hourly", [{}])[0].get("weatherDesc", [{"value": "未知"}])[0]["value"]
            
            if i == 0:
                prefix = "今天"
            elif i == 1:
                prefix = "明天"
            else:
                prefix = f"后天（{day.get('date', '')}）"
            summaries.append(f"{prefix}：{temp_min}~{temp_max}°C，{desc}")
        
        return f"📅 {params.city} 天气：\n" + "\n".join(summaries)
        
    except Exception as e:
        return f"❌ 请求异常：{e}"


# ==========================================
# 4. 工具注册表
# ==========================================

TOOLS = {
    "get_weather": {
        "function": get_weather,
        "params_model": WeatherParams,
        "description": "查询指定城市的天气"
    }
}


# ==========================================
# 5. 核心函数：真实大模型调用（完整修复版）
# ==========================================

def real_llm_think(messages: list) -> dict:
    """
    调用真实大模型 API，让 AI 决定下一步动作
    修复：system去重、action_input类型转换、action合法性校验
    """
    system_prompt = """你是一个智能助手，可以调用工具来帮助用户。

你有以下工具可用：
- get_weather: 查询指定城市的天气。参数：city（城市名，必填），days（查询天数，1-3天，默认1）

当用户询问天气时，你应该调用 get_weather 工具。
返回格式必须是 JSON，且 action_input 必须是一个对象（字典）：
{"action": "get_weather", "action_input": {"city": "北京", "days": 1}}

如果用户的问题不需要调用工具，直接回复即可，action 设为 "finish"，action_input 为 {"answer": "你的回复内容"}。

工具执行结果会以 `[工具 xxx 返回结果]` 的形式作为用户消息返回，你需要根据这些结果来回答用户。
"""

    # 1. 过滤掉原有的 system 消息，避免重复
    filtered_messages = [msg for msg in messages if msg["role"] != "system"]
    request_messages = [{"role": "system", "content": system_prompt}] + filtered_messages

    payload = {
        "model": MODEL_NAME,
        "messages": request_messages,
        "temperature": 0.3,
        "max_tokens": 500
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        print("🌐 正在调用大模型 API...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_message = result["choices"][0]["message"]["content"]
        
        # 尝试解析 AI 返回的 JSON
        try:
            parsed = json.loads(ai_message)
            action = parsed.get("action", "finish")
            action_input = parsed.get("action_input", {})
            
            # ========== 核心修复：确保 action_input 是字典 ==========
            if isinstance(action_input, str):
                action_input = {"answer": action_input}
            elif not isinstance(action_input, dict):
                action_input = {"answer": str(action_input)}
            
            # ========== 确保 action 合法 ==========
            if action not in ["finish", "get_weather"]:
                action = "finish"
                if "answer" not in action_input:
                    action_input["answer"] = f"我不理解该操作：{action}"
            
            return {
                "thought": f"AI 思考结果：{ai_message}",
                "action": action,
                "action_input": action_input
            }
            
        except json.JSONDecodeError:
            # 如果不是 JSON，当作普通文本回复
            return {
                "thought": ai_message,
                "action": "finish",
                "action_input": {"answer": ai_message}
            }
            
    except requests.exceptions.Timeout:
        return {
            "thought": "API 请求超时",
            "action": "finish",
            "action_input": {"answer": "抱歉，请求超时，请稍后重试。"}
        }
    except requests.exceptions.ConnectionError:
        return {
            "thought": "网络连接失败",
            "action": "finish",
            "action_input": {"answer": "网络连接失败，请检查网络设置。"}
        }
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ HTTP 错误：{e}")
        if hasattr(e, 'response') and e.response:
            print(f"  响应内容：{e.response.text[:200]}")  # 只打印前200字符避免刷屏
        return {
            "thought": f"API 调用失败：{e}",
            "action": "finish",
            "action_input": {"answer": f"API 调用失败：{e}"}
        }
    except Exception as e:
        print(f"💥 未知错误：{type(e).__name__} - {e}")
        return {
            "thought": f"发生错误：{e}",
            "action": "finish",
            "action_input": {"answer": f"发生错误：{e}"}
        }


# ==========================================
# 6. 执行工具
# ==========================================

def execute_tool(action: str, action_input: dict) -> str:
    """执行工具调用（复用 Day 07 的代码）"""
    if action not in TOOLS:
        return f"❌ 未知工具：{action}"
    
    tool = TOOLS[action]
    try:
        validated_params = tool["params_model"](**action_input)
        result = tool["function"](validated_params)
        return result
    except ValidationError as e:
        error_msgs = [f"{'.'.join(err['loc'])}：{err['msg']}" for err in e.errors()]
        return f"❌ 工具参数校验失败：{'; '.join(error_msgs)}"
    except Exception as e:
        return f"❌ 工具执行异常：{e}"


# ==========================================
# 7. 主循环（使用真实大模型，修复多轮对话问题）
# ==========================================

def run_agent():
    print("=" * 50)
    print("🤖 ReAct Agent 已启动（接入真实大模型）")
    print(f"📌 使用模型：{MODEL_NAME}")
    print("💡 输入 'exit' 退出程序")
    print("=" * 50)

    # 初始化消息队列
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以查询天气。"}
    ]

    max_steps = 5
    step = 0
    finished = False

    while step < max_steps and not finished:
        step += 1
        print(f"\n--- 第 {step} 轮 ---")

        user_input = input("👤 用户：").strip()
        if not user_input:
            print("⚠️ 输入为空，请重新输入。")
            step -= 1
            continue

        if user_input.lower() == "exit":
            print("👋 用户主动退出。")
            break

        # 添加用户消息
        messages.append({"role": "user", "content": user_input})

        # 调用真实大模型
        print("🧠 Agent 正在思考（调用大模型 API）...")
        llm_output = real_llm_think(messages)

        thought = llm_output.get("thought", "")
        action = llm_output.get("action", "finish")
        action_input = llm_output.get("action_input", {})

        # ========== 额外防御（兜底） ==========
        if not isinstance(action_input, dict):
            action_input = {"answer": str(action_input)}

        print(f"💭 思考：{thought}")
        print(f"🎯 动作：{action}")
        print(f"📦 参数：{json.dumps(action_input, ensure_ascii=False)}")

        # 执行动作
        if action == "finish":
            final_answer = action_input.get("answer", "好的，任务完成。")
            print(f"🤖 Agent：{final_answer}")
            messages.append({"role": "assistant", "content": final_answer})
            finished = True
            break
        else:
            print(f"🔧 正在执行工具：{action}...")
            observation = execute_tool(action, action_input)
            print(f"👀 观察结果：\n{observation}")

            # ========== 关键修复：将工具结果以 user 角色追加 ==========
            messages.append({
                "role": "user",
                "content": f"[工具 {action} 返回结果]\n{observation}"
            })

    if not finished and step >= max_steps:
        print(f"\n⏰ 已达到最大步数 {max_steps}，自动结束。")
    else:
        print("\n✅ 对话已结束。")


# ==========================================
# 程序入口
# ==========================================

if __name__ == "__main__":
    if not API_KEY:
        print("❌ 错误：未找到 API Key！")
        print("请在 .env 文件中配置 DEEPSEEK_API_KEY 或 ZHIPU_API_KEY")
        print("然后重新运行程序。")
    else:
        run_agent()