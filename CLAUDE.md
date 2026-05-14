# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在此仓库中工作时提供指导。

## 项目概述

一个最简的 ReAct（推理+行动）智能体原型。智能体通过 LLM（兼容 OpenAI 的 API）以文本解析的方式执行文件操作。启动后进入交互模式，持续等待用户输入并执行任务。

所有 agent 相关代码和运行时文件均在 `simple_agent/` 目录下，与开发文件隔离。

## 常用命令

```bash
pip install openai
cd simple_agent
python simple_agent.py
```

没有构建、代码检查或测试基础设施。

## 架构

```
simple_agent/
  simple_agent.py        # 入口：交互循环 + ReAct 控制循环
  setting.json           # API 配置（gitignore）
  tools/
    __init__.py          # 工具注册表 + build_system_prompt()
    file_tools.py        # create_file(), read_file()
  workspace/             # agent 文件操作的工作目录（gitignore）
```

### 核心流程

1. 启动时从 `setting.json` 加载 `api_key`、`base_url`、`model`
2. `tools/__init__.py` 的 `build_system_prompt()` 根据 `TOOL_REGISTRY` 动态生成 system prompt
3. `while True` 等待用户输入（`exit` / `quit` 退出）
4. 每轮用户输入启动独立的 ReAct 会话（最多 5 轮）：
   - LLM 返回 `Thought:` / `Action:` 文本
   - 正则提取工具调用 → `TOOLS` 字典分发执行
   - 结果作为 `Observation:` 反馈给 LLM
   - 检测到 `Final Answer:` 后结束本轮
5. 所有工具的文件操作限定在 `workspace/` 目录内

### 添加新工具

1. 在 `simple_agent/tools/` 下新建文件，实现工具函数
2. 在 `tools/__init__.py` 中 import 并注册到 `TOOL_REGISTRY`
3. system prompt 会自动包含新工具

## 配置

- `simple_agent/setting.json` — LLM 连接配置，已加入 gitignore：
  - `api_key`: API 密钥
  - `base_url`: API 端点地址
  - `model`: 模型名称
