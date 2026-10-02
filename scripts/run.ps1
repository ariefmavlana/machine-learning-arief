param()
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Environment .venv tidak tersedia. Ikuti setup pada README.md.'
}
$env:PYTHONUTF8 = '1'
$env:IPYTHONDIR = Join-Path $projectRoot '.ipython'
$env:JUPYTER_CONFIG_DIR = Join-Path $projectRoot '.jupyter'
$env:JUPYTER_RUNTIME_DIR = Join-Path $projectRoot '.jupyter\runtime'
$env:JUPYTER_PATH = Join-Path $projectRoot '.jupyter\share\jupyter'
$env:MPLCONFIGDIR = Join-Path $projectRoot '.cache\matplotlib'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
Push-Location -LiteralPath $projectRoot
try {
    & $pythonPath -m ipykernel install --prefix .jupyter --name bmlp --display-name 'Python 3 (BMLP)'
    if ($LASTEXITCODE -ne 0) { throw 'Pendaftaran kernel gagal.' }
    & $pythonPath scripts\build_notebooks.py
    if ($LASTEXITCODE -ne 0) { throw 'Pengisian template gagal.' }
    & $pythonPath scripts\execute_submission.py
    if ($LASTEXITCODE -ne 0) { throw 'Eksekusi notebook gagal.' }
    & $pythonPath -m pytest tests -q --basetemp .cache\pytest-manual-check
    if ($LASTEXITCODE -ne 0) { throw 'Verifikasi submission gagal.' }
} finally {
    Pop-Location
}
