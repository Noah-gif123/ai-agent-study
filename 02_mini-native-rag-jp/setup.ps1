<#
.SYNOPSIS
    阶段二 · N2 日语 RAG 项目 —— 环境搭建脚本

.DESCRIPTION
    按里程碑分阶段安装依赖，并把「模型缓存 / pip 缓存 / 临时目录」统一指向
    E 盘的项目 .cache 目录。
    原因：C 盘仅剩约 11GB，而 bge-m3 模型权重 + torch 解压很容易撑爆 C 盘。

    本脚本可重复执行（幂等），中断后重跑即可。

.EXAMPLE
    .\setup.ps1 -Stage core         # M1~M4：Embedding + 向量检索（约 1GB）  ← 先跑这个
    .\setup.ps1 -Stage service      # M6~M7：FastAPI + Gradio
    .\setup.ps1 -Stage langchain    # V1：LangChain 重构
    .\setup.ps1 -Stage cuda         # M5：把 CPU 版 torch 换成 CUDA 版（约 3GB）
    .\setup.ps1 -Stage all          # 一次装完（约 4GB，不推荐：先用 core 跑通 M1）
    .\setup.ps1 -Stage check        # 只做环境自检，不安装
#>
[CmdletBinding()]
param(
    [ValidateSet('core', 'service', 'langchain', 'cuda', 'all', 'check')]
    [string]$Stage = 'core'
)

$ErrorActionPreference = 'Stop'

$ProjDir = $PSScriptRoot
$VenvPy  = Join-Path $ProjDir '.venv\Scripts\python.exe'
$ReqDir  = Join-Path $ProjDir 'requirements'
$Cache   = Join-Path $ProjDir '.cache'

# ------------------------------------------------------------------
# 0. 前置检查
# ------------------------------------------------------------------
if (-not (Test-Path $VenvPy)) {
    Write-Host "[X] 未找到虚拟环境：$VenvPy" -ForegroundColor Red
    Write-Host "    请先执行：" -ForegroundColor Yellow
    Write-Host "    py -3.14 -m venv `"$ProjDir\.venv`"" -ForegroundColor Yellow
    exit 1
}

# ------------------------------------------------------------------
# 1. 缓存与临时目录 → E 盘
# ------------------------------------------------------------------
$HfHome   = Join-Path $Cache 'hf'
$PipCache = Join-Path $Cache 'pip'
$TmpDir   = Join-Path $Cache 'tmp'
foreach ($d in @($HfHome, $PipCache, $TmpDir)) {
    New-Item -ItemType Directory -Force -Path $d | Out-Null
}

# 持久化到「用户级」环境变量：模型缓存是长期需求，新开终端也要生效
try {
    [Environment]::SetEnvironmentVariable('HF_HOME',       $HfHome,   'User')
    [Environment]::SetEnvironmentVariable('PIP_CACHE_DIR', $PipCache, 'User')
    [Environment]::SetEnvironmentVariable('HF_ENDPOINT',   'https://hf-mirror.com', 'User')
    Write-Host "  （已写入用户环境变量，新开的终端同样生效）" -ForegroundColor DarkGray
}
catch {
    Write-Host "[!] 无法写入用户环境变量（权限不足），本次仅在当前会话生效。" -ForegroundColor Yellow
    Write-Host "    如需持久化，请手动执行下面两行：" -ForegroundColor Yellow
    Write-Host "      setx HF_HOME `"$HfHome`"" -ForegroundColor Yellow
    Write-Host "      setx PIP_CACHE_DIR `"$PipCache`"" -ForegroundColor Yellow
}

# 当前会话立即生效
$env:HF_HOME       = $HfHome
$env:PIP_CACHE_DIR = $PipCache
$env:TEMP          = $TmpDir
$env:TMP           = $TmpDir

# HuggingFace 镜像：国内直连 huggingface.co 会慢很多（实测响应 4.4s vs 镜像 2.1s）
# 想切回官方源，注释掉下面这行即可
$env:HF_ENDPOINT = 'https://hf-mirror.com'

# 控制台按 UTF-8 输出：Windows PowerShell 5.1 默认用 GBK，Python 的中文会乱码
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
$env:PYTHONIOENCODING = 'utf-8'

Write-Host ""
Write-Host "=== 环境变量 ===" -ForegroundColor Cyan
Write-Host "  HF_HOME       = $HfHome"
Write-Host "  PIP_CACHE_DIR = $PipCache"
Write-Host "  TEMP          = $TmpDir"
Write-Host "  venv python   = $VenvPy"

# ------------------------------------------------------------------
# 2. 安装函数
# ------------------------------------------------------------------
function Install-Req {
    param([string]$File)
    $path = Join-Path $ReqDir $File
    if (-not (Test-Path $path)) { throw "找不到依赖清单：$path" }
    Write-Host ""
    Write-Host "=== 安装 $File ===" -ForegroundColor Cyan
    & $VenvPy -m pip install -r $path --disable-pip-version-check
    if ($LASTEXITCODE -ne 0) { throw "安装失败：$File" }
}

# ------------------------------------------------------------------
# 3. 主流程
# ------------------------------------------------------------------
if ($Stage -ne 'check') {
    Write-Host ""
    Write-Host "=== 升级 pip ===" -ForegroundColor Cyan
    & $VenvPy -m pip install --upgrade pip --disable-pip-version-check

    switch ($Stage) {
        'core'      { Install-Req '01-core.txt' }
        'service'   { Install-Req '02-service.txt' }
        'langchain' { Install-Req '03-langchain.txt' }
        'all' {
            Install-Req '01-core.txt'
            Install-Req '02-service.txt'
            Install-Req '03-langchain.txt'
        }
        'cuda' {
            Write-Host ""
            Write-Host "=== 换成 CUDA 12.6 版 torch（约 3GB，耐心等） ===" -ForegroundColor Yellow
            & $VenvPy -m pip install --upgrade torch torchvision `
                --index-url https://download.pytorch.org/whl/cu126 `
                --disable-pip-version-check
            if ($LASTEXITCODE -ne 0) { throw "CUDA 版 torch 安装失败" }
            Write-Host "提示：若想回到 CPU 版，执行：" -ForegroundColor DarkGray
            Write-Host "  pip install --force-reinstall torch --index-url https://mirrors.aliyun.com/pypi/simple/" -ForegroundColor DarkGray
        }
    }

    # 锁定版本：LangChain 1.x 换代很快，不锁版本两周后就复现不了
    $lock = Join-Path $ProjDir 'requirements.lock.txt'
    & $VenvPy -m pip freeze | Out-File -FilePath $lock -Encoding utf8
    Write-Host ""
    Write-Host "=== 已锁定版本 → $lock ===" -ForegroundColor Green
}

# ------------------------------------------------------------------
# 4. 环境自检
# ------------------------------------------------------------------
Write-Host ""
Write-Host "=== 环境自检 ===" -ForegroundColor Cyan
& $VenvPy (Join-Path $ProjDir 'check_env.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "完成。激活虚拟环境后即可开始编码：" -ForegroundColor Green
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Green
