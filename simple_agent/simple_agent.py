import json
import os
import re
from openai import OpenAI
from tools import TOOLS, build_system_prompt

# 1. 从配置文件加载设置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "setting.json"), "r", encoding="utf-8") as f:
    config = json.load(f)

client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])

# 2. 动态生成 system prompt
SYSTEM_PROMPT = build_system_prompt()

# 3. 交互循环
print("Agent 已启动，输入任务开始对话（输入 exit 或 quit 退出）\n")

while True:
    user_input = input(">>> ")
    if user_input.strip().lower() in ("exit", "quit"):
        print("已退出。")
        break
    if not user_input.strip():
        continue

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    for i in range(5):
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages
        )

        ai_text = response.choices[0].message.content
        print(f"\n=== Agent 输出 ===\n{ai_text}")

        messages.append({"role": "assistant", "content": ai_text})

        if "Final Answer:" in ai_text:
            print("--- 任务完成 ---\n")
            break

        action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", ai_text)
        if action_match:
            tool_name = action_match.group(1)
            args = [arg.strip() for arg in action_match.group(2).split(',')]

            if tool_name in TOOLS:
                print(f"[执行工具] {tool_name} 参数: {args}")
                observation = TOOLS[tool_name](*args)
            else:
                observation = f"错误：找不到工具 {tool_name}"

            print(f"[Observation] {observation}")
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            print("[错误] 未提取到标准 Action 格式，终止本轮。\n")
            break
