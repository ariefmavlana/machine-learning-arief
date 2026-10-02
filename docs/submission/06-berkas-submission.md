# Ketentuan berkas dan pengiriman submission

[Indeks](README.md) · [Kriteria](02-kriteria.md) · [Ambiguitas](07-ambiguitas.md) · [Checklist](08-checklist.md)

R3 meminta pekerjaan Python dalam satu folder yang dikompresi menjadi ZIP. Dua notebook wajib menggunakan template, telah dieksekusi, dan memiliki output sehingga reviewer tidak perlu menjalankannya ulang.

## Daftar artefak

| Nama file | Status menurut gabungan R2 dan R3 | Isi atau kegunaan |
| --- | --- | --- |
| `[Clustering]_Submission_Akhir_BMLP_Your_Name.ipynb` | Wajib. | Notebook clustering dari template dengan output. |
| `[Klasifikasi]_Submission_Akhir_BMLP_Your_Name.ipynb` | Wajib. | Notebook klasifikasi dari template dengan output. |
| `model_clustering.h5` | Wajib K3 Basic. | Model K-Means utama, disimpan menggunakan joblib. |
| `decision_tree_model.h5` | Wajib K5 Basic. | Decision Tree terlatih, disimpan menggunakan joblib. |
| `data_clustering.csv` | Wajib K4 Basic dan tercantum pada struktur R3. | Fitur hasil preprocessing dan `Target`. |
| `PCA_model_clustering.h5` | Wajib jika mengerjakan K3 Advanced. | Model pembanding berbasis PCA sesuai template. |
| `explore_<Nama Algoritma>_classification.h5` | Wajib jika mengerjakan K5 Skilled atau Advanced. | Model tambahan selain Decision Tree. |
| `tuning_classification.h5` | Wajib jika mengerjakan K5 Advanced. | Model hasil hyperparameter tuning. |
| `data_clustering_inverse.csv` | Wajib jika mengerjakan K4 Advanced. | Data inverse dan `Target`; digunakan notebook klasifikasi. |
| `best_model_classification.h5` | Opsional dalam narasi R3; tidak muncul pada contoh struktur atau rubrik R2. | Model klasifikasi terbaik jika dipilih untuk dilampirkan; bukan pengganti model wajib. |

Ganti placeholder nama siswa pada notebook dan ZIP secara konsisten. Untuk model tambahan, ganti `<Nama Algoritma>` dengan nama algoritma, misalnya `explore_RandomForest_classification.h5`; ini contoh penamaan, bukan nama yang telah dikonfirmasi template. Pertahankan kapitalisasi nama model tetap dan kolom `Target` sesuai sumber.

Kata “opsional” pada struktur R3 berarti opsional untuk jalur dasar. File tersebut menjadi wajib ketika level yang mensyaratkannya dikerjakan. Konflik narasi “tiga model” dibahas di [A11](07-ambiguitas.md#a11-jumlah-model-dan-best-model).

## Struktur ZIP

Berikut representasi struktur R3. Penanda pada komentar hanya penjelasan dokumentasi, bukan bagian nama file.

```text
BMLP_Nama-siswa.zip
├── [Clustering]_Submission_Akhir_BMLP_Your_Name.ipynb
├── [Klasifikasi]_Submission_Akhir_BMLP_Your_Name.ipynb
├── model_clustering.h5
├── PCA_model_clustering.h5                       # K3 Advanced
├── decision_tree_model.h5
├── explore_<Nama Algoritma>_classification.h5     # K5 Skilled atau Advanced
├── tuning_classification.h5                      # K5 Advanced
├── data_clustering.csv
└── data_clustering_inverse.csv                   # K4 Advanced
```

`best_model_classification.h5` tidak tercantum pada pohon asli tersebut. Jika dilampirkan sesuai narasi opsional, tambahkan sebagai file tersendiri dan pertahankan file lain yang diwajibkan.

Sumber meminta satu folder yang di-zip, sedangkan pohon menampilkan file langsung di bawah ZIP. **Saran:** kumpulkan semua artefak dalam satu folder kerja, buat satu ZIP, lalu periksa isinya mudah ditemukan dan tidak memiliki nesting berulang. Bentuk internal folder yang benar-benar diwajibkan belum dirinci.

## Ekspor notebook dari Colab

R3 mengarahkan membuka menu File lalu mengunduh `.ipynb` serta `.py`. Daftar artefak wajib hanya mencantumkan `.ipynb`; `.py` tidak muncul pada struktur submission. **Interpretasi sementara:** unduhan `.py` boleh disimpan sebagai cadangan lokal, tetapi tidak dinyatakan sebagai lampiran wajib. Lihat [A12](07-ambiguitas.md#a12-file-python).

Sebelum unduhan final, pastikan eksekusi telah selesai, tidak ada error, dan output sudah tersimpan. Pastikan semua model serta CSV yang dirujuk notebook ikut diunduh dari lingkungan Colab bila pengerjaan dilakukan di sana.

## Alasan penolakan umum

R3 mencantumkan hal berikut:

1. Tidak melampirkan file yang diminta.
2. Tidak menggunakan template yang disediakan.
3. Menambahkan line code atau code cell yang tidak diperlukan atau diperintahkan.
4. Tidak memberikan penjelasan hasil clustering.
5. Tidak menggunakan dataset dan label dari hasil clustering.
6. Model klasifikasi tidak menampilkan accuracy dan F1 pada testing set.
7. Menggunakan platform atau metode AutoML yang dilarang.

Daftar platform AutoML ada di [pengantar](01-pengantar.md#batasan-alat-dan-bahasa). Alasan Reject per kriteria tersedia di [rubrik](02-kriteria.md). Keduanya diperiksa bersama, bukan saling menggantikan.

## Pemeriksaan sebelum mengirim

Gunakan [checklist](08-checklist.md). Sebagai saran pengemasan, buka ZIP yang dihasilkan untuk memastikan kedua notebook, model, dan CSV benar-benar ada; jangan hanya memeriksa folder sebelum kompresi. Pastikan file tidak kosong dan notebook memperlihatkan output hasil akhir.

Dokumentasi pendamping dalam folder `docs/submission` tidak disebut sebagai artefak wajib. Pakai untuk persiapan dan audit; jangan menganggap semua dokumentasi perlu dimasukkan ke ZIP.

## Proses review

Menurut R3, reviewer mengulas paling lambat tiga hari kerja, tidak termasuk Sabtu, Minggu, dan libur nasional. Sumber menyarankan tidak submit berkali-kali karena dapat memperlama penilaian. Hasil diberitahukan lewat email atau status akun Dicoding.

Ketentuan waktu tersebut berasal dari teks pengguna, bukan verifikasi jadwal layanan terkini. Jika ada kesulitan atau perlu penyelesaian ambiguitas, sumber mengarahkan ke [forum diskusi Dicoding](https://www.dicoding.com/academies/184/discussions).
