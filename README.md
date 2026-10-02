# Submission Machine Learning Arief Maulana

Implementasi dua tahap clustering dan klasifikasi berdasarkan template resmi serta dataset modifikasi dari Google Drive. Kedua notebook menargetkan seluruh kriteria Advanced dan telah dijalankan dari kernel baru. Hasil akhir dan batas interpretasinya tersedia di [laporan implementasi](reports/hasil-implementasi.md).

## Berkas utama

- [ZIP submission](dist/BMLP_Arief_Maulana.zip).
- [Notebook Clustering](submission/BMLP_Arief_Maulana/[Clustering]_Submission_Akhir_BMLP_Arief_Maulana.ipynb).
- [Notebook Klasifikasi](submission/BMLP_Arief_Maulana/[Klasifikasi]_Submission_Akhir_BMLP_Arief_Maulana.ipynb).
- [Dokumentasi ketentuan](docs/submission/README.md).
- [Metrik yang dapat dibaca program](reports/metrics.json) dan [checksum artefak](reports/manifest.json).

ZIP berisi dua notebook dengan output, lima model, dua CSV hasil clustering, dan snapshot CSV sumber untuk eksekusi ulang offline. Tidak ada AutoML. Model `.h5` menggunakan `joblib.dump()` sesuai template.

## Hasil eksperimen

Dataset aktual: 2.537 baris dan 16 kolom. Setelah dropna, duplikat, dan outlier sesuai urutan template, tersisa 1.945 baris. Model utama menghasilkan dua cluster beranggotakan 980 dan 965 observasi; silhouette 0,572160. Model PCA dua komponen menghasilkan silhouette 0,601743 pada ruang PCA.

Decision Tree, Random Forest, dan Random Forest hasil tuning memperoleh accuracy serta F1 macro 1,0 pada 389 observasi testing; training berisi 1.556 observasi. Tuning menguji 18 kombinasi dengan 5-fold CV pada training.

Interpretasi hasil harus mempertimbangkan bahwa kode kategori Location menyumbang sekitar 95,73% dari jumlah varians fitur clustering. Kedua label merupakan pembagian K-Means pada dataset ini, sehingga skor klasifikasi mengukur kemampuan meniru label tersebut. Ini belum menjadi bukti model fraud detection atau evaluasi seluruh pipeline pada transaksi baru.

## Menjalankan ulang

Environment kerja tersedia di `.venv` dengan Python 3.12 dan scikit-learn 1.7.0. Dari direktori proyek, jalankan:

```powershell
.\scripts\run.ps1
```

Script menyiapkan kernel lokal, mengisi ulang template, mengeksekusi dua notebook dari kernel bersih, memperbarui analisis berdasarkan hasil aktual, mengemas ZIP, dan menjalankan pemeriksaan integrasi. File output proyek akan diperbarui; simpan perubahan notebook manual terlebih dahulu bila ada.

Untuk environment baru, sediakan Python 3.12 dan uv, lalu gunakan:

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements-lock.txt
.\scripts\run.ps1
```

`requirements.txt` mencatat dependensi langsung. `requirements-lock.txt` mencatat seluruh versi yang terpasang saat verifikasi. Environment lokal dan konfigurasi Jupyter berada di workspace proyek.

Untuk eksekusi notebook secara manual, buka notebook dari folder `submission/BMLP_Arief_Maulana`, pilih kernel environment proyek, dan jalankan Clustering dahulu kemudian Klasifikasi. Semua CSV serta model memakai path relatif dalam folder yang sama. Import cell tetap sama persis dengan template.

## Struktur proyek

```text
sources/                    Template dan dataset resmi sebagai snapshot
submission/BMLP_Arief_Maulana/
                            Notebook dan artefak final
dist/                       ZIP untuk dikumpulkan
scripts/                    Pengisian template dan eksekusi reproducible
tests/                      Pemeriksaan kontrak submission
reports/                    Metrik, checksum, grafik, dan laporan
docs/submission/            Dokumentasi ketentuan dan checklist
```

Bagian jawaban interpretasi template diisi dengan hasil setiap cluster. Markdown tambahan bernama `Penilaian (Opsional)` mengikuti panduan pengguna. Penyesuaian kode pendamping dilakukan pada cell yang relevan untuk cakupan kategori, keterbacaan plot, evaluasi, serta bukti eksekusi; tidak ditambahkan code cell atau import baru. Nilai resmi tetap ditentukan reviewer.
