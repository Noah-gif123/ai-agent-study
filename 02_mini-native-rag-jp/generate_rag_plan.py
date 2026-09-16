# -*- coding: utf-8 -*-
"""
生成《AI Agent 应用开发学习总规划》（修订版 v2）

相比初版的修订要点见文档第〇章。
依赖：python-docx
运行：py -3.14 generate_rag_plan.py
输出：与本脚本同目录的 RAG项目规划以及后续.docx
"""

import os

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(OUT_DIR, "RAG项目规划以及后续.docx")

FONT = "微软雅黑"
MONO = "Consolas"
GREY = RGBColor(0x60, 0x60, 0x60)
RED = RGBColor(0xC0, 0x30, 0x30)
BLUE = RGBColor(0x1F, 0x4E, 0x79)


# --------------------------------------------------------------------------
# 排版辅助
# --------------------------------------------------------------------------
def set_cn_font(run, font_name=FONT):
    run.font.name = font_name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:eastAsia"), font_name)
    rfonts.set(qn("w:ascii"), font_name)
    rfonts.set(qn("w:hAnsi"), font_name)


def add_heading_cn(doc, text, level):
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        set_cn_font(run)
    return heading


def add_para_cn(doc, text, bold=False, size=11, color=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    set_cn_font(run)
    return p


def add_bullets(doc, items, size=11):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        run.font.size = Pt(size)
        set_cn_font(run)


def add_code_cn(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = MONO
    run.font.size = Pt(9)
    return p


def add_table_cn(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                set_cn_font(run)
                run.bold = True
    for i, row_data in enumerate(rows, start=1):
        for j, val in enumerate(row_data):
            cell = table.rows[i].cells[j]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    set_cn_font(run)
                    run.font.size = Pt(10)
    doc.add_paragraph()
    return table


# --------------------------------------------------------------------------
# 文档
# --------------------------------------------------------------------------
doc = Document()

style = doc.styles["Normal"]
style.font.name = FONT
style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
style.font.size = Pt(11)

title = doc.add_heading("AI Agent 应用开发学习总规划", 0)
title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
for run in title.runs:
    set_cn_font(run)
    run.font.size = Pt(24)

subtitle = doc.add_paragraph("—— 以 N2 日语知识库项目贯穿 RAG、ReAct 与 LangGraph 全程（修订版 v2）")
subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
for run in subtitle.runs:
    set_cn_font(run)
    run.font.size = Pt(13)
    run.font.color.rgb = GREY

meta = doc.add_paragraph("软件工程方向 · 目标 AI Agent 应用开发实习 · 同步备考日语 N2 · 2026 年 9 月起")
meta.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
for run in meta.runs:
    set_cn_font(run)
    run.font.size = Pt(11)
    run.font.color.rgb = GREY

doc.add_paragraph()

# ==========================================================================
add_heading_cn(doc, "〇、本版修订说明（v1 → v2）", level=1)
add_para_cn(
    doc,
    "初版的路线（先手写 V0、再框架重构、同一业务贯穿四阶段）是正确的，本版不改路线，"
    "只解决三个执行层面的问题：深度不足、两份文档口径打架、最能得分的内容被写成了“局限”。",
    bold=True,
)
add_table_cn(
    doc,
    ["#", "修订点", "初版", "修订版", "为什么改"],
    [
        (
            "1",
            "项目深度定位",
            "V0 手写模块拆分只到“检索 + 生成 + Gradio”",
            "补上数据资产、评测体系、服务化、日语场景深化四块，并从“选做”提升为必做",
            "初版产出是教程级完整度，同质化严重；缺的这四块正是拉开差距的地方",
        ),
        (
            "2",
            "时间口径",
            "总规划写“阶段二约 2 周”，版本规划书写“8~10 天”，两者矛盾",
            "统一按“每周 3 次 × 2~2.5 小时”计量，阶段二约 10 周，全流程约 14 周",
            "两份文档口径不一致会让排期直接作废",
        ),
        (
            "3",
            "投递节奏",
            "“11—12 月为可正式实习时间”，隐含“全做完再投”",
            "改为滚动投递：第 4 周产出可投递版本即开始投，后续迭代同步更新简历",
            "等全做完再投会错过窗口期；边投边做还能用面试反馈校准方向",
        ),
        (
            "4",
            "评测与差异化",
            "20 条测试 query + Recall@3，对比加/不加重排序",
            "60 条四层测试集 + Hit@1/MRR/拒答率 + 7 组消融矩阵 + bad case 归因",
            "“80 条库里 Recall@3 ≥70%”经不起追问；消融数据是应用岗最稀缺的证据",
        ),
        (
            "5",
            "工程化",
            "FastAPI、Docker、PDF 解析都放在“迭代计划”里",
            "FastAPI 服务化 + 并发压测 + 成本日志列为阶段二必做",
            "应用开发岗最核心的考察点被写成了“我没做”，等于主动交白卷",
        ),
        (
            "6",
            "阶段三定位",
            "手写 ReAct 约 1 周，产出代码提交",
            "压缩到 3 次，明确“以理解为目的，不追求工程完整”",
            "它的价值在于拿到 ReAct 的“为什么”，产出本身不进简历核心位置",
        ),
        (
            "7",
            "Java 背景",
            "只在附录“兜底方案”里出现，作为退路",
            "提升为并行优势，在第 9、10 章单独展开",
            "Spring AI / LangChain4j 方向的岗位看重“Java 后端 + AI 应用”组合，这是优势不是退路",
        ),
        (
            "8",
            "面试准备",
            "只列了高频问题清单",
            "新增 30 秒叙述结构、决策叙事模板、失败案例准备",
            "面试官考的是判断过程；同样经历，表达方式决定结果",
        ),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "1  规划总览", level=1)

add_heading_cn(doc, "1.1  本规划的目的", level=2)
add_para_cn(
    doc,
    "本规划面向一名软件工程专业本科生，主修语言为 Java，Python 基础相对薄弱，近期已完成 Python "
    "基础专项训练（Day 01～11）。目标是在 2026 年 9 月至 12 月期间，系统掌握 AI Agent 应用开发的"
    "核心能力，产出两个能写进简历、能在面试中深入讲解的完整项目，并为 11—12 月投递 AI Agent "
    "应用开发实习岗位做好准备。",
)

add_heading_cn(doc, "1.2  贯穿全流程的主线", level=2)
add_para_cn(
    doc,
    "全流程共用同一个业务项目：N2 日语知识库查询助手。以“日语备考”为垂直场景，先后用 RAG、"
    "手写 ReAct、LangGraph 三种技术形态实现同一业务，形成一条连贯的技术演进主线，"
    "而非几个互不相关的零散 Demo。这既满足练技术的要求，又与日语 N2 备考并行互惠。",
)
add_para_cn(
    doc,
    "需要强调的是：这条主线成立的前提是「同一个项目越做越深」，而不是「同一个题目换三种框架重做」。"
    "每一阶段都必须在前一阶段的评测基线上有可量化的提升，否则演进就只是重复劳动。",
    bold=True,
)

add_heading_cn(doc, "1.3  总体路线图", level=2)
add_table_cn(
    doc,
    ["阶段", "主题", "技术形态", "产出（仓库目录）", "周期", "备注"],
    [
        ("阶段一", "Python 基础", "语法与 API 调用练习", "01_python_basic", "已完成", "Day01-11"),
        ("阶段二", "N2 日语 RAG", "V0 原生手写 + V1 LangChain 重构", "02_mini-native-rag-jp", "约 10 周", "当前阶段，简历第一项目"),
        ("阶段三", "手写原生 ReAct", "不依赖框架的 Agent 循环", "03_handwritten_react", "约 1 周", "理解底层，不追求工程完整"),
        ("阶段四", "LangGraph 日语 Agent", "LangGraph 编排多工具智能体", "04_langgraph_jp_agent", "约 3 周", "简历核心项目"),
    ],
)

add_heading_cn(doc, "1.4  核心原则（新增三条）", level=2)
add_bullets(
    doc,
    [
        "【原有】先造轮子，再用轮子：先手写实现理解底层原理，再引入 LangChain / LangGraph 提速。",
        "【原有】先手写再框架：RAG 先手写 V0 再重构 V1；Agent 先手写 ReAct 再上 LangGraph。",
        "【原有】项目贯穿一致：同一个 N2 日语知识库数据，逐阶段升级，形成可讲述的演进式作品。",
        "【原有】不刷完整网课：每看 8—12 分钟暂停动手复现，边做项目边补语法。",
        "【新增】每一个改动都要有对照组：不写“我用了 X 所以更好”，只写“用了 X 之后指标从 A 变成 B”。",
        "【新增】数据规模和评测深度优先于功能数量：一个能聊 20 分钟的项目，胜过四个只能演示的项目。",
        "【新增】必须有可点开的产出：在线 Demo、评测报告、技术博客，这三样是“没有实习经历”时最有效的替代证据。",
    ],
)

# ==========================================================================
add_heading_cn(doc, "2  总体学习路线", level=1)
add_table_cn(
    doc,
    ["阶段", "核心目标", "主要技术", "承接关系"],
    [
        ("一、Python 基础", "够用的 Python 语法与 API 调用", "函数、异常、json、requests、dotenv", "为后续全部代码打底"),
        ("二、RAG 项目", "实现带知识库、带评测、可服务化的问答系统", "Embedding、向量检索、混合检索、重排序、FastAPI、Gradio", "复用 Python 能力，产出知识库与评测体系"),
        ("三、手写 ReAct", "看懂 Agent 底层循环", "Thought-Action-Observation、工具注册表", "把 RAG 检索抽象为工具"),
        ("四、LangGraph Agent", "实现自主调用工具的智能体", "LangGraph、State、多工具、流式输出", "把 RAG 封装为 Tool 接入"),
    ],
)
add_para_cn(
    doc,
    "与初版的差别主要在第二阶段：它不再只是“实现问答系统”，而是“实现一个带评测体系和服务化能力的"
    "问答系统”。这个差别决定了简历能不能过筛选。",
    bold=True,
)

# ==========================================================================
add_heading_cn(doc, "3  阶段一：Python 基础（已完成 Day 01～11）", level=1)
add_heading_cn(doc, "3.1  阶段定位", level=2)
add_para_cn(
    doc,
    "只学 AI Agent 开发高频用到的部分，不系统学完整个语言，也不学爬虫、数据分析、pandas 等"
    "与岗位无关的内容。目标是看得懂 Agent 代码、能写函数、能处理 json、能捕获异常、能调用大模型 API。",
)

add_heading_cn(doc, "3.2  已完成内容回顾", level=2)
add_bullets(
    doc,
    [
        "语法与数据结构：变量、f-string、list/dict 增删改查、while 循环与 break/continue。",
        "函数：def 定义、参数、返回值、关键字参数。",
        "异常处理：try-except 捕获 JSONDecodeError、KeyError、RequestException。",
        "文件与数据：with open 读写、json.dump/load、os.path、python-dotenv。",
        "数据校验：Pydantic BaseModel、Field。",
        "API 调用：requests.post 调用 DeepSeek；原生 Function Calling（tools 参数、tool_calls 解析）。",
        "工程能力：logging 双输出、tiktoken Token 计数、上下文压缩与 Token 超限自动触发。",
        "Agent 雏形：ReAct 主循环、工具注册表（TOOLS 字典）、模拟 LLM 思考。",
    ],
)

add_heading_cn(doc, "3.3  阶段产出", level=2)
add_para_cn(
    doc,
    "已提交至统一仓库的 01_python_basic 目录。此阶段已完成，直接进入阶段二。",
)
add_para_cn(
    doc,
    "补充一句：你已有的 Java 基础在这里是隐形资产 —— 异常体系、面向对象、分层设计、日志规范"
    "这些工程习惯，Python 初学者往往要花很久才建立。你缺的只是 Python 的语法手感，不是工程素养。"
    "这一点在第 9、10 章会展开。",
    bold=True,
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "4  阶段二：N2 日语 RAG 项目（当前阶段）", level=1)

add_heading_cn(doc, "4.1  项目定位与差异化", level=2)
add_para_cn(
    doc,
    "项目名为“N2 日语智能查询助手”，面向日语 N2 备考者，内置日语语法资料，用户用中文或日文提问，"
    "系统检索知识库并给出带出处的回答。选择日语垂直场景，区别于千篇一律的通用 PDF 问答。",
)
add_para_cn(
    doc,
    "一句话定位（写进 README 和简历）：",
    bold=True,
)
add_para_cn(
    doc,
    "「面向 N2 备考者的日语语法检索助手，重点解决中文提问 → 日文语法库的跨语言召回问题，"
    "并用可复现的评测数据量化每一次优化决策。」",
    color=BLUE,
)

add_heading_cn(doc, "4.2  技术路线：先手写 V0，再框架重构 V1", level=2)
add_para_cn(
    doc,
    "第一版不依赖 LangChain，用原生 Python 手动实现完整 RAG 链路；第二版用 LangChain 重构同一套业务。"
    "手写的价值不在于“证明自己能手搓”，而在于拿到那些“为什么”的答案 —— "
    "面试官问“为什么用稠密检索而不是 BM25”，只有手写过的人才答得出。",
    bold=True,
)

add_heading_cn(doc, "4.3  数据资产（初版缺失，本版前移为第一优先级）", level=2)
add_para_cn(
    doc,
    "初版把 80 条语法 JSON 同时当检索库和评测集。问题有两个：80 条规模下向量检索没有意义；"
    "用检索库考自己，指标必然虚高。修订版拆成两层：",
    bold=True,
)
add_table_cn(
    doc,
    ["数据层", "规模", "作用", "来源"],
    [
        ("文档集（检索对象）", "3000+ chunk", "被检索的语料，决定检索这个技术点是否成立", "N2 语法书结构化整理 + 例句拆分 + 辨析段落"),
        ("黄金评测集", "60 条 query", "评测检索质量，人工复核期望答案", "自己构造，按四层分类，与文档集严格分离"),
        ("开发集 / 测试集", "24 / 36 条", "调参只用开发集，最终只报测试集", "由黄金集按 4:6 划分"),
    ],
)
add_para_cn(
    doc,
    "文档集的 chunk 按“释义块 / 例句块 / 辨析块”三种粒度切分，每个 chunk 带 parent_id 以便命中后"
    "回溯完整条目 —— 这是引用溯源功能的实现基础。数据工程往往占真实 RAG 项目 60% 以上的时间，"
    "把它写进简历比多写一个功能更有价值。",
)

add_heading_cn(doc, "4.4  V0 原生手写模块拆分", level=2)
add_table_cn(
    doc,
    ["模块", "功能", "复用技能", "commit 示例"],
    [
        ("文档加载与切分", "读取语料，按三种粒度切 chunk 并保留父子关系", "with open、字符串处理", "feat: 三粒度分块与父子关系"),
        ("Embedding 向量化", "本地 bge-m3 批量编码 + L2 归一化", "requests/Pydantic、异常捕获", "feat: 文本向量化与异常捕获"),
        ("向量检索", "FAISS 索引 + 余弦相似度，召回 Top-K 并返回分数", "list/dict、排序", "feat: 原生向量检索与 top-k 召回"),
        ("重排序", "bge-reranker-v2-m3 二次打分，可开关对比", "模型加载、缓存", "feat: CrossEncoder重排序与开关"),
        ("RAG 主流程", "命中 chunk 注入 Prompt，要求标注出处、无据拒答", "Prompt 工程、LLM 调用", "feat: RAG 问答主链路"),
        ("评测脚本", "跑测试集输出 Hit@1 / Recall@3 / MRR", "json、统计", "feat: 检索评测脚本与基线数据"),
        ("工程打磨", "logging 双输出、token 计数、上下文压缩", "tiktoken、logging", "feat: 日志与 token 管理"),
        ("服务化", "FastAPI 接口 + 流式 + 超时重试 + 成本日志", "FastAPI、异步", "feat: FastAPI 服务化接口"),
        ("Gradio 界面", "网页交互演示，展示答案与引用来源", "Gradio", "feat: Gradio 演示页面"),
    ],
)
add_para_cn(
    doc,
    "相比初版，新增了「重排序开关」「评测脚本」「服务化」三个模块。"
    "注意重排序做成开关而不是写死在链路里 —— 没有开关就没有对照组，没有对照组就没有消融数据。",
    bold=True,
)

add_heading_cn(doc, "4.5  定制日语助教 Prompt 要点", level=2)
add_bullets(
    doc,
    [
        "严格使用提供的参考资料回答，资料中没有的内容明确说明“暂无该知识点”，不编造。",
        "讲解标注读音、接续、中文释义，附带 N2 难度例句。",
        "遇到易混淆语法主动对比辨析（如「に」与「で」）。",
        "【新增】每条结论后面标注来源 chunk 的 id 与语法名，支持引用溯源。",
        "【新增】输出结构固定化（释义 / 接续 / 读音 / 例句 / 辨析 / 出处），便于 Gradio 结构化渲染。",
        "【新增】Prompt 里显式给出拒答范式，并把“拒答是否正确”纳入评测指标。",
    ],
)

add_heading_cn(doc, "4.6  V1 LangChain 重构（修正初版的过时 API）", level=2)
add_para_cn(
    doc,
    "本机已装 langchain 1.3.18 / langchain-core 1.6.1 / langgraph 1.2.11，属于 LangChain 1.x 时代。"
    "初版对比表里的 ConversationBufferMemory 已被移除，JSONLoader 维护也很弱；更关键的是 "
    "langchain-community 在 1.x 线上最新仍是 1.0.0a1（alpha），而 FAISS / BM25Retriever / "
    "HuggingFaceEmbeddings / EnsembleRetriever 大半都在这个包里。因此 V1 的策略是："
    "检索层保持自研，只让框架负责编排与状态管理。",
    bold=True,
)
add_table_cn(
    doc,
    ["维度", "V0（手搓）", "V1（LangChain）"],
    [
        ("数据加载", "手写 json.load + chunk 拼装", "自写 loader 产出 Document（不用 JSONLoader）"),
        ("向量存储", "手写 FAISS + metadata 同序落盘", "FAISS.from_documents()"),
        ("检索", "单路稠密检索", "混合检索：日语分词 BM25 + 稠密 + 加权 RRF"),
        ("重排序", "手写 CrossEncoder 打分", "ContextualCompressionRetriever 组合"),
        ("对话记忆", "无", "RunnableWithMessageHistory（不用已移除的 ConversationBufferMemory）"),
        ("流式输出", "无", "astream_events 逐字返回"),
        ("日语分词", "无（余弦检索不需要）", "BM25Retriever 传 preprocess_func，用 fugashi + unidic-lite"),
    ],
)
add_para_cn(
    doc,
    "V0 与 V1 使用同一份数据、同一套评测集，指标直接可比。差异写入 README："
    "原生版本适合理解原理，框架版本适合工程落地，并说明框架替开发者省了什么、又拿走了什么控制权。",
)
add_para_cn(
    doc,
    "依赖侧的三条硬约束（详见《N2-Grammar-Companion 版本规划书》2.3 / 2.4）："
    "① Embedding 改走官方 partner 包 langchain-huggingface，不引入 alpha 状态的 community；"
    "② transformers 已到 5.x，与网上大量 4.x 教程 API 不一致；"
    "③ 装完立刻 pip freeze 钉死版本，否则 1.x 换代后两周就无法复现。",
    bold=True,
)

add_heading_cn(doc, "4.7  评测体系（本版重点重写）", level=2)
add_para_cn(
    doc,
    "初版是“20 条测试 query + Recall@3 ≥ 70%”。在 80 条的小库上，随机猜 Top-3 都有 3.75% 命中率，"
    "这个数字既没有区分度也经不起追问。修订为：",
    bold=True,
)
add_table_cn(
    doc,
    ["指标", "说明", "目标"],
    [
        ("Hit@1", "Top-1 是否命中，最贴近用户体验", "≥ 55%"),
        ("Recall@3", "Top-3 中是否命中，保留作为对照", "≥ 80%"),
        ("MRR@10", "首个正确结果排名的倒数均值，对排序敏感", "≥ 0.70"),
        ("拒答准确率", "知识库外问题正确拒答的比例", "≥ 90%"),
        ("端到端正确率", "LLM 最终答案是否正确（人工判 30 条）", "≥ 80%"),
        ("P95 延迟", "端到端耗时 95 分位（平均延迟会掩盖长尾）", "< 5 秒"),
    ],
)
add_para_cn(doc, "四层测试集设计（共 60 条）：", bold=True)
add_table_cn(
    doc,
    ["层级", "类型", "示例", "考察点", "条数"],
    [
        ("L1", "直接点名", "「〜ばかりに」是什么意思？", "基础检索，应接近满分", "15"),
        ("L2", "中文意图", "表示“正因为…才…”的语法有哪些？", "跨语言召回，本项目核心难点", "20"),
        ("L3", "近义辨析", "「〜ものの」和「〜にもかかわらず」有什么区别？", "多跳召回与对比", "15"),
        ("L4", "应拒答", "N1 的「〜ずにはおかない」怎么用？", "防幻觉能力", "10"),
    ],
)
add_para_cn(doc, "消融实验矩阵（简历上最有价值的一张表）：", bold=True)
add_table_cn(
    doc,
    ["组", "Embedding", "检索", "重排序", "分块", "验证什么"],
    [
        ("基线", "中文单语 embedding", "稠密", "无", "整条", "用数据证明“跨语言召回”这个问题真实存在"),
        ("E1", "bge-m3", "稠密", "无", "整条", "换多语言模型的提升幅度"),
        ("E2", "bge-m3", "BM25（日语分词）", "无", "整条", "纯稀疏在日语场景的水平"),
        ("E3", "bge-m3", "混合 RRF", "无", "整条", "混合是否优于单路"),
        ("E4", "bge-m3", "混合 RRF", "有", "整条", "重排序的增益（L2/L3 应最明显）"),
        ("E5", "bge-m3", "混合 RRF", "有", "三粒度", "分块粒度对召回的影响"),
        ("E6", "托管 API embedding", "混合 RRF", "有", "三粒度", "本地 vs 云端的性价比"),
    ],
)
add_para_cn(
    doc,
    "此外，每次评测失败都要填一张 bad case 归因表，固定四类归因：跨语言语义偏差、"
    "分词或关键词失效、分块切断上下文、同义语法互相干扰。跑完一轮你会得到一张分布图 —— "
    "“我的失败案例里 60% 是分块问题”这种结论，比任何技术名词都更像做过真项目的人说的。",
)

add_heading_cn(doc, "4.8  服务化与工程化（从“迭代计划”提升为必做）", level=2)
add_para_cn(
    doc,
    "初版把“未接 FastAPI”写在局限里。这是最大的战略性失误：应用开发岗最核心的考察点，"
    "被写成了“我没做”。本版把它提为必做。",
    bold=True,
)
add_table_cn(
    doc,
    ["能力", "做法", "面试可讲点"],
    [
        ("接口设计", "POST /ask、POST /ask/stream（SSE）、GET /health", "为什么流式单独开接口"),
        ("超时与重试", "LLM 超时 + 指数退避 + 熔断兜底", "依赖挂了是降级返回检索结果还是报错"),
        ("并发", "异步接口 + 连接池，脚本压 20 并发", "瓶颈在检索还是推理，怎么观测到的"),
        ("成本控制", "记录每次 token 数与预估费用", "单次问答成本多少，缓存怎么降本"),
        ("可观测性", "结构化日志：请求 id、检索耗时、生成耗时、命中数", "线上出问题怎么定位"),
        ("容器化", "Dockerfile，模型权重 volume 挂载不进镜像", "为什么模型不打进镜像"),
    ],
)

add_heading_cn(doc, "4.9  日语场景深化（唯一的真差异化）", level=2)
add_bullets(
    doc,
    [
        "日语分词：fugashi + unidic-lite 解决“日语没空格导致关键词检索失效”，是混合检索能生效的前提。",
        "读音标注：schema 增加 reading 字段，回答时输出假名，直接服务 N2 备考。",
        "近义网络：用 similar 字段建语法关系图，支持“和它相近的还有哪些”，是多跳查询的基础。",
        "易混辨析：内置高频易混语法对，对应真实备考痛点。",
        "语体标注：标注例句的书面/口语/敬语属性，支持按语体过滤。",
    ],
)
add_para_cn(
    doc,
    "通用 RAG 教程不会教这些，而它们恰好是你作为日语备考者的天然优势。"
    "面试官一天看几十份 RAG 简历，能被记住的往往是这类“只有真懂这个场景才做得出来”的细节。",
    bold=True,
)

add_heading_cn(doc, "4.10  阶段二验收清单", level=2)
add_para_cn(doc, "全部达成即可写进简历并在面试中展开：", color=GREY)
add_table_cn(
    doc,
    ["验收项", "标准"],
    [
        ("数据", "文档集 3000+ chunk；黄金评测集 60 条且人工复核过"),
        ("评测", "report.md 含 Hit@1/Recall@3/MRR/拒答率基线，含 7 组消融矩阵，含 bad case 归因分布"),
        ("可运行", "命令行能跑通；FastAPI 接口本地可访问"),
        ("可演示", "有一个点得开的链接（在线 Demo 或录屏）"),
        ("工程", "有超时重试、成本日志、20 并发压测记录"),
        ("对照", "V0/V1 指标对照表有明确结论"),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "5  阶段三：手写原生 ReAct（压缩为 3 次）", level=1)
add_heading_cn(doc, "5.1  目的", level=2)
add_para_cn(
    doc,
    "在进入 LangGraph 之前，先手写一个不依赖任何框架的简易 ReAct 智能体，用几十行原生 Python 实现 "
    "Thought → Action → Observation 循环，亲眼看见 Agent 底层到底发生了什么。",
)
add_para_cn(
    doc,
    "本版把这一阶段从“约 1 周”压缩到 3 次，并明确它的定位：以理解为目的，不追求工程完整。"
    "它的产出主要用于回答面试题“不依赖框架你怎么实现一个 Agent”，而不是作为简历的核心项目。"
    "省下的时间投入到阶段二的深度和阶段四的落地。",
    bold=True,
)

add_heading_cn(doc, "5.2  实现要点", level=2)
add_bullets(
    doc,
    [
        "while 循环维护 Agent 主循环，设置最大迭代次数，防止死循环。",
        "工具注册表 TOOLS 字典，按名称分发工具调用。",
        "把阶段二的 RAG 检索封装成第一个工具，为阶段四做准备。",
        "异常处理：工具调用失败、JSON 解析失败的兜底。",
        "【新增】打印完整的 Thought/Action/Observation 轨迹，这段轨迹截图就是面试时的讲解素材。",
    ],
)

# ==========================================================================
add_heading_cn(doc, "6  阶段四：LangGraph 日语 Agent 增强版", level=1)

add_heading_cn(doc, "6.1  承接关系", level=2)
add_para_cn(
    doc,
    "不重新做无关项目，而是复用阶段二的 N2 知识库与检索逻辑，把 RAG 检索封装为 LangGraph 的"
    "一个自定义 Tool，在此之上叠加 Agent 自主决策能力，形成真正的日语备考智能体，也是简历核心项目。",
)

add_heading_cn(doc, "6.2  基础必做能力", level=2)
add_table_cn(
    doc,
    ["能力", "说明", "难度"],
    [
        ("RAG 封装为 Tool", "Agent 自主判断是否调用知识库检索", "必做"),
        ("State 状态设计", "保存对话历史、工具返回、检索标记", "必做"),
        ("条件分支", "是否调用工具、工具失败/无结果的兜底", "必做"),
        ("多工具扩展", "语法检索、语法辨析、生成练习题、改错", "必做"),
        ("异常处理", "Function-Calling JSON 解析失败、接口超时", "必做"),
        ("流式输出", "astream_events，Gradio 对接", "必做"),
        ("【新增】评测", "复用阶段二测试集，对比“纯 RAG”与“Agent 调度”的端到端正确率", "必做"),
    ],
)
add_para_cn(
    doc,
    "最后一项是新增的，也是最能体现项目演进性的：如果加了 Agent 之后端到端指标没有提升，"
    "那这个 Agent 就是负收益。能说清楚这一点，比堆十个工具都有说服力。",
    bold=True,
)

add_heading_cn(doc, "6.3  进阶能力（拉开差距）", level=2)
add_bullets(
    doc,
    [
        "工具路由纠错：用户意图模糊时 Agent 反问澄清，而非无脑调用工具。",
        "内置评估链路：每轮回答后评估是否使用知识库、有无幻觉，记录日志。",
        "Checkpoint 持久化：使用 SqliteSaver，重启可恢复会话。",
    ],
)

add_heading_cn(doc, "6.4  高阶可选（写入迭代计划）", level=2)
add_para_cn(
    doc,
    "受日语备考时间约束，高阶内容做不完可写入 README 的后续迭代计划：接入 FastAPI 对外服务、"
    "扩展 PDF 教材导入、生成 N2 模拟题。但注意：FastAPI 在阶段二就应该做完了，"
    "不要留到这里。",
)

add_heading_cn(doc, "6.5  裁剪线（时间不够时）", level=2)
add_table_cn(
    doc,
    ["优先级", "内容", "理由"],
    [
        ("保", "RAG 封装为 Tool、State 设计、多工具、流式、评测对比", "这五项构成一个完整可讲的 Agent 项目"),
        ("简化", "Checkpoint 持久化", "能用内存版即可，持久化是加分项"),
        ("砍", "工具路由纠错、额外工具数量、界面美化", "边际收益低，面试几乎不追问"),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "7  项目仓库结构与 Git 维护", level=1)

add_heading_cn(doc, "7.1  统一仓库结构", level=2)
add_para_cn(doc, "全部学习内容提交到同一个仓库 ai-agent-study，保证提交时间线连续、项目演进清晰。")
add_code_cn(
    doc,
    """ai-agent-study/
├─ 01_python_basic/          # 阶段一 Python 基础练习
├─ 02_mini-native-rag-jp/    # 阶段二 N2 日语 RAG（V0 + V1 + 评测 + 服务化）
│   ├─ v0/                   #   原生手写版
│   ├─ v1/                   #   LangChain 重构版
│   ├─ api/                  #   FastAPI 服务 + Dockerfile
│   ├─ data/                 #   文档集（raw/ 原始语料 gitignore）
│   └─ evaluation/           #   黄金测试集、评测脚本、消融实验、报告
├─ 03_handwritten_react/     # 阶段三 手写原生 ReAct
└─ 04_langgraph_jp_agent/    # 阶段四 LangGraph 日语 Agent（简历核心）""",
)
add_para_cn(
    doc,
    "注意目录命名统一为 02_mini-native-rag-jp（与仓库现状一致），"
    "初版文档里混用的 02_mini_native_rag_jp、v0_handcrafted、v1_langchain 全部废弃。",
    bold=True,
)

add_heading_cn(doc, "7.2  提交与密钥安全", level=2)
add_bullets(
    doc,
    [
        "小步提交：每完成一个模块或小功能即 commit push，每日至少一次，维持 GitHub 活跃度。",
        "清晰 commit 信息：以 feat:/fix:/docs: 开头，写明内容。",
        "密钥安全：API_KEY 存入 .env，绝不硬编码提交；.env、venv、__pycache__ 加入 .gitignore。",
        "【新增】index/、data/raw/、模型权重目录加入 .gitignore —— 二进制文件不进 Git。",
        "【新增】evaluation/report.md 必须提交：它是简历里所有数字的出处，也是面试时最有力的证据。",
    ],
)

# ==========================================================================
add_heading_cn(doc, "8  时间规划与日语 N2 并行安排", level=1)

add_heading_cn(doc, "8.1  阶段时间表（统一口径）", level=2)
add_para_cn(
    doc,
    "口径统一为：每周 3 次代码学习，每次 2～2.5 小时。初版两份文档里“2 周”和“8~10 天”的"
    "矛盾说法全部作废，以本表为准。",
    bold=True,
)
add_table_cn(
    doc,
    ["阶段", "周期", "节奏建议", "里程碑式产出"],
    [
        ("阶段二 RAG", "约 10 周（含 40% 缓冲）", "每周 3 次，按里程碑推进", "第 4 周产出可投递第一版；第 10 周完整交付"),
        ("阶段三 手写 ReAct", "约 1 周（3 次）", "跑通为主，不追求工程完整", "能打印完整 Thought/Action/Observation 轨迹"),
        ("阶段四 LangGraph", "约 3 周（9～10 次）", "逐能力叠加，不一次复制大段代码", "含与纯 RAG 的端到端指标对比"),
        ("面试打磨", "持续", "每周 1 次", "复盘 bad case、练 30 秒叙述"),
    ],
)
add_para_cn(doc, "合计约 14 周 ≈ 3.5 个月。9 月起步，12 月中旬完整交付。", color=GREY)

add_heading_cn(doc, "8.2  滚动投递节奏（初版缺失，本版新增）", level=2)
add_para_cn(
    doc,
    "初版的隐含假设是“全做完再投”。风险是错过窗口期，而且没有面试反馈来校准方向。"
    "修订版改为滚动投递：",
    bold=True,
)
add_table_cn(
    doc,
    ["时间", "简历上有什么", "投什么", "目的"],
    [
        ("11 月初", "RAG V0 + 第一版评测报告", "中小厂、创业公司", "练面试手感，收集真实追问，反推要补的深度"),
        ("11 月中下旬", "加上服务化 + 在线 Demo + V1 对比报告", "大厂实习、垂直行业 AI 岗", "正式冲刺"),
        ("12 月", "加上 LangGraph Agent 项目", "补投 + 复盘二轮", "完整版简历"),
    ],
)
add_para_cn(
    doc,
    "特别提醒：面试被问倒的地方，就是下一周要补的内容。带着真实面试反馈回来迭代项目，"
    "比闷头把计划做完效率高得多。",
    bold=True,
)

add_heading_cn(doc, "8.3  每周节奏与日语 N2 并行", level=2)
add_bullets(
    doc,
    [
        "每周 3 次代码学习，每次 2—3 小时；其余碎片时间用于日语 N2 备考。",
        "项目本身就是日语学习的一部分：整理语法条目、写例句的过程直接服务备考。",
        "时间不足时优先保主线（阶段二深度 + 阶段四落地），进阶/高阶内容降级为 README 迭代计划。",
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "9  面试准备要点", level=1)

add_heading_cn(doc, "9.1  项目讲述话术（升级版，30 秒结构）", level=2)
add_para_cn(
    doc,
    "初版的话术是一段流水账，把技术栈报了一遍。但面试官要听的不是你用了什么，"
    "而是你在关键节点上做过什么判断。改用下面的三句话结构：",
    bold=True,
)
add_bullets(
    doc,
    [
        "【什么问题】具体到一个场景。例：“中文用户问‘表示虽然的语法’，系统总是召回形式上相近"
        "但意思无关的条目，L2 层中文意图查询的 Hit@1 只有 38%。”",
        "【什么选择】例：“我对比了本地 bge-m3 和中文单语 embedding，前者在中文意图查询上 MRR 从 "
        "0.41 提到 0.68；又用日语分词后的 BM25 做混合检索，L3 辨析类查询 Recall@3 再提 12 个点。”",
        "【结果与局限】例：“最终测试集 Hit@1 61%、MRR 0.73。局限是知识库只有 N2 语法，"
        "跨到 N1 时召回明显下降，下一步做分级索引。”",
    ],
)
add_para_cn(
    doc,
    "关键点：主动说局限，比被追问出来再承认，给人的感觉完全不同。主动说说明你对项目有清醒认识；"
    "被问出来说明你在遮掩。",
    bold=True,
)

add_heading_cn(doc, "9.2  贯穿主线的话术（保留初版，作为长版本）", level=2)
add_para_cn(
    doc,
    "“我先做了 N2 日语语法 RAG 助手，V0 纯手写向量检索与 Cross-Encoder 重排序，"
    "解决中文查询日文知识库的跨语言召回问题，并用 Hit@1/Recall@3/MRR 和 7 组消融实验量化评估；"
    "随后 V1 用 LangChain 重构实现混合检索；再手写原生 ReAct 理解智能体循环；"
    "最后在 LangGraph 中将 RAG 封装为 Tool，扩展多个专用工具，实现能自主检索、辨析语法、"
    "生成练习题的日语备考 Agent。全程复用同一套 N2 语法数据集。”",
)

add_heading_cn(doc, "9.3  高频问题清单（升级版）", level=2)
add_table_cn(
    doc,
    ["问题", "你的准备方向"],
    [
        ("RAG 完整链路、chunk 调参、幻觉如何缓解", "用你 E5 组的分块消融数据回答，不要背通用答案"),
        ("你为什么不直接用 BM25 / 只用向量检索？", "用 E2、E3 组数据回答，说明日语分词为什么是前提"),
        ("重排序到底有没有用？", "用 E4 组数据回答，并说清什么情况下增益有限"),
        ("你用过什么模型、为什么选它？", "本地 bge-m3 vs 中文单语 vs 托管 API 的三方对比（E1/E6）"),
        ("LangChain 与 LangGraph 的区别", "组件库 vs 有状态图编排，结合你重构时丢掉的控制权来讲"),
        ("Agent 如何实现流式输出、对话历史如何持久化", "astream_events + RunnableWithMessageHistory / checkpoint"),
        ("Function Calling 解析失败如何排查", "结合阶段一写过的 tool_calls 解析经历"),
        ("不依赖框架如何实现一个简单 Agent", "阶段三手写 ReAct 的轨迹截图"),
        ("【新增】你的项目最大的失败案例是什么？", "bad case 归因分布图 + 你是怎么定位到根因的"),
        ("【新增】如果知识库扩到 10 万条，你的方案哪里会先崩？", "索引构建时间、检索延迟、召回质量、成本，四条分别说"),
        ("【新增】这个项目上线了吗？有多少人用？", "诚实回答单机 Demo，但补充服务化与压测数据；不要编造用户量"),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "10  附录", level=1)

add_heading_cn(doc, "10.1  技术栈清单", level=2)
add_table_cn(
    doc,
    ["级别", "技术", "用途"],
    [
        ("P0 必学", "Python、requests、pydantic、python-dotenv、tiktoken", "全流程基础"),
        ("P0 必学", "sentence-transformers（bge-m3）、bge-reranker-v2-m3", "向量化与重排序，跨语言检索核心"),
        ("P0 必学", "FAISS 或 Chroma、余弦/RRF 融合", "向量检索与混合召回"),
        ("P0 必学", "FastAPI、异步、Docker", "服务化，这是应用岗的核心考察点"),
        ("P0 必学", "fugashi + unidic-lite", "日语分词，混合检索的前提"),
        ("P0 必学", "LangChain 1.x、LangGraph、langchain-huggingface", "框架层提速（不引入仍是 alpha 的 langchain-community）"),
        ("P0 必学", "Gradio", "演示界面"),
        ("P1 选学", "RAGAS、LangSmith、locust", "评测自动化与压测，加分项"),
        ("P1 选学", "pdfplumber / PyMuPDF", "PDF 教材导入"),
        ("P2 暂不学", "微调、LoRA、K8s、复杂前端", "避免跑偏"),
    ],
)
add_para_cn(
    doc,
    "本机环境实测（决定了上表怎么落地，详见《N2-Grammar-Companion 版本规划书》2.1~2.4）："
    "RTX 4060 Laptop 8GB 显存；PyTorch 当前是 CPU 版，需在独立 venv 中升级 CUDA（cu126/cu128 "
    "均有 cp314 wheel）；内存 15.7GB 已用约 89%，模型必须 fp16 + 按需加载；"
    "C 盘仅剩 11.4GB，HF_HOME 必须改到 E 盘；Python 3.14 无需降级，关键包均有对应 wheel。",
    bold=True,
)

add_heading_cn(doc, "10.2  你的隐藏优势：Java 背景（初版低估了这点）", level=2)
add_para_cn(
    doc,
    "初版把 Java 只写在“兜底方案”里，当成退路。这是低估。实际情况是：",
    bold=True,
)
add_bullets(
    doc,
    [
        "企业级 AI 应用落地大量使用 Java 技术栈（Spring AI、LangChain4j），"
        "金融、制造、传统行业的 AI 岗尤其明显。",
        "“Java 后端 + Python AI 应用”的双栈组合，比纯 Python 转行的人更稀缺，"
        "因为你自带工程素养：分层设计、异常体系、日志规范、接口设计。",
        "所以正确策略是：Python 路线为主，但在简历里明确写出 Java 后端能力，"
        "让面试官看到你不是“只会调 API 的人”。",
        "如果 Python 方向确实卡住，切换到 Spring AI / LangChain4j 是平级选项而不是降级退路；"
        "相关岗位数量少于 Python 方向，但竞争也小。",
    ],
)
add_para_cn(
    doc,
    "建议在简历技能栏写：Java（后端开发基础扎实）+ Python（AI 应用开发，已完成 RAG/Agent 项目）。"
    "这个组合本身就是差异化。",
    bold=True,
)

add_heading_cn(doc, "10.3  没有实习经历，用什么替代", level=2)
add_para_cn(
    doc,
    "实习的价值本质是“证明有人愿意付钱让你干活”。没有实习，就用可验证的产出替代：",
)
add_table_cn(
    doc,
    ["替代物", "具体做法", "说服力"],
    [
        ("在线 Demo", "部署一个可访问的链接或录制演示视频", "最高：点得开就是硬证据"),
        ("评测报告", "evaluation/report.md 放进仓库，含消融矩阵与 bad case 分析", "很高：数字和结论假不了"),
        ("技术博客", "把跨语言召回、日语分词、消融实验写成文章发出去", "很高：写得出细节的人骗不了人"),
        ("开源 PR", "给用到的库提修复或补文档、补测试", "中等：证明能读别人的代码"),
        ("项目演进主线", "RAG → ReAct → Agent 的同业务演进", "中等：证明有长期思考，不是拼凑 Demo"),
    ],
)
add_para_cn(
    doc,
    "最后一句实话：这份规划的目标是产出“一到两个能讲得深的应用项目”。"
    "能不能拿 offer，最终不取决于你做了多少功能，而取决于你能不能对其中一个项目，"
    "把每一个“为什么”和“代价是什么”讲清楚。",
    bold=True,
)

doc.save(OUT_PATH)
print(f"[OK] 已生成：{OUT_PATH}")
