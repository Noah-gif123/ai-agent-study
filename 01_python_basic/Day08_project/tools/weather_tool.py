# -*- coding: utf-8 -*-
"""天气工具（Day 04 + Day 06 的知识）"""
import requests
from pydantic import BaseModel, Field, ValidationError

class WeatherParams(BaseModel):
    city: str = Field(..., min_length=1, description="城市名")

def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=j1"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return f"⚠️ 查询失败，城市 '{city}' 可能不存在。"
        data = resp.json()
        current = data.get("current_condition", [{}])[0]
        temp = current.get("temp_C", "?")
        desc = current.get("weatherDesc", [{"value": "未知"}])[0]["value"]
        return f"🌤️ {city}：{temp}°C，{desc}"
    except Exception as e:
        return f"❌ 请求异常：{e}"

TOOL_DEFINITION = {
    "name": "get_weather",
    "description": "查询指定城市的实时天气",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "城市名"}},
        "required": ["city"]
    },
    "func": get_weather,
    "params_model": WeatherParams
}