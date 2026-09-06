#项目背景：
#你需要编写一个 ultimate_agent.py，实现一个 “智能文件归档助手”。这个 Agent 不查天气，而是模拟管理本地文件目录。
#核心需求：用户输入自然语言指令（如“列出当前目录所有文件”、“统计一下文件夹大小”、“新建一个叫 test 的文件夹”），Agent 通过模拟思考，调用相应的“工具函数”来完成任务。
# 你必须实现的 3 个核心工具（Tool）
# 你需要编写以下 3 个函数，并注册到 TOOLS 字典中：

# list_files：
# 功能：列出当前运行目录下的所有文件和文件夹。
# 参数：无（或可选参数 path，本期可忽略）。
# 返回：格式化的字符串（如 📁 找到 5 个条目：file1.py, folderA, ...）。
# 技术点：需使用 os.listdir() 或 os.scandir()。

# create_folder：
# 功能：根据名称创建一个新文件夹。
# Pydantic 参数校验：
# folder_name: str（必填，长度至少 1 个字符）。
# exist_ok: bool（可选，默认 False，决定如果文件夹已存在是否报错）。
# 返回：成功或失败的提示字符串。
# 技术点：使用 os.makedirs(folder_name, exist_ok=exist_ok)。

# get_file_size：
# 功能：获取指定文件的大小（以 KB 为单位）。
# Pydantic 参数校验：
# file_path: str（必填）。
# 返回：文件 xxx 大小为 xxx KB。（如果文件不存在，返回友好的提示信息）。
# 异常处理：如果文件不存在，必须捕获 FileNotFoundError 并返回友好提示，不能让程序崩溃。

# 验收标准（Checklist）
# □ 运行脚本，自动加载历史消息（如果存在）。
# □ 输入 列出，正确调用 list_files，显示工作目录下的文件列表。
# □ 输入 新建 folderA，正确调用 create_folder，文件夹被创建，且 Pydantic 校验通过。
# □ 再次输入 新建 folderA（重复），因为 exist_ok=False，Pydantic 或业务逻辑应报错提示“已存在”（或你自行修改逻辑让其通过）。
# □ 输入 大小 day04_pydantic.py（假设存在），正确返回文件大小。
# □ 输入 大小 不存在的文件.txt，返回“文件不存在”的友好提示（程序未崩溃）。
# □ 输入 hello，Agent 回复“我不理解...”的提示。
# □ 输入 exit，程序退出，且 output/archive_history.json 中存有本次对话的完整记录。
# □ 再次运行程序，上一条的对话记录被正确加载（例如再次输入 列出 前，可以看到历史消息打印）。

# ultimate_agent.py
# ultimate_agent.py
import os
import json
import re
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

# 1. 加载环境变量
load_dotenv()
WORK_DIR = os.getenv("WORK_DIR", "./agent_workspace")
os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)

# 2. 定义 Pydantic 模型
class CreateFolderParams(BaseModel):
    folder_name: str = Field(..., min_length=1)
    exist_ok: bool = Field(default=False)

class GetFileSizeParams(BaseModel):
    file_path: str = Field(..., min_length=1)

# 3. 工具函数
def list_files() -> str:
    entries = os.listdir(WORK_DIR)
    if not entries:
        return "📁 目录为空"
    return f"📁 找到 {len(entries)} 个条目：{', '.join(entries)}"

def create_folder(params: CreateFolderParams) -> str:
    full_path = os.path.join(WORK_DIR, params.folder_name)
    try:
        os.makedirs(full_path, exist_ok=params.exist_ok)
        return f"✅ 文件夹创建成功：{params.folder_name}"
    except FileExistsError:
        return f"⚠️ 文件夹已存在：{params.folder_name}"

def get_file_size(params: GetFileSizeParams) -> str:
    full_path = os.path.join(WORK_DIR, params.file_path)
    try:
        stat_info = os.stat(full_path)
        kb = stat_info.st_size / 1024
        return f"📄 文件 {params.file_path} 大小为 {kb:.2f} KB"
    except FileNotFoundError:
        return f"❌ 文件不存在：{params.file_path}"

# 4. 工具注册表
TOOLS = {
    "list_files": {"function": list_files, "params_model": None},
    "create_folder": {"function": create_folder, "params_model": CreateFolderParams},
    "get_file_size": {"function": get_file_size, "params_model": GetFileSizeParams}
}

# 5. 模拟 LLM 思考（更智能的规则匹配）
def mock_llm_think(messages) -> dict:
    # 取最后一条用户消息
    last_msg = messages[-1]["content"].strip()
    if not last_msg:
        return {"action": None, "action_input": None}

    # 1. 判断是否包含“列出”或“list”
    if "列出" in last_msg or "list" in last_msg.lower():
        return {"action": "list_files", "action_input": {}}

    # 2. 判断是否包含“新建”或“create”
    if "新建" in last_msg or "create" in last_msg.lower():
        # 尝试提取文件夹名：常见句式“新建 folderA”、“新建一个叫folderA的文件夹”
        # 方法：正则匹配中文或英文、数字、下划线组成的连续字符
        match = re.search(r'新建\s*([\w\u4e00-\u9fa5]+)', last_msg)
        if match:
            folder = match.group(1)
            return {"action": "create_folder", "action_input": {"folder_name": folder}}
        else:
            # 如果提取失败，尝试从“叫”或“名为”后面提取
            match = re.search(r'(?:叫|名为)\s*([\w\u4e00-\u9fa5]+)', last_msg)
            if match:
                folder = match.group(1)
                return {"action": "create_folder", "action_input": {"folder_name": folder}}
        # 如果实在提取不到，返回提示
        return {"action": None, "action_input": None, "hint": "未识别到文件夹名，请指定名称，如“新建 folderA”"}

    # 3. 判断是否包含“大小”或“size”
    if "大小" in last_msg or "size" in last_msg.lower():
        # 提取文件名：通常为“大小 test.txt” 或 “看看 test.txt 的大小”
        match = re.search(r'(?:大小|size)\s*([\w\.\-]+)', last_msg)
        if match:
            filename = match.group(1)
            return {"action": "get_file_size", "action_input": {"file_path": filename}}
        else:
            # 尝试提取“文件”后面的内容
            match = re.search(r'文件\s*([\w\.\-]+)', last_msg)
            if match:
                filename = match.group(1)
                return {"action": "get_file_size", "action_input": {"file_path": filename}}
        return {"action": None, "action_input": None, "hint": "未识别到文件名，请指定，如“大小 test.txt”"}

    # 4. 检查是否包含退出关键词
    if "exit" in last_msg.lower() or "退出" in last_msg:
        return {"action": "finish", "action_input": {"answer": "已收到退出指令"}}

    # 5. 默认：不理解
    return {"action": None, "action_input": None}

# 6. 执行工具
def execute_tool(action, action_input) -> str:
    tool_info = TOOLS.get(action)
    if not tool_info:
        return f"❌ 未知工具：{action}"
    func = tool_info["function"]
    model_cls = tool_info["params_model"]

    if model_cls is None:
        return func()
    try:
        params = model_cls(**action_input)
        return func(params)
    except ValidationError as e:
        errs = []
        for err in e.errors():
            field = ".".join(err["loc"])
            errs.append(f"字段 {field}：{err['msg']}")
        return "⚠️ 参数校验失败：" + "; ".join(errs)

# 7. 加载历史记录
history_file = "output/archive_history.json"
messages = []
if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
    print(f"💾 已加载历史对话记录，共 {len(messages)} 条消息")
else:
    # 如果历史文件不存在，初始化系统提示
    messages = [{"role": "system", "content": "你是文件管理助手，支持列出、新建文件夹、查看文件大小。"}]

# 8. 主循环
max_steps = 5
step = 0
finished = False

print("📂 工作目录：", WORK_DIR)
print("💡 支持指令：列出、新建 文件夹名、大小 文件名、exit")

while step < max_steps and not finished:
    user_input = input("\n👤 用户：").strip()
    
    # 空输入处理：不消耗步数
    if not user_input:
        print("⚠️ 输入为空，请重新输入。")
        continue

    # 退出指令（直接退出循环）
    if user_input.lower() in ["exit", "退出"]:
        finished = True
        messages.append({"role": "user", "content": user_input})
        break

    # 添加用户消息到历史
    messages.append({"role": "user", "content": user_input})

    # Agent 思考
    think_result = mock_llm_think(messages)
    action = think_result.get("action")
    action_input = think_result.get("action_input", {})
    hint = think_result.get("hint")

    # 处理特殊 action: finish
    if action == "finish":
        reply = "👋 " + action_input.get("answer", "再见！")
        print(f"🤖 Agent：{reply}")
        messages.append({"role": "assistant", "content": reply})
        finished = True
        break

    # 处理未知指令或提取失败
    if action is None:
        reply = "🤖 我不理解该指令。"
        if hint:
            reply += " " + hint
        else:
            reply += " 支持指令：列出、新建 文件夹名、大小 文件名、exit"
    else:
        reply = execute_tool(action, action_input)

    print(f"🤖 Agent：{reply}")
    messages.append({"role": "assistant", "content": reply})
    step += 1

    # 检查是否达到步数上限
    if step >= max_steps:
        print(f"\n⏰ 已达到最大步数 {max_steps}，自动结束。")

# 9. 保存完整对话历史
with open(history_file, "w", encoding="utf-8") as f:
    json.dump(messages, f, ensure_ascii=False, indent=2)

print(f"\n💾 对话已保存至 {history_file}，程序退出。")
