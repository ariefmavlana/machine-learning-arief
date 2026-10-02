# Submission Machine Learning Arief Maulana

Proyek ini mengelompokkan transaksi dengan K-Means, lalu melatih model klasifikasi untuk memprediksi label cluster. Dataset dan notebook menggunakan berkas resmi kursus. Kedua notebook sudah dijalankan dari kernel baru; hasil analisis tersedia di [laporan implementasi](reports/hasil-implementasi.md).

## Berkas utama

- [ZIP submission](dist/BMLP_Arief_Maulana.zip).
- [Notebook Clustering](submission/BMLP_Arief_Maulana/[Clustering]_Submission_Akhir_BMLP_Arief_Maulana.ipynb).
- [Notebook Klasifikasi](submission/BMLP_Arief_Maulana/[Klasifikasi]_Submission_Akhir_BMLP_Arief_Maulana.ipynb).
- [Dokumentasi ketentuan](docs/submission/README.md).
- [Panduan test manual VS Code dan Jupyter](docs/submission/10-panduan-test-manual.md) serta [lembar pencatatan](docs/submission/11-lembar-hasil-test-manual.md).
- [Hasil pengujian ulang dari ZIP](reports/hasil-pengujian-ulang.md).
- [Metrik yang dapat dibaca program](reports/metrics.json) dan [checksum artefak](reports/manifest.json).

ZIP berisi dua notebook dengan output, lima model, dua CSV hasil clustering, dan CSV sumber untuk eksekusi ulang offline. Model `.h5` disimpan menggunakan `joblib.dump()` sesuai template.

## Hasil eksperimen

Dataset aktual: 2.537 baris dan 16 kolom. Setelah dropna, duplikat, dan outlier sesuai urutan template, tersisa 1.945 baris. Model utama menghasilkan dua cluster beranggotakan 980 dan 965 observasi; silhouette 0,572160. Model PCA dua komponen menghasilkan silhouette 0,601743 pada ruang PCA.

Decision Tree, Random Forest, dan Random Forest hasil tuning memperoleh accuracy serta F1 macro 1,0 pada 389 observasi testing; training berisi 1.556 observasi. Tuning menguji 18 kombinasi dengan 5-fold CV pada training.

Kode kategori Location menyumbang sekitar 95,73% dari jumlah varians fitur clustering dan sangat memengaruhi pembagian kelompok. Skor klasifikasi mengukur prediksi label K-Means tersebut. Data tidak menyediakan label fraud terverifikasi; kemampuan mendeteksi fraud dan kinerja seluruh pipeline pada transaksi baru belum diuji.

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

Untuk menguji tanpa mengubah artefak utama, jalankan `scripts/prepare_manual.ps1` dan ikuti [panduan manual](docs/submission/10-panduan-test-manual.md). Script mengambil salinan dari ZIP dengan output notebook kosong dan tanpa model/CSV hasil sebelumnya. Sesudah Run All dan Save di GUI, gunakan `scripts/manual_check.py --folder` terhadap lokasi sesi untuk pemeriksaan 13 kontrak hasil.

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

Analisis setiap cluster tersedia pada bagian interpretasi notebook. Penjelasan tambahan ditempatkan pada markdown `Penilaian (Opsional)` sesuai panduan submission. Jumlah code cell dan import mengikuti template asli. Penilaian akhir dilakukan oleh reviewer kursus.
