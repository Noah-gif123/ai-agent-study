# 路径拼接："configs/" + username + ".json"	改为 os.path.join("configs", f"{username}.json")
# load_user_config 无异常处理	增加了 FileNotFoundError 和 json.JSONDecodeError 捕获，返回空字典兜底
# save_user_data 未被调用	在主循环中增加了 save_user_xxx 命令，真正调用该函数，形成了"增删查"闭环
# cmd.split("_")[1] 会导致索引越界	改用 re.match(r'^(get_user|save_user)_(\w+)$', cmd)，不匹配就直接跳过，绝不报错
# eval(raw_input) 致命安全漏洞	完全删除 eval，改用 json.loads 仅解析数据格式，并做了单独的异常捕获
# 无 list 命令，不知道存了啥	增加了 list 命令，列出所有已存储的用户名
import os
import json
import re  # 用于安全提取

# ==========================================
# 修复点 1：路径拼接使用 os.path.join（跨平台兼容）
# 修复点 2：增加 try-except 处理文件不存在和 JSON 格式错误
# ==========================================
def load_user_config(username):
    """加载用户配置，如果文件不存在或格式错误，返回空字典并提示"""
    # 使用 os.path.join 代替字符串拼接
    file_path = os.path.join("configs", f"{username}.json")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 成功加载 {username} 的配置")
        return data
    except FileNotFoundError:
        print(f"⚠️ 用户 {username} 的配置文件不存在，将返回空配置。")
        return {}  # 优雅降级，不崩溃
    except json.JSONDecodeError:
        print(f"❌ 用户 {username} 的配置文件格式损坏，已重置。")
        return {}  # 防止因格式错误导致整个程序卡死

def save_user_data(username, data):
    """保存用户数据，确保目录存在"""
    file_path = os.path.join("configs", f"{username}.json")
    
    try:
        # 确保目录存在（防止手动删除 configs 文件夹导致报错）
        os.makedirs("configs", exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 用户 {username} 的数据已保存成功！")
        return True
    except Exception as e:
        print(f"❌ 保存失败：{e}")
        return False

# ==========================================
# 修复点 3：彻底移除危险的 eval()
# 改为直接返回字符串提示，或者交由主流程处理
# 在 Agent 真实场景中，这里会调用 Pydantic 模型，而不是执行用户代码
# ==========================================
def process_input(raw_input):
    """
    安全处理用户输入（模拟工具解析）
    不再执行任何代码，只做简单的文本反应
    """
    # 如果用户输入看起来像 JSON，只打印解析后的结构，绝不执行
    if raw_input.strip().startswith('{') and raw_input.strip().endswith('}'):
        try:
            data = json.loads(raw_input)
            return f"识别到 JSON 数据：{json.dumps(data, ensure_ascii=False)}"
        except json.JSONDecodeError:
            return "输入的不是合法的 JSON 格式"
    else:
        # 普通文本直接返回
        return f"收到指令：{raw_input}"

# ==========================================
# 修复点 4：逻辑闭环——让 save 函数真正被调用
# 增加“列出所有配置”功能，让 get/save/list 形成完整闭环
# ==========================================
def list_all_users():
    """列出 configs 目录下所有的 JSON 配置文件"""
    try:
        files = os.listdir("configs")
        json_files = [f.replace(".json", "") for f in files if f.endswith(".json")]
        if not json_files:
            return "📁 当前没有存储任何用户数据。"
        return f"📁 已存储的用户：{', '.join(json_files)}"
    except FileNotFoundError:
        return "📁 configs 目录尚未创建。"

# ==========================================
# 修复点 5：重写主循环，增加边界判断和命令解析
# 支持：get_user_xxx、save_user_xxx {json}、list、quit
# ==========================================
def main_loop():
    print("="*40)
    print("📂 用户数据管理 Agent (修复版)")
    print("支持命令：")
    print("  - get_user_<用户名>     (获取用户配置)")
    print("  - save_user_<用户名>    (保存用户配置，需输入 JSON 数据)")
    print("  - list                  (列出所有用户)")
    print("  - quit                  (退出程序)")
    print("="*40)

    while True:
        cmd = input("\n请输入命令：").strip()
        
        # 1. 退出
        if cmd.lower() == "quit":
            print("👋 程序退出。")
            break
        
        # 2. 空输入处理
        if not cmd:
            print("⚠️ 输入为空，请重新输入。")
            continue

        # 3. list 命令
        if cmd == "list":
            print(list_all_users())
            continue

        # 4. 正则提取命令（安全性远比暴力 split 高）
        # 匹配 get_user_xxx 或 save_user_xxx
        match = re.match(r'^(get_user|save_user)_(\w+)$', cmd)
        
        if match:
            action = match.group(1)  # get_user 或 save_user
            username = match.group(2)  # 用户名（只允许字母数字下划线）

            if action == "get_user":
                # 加载并打印配置
                config = load_user_config(username)
                print(f"📋 {username} 的配置内容：{json.dumps(config, ensure_ascii=False)}")
                
            elif action == "save_user":
                # 获取要保存的数据
                data_input = input(f"请输入要保存的 JSON 数据（将覆盖 {username} 的现有配置）：").strip()
                try:
                    # 尝试解析 JSON
                    new_data = json.loads(data_input)
                    save_user_data(username, new_data)
                except json.JSONDecodeError:
                    print("❌ 输入的不是有效的 JSON 格式，保存失败。")
            continue

        # 5. 其他指令（走安全处理流程，不使用 eval）
        result = process_input(cmd)
        print(f"🤖 处理结果：{result}")

# ==========================================
# 程序入口
# ==========================================
if __name__ == "__main__":
    os.makedirs("configs", exist_ok=True)
    main_loop()