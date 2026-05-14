import os
import re
from openai import OpenAI  # 或者使用 google-genai 库

# 1. 真正的工具实现
def create_file(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    return "文件创建成功。"

def read_file(file_name):
    if not os.path.exists(file_name):
        return "错误：文件不存在。"
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()

# 工具映射字典，方便根据大模型的文本直接调用
tools = {
    "create_file": create_file,
    "read_file": read_file
    # delete_file 和 append_file 后面可以自行补充
}

# 2. 初始化大模型客户端 (保持 100% 本地或直接调用 API)
client = OpenAI(api_key="你的_API_KEY", base_url="你的_BASE_URL")

# 把你刚才测试成功的 Prompt 作为 System Prompt
SYSTEM_PROMPT = """你是一个文件管理 Agent。你拥有以下工具来操作文件：
1. read_file(file_name)
2. create_file(file_name, content)

你必须严格按照以下格式交替进行：
Thought: [思考过程]
Action: 工具名(参数1, 参数2)

等待用户给出 Observation 后继续。完成任务后输出：Final Answer: [结果]"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "帮我创建一个名为 todo.txt 的文件，里面写上‘买牛奶’，然后读取这个文件的内容确认是否写进去了。"}
]

# 3. 核心控制循环 (让 Agent 自己跑起来)
for i in range(5):  # 最多允许思考/行动 5 轮，防止死循环
    response = client.chat.completions.create(
        model="你的模型名称",
        messages=messages
    )
    
    ai_text = response.choices[0].message.content
    print(f"\n=== Agent 输出了 ===\n{ai_text}")
    
    # 将 AI 的发言记录到上下文中
    messages.append({"role": "assistant", "content": ai_text})
    
    # 检查是否完成
    if "Final Answer:" in ai_text:
        print("\n🎉 任务圆满完成！")
        break
        
    # 用正则表达式提取 Action: create_file(todo.txt, 买牛奶)
    action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", ai_text)
    if action_match:
        tool_name = action_match.group(1)
        # 简单切分参数（这里先做最粗暴的处理，后面可以用 json 规范化）
        args = [arg.strip() for arg in action_match.group(2).split(',')]
        
        if tool_name in tools:
            print(f"⚙️ 自动化系统：正在为您执行物理操作 {tool_name}，参数为 {args}...")
            # 执行物理操作
            observation = tools[tool_name](*args)
        else:
            observation = f"错误：找不到工具 {tool_name}"
            
        print(f"📝 得到反馈 (Observation): {observation}")
        # 把物理世界的结果当成 user 消息喂回给大模型
        messages.append({"role": "user", "content": f"Observation: {observation}"})
    else:
        print("⚠️ 未提取到标准 Action 格式，强制退出。")
        break