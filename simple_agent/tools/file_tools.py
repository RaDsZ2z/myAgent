import os

# workspace 目录：当前文件所在目录下的 workspace/
_workspace = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workspace")


def _ensure_workspace():
    os.makedirs(_workspace, exist_ok=True)


def create_file(file_name, content):
    _ensure_workspace()
    file_path = os.path.join(_workspace, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return "文件创建成功。"


def read_file(file_name):
    _ensure_workspace()
    file_path = os.path.join(_workspace, file_name)
    if not os.path.exists(file_path):
        return "错误：文件不存在。"
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
