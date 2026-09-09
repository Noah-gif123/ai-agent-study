import os
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# ========== 任务 1：配置 logging ==========
# 配置 logging 同时输出到控制台和文件
# - 控制台输出 INFO 及以上级别
# - 文件输出 DEBUG 及以上级别，保存为 logs/agent.log
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 配置 logging（完成空1）
# 先创建两个handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台只输出 INFO 及以上

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "agent.log"), encoding="utf-8")
file_handler.setLevel(logging.DEBUG)  # 文件记录 DEBUG 及以上
#DEBUG < INFO < WARNING < ERROR < CRITICAL
# 配置日志格式
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[console_handler, file_handler]
)
# ========== 任务 2：Token 计数器 ==========
try:
    import tiktoken
    ENCODING = tiktoken.encoding_for_model("gpt-3.5-turbo")
except ImportError:
    print("⚠️ tiktoken 未安装，请执行 pip install tiktoken")
    ENCODING = None

def count_tokens(messages: list) -> int:
    """计算 messages 列表的 token 总数"""
    if ENCODING is None:
        return 0
    # 完成空2：将 messages 转成文本后计算 token
    text = ""
    for msg in messages:
        # 提取 role 和 content，如果 content 不存在则用空字符串
        role = msg.get("role", "")
        content = msg.get("content", "")
        text += f"{role}: {content}\n"
    return len(ENCODING.encode(text))

# ========== 任务 3：模拟 Agent 主循环（集成日志和监控） ==========
def mock_llm_response(user_input: str) -> str:
    """模拟大模型返回（仅用于演示）"""
    time.sleep(0.5)  # 模拟网络延迟
    return f"你说了：{user_input}，我收到了！"

def run_agent():
    # 初始化消息历史
    messages = [{"role": "system", "content": "你是一个智能助手。"}]
    
    # 累计 token 消耗
    total_tokens = 0
    max_steps = 5
    step = 0

    logging.info("===== Agent 启动 =====")
    logging.info(f"初始 messages 长度：{len(messages)} 条")

    while step < max_steps:
        step += 1
        user_input = input("\n👤 用户：").strip()
        if user_input.lower() == "exit":
            logging.info("用户主动退出")
            break
        if not user_input:
            logging.warning("用户输入为空，重新请求")
            step -= 1
            continue

        # 追加用户消息
        messages.append({"role": "user", "content": user_input})
        logging.debug(f"用户消息：{user_input}")

        # 模拟 Agent 思考（此处可替换为真实 API）
        start_time = time.time()
        reply = mock_llm_response(user_input)
        elapsed = time.time() - start_time

        # 追加助手回复
        messages.append({"role": "assistant", "content": reply})
        print(f"🤖 Agent：{reply}")

        # ========== 任务 4：Token 统计与预警 ==========
        # 完成空3：计算当前 messages 的 token 数，累加到 total_tokens
        tokens_this_round = count_tokens(messages)
        total_tokens += tokens_this_round
        
        # 如果单次请求 token > 1000，打印警告
        if tokens_this_round > 1000:
            logging.warning(f"本轮 token 数 {tokens_this_round} 超过 1000，注意预算！")
        # 如果累计 token > 2000，打印警告
        if total_tokens > 2000:
            logging.warning(f"累计 token 数 {total_tokens} 超过 2000，建议重置对话！")

        # 记录日志
        logging.info(
            f"第 {step} 轮完成 | 耗时 {elapsed:.2f}s | "
            f"当前总 tokens：{total_tokens}"
        )

    # 最终总结
    logging.info(f"Agent 结束 | 总步数：{step} | 累计 tokens：{total_tokens}")
    print(f"\n📊 本次会话共消耗约 {total_tokens} tokens")

# ========== 程序入口 ==========
if __name__ == "__main__":
    load_dotenv()
    run_agent()
