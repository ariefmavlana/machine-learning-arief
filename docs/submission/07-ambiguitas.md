# Ambiguitas sumber dan interpretasi sementara

[Indeks](README.md) · [Kriteria](02-kriteria.md) · [Berkas](06-berkas-submission.md) · [Sumber](09-sumber.md)

Dokumen ini menjaga agar kontradiksi pada materi tidak berubah menjadi aturan yang seolah-olah telah dikonfirmasi. Semua interpretasi di bawah adalah panduan kerja sementara. Jika template asli atau reviewer memberikan jawaban berbeda, perbarui panduan terkait dan checklist.

## A1 Pilihan dataset

**Sumber:** pembuka R1 memperbolehkan dataset yang disediakan atau dicari sendiri. Panduan operasional R1 mewajibkan dataset proyek versi Google Drive dan melarang penggantian dengan versi Kaggle.

**Interpretasi sementara:** ikuti ketentuan yang lebih spesifik dan gunakan versi Google Drive. Tidak ada alasan mengasumsikan dataset lain disetujui untuk submission ini.

**Dampak:** [pengantar](01-pengantar.md#dataset-yang-digunakan) dan langkah load data.

## A2 Penghapusan kolom

**Sumber:** instruksi utama, K2 Basic, dan R3 meminta drop kolom ID, Address, serta Date. Daftar Reject K2 justru mencantumkan “Melakukan drop pada kolom yang memiliki keterangan ID, Address, dan Date.”

**Interpretasi sementara:** kemungkinan ada kekeliruan redaksi pada Reject, tetapi ini belum dikonfirmasi. Lakukan drop sesuai tiga bagian sumber yang konsisten dan catat kolom yang dihapus. Jangan diam-diam mengubah salinan sumber.

**Dampak:** K2 Basic, pemilihan fitur, dan seluruh tahapan berikutnya.

## A3 Cakupan histogram

**Sumber:** K1 Skilled R2 menyebut seluruh kolom numerik maupun kategorikal. Urutan R3 hanya menyebut histogram numerik.

**Interpretasi sementara:** cakup kedua jenis fitur mengikuti rubrik yang lebih lengkap. Distribusi kategorikal perlu divisualisasikan secara terbaca; bentuk persisnya dicocokkan dengan template/contoh karena sumber menggunakan istilah histogram.

**Dampak:** K1 Skilled dan Advanced; [tips visualisasi](05-tips-dan-analisis.md#saran-untuk-visualisasi).

## A4 Statistik deskriptif

**Sumber:** R2 mengizinkan minimal mean, min, atau max, dengan rekomendasi semua. R3 menyebut mean, min, dan max. Untuk kategorikal R2 mengatakan “minimal salah satu” tanpa daftar tegas; R3 menyebut mode.

**Interpretasi sementara:** tampilkan dan tulis mean, min, max numerik serta mode kategorikal sesuai bagian yang dikerjakan. Jangan membatasi bukti pada tabel tanpa penjelasan tertulis.

**Dampak:** K4 Basic dan Skilled; narasi karakteristik seluruh cluster.

## A5 Evaluasi klasifikasi pada Basic

**Sumber:** empat metrik berada di K5 Skilled pada R2. R3 menyebut tidak menampilkan accuracy dan F1 pada testing set sebagai alasan penolakan umum.

**Interpretasi sementara:** tampilkan minimal accuracy dan F1 testing set sejak Basic. Untuk Skilled dan Advanced, tampilkan accuracy, precision, recall, F1 seluruh algoritma; model tuning juga dievaluasi menurut R3.

**Dampak:** K5 dan kelulusan umum. Tidak ada nilai minimum metrik yang disebutkan.

## A6 Penanda code opsional

**Sumber:** R3 menaruh `MULAI CODE OPSIONAL` sebelum `train_test_split()`, Decision Tree, dan penyimpanan model, yang dinyatakan wajib pada K5 Basic serta Reject.

**Interpretasi sementara:** penanda tersebut tidak membatalkan ketentuan wajib. Split, Decision Tree, dan file model harus tetap dikerjakan.

**Dampak:** [alur klasifikasi](04-alur-notebook.md#notebook-klasifikasi). Penempatan cell perlu dipastikan pada template asli.

**Temuan implementasi:** template asli menempatkan penanda code opsional pada cell One Hot Encoding. Cell split dan Decision Tree berada di bagian wajib yang terpisah. Perbedaan urutan salinan R3 sudah dapat dijelaskan oleh struktur asli.

## A7 Model PCA

**Sumber:** K3 Advanced meminta “Membangun model menggunakan PCA” dan `joblib.dump(model,"PCA_model_clustering.h5")`. Teks tidak menjelaskan apakah `model` berisi estimator clustering pada data PCA, transformer PCA, atau rangkaian keduanya.

**Interpretasi sementara:** buat model clustering pembanding dengan representasi PCA; plot PCA saja belum cukup. Jangan menetapkan bentuk objek file sebagai ketentuan pasti sebelum melihat cell template dan harapan reviewer.

**Dampak:** K3 Advanced, evaluasi pembanding, dan `PCA_model_clustering.h5`. Pertahankan model clustering utama dan label yang konsisten.

**Temuan implementasi:** template meminta `kmeans_pca` baru, dilatih pada `data_final` hasil PCA dua komponen. File yang disimpan berisi K-Means fitted tersebut. Ketidakjelasan bentuk objek terselesaikan oleh cell asli.

## A8 Kategori pada CSV inverse

**Sumber:** K4 mengembalikan kategori asal melalui inverse. K5 Basic meminta memakai CSV inverse jika K4 Advanced, tetapi urutan klasifikasi tidak menyebut cell encoding ulang.

**Interpretasi sementara:** ikuti kewajiban memakai CSV inverse. Periksa cell preprocessing pada template untuk mengubah fitur kategorikal kembali ke representasi yang dapat dipakai classifier. Bila cell tersebut tidak tersedia, minta kejelasan di forum sebelum menambah code cell yang tidak diperintahkan.

**Dampak:** K4 Advanced → K5 Basic; [tips klasifikasi](05-tips-dan-analisis.md#klasifikasi-dari-data-inverse).

**Temuan implementasi:** template klasifikasi memiliki cell One Hot Encoding menggunakan `pd.get_dummies()`. Cell tersedia dan digunakan; penambahan code cell tidak diperlukan.

## A9 Syarat perhitungan nilai

**Sumber:** R1 menyatakan formula berlaku apabila “setiap kriteria mendapatkan nilai 2 pts atau tidak ada kriteria yang ditolak.” Redaksi tidak secara eksplisit mengatakan “minimal 2”.

**Interpretasi sementara:** untuk perencanaan, penuhi minimal Basic pada semua kelompok dan jangan menggunakan rata-rata untuk menutupi Reject. Status final kondisi Reject mengikuti reviewer.

**Dampak:** [penilaian](03-penilaian.md#rumus-nilai-akhir).

## A10 Rentang Bintang 2

**Sumber:** tabel R1 memuat rata-rata 1 sampai kurang dari 2 sebagai Bintang 2. Kelompok rubrik R2 hanya menyediakan 0, 2, 3, dan 4 pts.

**Interpretasi sementara:** pertahankan tabel konversi, tetapi jangan mengarang skor 1 untuk sebuah kriteria. Rentang tersebut tidak menjadi sasaran kerja karena seluruh Basic menghasilkan rata-rata 2.

**Dampak:** pembacaan nilai dan estimasi kelulusan.

## A11 Jumlah model dan best model

**Sumber:** R3 menyebut “Tiga model” tetapi kemudian menyebut dua mandatory (`model_clustering`, `decision_tree_model`) dan `best_model_classification` opsional. Contoh struktur justru memuat PCA, explore, tuning, tanpa best model.

**Interpretasi sementara:** dua model mandatory selalu disertakan; tambah PCA, explore, dan tuning sesuai level yang dikerjakan. Best model tetap opsional dan tidak menggantikan model wajib. Jangan menyebut tepat tiga model sebagai syarat yang telah terkonfirmasi.

**Dampak:** [manifest berkas](06-berkas-submission.md#daftar-artefak). Jika model tambahan lebih dari satu dibuat, simpan dan identifikasi hasilnya sesuai cell template.

## A12 File Python

**Sumber:** instruksi ekspor R3 menyebut mengunduh `.ipynb` dan `.py`, sementara daftar submission dan pohon ZIP hanya menyebut notebook `.ipynb`.

**Interpretasi sementara:** `.ipynb` wajib; `.py` adalah cadangan yang tidak dinyatakan sebagai lampiran wajib pada daftar tersebut.

**Dampak:** pengunduhan dan isi ZIP.

## A13 Nama dasar dan ekstensi model

**Sumber:** R2 menyebut nama dasar tanpa ekstensi untuk `model_clustering`, `explore_<Nama Algoritma>_classification`, dan `tuning_classification`; R3 memperlihatkan ketiganya dengan `.h5`.

**Interpretasi sementara:** gunakan nama `.h5` pada struktur berkas R3 dan metode `joblib.dump()` yang diminta R2. Ekstensi tidak mengubah serialisasi joblib menjadi HDF5.

**Dampak:** nama artefak dan pembacaan otomatis reviewer.

## A14 Binning dan inverse

**Sumber:** R3 menempatkan scaling sebelum binning, lalu meminta inverse numerik dan kategorikal. Tidak dijelaskan apakah fitur numerik asal dipertahankan atau diganti oleh kategori bin.

**Interpretasi sementara:** jelaskan satuan rentang bin dan simpan hubungan dengan fitur asli bila diizinkan template. Inverse encoder kategori bin tidak mengembalikan nilai numerik asal persis. Jangan mengklaim rekonstruksi yang tidak terjadi.

**Dampak:** K2 Advanced, K4 Skilled/Advanced, dan interpretasi satuan fitur.

**Temuan implementasi:** cell asli menambah kolom kategori baru dengan `pd.qcut()` dan mempertahankan fitur numerik asal. Implementasi menambah `CustomerAgeGroup`; CustomerAge tetap dapat dipulihkan dengan scaler. Ketidakjelasan pelestarian fitur asal terselesaikan.

## Penyelesaian ambiguitas

Prioritaskan pembacaan template yang diunduh untuk A6, A7, A8, dan A14. Jika ketidakjelasan masih berpengaruh pada isi kode atau objek model yang dikumpulkan, gunakan [forum diskusi yang dirujuk sumber](https://www.dicoding.com/academies/184/discussions).

Template asli kini telah diunduh dan diperiksa. Temuan pada A6, A7, A8, dan A14 dicatat di atas serta pada [laporan implementasi](../../reports/hasil-implementasi.md). Butir lain yang berasal dari kontradiksi redaksi masih berupa interpretasi kerja; belum ada konfirmasi reviewer.
