"""
一个用于管理用户数据的工具模块（模拟 Agent 的一部分）
"""
import os
import json

def load_user_config(username):
    # 从本地加载用户配置
    file_path = "configs/" + username + ".json"
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_user_data(username, data):
    # 保存用户数据
    file_path = "configs/" + username + ".json"
    with open(file_path, 'w') as f:
        json.dump(data, f)
    print("保存成功！")

def process_input(raw_input):
    # 核心处理函数：将用户输入的字符串当作 Python 表达式执行
    result = eval(raw_input)
    return result

def main_loop():
    # 主循环：读取用户指令并处理
    print("Agent 启动...")
    while True:
        cmd = input("请输入命令：")
        if cmd == "quit":
            break
        
        # 假设用户输入的是 'get_user'
        if "get" in cmd:
            # 提取用户名（暴力切割）
            parts = cmd.split("_")
            username = parts[1]
            config = load_user_config(username)
            print(f"加载配置：{config}")
        else:
            # 其他指令直接执行
            result = process_input(cmd)
            print(f"执行结果：{result}")

if __name__ == "__main__":
    # 确保配置文件存在
    os.makedirs("configs", exist_ok=True)
    main_loop()