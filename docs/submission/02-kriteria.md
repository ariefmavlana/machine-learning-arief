# Kriteria utama dan bukti penilaian

[Indeks](README.md) · [Penilaian](03-penilaian.md) · [Alur](04-alur-notebook.md) · [Checklist](08-checklist.md)

R2 memuat lima kelompok rubrik. K1–K4 dikerjakan pada clustering; K5 pada klasifikasi. Skilled mewarisi semua Basic, dan Advanced mewarisi semua Skilled. Memenuhi fitur Advanced saja tidak menutup kekurangan pada level sebelumnya.

## K1 Menampilkan dan memahami dataset

| Level | Ketentuan | Bukti yang diperiksa |
| --- | --- | --- |
| Basic 2 pts | Tampilkan dataset dengan `head()`, informasi dengan `info()`, serta statistik dengan `describe()`. | Ketiga output tersimpan dan dapat dibaca. |
| Skilled 3 pts | Semua Basic; matriks korelasi; histogram untuk semua kolom, numerik maupun kategorikal. | Korelasi dan visualisasi mencakup seluruh kolom. |
| Advanced 4 pts | Semua Skilled; visualisasi tanpa label yang saling overlap. | Judul, sumbu, tick, dan legenda terbaca. |

**Reject 0 pts:** tidak menampilkan salah satu dari `head()`, `info()`, `describe()`; cell yang seharusnya menampilkan output tidak memiliki output atau mengalami error.

Cakupan histogram berbeda pada urutan cell R3 yang hanya menyebut numerik. [A3](07-ambiguitas.md#a3-cakupan-histogram) mencatat interpretasinya. Perapian plot bukan alasan menghilangkan fitur yang sulit ditampilkan.

## K2 Melakukan preprocessing

| Level | Ketentuan | Bukti yang diperiksa |
| --- | --- | --- |
| Basic 2 pts | Periksa missing dengan `isnull().sum()` dan duplikat dengan `duplicated().sum()`; tangani missing dengan `dropna()`; hapus duplikat dengan `drop_duplicates()`; drop kolom ID, Address, Date; gunakan `LabelEncoder()` untuk fitur kategorikal. | Output pemeriksaan, operasi yang diminta, dan hasil preprocessing. |
| Skilled 3 pts | Semua Basic; handling outlier dengan metode drop; `StandardScaler()` untuk fitur numerik. | Metode dan hasil penghapusan outlier serta fitur yang di-scale. |
| Advanced 4 pts | Semua Skilled; binning berdasarkan rentang nilai pada satu sampai dua fitur numerik; encode hasil binning dengan `LabelEncoder`. | Fitur terpilih, rentang bin, kategori bin, dan hasil encoding. |

**Reject 0 pts menurut R2:** tidak mengecek missing dan duplikat; tidak menjalankan `dropna()`; tidak menjalankan `drop_duplicates()`; tidak menggunakan `LabelEncoder()`; serta satu poin drop kolom yang bertentangan dengan Basic.

Poin kontradiktif berbunyi “Melakukan drop pada kolom yang memiliki keterangan ID, Address, dan Date.” Dokumen ini tidak menganggapnya telah dikoreksi secara resmi. **Interpretasi sementara:** lakukan drop karena instruksi utama, Basic, dan urutan R3 sepakat; lihat [A2](07-ambiguitas.md#a2-penghapusan-kolom).

Walaupun pemeriksaan menemukan nol missing atau duplikat, tetap jalankan operasi yang diwajibkan dan laporkan hasil sebenarnya. Jangan membuat masalah data buatan untuk menunjukkan pembersihan.

## K3 Membangun model clustering

| Level | Ketentuan | Bukti yang diperiksa |
| --- | --- | --- |
| Basic 2 pts | Gunakan data hasil preprocessing; visualisasikan Elbow dengan `KElbowVisualizer()`; gunakan `sklearn.cluster.KMeans()`; simpan model dengan `joblib.dump()` bernama dasar `model_clustering`. | Data input, plot Elbow, model terlatih, dan `model_clustering.h5` sesuai R3. |
| Skilled 3 pts | Semua Basic; hitung dan tampilkan Silhouette Score; visualisasikan hasil clustering. | Nilai silhouette dan plot dengan label cluster terbaca. |
| Advanced 4 pts | Semua Skilled; bangun model menggunakan PCA; simpan model pembanding melalui `joblib.dump(model,"PCA_model_clustering.h5")`. | Proses PCA, model pembanding, dan file dengan nama persis. |

**Reject 0 pts:** tidak menggunakan data hasil preprocessing; tidak memakai `KElbowVisualizer()`; tidak menggunakan K-Means; tidak menjalankan penyimpanan `model_clustering` dengan `joblib.dump()`.

Walaupun daftar Basic tidak mengulang syarat dataset preprocessing, syarat itu tercantum pada instruksi utama dan Reject sehingga tetap wajib. Tidak ada jumlah cluster baku pada sumber. PCA sebagai model pembanding dan objek yang disimpan perlu dicocokkan dengan template; lihat [A7](07-ambiguitas.md#a7-model-pca).

## K4 Menginterpretasi cluster dan mengekspor data

| Level | Ketentuan | Bukti yang diperiksa |
| --- | --- | --- |
| Basic 2 pts | Tampilkan dan tulis analisis numerik minimal mean, min, atau max; jelaskan karakteristik setiap cluster dari agregasi; ekspor data training hasil preprocessing bersama label bernama `Target`. | Tabel agregasi, narasi semua cluster, dan `data_clustering.csv`. |
| Skilled 3 pts | Semua Basic; kembalikan encoding dan scaling melalui `inverse_transform()`; tampilkan dan tulis analisis numerik dan kategorikal; jelaskan karakteristik cluster dari agregasi tersebut. | Data inverse, agregasi numerik, ringkasan kategorikal, dan narasi per cluster. |
| Advanced 4 pts | Semua Skilled; gabungkan data inverse dengan hasil cluster; simpan sebagai `data_clustering_inverse.csv` dengan kolom `Target`. | CSV inverse dan kesesuaian label per baris. |

**Reject 0 pts:** tidak menjelaskan karakteristik setiap cluster berdasarkan rentangnya; tidak mengekspor data preprocessing bersama label atau tidak menamai kolomnya `Target`.

R2 sangat merekomendasikan mean, min, dan max sekaligus. Urutan R3 menyebut ketiganya dan mode untuk kategorikal. **Interpretasi sementara:** tampilkan mean, min, max, serta mode agar bukti memenuhi redaksi yang lebih lengkap. R2 tidak mendefinisikan secara tegas pilihan statistik kategorikal; lihat [A4](07-ambiguitas.md#a4-statistik-deskriptif).

Skilled mewajibkan proses inverse dan analisisnya; Advanced menambahkan penyimpanan CSV inverse. Klasifikasi harus memakai CSV inverse apabila K4 Advanced diterapkan, menurut K5 Basic.

## K5 Membangun dan mengevaluasi klasifikasi

| Level | Ketentuan | Bukti yang diperiksa |
| --- | --- | --- |
| Basic 2 pts | Gunakan `Target` dari clustering; gunakan `data_clustering_inverse.csv` jika K4 Advanced; split dengan `train_test_split()`; bangun Decision Tree; simpan dengan `joblib.dump()` sebagai `decision_tree_model.h5`. | Dataset input, X dan y, pembagian data, model, serta file wajib. |
| Skilled 3 pts | Semua Basic; coba minimal satu algoritma selain Decision Tree; tampilkan accuracy, precision, recall, F1 seluruh algoritma; simpan model tambahan dengan nama dasar `explore_<Nama Algoritma>_classification`. | Perbandingan evaluasi dan file `.h5` menurut struktur R3. |
| Advanced 4 pts | Semua Skilled; tuning hyperparameter pada salah satu model klasifikasi; simpan dengan nama dasar `tuning_classification`. | Proses tuning, evaluasi model tuning menurut urutan R3, dan `tuning_classification.h5`. |

**Reject 0 pts pada rubrik:** target tidak bernama `Target`; tidak memakai `train_test_split()`; tidak membangun Decision Tree; tidak menjalankan penyimpanan `decision_tree_model.h5`.

**Aturan umum R3 yang juga berlaku pada Basic:** model klasifikasi harus menampilkan accuracy dan F1 pada testing set. Penempatan evaluasi lengkap di Skilled tidak menghapus aturan umum ini. Lihat [A5](07-ambiguitas.md#a5-evaluasi-klasifikasi-pada-basic).

Decision Tree wajib tetap ada ketika model tambahan atau model tuning menghasilkan skor lebih baik. Daftar model wajib dan bersyarat tersedia pada [ketentuan berkas](06-berkas-submission.md).

## Aturan lintas kriteria

Gunakan dataset dan template yang diminta, simpan output, hindari error, berikan penjelasan clustering, serta patuhi larangan AutoML dan kode tambahan yang tidak diperintahkan. Daftar lengkap alasan penolakan umum ada di [ketentuan berkas](06-berkas-submission.md#alasan-penolakan-umum).
