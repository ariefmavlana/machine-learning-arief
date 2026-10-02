# Sumber dokumentasi dan keterlacakan

[Indeks](README.md) · [Pengantar](01-pengantar.md) · [Kriteria](02-kriteria.md) · [Ambiguitas](07-ambiguitas.md)

Dokumentasi disusun pada 2 Oktober 2026 dari materi pengguna. Pernyataan kurikulum adalah ringkasan materi tersebut, bukan konfirmasi bahwa halaman kursus daring saat ini identik. Referensi teknis digunakan hanya untuk menjelaskan perilaku alat dan saran pendamping.

## Materi utama pengguna

| Kode | Materi | Salinan lokal | Dipakai untuk |
| --- | --- | --- | --- |
| R1 | Pengantar, panduan dataset, formula nilai, tabel konversi, dan tautan tips dari pengguna. | [Transkripsi pengantar](sumber/01-pengantar.txt) | Tujuan, dataset, template, markdown, penilaian. |
| R2 | Berkas dengan pembuka “Submission ini mencakup dua tahap utama, yaitu Clustering dan Klasifikasi”. | [Berkas kriteria asli](sumber/02-kriteria-asli.txt) | Lima rubrik dan level penilaian. |
| R3 | Berkas dengan pembuka “Beberapa poin ini perlu diperhatikan ketika mengirimkan berkas submission”. | [Berkas ketentuan asli](sumber/03-ketentuan-berkas-asli.txt) | Template, urutan cell, file, alasan penolakan, ekspor, review. |

R2 dan R3 disalin dari attachment tanpa mengubah isinya; perbedaan atau kemungkinan salah ketik dipertahankan. R1 ditranskripsi dari pengantar yang dikirim pengguna dengan normalisasi tata letak tabel, spasi, dan baris kosong. Transkripsi bukan halaman kursus yang diunduh.

## Tautan dataset dan template dari sumber

- [Dataset clustering project versi Google Drive](https://drive.google.com/drive/folders/1Zs7VmPZ-jNwsRlMKH65Ea-LApSwx6lKx?hl=ID).
- [Template notebook Clustering](https://colab.research.google.com/drive/1nhbV-jBc9VwTw9nmrMMlnjWaMrPaS7JR?usp=sharing).
- [Template notebook Klasifikasi](https://colab.research.google.com/drive/1MW8dlA9_XL0WHsltwP1BnYwAA5SlfaWo?usp=sharing).
- [Forum diskusi Dicoding yang dirujuk R3](https://www.dicoding.com/academies/184/discussions).

Saat dokumentasi awal dibuat, tautan Colab belum dapat dibaca. Pada tahap implementasi berikutnya, kedua template berhasil diunduh melalui endpoint unduhan Drive. Folder dataset diperiksa dan file `bank_transactions_data_edited.csv` berhasil diunduh. Snapshot berada di [folder sources](../../sources/); hasil eksekusi dan audit dijelaskan di [laporan implementasi](../../reports/hasil-implementasi.md). Forum belum dibaca.

## Tautan gambar dari materi

| Sumber | Keterangan | Tautan |
| --- | --- | --- |
| R1 | Fig 1 Cell Import Library. | [Gambar import](https://assets.cdn.dicoding.com/original/academy/dos-aaae07b93e9e70a95d18b453a028ba8f20251105094826.png) |
| R1 | Fig 2 Struktur Markdown Clustering. | [Gambar markdown clustering](https://assets.cdn.dicoding.com/original/academy/dos-118f594d0e3af53fd8464c83d1c5770520251105110001.png) |
| R1 | Fig 3 Struktur Markdown Klasifikasi. | [Gambar markdown klasifikasi](https://assets.cdn.dicoding.com/original/academy/dos-985547d64d8d5418a1db9ed75800edd820251105110125.png) |
| R1 | Tips urutan clustering. | [Diagram clustering](https://assets.cdn.dicoding.com/original/academy/dos-1a6ac07e5b6deebbaa9b9e7492c62cba20250429144041.png) |
| R1 | Tips urutan klasifikasi. | [Diagram klasifikasi](https://assets.cdn.dicoding.com/original/academy/dos-a962968f062206df99c80e89604630e920250429141500.jpeg) |
| R2 | Fig 3 Visualisasi baik dan informatif 1. | [Contoh visualisasi 1](https://assets.cdn.dicoding.com/original/academy/dos-ddead116aa98f3997829cab72866856c20250429140014.jpeg) |
| R2 | Fig 4 Visualisasi baik dan informatif 2. | [Contoh visualisasi 2](https://assets.cdn.dicoding.com/original/academy/dos-e861e7bd7e83ebded895453e9e71a4ae20250429140013.jpeg) |
| R2 | Fig 5 Label tumpang tindih. | [Contoh label overlap](https://assets.cdn.dicoding.com/original/academy/dos-8e1502cda59a9ce75fcabafd94645a7220250429140013.jpeg) |
| R2 | Fig 6 Visualisasi kurang informatif. | [Contoh visualisasi kurang informatif](https://assets.cdn.dicoding.com/original/academy/dos-c85f1fe22a52c03303d0a4160945765e20250429140014.jpeg) |
| R2 | Gambar pada bagian interpretasi dan ekspor. | [Rujukan interpretasi](https://assets.cdn.dicoding.com/original/academy/dos-4bf1e1e72caa4ce02b4c4ed862e7392f20250429140014.jpeg) |
| R3 | Ekspor dari Colab. | [Gambar ekspor](https://assets.cdn.dicoding.com/original/academy/dos-af2140130c75598c90c944eef897e7ed20251105114100.png) |

Deskripsi pada tabel mengikuti caption atau konteks teks pengguna. Kedua diagram urutan dicoba dibaca tetapi tidak berhasil; gambar lainnya belum diperiksa. Dokumentasi tidak menyimpulkan detail visual yang tidak terlihat. Pada R2, nama tautan gambar interpretasi berbeda dengan URL tujuan; tabel memakai URL tujuan yang diberikan.

## Referensi teknis primer

Referensi berikut dibaca melalui web untuk memeriksa penjelasan teknis. Halaman `stable` atau `latest` dapat menunjuk versi berbeda dari scikit-learn 1.7.0 yang disarankan materi. Rujukan ini tidak menjadi alasan mengubah versi atau template submission.

| Referensi | Klaim yang didukung |
| --- | --- |
| [LabelEncoder scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) | Encoder target dan transformasi kembali label. |
| [StandardScaler scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) | Scaling serta `inverse_transform()`. |
| [PCA scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) | PCA sebagai pengurangan dimensi. |
| [Elbow Method Yellowbrick](https://www.scikit-yb.org/en/latest/api/cluster/elbow.html) | Penggunaan KElbowVisualizer untuk pemilihan k. |
| [joblib.dump](https://joblib.readthedocs.io/en/latest/generated/joblib.dump.html) | Persistensi objek Python melalui joblib. |
| [train_test_split scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) | Pembagian data, random state, dan stratifikasi. |
| [Common pitfalls scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html) | Konsistensi preprocessing dan pencegahan data leakage. |

## Pemetaan kebutuhan ke dokumen

| Kebutuhan pengguna | Acuan utama | Dokumen hasil |
| --- | --- | --- |
| Pengantar | R1 | [01 Pengantar](01-pengantar.md) |
| Kriteria utama | R2, aturan umum R3 | [02 Kriteria](02-kriteria.md) |
| Ketentuan penilaian | R1 dan level R2 | [03 Penilaian](03-penilaian.md) |
| Tips dan trick | R1, urutan R3, saran teknis primer | [04 Alur](04-alur-notebook.md), [05 Tips](05-tips-dan-analisis.md) |
| Ketentuan berkas | R3 dan kewajiban bersyarat R2 | [06 Berkas](06-berkas-submission.md) |
| Konflik dan kesiapan | R1, R2, R3 | [07 Ambiguitas](07-ambiguitas.md), [08 Checklist](08-checklist.md) |
