param()
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Environment .venv tidak ditemukan. Ikuti panduan manual testing.'
}
$env:PYTHONUTF8 = '1'
$env:IPYTHONDIR = Join-Path $projectRoot '.ipython'
$env:JUPYTER_CONFIG_DIR = Join-Path $projectRoot '.jupyter'
$env:JUPYTER_DATA_DIR = Join-Path $projectRoot '.jupyter\data'
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
    $kernelPath = Join-Path $projectRoot '.jupyter\share\jupyter\kernels\bmlp\kernel.json'
    $kernel = Get-Content -LiteralPath $kernelPath -Raw | ConvertFrom-Json
    $kernelEnv = @{
        PYTHONUTF8 = '1'
        IPYTHONDIR = $env:IPYTHONDIR
        JUPYTER_CONFIG_DIR = $env:JUPYTER_CONFIG_DIR
        JUPYTER_DATA_DIR = $env:JUPYTER_DATA_DIR
        JUPYTER_RUNTIME_DIR = $env:JUPYTER_RUNTIME_DIR
        MPLCONFIGDIR = $env:MPLCONFIGDIR
        OMP_NUM_THREADS = '1'
        OPENBLAS_NUM_THREADS = '1'
        MKL_NUM_THREADS = '1'
    }
    $kernel | Add-Member -MemberType NoteProperty -Name env -Value $kernelEnv -Force
    [System.IO.File]::WriteAllText($kernelPath, ($kernel | ConvertTo-Json -Depth 10),
                                  [System.Text.UTF8Encoding]::new($false))
    $kernelList = & $pythonPath -m jupyter kernelspec list --json
    if ($LASTEXITCODE -ne 0) { throw 'Pemeriksaan daftar kernel gagal.' }
    $kernelInfo = $kernelList | ConvertFrom-Json
    if ($null -eq $kernelInfo.kernelspecs.bmlp) { throw 'Kernel bmlp tidak terdeteksi.' }
    $sessionText = & $pythonPath scripts\manual_check.py --prepare
    if ($LASTEXITCODE -ne 0) { throw 'Persiapan salinan manual testing gagal.' }
    $session = $sessionText | ConvertFrom-Json
    Write-Output ('Folder manual test: ' + $session.folder)
    Write-Output ('Python kernel: ' + $session.python)
    Write-Output 'Folder berisi dua notebook dengan output kosong dan satu CSV sumber.'
    Write-Output 'Jalankan Clustering dahulu, lalu Klasifikasi. Simpan kedua notebook.'
    Write-Output 'Lokasi disimpan di .cache/manual-session.json.'
} finally {
    Pop-Location
}
