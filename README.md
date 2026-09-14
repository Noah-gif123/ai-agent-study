# AI Agent 学习仓库
> 个人 AI Agent 技术学习记录。
> 📌 整套学习采用**同一套N2日语语法知识库**贯穿全部项目：原生手搓RAG → LangChain重构RAG → 手写ReAct → LangGraph日语备考Agent，实现技术逐层迭代。

## 学习路线
| 阶段 | 内容 | 状态 |
|------|------|------|
| 01 | Python 基础练习（API调用、JSON、异常、dotenv、Token管理等） | ✅ 已完成 |
| 02 | N2‑Grammar‑Companion RAG项目<br>V0：手搓FAISS+重排序；V1：LangChain重构混合检索 | 🟡 进行中 |
| 03 | 手写原生 ReAct 智能体循环（不依赖LangGraph） | ⏳ 待开始 |
| 04 | LangGraph 日语备考Agent【简历核心项目】，复用02知识库，多工具扩展 | ⏳ 待开始 |

## 目录结构
```

ai-agent-study/
├── 01_python_basic/                # Python 基础练习：API 调用、数据结构、文件读写、异常处理、Token 压缩练习
├── 02_mini-native-rag-jp/          # N2 日语语法 RAG 项目
│   ├── v0_native_faiss/            # V0：纯手搓 RAG，FAISS 向量库 + Cross‑Encoder 重排序
│   └── v1_langchain_refactor/       # V1：LangChain 重构，混合检索 (BM25 + 语义)、多轮记忆、Gradio
├── 03_handwritten_react/           # 手写 ReAct 推理循环，原生 Python 实现 Thought‑Action‑Observation
└── 04_langgraph_jp_agent/          # LangGraph 简历核心项目：日语备考增强 Agent

```

### 版本简要说明
- **V0（手搓RAG）**：理解RAG底层原理；处理中文查询日文知识库跨语言召回问题；基于Recall@3做效果评估。
- **V1（LangChain重构）**：使用框架工程化实现，对比原生手写版本的优缺点；增加混合检索、流式输出、Web演示。
- **V2（LangGraph Agent）**：将RAG封装为Tool；扩展语法辨析、练习题生成、语法纠错多工具；实现意图澄清、上下文Token压缩、会话持久化。

## 当前阶段：02 N2‑Grammar‑Companion RAG项目
目标：搭建N2日语语法垂直知识库RAG助手
- 数据源：结构化JSON N2语法库（语法、释义、接续、例句、相似语法）
- 核心难点：**中文提问检索日语资料的跨语言召回**
- 评估方式：自建测试集，使用 Recall@3 衡量检索效果

## 运行前准备
1. 复制环境变量模板：`cp .env.example .env`
2. 在 `.env` 中填入 LLM / Embedding API 密钥
> 根目录统一依赖安装：`pip install -r requirements.txt`

## 注意事项
- **切勿将 `.env` 文件提交到仓库**，已加入 `.gitignore`
- 按模块小步提交commit，保持GitHub提交记录连续
- 每个子项目内部维护独立README，记录实现思路、踩坑点、项目局限与后续迭代计划
