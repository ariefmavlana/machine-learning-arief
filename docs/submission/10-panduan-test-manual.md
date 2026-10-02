# Panduan pengujian manual di VS Code dan Jupyter

[Indeks dokumentasi](README.md) · [Lembar pencatatan](11-lembar-hasil-test-manual.md) · [Hasil pengujian ulang](../../reports/hasil-pengujian-ulang.md)

Panduan ini membawa Anda dari pemeriksaan lingkungan hingga ZIP hasil pengujian manual. Gunakan salinan uji yang disiapkan dari ZIP final, jalankan Clustering dahulu lalu Klasifikasi, periksa hasil, dan simpan kedua notebook. Pemeriksaan otomatis pelengkap tersedia agar kesalahan file, label, atau output tidak hanya dinilai dari tampilan.

Kode kedua notebook sudah dijalankan ulang melalui kernel Jupyter baru pada salinan ZIP, tanpa model atau CSV hasil sebelumnya. Hasilnya sama dengan acuan pengujian. Pengujian melalui antarmuka VS Code atau Jupyter belum dilakukan; gunakan panduan ini untuk menjalankannya dan catat hasil pada lembar pengujian.

## 1 Memilih cara pengujian

| Pilihan | Gunakan ketika | Yang perlu tersedia |
| --- | --- | --- |
| VS Code | Ingin melihat notebook, file hasil, dan terminal dalam satu aplikasi. | Extension Python dan Jupyter, serta kernel environment proyek. |
| Jupyter di browser | Sudah mempunyai Notebook atau JupyterLab dan terbiasa dengan menunya. | Server Jupyter milik Anda dan kernel Python 3 BMLP. |

Pilih salah satu untuk pengujian utama. Mengulangi di aplikasi kedua bersifat tambahan; buat salinan uji baru untuk menjaga catatan kedua sesi terpisah.

Pada pemeriksaan lingkungan sesi ini, VS Code tersedia dan extension Python terdaftar, tetapi `ms-toolsai.jupyter` belum muncul dalam daftar extension. `.venv` proyek memiliki ipykernel dan nbclient, tetapi belum memiliki server `notebook` atau `jupyterlab`. Ini tidak memastikan bahwa instalasi Jupyter Anda di environment lain tidak ada.

Untuk langkah manual, Anda tidak perlu menjalankan `scripts/run.ps1`: script itu membangun ulang artefak utama. Gunakan `scripts/prepare_manual.ps1` untuk menyiapkan salinan uji yang terpisah.

## 2 Memeriksa environment proyek

Buka PowerShell, lalu jalankan:

```powershell
Set-Location -LiteralPath 'F:\portfolio-arief\ml-arief'
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import sys, sklearn, pandas, numpy, yellowbrick, joblib; print(sys.executable); print('sklearn', sklearn.__version__); print('pandas', pandas.__version__); print('numpy', numpy.__version__); print('yellowbrick', yellowbrick.__version__); print('joblib', joblib.__version__)"
```

| Pemeriksaan | Hasil acuan |
| --- | --- |
| Executable | `F:\portfolio-arief\ml-arief\.venv\Scripts\python.exe` |
| Python | 3.12.14 pada environment saat ini. |
| scikit-learn | 1.7.0 |
| pandas | 2.2.3 |
| NumPy | 2.2.6 |
| Yellowbrick | 1.5 |
| joblib | 1.5.1 |

Versi patch Python dapat berbeda pada pemasangan baru, tetapi untuk mengulang hasil sedekat mungkin gunakan Python 3.12 dan versi paket yang dikunci. Jangan memilih Python global 3.14 untuk pengujian ini.

Jika `.venv` sudah berfungsi, lewati pemasangan. Jika environment belum ada, gunakan uv dan Python 3.12:

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements-lock.txt
```

Tidak perlu menjalankan `Activate.ps1`; contoh menggunakan executable environment secara langsung. Cara ini juga mencegah perintah pip tidak sengaja memasang paket ke Python global. [Dokumentasi environment uv](https://docs.astral.sh/uv/pip/environments/).

## 3 Menyiapkan salinan uji tanpa output lama

Dari PowerShell di direktori proyek:

```powershell
.\scripts\prepare_manual.ps1
$session = Get-Content -LiteralPath '.cache\manual-session.json' -Raw | ConvertFrom-Json
$manualFolder = $session.folder
$projectPython = $session.python
Get-ChildItem -LiteralPath $manualFolder
```

Script membuat folder baru di `.cache/manual-tests`, mengambil dua notebook dan CSV mentah dari ZIP, lalu mengosongkan output serta execution count pada salinan notebook. Model dan CSV hasil tidak disalin. ZIP serta notebook utama tetap utuh.

**Kondisi awal yang harus terlihat:** tepat tiga file, yaitu kedua notebook `.ipynb` dan `bank_transactions_data_edited.csv`. Tidak ada `model_clustering.h5`, `data_clustering.csv`, atau `data_clustering_inverse.csv` sebelum Anda menjalankan clustering.

Script juga mendaftarkan kernel `Python 3 (BMLP)` di workspace, mengatur direktori konfigurasi/cache yang dapat ditulis, dan menetapkan thread numerik ke 1. Kernel terdaftar membawa pengaturan environment tersebut melalui `kernel.json`; ini mengikuti mekanisme kernelspec Jupyter. [Dokumentasi kernel Jupyter](https://jupyter-client.readthedocs.io/en/stable/kernels.html).

Simpan lokasi `$manualFolder` pada [lembar hasil](11-lembar-hasil-test-manual.md). Setiap pemanggilan persiapan membuat folder baru dan memperbarui `.cache/manual-session.json`; jika membuat beberapa sesi, catat lokasi masing-masing agar pemeriksa tidak diarahkan ke sesi yang salah.

## 4 Membuka salinan di VS Code

1. Di Extensions, pastikan **Python** dari Microsoft dan **Jupyter** dengan ID `ms-toolsai.jupyter` terpasang. Untuk Jupyter yang belum ada, cari extension tersebut lalu pilih Install.
2. Dari PowerShell persiapan, buka folder uji dengan `code --new-window "$manualFolder"`, atau gunakan File → Open Folder dan pilih lokasi yang tercetak.
3. Buka notebook `[Clustering]_Submission_Akhir_BMLP_Arief_Maulana.ipynb` dari Explorer.
4. Pada **Select Kernel**, pilih `Python 3 (BMLP)` jika terdaftar. Pastikan interpreter menunjuk `.venv` proyek, bukan Python global atau environment lain.
5. Jika kernel terdaftar belum muncul, gunakan pemilih kernel untuk memilih environment Python di `F:\portfolio-arief\ml-arief\.venv\Scripts\python.exe`. Jika muncul warning thread pada cara ini, gunakan kernel BMLP melalui server Jupyter pada bagian berikut.
6. Gunakan tombol Run untuk eksekusi cell per cell. Untuk pengujian akhir, pilih Restart kernel lalu Run All, tunggu selesai, dan simpan dengan Ctrl+S.

Pemilihan kernel, Run All, dan penyimpanan mengikuti fitur notebook resmi VS Code. Nama pilihan dapat sedikit berbeda sesuai versi extension. [Dokumentasi notebook VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).

Jika membuka hanya satu file membuat relative path membingungkan, buka folder uji sebagai workspace. CSV mentah harus terlihat di folder yang sama dengan notebook.

## 5 Membuka salinan di Jupyter

Jupyter mempunyai dua bagian: server yang menampilkan halaman, dan kernel yang menjalankan Python. Server boleh berasal dari instalasi Jupyter Anda, tetapi pilih kernel BMLP untuk mengeksekusi notebook proyek.

### Menggunakan server Jupyter yang sudah ada

Di PowerShell tempat script persiapan dijalankan, cari executable server Anda:

```powershell
Get-Command jupyter -ErrorAction SilentlyContinue
jupyter notebook --notebook-dir "$manualFolder"
```

Jika Anda memakai Anaconda Prompt atau launcher lain, buka direktori uji di sana dan teruskan `JUPYTER_PATH` ke `F:\portfolio-arief\ml-arief\.jupyter\share\jupyter` supaya kernel lokal dapat ditemukan. Lokasi executable server mengikuti instalasi Anda; tidak diasumsikan berada di `.venv` proyek.

### Jika belum ada executable server

Anda dapat menyediakan server pada environment terpisah sehingga paket ML tidak berubah:

```powershell
Set-Location -LiteralPath 'F:\portfolio-arief\ml-arief'
uv venv --python .venv\Scripts\python.exe .venv-jupyter-ui
uv pip install --python .venv-jupyter-ui\Scripts\python.exe notebook
$session = Get-Content -LiteralPath '.cache\manual-session.json' -Raw | ConvertFrom-Json
$manualFolder = $session.folder
.\scripts\prepare_manual.ps1
$session = Get-Content -LiteralPath '.cache\manual-session.json' -Raw | ConvertFrom-Json
$manualFolder = $session.folder
.\.venv-jupyter-ui\Scripts\jupyter.exe notebook --notebook-dir "$manualFolder"
```

Pemanggilan persiapan di contoh tersebut memastikan environment kernel tersedia pada terminal yang sama, sekaligus membuat sesi baru. Catat lokasi terbaru. Instalasi server memerlukan akses unduhan; paket model tetap berada pada `.venv`, sedangkan server berada pada `.venv-jupyter-ui`.

Di halaman Jupyter, buka notebook Clustering, pilih kernel `Python 3 (BMLP)`, lalu lakukan pengujian bertahap di bagian berikut. Pada sesi akhir, pilih tindakan **restart kernel dan jalankan semua cell**, tunggu kernel idle, lalu Save. Notebook klasik dan Notebook 7/JupyterLab dapat menempatkan tindakan tersebut di menu yang berbeda. [Panduan menjalankan server Jupyter](https://docs.jupyter.org/en/latest/running.html), [panduan Notebook](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html).

Jika memilih VS Code tetapi ingin memakai kernel dari server ini, gunakan opsi koneksi ke existing Jupyter server di pemilih kernel VS Code dan masukkan URL lokal yang tercetak pada terminal Anda. Setelah tersambung, pilih kernel BMLP.

## 6 Memastikan kernel dan direktori kerja

Pastikan kernel yang dipilih adalah environment proyek. Untuk diagnosis, Anda boleh membuat notebook sementara `diagnostik.ipynb` di folder uji dan menjalankan kode berikut. Notebook tersebut bukan bagian submission dan jangan menambahkan cell ini ke notebook resmi:

```python
import os
import sys
import sklearn
from pathlib import Path

print('Python:', sys.executable)
print('scikit-learn:', sklearn.__version__)
print('Working directory:', Path.cwd())
print('CSV ditemukan:', Path('bank_transactions_data_edited.csv').is_file())
print('OMP_NUM_THREADS:', os.environ.get('OMP_NUM_THREADS'))
```

Expected: executable `.venv`, sklearn 1.7.0, direktori kerja folder uji, CSV ditemukan `True`, dan OMP_NUM_THREADS `1` pada kernel BMLP. Diagnosis di notebook lain tidak membuktikan bahwa kernel notebook resmi sama; tetap pilih kernel BMLP pada **kedua** notebook resmi.

Jangan mengganti relative path notebook menjadi path khusus komputer hanya untuk menyelesaikan FileNotFoundError. Perbaiki direktori kerja atau pilihan folder/kernel agar notebook tetap portable.

## 7 Menguji notebook Clustering per tahap

Kolom **Cell** di bawah menyebut urutan eksekusi code cell 1–35 setelah restart, bukan indeks seluruh cell notebook. **C01–C20** adalah ID kasus yang mengelompokkan beberapa cell. Markdown tidak dihitung. Komentar awal code cell membantu mencari tahapnya. Output kosong pada import atau assignment murni merupakan hal wajar; pada cell yang memang menampilkan data atau plot, output harus ada.

### Data dan visualisasi

| Kasus | Cell | Tindakan dan hasil yang diharapkan |
| --- | --- | --- |
| C01 | 1 | Jalankan import bawaan; tidak ada ModuleNotFoundError atau warning runtime. |
| C02 | 2–5 | Load CSV, head, info, describe tampil. Data mentah mempunyai 2.537 baris, 16 kolom, lima kolom numerik, dan sebelas kolom object. |
| C03 | 6–8 | Daftar numerik, matriks korelasi lima fitur, histogram lima fitur tampil; subplot kosong disembunyikan. |
| C04 | 9 | Boxplot, sebelas distribusi kategorikal, dan violinplot tampil. Semua kategori dicakup; label tick hanya dijarangkan. Judul, sumbu, dan label terbaca. |

Jangan membandingkan jumlah baris aktual dengan deskripsi 2.512 pada markdown bawaan seolah-olah merupakan error. Deskripsi dan gambar expected output asli dipertahankan; hasil aktual dijelaskan pada `Penilaian (Opsional)`.

### Pembersihan dan preprocessing

| Kasus | Cell | Expected |
| --- | --- | --- |
| C05 | 10–11 | Pemeriksaan missing menunjukkan total 403 sel kosong, duplikat 21. |
| C06 | 12 | Sesudah dropna, semua missing nol dan tersisa 2.156 observasi. |
| C07 | 13 | Sesudah drop_duplicates, duplikat nol dan tersisa 2.135 observasi. |
| C08 | 14 | Tujuh kolom ID/IP/date dihapus, termasuk PreviousTransactionDate. Tersisa sembilan fitur. |
| C09 | 15–16 | TransactionType, Location, Channel, CustomerOccupation menjadi kode numerik; daftar kolom sesuai. |
| C10 | 17 | Sesudah filter outlier IQR berurutan, tersisa 1.945 observasi. |
| C11 | 18 | Lima fitur numerik distandardisasi. LoginAttempts konstan menjadi nol setelah scaling. |
| C12 | 19–20 | CustomerAgeGroup ditambahkan dan di-encode; fitur asli CustomerAge tetap ada. Model memakai sepuluh fitur hasil preprocessing. |

Kolom yang harus dihapus: TransactionID, AccountID, TransactionDate, DeviceID, IP Address, MerchantID, PreviousTransactionDate.

| Filter outlier | Baris tersisa |
| --- | --- |
| TransactionAmount | 2.042 |
| CustomerAge | 2.042 |
| TransactionDuration | 2.042 |
| LoginAttempts | 1.945 |
| AccountBalance | 1.945 |

IQR LoginAttempts nol sehingga hanya nilai 1 bertahan. Itu hasil metode pada template, bukan bukti seluruh observasi yang dihapus adalah fraud.

### Clustering dan PCA

| Kasus | Cell | Expected |
| --- | --- | --- |
| C13 | 21–22 | KElbowVisualizer memakai silhouette untuk k=2–9; model utama memilih dua cluster. |
| C14 | 23 | `model_clustering.h5` terbentuk di folder uji. |
| C15 | 24–25 | Silhouette utama sekitar 0,5721599258; scatter plot PCA dengan dua cluster dan centroid tampil. |
| C16 | 26–27 | Dua komponen PCA, varians dijelaskan sekitar 0,9731776820, silhouette PCA sekitar 0,6017426993; `PCA_model_clustering.h5` terbentuk. |

Gunakan toleransi 1e-6 untuk membandingkan angka yang ditampilkan. Perbedaan desimal sangat akhir dapat bergantung pada platform; perbedaan jumlah cluster, fitur, atau baris perlu ditelusuri. Pemeriksa otomatis lokal memakai toleransi lebih ketat karena environment baseline dikunci.

### Interpretasi dan ekspor

| Kasus | Cell | Expected |
| --- | --- | --- |
| C17 | 28 | Agregasi mean/min/max numerik untuk kedua cluster tampil. Narasi sebelum inverse tersedia. |
| C18 | 29–30 | Kolom Cluster diganti persis `Target`; `data_clustering.csv` terbentuk tanpa indeks tambahan. |
| C19 | 31–33 | Nilai numerik kembali ke satuan asal; kategori string kembali; tabel mean/min/max dan mode tampil. Narasi seluruh cluster sesudah inverse tersedia. |
| C20 | 34–35 | `data_clustering_inverse.csv` terbentuk dan Target tetap selaras. |

Sesudah clustering selesai, folder uji memiliki **tujuh file wajib hasil tahap ini**: dua notebook, CSV mentah, dua model clustering, dan dua CSV hasil. Notebook diagnosis, jika Anda membuatnya, dihitung sebagai tambahan di luar artefak wajib.

| Kontrol CSV | Expected |
| --- | --- |
| Bentuk kedua CSV hasil | 1.945 baris × 11 kolom. |
| Label | Target 0: 980 observasi; Target 1: 965 observasi. |
| Kolom terakhir | Target. |
| Missing pada CSV hasil | Tidak ada. |
| Indeks tambahan | Tidak ada `Unnamed: 0`. |
| CustomerAgeGroup inverse | 1_Muda, 2_Dewasa, 3_Senior. |
| Target kedua CSV | Sama per baris, bukan hanya sama jumlahnya. |

Centang hasil tahap tersebut pada [lembar pencatatan](11-lembar-hasil-test-manual.md). Simpan notebook Clustering sebelum membuka Klasifikasi.

## 8 Menguji notebook Klasifikasi

Pilih kernel BMLP pada notebook Klasifikasi secara terpisah. CSV inverse harus sudah tersedia dari tahap Clustering. Angka berikut adalah urutan 13 code cell klasifikasi setelah restart.

| Kasus | Cell | Expected |
| --- | --- | --- |
| K01 | 1–3 | Import berhasil; data diambil dari `data_clustering_inverse.csv`; head memperlihatkan Target dan kategori string. |
| K02 | 4 | One Hot Encoding berjalan pada kolom object; target tidak di-encode atau dimasukkan sebagai fitur. |
| K03 | 5 | Total 1.945 observasi, training 1.556, testing 389; 55 fitur X dan stratify=y. |
| K04 | 6–7 | Decision Tree dilatih dan `decision_tree_model.h5` terbentuk. |
| K05 | 8–10 | Random Forest dilatih; kedua classification report dan tabel empat metrik tampil; `explore_RandomForest_classification.h5` terbentuk. |
| K06 | 11 | GridSearchCV menguji 18 kombinasi pada training dengan 5 fold dan scoring accuracy; best CV accuracy 1,0. |
| K07 | 12–13 | Report serta tabel model tuning tampil; `tuning_classification.h5` terbentuk. |

| Model | Accuracy | Precision macro | Recall macro | F1 macro |
| --- | --- | --- | --- | --- |
| Decision Tree | 1,0 | 1,0 | 1,0 | 1,0 |
| Random Forest | 1,0 | 1,0 | 1,0 | 1,0 |
| Random Forest tuning | 1,0 | 1,0 | 1,0 | 1,0 |

Parameter terbaik baseline: max_depth=None, min_samples_leaf=1, n_estimators=200. Skor sempurna mengukur replikasi label clustering yang sangat dipengaruhi kategori lokasi. Jangan menuliskan kesimpulan bahwa model sudah mendeteksi fraud dengan akurasi sempurna.

Sesudah kedua notebook selesai, sepuluh artefak wajib harus tersedia. File `.h5` merupakan serialisasi joblib sesuai template; membukanya sebagai HDF5 bukan cara pengujian yang tepat.

## 9 Menguji urutan dari kernel bersih

Setelah pengujian per tahap, ulangi kedua notebook untuk memastikan hasil tidak bergantung pada variabel sesi lama:

1. Restart kernel Clustering, kemudian Run All. Tunggu seluruh cell selesai dan simpan.
2. Restart kernel Klasifikasi, kemudian Run All. Tunggu seluruh cell selesai dan simpan.
3. Pastikan cell Clustering bernomor eksekusi 1 sampai 35 dan Klasifikasi 1 sampai 13, tanpa traceback.
4. Setelah penyimpanan akhir, jangan menjalankan cell individual lagi sebelum pemeriksaan; langkah itu dapat membuat execution count tidak berurutan.

Restart kernel tidak sama dengan Clear Outputs. Restart menghapus variabel dari memori; Clear Outputs hanya menghapus tampilan yang disimpan.

Kode notebook menghasilkan ulang model dan CSV di **folder uji**, bukan folder artefak utama. Markdown analisis merupakan hasil baseline yang disimpan di notebook. Jika Anda sengaja mengubah data atau parameter, kode saja tidak memperbarui narasi tersebut; analisis harus diperbarui sesuai hasil baru. Pada pengujian tanpa perubahan, baseline seharusnya tetap cocok.

## 10 Memeriksa hasil manual dengan script

Kembali ke PowerShell di direktori proyek, baca lokasi sesi yang benar, lalu jalankan:

```powershell
Set-Location -LiteralPath 'F:\portfolio-arief\ml-arief'
$session = Get-Content -LiteralPath '.cache\manual-session.json' -Raw | ConvertFrom-Json
$manualFolder = $session.folder
.\.venv\Scripts\python.exe scripts\manual_check.py --folder "$manualFolder" --report 'reports\manual-check-latest.json'
$LASTEXITCODE
```

Expected: **13/13 checks passed** dan exit code **0**. Report berada di `reports/manual-check-latest.json`. Jika salah satu check gagal, exit code 1 dan nama check serta penyebabnya tercetak. Script membaca hasil dan membuat laporan; tidak memperbaiki notebook atau mengganti artefak submission secara diam-diam.

| Check | Yang diverifikasi |
| --- | --- |
| required_files | Sepuluh file wajib ada dan tidak kosong. |
| notebook_clustering | Format notebook valid, jumlah code cell/import sama, output tersimpan, urutan eksekusi benar, 17 grafik, tanpa error/warning. |
| notebook_classification | Format, 13 code cell, import, output, dan urutan eksekusi benar. |
| raw_dataset | Snapshot CSV identik dengan sumber, bentuk serta kualitas data sesuai. |
| csv_alignment | Kedua CSV 1.945 × 11, Target selaras, tidak ada missing/indeks tambahan/kolom terlarang. |
| inverse_roundtrip | Nilai dan urutan baris inverse cocok dengan observasi sumber yang lolos preprocessing, termasuk bin usia. |
| clustering_model | Prediksi model utama sesuai Target dan silhouette sesuai baseline. |
| pca_model | Model pembanding menerima dua fitur dan silhouette sesuai. |
| classification_split | Rekonstruksi split menghasilkan 1.556/389 observasi dan 55 fitur tanpa overlap indeks. |
| decision_tree | Model dapat dipakai untuk predict pada fitur test yang benar; empat metrik sesuai. |
| random_forest | Pemeriksaan yang sama untuk model tambahan. |
| tuned_random_forest | Pemeriksaan yang sama untuk hasil tuning. |
| tuning_cv | Lima fold, 18 kombinasi, parameter dan hasil CV terbaik konsisten. |

Untuk suite proyek lengkap, jalankan dari root:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q --tb=short --basetemp .cache\pytest-manual-check
```

Expected saat panduan dibuat: **11 passed**. Suite ini memeriksa artefak utama proyek dan perilaku pemeriksa, termasuk mendeteksi kegagalan buatan pada salinan sementara. Untuk folder manual Anda, gunakan `manual_check.py --folder`, bukan menganggap pytest otomatis memilih folder tersebut.

## 11 Menguji kegagalan yang seharusnya terdeteksi

Lakukan pada sesi uji tambahan, bukan sesi yang akan Anda kemas. Uji negatif membantu memastikan Anda mengenali kegagalan sebenarnya.

| Kasus | Tindakan pada salinan baru | Hasil yang benar |
| --- | --- | --- |
| N01 | Jalankan Klasifikasi sebelum Clustering pada folder tiga file awal. | FileNotFoundError untuk CSV inverse; selesaikan clustering dahulu. |
| N02 | Restart kernel, lalu langsung jalankan cell training tanpa load/split. | NameError untuk variabel yang belum dibuat; Run All sesuai urutan. |
| N03 | Buat salinan tambahan folder hasil dan pindahkan satu model keluar dari salinan itu. | required_files dan check model terkait gagal. |
| N04 | Pada salinan tambahan, ubah satu Target hanya di CSV inverse. | csv_alignment gagal; kesamaan jumlah label saja tidak cukup. |
| N05 | Simpan notebook dengan traceback dari N01/N02. | Check notebook gagal walaupun beberapa file hasil lain masih ada. |

Tes regresi otomatis telah mencakup N03, N04, dan N05 secara terisolasi. Pengujian N01/N02 dari GUI tetap Anda lakukan bila diinginkan. Setelah uji negatif, restart dan Run All kedua notebook pada sesi final; jangan mengemas notebook dengan traceback tersimpan.

## 12 Mengemas ZIP setelah tes manual

Anda dapat tetap menggunakan ZIP utama yang sudah diuji. Jika ingin mengirim hasil penyimpanan manual Anda, kemas sepuluh file yang diperiksa dari folder sesi final. Jangan memasukkan notebook diagnosis, file report, cache, atau environment.

Setelah `manual_check.py` lulus, gunakan PowerShell dari root:

```powershell
$session = Get-Content -LiteralPath '.cache\manual-session.json' -Raw | ConvertFrom-Json
$manualFolder = $session.folder
$names = @(
    '[Clustering]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
    '[Klasifikasi]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
    'bank_transactions_data_edited.csv',
    'data_clustering.csv',
    'data_clustering_inverse.csv',
    'model_clustering.h5',
    'PCA_model_clustering.h5',
    'decision_tree_model.h5',
    'explore_RandomForest_classification.h5',
    'tuning_classification.h5'
)
$packFiles = $names | ForEach-Object { Join-Path $manualFolder $_ }
$zipPath = Join-Path (Get-Location) ('dist\BMLP_Arief_Maulana_manual_' + (Get-Date -Format yyyyMMdd_HHmmss) + '.zip')
Compress-Archive -LiteralPath $packFiles -DestinationPath $zipPath
$zipPath
```

Gunakan `-LiteralPath` karena nama notebook memiliki tanda kurung siku. Nama ZIP baru menjaga ZIP utama. Buka ZIP di File Explorer: pastikan sepuluh file tersedia langsung, tidak kosong, dan notebook yang dibuka masih memiliki output serta narasi. Jika Anda mengubah file setelah pengecekan, ulangi check dan kemas ulang versi terbaru.

## 13 Menangani masalah

| Gejala | Penyebab yang perlu dicek | Tindakan |
| --- | --- | --- |
| Notebook tampil sebagai JSON | Dibuka dengan text editor atau extension Jupyter belum ada. | Pasang/aktifkan extension Jupyter; buka sebagai notebook. |
| ModuleNotFoundError sklearn/yellowbrick | Kernel salah atau dependensi belum terpasang. | Pilih `.venv` proyek, cek executable, gunakan requirements-lock. |
| No module named distutils | Setuptools yang diperlukan Yellowbrick tidak tersedia. | Pastikan setuptools 80.9.0 dari lock terpasang; restart kernel. |
| FileNotFoundError CSV mentah | Direktori kerja berbeda atau CSV tidak disalin. | Buka folder manual yang benar dan cek CSV di sebelah notebook. |
| FileNotFoundError CSV inverse | Clustering belum berhasil sampai ekspor akhir. | Selesaikan seluruh 35 code cell Clustering terlebih dahulu. |
| NameError df/X_train/model | Cell tidak dijalankan berurutan atau kernel baru. | Restart, lalu Run All dari atas. |
| Kernel BMLP tidak terlihat | Server/editor tidak memakai JUPYTER_PATH dari persiapan. | Jalankan persiapan pada terminal peluncur; gunakan server Jupyter dengan kernel terdaftar. |
| PermissionError cache/Jupyter | Runtime memilih folder konfigurasi default yang tidak dapat ditulis. | Gunakan persiapan proyek yang menetapkan cache, config, data, dan runtime lokal. |
| Warning K-Means tentang thread/memory di Windows | Kernel tidak membawa OMP_NUM_THREADS=1. | Gunakan kernel BMLP; restart kernel setelah pengaturan. |
| Run All terlihat sibuk | Cell plot atau tuning masih berjalan. | Tunggu indikator kernel idle; baca cell aktif, jangan klik Run All berulang. |
| Grafik terlalu kecil | Zoom editor atau output diringkas. | Buka gambar pada ukuran penuh; periksa tick dan legenda. |
| nbformat/error check gagal | Cell tambahan, output error, atau struktur berubah. | Kembali ke salinan template terisi; jangan menambah code cell pada notebook resmi. |
| execution count check gagal | Cell individual dijalankan sesudah Run All atau kernel tidak direstart. | Restart, Run All sekali, Save, lalu check. |
| csv_alignment gagal | CSV berasal dari sesi berbeda atau label bergeser. | Jalankan ulang Clustering dan kemudian Klasifikasi pada folder yang sama. |
| F1 atau jumlah baris berbeda | Dataset/parameter/versi/fitur atau tahap preprocessing berbeda. | Cocokkan tahapan dengan tabel expected, mulai dari perbedaan paling awal. |
| script PowerShell diblokir | Execution policy pada sesi terminal. | Jalankan proses khusus: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\prepare_manual.ps1`; lalu baca file sesi dan set environment peluncur di terminal Anda. |
| Perintah jupyter notebook tidak dikenali | Server ada di environment lain atau belum dipasang. | Gunakan executable instalasi Anda atau environment UI terpisah pada bagian 5. |

Jika script persiapan dijalankan lewat proses PowerShell terpisah, environment proses itu tidak otomatis berpindah ke terminal induk. Jalankan server dari proses yang memperoleh variabel tersebut, atau set `JUPYTER_PATH` ke folder kernel proyek pada terminal peluncur. Pengaturan env di kernelspec BMLP tetap melekat pada kernel terdaftar.

## 14 Kapan pengujian dianggap selesai

- Kedua notebook telah di-restart, Run All, dan disimpan dengan output akhir.
- Tidak ada error atau warning yang belum diselesaikan.
- Seluruh tahapan preprocessing, clustering, inverse, dan klasifikasi sesuai kontrol pada panduan.
- Target selaras dan model dapat dipakai untuk predict dengan fitur yang benar.
- Semua 13 check folder manual lulus.
- ZIP final berisi file dari sesi final yang sama.
- Lembar hasil berisi catatan aktual, lokasi sesi, hasil, dan bukti yang relevan.

Pengujian ini menilai kebenaran eksekusi dan kesesuaian artefak. Keputusan penilaian resmi tetap mengikuti reviewer. Penjelasan metodologis tentang kategori lokasi dan label pseudo harus tetap terlihat pada notebook.
