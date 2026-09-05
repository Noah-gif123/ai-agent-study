#你接手了一个遗留系统的数据对接任务。对方只给了一个 API 地址，没有任何文档说明。
# 你必须自己通过发送请求、分析返回的 JSON 结构，从中提取出指定的业务字段。
#请求方式：GET
#接口地址（Endpoint）：https://api.zippopotam.am/us/10001
#注：这是一个查询美国纽约邮编 10001 对应地理信息的公开服务。
#你必须从这个接口返回的混乱数据中，精准提取出以下 4 个信息，并最终组装成一个干净的字典（变量名为 result）：
#邮政编码（对应原始键：post code）
#国家名称（对应原始键：country）
#州名全称（对应原始键：state）
#城市/地名（对应原始键：place name）

import json
import requests
from datetime import datetime

# 导入requests库用于发送HTTP请求
import requests
# 导入json库用于处理JSON数据
import json
# 发送GET请求获取指定邮编(10001)的数据
response = requests.get('https://api.zippopotam.us/us/10001')
# 将响应数据转换为JSON格式
data = response.json()
# 以格式化的方式打印原始JSON数据
print(json.dumps(data,indent=2,ensure_ascii=False))

# 从JSON数据中获取州名信息，如果找不到则返回"未知"
# 使用get方法安全地获取嵌套数据，避免KeyError异常
state = data.get("places", [{}])[0].get("state", "未知") 

# 从JSON数据中获取地名信息，如果找不到则返回"未知"
place_name = data.get("places", [{}])[0].get("place name", "未知") 

# 构建结果字典，包含提取的关键信息
result = {
    "邮政编码": data.get("post code"),
    "国家名称": data.get("country"),
    "州名全称": state,
    "城市/地名": place_name
}

# 将结果字典转换为格式化的JSON字符串
json_output = json.dumps(result, indent=2, ensure_ascii=False)
# 打印格式化的结果
print("\n📦 标准 JSON 格式输出：")
print(json_output)

