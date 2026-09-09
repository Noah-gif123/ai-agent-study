"""
Day 6 实战：世界之最查询器（接入 DeepSeek + Function Calling）
功能：用户输入关键词（如山、海、河、湖），返回对应的世界之最信息
限制：最多 5 轮对话
特性：结果持久化、Token 监控、异常兜底
"""

import os
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# ========== 1. 加载环境变量 ==========
#导入包 + 加载环境变量
#读取当前目录的.env文件
load_dotenv()
#取出.env文件中的DEEPSEEK_API_KEY变量
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
#如果没有设置DEEPSEEK_API_KEY，则抛出异常
if not DEEPSEEK_API_KEY:
    raise ValueError("请在 .env 中设置 DEEPSEEK_API_KEY")

# ========== 2. 日志配置 ==========
# 创建日志目录，确定日志文件夹名
LOG_DIR = "logs"
# 创建 logs 文件夹，如果目录存在不会报错
os.makedirs(LOG_DIR, exist_ok=True)

# 创建 logger 对象，控制台输出通道和文件输出通道
console_handler = logging.StreamHandler()
#**控制台只打印 INFO 及以上**，DEBUG 调试信息控制台看不见
#DEBUG < INFO < WARNING < ERROR < CRITICAL
console_handler.setLevel(logging.INFO)
#文件输出通道，写入`logs/world_record.log`，utf8 防止中文乱码
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "world_record.log"), encoding="utf-8")
#日志文件保存 DEBUG 及以上所有日志信息
file_handler.setLevel(logging.DEBUG)
#日志模板，时间、logger 名称、级别、文件名 + 行号、日志消息
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
#给两个通道绑定这个日志模板
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

#全局日志基础配置，`handlers`传入两个输出通道，`level`设置 DEBUG
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
#拿到当前模块的 logger 对象，后面用`logger.info/debug/error`打印日志
logger = logging.getLogger(__name__)

# ========== 3. Token 计数器 ==========
#尝试导入分词库`tiktoken`，**用来统计 token 数量（大模型按 token 计费）**
try:
    import tiktoken
    #加载 gpt3.5 的分词器
    ENCODING = tiktoken.encoding_for_model("gpt-3.5-turbo")
    logger.info("✅ tiktoken 加载成功")
    #如果没安装 tiktoken，捕获异常，ENCODING=None，计数直接返回 0，程序不会崩溃
except ImportError:
    logger.warning("⚠️ tiktoken 未安装，Token 统计返回 0")
    ENCODING = None

#函数，输入 messages 对话列表，返回 token 总数
def count_tokens(messages: list) -> int:
    #没有分词器直接返回 0
    if ENCODING is None:
        return 0
    text = ""
    for msg in messages:
        text += f"{msg['role']}: {msg.get('content', '')}\n"
    #调用 ENCODING 的 encode 函数，统计 token 数量
    return len(ENCODING.encode(text))

# ========== 4. 工具定义（世界之最数据库） ==========
#本地静态知识库字典，模拟数据库。key 是问题，value 是答案
WORLD_RECORDS = {
    "山": "世界最高峰是珠穆朗玛峰（海拔 8848.86 米），位于中国与尼泊尔边境。",
    "海": "世界最大的海是珊瑚海（面积约 479.1 万平方公里），位于太平洋西南部。",
    "河": "世界最长的河流是尼罗河（全长约 6670 公里），流经非洲东部。",
    "湖": "世界最大的淡水湖是苏必利尔湖（面积约 8.21 万平方公里），位于美国与加拿大之间。",
    "岛": "世界最大的岛屿是格陵兰岛（面积约 216.6 万平方公里），属于丹麦。",
    "沙漠": "世界最大的沙漠是撒哈拉沙漠（面积约 940 万平方公里），位于非洲北部。",
    "瀑布": "世界最宽的瀑布是伊瓜苏瀑布（宽约 2700 米），位于阿根廷与巴西边境。"
}

#工具本体，大模型触发工具调用后，Python 执行这个函数，返回结果
def query_world_record(category: str) -> str:
    """
    查询世界之最的工具函数
    参数 category: 类别（山、海、河、湖、岛、沙漠、瀑布）
    """
    #去掉前后空格
    category = category.strip()
    matched = None
    #1. **模糊匹配**。比如用户输入 “最高的山”，key="山" 在字符串里面，匹配成功
    #2. 匹配成功：返回知识库对应的文本；匹配失败返回提示，告知支持哪些类别。
    for key in WORLD_RECORDS:
        if key in category:
            matched = key
            break
    if matched:
        return WORLD_RECORDS[matched]
    else:
        return f"未找到关于“{category}”的世界之最，目前支持：{', '.join(WORLD_RECORDS.keys())}"

# ========== 5. 注册工具（JSON Schema） ==========
#`TOOLS`列表传给 DeepSeek API，**告诉模型：我这边有什么工具，工具叫什么、干什么，参数需要什么**
#`name`：工具函数名字，必须和 python 函数名完全一致
#`description`：给大模型看的，描述这个工具用途，模型靠这个判断要不要调用
# `parameters`：参数定义
# - `type:object`：参数是一个 json 对象
# - `properties`：里面的字段：category，字符串类型，描述给模型看
# - `required:["category"]`：category 是必填参数，模型必须生成这个字段
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_world_record",
            "description": "查询世界之最信息，例如世界最高峰、最大的海等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "查询类别，如'山'、'海'、'河'、'湖'、'岛'、'沙漠'、'瀑布'"
                    }
                },
                "required": ["category"]
            }
        }
    }
]
#模型收到 TOOLS 之后，当用户问题需要查世界之最，模型会输出`tool_calls`，里面包含工具名 + 参数 json 字符串。模型会自动调用工具函数，并返回结果

# ========== 6. 调用 DeepSeek API（含工具调用处理） ==========
import requests

#定义函数，函数名`call_deepseek_with_tools`
#调用 DeepSeek 并自动处理工具调用
def call_deepseek_with_tools(messages: list) -> dict:
    """
    调用 DeepSeek API，自动处理 tool_calls
    返回：最终的回复文本（dict）
    """
    # 设置请求头和请求体
    headers = {
        #告诉服务器本次请求体是 JSON 格式
        "Content-Type": "application/json",
        #Bearer 鉴权，带上你的 DeepSeek 密钥
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    #发给 API 的请求体 JSON
    payload = {
        #指定使用 deepseek-chat 模型
        "model": "deepseek-chat",
        #完整对话上下文
        "messages": messages,
        #工具定义 schema 列表，告诉模型有哪些可用工具
        "tools": TOOLS,
        #模型决定是否调用工具
        "tool_choice": "auto",
        #低随机性，更确定
        "temperature": 0.3,
        #限制模型单次最多输出 500 个 token
        "max_tokens": 500
    }

    # ----- 第一次请求（模型决定是否调用工具） -----
    #捕获本次 API 请求的网络异常。第一次请求：让模型思考，判断是否需要调用工具。
    #如果需要调用工具，模型会输出`tool_calls`，里面包含工具名 + 参数 json 字符串。模型会自动调用工具函数，并返回结果
    try:
        #发送 POST 请求到 DeepSeek 的对话补全接口。请求体是 JSON 格式的 payload
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            #自动把 payload 字典转为 json 字符串放入请求 body
            json=payload,
            #30 秒超时，防止程序卡死
            timeout=30
        )
        #如果 HTTP 状态码不是 200（401/404/500 等），直接抛出异常，进入 except。如果 HTTP 状态码是 200，继续执行
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"API 请求失败: {e}")
        return {"role": "assistant", "content": f"❌ 网络错误：{e}"}

    result = resp.json()
    assistant_msg = result["choices"][0]["message"]
    messages.append(assistant_msg)  # 保存模型的第一条回复

    # ----- 检查是否有工具调用 -----
    if "tool_calls" in assistant_msg:
        tool_call = assistant_msg["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])

        logger.info(f"🔧 调用工具：{tool_name}，参数：{tool_args}")

        # 执行工具
        try:
            if tool_name == "query_world_record":
                category = tool_args.get("category", "")
                tool_result = query_world_record(category)
            else:
                tool_result = f"未知工具：{tool_name}"
        except Exception as e:
            logger.error(f"工具执行异常: {e}")
            tool_result = f"❌ 工具执行失败：{e}"

        # 将工具结果以 tool 角色回传
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": tool_result
        })

        # ----- 第二次请求（模型根据工具结果生成最终回复） -----
        try:
            payload2 = {
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 500
            }
            resp2 = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload2,
                timeout=30
            )
            resp2.raise_for_status()
            result2 = resp2.json()
            final_msg = result2["choices"][0]["message"]
            messages.append(final_msg)
            return final_msg
        except requests.exceptions.RequestException as e:
            logger.error(f"二次请求失败: {e}")
            return {"role": "assistant", "content": f"❌ 二次请求错误：{e}"}

    else:
        # 没有工具调用，直接返回模型回复
        return assistant_msg

# ========== 7. 主循环（5轮限制 + 结果持久化） ==========
def save_record_to_file(category: str, result: str):
    """将查询结果追加到文件"""
    record_file = "output/world_records.txt"
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(record_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] 类别：{category} -> {result}\n")
    logger.info(f"结果已保存至 {record_file}")

def run_agent():
    logger.info("🚀 世界之最查询器启动")
    print("🌍 世界之最查询器（输入 exit 退出）")
    print("支持查询：山、海、河、湖、岛、沙漠、瀑布")

    messages = [{"role": "system", "content": "你是一个知识渊博的助手，擅长回答世界之最的问题。当用户询问某类别的世界之最时，请调用 query_world_record 工具。"}]

    total_tokens = 0
    max_rounds = 5
    round_count = 0

    while round_count < max_rounds:
        round_count += 1
        user_input = input(f"\n👤 第 {round_count} 轮，输入查询关键词：").strip()

        if user_input.lower() == "exit":
            logger.info("用户主动退出")
            break
        if not user_input:
            logger.warning("输入为空，重新输入")
            round_count -= 1
            continue

        # 添加用户消息
        messages.append({"role": "user", "content": user_input})

        # Token 预统计（请求前）
        tokens_before = count_tokens(messages)
        logger.debug(f"请求前 token 数：{tokens_before}")

        # 调用模型（含工具处理）
        start = time.time()
        try:
            final_msg = call_deepseek_with_tools(messages)
            elapsed = time.time() - start
        except Exception as e:
            logger.error(f"主循环异常: {e}")
            print(f"❌ 发生未知错误：{e}")
            continue

        reply = final_msg.get("content", "我无法回答这个问题。")
        print(f"🤖 Agent：{reply}")

        # 如果本次调用了工具，尝试提取查询类别并保存结果
        # 简单方法：从最后一条 tool 消息里提取内容
        for msg in reversed(messages):
            if msg.get("role") == "tool":
                tool_result = msg.get("content", "")
                # 尝试从原始用户输入中提取类别
                category = user_input
                save_record_to_file(category, tool_result)
                break

        # Token 后统计
        tokens_after = count_tokens(messages)
        total_tokens += tokens_after
        logger.info(
            f"第 {round_count} 轮完成 | 耗时 {elapsed:.2f}s | "
            f"本轮 tokens：{tokens_after} | 累计 tokens：{total_tokens}"
        )

        # 预警
        if tokens_after > 1000:
            logger.warning(f"本轮消息 token 数 {tokens_after} 超过 1000")
        if total_tokens > 2000:
            logger.warning(f"累计 token {total_tokens} 超过 2000，建议重置")

    logger.info(f"🏁 会话结束，共 {round_count} 轮，累计 tokens：{total_tokens}")
    print(f"\n📊 本次会话共消耗约 {total_tokens} tokens")
    print("📄 查询结果已保存至 output/world_records.txt")

# ========== 入口 ==========
if __name__ == "__main__":
    run_agent()