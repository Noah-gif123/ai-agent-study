import os
import json
import requests
from dotenv import load_dotenv
# ==========================================
# 0. 准备工作：加载环境变量 + 创建输出文件夹
# ==========================================
# 加载 .env 文件中的变量（必须放在最前面）
load_dotenv()
# 获取脚本所在目录，全局统一路径，修复文件夹创建位置问题
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件的绝对路径，并获取其所在目录的路径
OUTPUT_DIR = os.path.join(BASE_DIR, "output")  # 将 output 文件夹的路径拼接出来
os.makedirs(OUTPUT_DIR, exist_ok=True)  # 在脚本所在目录下创建output文件夹，已存在不会报错
print("✅ 环境变量已加载，output 文件夹已就绪。\n")
# ==========================================
# 任务 1：模拟或获取数据，并写入 JSON 文件
# 这里我们用昨天的 API 拉一份真实数据
# ==========================================
print("========== 任务 1：获取数据并写入 result.json ==========")
# 从环境变量读取 base_url（如果没读到，给个默认值方便调试）
#os.getenv(环境变量名, 默认值)，如果环境变量存在，返回环境变量的值，如果不存在，返回默认值
BASE_URL = os.getenv("BASE_URL", "https://api.zippopotam.us")
# 拼接 URL
url = f"{BASE_URL}/us/10002"
try:
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()  # 如果状态码不是 200，抛异常
    # 将响应对象解析为JSON格式数据
    data = resp.json()
    
    # --- 安全提取字段（Day 3 练过的防御性取值） ---
    result = {
        "邮政编码": data.get("post code", "未知"),
        "国家名称": data.get("country", "未知"),
        "州名全称": data.get("places", [{}])[0].get("state", "未知"),
        "城市/地名": data.get("places", [{}])[0].get("place name", "未知")
    }
    
    # --- 写入 JSON 文件（注意是 json.dump，没有 s） ---
    file_path = os.path.join(OUTPUT_DIR, "result.json")  # 使用全局OUTPUT_DIR拼接完整文件路径
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 数据已保存到 {file_path}")
    print(f"   → 内容预览：{json.dumps(result, indent=2,ensure_ascii=False)}\n")
except requests.exceptions.RequestException as e:
    print(f"❌ 网络请求失败：{e}")
    # 如果请求失败，造一个模拟数据用于演示文件写入
    print("⚠️ 使用模拟数据演示文件写入...")
    mock_result = {
        "邮政编码": "10001",
        "国家名称": "模拟国家",
        "州名全称": "模拟州",
        "城市/地名": "模拟城市"
    }
    mock_file_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(mock_file_path, "w", encoding="utf-8") as f:
        json.dump(mock_result, f, indent=2, ensure_ascii=False)
    print("✅ 模拟数据已保存。\n")
# ==========================================
# 任务 2：把刚存的文件读回来（验证持久化）
# ==========================================
print("========== 任务 2：读取 result.json ==========")
try:
    read_file_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(read_file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)  # 注意是 json.load，没有 s
    
    print("✅ 读取文件成功，内容如下：")
    print(json.dumps(loaded_data, indent=2, ensure_ascii=False))
    
    # 验证是否和原来的结构一致
    if "邮政编码" in loaded_data:
        print(f"   → 提取测试：邮政编码 = {loaded_data['邮政编码']}\n")
except FileNotFoundError:
    print("❌ 文件未找到，请先运行任务 1。\n")
# ==========================================
# 任务 3：演示从 .env 读取配置（前面已经做了）
# ==========================================
print("========== 任务 3：验证 .env 读取 ==========")
print(f"📌 从 .env 读取的 BASE_URL = {BASE_URL}")
if BASE_URL == "https://api.zippopotam.us":
    print("✅ 环境变量读取成功！\n")
else:
    print("⚠️ 未读取到 .env 中的值，使用了默认值。请检查 .env 文件是否存在。\n")
# ==========================================
print("========== 🏆 终极挑战：多邮编查询 & 历史记录 ==========")
# 初始化历史记录列表
history = []
# 如果之前有 history.json 文件，我们可以加载它（实现记忆恢复）
history_file_path = os.path.join(OUTPUT_DIR, "history.json")
if os.path.exists(history_file_path):
    try:
        with open(history_file_path, "r", encoding="utf-8") as f:
            history = json.load(f)
        print(f"📂 已加载历史记录，当前共 {len(history)} 条。")
    except (json.JSONDecodeError, FileNotFoundError):
        print("📂 历史文件损坏或不存在，重新开始。")
        history = []
print("\n💡 输入邮编查询（如 10001），输入 exit 退出程序。")
while True:
    user_input = input("\n🏙️ 请输入邮编（或 exit 退出）：").strip()
    
    # 退出条件
    if user_input.lower() == "exit":
        print("👋 用户主动退出。")
        break
    
    # 空输入过滤（Day 2 的 continue）
    if user_input == "":
        print("⚠️ 输入为空，请重新输入。")
        continue
    
    # ---------- 发起请求 ----------
    query_url = f"{BASE_URL}/us/{user_input}"
    print(f"⏳ 正在查询邮编 {user_input}，请稍候 ...{query_url} ...")
    
    try:
        resp = requests.get(query_url, timeout=5)
        
        # 如果状态码是 404（邮编不存在）
        if resp.status_code == 404:
            print(f"❌ 邮编 {user_input} 不存在，请重新输入。")
            continue  # 不存入历史，继续下一轮
        
        resp.raise_for_status()  # 其他 4xx/5xx 异常统一捕获
        data = resp.json()
        
        # ---------- 安全解析 ----------
        # 这里故意用紧凑写法，展示防御性取值的威力
        entry = {
            "查询邮编": user_input,
            "邮政编码": data.get("post code", "未知"),
            "国家": data.get("country", "未知"),
            "州": data.get("places", [{}])[0].get("state", "未知"),
            "城市": data.get("places", [{}])[0].get("place name", "未知")
        }
        
        # ---------- 存入内存 ----------
        history.append(entry)
        print(f"✅ 查询成功！已存入第 {len(history)} 条记录。")
        print(f"   → {entry['城市']}，{entry['州']}，{entry['国家']}")
        
        # ---------- 持久化到硬盘（每次查询都覆盖写入最新列表） ----------
        history_file_path = os.path.join(OUTPUT_DIR, "history.json")
        with open(history_file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print("   💾 历史记录已同步保存到文件。")
        
    except requests.exceptions.Timeout:
        print("⏰ 请求超时，请检查网络。")
    except requests.exceptions.ConnectionError:
        print("🔌 网络连接失败。")
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ HTTP 错误：{e}")
    except json.JSONDecodeError:
        print("❌ 返回数据格式错误，无法解析。")
    except Exception as e:
        print(f"💥 未知错误：{type(e).__name__} - {e}")
# ==========================================
# 程序结束，展示最终历史记录
# ==========================================
print("\n" + "="*40)
print("📋 本次会话结束，共查询了 {} 条历史记录：".format(len(history)))
if history:
    for idx, item in enumerate(history, start=1):
        print(f"--- 记录 {idx}：邮编 {item['查询邮编']} → {item['城市']}, {item['州']} ---")
else:
    print("（暂无有效查询记录）")
