import random  # 相当于 Java 的 java.util.Random

# ==========================================
# 任务 1：基础计数器循环（替代 Java 的 for 循环）
# Java 写法：for (int step = 0; step < 5; step++) { ... }
# ==========================================
print("========== 任务 1：带计数器的 while 循环 ==========")
step = 0  # 相当于 int step = 0;
max_steps = 5  # 相当于 final int MAX_STEPS = 5;

# 注意！Python 没有 step++，必须写 step += 1（相当于 Java 的 step++）
while step < max_steps:
    print(f"当前步数：{step}（共最大 {max_steps} 步）")
    step += 1  # 千万不能忘！忘了就是死循环（相当于 Java 的 i++）
print("循环正常结束，步数已到达上限。\n")


# ==========================================
# 任务 2：猜数字游戏（模拟 Agent 在“找到答案”时提前 break）
# 场景：Agent 在 5 步内猜中数字，立即结束，不浪费剩余步数
# ==========================================
print("========== 任务 2：猜数字（找到答案立即 break） ==========")

# 生成一个 1 到 10 之间的随机数作为秘密数字
secret_number = random.randint(1, 10) 
# 设置最大猜测次数为 5
max_guesses = 5
# 初始化猜测次数和是否找到的标志
guess_count = 0
found = False
# 打印游戏规则提示信息
print(f"（系统已生成 1~10 的随机数，你有 {max_guesses} 次机会）")

# 开始游戏主循环，限制最大猜测次数
while guess_count < max_guesses:
    
    # Agent 生成一个1-10的随机猜测数字
    agent_guess = random.randint(1, 10)
    # 增加猜测计数
    guess_count += 1  
    
    # 打印当前猜测信息
    print(f"第 {guess_count} 次尝试：Agent 猜了 {agent_guess}")
    
    # 判断猜测是否正确
    if agent_guess == secret_number:
        # 如果猜中，打印成功信息并设置找到标志
        print(f"🎉 猜中了！数字就是 {secret_number}，Agent 在 {guess_count} 步内完成任务。")
        found = True
        # 退出循环
        break  
    else:
        # 如果猜错，提示继续尝试
        print("猜错了，继续尝试...")


# 检查是否用尽所有机会仍未猜中
if not found:
    # 打印游戏失败信息，显示正确答案
    print(f"😞 步数用尽，没能猜中。正确答案是 {secret_number}。")

# 打印游戏结束信息
print("猜数字游戏结束。\n")


# ==========================================
# 任务 3：continue 的用法（跳过脏数据/无效轮次）
# 场景：模拟 Agent 遇到格式错误的输入，不计数跳过（但为了演示，我们单独讲）
# ==========================================
print("========== 任务 3：continue 跳过无效数据 ==========")
# 模拟一个数据流，其中包含无效的 "skip" 项
data_stream = ["正常数据1", "skip", "正常数据2", "正常数据3", "skip", "skip"]
# 设置最大处理数量为5
max_process = 5
# 初始化步数数量为0
processed = 0
# 初始化数据流索引为0
index = 0
# 初始化变量all_process，用于存储所有进程的总数
all_process = 0;

# 循环处理数据，直到达到最大处理数量或数据流结束
while all_process < max_process and index < len(data_stream):
    # 获取当前索引的数据项
    item = data_stream[index]
    # 索引递增，准备处理下一条数据
    index += 1
    # 增加总进程计数
    all_process += 1;  # 将总进程数加1
    
    # 如果遇到"skip"项，打印提示信息并跳过本次处理
    if item == "skip":
        print(f"遇到 'skip'，跳过本次处理（不消耗步数）")
        continue  # 跳过下面代码，直接进入下一次循环
    
    # 正常处理逻辑
    processed += 1  # 只有正常数据才消耗步数
    print(f"处理第 {processed} 条数据：{item}")


print(f"循环一共执行 {all_process} 轮，成功处理 {processed} 条数据。")
# 打印最终处理结果统计信息


# ==========================================
# 🏆 终极挑战（Day 2 毕业设计）：带“最大轮次”的智能客服机器人
# 这是昨天聊天机器人的“安全加固版”
# 新增功能：
# 1. 限定最多对话 3 轮（防止无限聊下去）
# 2. 用户说 exit 立即退出（提前 break）
# 3. 用户输入空格时，提示并 continue（不消耗轮次）
# ==========================================
print("========== 终极挑战：限次智能客服（最大 3 轮） ==========")
# 初始化消息队列（Map) ，用于存储用户和客服的对话内容
chat_messages = [{"role": "system", "content": "你是客服助手，最多回答3轮"}]

# 设定最大迭代次数（在 Agent 中这就是保命索）
MAX_ROUNDS = 3
current_round = 0

while current_round < MAX_ROUNDS:
    # 获取用户输入
    user_input = input("👤 用户说：")
    
    # 情况 1：用户主动退出（提前终止）
    if user_input == "exit":
        print("👋 用户主动退出，结束会话。")
        break  # 跳出整个循环
    
    # 情况 2：用户输入空字符串或只有空格（模拟无效输入）
    if user_input.strip() == "":
        print("⚠️ 检测到空输入，请重新输入（本轮不计数）")
        continue  # 不消耗 current_round，直接进入下一轮输入
    
    # --- 正常处理逻辑（只有走到这里才消耗步数） ---
    current_round += 1  # 计数器加1（相当于 Java 的 round++）
    
    # 将用户消息加入历史
    chat_messages.append({"role": "user", "content": user_input})
    
    # 模拟 Agent 回复（硬编码）
    assistant_reply = f"🤖 第 {current_round} 轮回复：您说了 '{user_input}'，已记录。剩余 {MAX_ROUNDS - current_round} 轮机会。"
    chat_messages.append({"role": "assistant", "content": assistant_reply})
    
    # 打印状态
    print(assistant_reply)
    print(f"📊 当前总消息数：{len(chat_messages)}")
    print("-" * 40)

# 循环结束后的善后处理（类似于 Java 的 try-catch-finally 的 finally，或循环后的收尾）
if current_round >= MAX_ROUNDS:
    print("⏰ 已达到最大对话轮次（3轮），会话自动结束。")
elif user_input == "exit":
    print("✅ 会话已由用户正常终止。")