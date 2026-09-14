# -*- coding: utf-8 -*-
"""工具注册表"""
from pydantic import ValidationError
from tools.time_tool import TOOL_DEFINITION as TIME_TOOL
from tools.weather_tool import TOOL_DEFINITION as WEATHER_TOOL
from utils.logger import get_logger

logger = get_logger(__name__)

# 所有工具定义
ALL_TOOLS = [TIME_TOOL, WEATHER_TOOL]

# 生成 LLM 需要的 JSON Schema 列表
def get_tools_schema():
    """返回给 LLM 的工具列表（符合 Function Calling 格式）"""
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"]
            }
        }
        for t in ALL_TOOLS
    ]

# 生成 {工具名: 工具信息} 映射
TOOL_MAP = {t["name"]: t for t in ALL_TOOLS}

def execute_tool(action: str, action_input: dict) -> str:
    """执行工具（含参数校验）"""
    if action not in TOOL_MAP:
        return f"❌ 未知工具：{action}"

    tool = TOOL_MAP[action]
    try:
        if "params_model" in tool:
            params = tool["params_model"](**action_input)
            return tool["func"](**params.model_dump())
        else:
            return tool["func"]()
    except ValidationError as e:
        errors = [f"{'.'.join(err['loc'])}: {err['msg']}" for err in e.errors()]
        return f"❌ 参数校验失败：{'; '.join(errors)}"
    except Exception as e:
        logger.error(f"工具执行异常: {e}")
        return f"❌ 执行失败：{e}"