# Alur pengerjaan notebook dan perpindahan data

[Indeks](README.md) · [Kriteria](02-kriteria.md) · [Tips](05-tips-dan-analisis.md) · [Berkas](06-berkas-submission.md)

Urutan berikut berasal dari komentar cell pada R3. Nomor di tabel adalah nomor langkah dokumentasi, bukan nomor cell asli. Pertahankan penempatan cell pada template yang diunduh; tabel ini membantu memeriksa urutan dan cakupan.

## Notebook clustering

| Langkah | Instruksi cell dari sumber | Kriteria atau status |
| --- | --- | --- |
| 1 | Import library bawaan. | Aturan umum; tidak menambah import. |
| 2 | Load data. | Dataset dari Drive. |
| 3 | Tampilkan lima baris pertama dengan `head()`. | K1 Basic. |
| 4 | Tinjau baris, kolom, dan jenis data dengan `info()`. | K1 Basic. |
| 5 | Tampilkan statistik dengan `describe()`. | K1 Basic. |
| 6 | Tampilkan korelasi antarfitur. | K1 Skilled. |
| 7 | Tampilkan histogram seluruh kolom numerik. | K1 Skilled; R2 juga meminta kategorikal. |
| 8 | Buat visualisasi lebih informatif. | K1 Advanced; label tidak overlap. |
| 9 | Periksa missing dengan `isnull().sum()`. | K2 Basic. |
| 10 | Periksa duplikat dengan `duplicated().sum()`. | K2 Basic. |
| 11 | Tangani data hilang dengan `dropna()`. | K2 Basic. |
| 12 | Hapus duplikat dengan `drop_duplicates()`. | K2 Basic. |
| 13 | Drop kolom Date, ID, dan IP Address. | K2 Basic; cocokkan cakupan Address di R2. |
| 14 | Encode fitur kategorikal dengan `LabelEncoder()`. | K2 Basic. |
| 15 | Last checking dengan `columns.tolist()`. | Instruksi R3. |
| 16 | Handling outlier menggunakan metode drop. | K2 Skilled. |
| 17 | Scale fitur numerik dengan `StandardScaler()`. | K2 Skilled. |
| 18 | Binning berdasarkan rentang pada satu sampai dua fitur numerik; encode hasilnya. | K2 Advanced menurut R2. |
| 19 | Gunakan `describe()` untuk memastikan input clustering merupakan data preprocessing. | Instruksi R3 dan K3. |
| 20 | Visualisasi Elbow dengan `KElbowVisualizer()`. | K3 Basic. |
| 21 | Bangun K-Means. | K3 Basic. |
| 22 | Simpan model dengan joblib. | `model_clustering.h5`. |
| 23 | Hitung dan tampilkan Silhouette Score. | K3 Skilled. |
| 24 | Visualisasikan hasil clustering. | K3 Skilled. |
| 25 | Bangun model menggunakan PCA. | K3 Advanced. |
| 26 | Simpan model pembanding PCA. | `PCA_model_clustering.h5`. |
| 27 | Tampilkan analisis numerik mean, min, max. | K4; R2 menyebut minimal salah satu. |
| 28 | Pastikan kolom hasil clustering bernama `Target`. | K4 Basic. |
| 29 | Simpan data. | `data_clustering.csv`. |
| 30 | Inverse data numerik ke rentang normal. | K4 Skilled. |
| 31 | Inverse kategori yang telah di-encode ke kategori asal. | K4 Skilled. |
| 32 | Analisis data inverse: mean, min, max numerik dan mode kategorikal. | K4 Skilled. |
| 33 | Periksa kembali data inverse. | Instruksi R3. |
| 34 | Simpan data inverse bersama `Target`. | K4 Advanced; `data_clustering_inverse.csv`. |

Tambahkan penjelasan pada bagian markdown yang diizinkan dengan nama `Penilaian (Opsional)`. Penjelasan tidak menggantikan code cell atau output yang diwajibkan.

## Notebook klasifikasi

| Langkah | Instruksi cell dari sumber | Kriteria atau status |
| --- | --- | --- |
| 1 | Import library bawaan. | Aturan umum. |
| 2 | Gunakan dataset hasil clustering yang memiliki `Target`. | K5 Basic; CSV inverse jika K4 Advanced. |
| 3 | Tampilkan lima baris pertama dengan `head()`. | Instruksi R3. |
| 4 | Bagi dataset menggunakan `train_test_split()`. | K5 Basic. |
| 5 | Buat dan latih Decision Tree. | K5 Basic. |
| 6 | Simpan model. | `decision_tree_model.h5`. |
| 7 | Latih minimal satu algoritma scikit-learn selain Decision Tree. | K5 Skilled; contoh sumber: Random Forest. |
| 8 | Tampilkan accuracy, precision, recall, F1 seluruh algoritma. | K5 Skilled; accuracy dan F1 testing set juga syarat umum. |
| 9 | Simpan model selain Decision Tree. | `explore_<Nama Algoritma>_classification.h5`. |
| 10 | Tuning hyperparameter dan latih ulang salah satu model. | K5 Advanced. |
| 11 | Tampilkan accuracy, precision, recall, F1 model tuning. | Instruksi R3. |
| 12 | Simpan model tuning. | `tuning_classification.h5`. |

R3 menempatkan penanda `MULAI CODE OPSIONAL` sebelum pembagian data. **Interpretasi sementara:** split dan Decision Tree tetap wajib karena K5 Basic dan Reject menyebutnya eksplisit. Jangan menghilangkan langkah tersebut. Lihat [A6](07-ambiguitas.md#a6-penanda-code-opsional).

Untuk target Basic, evaluasi testing set tetap harus tersedia di cell relevan yang diizinkan template. Inspeksi template asli pada tahap implementasi mengonfirmasi adanya cell One Hot Encoding sebelum split, serta cell evaluasi baseline dan tuning. Implementasi mempertahankan seluruh code cell asli; lihat [laporan implementasi](../../reports/hasil-implementasi.md).

## Kontrak data antartahap

| Data | Isi | Ketentuan penggunaan |
| --- | --- | --- |
| Dataset sumber | Data tanpa label dari Drive. | Input awal clustering. |
| Fitur hasil preprocessing | Baris yang lolos pembersihan dan fitur yang diolah. | Input K-Means; jangan masukkan `Target` ke fitur clustering. |
| `data_clustering.csv` | Fitur preprocessing dan label `Target` hasil clustering. | Wajib diekspor; input klasifikasi ketika tidak menerapkan K4 Advanced. |
| Data inverse | Representasi fitur yang dikembalikan dengan transformer yang sama dan label yang selaras. | Analisis K4 Skilled. |
| `data_clustering_inverse.csv` | Fitur hasil inverse dan `Target`. | Wajib untuk K4 Advanced; menjadi input K5 menurut R2. |
| X klasifikasi | Kolom fitur tanpa `Target`. | Masukan model klasifikasi. |
| y klasifikasi | Kolom `Target`. | Label yang diprediksi. |

Istilah “data training” pada ekspor K4 merujuk pada data hasil preprocessing yang diberi label menurut teks sumber. Urutan R3 baru melakukan train/test split di notebook klasifikasi; jangan mengasumsikan CSV wajib hanya berisi subset `X_train` klasifikasi.

## Saran pemeriksaan konsistensi

Pastikan label ditambahkan ke baris yang benar setelah `dropna()`, penghapusan duplikat, dan drop outlier. Jumlah label harus sama dengan jumlah observasi yang masuk model utama. Gunakan indeks atau urutan baris yang dipertahankan secara konsisten.

Jaga label model utama ketika membuat model pembanding PCA. Jika keduanya memakai jumlah cluster atau penomoran berbeda, jangan menimpa `Target` tanpa keputusan yang jelas. Analisis cluster, file CSV, dan model yang menghasilkan label harus merujuk ke hasil yang sama.

Ekspor CSV tanpa indeks tambahan merupakan **saran teknis** untuk mencegah kolom indeks terbaca sebagai fitur. Encoding ulang kategorikal untuk klasifikasi CSV inverse dibahas di [tips](05-tips-dan-analisis.md#klasifikasi-dari-data-inverse).
