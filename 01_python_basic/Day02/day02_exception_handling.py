import json
import re
import requests
from datetime import datetime

# ==========================================
# 任务 1：捕获 KeyError（对应 Java 的 NullPointerException / 取不到 key）
# 场景：从大模型返回的字典中安全取值
# ==========================================
print("========== 任务 1：安全访问字典（KeyError 捕获） ==========")
# 模拟大模型返回的 JSON（但缺少了 tool_calls 字段）
model_output = {
    "content": "今天天气不错",
    "role": "assistant"
    # 故意没有 "tool_calls" 字段
}

# ---------- 错误示范（会崩溃） ----------
# 如果直接这样写，程序会报错终止：
# tool_calls = model_output["tool_calls"]  # KeyError!

# ---------- 正确示范 1：用 .get() 安全取值（最推荐） ----------
print("【方法一】使用 .get() 安全取值（类似 Java 的 getOrDefault）")
tool_calls = model_output.get("tool_calls", [])  # 取不到就返回空列表 []
print(f"通过 .get() 取到的 tool_calls：{tool_calls}")

# ---------- 正确示范 2：用 try-except 捕获（对应 Java 的 try-catch） ----------
print("\n【方法二】使用 try-except 显式捕获")
try:
    # 故意尝试访问不存在的键
    tool_calls = model_output["tool_calls"]
    print(f"取值成功：{tool_calls}")
except KeyError as e:
    # 相当于 Java 的 catch (KeyError e) { ... }
    print(f"捕获到 KeyError！错误信息：{e}")
    print("已经优雅处理，程序没有崩溃，我们可以在这里赋默认值或做其他操作。")
    tool_calls = []  # 兜底赋值

print(f"最终 tool_calls 值为：{tool_calls}\n")


# ==========================================
# 任务 2：捕获 JSONDecodeError（Agent 开发最最最常见的报错！）
# 场景：大模型返回了带 Markdown 标记的 JSON，或者返回了纯文本
# ==========================================
print("========== 任务 2：解析 JSON 并处理脏数据（JSONDecodeError） ==========")
# 模拟大模型常见的“不听话”返回（外面包了 Markdown 代码块）
raw_response = '```json\n{"city": "北京", "temperature": 25}\n```'

print(f"原始返回内容：\n{raw_response}")

# ---------- 第一步：暴力清洗（去掉 Markdown 反引号和换行） ----------
# 这就是为什么我们 Day 1 要学 strip 和 split！
cleaned = raw_response.strip('`').strip()  # 去掉首尾的反引号和多余空格
# 但万一模型返回的是 '```json'，我们用 replace 去掉 'json' 字样，或者用正则提取
# 更健壮的方法：用正则提取 {} 之间的内容（备胎技能）
json_match = re.search(r'\{.*?\}', raw_response, re.DOTALL)

if json_match:
    json_str = json_match.group()
    print(f"清洗后提取的 JSON 字符串：{json_str}")
else:
    json_str = cleaned  # 如果正则没匹配到，就用简单清洗的

# ---------- 第二步：用 try-except 尝试解析 ----------
try:
    # 尝试将字符串转为 Python 字典
    parsed_data = json.loads(json_str)
    print("✅ JSON 解析成功！")
    print(f"解析结果：{parsed_data}")
    print(f"城市：{parsed_data.get('city')}，温度：{parsed_data.get('temperature')}")
except json.JSONDecodeError as e:
    # 相当于 Java 的 catch (JsonParseException e)
    print(f"❌ JSON 解析失败！错误信息：{e}")
    print("模型可能返回了纯文本或格式错误的 JSON，我们需要在这里做兜底处理。")
    # 真实 Agent 场景：这里会记录日志，并提示模型重新生成
    parsed_data = {}  # 赋空字典防止后续报错

print("\n程序继续运行，没有因为 JSON 解析错误而崩溃。\n")


#==========================================
# 任务 3：捕获网络请求异常（requests.RequestException）
# 场景：调用大模型 API 时网络超时、断连、HTTP 错误
# ==========================================
print("========== 任务 3：模拟 HTTP 请求异常（捕获网络错误） ==========")

# 我们用一个不存在的 URL 来模拟超时/连接失败
test_url = "https://api.example.com/llm"  # 故意用不存在的地址

# 定义最大重试次数（结合我们 Day 2 学的循环控制！）
max_retries = 3
retry_count = 0
success = False

while retry_count < max_retries and not success:
    retry_count += 1
    print(f"\n第 {retry_count} 次尝试请求...")
    
    try:
        # 发起 GET 请求（设置超时 1 秒，必定超时触发异常）
        # 注意！这里会真的发起网络请求，但因为域名不存在会报错，我们故意捕获它
        # 真实开发中，这里换成 requests.post(url, json=data, timeout=30)
        response = requests.get(test_url, timeout=1)
        
        # 如果请求成功（状态码 200）
        response.raise_for_status()  # 如果状态码不是 200，会抛出 HTTPError（继承自 RequestException）
        print("✅ 请求成功！")
        success = True
        
    except requests.exceptions.Timeout as e:
        # 对应 Java 的 catch (SocketTimeoutException e)
        print(f"⏰ 请求超时：{e}")
        if retry_count >= max_retries:
            print("重试次数用尽，放弃请求。")
            
    except requests.exceptions.ConnectionError as e:
        # 对应 Java 的 catch (ConnectException e)
        print(f"🔌 连接错误（网络不通或域名不存在）：{e}")
        if retry_count >= max_retries:
            print("重试次数用尽，放弃请求。")
            
    except requests.exceptions.RequestException as e:
        # 这是所有 requests 异常的父类（相当于 Java 的 Exception 总基类）
        print(f"⚠️ 其他请求异常：{e}")
        if retry_count >= max_retries:
            print("重试次数用尽，放弃请求。")
    
    else:
        # Python 的 try-else：如果 try 块没有抛出任何异常，会执行这里的代码（对应 Java 里 try 块结束后的正常流程）
        print("✅ try 块执行成功，没有异常，进入 else 块。")
        # 这里可以放解析响应的逻辑
        
    finally:
        # 无论是否发生异常，都会执行（对应 Java 的 finally）
        # Agent 场景：在这里关闭文件、打印日志、记录耗时等
        print(f"📌 [finally] 第 {retry_count} 次尝试结束（无论成功失败都会打印）")

if not success:
    print("\n💀 最终所有重试均失败，请检查网络或 API 配置。")
else:
    print("\n🎉 请求成功，数据已获取。")

print("\n程序继续运行，网络异常已被妥善处理。\n")



# ==========================================
# 任务 4：try-except-else-finally 标准大综合（模拟 Agent 工作流）
# ==========================================
print("========== 任务 4：综合演练（模拟 Agent 工具调用） ==========")

def safe_tool_call(tool_name, params_str):
    """
    模拟一个安全的工具调用函数
    参数：
        tool_name: 工具名称（字符串）
        params_str: 参数的 JSON 字符串（可能是脏数据）
    返回：
        字典格式的执行结果
    """
    # 初始化一个默认的错误状态结果字典
    # 包含状态码和错误信息
    result = {"status": "error", "message": "未知错误"}
    
    try:
        # 1. 尝试解析参数
        print(f"🛠️ 调用工具：{tool_name}，原始参数：{params_str}")
        params = json.loads(params_str)# 如果 params_str 不是合法的 JSON 字符串，会抛出 json.JSONDecodeError
        
        # 2. 模拟执行业务逻辑（这里故意制造一个 KeyError 风险）
        city = params.get("city")  # 如果 city 不存在，后面会报错
        if city is None:
            # 手动抛出一个 ValueError 来演示捕获
            raise ValueError("参数中缺少 'city' 字段")
        
        # 3. 模拟正常业务（如果一切顺利）
        print(f"✅ 成功获取城市：{city}，正在查询天气...")
        result = {
            "status": "success",
            "data": f"{city} 的天气是晴天，温度 25 度"
        }
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        result["message"] = f"JSON 格式错误，请检查输入。错误详情：{e}"
        
    except ValueError as e:
        print(f"❌ 参数校验失败：{e}")
        result["message"] = str(e)
        
    except Exception as e:
        # 捕获所有其他未知异常（相当于 Java 的 catch (Exception e)）
        print(f"❌ 发生了未知异常：{type(e).__name__} - {e}")
        result["message"] = f"系统内部错误，请联系管理员。"
        
    else:
        # 如果 try 块没有异常，执行这里
        print("✅ 工具执行成功，没有异常发生。")
        
    finally:
        # 无论成败，都打印一条日志（模拟 Agent 的审计日志）
        print(f"📝 [审计日志] 工具 {tool_name} 执行完毕，状态：{result['status']}\n")
    
    return result

# ---------- 测试这个安全函数 ----------
print("【测试 1】传入正确的 JSON")
safe_tool_call("get_weather", '{"city": "上海"}')

print("【测试 2】传入格式错误的 JSON（缺少引号）")
safe_tool_call("get_weather", '{city: "上海"}')  # 会触发 JSONDecodeError

print("【测试 3】传入缺少必要字段的 JSON（缺少 city）")
safe_tool_call("get_weather", '{"country": "中国"}')  # 会触发 ValueError

print("【测试 4】传入 None（极端情况）")
safe_tool_call("get_weather", None)  # 会触发 TypeError，会被 Exception 兜底捕获



# ==========================================
# 🏆 终极挑战（Day 3 毕业设计）：带异常处理的智能解析器
# 要求：写一个循环，让用户输入 JSON 字符串，程序尝试解析，直到用户输入 exit
# 必须捕获 JSONDecodeError 和 KeyError
# ==========================================
# ==========================================
# 🏆 终极挑战（Day 3 完整版）：带异常处理和类型检查的解析器
# ==========================================
print("\n" + "="*50)
print("🏆 终极挑战：交互式 JSON 安全解析器（最大 5 次尝试）")
print("规则：输入 JSON，程序会解析并提取 'name' 字段")
print("输入 exit 退出，空输入不计次数。")
print("="*50)

max_attempts = 5
attempt = 0

while attempt < max_attempts:
    remaining = max_attempts - attempt
    user_input = input(f"\n📥 请输入 JSON（剩余 {remaining} 次机会，输入 exit 退出）：")
    
    if user_input.lower() == "exit":
        print("👋 已退出解析器。")
        break
    
    if user_input.strip() == "":
        print("⚠️ 输入为空，请重新输入（本轮不计数）")
        continue
    
    attempt += 1  # 有效输入，消耗次数
    
    try:
        data = json.loads(user_input)
        print("✅ JSON 格式正确！")
        
        # ---------- 关键检查：data 必须是字典 ----------
        if not isinstance(data, dict):
            print(f"⚠️ 输入的不是对象（dict），而是 {type(data).__name__}，无法提取 name 字段。")
            # 这里不 break，继续让用户尝试
        else:
            # 安全提取 name
            name = data.get("name")  # 不存在返回 None
            if name is not None:
                print(f"✅ 成功提取 name 字段：{name}")
                print(f"🎉 在第 {attempt} 次尝试成功！")
                break  # 成功后退出循环
            else:
                print("⚠️ JSON 中缺少 'name' 字段。")
                
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        print("💡 提示：JSON 需要双引号，例如 {\"name\": \"张三\"}")
    
    # 如果达到最大次数
    if attempt >= max_attempts:
        print(f"\n⏰ 已达到最大尝试次数（{max_attempts} 次），程序自动结束。")

print("\n🏁 解析器已退出。")