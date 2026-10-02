# Ketentuan penilaian dan strategi pencapaian

[Indeks](README.md) · [Kriteria](02-kriteria.md) · [Ambiguitas](07-ambiguitas.md) · [Checklist](08-checklist.md)

Dokumen ini menyalin mekanisme nilai pada R1 dan menghubungkannya dengan lima kelompok kriteria pada R2. Contoh angka adalah simulasi perencanaan, bukan prediksi hasil reviewer.

## Rumus nilai akhir

`Nilai Akhir = Total Points / Jumlah Kriteria`

Dengan lima kelompok rubrik pada R2, perhitungan kerja adalah `(K1 + K2 + K3 + K4 + K5) / 5`. Setiap kelompok memiliki Reject 0, Basic 2, Skilled 3, dan Advanced 4 pts.

Catatan R1 berbunyi: “Perhitungan nilai akhir di atas digunakan apabila setiap kriteria mendapatkan nilai 2 pts atau tidak ada kriteria yang ditolak.” Kalimat tersebut ambigu. **Interpretasi sementara untuk perencanaan:** penuhi minimal Basic pada semua kriteria sebelum menghitung peluang lulus. Jangan memakai rata-rata untuk menutupi satu kriteria Reject; lihat [A9](07-ambiguitas.md#a9-syarat-perhitungan-nilai).

## Konversi nilai dari sumber

| Nilai akhir | Nilai Dicoding | Huruf | Level of Mastery | Makna |
| --- | --- | --- | --- | --- |
| Kurang dari 1 | Rejected | E | Tidak dicantumkan | Tidak lulus. |
| 1 sampai kurang dari 2 | Bintang 2 | D | Below Basic | Kurang. |
| 2 sampai kurang dari 3 | Bintang 3 | C | Basic | Cukup. |
| 3 sampai kurang dari 4 | Bintang 4 | B | Skilled | Mahir. |
| Tepat 4 | Bintang 5 | A | Advanced | Tingkat lanjut. |

R1 menggambarkan Basic sebagai memenuhi seluruh kompetensi minimal, Skilled sebagai memenuhi kompetensi dengan baik, dan Advanced sebagai memenuhi kompetensi dengan sangat baik. Baris Bintang 2 dipertahankan sesuai sumber walaupun rubrik yang diberikan tidak menyediakan skor 1; lihat [A10](07-ambiguitas.md#a10-rentang-bintang-2).

## Contoh perencanaan

| K1 | K2 | K3 | K4 | K5 | Total | Rata-rata | Konversi tabel |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | 2 | 2 | 2 | 10 | 2,0 | Bintang 3. |
| 3 | 3 | 3 | 3 | 3 | 15 | 3,0 | Bintang 4. |
| 4 | 4 | 4 | 4 | 3 | 19 | 3,8 | Bintang 4. |
| 4 | 4 | 4 | 4 | 4 | 20 | 4,0 | Bintang 5. |

Secara aritmetika, rata-rata 4 dengan maksimum 4 per kriteria membutuhkan lima skor 4. Empat kriteria Advanced dan satu Skilled belum mencapai Bintang 5.

Contoh `4, 4, 4, 4, 0` menghasilkan rata-rata aritmetika 3,2, tetapi **tidak layak disebut estimasi kelulusan** karena terdapat kriteria Reject. Hasil formal untuk kondisi tersebut belum dapat dipastikan dari redaksi yang diberikan.

## Strategi pengerjaan

1. **Amankan Basic:** semua cell wajib, label `Target`, penjelasan cluster, evaluasi accuracy dan F1 testing set, model wajib, CSV, serta notebook dengan output.
2. **Naikkan ke Skilled:** lengkapi visualisasi, handling outlier dan scaling, silhouette, inverse dan analisis kategorikal, model klasifikasi tambahan serta empat metrik seluruh model.
3. **Naikkan ke Advanced:** rapikan plot, binning satu sampai dua fitur, model pembanding PCA, CSV inverse, dan tuning klasifikasi.
4. **Ulangi pemeriksaan lintas dokumen:** peningkatan K4 ke Advanced mengubah dataset yang dipakai K5; tambahan algoritma mengubah daftar model dan evaluasi yang wajib dikumpulkan.

Ini saran urutan pengerjaan, bukan keharusan memperoleh skor seragam di semua kriteria. Nilai akhir tetap bergantung pada review dan kelengkapan aturan umum.
