# -*- coding: utf-8 -*-
r"""
阶段二环境自检 —— 确认虚拟环境、缓存路径与关键依赖是否正确。

运行：
    .\setup.ps1 -Stage check
或：
    .\.venv\Scripts\python.exe check_env.py
"""

import importlib
import os
import sys
from pathlib import Path

OK = "[OK]  "
NG = "[--]  "
WARN = "[!!]  "

# 按安装阶段分组，方便一眼看出「当前进度到哪了」
GROUPS = [
    ("基础环境", ["numpy", "requests", "pydantic", "dotenv", "tiktoken", "openai"]),
    ("M1~M4 检索链路", ["torch", "sentence_transformers", "transformers", "faiss"]),
    ("M6~M7 服务化", ["fastapi", "uvicorn", "gradio"]),
    ("V1 LangChain", ["langchain", "langgraph", "langchain_huggingface", "rank_bm25", "fugashi"]),
]


def show_paths() -> None:
    print("=== 路径 ===")
    print(f"  Python      : {sys.executable}")
    print(f"  sys.prefix  : {sys.prefix}")
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    print(f"  虚拟环境    : {'是' if in_venv else '否 —— 警告：正在使用全局解释器！'}")

    hf_home = os.environ.get("HF_HOME")
    if not hf_home:
        print(f"{WARN}HF_HOME 未设置 —— 模型会下载到 C 盘默认缓存目录，C 盘空间紧张！")
    else:
        print(f"  HF_HOME     : {hf_home}")
        drive = Path(hf_home).drive.upper()
        if drive == "C:":
            print(f"{WARN}HF_HOME 在 C 盘，建议改到 E 盘（见 setup.ps1）")

    pip_cache = os.environ.get("PIP_CACHE_DIR")
    print(f"  PIP_CACHE_DIR: {pip_cache or '（未设置，使用默认 C 盘路径）'}")
    print()


def show_packages() -> None:
    print("=== 依赖自检 ===")
    for group, mods in GROUPS:
        print(f"\n  -- {group} --")
        for name in mods:
            try:
                mod = importlib.import_module(name)
                ver = getattr(mod, "__version__", "")
                print(f"  {OK}{name:<22} {ver}")
            except Exception as exc:  # noqa: BLE001 - 自检脚本，报告任何失败
                print(f"  {NG}{name:<22} 未安装（{type(exc).__name__}）")
    print()


def show_torch() -> None:
    print("=== 算力 ===")
    try:
        import torch
    except Exception:  # noqa: BLE001
        print(f"{WARN}torch 未安装，跳过")
        return

    print(f"  torch       : {torch.__version__}")
    cuda_ok = torch.cuda.is_available()
    print(f"  CUDA 可用   : {cuda_ok}")
    if cuda_ok:
        print(f"  设备        : {torch.cuda.get_device_name(0)}")
        total = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"  显存        : {total:.1f} GB")
    elif "+cpu" in torch.__version__:
        print(f"{WARN}当前是 CPU 版 torch，显卡未启用。")
        print("       M1~M4 用 CPU 跑没问题（编码是一次性成本）；")
        print("       到 M5 再执行： .\\setup.ps1 -Stage cuda")
    else:
        print(f"{WARN}torch 是 CUDA 版但 CUDA 不可用，检查显卡驱动。")
    print()


def main() -> int:
    print()
    show_paths()
    show_packages()
    show_torch()

    print("=== 下一步 ===")
    print("  1. 按里程碑 M1 开始整理数据资产（文档集 + 黄金评测集）")
    print("  2. 若刚装完 core，先跑通一次 embedding + 一次检索，确认模型能下载成功")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
