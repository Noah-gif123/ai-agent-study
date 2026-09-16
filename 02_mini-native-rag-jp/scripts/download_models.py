# -*- coding: utf-8 -*-
r"""
模型预下载脚本 —— 把 bge-m3 与重排序模型拉到本地缓存。

为什么要单独预下载：
    模型权重约 2~3GB，直接在业务代码里第一次调用会阻塞很久，
    而且下载中断后不容易观察进度。这里用 snapshot_download，支持断点续传。

用法（在项目目录下）：
    .\.venv\Scripts\Activate.ps1
    python scripts\download_models.py              # 只下 Embedding 模型（M1~M4 够用）
    python scripts\download_models.py --reranker   # 同时下重排序模型（M5 用）
    python scripts\download_models.py --check      # 只看本地状态，不下载
"""

import argparse
import os
import sys
import time
from pathlib import Path

EMBEDDING_MODEL = "BAAI/bge-m3"
RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"

# 权重文件小于这个体积，就认为没下完。
# 关键：不能用「缓存目录非空」判断 —— 失败的下载会留下几百 KB 的 json/配置，
# 那会让脚本误以为模型已就绪，直接跳过，白白浪费排查时间。
MIN_WEIGHT_BYTES = 100 * 1024 * 1024  # 100MB

WEIGHT_SUFFIXES = {".safetensors", ".bin", ".pt"}


def human(nbytes: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"


def cache_dir_for(model_id: str) -> Path:
    """推算出模型在 HF 缓存里的目录（models--org--name）。"""
    hf_home = os.environ.get("HF_HOME")
    if not hf_home:
        print("[!] HF_HOME 未设置 —— 模型会下到 C 盘默认目录，C 盘空间紧张！")
        print("    请先运行： .\\setup.ps1 -Stage check")
        hf_home = str(Path.home() / ".cache" / "huggingface")
    safe = "models--" + model_id.replace("/", "--")
    return Path(hf_home) / "hub" / safe


def dir_size(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def weights_size(model_id: str) -> int:
    """只统计权重文件，忽略配置与元数据。"""
    root = cache_dir_for(model_id)
    if not root.exists():
        return 0
    total = 0
    for f in root.rglob("*"):
        try:
            if f.is_file() and f.suffix in WEIGHT_SUFFIXES:
                total += f.stat().st_size
        except OSError:
            continue
    return total


def is_ready(model_id: str) -> bool:
    return weights_size(model_id) >= MIN_WEIGHT_BYTES


def show_env() -> None:
    print("=== 下载环境 ===")
    print(f"  HF_HOME     : {os.environ.get('HF_HOME', '(未设置)')}")
    print(f"  HF_ENDPOINT : {os.environ.get('HF_ENDPOINT', '(官方源 huggingface.co)')}")
    print()


def check_local(model_id: str) -> None:
    total = dir_size(cache_dir_for(model_id))
    w = weights_size(model_id)
    if is_ready(model_id):
        flag = "[已就绪]"
    elif total > 0:
        flag = "[不完整]"
    else:
        flag = "[未下载]"
    print(f"  {flag} {model_id:<28} 缓存 {human(total):>9}   权重 {human(w):>9}")


def download(model_id: str) -> bool:
    from huggingface_hub import snapshot_download

    print(f"=== 下载 {model_id} ===")
    start = time.time()
    try:
        path = snapshot_download(
            repo_id=model_id,
            # 只取推理需要的文件，跳过 onnx 导出（约 2GB）、示例图片与文档。
            #
            # 注意：必须带上 *.bin —— BAAI/bge-m3 仓库并没有 model.safetensors，
            # 权重只存在于 pytorch_model.bin。只写 *.safetensors 会下到一个空壳。
            # *.pt 是 bge-m3 的 colbert / sparse 两个附加头，体积很小。
            allow_patterns=[
                "*.json", "*.txt", "*.model", "*.safetensors", "*.bin", "*.pt",
                "sentence_*/**", "1_Pooling/**",
            ],
            max_workers=4,
        )
    except Exception as exc:  # noqa: BLE001 - 脚本需要报告任何下载失败
        print(f"[X] 下载失败：{type(exc).__name__}: {str(exc)[:200]}")
        print("    常见原因：网络中断 / 镜像不可用。可重跑本脚本，支持断点续传。")
        print("    也可设 HF_ENDPOINT=https://huggingface.co 换回官方源试试。")
        return False

    elapsed = time.time() - start
    size = dir_size(Path(path))
    print(f"[OK] 完成：{human(size)}，耗时 {elapsed/60:.1f} 分钟")
    print(f"     位置：{path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="预下载 N2 RAG 项目所需模型")
    parser.add_argument("--reranker", action="store_true", help="同时下载重排序模型（约 2GB，M5 才需要）")
    parser.add_argument("--check", action="store_true", help="只检查本地状态，不下载")
    args = parser.parse_args()

    show_env()

    if args.check:
        print("=== 本地缓存 ===")
        for model_id in (EMBEDDING_MODEL, RERANKER_MODEL):
            check_local(model_id)
        return 0

    targets = [EMBEDDING_MODEL]
    if args.reranker:
        targets.append(RERANKER_MODEL)

    ok = True
    for model_id in targets:
        if is_ready(model_id):
            print(f"=== 已就绪，跳过 {model_id} ===")
            check_local(model_id)
            print()
            continue
        if dir_size(cache_dir_for(model_id)) > 0:
            print(f"=== {model_id} 有未完成的下载，继续续传 ===")
        ok = download(model_id) and ok
        print()

    print("=== 结果 ===")
    for model_id in (EMBEDDING_MODEL, RERANKER_MODEL):
        check_local(model_id)

    if not ok:
        print("\n[!] 有模型未下载完成。重跑本脚本可续传。")
        return 1

    print("\n模型就绪。下一步：M1 整理数据资产（文档集 + 黄金评测集）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
