from .file_tools import create_file, read_file

# 工具注册表：(名称, 函数, 描述)
TOOL_REGISTRY = [
    ("create_file", create_file, "create_file(file_name, content) — 创建文件并写入内容"),
    ("read_file", read_file, "read_file(file_name) — 读取文件内容"),
]

# 方便按名称调用的字典
TOOLS = {name: fn for name, fn, _ in TOOL_REGISTRY}


def build_system_prompt():
    tool_descriptions = "\n".join(f"{i+1}. {desc}" for i, (_, _, desc) in enumerate(TOOL_REGISTRY))
    return f"""你是一个文件管理 Agent。你拥有以下工具来操作文件：
{tool_descriptions}

你必须严格按照以下格式交替进行：
Thought: [思考过程]
Action: 工具名(参数1, 参数2)

等待用户给出 Observation 后继续。完成任务后输出：Final Answer: [结果]"""
