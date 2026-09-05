import json
import requests
from datetime import datetime

# ==========================================
# 任务 1：初识 requests.get()（对比 Java 的 HttpClient）
# 目标：发送 GET 请求，打印返回的 JSON 数据
# ==========================================
print("========== 任务 1：发送 GET 请求（测试接口） ==========")
# 使用免费测试 API（https://httpbin.org 专门用于测试）
test_url = "https://httpbin.org/get?name=Agent&age=1"

print(f"📤 正在请求：{test_url}")

# ---------- Python 方式（3行搞定） ----------
response = requests.get(test_url)  # 1. 发送请求（对应 Java 的 client.newCall().execute()）

# 2. 检查状态码（对应 Java 的 response.code()）
if response.status_code == 200:
    print("✅ 请求成功！状态码：200")
    
    # 3. 解析 JSON（对应 Java 的 new JSONObject(response.body().string())）
    data = response.json()  # requests 自带 .json() 方法，比 Java 的解析库方便太多。
    #再次反转成json格式，便于查看。分别是data，换行，转译中文
    print(f"📦 返回数据：{json.dumps(data, indent=2, ensure_ascii=False)}")
    
    # 提取我们发送的参数，看看服务器是否原样返回
    # data 是一个字典,args是字典中的键，data.get("args", {})是获取args的值，如果不存在则返回空字典
    arg = data.get("args", {})
    print(f"🔍 服务器回显的参数：name={arg.get('name')}, age={arg.get('age')}")
else:
    print(f"❌ 请求失败，状态码：{response.status_code}")

print("\n" + "="*50 + "\n")



# ==========================================
# 任务 2：调用真实天气 API（wttr.in）—— 无需 API Key
# 目标：输入城市名，获取当前温度
# ==========================================
print("========== 任务 2：查询天气（wttr.in 免费 API） ==========")

def fetch_weather(city: str):#工具名称city，参数str
    """
    根据城市名获取天气（使用 wttr.in）
    返回：字典 {"city": 城市, "temp": 温度, "desc": 天气描述} 或 None
    """
    # wttr.in 支持中文城市名，返回 JSON 格式（?format=j1 必须加）
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        # 设置超时时间 5 秒（防止卡死）
        resp = requests.get(url, timeout=5)
        
        # 如果状态码不是 200，抛出异常（对应 Java 的 resp.isSuccessful()）
        resp.raise_for_status()  # 这一步很关键！
        
        # 解析 JSON
        data = resp.json()
        
        # ---------- 解析 wttr.in 的嵌套结构（练练 Dict 取值） ----------
        # 当前温度在 current_condition[0].temp_C
        #等价
        #current_condition_list = data.get("current_condition", [{}])
        #current = current_condition_list[0]
        #temp_c = current.get("temp_C", "未知")
        current = data.get("current_condition", [{}])[0]
        temp_c = current.get("temp_C", "未知")
        
        # 天气描述（英文，示例："Sunny", "Cloudy"）
        desc = current.get("weatherDesc", [{"value": "未知"}])[0].get("value", "未知")
        
        # 地区名（从 nearest_area 取）
        area = data.get("nearest_area", [{}])[0].get("areaName", [{"value": city}])[0].get("value", city)
        
        return {
            "city": area,
            "temp": temp_c,
            "desc": desc
        }
        
    except requests.exceptions.Timeout:
        print("⏰ 请求超时（5秒），请检查网络或稍后重试。")
        return None
    except requests.exceptions.ConnectionError:
        print("🔌 网络连接失败，请检查是否联网。")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ HTTP 错误：{e}")
        return None
    except json.JSONDecodeError:
        print("❌ 返回的数据不是有效的 JSON，可能 API 接口有变动。")
        return None
    except Exception as e:
        print(f"💥 发生了未知错误：{type(e).__name__} - {e}")
        return None

# ---------- 测试任务 2 ----------
test_city = "Dalian"
print(f"🌤️ 正在查询 {test_city} 的天气...")
weather = fetch_weather(test_city)

if weather:
    print(f"✅ 查询成功！")
    print(f"📍 城市：{weather['city']}")
    print(f"🌡️ 温度：{weather['temp']}°C")
    print(f"☁️ 天气：{weather['desc']}")
else:
    print("❌ 天气查询失败，请检查输入或网络。")

print("\n" + "="*50 + "\n")


# ==========================================
# 🏆 终极挑战（Day 4 毕业设计）：交互式多城市天气查询器
# 整合 Day 1~3 所有知识点：
# 1. while 循环 + 最大次数限制（Day 2）
# 2. try-except 异常捕获（Day 3）
# 3. List 存储历史查询记录（Day 1）
# 4. f-string 格式化输出（Day 1）
# 5. 类型检查 + 防御性编程（Day 3）
# ==========================================
print("========== 🏆 终极挑战：交互式天气查询器 ==========")

# 存储查询历史（List of Dict）
history = []
max_queries = 5
query_count = 0

print(f"🌍 欢迎使用天气查询系统（最多查询 {max_queries} 个城市，输入 exit 退出）")

while query_count < max_queries:
    # 获取用户输入
    city_input = input(f"\n🏙️ 请输入城市名（剩余 {max_queries - query_count} 次机会）：").strip()
    
    # 1. 退出条件（Day 2 的 break）
    if city_input.lower() == "exit":
        print("👋 用户主动退出。")
        break
    
    # 2. 空输入过滤（Day 2 的 continue）
    if city_input == "":
        print("⚠️ 城市名不能为空，请重新输入（本轮不计数）")
        continue
    
    # 3. 消耗次数（Day 2 计数器）
    query_count += 1
    
    # 4. 调用 fetch_weather（内部已包含 Day 3 的异常捕获）
    print(f"⏳ 正在查询 {city_input} 的天气...")
    result = fetch_weather(city_input)
    
    if result:
        # 5. 将结果存入历史记录（Day 1 的 List 追加）
        result["query_city"] = city_input  # 额外保存用户输入的原名
        history.append(result)
        
        # 6. 使用 f-string 打印结果（Day 1）
        print(f"✅ 【{result['city']}】当前温度：{result['temp']}°C，{result['desc']}")
        print(f"📊 已成功查询 {len(history)} 个城市。")
    else:
        print(f"❌ 查询 {city_input} 失败，请检查城市名是否正确（支持拼音如 'Shanghai' 或中文）。")
    
    # 7. 如果达到最大次数，自动结束（循环条件会自动判断，这里加个友好提示）
    if query_count >= max_queries:
        print(f"\n⏰ 已达到最大查询次数（{max_queries} 次），自动结束。")

# ========== 最终展示：打印所有历史记录（Day 1 的遍历） ==========
print("\n" + "="*40)
print("📋 本次会话查询历史记录：")

if not history:
    print("（暂无有效查询记录）")
else:
    # 使用 enumerate 遍历（Day 1 知识点）
    for idx, record in enumerate(history, start=1):
        print(f"--- 记录 {idx}：城市【{record['city']}】，温度 {record['temp']}°C，{record['desc']} ---")
