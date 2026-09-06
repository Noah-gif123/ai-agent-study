import json
import requests
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

# ==========================================
# 0. 准备工作：模拟真实 Agent 场景
# ==========================================
print("="*50)
print("🚀 Day 04：Pydantic 数据校验实战")
print("场景模拟：大模型（LLM）要调用你的工具，我们校验它传的参数。\n")

# ==========================================
# 任务 1：定义工具参数模型（像 Java 的 DTO + 校验注解）
# 模拟场景：大模型要调用 "get_weather" 工具，需要两个参数：
#   - city: 字符串（必须填写）
#   - days: 整数（1~7 天，默认 1）
#   - unit: 字符串（可选，默认 "celsius"）
# ==========================================
print("========== 任务 1：定义 Pydantic 模型 ==========")
#**Pydantic 数据模型类**，专门用来做参数校验、解析，常用于 AI Agent 工具调用、接口请求体解析
#继承自 BaseModel，使用 Field 来定义字段属性和校验规则
class WeatherParams(BaseModel):
    """天气查询参数模型"""
    city: str = Field(..., description="城市名，必须填写")  # ... 表示必填
    days: int = Field(default=1, ge=1, le=7, description="查询天数，1~7天")  # 默认1，限制1-7
    unit: Optional[str] = Field(default="celsius", description="温度单位，默认摄氏度")

    # 你可以加上自定义校验器，这里暂不展开，防止增加复杂度

print("✅ 模型定义完成！")
print("   - city: str (必填)")
print("   - days: int (默认1，范围1~7)")
print("   - unit: str (可选，默认 celsius)")


# ==========================================
# 任务 2：正常数据（模型校验通过）
# ==========================================
print("\n========== 任务 2：测试正常数据 ==========")

# 模拟大模型传过来的参数（JSON 格式）
llm_input_good = '{"city": "Shanghai", "days": 2, "unit": "celsius"}'

try:
    # 1. 先将 JSON 转为字典
    raw_data = json.loads(llm_input_good)
    
    # 2. 用 Pydantic 模型校验（这一步会自动检查类型、范围、必填）
    params = WeatherParams(**raw_data)  # ** 解包字典，相当于 Java 的构造器传参
    
    print(f"✅ 校验通过！解析后的参数：")
    print(f"   → 城市：{params.city}")
    print(f"   → 天数：{params.days}")
    print(f"   → 单位：{params.unit}")
    
    # 模拟调用工具函数
    print(f"   🔧 正在查询 {params.city} 未来 {params.days} 天的天气...")
    
except json.JSONDecodeError:
    print("❌ 传入的不是合法的 JSON 格式")
except ValidationError as e:
    # 如果参数校验失败，会抛出 ValidationError（类似 Java 的 ConstraintViolationException）
    print(f"❌ 数据校验失败：{e}")
except Exception as e:
    print(f"💥 未知错误：{e}")


# ==========================================
# 任务 3：脏数据（模型校验拦截）
# 场景 1：缺少必填字段 city
# ==========================================
print("\n========== 任务 3.1：测试脏数据（缺少必填字段） ==========")

llm_input_missing = '{"days": 2}'  # 故意不传 city

try:
    raw_data = json.loads(llm_input_missing)
    params = WeatherParams(**raw_data)
    print("✅ 校验通过（这不合理，说明模型没拦住！）")
except ValidationError as e:
    print("❌ 校验拦截成功！错误详情：")
    # 优雅地打印错误信息（展开字段）
    for error in e.errors():
        print(f"   → 字段 '{'.'.join(error['loc'])}'：{error['msg']}")


# ==========================================
# 任务 4：脏数据（模型校验拦截）
# 场景 2：days 超出范围（传了 10 天）
# ==========================================
print("\n========== 任务 3.2：测试脏数据（days 超出范围） ==========")

llm_input_out_of_range = '{"city": "Beijing", "days": 10}'

try:
    raw_data = json.loads(llm_input_out_of_range)
    params = WeatherParams(**raw_data)
    print("✅ 校验通过（这不合理！）")
except ValidationError as e:
    print("❌ 校验拦截成功！错误详情：")
    for error in e.errors():
        print(f"   → 字段 '{'.'.join(error['loc'])}'：{error['msg']}")       

# ==========================================
# 任务 5：脏数据（模型校验拦截）
# 场景 3：days 传了字符串（类型错误）
# ==========================================
print("\n========== 任务 3.3：测试脏数据（类型错误） ==========")

llm_input_wrong_type = '{"city": "Shanghai", "days": "three"}'  # "three" 不是整数

try:
    raw_data = json.loads(llm_input_wrong_type)
    params = WeatherParams(**raw_data)
    print("✅ 校验通过（不可能！）")
except ValidationError as e:
    print("❌ 校验拦截成功！错误详情：")
    for error in e.errors():
        print(f"   → 字段 '{'.'.join(error['loc'])}'：{error['msg']}")


# ==========================================
# 🏆 终极挑战（Day 06 毕业设计）：模拟 Agent 工具调用系统
# 综合运用：JSON 解析 + Pydantic 校验 + 真实 API 调用 + 历史记录
# ==========================================
print("\n" + "="*50)
print("🏆 终极挑战：带校验的 Agent 工具调用系统")
print("规则：输入一个 JSON 格式的参数字符串，程序会校验并调用模拟工具")
print("输入 exit 退出。")
print("示例正确输入：{\"city\": \"Beijing\", \"days\": 3}")

# 再定义一个更复杂的模型，用于本次挑战（包含可选字段）
class QueryParams(BaseModel):
    city: str = Field(..., description="城市名")
    days: int = Field(default=1, ge=1, le=3, description="天数 1~3")
    # 新增一个可选字段：aqi（空气质量指数，布尔值，默认 False）
    aqi: bool = Field(default=False, description="是否查询空气质量")

# 模拟一个真实的天气查询函数（带校验）
def call_weather_api(params: QueryParams):
    """校验通过后执行的真实函数，支持查询1~3天（含今天）"""
    # 根据天数生成友好的提示语
    if params.days == 1:
        print(f"\n⏳ 正在查询 {params.city} 今天的天气...")
    else:
        print(f"\n⏳ 正在查询 {params.city} 今天及未来 {params.days - 1} 天的天气...")
    
    # wttr.in 的 days 参数表示包括今天在内的总天数
    url = f"https://wttr.in/{params.city}?format=j1&days={params.days}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            print(f"⚠️ API 返回状态码：{resp.status_code}，请检查城市名。")
            return None
        
        data = resp.json()
        weather_list = data.get("weather", [])
        
        # 实际可用天数（API 可能返回少于请求的天数）
        actual_days = min(len(weather_list), params.days)
        if actual_days == 0:
            print("❌ 未获取到任何天气数据。")
            return None
        
        daily_summaries = []
        for i in range(actual_days):
            day_data = weather_list[i]
            date = day_data.get("date", f"第{i+1}天")
            temp_max = day_data.get("maxtempC", "?")
            temp_min = day_data.get("mintempC", "?")
            desc = day_data.get("hourly", [{}])[0].get("weatherDesc", [{"value": "未知"}])[0]["value"]
            
            # 根据索引确定前缀
            if i == 0:
                prefix = "今天"
            elif i == 1:
                prefix = "明天"
            else:
                prefix = f"后天（{date}）"
            
            daily_summaries.append(f"{prefix}：{temp_min}~{temp_max}°C，{desc}")
        
        # 构造最终输出摘要
        if actual_days == 1:
            title = f"📅 {params.city} 今天天气："
        else:
            title = f"📅 {params.city} 今明 {actual_days} 天天气："
        full_weather_text = title + "\n" + "\n".join(daily_summaries)
        print(f"✅ 查询成功！\n{full_weather_text}")
        
        return {
            "city": params.city,
            "days": actual_days,
            "summary": full_weather_text,
            "details": daily_summaries
        }
        
    except requests.exceptions.Timeout:
        print("⏰ 请求超时，请稍后重试。")
        return None
    except requests.exceptions.ConnectionError:
        print("🔌 网络连接失败，请检查网络。")
        return None
    except Exception as e:
        print(f"❌ 请求异常：{e}")
        return None
# ---------- 主循环 ----------
history = []
while True:
    user_input = input("\n📥 请输入工具参数 JSON（或 exit 退出）：").strip()
    
    if user_input.lower() == "exit":
        print("👋 退出程序。")
        break
    
    if user_input == "":
        print("⚠️ 输入为空，请重新输入。")
        continue
    
    # 1. 尝试解析 JSON
    try:
        raw_data = json.loads(user_input)
    except json.JSONDecodeError:
        print("❌ 不是有效的 JSON 格式，请检查引号和括号。")
        continue
    
    # 2. 用 Pydantic 校验参数
    try:
        # 这一步是关键！如果 raw_data 缺少 city，或者 days 超出范围，会抛出 ValidationError
        params = QueryParams(**raw_data)
        print("✅ 参数校验通过！")
        print(f"   → 城市：{params.city}，天数：{params.days}，AQI：{params.aqi}")
        
        # 3. 调用真实函数（只有校验通过才会执行到这里）
        result = call_weather_api(params)
        
        if result:
            # 4. 存储历史记录（复用 Day 05 的知识）
            history.append(result)
            print(f"📊 已成功查询 {len(history)} 个城市。")
            
        else:
            print("⚠️ 查询失败，请检查城市名。")
            
    except ValidationError as e:
        print("❌ 参数校验失败！请检查以下字段：")
        for error in e.errors():
            # 提取报错字段和原因
            field = '.'.join(error['loc'])
            msg = error['msg']
            print(f"   → {field}：{msg}")
    except Exception as e:
        print(f"💥 发生了未知错误：{type(e).__name__} - {e}")

# ---------- 展示历史 ----------
print("\n" + "="*40)
print("📋 本次会话查询历史：")
if history:
    for idx, item in enumerate(history, start=1):
        print(f"--- {idx}. {item['city']}：{item['temp']}°C，{item['desc']} ---")
else:
    print("（暂无查询记录）")