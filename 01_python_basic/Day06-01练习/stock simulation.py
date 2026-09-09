# 场景：你是某金融科技公司的 Agent 工程师，需要开发一个 “智能股票行情助手”，它能回答用户关于股票价格、涨跌幅、市值等方面的问题。

# 数据源：你不需要真实 API，而是使用一个内置的模拟数据 CSV 文件（代码中会内置，无需外部文件）。

# 核心功能：

# 查询股票价格：输入股票代码（如 AAPL），返回当前价格。

# 查询涨跌幅：输入股票代码，返回今日涨跌幅百分比。

# 查询市盈率（PE）：输入股票代码，返回市盈率。

# 列出所有股票：返回所有可查询的股票代码和名称。

import os
import json
import logging
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
try:
    import tiktoken
except ImportError:
    tiktoken = None
import requests
from dotenv import load_dotenv

# ========== 加载环境变量 ==========
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ========== 任务1：模拟数据源 ==========
STOCK_DATA = {
    "AAPL": {"name": "Apple Inc.", "price": 175.34, "change_percent": 1.20, "pe_ratio": 28.50},
    "GOOGL": {"name": "Alphabet Inc.", "price": 142.80, "change_percent": -0.75, "pe_ratio": 24.20},
    "MSFT": {"name": "Microsoft Corp.", "price": 380.12, "change_percent": 0.54, "pe_ratio": 36.80},
    "TSLA": {"name": "Tesla Inc.", "price": 245.60, "change_percent": -2.10, "pe_ratio": 72.30},
    "AMZN": {"name": "Amazon.com Inc.", "price": 185.22, "change_percent": 0.92, "pe_ratio": 45.10},
    "META": {"name": "Meta Platforms", "price": 512.45, "change_percent": 1.85, "pe_ratio": 19.70},
    "NVDA": {"name": "NVIDIA Corp.", "price": 910.30, "change_percent": 2.31, "pe_ratio": 62.40},
    "ORCL": {"name": "Oracle Corp.", "price": 118.76, "change_percent": -0.33, "pe_ratio": 21.60},
}
NAME_TO_SYMBOL = {
    "Apple": "AAPL",
    "Google": "GOOGL",
    "Microsoft": "MSFT",
    "特斯拉": "TSLA",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Meta": "META",
    "Nvidia": "NVDA",
    "Oracle": "ORCL"
}

# ========== 任务2：Pydantic参数模型 + 工具函数 ==========
class StockSymbolParam(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=5, description="股票代码，1~5位字母")

def get_price(symbol: str) -> str:
    symbol = symbol.upper()
    if symbol not in STOCK_DATA:
        return f"❌ 未找到股票代码 {symbol}"
    info = STOCK_DATA[symbol]
    return f"📈 {symbol} 当前价格：${info['price']:.2f}"

def get_change(symbol: str) -> str:
    symbol = symbol.upper()
    if symbol not in STOCK_DATA:
        return f"❌ 未找到股票代码 {symbol}"
    info = STOCK_DATA[symbol]
    sign = "+" if info["change_percent"] >=0 else ""
    return f"📊 {symbol} 今日涨跌幅：{sign}{info['change_percent']:.2f}%"

def get_pe(symbol: str) -> str:
    symbol = symbol.upper()
    if symbol not in STOCK_DATA:
        return f"❌ 未找到股票代码 {symbol}"
    info = STOCK_DATA[symbol]
    return f"📉 {symbol} 市盈率：{info['pe_ratio']:.2f}"

def list_stocks() -> str:
    items = [f"{code}({data['name']})" for code, data in STOCK_DATA.items()]
    return f"📋 可查询的股票：{', '.join(items)}"

# ========== 任务3：工具注册表 TOOLS Schema + AVAILABLE_FUNCTIONS ==========
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "查询股票当前价格",
            "parameters": {
                "type": "object",
                "properties": {"symbol": {"type": "string", "description": "股票代码"}},
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_change",
            "description": "查询股票今日涨跌幅百分比",
            "parameters": {
                "type": "object",
                "properties": {"symbol": {"type": "string", "description": "股票代码"}},
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pe",
            "description": "查询股票市盈率PE",
            "parameters": {
                "type": "object",
                "properties": {"symbol": {"type": "string", "description": "股票代码"}},
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_stocks",
            "description": "列出所有支持查询的股票代码和名称",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]
AVAILABLE_FUNCTIONS = {
    "get_price": get_price,
    "get_change": get_change,
    "get_pe": get_pe,
    "list_stocks": list_stocks
}

# ========== 任务4：mock_llm_think 模拟LLM思考（规则匹配） ==========
def mock_llm_think(messages: list):
    user_msg = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_msg = msg["content"].strip()
            break
    lower_text = user_msg.lower()
    # 列出所有股票
    if "列出所有股票" in user_msg:
        return {"action": "list_stocks", "action_input": {}}
    # 名称映射匹配
    for name, sym in NAME_TO_SYMBOL.items():
        if name.lower() in lower_text:
            if "价格" in user_msg:
                return {"action": "get_price", "action_input": {"symbol": sym}}
            elif "涨跌幅" in user_msg:
                return {"action": "get_change", "action_input": {"symbol": sym}}
            elif "pe" in lower_text or "市盈率" in user_msg:
                return {"action": "get_pe", "action_input": {"symbol": sym}}
    # 直接代码匹配
    words = user_msg.split()
    for w in words:
        if w.upper() in STOCK_DATA:
            sym = w.upper()
            if "价格" in user_msg:
                return {"action": "get_price", "action_input": {"symbol": sym}}
            elif "涨跌幅" in user_msg:
                return {"action": "get_change", "action_input": {"symbol": sym}}
            elif "pe" in lower_text or "市盈率" in user_msg:
                return {"action": "get_pe", "action_input": {"symbol": sym}}
    # 无法识别
    return {"action": "finish", "action_input": {"reply": "我不理解，请询问股票信息。"}}

# ========== 任务5：execute_tool 执行工具，捕获参数校验异常 ==========
def execute_tool(action: str, action_input: dict):
    if action not in AVAILABLE_FUNCTIONS and action != "finish":
        return f"❌ 不存在工具 {action}"
    if action == "finish":
        return action_input["reply"]
    try:
        func = AVAILABLE_FUNCTIONS[action]
        if action == "list_stocks":
            return func()
        param = StockSymbolParam(**action_input)
        return func(param.symbol)
    except ValidationError as e:
        err_info = []
        for err in e.errors():
            err_info.append(f"字段 {'.'.join(err['loc'])}: {err['msg']}")
        return "❌ 参数校验失败：" + "; ".join(err_info)
    except Exception as e:
        logger.error(f"工具执行异常: {e}")
        return f"❌ 工具执行异常：{str(e)}"

# ========== 任务6：日志配置 + Token计数器 ==========
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "stock_agent.log"), encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)
logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
logger = logging.getLogger(__name__)

ENCODING = None
if tiktoken is not None:
    ENCODING = tiktoken.encoding_for_model("gpt-3.5-turbo")
    logger.info("✅ tiktoken 加载成功")
else:
    logger.warning("⚠️ tiktoken未安装，token统计返回0")

def count_tokens(messages: list) -> int:
    if ENCODING is None:
        return 0
    full_text = ""
    for m in messages:
        full_text += f"{m['role']}: {m.get('content','')}\n"
    return len(ENCODING.encode(full_text))

# ========== 任务7：对话压缩 TOKEN_LIMIT=800，调用DeepSeek生成摘要 ==========
TOKEN_LIMIT = 800
def compress_messages(messages: list):
    logger.info("===== 触发对话压缩 =====")
    before_token = count_tokens(messages)
    # 保留最近3条 user / assistant，跳过tool、tool_calls消息
    keep = []
    temp = []
    for m in reversed(messages):
        if m["role"] in ("user", "assistant"):
            temp.append(m)
        if len(temp) >=3:
            break
    keep = list(reversed(temp))
    # 取出历史消息，只把非system消息拿去做摘要
    old_msgs = [m for m in messages if m["role"] != "system"]
    old_text = json.dumps(old_msgs, ensure_ascii=False, indent=1)
    summary_prompt = f"请把下面对话内容精简成简短摘要，保留关键信息：\n{old_text}"
    headers = {"Content-Type":"application/json", "Authorization":f"Bearer {DEEPSEEK_API_KEY}"}
    payload = {
        "model":"deepseek-chat",
        "messages":[{"role":"user", "content":summary_prompt}],
        "temperature":0.3,
        "max_tokens":300
    }
    resp = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
    resp.raise_for_status()
    summary = resp.json()["choices"][0]["message"]["content"]
    new_system = {"role":"system", "content":f"你是股票行情助手，可以查询股价、涨跌幅、市盈率。历史对话摘要：{summary}"}
    new_messages = [new_system] + keep
    after_token = count_tokens(new_messages)
    logger.info(f"压缩前token: {before_token}, 压缩后token: {after_token}")
    logger.info("===== 压缩完成 =====")
    return new_messages

# ========== 任务8：主循环 ==========
def save_history(messages):
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "stock_history.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    logger.debug(f"对话历史保存到 {path}")

def run_stock_agent():
    logger.info("🚀 股票行情助手启动")
    messages = [{"role":"system", "content":"你是股票行情助手，可以查询股价、涨跌幅、市盈率。"}]
    max_round = 5
    round_cnt = 0
    total_tokens = 0
    print("📈 股票行情助手，输入 exit 退出，最多5轮对话")
    while round_cnt < max_round:
        round_cnt +=1
        user_input = input(f"\n第{round_cnt}轮，请输入查询：").strip()
        if user_input.lower() == "exit":
            logger.info("用户主动退出")
            break
        if not user_input:
            logger.warning("输入为空")
            round_cnt -=1
            continue
        messages.append({"role":"user", "content":user_input})
        # token监控
        current_tokens = count_tokens(messages)
        logger.info(f"本轮messages token数：{current_tokens}")
        total_tokens += current_tokens
        logger.info(f"累计token：{total_tokens}")
        if current_tokens >1000:
            logger.warning(f"警告！当前token {current_tokens} >1000")
        # 判断是否压缩
        if current_tokens > TOKEN_LIMIT:
            messages = compress_messages(messages)
        # mock llm思考
        think_result = mock_llm_think(messages)
        action = think_result["action"]
        action_input = think_result["action_input"]
        # 执行工具
        tool_output = execute_tool(action, action_input)
        messages.append({"role":"assistant", "content":tool_output})
        print(f"🤖 Agent: {tool_output}")
        # 保存历史
        save_history(messages)
    logger.info(f"会话结束，总轮次：{round_cnt}，累计token {total_tokens}")
    print(f"\n✅ 会话结束，对话记录保存在 output/stock_history.json")

if __name__ == "__main__":
    run_stock_agent()
