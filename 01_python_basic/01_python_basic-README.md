# 🐍 01_python_basic —— Python 基础 + 手写 ReAct Agent

> 整个 AI Agent 学习路线的**地基**：从零系统学习 Python，用 8 天时间手写一个**不依赖 LangChain** 的 ReAct Agent，并完成工程化分层。

| 项目 | 说明 |
| :--- | :--- |
| 代码规模 | **37 个 `.py` 文件 / 约 4000 行 Python**（Day01~Day07 共 21 个练习脚本 + Day08_project 16 个模块文件） |
| 运行环境 | Python **3.10+**（本机实测 3.14.4） |
| 外部依赖 | DeepSeek API + 3 个免费公开 API（天气 / 邮编 / httpbin） |
| 核心产出 | ReAct Agent 主循环 + Function Calling + 脏数据防御 + 工程化分层项目 |

---

## 📌 这个阶段在干什么

用「**硬编码跑通 → 动态化替换 → 异常兜底**」三步迭代法推进，8 天完成一条完整的成长线：

```
Day01 数据结构/F-string ──► Day02 循环控制 + 异常处理 ──► Day03 网络请求 + 文件/环境变量
                                                                    │
Day07 脏数据防御 ◄── Day06 日志监控 + 对话压缩 ◄── Day05 Function Calling ◄── Day04 Pydantic + ReAct 主循环（模拟）
        │
        └──► Day08 项目工程化（config / core / tools / utils / prompts 分层）
```

一句话总结这段学习的信条（写在学习手册里）：

> **写 Agent 不是比谁代码优雅，而是比谁容错性强。**

---

## 📅 每日内容与产出

| Day | 主题 | 主要文件 | 关键知识点 |
| :---: | :--- | :--- | :--- |
| **01** | 数据结构基础 | `test.py`、`generate_manual.py` | `list`/`dict` 增删改查、`f-string`、`enumerate`、用 `messages = [{"role":...}]` 模拟对话消息队列 |
| **02** | 循环控制 + 异常处理 | `day02_loop_control.py`、`day02_exception_handling.py`、`summary_exercise.py` | `while`/`break`/`continue`、最大迭代次数防死循环、`try-except-else-finally`、三大异常捕获、请求重试 |
| **03** | 网络请求 + 文件/环境变量 | `day03_http_request.py`、`day03_file_env.py`、`day03_explore_mission.py` | `requests.get` + `timeout` + `raise_for_status`、`with open`、`json.dump/load`、`python-dotenv`、历史记录持久化、嵌套 `.get()` 防御取值 |
| **04** | 数据校验 + ReAct 主循环 | `day04_pydantic.py`、`day04_agent_loop.py`、`ultimate_agent.py` | Pydantic `BaseModel`/`Field` 约束、`ValidationError` 格式化、**工具注册表**、Thought/Action/Observation 闭环（模拟 LLM） |
| **04-01** | 代码审查与重构练习 | `review_practice.py`、`review_practice_fixed.py` | 对照修复：移除 `eval` 注入、`os.path.join` 替代路径硬拼、补异常捕获、正则替代 `split` 越界 |
| **05** | Function Calling | `day05_function_calling.py`、`day05_practice.py`、`day05_real_llm.py` | 原生 `tool_calls` / `tool_call_id` 完整闭环、`tool_choice: auto`、**规则模式 vs LLM 模式双实现**、接入真实 LLM 的 ReAct |
| **06** | 日志监控 + 对话压缩 | `day06_logging_monitor.py`、`day06_context_compression.py`、`day06_world_record.py` | `logging` 双通道（控制台 INFO / 文件 DEBUG）、耗时与 Token 阈值预警、**上下文压缩**（旧对话摘要注入 system） |
| **06-01** | 练习：股票行情助手 | `stock simulation.py` | 规则匹配 mock LLM + 真实 API 摘要压缩、名称→代码映射、会话历史持久化 |
| **07** | 脏数据终极防御 | `day07_dirty_data_defense.py` | **5 层 `safe_json_loads`** 清洗、解析失败自动重试、自带单元测试、降级回复 |
| **08** | 项目工程化 | `Day08_project/`（config / core / tools / utils / prompts） | 目录分层、模块导入、配置集中管理、路径基于 `__file__`、统一 logger |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r Day08_project/requirements.txt
```

依赖清单：`requests`、`python-dotenv`、`pydantic`、`tiktoken`（`Day01/generate_manual.py` 额外需要 `python-docx`）。

### 2. 配置 API 密钥

在 `01_python_basic/` 下创建 `.env`（**当前仓库里还没有这个文件**）：

```ini
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

> `Day01` ~ `Day04` 不需要密钥；`Day05`、`Day06`、`Day06-01`、`Day07`、`Day08_project` 必须配置。

### 3. 运行工程化项目（推荐入口）

```bash
cd Day08_project
python main.py
```

### 4. 运行单日练习脚本

⚠️ **必须在 `01_python_basic/` 目录下运行**（除 `Day03/day03_file_env.py` 与 `Day08_project` 用 `__file__` 定位路径外，其余脚本的 `logs/`、`output/`、`configs/`、`agent_workspace/` 都是**相对当前工作目录**的）。

```bash
cd 01_python_basic
python Day04/day04_agent_loop.py      # 模拟 ReAct 主循环
python Day05/day05_real_llm.py        # 接入真实 DeepSeek 的 ReAct
python Day07/day07_dirty_data_defense.py   # 先跑单元测试，再进入交互
```

交互式脚本统一约定：命令行输入，**输入 `exit` 退出**，多数脚本有最大轮次限制（3~5 轮）。

---

## 🔑 环境变量

| 变量名 | 必需 | 使用位置 | 说明 |
| :--- | :---: | :--- | :--- |
| `DEEPSEEK_API_KEY` | ✅ | Day05 / Day06 / Day06-01 / Day07 / Day08_project | DeepSeek 大模型密钥 |
| `BASE_URL` | ⭕ | `Day03/day03_file_env.py` | 邮编 API 基地址，默认 `https://api.zippopotam.us` |
| `WORK_DIR` | ⭕ | `Day04/ultimate_agent.py` | 文件归档助手的工作目录，默认 `./agent_workspace` |

> 密钥一律通过 `os.getenv()` 读取，**严禁硬编码**；`.env` 已加入 `.gitignore`。

---

## 🛠️ 技术栈

| 类别 | 内容 |
| :--- | :--- |
| **第三方库** | `requests`（HTTP）、`python-dotenv`（环境变量）、`pydantic`（入参校验）、`tiktoken`（Token 计数）、`python-docx`（生成学习手册） |
| **标准库** | `json`、`re`、`os`、`time`、`logging`、`datetime`、`ast`、`random`、`typing` |
| **外部 API** | **DeepSeek**（`api.deepseek.com/v1/chat/completions`，`deepseek-chat`）、**wttr.in**（免费天气，无需 Key）、**zippopotam.us**（邮编地理信息）、**httpbin.org**（请求测试） |

---

## 📂 目录结构

```
01_python_basic/
├── 01_python_basic-README.md        # 本文件
├── AI-Agent_Python学习手册.docx      # 由 Day01/generate_manual.py 程序化生成
│
├── Day01/                           # 数据结构基础
│   ├── test.py                      # List/Dict/f-string + 命令行聊天机器人
│   └── generate_manual.py           # 用 python-docx 生成学习手册
├── Day02/                           # 循环控制 + 异常处理
│   ├── day02_loop_control.py        # while/break/continue、限次智能客服
│   ├── day02_exception_handling.py  # safe_tool_call、重试、脏数据清洗
│   └── summary_exercise.py          # JSON 解析 → 校验 → 存储 综合演练
├── Day03/                           # 网络请求 + 文件/环境变量
│   ├── day03_http_request.py        # requests + wttr.in 天气查询器
│   ├── day03_file_env.py            # 文件读写 + dotenv + 历史记录持久化
│   └── day03_explore_mission.py     # 无文档接口的数据提取任务
├── Day04/                           # 数据校验 + ReAct 雏形
│   ├── day04_pydantic.py            # Pydantic 工具入参校验实战
│   ├── day04_agent_loop.py          # ReAct 主循环（模拟 LLM）
│   └── ultimate_agent.py            # 智能文件归档助手（3 个工具 + 历史持久化）
├── Day04-01练习/                     # 代码审查练习（坏味道 → 重构）
│   ├── review_practice.py           # 反面教材：eval 注入、路径硬拼、无异常处理
│   └── review_practice_fixed.py     # 修复版：逐条对照
├── Day05/                           # Function Calling
│   ├── day05_function_calling.py    # 原生 tool_calls 闭环（含填空 TODO）
│   ├── day05_practice.py            # 规则模式 vs LLM 模式双实现
│   └── day05_real_llm.py            # 接入真实 LLM 的 ReAct Agent
├── Day06/                           # 日志监控 + 对话压缩
│   ├── day06_logging_monitor.py     # logging 双通道 + Token 预警
│   ├── day06_context_compression.py # 上下文压缩（摘要注入 system）
│   └── day06_world_record.py        # 世界之最查询器（结果持久化）
├── Day06-01练习/                     # 练习：智能股票行情助手
│   └── stock simulation.py
├── Day07/                           # 脏数据终极防御
│   └── day07_dirty_data_defense.py  # 5 层清洗 + 自动重试 + 单元测试
├── Day08_project/                   # ⭐ 工程化重构产物
│   ├── main.py                      # 入口
│   ├── requirements.txt
│   ├── .gitignore
│   ├── config/settings.py           # 集中配置：API / 路径 / Agent 行为常量
│   ├── core/
│   │   ├── agent.py                 # ReAct 主循环
│   │   ├── llm_client.py            # LLM 调用封装（含自动重试）
│   │   └── memory.py                # 对话压缩
│   ├── tools/
│   │   ├── registry.py              # 工具注册表 + 统一执行与参数校验
│   │   ├── time_tool.py             # get_time
│   │   └── weather_tool.py          # get_weather
│   ├── prompts/templates.py         # System Prompt 集中管理
│   ├── utils/
│   │   ├── json_cleaner.py          # safe_json_loads（5 层清洗）
│   │   └── logger.py                # 统一 logger
│   ├── logs/                        # 运行日志（不入库）
│   └── output/history.json          # 对话历史（不入库）
│
├── agent_workspace/                 # ultimate_agent 的工作目录（WORK_DIR）
├── configs/zhangsan.json            # Day04-01 练习的用户配置样例
├── logs/                            # Day06/Day07 脚本日志（不入库）
└── output/                          # 脚本运行产物
    ├── archive_history.json         # 文件归档助手的对话历史
    ├── stock_history.json           # 股票助手的对话历史
    └── world_records.txt            # 世界之最查询结果（追加写入）
```

---

## ✨ 这段学习沉淀下来的 8 个可复用能力

1. **工具注册表模式** —— `TOOLS = {"get_weather": {"func":..., "params_model":...}}`，一次注册，主循环统一调度，新增工具不改核心逻辑。
2. **脏数据 5 层清洗** —— `safe_json_loads()`：直接解析 → 去 Markdown 代码块 → 正则提 `{...}` → 首尾花括号截取 → `ast.literal_eval` 兜底，配 7 条单元测试。
3. **失败自动重试** —— 网络请求与 JSON 解析失败均自动重试（`max_retries=3`），最终降级为友好回复而非崩溃。
4. **上下文压缩** —— 超 Token 阈值时，把旧对话交给 LLM 生成摘要并注入 system prompt，只保留最近 N 条，附带压缩前后 Token 对比。
5. **日志双通道 + 监控** —— 控制台 INFO、文件 DEBUG，格式含 `%(filename)s:%(lineno)d`；每轮打印 Token 消耗与耗时。
6. **会话持久化与记忆恢复** —— `history.json` / `archive_history.json` / `world_records.txt`，重启后可恢复上下文。
7. **入参强校验** —— Pydantic `Field(..., ge=, le=)` 拦住模型传来的脏参数，`ValidationError` 逐字段格式化返回。
8. **安全加固** —— 练习中主动对比移除 `eval` 注入、用 `os.path.join` 替代路径硬拼、用正则替代 `split("_")[1]` 越界。

---

## ⚠️ 已知注意事项

| 项 | 说明 |
| :--- | :--- |
| `Day04-01练习/review_practice.py` | **反面教材，故意留有安全漏洞**（`eval`、路径硬拼、无异常处理）。请对照 `review_practice_fixed.py` 阅读，不要照抄。 |
| `Day05/day05_practice.py` 的 `calculate` | 先做字符白名单过滤再 `eval`，代码注释已标注生产环境应改用 `ast`。 |
| `Day02` / `Day03` 的部分请求 | 请求 `https://api.example.com/llm` 这类**不存在的地址**是刻意的，用于演示异常捕获。 |
| 路径依赖 | Day01~Day07 脚本的相对路径基于**当前工作目录**，请在 `01_python_basic/` 下运行；`Day03/day03_file_env.py` 与 `Day08_project` 基于 `__file__`，可在任意目录运行。 |
| `.env` 缺失 | 当前仓库只有 `.gitignore`，没有 `.env`。没有它时 Day05 及之后的脚本会给出密钥缺失提示。 |
| 免费 API 时效性 | `wttr.in`、`zippopotam.us`、`httpbin.org` 为公共免费服务，偶有不稳定属正常，脚本已做降级处理。 |
| Token 阈值不一致 | `Day06/day06_context_compression.py` 与 `Day06-01练习/stock simulation.py` 内部常量 `TOKEN_LIMIT=800`，`Day08_project` 集中配置为 1500。 |
| 日志文件命名 | `Day07/day07_dirty_data_defense.py` 输出的日志仍沿用旧编号命名 `logs/day12_dirty.log`。 |

---

## 🔗 与《AI-Agent_Python学习手册》的对应关系

手册里规划的是 **14 天**路径，实际按 **8 天（Day01~Day08）** 落地并在压缩中合并了部分内容：

| 手册计划 | 实际落点 |
| :--- | :--- |
| Day 1-3 语法热身 | Day01（数据结构）+ Day02（循环/异常）+ Day03（网络/文件） |
| Day 4-7 核心交互（ReAct 雏形） | Day04（Pydantic + 模拟 ReAct）+ Day05（Function Calling + 真实 LLM） |
| Day 8-11 工具扩展与健壮性 | Day05 工具注册表 + Day06（日志/压缩/持久化）+ Day07（脏数据防御） |
| Day 12 脏数据清洗 | Day07 |
| Day 13 项目工程化 | **Day08_project**（`config` / `core` / `tools` / `utils` / `prompts` 分层） |
| Day 14 部署与交付 | 已并入本 README 与 `Day08_project/requirements.txt` |

---

## 📎 下一步

- [ ] 补齐 `Day08_project` 的 `.env.example`（当前只有 `.env` 说明）
- [ ] 为 `Day08_project` 引入单元测试（目前仅 Day07 自带测试用例）
- [ ] 将 `Day08_project` 的工具注册表扩展为可插拔加载（自动扫描 `tools/` 目录）
- [ ] 进入下一阶段：`02_rag_project`（RAG 完整项目）
