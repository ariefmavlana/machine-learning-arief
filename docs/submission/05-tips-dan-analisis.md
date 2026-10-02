# Tips pengerjaan dan penulisan analisis

[Indeks](README.md) · [Kriteria](02-kriteria.md) · [Alur](04-alur-notebook.md) · [Ambiguitas](07-ambiguitas.md)

Bagian ini memisahkan tips yang tertulis pada materi pengguna dari saran teknis pendamping. Semua saran harus ditempatkan dalam struktur template dan tidak menjadi alasan menambah kode yang tidak diperintahkan.

## Tips yang tercantum dalam sumber

R1 menyarankan memenuhi Basic dahulu, kemudian Skilled dan Advanced. Notebook dijalankan tanpa error. Pada import dependencies, cukup jalankan cell yang disediakan.

Untuk dokumentasi analisis, R1 menyarankan tiga unsur: **metode yang digunakan, alasan penggunaan, dan hasil yang didapat**. Markdown tambahan diberi nama `Penilaian (Opsional)`. R2 sangat merekomendasikan mean, min, dan max sekaligus untuk analisis numerik.

R1 menautkan gambar urutan pengerjaan clustering dan klasifikasi. Isi gambar belum berhasil diverifikasi; [alur notebook](04-alur-notebook.md) memakai urutan teks R3, bukan pembacaan diagram yang diasumsikan. Tautannya tersimpan di [sumber](09-sumber.md#tautan-gambar-dari-materi).

## Pola markdown analisis

Gunakan pola berikut di lokasi markdown yang diizinkan:

```markdown
### Penilaian (Opsional)

**Metode yang digunakan:** [teknik yang benar-benar dijalankan].

**Alasan penggunaan:** [hubungan teknik dengan masalah dan fitur dataset].

**Hasil yang didapat:** [output aktual, angka, dan interpretasi yang didukung hasil].
```

Teks dalam kurung siku adalah isian, bukan hasil eksperimen. Isi sesudah notebook dijalankan. Jangan membuat angka contoh seolah-olah merupakan output dataset.

| Bagian | Informasi yang perlu dijelaskan |
| --- | --- |
| EDA | Struktur data, distribusi, missing, duplikat, serta pola yang terlihat. |
| Pembersihan | Jumlah baris sebelum dan sesudah, kolom yang dibuang, alasan, dan dampaknya. |
| Encoding dan scaling | Fitur yang diolah dan makna perubahan representasinya. |
| Binning | Satu sampai dua fitur yang dipilih, batas interval, label, dan alasan rentang. |
| Elbow | Rentang k yang dicoba, bentuk kurva, dan dasar pilihan jumlah cluster. |
| Clustering | Jumlah anggota, kualitas pemisahan yang ditunjukkan output, serta batas interpretasi. |
| Inverse dan agregasi | Statistik dalam satuan asli, kategori dominan, dan perbedaan setiap cluster. |
| Klasifikasi | Dataset input, pembagian data, metrik testing set, dan perbandingan model. |
| Tuning | Model dan parameter yang dicoba, cara validasi, pilihan terbaik, serta hasil akhirnya. |

## Saran untuk visualisasi

K1 Skilled meminta distribusi seluruh fitur; K1 Advanced meminta label tidak overlap. Atur ukuran gambar, susunan subplot, rotasi tick, judul, dan jarak elemen di cell visualisasi yang disediakan. Periksa output yang tersimpan, bukan hanya ukuran saat plot dibuka terpisah.

Untuk kategorikal, distribusi frekuensi atau bar chart sering lebih bermakna daripada histogram numerik atas kode kategori. **Interpretasi teknis:** karena R2 menyebut “histogram” untuk kategorikal juga, pastikan hasil memenuhi maksud distribusi semua kolom dan cocokkan dengan contoh/template. Jangan menyatakan bentuk alternatif telah disetujui reviewer.

Kolom berkardinalitas tinggi memerlukan perhatian khusus. Mengambil beberapa kategori teratas saja tidak membuktikan bahwa seluruh distribusi sudah tercakup. Jelaskan setiap pengelompokan atau pembatasan dan cocokkan dengan ketentuan template.

## Saran untuk preprocessing dan inverse

Simpan pemetaan encoder untuk setiap kolom dan scaler yang digunakan, setidaknya sebagai objek dalam notebook. Gunakan objek fitted yang sama untuk inverse. `StandardScaler.inverse_transform()` mengembalikan representasi scaled ke skala asal; susunan fitur saat inverse harus sesuai susunan saat fit. [Dokumentasi StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).

Dokumentasi scikit-learn menempatkan `LabelEncoder` sebagai encoder target `y`, sementara rubrik submission meminta alat ini untuk fitur kategorikal. **Saran kepatuhan:** tetap gunakan alat yang diminta rubrik, dengan encoder terpisah untuk setiap fitur dan pemetaan yang dicatat; jelaskan bahwa nomor kategori bukan ukuran besar-kecil kategori. [Dokumentasi LabelEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html).

**Penjelasan teknis:** inverse encoding hasil binning hanya mengembalikan kategori bin, bukan nilai numerik persis sebelum binning. Bila fitur asli diperlukan untuk analisis, pertahankan representasinya dan hubungan barisnya sejak awal, sejauh diizinkan cell template. Jangan melaporkan kategori rentang sebagai nilai asli yang telah direkonstruksi.

Urutan R3 menempatkan scaling sebelum binning. Cocokkan satuan batas bin dengan data yang digunakan: batas pada nilai scaled berbeda dari batas pada satuan asli. Tuliskan fitur, satuan, batas, dan label bin agar analisis dapat dipahami.

## Saran untuk Elbow dan PCA

`KElbowVisualizer` membantu menilai perubahan skor ketika jumlah cluster berubah. Bentuk kurva yang tidak memiliki elbow jelas perlu diakui dalam analisis; pilihan k harus terkait hasil yang terlihat. [Dokumentasi Elbow Yellowbrick](https://www.scikit-yb.org/en/latest/api/cluster/elbow.html).

PCA adalah teknik pengurangan dimensi. Plot dua komponen utama saja belum membuktikan bahwa model pembanding dibangun pada data PCA. **Temuan template asli:** cell Advanced meminta PCA dua komponen, kemudian K-Means baru yang dilatih pada data tersebut. File pembanding menyimpan K-Means fitted itu. [Dokumentasi PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html), [A7](07-ambiguitas.md#a7-model-pca).

## Saran untuk interpretasi setiap cluster

Tampilkan jumlah anggota sebagai konteks tambahan, lalu hubungkan narasi ke agregasi aktual. Untuk numerik, jelaskan mean dan rentang min–max; untuk kategorikal, jelaskan mode. Jika beberapa kategori berbagi frekuensi tertinggi, jangan menyatakan ada satu kategori dominan tanpa dukungan.

Pola narasi yang dapat diisi: “Cluster [id] berisi [jumlah] observasi. Fitur [nama] memiliki mean [nilai], min [nilai], dan max [nilai]. Mode fitur [kategori] adalah [nilai]. Dibandingkan cluster lain, kelompok ini memiliki [perbedaan yang ditunjukkan tabel].”

Gunakan nama deskriptif seperti transaksi bernilai relatif tinggi hanya ketika agregasi mendukungnya. Jangan memberi label fraud atau aman tanpa bukti label eksternal yang sah.

## Klasifikasi dari data inverse

CSV inverse dapat mengandung kategori string. **Temuan template asli:** cell One Hot Encoding menggunakan `pd.get_dummies()` pada fitur object sebelum split. Implementasi menggunakan cell tersebut tanpa menambah import atau code cell. Lihat [A8](07-ambiguitas.md#a8-kategori-pada-csv-inverse).

Pisahkan `Target` dari X. Untuk preprocessing klasifikasi yang memerlukan fit, fit pada training set dan transform testing set dengan objek yang sama. Hindari memilih parameter menggunakan testing set; gunakan validasi dalam data training untuk tuning, kemudian laporkan hasil test. [Panduan resmi scikit-learn tentang data leakage](https://scikit-learn.org/stable/common_pitfalls.html).

Saran untuk split: gunakan pembagian yang konsisten antaralgoritma; tetapkan `random_state` bila diizinkan; pertimbangkan `stratify=y` ketika jumlah anggota setiap kelas mencukupi. Stratifikasi menjaga proporsi kelas, tetapi tidak selalu dapat digunakan pada kelas yang sangat sedikit anggotanya. [Dokumentasi train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html).

Sebutkan apakah precision, recall, dan F1 diringkas dengan macro atau weighted agar perbandingan model jelas. Ini saran pelaporan, bukan syarat averaging dari rubrik. Akurasi tinggi pada label clustering tidak otomatis membuktikan kemampuan mendeteksi fraud atau generalisasi pada transaksi masa depan.

## Saran untuk pemeriksaan akhir

Restart sesi dan jalankan semua cell berurutan, lalu simpan notebook dengan output. Ini membantu menemukan variabel yang hanya tersedia karena cell pernah dijalankan di luar urutan. Pastikan file model berasal dari eksekusi akhir yang sama dengan evaluasi dan CSV.

Ekstensi `.h5` pada submission tetap mengikuti nama yang diminta. Penyimpanan `joblib.dump()` adalah serialisasi objek Python; memberi ekstensi `.h5` tidak menjadikannya format HDF5. Jangan mengganti mekanisme ke penyimpanan Keras hanya karena ekstensi tersebut. [Dokumentasi joblib.dump](https://joblib.readthedocs.io/en/latest/generated/joblib.dump.html).
