# -*- coding: utf-8 -*-
"""
生成《N2-Grammar-Companion 版本规划书》（修订版 v2）

相比初版的修订要点见文档第一章。
依赖：python-docx
运行：py -3.14 generate_n2_plan.py
输出：与本脚本同目录的 N2_Grammar_Companion_Plan.docx
"""

import os

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(OUT_DIR, "N2_Grammar_Companion_Plan.docx")

FONT = "微软雅黑"
MONO = "Consolas"
GREY = RGBColor(0x60, 0x60, 0x60)
RED = RGBColor(0xC0, 0x30, 0x30)
BLUE = RGBColor(0x1F, 0x4E, 0x79)


# --------------------------------------------------------------------------
# 排版辅助
# --------------------------------------------------------------------------
def set_cn_font(run, font_name=FONT):
    """设置中西文字体，避免中文显示成方框。"""
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

title = doc.add_heading("N2-Grammar-Companion 版本规划书", 0)
title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
for run in title.runs:
    set_cn_font(run)
    run.font.size = Pt(24)

subtitle = doc.add_paragraph("日语 N2 智能查询助手 —— V0 手搓版 + V1 LangChain 版（修订版 v2）")
subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
for run in subtitle.runs:
    set_cn_font(run)
    run.font.size = Pt(14)
    run.font.color.rgb = GREY

lead = doc.add_paragraph(
    "一句话定位：面向 N2 备考者的日语语法检索助手，重点解决“中文提问 → 日文语法库”的跨语言召回，"
    "并用可复现的评测数据量化每一次优化决策。"
)
lead.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
for run in lead.runs:
    set_cn_font(run)
    run.font.size = Pt(11)
    run.font.color.rgb = GREY

doc.add_paragraph()

# ==========================================================================
add_heading_cn(doc, "〇、本版修订说明（v1 → v2）", level=1)
add_para_cn(
    doc,
    "初版是一份“功能完整”的施工图，但深度停留在教程级：数据量太小、评测不足以支撑结论、"
    "最能体现工程能力的部分被写进了“局限”。本版针对这三点做了结构性调整。",
)
add_table_cn(
    doc,
    ["#", "修订点", "初版", "修订版", "为什么改"],
    [
        (
            "1",
            "Embedding 选型",
            "2.1 表写“调用 Embedding 接口”，3.1 表写 sentence-transformers，自相矛盾",
            "定死默认方案 A（本地 bge-m3），给出方案 B（托管 API）与切换规则",
            "选型不确定就没法写 requirements、没法估计下载体积和启动时间",
        ),
        (
            "2",
            "数据规模",
            "80 条语法 JSON 既当检索库又当评测集",
            "拆成“文档集 3000+ chunk”与“黄金评测集 60 条 query”，两者分离",
            "80 条数据下向量检索没有意义（关键词匹配就够），技术点体现不出来",
        ),
        (
            "3",
            "评测体系",
            "20 条测试集，只报 Recall@3",
            "60 条四层测试集 + Hit@1/MRR/拒答准确率 + 消融实验矩阵 + bad case 归因表",
            "“80 条库里 Recall@3 ≥70%”经不起追问；消融实验是实习生简历里最稀缺的证据",
        ),
        (
            "4",
            "工程化",
            "FastAPI / PDF 解析 / 规模扩展全部列在“局限与迭代计划”",
            "FastAPI 服务化 + 并发压测提升为必做里程碑 M6，局限只写真正没做的",
            "主动交白卷是最亏的写法：这三条恰恰是面试官最想听的工程能力",
        ),
        (
            "5",
            "目录命名",
            "2.5 写 v0_handcrafted/，3.4 又写 02_mini_native_rag_jp/，与仓库实际不符",
            "统一为 v0/ v1/ evaluation/ api/ data/（与仓库现状一致）",
            "命名不统一会让 import 路径、README、部署脚本全都对不上",
        ),
        (
            "6",
            "LangChain API",
            "ConversationBufferMemory / JSONLoader / 裸 BM25Retriever",
            "RunnableWithMessageHistory 或 LangGraph checkpoint；自写 loader；BM25 接日语分词",
            "ConversationBufferMemory 在新版已移除，照抄教程会直接跑不起来",
        ),
        (
            "7",
            "排期单位",
            "按“每日任务”排（Day 1 ~ Day 10）",
            "改为里程碑 M1~M8，按“次”计量（每次 2~2.5 小时）",
            "每天一模块不现实，且一次没跟上整份计划就作废",
        ),
        (
            "8",
            "日语场景深化",
            "无",
            "新增第八章：日语分词、读音标注、近义网络、易混辨析",
            "这是本项目唯一的真差异化，通用 RAG 教程里没有，面试官一听就记住",
        ),
        (
            "9",
            "面试表达",
            "只列了“亮点”名词",
            "第十一章给出 30 秒叙述结构与决策叙事模板",
            "亮点是名词，面试官要听的是判断过程；同样的项目，表达决定成败",
        ),
        (
            "10",
            "环境准备（本次补充）",
            "无，选型建立在通用假设上",
            "2.1 / 2.2 / 2.3 改写为本机实测结论，并新增 2.4 开工准备清单",
            "决策必须建立在这台机器的实际能力上：torch 是 CPU 版、内存吃紧、C 盘空间不足、"
            "langchain-community 在 1.x 上仍是 alpha —— 这些都会直接改变做法",
        ),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "一、项目定位与差异化", level=1)
add_table_cn(
    doc,
    ["维度", "说明"],
    [
        ("目标用户", "N2 备考者（包括你自己）"),
        ("核心场景", "输入“表示‘虽然’的语法有哪些”，返回 N2 语法 + 接续 + 读音 + 例句 + 出处"),
        ("差异化", "不做通用 PDF 问答，聚焦日语语法垂直场景；解决中文提问检索日文语料这一具体问题"),
        (
            "技术看点",
            "跨语言召回、日语分词下的混合检索、重排序消融实验、可复现评测、服务化落地",
        ),
        ("双重价值", "写项目的同时整理 N2 语法知识，项目直接服务于备考"),
    ],
)

# ==========================================================================
add_heading_cn(doc, "二、开工前必须定死的三个决策（含本机实测）", level=1)
add_para_cn(
    doc,
    "初版最大的问题不是内容少，而是有互相矛盾的表述，而且选型建立在通用假设上。"
    "这三件事在写第一行代码前必须定下来，且必须按这台机器的实际能力来定，"
    "否则 requirements、目录结构和排期都会返工。",
    bold=True,
)

add_heading_cn(doc, "2.1 决策一：Embedding 与重排序选型 → 结论：走本地模型", level=2)
add_para_cn(
    doc,
    "本机实测（开发机）：RTX 4060 Laptop 8GB 显存，驱动 572.70；内存 15.7GB（当前已用约 89%、"
    "可用约 1.6GB）；C 盘剩余 11.4GB、E 盘剩余 93GB；Python 3.14.4；已装 PyTorch 2.13.0+cpu。",
    bold=True,
)
add_table_cn(
    doc,
    ["", "方案 A（已选定）本地模型", "方案 B（保留为对照）托管 API"],
    [
        ("组成", "sentence-transformers 加载 BAAI/bge-m3（fp16）；重排序 BAAI/bge-reranker-v2-m3", "阿里百炼 text-embedding-v4 + gte-rerank-v2（以控制台当前可用型号为准）"),
        ("优点", "离线可跑、免费、可复现；8GB 显存可同时驻留两个模型（约 2.5GB）；面试可现场演示", "零下载、启动快；不吃本机显存与内存"),
        ("代价", "首次下载约 2~3GB；未升级 CUDA 前只能走 CPU，冷启动与批量编码较慢", "依赖网络与额度；断网无法演示；调用成本需自己记账"),
        ("本机结论", "选它。显存不是瓶颈，内存才是", "保留为 E6 组消融实验的对照组"),
    ],
)
add_para_cn(doc, "选方案 A 之前必须先解决三件事（按优先级）：", bold=True)
add_table_cn(
    doc,
    ["#", "问题（实测）", "处理方式"],
    [
        ("1", "PyTorch 装的是 CPU 版（2.13.0+cpu），4060 完全用不上", "先按 CPU 跑通 M1~M4，不要卡在第一周；把“升级 CUDA 版 torch”单独列为 M5 附近的小任务，在独立 venv 里做"),
        ("2", "C 盘只剩 11.4GB，而模型缓存默认写在 C 盘", "把缓存改到 E 盘：环境变量 HF_HOME 与 TRANSFORMERS_CACHE 指向 E:\\ai-agent-study\\.hf_cache"),
        ("3", "内存 15.7GB 已用 89%，两模型 + Gradio + 浏览器极易 OOM", "模型一律 fp16；按需加载（检索时才加载 embedder、重排时才加载 reranker）；开发时关掉 Steam 与多余浏览器标签"),
    ],
)
add_para_cn(
    doc,
    "关于 CUDA：实测 PyTorch 官方源上 cu126 / cu128 / cu129 均提供常规 cp314 的 Windows wheel"
    "（例如 torch-2.9.1+cu126-cp314-cp314-win_amd64.whl），所以升级可行。但注意这可能把 torch 从 "
    "2.13.0 回退到 2.9.x —— 不影响使用，只是必须放在独立 venv 中操作，避免污染当前全局环境。"
    "另外 Python 3.14 无需降级：faiss-cpu、fugashi 均有 cp314 wheel，sentence-transformers 与 "
    "transformers 是纯 Python 包。",
)
p = doc.add_paragraph()
run = p.add_run(
    "关键提醒：不要用 bge-large-zh 之类的中文单语模型。它是纯中文模型，对日文召回天然差，"
    "而“中文提问检索日文语料”正是本项目要解决的核心问题本身。它在本项目里的唯一用途，"
    "是作为 E1 组的“故意选错的基线”，用数据证明跨语言这个问题真实存在。"
)
run.bold = True
run.font.color.rgb = RED
set_cn_font(run)

add_heading_cn(doc, "2.2 决策二：目录与命名统一", level=2)
add_para_cn(
    doc,
    "仓库实际目录是 v0/ 和 v1/，初版文档里却写成了 v0_handcrafted/ 与 v1_langchain/，"
    "还混用了 02_mini_native_rag_jp 和 02_mini-native-rag-jp 两种写法。全部统一为仓库现状，"
    "以本文件第四章的目录结构为准。",
)
add_para_cn(doc, "附加要求：v0/ 与 v1/ 的文件名必须一一对应。", bold=True)
add_code_cn(
    doc,
    """v0/loader.py    ←→  v1/loader.py
v0/chunker.py   ←→  v1/chunker.py
v0/embedder.py  ←→  v1/embedder.py
v0/retriever.py ←→  v1/retriever.py
v0/generator.py ←→  v1/generator.py""",
)
add_para_cn(
    doc,
    "好处：diff v0/retriever.py v1/retriever.py 就是天然的“手搓 vs 框架”对比材料，"
    "README 里那张对比表可以基于真实 diff 来写，而不是靠回忆。V1 一旦自由发挥，"
    "两个版本就无法逐文件对照，对比表也就失效了。",
)

add_heading_cn(doc, "2.3 决策三：依赖版本与新版 LangChain 的坑", level=2)
add_para_cn(
    doc,
    "本机实测已装：langchain 1.3.18、langchain-core 1.6.1、langgraph 1.2.11、langchain-openai 1.6.0、"
    "gradio 6.26.0、fastapi 0.141.1。也就是说本项目处在 LangChain 1.x 时代，"
    "网上绝大多数教程（0.1~0.3 时期）对不上。",
    bold=True,
)
add_para_cn(
    doc,
    "最关键的一条实测结论：langchain-community 在 1.x 线上最新版是 1.0.0a1，仍属 alpha。"
    "而初版想用的便利检索器（FAISS / BM25Retriever / HuggingFaceEmbeddings / EnsembleRetriever）"
    "大半都在这个包里。因此 V1 的正确策略是：检索层保持自研，只让框架负责编排与状态管理。",
    bold=True,
)
add_table_cn(
    doc,
    ["初版想用", "1.x 下的问题", "修订版做法"],
    [
        ("ConversationBufferMemory", "已从主包移除（旧组件迁往 langchain-classic）", "langgraph.checkpoint（已装 4.2.0）或 RunnableWithMessageHistory"),
        ("JSONLoader + jq schema", "位于 community 包且维护弱，自定义 schema 比手写还长", "自己写 15 行 loader（json.load + 拼 chunk_text）"),
        ("HuggingFaceEmbeddings", "位于 community 包", "改用官方 partner 包 langchain-huggingface（1.2.2，稳定线）"),
        ("FAISS 向量库封装", "位于 community 包", "V0 已手写 FAISS 封装，V1 直接复用，不引入 alpha 依赖"),
        ("BM25Retriever", "位于 community 包，且默认按空格切词，日语场景等于失效", "自己写：rank-bm25 + fugashi 分词，约 30 行胶水代码"),
        ("EnsembleRetriever", "位于 community 包，且默认平均融合未必优于单路", "自己写 RRF 融合（约 15 行），权重用评测数据来选"),
    ],
)
add_para_cn(doc, "这不是妥协，而是一个更好的叙事。V1 的定位从“我用框架搭了个 RAG”变成：", bold=True)
p = doc.add_paragraph()
run = p.add_run(
    "「框架负责编排和状态管理，检索层我保持自研 —— 因为 1.x 的 community 检索器仍处于 alpha，"
    "且其 BM25 对日语分词支持不足。」"
)
run.bold = True
run.font.color.rgb = BLUE
set_cn_font(run)
add_para_cn(doc, "另外两个版本坑：", bold=True)
add_bullets(
    doc,
    [
        "transformers 最新为 5.9.0（大版本），与网上大量 4.x 教程的 API 不一致，照抄会报错。",
        "装完立刻执行 pip freeze > requirements.txt 钉死版本 —— 1.x 换代很快，不锁版本两周后就复现不了。",
        "langchain-classic（1.0.8）是旧组件迁移地，新代码不要用它，只在对照旧教程时参考。",
    ],
)

add_heading_cn(doc, "2.4 开工准备清单（决策之外，但必须先做）", level=2)
add_table_cn(
    doc,
    ["#", "事项（均为本机实测）", "命令 / 做法"],
    [
        ("1", "建独立 venv —— 当前所有包都装在 Python 3.14 全局环境里", "py -3.14 -m venv .venv；然后 .venv/Scripts/Activate.ps1"),
        ("2", "把模型缓存指向 E 盘，避免撑爆只剩 11.4GB 的 C 盘", "设置 HF_HOME 与 TRANSFORMERS_CACHE 为 E:\\ai-agent-study\\.hf_cache"),
        ("3", "确认 pip 镜像（已确认是阿里云镜像，无需改动）", "pip config list → global.index-url = mirrors.aliyun.com"),
        ("4", "装依赖并锁版本", "pip install sentence-transformers faiss-cpu rank-bm25 fugashi unidic-lite langchain-huggingface；然后 pip freeze > requirements.txt"),
        ("5", "整理 workspace 重复目录", "E:\\ai-agent-study 下同时存在 02_mini-native-rag-jp 与 02_rag_project，需确认哪个是正式目录并清理另一个"),
        ("6", "清理空占位文件", "v0\\001.docx 与 v1\\002.docx 均为 0 字节，删除或开始使用"),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "三、数据资产设计（核心资产，先做）", level=1)
add_para_cn(
    doc,
    "初版把“整理 80 条语法 JSON”当成 Day 1 任务，并同时用它当检索库和评测集。"
    "这有两个问题：一是 80 条规模下向量检索没有意义；二是用检索库自己去考自己，指标必然虚高。"
    "修订版把数据拆成两层。",
    bold=True,
)

add_heading_cn(doc, "3.1 两层数据，职责分离", level=2)
add_table_cn(
    doc,
    ["数据层", "文件", "规模", "作用", "注意"],
    [
        ("文档集（检索对象）", "data/n2_docs.json", "3000+ chunk", "被检索的语料，决定检索这个技术点有没有意义", "每条语法拆成多个 chunk（释义 / 接续 / 每个例句 / 辨析）"),
        ("黄金评测集", "evaluation/gold_set.json", "60 条 query", "评测检索质量，人工复核过期望答案", "必须与文档集分离，且不参与调参"),
        ("开发集 / 测试集", "由黄金集按 4:6 划分", "24 / 36 条", "调 chunk size、权重用开发集，最终只报测试集", "防止反复调参把测试集调过拟合"),
    ],
)

add_heading_cn(doc, "3.2 文档集 schema（相比初版新增字段）", level=2)
add_code_cn(
    doc,
    """{
  "id": "n2_001",
  "grammar": "〜ばかりに",
  "reading": "ばかりに",                     // 新增：读音，用于展示与发音
  "meaning_cn": "正因为...才...（表示原因导致坏结果）",
  "usage": "动词/形容词た形 + ばかりに",
  "tags": ["原因", "消极结果", "N2核心"],     // 新增：功能分类，支撑“表示原因的语法有哪些”这类查询
  "examples": [
    {"jp": "彼の話を信じたばかりに、大損した。",
     "cn": "正因为信了他的话，才损失惨重。",
     "reading": "かれのはなしをしんじたばかりに、たいそんした。"}   // 新增
  ],
  "similar": ["〜せいで", "〜おかげで"],
  "contrast": "「〜おかげで」接好结果，「〜ばかりに」只接坏结果。",   // 新增：辨析
  "level": "N2",
  "source": "N2语法书 P.xx"                   // 新增：出处，支撑引用溯源
}""",
)

add_heading_cn(doc, "3.3 chunk 拼装策略", level=2)
add_para_cn(
    doc,
    "检索用的文本不是把整个 JSON 塞进去，而是按粒度拆开，让召回更精准：",
)
add_bullets(
    doc,
    [
        "chunk 1（释义块）：grammar + reading + meaning_cn + usage + tags",
        "chunk 2~n（例句块）：每个例句单独成块，附带所属语法 id",
        "chunk m（辨析块）：contrast + similar 组成的对比说明",
        "每个 chunk 都带 parent_id，命中后可以回溯到完整语法条目 —— 这就是“引用溯源”的实现基础。",
    ],
)
add_para_cn(
    doc,
    "这一处改动同时解决了两件事：文档量从 80 涨到 3000+，向量检索变得有意义；"
    "chunk 粒度可控，后面的 chunk size 消融实验才有东西可比。",
)

add_heading_cn(doc, "3.4 语料来源与清洗", level=2)
add_bullets(
    doc,
    [
        "主源：你手上的 N2 语法书 / 教材，整理成结构化 JSON（人工校对，这是黄金集的质量保证）。",
        "补充：JLPT 官方样题与真题的题干句、青空文库的例句（注意版权，仅本地演示使用，不公开分发）。",
        "大规模补充（可选，用于把文档集做到 1 万+）：PDF 教材解析，练习 pdfplumber / PyMuPDF 抽文本、按标题切分。",
        "清洗必做：去页眉页脚、去全角半角混排噪声、按 grammar id 去重、统一「〜」与「～」写法。",
        "数据工程是真实 RAG 项目里最耗时的部分（往往占 60% 以上），把它写进简历比多写一个功能更有价值。",
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "四、V0 原生手写版（不依赖 LangChain）", level=1)
add_para_cn(
    doc,
    "技术原则：纯原生 Python 实现，复用阶段一的全部能力。手写的目的是拿到“为什么”的答案，"
    "而不是证明自己能手搓 —— 这一条决定了后面 V1 对比时你有话可说。",
    bold=True,
)

add_heading_cn(doc, "4.1 模块拆分", level=2)
add_table_cn(
    doc,
    ["模块", "文件", "功能", "复用技能", "commit 示例"],
    [
        ("数据加载", "loader.py", "读取 n2_docs.json，构造文档集", "with open、json.load", "feat: N2知识库加载"),
        ("文档切分", "chunker.py", "按“释义/例句/辨析”三粒度切 chunk 并保留 parent_id", "字符串处理、列表推导", "feat: 三粒度分块与父子关系"),
        ("向量化", "embedder.py", "加载 bge-m3，批量编码 + L2 归一化", "异常捕获、批处理", "feat: bge-m3向量化"),
        ("索引构建", "indexer.py", "FAISS 索引 + metadata 同序落盘", "list/dict、pickle", "feat: 向量索引构建与持久化"),
        ("检索", "retriever.py", "余弦相似度 Top-K，附带相似度分数", "排序、列表推导", "feat: 原生向量检索"),
        ("重排序", "reranker.py", "bge-reranker-v2-m3 二次打分，可开关", "模型加载、缓存", "feat: CrossEncoder重排序"),
        ("生成", "generator.py", "命中 chunk 注入 Prompt，要求标注出处、无据拒答", "Prompt 工程", "feat: RAG问答主链路"),
        ("评测", "evaluation/run_eval.py", "跑测试集，输出 Hit@1 / Recall@3 / MRR", "json、统计", "feat: 检索评测脚本与基线数据"),
        ("工程打磨", "utils/", "logging 双输出、tiktoken 计数、上下文压缩", "tiktoken、logging", "feat: 日志与token管理"),
        ("服务化", "api/main.py", "FastAPI 接口 + 流式输出 + 超时重试", "FastAPI、异步", "feat: FastAPI服务化接口"),
        ("主入口", "main.py", "命令行交互", "input、while", "feat: 命令行入口"),
        ("界面", "app.py", "Gradio 网页演示，展示答案与引用来源", "Gradio", "feat: Gradio演示页面"),
    ],
)

add_heading_cn(doc, "4.2 目录结构（统一后）", level=2)
add_code_cn(
    doc,
    """02_mini-native-rag-jp/
├── v0/
│   ├── main.py              # 命令行入口
│   ├── app.py               # Gradio 演示
│   ├── loader.py
│   ├── chunker.py           # 新增
│   ├── embedder.py
│   ├── indexer.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── generator.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── token_counter.py
│   │   └── json_cleaner.py
│   ├── index/               # faiss.index + metadata.pkl（同序保存，gitignore）
│   └── requirements.txt
├── v1/                      # LangChain 重构版，文件结构与 v0 对齐，便于逐文件对照
├── api/                     # FastAPI 服务（v0/v1 共用）
│   ├── main.py
│   └── Dockerfile
├── data/
│   ├── n2_docs.json         # 文档集（检索对象）
│   └── raw/                 # 原始教材/PDF，gitignore
├── evaluation/
│   ├── gold_set.json        # 60 条黄金评测集
│   ├── run_eval.py
│   ├── ablation.py          # 消融实验
│   └── report.md            # 评测报告（简历里的数字都从这里来）
└── README.md""",
)

add_heading_cn(doc, "4.3 里程碑（替代初版的“每日任务”）", level=2)
add_para_cn(
    doc,
    "按“次”计量，一次 = 2~2.5 小时。V0 部分共约 12 次；加上第五章 V1 的 6 次，"
    "理想工期约 6 周。实际预留见第九章。",
    color=GREY,
)
add_table_cn(
    doc,
    ["里程碑", "内容", "完成标准（可验证）", "次数"],
    [
        ("M1 数据资产", "文档集 3000+ chunk + 黄金评测集 60 条", "两份 json 通过 schema 校验；评测集人工复核过一遍", "2"),
        ("M2 检索链路", "loader / chunker / embedder / indexer / retriever", "CLI 输入中文问句能召回 Top-5，索引落盘后重启结果一致", "2"),
        ("M3 生成链路", "Prompt + LLM 调用 + 引用溯源 + 无据拒答", "答案带出处；问知识库外内容时明确拒答而非编造", "1"),
        ("M4 评测基线", "run_eval.py + 四层测试集", "report.md 出现第一版 Hit@1 / Recall@3 / MRR 基线", "1"),
        ("M5 重排序 + 消融", "接入 reranker，跑完整消融矩阵", "消融表有结论：哪个改动有效、有效多少", "2"),
        ("M6 服务化", "FastAPI + 流式 + 超时重试 + Docker", "本地 URL 可访问；20 并发压测不崩、有耗时日志", "2"),
        ("M7 演示界面", "Gradio 展示答案、引用卡片、耗时与 token 成本", "可对着屏幕演示完整一轮问答", "1"),
        ("M8 文档复盘", "README + 架构图 + bad case 分析 + 技术博客", "仓库外人看得懂；博客能贴出链接", "1"),
    ],
)

add_heading_cn(doc, "4.4 若时间不够：砍什么、保什么", level=2)
add_para_cn(doc, "这是初版完全没有、但实际最重要的一节。", color=GREY)
add_table_cn(
    doc,
    ["优先级", "内容", "理由"],
    [
        ("绝不能砍", "数据规模、评测体系、服务化、bad case 分析", "这四项是“教程级”和“能聊 20 分钟”的分界线，缺一项简历就退回同质化池子"),
        ("可以简化", "重排序（只做离线对比，不接生产链路）", "消融数据本身就有价值，不一定非要上线"),
        ("可以砍", "流式输出、Gradio 美化、PDF 大批量解析", "体验层的东西，面试官几乎不会追问"),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "五、V1 LangChain 重构版", level=1)
add_para_cn(
    doc,
    "技术原则：用 LangChain 重构同一业务，重点理解框架封装了什么。保留 V0 作为对照，"
    "并在 README 里明确写“什么场景该用手写、什么场景该用框架”。",
    bold=True,
)

add_heading_cn(doc, "5.1 V0 vs V1 对比（修正版）", level=2)
add_table_cn(
    doc,
    ["维度", "V0（手搓）", "V1（LangChain）"],
    [
        ("数据加载", "手写 json.load + chunk 拼装", "自写 loader 产出 Document（不再用 JSONLoader）"),
        ("Embedding", "sentence-transformers 加载 bge-m3", "HuggingFaceEmbeddings 包装同一模型（向量可比）"),
        ("向量存储", "手写 FAISS + metadata 同序落盘", "FAISS.from_documents() 自动管理映射"),
        ("检索", "单路稠密检索", "混合检索：BM25（日语分词）+ 稠密 + 加权融合"),
        ("重排序", "手写 CrossEncoder 打分", "ContextualCompressionRetriever 组合"),
        ("对话记忆", "无", "RunnableWithMessageHistory（不用已移除的 ConversationBufferMemory）"),
        ("流式输出", "无", "astream_events，逐字返回"),
        ("代码量", "约 400 行（含服务化）", "约 250 行（框架省掉的是胶水代码，不是思考）"),
    ],
)
add_para_cn(
    doc,
    "注意最后一行：V1 代码更少，但省掉的是胶水，不是判断。面试时要说清楚“框架替我省了什么、"
    "又让我失去了什么控制权”，这才是这道对比题的标准答案。",
    bold=True,
)

add_heading_cn(doc, "5.2 V1 新增能力", level=2)
add_bullets(
    doc,
    [
        "混合检索：BM25（fugashi 分词）+ 稠密检索，用加权 RRF 融合；权重由评测数据决定，不用默认值。",
        "多轮对话记忆：支持追问“那「〜ものの」和「〜にもかかわらず」有什么区别？”。",
        "流式输出：astream_events 逐字返回，Gradio 对接。",
        "与 V0 共用同一份数据、同一套评测集，指标可直接对比 —— 这是“重构”而非“重做”的证明。",
    ],
)

add_heading_cn(doc, "5.3 V1 里程碑", level=2)
add_table_cn(
    doc,
    ["里程碑", "内容", "完成标准", "次数"],
    [
        ("N1 复刻", "用 LangChain 复刻 V0 检索链路", "同一测试集上指标与 V0 持平（证明重构无回退）", "2"),
        ("N2 混合检索", "加日语分词 BM25 + RRF，调权重", "混合检索指标超过单路稠密，且有权重对比数据", "2"),
        ("N3 记忆与流式", "多轮记忆 + 流式输出", "能连续追问 3 轮不丢上下文", "1"),
        ("N4 对比报告", "V0/V1 全指标对照 + 结论", "report.md 有结论段：各自适合什么场景", "1"),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "六、评测体系（本版重点重写）", level=1)
add_para_cn(
    doc,
    "初版只有“20 条测试集 + Recall@3 ≥ 70%”。问题在于：在 80 条的小库上，"
    "随机猜 Top-3 都有 3.75% 命中，70% 这个数字既没有区分度、也经不起追问。"
    "而且一个 query 对应多个正确答案时，“算命中”的判定规则没有定义。",
    bold=True,
)

add_heading_cn(doc, "6.1 指标体系", level=2)
add_table_cn(
    doc,
    ["指标", "定义", "为什么需要它", "目标"],
    [
        ("Hit@1", "Top-1 是否命中", "最贴近用户体验：第一个答案对不对", "≥ 55%"),
        ("Recall@3", "Top-3 中是否命中", "初版唯一指标，保留作为对照", "≥ 80%"),
        ("MRR@10", "首个正确结果的排名倒数均值", "对排序敏感，是检索优化的主指标", "≥ 0.70"),
        ("拒答准确率", "知识库外问题正确拒答的比例", "直接对应“防幻觉”这个业务价值", "≥ 90%"),
        ("端到端正确率", "LLM 最终答案是否正确（人工判 30 条）", "检索对 ≠ 答案对，这一步能暴露 Prompt 问题", "≥ 80%"),
        ("P95 延迟", "端到端响应耗时 95 分位", "初版写“<5 秒”，但平均延迟会掩盖长尾", "< 5s"),
    ],
)
add_para_cn(doc, "命中判定规则（初版缺失，必须定义）：", bold=True)
add_bullets(
    doc,
    [
        "一个 query 有多个可接受答案时，命中任一即算命中（Hit 口径），同时在报告里附“全部命中率”作为严格口径。",
        "判定基于 grammar id，不基于文本相似度，避免人工打分带来的主观性。",
        "测试集按 4:6 划分开发集与测试集，调参只用开发集，最终结果只报测试集。",
    ],
)

add_heading_cn(doc, "6.2 四层测试集设计（60 条）", level=2)
add_table_cn(
    doc,
    ["层级", "类型", "示例 query", "考察点", "条数"],
    [
        ("L1", "直接点名", "「〜ばかりに」是什么意思？", "基础检索能力，应该接近满分", "15"),
        ("L2", "中文意图", "表示“正因为…才…”的语法有哪些？", "跨语言召回，本项目核心难点", "20"),
        ("L3", "近义辨析", "「〜ものの」和「〜にもかかわらず」有什么区别？", "同时召回多条并正确对比，考察多跳", "15"),
        ("L4", "应拒答", "N1 的「〜ずにはおかない」怎么用？", "知识库外问题，考察防幻觉", "10"),
    ],
)
add_para_cn(
    doc,
    "分层的好处：每一层对应一个具体的技术能力，指标一掉你立刻知道是哪个环节退化了。"
    "这也是初版“20 条混在一起测”做不到的。",
)

add_heading_cn(doc, "6.3 消融实验矩阵（简历上最有价值的一张表）", level=2)
add_para_cn(
    doc,
    "同一套测试集，逐个变量替换，每次只动一个因素。这张表是“我做过工程决策”最硬的证据。",
    bold=True,
)
add_table_cn(
    doc,
    ["实验组", "Embedding", "检索方式", "重排序", "chunk 粒度", "预期结论"],
    [
        ("基线", "bge-large-zh（中文单语）", "稠密", "无", "整条 512", "故意选错模型，用数据证明“跨语言”这个问题真实存在"),
        ("E1", "bge-m3", "稠密", "无", "整条 512", "换多语言模型后的提升幅度"),
        ("E2", "bge-m3", "BM25（日语分词）", "无", "整条 512", "纯稀疏在日语语法场景能到什么水平"),
        ("E3", "bge-m3", "混合 RRF", "无", "整条 512", "混合是否优于单路"),
        ("E4", "bge-m3", "混合 RRF", "有", "整条 512", "重排序的增益，L2/L3 层应最明显"),
        ("E5", "bge-m3", "混合 RRF", "有", "三粒度分块", "分块粒度对召回的影响"),
        ("E6", "托管 API embedding", "混合 RRF", "有", "三粒度分块", "本地 vs 云端的性价比对照"),
    ],
)
add_para_cn(
    doc,
    "跑完这 7 组，你手上有 7 行数据、至少 3 个真实结论。面试时任何“你为什么不直接用 X”"
    "的问题，你都能指着表回答。这就是初版和修订版最大的差距。",
)

add_heading_cn(doc, "6.4 bad case 归因表（模板）", level=2)
add_table_cn(
    doc,
    ["query", "期望", "实际召回", "归因分类", "处理"],
    [
        ("表示“虽然”的语法", "ものの / にもかかわらず", "（待填）", "跨语言 / 分词 / 分块 / 同义干扰", "（改了什么都记下来）"),
    ],
)
add_para_cn(
    doc,
    "归因分类固定成四类（跨语言语义偏差、分词或关键词失效、分块切断了必要上下文、同义语法互相干扰），"
    "每次失败都归类，最后你会得到一张分布图 —— “我的检索失败里 60% 是分块问题”"
    "这种句子，比任何技术名词都像做过真项目的人说的。",
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "七、服务化与工程化（初版列为“局限”，本版提升为必做）", level=1)
add_para_cn(
    doc,
    "初版把“未接 FastAPI”写在第八章“项目局限”里。这是个战略性失误：服务化恰恰是应用开发岗"
    "最核心的考察点，把它写成“我没做”，等于主动交白卷。本版提升为必做里程碑 M6。",
    bold=True,
)
add_table_cn(
    doc,
    ["能力", "做法", "面试可讲点"],
    [
        ("接口设计", "POST /ask（同步）、POST /ask/stream（SSE 流式）、GET /health", "为什么流式要单独一个接口，而不是一个接口带参数"),
        ("超时与重试", "LLM 调用设超时 + 指数退避重试 + 熔断兜底", "接口挂了怎么办，降级返回检索结果还是直接报错"),
        ("并发", "异步接口 + 连接池；用脚本压 20 并发", "并发下模型推理是瓶颈，你怎么观测到的"),
        ("成本控制", "记录每次请求的 token 数与预估费用，写进日志", "单次问答成本多少，怎么做缓存降本"),
        ("可观测性", "结构化日志：请求 id、检索耗时、生成耗时、命中 chunk 数", "出问题怎么定位：是检索慢还是模型慢"),
        ("容器化", "Dockerfile，模型权重用 volume 挂载不打进镜像", "为什么模型不进镜像（镜像体积、构建时间）"),
    ],
)
add_para_cn(
    doc,
    "一条硬性要求：项目必须有一个“点得开的链接”。在线 Demo 或录屏演示，"
    "在简历筛选环节的说服力远大于“GitHub 上有 800 行代码”。",
    bold=True,
)

# ==========================================================================
add_heading_cn(doc, "八、日语场景深化（新增，这是你唯一的真差异化）", level=1)
add_para_cn(
    doc,
    "通用 RAG 教程不会教这些，而它们恰好是你作为日语备考者的天然优势。"
    "面试官一天看几十份 RAG 简历，能被记住的往往是这类“只有你真懂这个场景才做得出来”的细节。",
    bold=True,
)
add_table_cn(
    doc,
    ["方向", "做法", "价值"],
    [
        ("日语分词", "fugashi + unidic-lite 给 BM25Retriever 传 preprocess_func", "解决“日语没空格导致关键词检索失效”，是混合检索能生效的前提"),
        ("读音标注", "schema 增加 reading 字段，回答时输出假名", "直接服务 N2 备考，也让答案更像“助教”而不是“搜索引擎”"),
        ("近义网络", "用 similar 字段建语法关系图，支持“和它相近的还有哪些”", "把静态知识库变成有结构的知识图谱，多跳查询的基础"),
        ("易混辨析", "内置高频易混语法对（に/で、ものの/にもかかわらず、ばかりに/せいで）", "对应真实备考痛点，也是最容易做出效果差异的功能"),
        ("敬语与语体", "标注例句的语体（书面/口语/敬语）", "N2 阅读与听力都会考语体，检索时可按语体过滤"),
    ],
)

doc.add_page_break()

# ==========================================================================
add_heading_cn(doc, "九、时间线（里程碑制，替代初版的“8~10 天”）", level=1)
add_para_cn(
    doc,
    "初版写 8~10 天，是按“每天一模块、每模块只是跑通”估的。本版深度上去之后，"
    "按每周 3 次、每次 2~2.5 小时的口径重估：里程碑合计 18 次（理想 6 周），"
    "加上新手常见的返工、模型下载、环境问题，按 40% 缓冲预留，实际排期约 10 周。"
    "这与《AI Agent 应用开发学习总规划》第 8 章完全一致。",
    bold=True,
)
add_table_cn(
    doc,
    ["周次", "里程碑", "理想次数", "产出", "可否投递"],
    [
        ("第 1~3 周", "M1 数据资产、M2 检索链路、M3 生成链路", "5", "文档集 3000+ chunk；CLI 能召回并生成带出处、能拒答的答案", "否"),
        ("第 4 周", "M4 评测基线", "1", "第一版 Hit@1 / Recall@3 / MRR 基线", "✅ 从这里开始投"),
        ("第 5~6 周", "M5 重排序与消融实验", "2", "7 组消融矩阵与结论", "✅"),
        ("第 7 周", "M6 服务化、M7 演示界面", "3", "在线可访问 Demo、并发压测记录", "✅"),
        ("第 8~9 周", "V1 重构 N1~N4", "6", "V0/V1 全指标对照报告", "✅"),
        ("第 10 周", "M8 文档与复盘", "1", "README、架构图、技术博客", "✅"),
        ("缓冲", "新手返工、模型下载、环境问题（按 40% 预留）", "—", "—", "—"),
    ],
)
add_para_cn(
    doc,
    "注意第 4 周这个节点：此时你已经有一个带评测数据的 V0，足以开始投中小厂练手感。"
    "不要把投递推到第 10 周之后 —— 面试反馈本身就是最好的迭代输入。",
    bold=True,
)

# ==========================================================================
add_heading_cn(doc, "十、最终交付物（升级版）", level=1)
add_table_cn(
    doc,
    ["交付物", "说明", "状态"],
    [
        ("data/n2_docs.json", "文档集，3000+ chunk", "必做"),
        ("evaluation/gold_set.json", "60 条分层黄金评测集", "必做"),
        ("evaluation/report.md", "含消融矩阵与 bad case 归因的评测报告", "必做"),
        ("v0/", "手搓版完整代码（含服务化）", "必做"),
        ("v1/", "LangChain 版完整代码", "必做"),
        ("api/", "FastAPI 服务 + Dockerfile", "必做"),
        ("README.md", "架构图、V0/V1 对比、评测结论、局限与迭代", "必做"),
        ("在线 Demo 链接", "可访问的部署地址或演示录屏", "必做"),
        ("技术博客", "把跨语言召回与消融实验写成文章", "强烈建议"),
    ],
)

# ==========================================================================
add_heading_cn(doc, "十一、面试可讲的亮点（附 30 秒叙述结构）", level=1)
add_para_cn(
    doc,
    "初版只列了亮点名词。但面试官要听的不是名词，是判断过程。"
    "同样一段经历，按下面的结构说和按“我用了 RAG 和 LangChain”说，结果完全不同。",
    bold=True,
)
add_para_cn(doc, "30 秒结构（三句话，全是钩子）：", bold=True)
add_bullets(
    doc,
    [
        "【什么问题】具体到一个场景，不要泛泛说“提升了效果”。例：“中文用户问‘表示虽然的语法’，"
        "系统总是召回日文形式相近但意思无关的条目，L2 层中文意图查询的 Hit@1 只有 38%。”",
        "【做了什么选择】例：“我对比了本地 bge-m3 和中文单语 embedding，前者在中文意图查询上 MRR 从 "
        "0.41 提到 0.68；又加了日语分词后的 BM25 做混合检索，L3 辨析类查询的 Recall@3 再提 12 个点。”",
        "【结果与局限】例：“最终测试集 Hit@1 是 61%、MRR 0.73。局限是知识库只有 N2 语法，"
        "跨到 N1 时召回明显下降，下一步打算做分级索引。”",
    ],
)
add_para_cn(doc, "可讲的五个点：", bold=True)
add_bullets(
    doc,
    [
        "跨语言检索：中文提问检索日文语料，这是有明确技术含义的问题，不是“我用了向量库”。",
        "重排序与消融：有对照组、有数据、有结论，能说清“什么情况下重排序没用”。",
        "日语分词：能解释为什么日语场景下朴素 BM25 会失效 —— 这个细节很少有人讲得出来。",
        "手搓 vs 框架：能对比底层实现与工业封装的差异，包括框架替你省了什么、又拿走了什么控制权。",
        "量化与工程：有评测报告、有 bad case 归因、有服务化和成本数据，不是只有功能列表。",
    ],
)

# ==========================================================================
add_heading_cn(doc, "十二、项目局限与迭代计划（重写）", level=1)
add_para_cn(
    doc,
    "初版把“未接 FastAPI、未处理 PDF、知识库小”写在这里，这三条本版都做掉了。"
    "局限只写真正没做的，而且要写成“我知道边界在哪”，而不是“我不会”。",
    bold=True,
)
add_table_cn(
    doc,
    ["局限", "现状", "迭代方向"],
    [
        ("知识范围限于 N2", "已支持 N2，N1/N3 未覆盖", "分级索引 + 按 level 过滤，扩展到 N1"),
        ("无用户系统", "单用户本地使用", "加入学习进度追踪与错题本，形成复习闭环"),
        ("评测终判仍含人工", "端到端正确率依赖人工判 30 条", "引入 LLM-as-judge 做自动初判，人工只复核分歧样本"),
        ("未做多模态", "仅文本语料", "教材扫描件走 OCR/版面分析，再入库"),
        ("检索规模上限未验证", "当前 3000+ chunk", "压到 10 万 chunk 后测索引构建时间与查询 P95 变化"),
    ],
)

add_para_cn(
    doc,
    "最后一句：这份规划的价值不在于“功能列得全”，而在于每个功能后面都跟了一句"
    "“我怎么知道它有用”。带着评测报告去面试，比带着功能列表去面试，是两个完全不同的起点。",
    bold=True,
)

doc.save(OUT_PATH)
print(f"[OK] 已生成：{OUT_PATH}")
