# Checklist persiapan dan pengiriman submission

[Indeks](README.md) · [Kriteria](02-kriteria.md) · [Alur](04-alur-notebook.md) · [Berkas](06-berkas-submission.md)

Checklist ini mencatat pemeriksaan implementasi final pada 2 Oktober 2026. Centang menunjukkan bukti internal telah diperiksa, bukan skor resmi reviewer. Item bertanda **saran** merupakan verifikasi tambahan, bukan rubrik baru. Temuan dan batas interpretasi tersedia pada [laporan implementasi](../../reports/hasil-implementasi.md).

## Persiapan dan aturan umum

- [x] Dataset memakai versi modifikasi Google Drive, bukan versi Kaggle.
- [x] Kedua notebook berasal dari template yang disediakan.
- [x] Struktur dan urutan template dipertahankan.
- [x] Import bawaan dijalankan tanpa tambahan yang tidak diminta.
- [x] Tidak ada baris atau code cell yang tidak diperlukan atau diperintahkan.
- [x] Markdown tambahan bernama `Penilaian (Opsional)`.
- [x] Penjelasan memakai metode, alasan, dan hasil aktual.
- [x] Python digunakan; tidak memakai AutoML yang dilarang.
- [x] Rekomendasi scikit-learn 1.7.0 dipertimbangkan; versi bukan diklaim wajib.
- [x] Butir ambigu yang memengaruhi implementasi dicocokkan dengan template atau jawaban reviewer.

## K1 Basic

- [x] `head()` memiliki output.
- [x] `info()` memiliki output.
- [x] `describe()` memiliki output.
- [x] Tidak ada error atau output yang hilang pada cell yang seharusnya menampilkan hasil.

## K2 Basic

- [x] `isnull().sum()` dijalankan dan ditampilkan.
- [x] `duplicated().sum()` dijalankan dan ditampilkan.
- [x] `dropna()` dijalankan untuk menangani missing.
- [x] `drop_duplicates()` dijalankan.
- [x] Kolom ID, Address, Date di-drop mengikuti interpretasi A2.
- [x] Fitur kategorikal di-encode menggunakan `LabelEncoder()`.
- [x] `columns.tolist()` dijalankan sesuai urutan R3.

## K3 Basic

- [x] Input model adalah dataset hasil preprocessing.
- [x] `describe()` sesudah preprocessing dijalankan sesuai R3.
- [x] Elbow divisualisasikan menggunakan `KElbowVisualizer()`.
- [x] Model menggunakan `sklearn.cluster.KMeans()`.
- [x] `joblib.dump()` menghasilkan `model_clustering.h5`.

## K4 Basic

- [x] Agregasi numerik ditampilkan dan dianalisis tertulis untuk setiap cluster.
- [x] Mean, min, max dilengkapi mengikuti rekomendasi dan urutan R3.
- [x] Karakteristik setiap cluster dijelaskan berdasarkan agregasi dan rentang.
- [x] Label clustering diberi nama persis `Target`.
- [x] Data hasil preprocessing dan `Target` diekspor ke `data_clustering.csv`.
- [x] **Saran:** label, tabel analisis, dan CSV cocok dengan model utama yang sama.

## K5 Basic dan evaluasi wajib umum

- [x] Dataset serta label berasal dari hasil notebook clustering.
- [x] `data_clustering_inverse.csv` digunakan jika K4 Advanced diterapkan.
- [x] `Target` tersedia dan dipisahkan dari fitur X.
- [x] `head()` dataset klasifikasi ditampilkan sesuai R3.
- [x] Pembagian data memakai `train_test_split()`.
- [x] Decision Tree dibangun dan dilatih.
- [x] `joblib.dump()` menghasilkan `decision_tree_model.h5`.
- [x] Accuracy pada testing set ditampilkan.
- [x] F1 pada testing set ditampilkan.

## Tambahan Skilled

- [x] K1: matriks korelasi ditampilkan.
- [x] K1: distribusi seluruh kolom numerik dan kategorikal divisualisasikan mengikuti A3.
- [x] K2: outlier ditangani dengan metode drop.
- [x] K2: fitur numerik di-scale menggunakan `StandardScaler()`.
- [x] K3: Silhouette Score dihitung dan ditampilkan.
- [x] K3: hasil clustering divisualisasikan.
- [x] K4: scaling numerik dikembalikan dengan `inverse_transform()`.
- [x] K4: encoding kategorikal dikembalikan dengan `inverse_transform()`.
- [x] K4: analisis numerik dan kategorikal inverse ditampilkan serta ditulis.
- [x] K4: karakteristik seluruh cluster dijelaskan dari agregasi inverse.
- [x] K5: minimal satu algoritma selain Decision Tree dilatih.
- [x] K5: accuracy, precision, recall, F1 seluruh algoritma ditampilkan.
- [x] K5: model tambahan disimpan sebagai `explore_<Nama Algoritma>_classification.h5`.
- [x] Seluruh Basic pada kriteria yang ditargetkan Skilled tetap terpenuhi.

## Tambahan Advanced

- [x] K1: label semua visualisasi tidak overlap dan terbaca.
- [x] K2: binning dilakukan pada satu sampai dua fitur numerik dengan rentang yang dijelaskan.
- [x] K2: hasil binning di-encode menggunakan `LabelEncoder`.
- [x] K3: model menggunakan PCA dibangun sebagai pembanding sesuai template.
- [x] K3: `PCA_model_clustering.h5` disimpan dengan joblib.
- [x] K4: data inverse digabungkan kembali dengan `Target` yang selaras.
- [x] K4: `data_clustering_inverse.csv` disimpan.
- [x] K5: salah satu model klasifikasi dituning hyperparameternya dan dilatih ulang.
- [x] K5: model tuning dievaluasi dengan accuracy, precision, recall, F1 sesuai R3.
- [x] K5: `tuning_classification.h5` disimpan.
- [x] Seluruh Skilled dan Basic pada kriteria yang ditargetkan Advanced tetap terpenuhi.

## Pemeriksaan teknis tambahan

- [x] **Saran:** kedua notebook dijalankan dari sesi bersih secara berurutan.
- [x] **Saran:** transformasi inverse memakai objek fitted dan urutan fitur yang benar.
- [x] **Saran:** jumlah serta posisi label selaras dengan data setelah penghapusan baris.
- [x] **Saran:** `Target` tidak menjadi fitur masukan clustering ataupun klasifikasi.
- [x] **Saran:** CSV tidak mengandung indeks tambahan yang tidak dimaksudkan sebagai fitur.
- [x] **Saran:** preprocessing klasifikasi yang perlu fit tidak di-fit pada testing set.
- [x] **Saran:** seluruh model dibandingkan pada pembagian testing set yang sama.
- [x] **Saran:** metode averaging metrik klasifikasi dijelaskan.
- [x] **Saran:** tuning memakai validasi data training, bukan testing set untuk pemilihan parameter.
- [x] **Saran:** seluruh angka dan narasi benar-benar sesuai output akhir.

## Pengiriman

- [x] Kedua notebook `.ipynb` tersedia dan output akhirnya tersimpan.
- [x] Tidak ada error pada notebook final.
- [x] `model_clustering.h5`, `decision_tree_model.h5`, dan `data_clustering.csv` tersedia.
- [x] Artefak PCA, explore, tuning, serta CSV inverse disertakan sesuai level yang dikerjakan.
- [x] `best_model_classification.h5`, bila dilampirkan, tidak menggantikan model wajib.
- [x] Placeholder nama siswa dan nama algoritma sudah diganti.
- [x] Semua pekerjaan dikumpulkan dalam satu folder dan satu ZIP.
- [x] **Saran:** ZIP dibuka untuk memeriksa file tidak hilang, kosong, atau tersarang berulang.
- [x] Kelengkapan diperiksa terhadap aturan umum dan setiap kriteria, bukan rata-rata saja.

## Catatan bukti yang dapat diisi

| Kriteria | Level yang dikerjakan | Lokasi cell atau bagian | Artefak | Hasil pemeriksaan |
| --- | --- | --- | --- | --- |
| K1 | Target Advanced | Clustering bagian 2 | 17 grafik termasuk clustering | Output dan keterbacaan diperiksa. |
| K2 | Target Advanced | Clustering bagian 3 | Data preprocessing | Inverse dan observasi sumber sesuai. |
| K3 | Target Advanced | Clustering bagian 4 | Dua model clustering | Prediksi model utama sesuai Target; PCA menerima dua fitur. |
| K4 | Target Advanced | Clustering bagian 5–6 | Narasi dan dua CSV | Label dan inverse selaras. |
| K5 | Target Advanced | Klasifikasi bagian 2–5 | Tiga model dan evaluasi | Split, metrik, tuning, dan model diperiksa. |
