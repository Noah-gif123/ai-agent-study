# AI Agent 学习仓库

> 个人 AI Agent 技术学习记录，从零开始系统学习 Python → RAG → ReAct → LangGraph。

## 学习路线

| 阶段 | 内容 | 状态 |
|------|------|------|
| 01 | Python 基础练习 | 进行中 |
| 02 | RAG 完整项目（LangChain） | 待开始 |
| 03 | 手写 ReAct Agent | 待开始 |
| 04 | LangGraph 简历核心项目 | 待开始 |

## 目录结构

```
ai-agent-study/
├── 01_python_basic/        # Python 基础：API 调用、数据结构、文件读写、异常处理
├── 02_rag_project/         # RAG 完整项目
├── 03_handwritten_react/   # 手写 ReAct 推理循环
└── 04_langgraph_agent/     # LangGraph 核心项目（简历重点）
```

## 当前阶段：01 Python 基础

练习内容：
- 列表、字典操作
- 文件读取
- try-except 异常捕获
- requests 调用大模型 API
- python-dotenv 管理密钥（不硬编码）

## 运行前准备

1. 复制环境变量模板：`cp .env.example .env`
2. 在 `.env` 中填入你的 API 密钥

> 依赖安装：`pip install -r requirements.txt`

## 注意事项

- **切勿将 `.env` 文件提交到仓库**，已加入 `.gitignore`
- 每完成一个小练习就 commit 一次，保持提交记录连续
