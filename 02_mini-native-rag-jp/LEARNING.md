# 学习协作契约

> 本文件规定「我（AI）」和「你」在阶段二里各自的职责。
> 当你觉得我越界了（比如直接甩代码给你），把这份文件拍我脸上。

---

## 一、核心目标

**不是「每行代码都是我写的」，而是「每个关键决策我都能负责，每个为什么我都答得出」。**

项目约 1500~2500 行，但真正决定面试表现的是其中约 20% 的决策点：

| 必须真懂（约 20%） | 会用就行（约 80%） |
|---|---|
| chunk 三粒度怎么切、为什么 | `with open` / `Path` / `json.load` 的写法 |
| 为什么向量要 L2 归一化 | argparse、logging 配置样板 |
| 余弦相似度怎么算 | Gradio 界面代码 |
| FAISS 索引与 metadata 为什么必须同序 | FastAPI 路由样板 |
| rerank 什么时候有用、什么时候没用 | HF 模型下载与加载 |
| Hit@1 / MRR 的数学定义 | dataclass / Pydantic 样板 |
| prompt 怎么防幻觉 | 目录遍历、进度条 |

---

## 二、分层原则

| 模块 | 谁写 | 理由 |
|---|---|---|
| `chunker` / `embedder` / `retriever` / `reranker` | **你手写** | RAG 的核心，面试主战场 |
| `evaluation/run_eval.py` | **你手写** | 指标要自己推一遍才记得住 |
| `generator`（prompt 拼装） | **你手写**，我给设计要点 | 防幻觉的关键 |
| `loader` / 日志 / 配置 | 你写，可以快 | 不难，但也不该我代劳 |
| Gradio 界面 / FastAPI 路由 / Dockerfile | **我生成**，你读懂并改 | 纯模板，学它性价比极低 |
| 数据清洗脚本 | 我生成，你改参数 | 一次性工具 |

---

## 三、协作流程（每个模块走一遍）

1. **我给契约，不给代码**
   输入、输出、边界条件、以及这个模块有哪些坑。

2. **你先写第一版。** 我不介入。

3. **卡住时，我给三级提示，逐级升级：**
   - **一级（方向）**：「如果文件不存在，你希望调用方看到异常还是一句人话？」
   - **二级（伪代码）**：「先判断路径 → 再 try json.load → 再校验结构」
   - **三级（代码）**：**只有你明说「给我看」时我才给**，且只给卡住的那几行，不给整个函数。

4. **写完我做 code review**，指出问题并讲清楚为什么。

5. **跑测试 / 跑评测**，用数据说话。

6. **你用大白话给我讲一遍这个模块。** 讲不顺 = 没懂，回去改。
   这是检验「真懂」的唯一有效手段。

---

## 四、每个模块的收尾动作

更新 `DECISIONS.md`，每个决策记三行：

```
## <决策名>
- 为什么：
- 放弃了什么：
- 怎么验证：
```

**这份文件比代码本身值钱。** 面试前复盘、简历上写、面试时讲，全部从它来。
代码面试官不会逐行看，但「你为什么这么选」他一定会问。

---

## 五、你可以随时叫停我

- 我说得太快、跳步了 → 「停，展开讲」
- 我直接给了代码 → 「契约呢？重来」
- 你觉得某个点没懂但我说「这个不重要」→ 「我要懂这个」

**默认我不用代码回答你的问题**，除非你明确说「给我看」。

---

## 六、语法补课大纲（开工前 1~2 次）

设计思路：**你有 Java 的思维模型，不需要「学」概念，只需要「认」它们在 Python 里长什么样。**
所以全部用 Java 对照的方式讲，会快很多。

### Session 1：类型与数据建模
- 类型标注：`def f(x: int) -> str:` —— 它和 Java 的类型有什么区别（提示：运行时不做检查）
- 容器类型：`list[str]` / `dict[str, Any]` / `str | None`
- `@dataclass` 与 Pydantic `BaseModel` 的差别，以及为什么 AI 项目大量用 Pydantic
- **练习**：读懂一个真实项目里的函数签名

### Session 2：Pythonic 写法与工程结构
- 列表 / 字典推导式
- 生成器与 `yield` —— 流式输出会用到
- `with` 上下文管理器
- 装饰器 —— `@app.post` 就是它，FastAPI 全靠这个
- `if __name__ == "__main__":`、包结构与导入
- `*args` / `**kwargs` / 解包

---

## 七、已知的排期代价

分层模式比「我直接生成」慢约 2 倍。阶段二预计 **10~11 周**（原计划 10 周）。
若时间不够，砍的顺序见规划书 4.4「砍什么保什么」：先砍界面美化，最后才砍评测。

---

## 八、Python 易混点清单（累积，随项目更新）

### 8.1 必填 / 可选，只看有没有 `= 默认值`

```python
def f(a: str, b: str = "x") -> None: ...
#      ↑ 必填        ↑ 可选
```

**类型标注管「值可以是哪些」，默认值管「能不能不传」——两个独立维度。**

| Python | Java 对应 | 能不传？ | 能传 null？ |
|---|---|---|---|
| `d: str` | `M(@NotNull String d)` | ❌ | ❌ |
| `d: str \| None` | `M(String d)` | ❌ | ✅ |
| `d: str = "x"` | 重载 `M()` 内部给默认 | ✅ | ❌ |
| `d: str \| None = None` | 重载 `M()` + `M(String d)` | ✅ | ✅ |

⚠️ `d: str | None` 没有默认值时**仍然是必填**。想要可选就要写 `= None`。

### 8.2 可变默认值：三种环境三种行为

```python
def f(box=[]): ...                              # ⚠️ 危险，所有调用共享同一个 list
```
```python
@dataclass
class A:
    tags: list = []                             # ❌ 类定义时就 ValueError
    tags2: list = field(default_factory=list)   # ✅ 正确写法
```
```python
class B(BaseModel):
    tags: list[str] = []                        # ✅ 安全，Pydantic 为每个实例深拷贝
```

### 8.3 类型标注在运行时**不做检查**

```python
def a(p: Path) -> bool:
    return p.exists()      # 传字符串 → AttributeError（用到时才炸）

def b(p: Path) -> str:
    with open(p) as f:     # 传字符串 → 静默正常工作！
        return f.read()
```

报错发生在「用到它的那一刻」，不是「传进去的那一刻」。
所以 `b()` 能跑不代表没问题——它是颗雷，改天用了 `Path` 专属方法就炸。
这正是需要 mypy / Pydantic 的原因。

### 8.4 Pydantic coercion 是单向的

```
int 字段收到 "123"  →  ✅ 转成 123
str 字段收到 123    →  ❌ ValidationError（v2 移除了 int→str 隐式转换）
```

### 8.5 Pydantic 默认会静默丢弃未声明字段

```python
class M(BaseModel):
    id: str

M(id="1", typo_field="x")   # 不报错，typo_field 被悄悄丢掉
# 想报错： model_config = ConfigDict(extra="forbid")
```

### 8.6 `*` 单独出现是 keyword-only 分隔符

```python
def f(p: Path, *, strict: bool = True) -> None: ...
f(p, strict=False)    # ✅
f(p, False)           # ❌ TypeError
```
注意：单独一个 `*` ≠ `*args`。

---

## 九、铁律：不确定就自己跑

**不要问我语法问题，写个 `t.py` 跑一遍。**

跑一遍 10 秒，问我得等一轮，而且自己看到输出记得更牢。
`E:\ai-agent-study\02_mini-native-rag-jp\t.py` 就是你的实验场。
