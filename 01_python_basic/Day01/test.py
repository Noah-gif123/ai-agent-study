#print("========== 任务 1：List 和 Dict 基础 ==========")

# 创建一个空列表用于存储消息
messages = []   
# 向列表中添加第一条消息
messages.append("你好")
# 向列表中添加第二条消息
messages.append("世界")
# 打印存储所有消息的列表
print("当前列表内容：", messages)

# 在索引位置0处插入"中间"这个元素
messages.insert(0,"中间")
print("插入后：", messages)

# 移除列表中的最后一个元素   并存储到last_item变量中
last_item = messages.pop()
print("移除的最后一个元素：", last_item)
print("移除后列表：", messages)


messages[0] = "嗨" #  修改列表中第一个元素的值
print("修改后：", messages)


# 打印遍历结果的标题
print("遍历结果：")
# 遍历messages列表中的每条消息
for n in messages:
    # 为每条消息添加缩进和短横线前缀后打印
    print("  - " + n)

# 打印分隔线，由40个等号组成，前后各有一个换行符
print("\n" + "="*40 + "\n")



print("========== 任务 2：Dict 操作 ==========")
msg = {"role": "user", "content": "你好"} # 创建一个字典，存储一条消息

# 使用字典的键获取对应的值
role = msg["role"]
# 从消息字典中获取内容信息，如果不存在则使用默认值"默认内容"
content = msg.get("content", "默认内容") 
# 打印角色和内容信息，使用格式化字符串输出
print( f"角色：{role}，内容：{content}" )


# 为消息添加时间戳字段
msg["timestamp"] = "2026-09-03"  # 设置时间戳为2026年9月3日
# 打印添加时间戳后的消息内容
print("新增时间戳后：", msg)
# 打印角色、内容和时间戳的信息
# 使用f-string格式化输出字符串，包含三个变量：role、content和msg中的timestamp
print(f"角色：{role}，内容：{content}，时间戳：{msg['timestamp']}")

# 为消息内容赋值
msg["content"] = "明天天气"
print("修改内容后：", msg)
# 打印修改后的消息内容
print(f"角色：{role}，内容：{msg['content']}，时间戳：{msg['timestamp']}")


# 从字典中删除指定键的值，如果键不存在则返回默认值None
removed_value = msg.pop("timestamp", None) 
# 打印被删除的值和更新后的字典内容
print(f"删除了：{removed_value}，现在字典为：{msg}")
# 打印分隔线，用于视觉区分不同的输出部分
print("\n" + "="*40 + "\n")


print("========== 任务 3：F-string 格式化 ==========")

user_name = "小明"
user_input = "查一下气温"
time_now = "下午3点"

# 在字符串前面加 f，里面用 {变量名} 直接插值，支持换行符 \n
prompt = f"【用户信息】{user_name}\n【当前时间】{time_now}\n【用户问题】{user_input}\n请根据以上信息调用工具。"
print(prompt)

print("\n" + "="*40 + "\n")


print("========== 任务 4：多轮对话模拟（手动硬编码） ==========")
# 初始化系统消息（相当于 Agent 的系统提示词）
messages = [{"role": "system", "content": "我是一个智能助手"}]

# 模拟用户第一次提问
user_question = "我是张三，1+1等于几？"
# 1. 将用户问题包装成字典，追加到列表中（相当于 Java 的 add）
messages.append({"role": "user", "content": user_question})

# 2. 模拟 Agent 回复（这里我们用字符串切片和 f-string 强行做一次处理，练手）
# 提取用户名字：按"是"分割取后半段，再按"，"分割取第一个
user_name_extracted = user_question.split("是")[1].split("，")[0]
assistant_reply = f"你好 {user_name_extracted}，1+1 的答案是 2。"

# 3. 将助手回复追加进列表
messages.append({"role": "assistant", "content": assistant_reply})

# 4. 打印所有消息（带索引）
print("当前完整对话记录：")
for i, single_msg in enumerate(messages):  # enumerate 相当于带索引的 for 循环
    print(f"索引 {i}：角色 [{single_msg['role']}] 说：{single_msg['content']}")

print(f"\n当前对话共 {len(messages)} 条消息）")#相当于 messages.size()

print("\n" + "="*40 + "\n")



print("========== 终极挑战：命令行聊天机器人（输入 exit 退出） ==========")

# 重置消息列表
chat_messages = [{"role": "system", "content": "你是客服助手"}]

# 死循环（相当于 Java 的 while (true)）
while True:
    # 获取用户输入（相当于 Java 的 scanner.nextLine()）
    user_input = input("👤 用户说：")
    
    # 退出条件（相当于 if (user_input.equals("exit")) break;）
    if user_input == "exit":
        print("👋 已退出对话。")
        break  # 跳出循环
    
    # 将用户输入添加到历史记录
    chat_messages.append({"role": "user", "content": user_input})
    
    # 模拟助手自动回复（硬编码，不带 AI）
    assistant_reply = f"🤖 收到，您说的是：{user_input}，已记录。"
    chat_messages.append({"role": "assistant", "content": assistant_reply})
    
    # 打印当前总消息条数
    print(f"📊 当前对话共 {len(chat_messages)} 条消息")
    # 打印最后一条助手回复，让用户看到
    print(assistant_reply)
    print("-" * 30)  # 分隔线
