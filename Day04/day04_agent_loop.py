import json
import requests
import re
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Optional
import os
from datetime import datetime

# ==========================================
# 0. 准备工作：工具函数（复用天气查询）
# ==========================================

class WeatherParams(BaseModel):
    """天气查询参数校验"""
    city: str = Field(..., description="城市名")
    days: int = Field(default=1, ge=1, le=3, description="查询天数 1~3")

def get_weather(params: WeatherParams) -> str:
    """
    真实的天气查询工具
    返回：格式化的天气字符串
    """
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
            date = day.get("date", f"第{i+1}天")
            temp_max = day.get("maxtempC", "?")
            temp_min = day.get("mintempC", "?")
            desc = day.get("hourly", [{}])[0].get("weatherDesc", [{"value": "未知"}])[0]["value"]
            
            if i == 0:
                prefix = "今天"
            elif i == 1:
                prefix = "明天"
            else:
                prefix = f"后天（{date}）"
            summaries.append(f"{prefix}：{temp_min}~{temp_max}°C，{desc}")
        
        return f"📅 {params.city} 天气：\n" + "\n".join(summaries)
        
    except Exception as e:
        return f"❌ 请求异常：{e}"

# ==========================================
# 1. 模拟大模型“思考”的函数（核心替换点）
# 修正：优先匹配“城市名+天气”模式
# ==========================================

def mock_llm_think(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    模拟大模型根据当前对话历史，输出决策。
    真实场景：这里调用 OpenAI / 智谱 / 通义千问 的 API。
    今天我们用 if-else 逻辑模拟。
    """
    # 获取最后一条用户消息
    last_user_msg = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            last_user_msg = msg["content"].lower()
            break
    
    # 默认返回“结束”动作
    response = {
        "thought": "任务已完成，准备结束。",
        "action": "finish",
        "action_input": {}
    }
    
    # ---------- 模拟决策逻辑 ----------
    if "天气" in last_user_msg or "温度" in last_user_msg:
        # 尝试提取城市名，优先匹配“城市+天气”模式
        city = None
        # 先匹配“XX天气”
        city_match = re.search(r'([\u4e00-\u9fa5]{2,3})天气', last_user_msg)
        if city_match:
            city = city_match.group(1)
        else:
            # 再尝试匹配纯城市名（可能用户只输入“北京”）
            city_match = re.search(r'([\u4e00-\u9fa5]{2,3})', last_user_msg)
            if city_match:
                city = city_match.group(1)
            else:
                city = None
        
        if city:
            response = {
                "thought": f"用户想查询{city}的天气，我需要调用天气工具。",
                "action": "get_weather",
                "action_input": {"city": city, "days": 1}
            }
        else:
            response = {
                "thought": "用户想查天气，但我没识别出城市名，请用户补充。",
                "action": "finish",
                "action_input": {"answer": "请问您想查询哪个城市的天气呢？"}
            }
    elif "exit" in last_user_msg or "退出" in last_user_msg:
        response = {
            "thought": "用户想退出，结束对话。",
            "action": "finish",
            "action_input": {"answer": "好的，再见！"}
        }
    else:
        # 普通闲聊
        response = {
            "thought": "用户说了句普通的话，我直接回复。",
            "action": "finish",
            "action_input": {"answer": f"您好！我收到了您的消息：'{last_user_msg}'。我可以帮您查天气（例如：北京天气），或输入 exit 退出。"}
        }
    
    return response

# ==========================================
# 2. 工具注册表（Tool Registry）
# ==========================================

TOOLS = {
    "get_weather": {
        "function": get_weather,
        "params_model": WeatherParams
    }
}

def execute_tool(action: str, action_input: dict) -> str:
    """
    执行工具调用
    """
    if action not in TOOLS:
        return f"❌ 未知工具：{action}"
    
    tool = TOOLS[action]
    try:
        # 用 Pydantic 校验参数
        validated_params = tool["params_model"](**action_input)
        # 执行函数
        result = tool["function"](validated_params)
        return result
    except ValidationError as e:
        error_msgs = [f"{'.'.join(err['loc'])}：{err['msg']}" for err in e.errors()]
        return f"❌ 工具参数校验失败：{'; '.join(error_msgs)}"
    except Exception as e:
        return f"❌ 工具执行异常：{e}"

# ==========================================
# 🏆 终极挑战：ReAct Agent 主循环
# ==========================================

def run_agent():
    """
    ReAct Agent 主循环
    """
    print("="*50)
    print("🤖 ReAct Agent 已启动（模拟模式）")
    print("📌 你可以输入：'北京天气'、'上海天气'、'exit' 等")
    print("="*50)
    
    # 1. 初始化消息队列（Day 1 知识）
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以查询天气。当用户问天气时，调用 get_weather 工具。"}
    ]
    
    # 2. 循环控制变量（Day 2 知识）
    max_steps = 5
    step = 0
    finished = False
    
    while step < max_steps and not finished:
        step += 1
        print(f"\n--- 第 {step} 轮 ---")
        
        # 获取用户输入
        user_input = input("👤 用户：").strip()
        if user_input == "":
            print("⚠️ 输入为空，请重新输入。")
            step -= 1  # 不消耗步数
            continue
        
        # 追加用户消息到历史（Day 1）
        messages.append({"role": "user", "content": user_input})
        
        # 3. Agent 思考（调用模拟 LLM）
        print("🧠 Agent 思考中...")
        llm_output = mock_llm_think(messages)
        
        thought = llm_output.get("thought", "")
        action = llm_output.get("action", "finish")
        action_input = llm_output.get("action_input", {})
        
        print(f"💭 思考：{thought}")
        print(f"🎯 动作：{action}")
        print(f"📦 参数：{json.dumps(action_input, ensure_ascii=False)}")
        
        # 4. 执行动作
        if action == "finish":
            # 如果模型返回了最终的答案，直接回复
            final_answer = action_input.get("answer", "好的，任务完成。")
            print(f"🤖 Agent：{final_answer}")
            messages.append({"role": "assistant", "content": final_answer})
            finished = True
            break
        else:
            # 5. 执行工具调用（Observation）
            print(f"🔧 正在执行工具：{action}...")
            observation = execute_tool(action, action_input)
            print(f"👀 观察结果：\n{observation}")
            
            # 6. 将工具执行结果追加到消息历史（这是 ReAct 的关键！）
            messages.append({
                "role": "tool",
                "tool_name": action,
                "content": observation
            })
            
            # 真实场景：LLM 会根据 Observation 自动决定下一步。
            # 在模拟模式中，我们让用户继续输入新的指令。
            print("\n💡 （模拟模式：请继续输入新的指令，或输入 exit 结束）")
    
    # 7. 循环结束后的收尾
    if not finished and step >= max_steps:
        print(f"\n⏰ 已达到最大步数 {max_steps}，自动结束。")
    else:
        print("\n✅ 对话已结束。")

# ==========================================
# 程序入口
# ==========================================

if __name__ == "__main__":
    run_agent()