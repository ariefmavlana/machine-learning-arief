# Pengantar dan ruang lingkup submission

[Indeks](README.md) · [Kriteria](02-kriteria.md) · [Alur notebook](04-alur-notebook.md) · [Sumber](09-sumber.md)

Dokumen ini menjelaskan hasil yang hendak dicapai, sumber dataset, dan aturan penggunaan notebook. Dasarnya adalah R1, dengan ketentuan berkas dari R3.

## Tujuan proyek

Submission mengintegrasikan unsupervised learning dan supervised learning. Clustering mengelompokkan observasi berdasarkan fitur pada dataset tanpa label. Label hasil clustering ditambahkan sebagai `Target`, lalu menjadi target pelatihan model klasifikasi.

Hubungan kedua tahap harus dapat ditelusuri: dataset klasifikasi berasal dari hasil notebook clustering. Sumber R3 menyebut penggunaan dataset atau label yang tidak berasal dari clustering sebagai alasan penolakan.

**Penjelasan konseptual:** keberhasilan klasifikasi menunjukkan kemampuan meniru pembagian cluster yang dibuat sebelumnya. Label cluster tidak otomatis menjadi label fraud yang telah diverifikasi; nama dataset transaksi tidak cukup untuk menyimpulkan bahwa suatu cluster adalah penipuan.

## Dataset yang digunakan

Walaupun paragraf pembuka memberi pilihan dataset, panduan operasional kemudian mewajibkan dataset yang disediakan. **Interpretasi sementara:** gunakan versi [dataset clustering project di Google Drive](https://drive.google.com/drive/folders/1Zs7VmPZ-jNwsRlMKH65Ea-LApSwx6lKx?hl=ID), bukan versi Kaggle. Lihat [A1](07-ambiguitas.md#a1-pilihan-dataset).

Menurut R1, dataset Drive adalah modifikasi dari “Bank Transaction Dataset for Fraud Detection” di Kaggle agar sesuai capaian penilaian. Snapshot resmi yang digunakan pada implementasi adalah `bank_transactions_data_edited.csv`, dengan 2.537 baris dan 16 kolom. Hasil pemeriksaan kualitas data tersedia pada [laporan implementasi](../../reports/hasil-implementasi.md).

R2 memberi contoh kolom untuk dihapus: `TransactionID`, `AccountID`, `DeviceID`, `IPAddress`, `MerchantID`, dan `TransactionDate`. Kata “seperti” berarti contoh tersebut bukan daftar lengkap. Inventarisasikan semua kolom yang berketerangan ID, Address, dan Date sesuai dataset serta instruksi template. Konflik redaksi aturan drop dicatat di [A2](07-ambiguitas.md#a2-penghapusan-kolom).

## Template dan struktur notebook

- Gunakan [template Clustering](https://colab.research.google.com/drive/1nhbV-jBc9VwTw9nmrMMlnjWaMrPaS7JR?usp=sharing).
- Gunakan [template Klasifikasi](https://colab.research.google.com/drive/1MW8dlA9_XL0WHsltwP1BnYwAA5SlfaWo?usp=sharing).
- Isi bagian kosong sesuai struktur dan urutan yang disediakan.
- Pada import dependencies, cukup jalankan cell bawaan; R1 menyatakan tidak perlu menambahkan apa pun.
- R3 melarang tambahan baris atau code cell yang tidak diperlukan atau diperintahkan.
- Pertahankan markdown bawaan. Jika menambahkan markdown penjelasan, gunakan nama `Penilaian (Opsional)` sesuai R1.
- Jalankan notebook tanpa error dan simpan output sebelum dikumpulkan.

Pada tahap dokumentasi awal, tautan template belum dapat dibaca. Pada implementasi berikutnya, kedua notebook asli berhasil diunduh dan diperiksa. [Alur notebook](04-alur-notebook.md) menormalisasi urutan komentar R3; temuan tambahan dari template, termasuk One Hot Encoding klasifikasi dan bentuk model PCA, tersedia pada [laporan implementasi](../../reports/hasil-implementasi.md).

## Batasan alat dan bahasa

Gunakan Python. R2 **menyarankan** scikit-learn `1.7.0` untuk mengurangi konflik pemeriksaan; sumber tidak menyebutnya sebagai syarat wajib tersendiri.

R3 melarang AutoML. Daftar yang disebut: PyCaret, Auto-sklearn, Google Cloud AutoML, H2O Driverless AI, Microsoft Azure Automated Machine Learning, TPOT, DataRobot, RapidMiner Auto Model, Amazon SageMaker Autopilot, dan IBM Watson AutoAI. Larangan berlaku pada metode atau platform AutoML, bukan hanya nama dalam daftar contoh.

Hyperparameter tuning tetap tercantum pada K5 Advanced. Kerjakan tuning model yang dipilih dalam batas template; jangan memakai larangan AutoML sebagai alasan menghilangkan syarat tersebut.

## Hasil yang diharapkan

| Tahap | Bukti utama | Digunakan oleh |
| --- | --- | --- |
| EDA | `head()`, `info()`, `describe()`, visualisasi sesuai level | Pemahaman fitur dan keputusan preprocessing. |
| Preprocessing | Pemeriksaan dan pembersihan, drop kolom, encoding; scaling, outlier, binning sesuai level | Model clustering. |
| Clustering | Elbow, K-Means, model tersimpan, evaluasi sesuai level | Interpretasi dan pembuatan `Target`. |
| Interpretasi | Agregasi dan penjelasan per cluster, CSV; inverse sesuai level | Pemilihan dataset klasifikasi. |
| Klasifikasi | Split, Decision Tree, model tersimpan, evaluasi testing set | Bukti kompetensi supervised learning. |
| Pengiriman | Dua notebook dengan output dan artefak sesuai level dalam ZIP | Pemeriksaan reviewer. |

Tidak ada batas minimum accuracy, F1, atau silhouette numerik pada teks yang diberikan. Kewajiban menampilkan metrik tidak boleh diubah menjadi angka minimum yang tidak bersumber.
