# 场景：你要写一个程序，模拟 Agent 接收用户（或大模型）传来的 JSON 格式数据，将其解析并存入内存列表中。

# 功能要求（必须全部实现）：

# 初始化：创建一个空列表 profiles = [] 用于存储有效的用户档案。

# 循环控制：程序最多允许用户尝试 5 次（有效输入算一次，空输入不算）。

# 退出机制：用户输入 exit 可随时退出程序（不消耗次数）。

# 空输入过滤：如果用户直接按回车（空字符串），提示“输入为空，请重新输入”，并使用 continue 跳过本次（不消耗次数）。

# JSON 解析：使用 json.loads() 解析用户输入的字符串，捕获 JSONDecodeError 并给出友好提示。

# 类型校验（重点）：

# 检查解析后的数据必须是 字典（dict），否则提示“输入的不是有效的 JSON 对象”。

# 检查字典中是否包含 "name" 字段（字符串）和 "age" 字段（整数）。

# 如果缺少字段，提示缺少哪个字段。

# 如果 age 不是整数类型，提示“年龄必须是数字（整数）”。

# 存储与反馈：校验全部通过后，将整个字典 append 到 profiles 列表中，并用 f-string 打印成功信息及当前已存储的总条数（例如：✅ 已保存 {name}，年龄 {age}。当前共 {len(profiles)} 条记录。）。

# 结束展示：当循环结束（达到 5 次或因 exit 退出）时，用 for 循环遍历 profiles，按格式打印出所有已存储的档案（例如：--- 档案 1：姓名=张三，年龄=25 ---）。



print("========== 场景练习程序 ==========")
import json

profiles = []
max_attempts = 5
attempts = 0

while attempts < max_attempts:
    user_input = input(f"请输入用户档案（剩余 {max_attempts - attempts} 次），或输入exit退出：")
    
    if user_input == "exit":
        break
        
    if user_input.strip() == "":  # 顺便用 strip() 过滤空格，比 == "" 更健壮
        print("输入为空，请重新输入（本轮不计数）")
        continue
    
    # ========== 关键修改：只要是非空、非退出的输入，立即消耗次数 ==========
    attempts += 1
    
    try:
        user_data = json.loads(user_input)
    except json.JSONDecodeError:
        print("❌ 输入的不是有效的 JSON 对象")
        continue  # 继续下一次循环（但 attempts 已经+1了）
        
    if not isinstance(user_data, dict):
        print("❌ 输入的不是有效的 JSON 对象（解析后非字典）")
        continue
        
    if "name" not in user_data or "age" not in user_data:
        missing_fields = []
        if "name" not in user_data:
            missing_fields.append("name")
        if "age" not in user_data:
            missing_fields.append("age")
        print(f"❌ 缺少字段：{', '.join(missing_fields)}")
        continue
        
    if not isinstance(user_data["age"], int):
        print("❌ 年龄字段必须是整数")
        continue
        
    # 所有校验通过，存入数据
    profiles.append(user_data)
    print(f"✅ 已保存 {user_data['name']}，年龄 {user_data['age']}。当前共 {len(profiles)} 条记录。")

# 结束展示
print("\n========== 档案列表 ==========")
if not profiles:
    print("（暂无有效档案）")
else:
    for i, profile in enumerate(profiles):
        print(f"--- 档案 {i+1}：姓名={profile['name']}，年龄={profile['age']} ---")



















