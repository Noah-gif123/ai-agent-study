# 02 · N2-Grammar-Companion（日语 N2 语法检索助手）

> 面向 N2 备考者的日语语法检索助手。核心是解决**中文提问 → 日文语料**的跨语言召回问题，
> 并用可复现的评测数据量化每一次优化决策。
>
> 本阶段分 V0（原生手写）与 V1（LangChain 重构）两版，完整规划见根目录
> `N2_Grammar_Companion_Plan.docx` 与 `RAG项目规划以及后续.docx`。

**当前状态：环境已搭建并验证通过 ✅ → 下一步 M1（数据资产）**

---

## 一、环境状态（实测，已完成）

| 项 | 值 |
|---|---|
| Python | 3.14.4（`py -3.14`） |
| 虚拟环境 | `.venv/`（项目内，非全局） |
| 显卡 | RTX 4060 Laptop 8GB，**当前 torch 为 CPU 版**，CUDA 未启用 |
| 磁盘 | E 盘剩余 89GB；模型与 pip 缓存均已指向 E 盘 |

### 已安装依赖

| 分组 | 版本 |
|---|---|
| 基础 | numpy 2.5.3、requests 2.34.2、pydantic 2.13.5、tiktoken 0.14.0、openai 3.14.1 |
| M1~M4 检索 | **torch 2.14.0+cpu**、sentence-transformers 6.0.1、transformers 5.17.0、faiss-cpu 1.15.0 |
| M6~M7 服务化 | fastapi 0.141.1、uvicorn 0.53.0、gradio 6.27.0、sse-starlette 3.4.11 |
| V1 LangChain | langchain 1.4.0、langgraph 1.2.11、langchain-huggingface 1.2.2、rank-bm25 0.2.2、fugashi 1.5.2 |

完整版本清单见 `requirements.lock.txt`（已锁定，勿手改）。

### 模型状态

| 模型 | 状态 | 体积 |
|---|---|---|
| `BAAI/bge-m3`（Embedding） | ✅ 已下载并验证可加载 | 2.16 GB |
| `BAAI/bge-reranker-v2-m3`（重排序） | ⏳ 未下载，M5 再装 | — |

### 首次真实验证结果

用 bge-m3 跑通了一次跨语言相似度测试，**项目核心假设成立**：

```
向量维度 1024 | 模型加载 36.5s（CPU 冷启动）| 编码 3 条 0.3s

余弦相似度：
  "表示虽然但是的语法"(中文)  ↔  〜にもかかわらず  = 0.698   ← 正确目标
  "表示虽然但是的语法"(中文)  ↔  〜ばかりに        = 0.528   ← 无关项
```

正确目标的相似度比无关项高 **0.17**，跨语言召回在模型层面是可行的。
这组数字也是后面消融实验 E1 组的起点。

---

## 二、环境搭建（已完成，此处供重建参考）

```powershell
# 1. 建虚拟环境
py -3.14 -m venv .venv

# 2. 安装依赖（分阶段）
.\setup.ps1 -Stage core        # M1~M4：约 1GB
.\setup.ps1 -Stage service     # M6~M7：约 100MB
.\setup.ps1 -Stage langchain   # V1：约 200MB
# .\setup.ps1 -Stage cuda      # M5 才需要：把 CPU 版 torch 换成 CUDA 版（约 3GB）

# 3. 下载模型
.\.venv\Scripts\Activate.ps1
python scripts\download_models.py            # Embedding 模型（约 2.2GB，约 4 分钟）
python scripts\download_models.py --reranker # M5 时再加重排序模型
python scripts\download_models.py --check    # 只看状态，不下载

# 4. 自检
.\setup.ps1 -Stage check
```

若提示「禁止运行脚本」，先执行一次：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## 三、分阶段安装对照

| 阶段 | 命令 | 装什么 | 体积 | 对应里程碑 |
|---|---|---|---|---|
| 核心 | `-Stage core` | torch、sentence-transformers、faiss-cpu | ~1GB | M1~M4 |
| 服务化 | `-Stage service` | fastapi、uvicorn、gradio | ~100MB | M6~M7 |
| 框架重构 | `-Stage langchain` | langchain、langgraph、fugashi 等 | ~200MB | V1 |
| 显卡加速 | `-Stage cuda` | 把 CPU 版 torch 换成 CUDA 12.6 版 | ~3GB | M5 |

**CUDA 留到 M5 再升。** M1~M4 用 CPU 版足够：模型加载 36.5s 是一次性成本，
编码速度（本机实测 3 条 0.3s）对几千条语料的批量编码完全可接受。

---

## 四、缓存为什么不在 C 盘

C 盘只剩约 12.8GB，而 bge-m3 权重 2.2GB、CUDA 版 torch 又 3GB，很容易撑爆。

`setup.ps1` 已把缓存与临时目录指向项目的 `.cache/`，并写入用户级环境变量：

```
.cache/hf     ← HF_HOME，HuggingFace 模型权重
.cache/pip    ← PIP_CACHE_DIR，pip 下载缓存
.cache/tmp    ← TEMP / TMP，pip 解压临时目录
```

同时设置了 `HF_ENDPOINT=https://hf-mirror.com`（实测镜像 2.1s vs 官方 4.4s）。
想切回官方源，删除这一行环境变量即可。

---

## 五、目录结构

```
02_mini-native-rag-jp/
├── .venv/                  # 虚拟环境（gitignore）
├── .cache/                 # 模型与 pip 缓存（gitignore）
├── setup.ps1               # 环境搭建脚本
├── check_env.py            # 环境自检
├── requirements/           # 分阶段依赖清单
│   ├── 01-core.txt
│   ├── 02-service.txt
│   └── 03-langchain.txt
├── requirements.lock.txt   # 已锁定的完整版本（gitignore）
├── scripts/
│   └── download_models.py  # 模型预下载（支持断点续传）
├── v0/                     # 原生手写版
├── v1/                     # LangChain 重构版（文件名与 v0 一一对应）
├── data/                   # 文档集（raw/ 已 gitignore）
├── evaluation/             # 黄金测试集、评测脚本、消融实验、报告
├── index/                  # FAISS 索引 + metadata（gitignore）
└── .backup/                # 规划文档的初版备份
```

> 📌 根目录 `README.md` 里写的是 `v0_native_faiss/` 和 `v1_langchain_refactor/`，
> 与本项目实际目录 `v0/` `v1/` 不一致，需要把根 README 改过来。

---

## 六、里程碑进度

| 里程碑 | 内容 | 状态 |
|---|---|---|
| — | 环境搭建与验证 | ✅ 完成 |
| M1 | 数据资产：文档集 3000+ chunk + 黄金评测集 60 条 | ⏳ **下一步** |
| M2 | 检索链路：loader / chunker / embedder / indexer / retriever | ⏳ |
| M3 | 生成链路：Prompt + 引用溯源 + 无据拒答 | ⏳ |
| M4 | 评测基线：Hit@1 / Recall@3 / MRR | ⏳ |
| M5 | 重排序 + 7 组消融实验（含 CUDA 升级） | ⏳ |
| M6 | 服务化：FastAPI + 流式 + 超时重试 + Docker | ⏳ |
| M7 | 演示界面：Gradio | ⏳ |
| M8 | 文档复盘：README + 架构图 + bad case 分析 + 博客 | ⏳ |

**第 4 周（M4 完成）即可开始投递**，不必等 M8 全部做完。

---

## 七、已踩过的坑（务必先看，能省你几小时）

1. **`.ps1` 必须存成 UTF-8 with BOM**
   本机默认的 `pwsh` 实际是 Windows PowerShell 5.1，它会把无 BOM 的 UTF-8 当本地
   ANSI 码页读取，脚本里的中文会乱码并直接报语法错误（`Unexpected token '}'`）。
   `setup.ps1` 已存为带 BOM 格式，新增 PowerShell 脚本请照做。

2. **控制台中文乱码**
   PS 5.1 的 `[Console]::OutputEncoding` 默认是 GBK。`setup.ps1` 已强制设为 UTF-8
   并设置 `PYTHONIOENCODING=utf-8`。

3. **`BAAI/bge-m3` 没有 `model.safetensors`**
   它的权重只存在于 `pytorch_model.bin`。用 `allow_patterns=["*.safetensors"]`
   下载会得到一个只有配置文件的空壳。`download_models.py` 已同时匹配 `*.bin`。

4. **不能用「缓存目录非空」判断模型是否下好**
   失败的下载会留下几 MB 的配置与元数据。必须校验权重文件体积
   （`download_models.py` 用 100MB 作为阈值）。

5. **HF 符号链接警告**
   下载时会提示 "your machine does not support symlinks"。这不影响使用，
   只是缓存会多占一些磁盘。想消除：开启 Windows 开发者模式。

6. **`python` 命令是商店假别名**
   直接敲 `python` 会报 9009。用 `py -3.14`，或先激活 `.venv`。

---

## 八、依赖策略说明（对应规划书「决策三」）

**刻意不安装 `langchain-community`。**

实测：在 LangChain 1.x 线上，`langchain-community` 最新版仍是 `1.0.0a1`（alpha），
而 `FAISS` / `BM25Retriever` / `HuggingFaceEmbeddings` / `EnsembleRetriever`
大半都在这个包里。

因此 V1 的策略是「**框架负责编排，检索层保持自研**」：

| 能力 | 做法 |
|---|---|
| Embedding | `langchain-huggingface`（官方 partner 包，稳定线） |
| 向量检索 | 复用 V0 已手写的 FAISS 封装 |
| 混合检索 | 自己写 RRF 融合（约 15 行），权重用评测数据选 |
| 对话记忆 | `langgraph.checkpoint`，不用已移除的 `ConversationBufferMemory` |

这不是妥协 —— 它有版本依据和取舍理由，本身就是面试可讲的技术判断。
