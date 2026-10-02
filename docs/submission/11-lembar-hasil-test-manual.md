# Lembar hasil pengujian manual submission

[Panduan lengkap](10-panduan-test-manual.md) · [Indeks](README.md) · [Hasil tes otomatis](../../reports/hasil-pengujian-ulang.md)

Gunakan lembar ini untuk mencatat pengujian yang Anda lakukan di VS Code atau Jupyter. Status seluruh baris dimulai dari **Belum diuji** karena hasil otomatis tidak menggantikan pengamatan GUI oleh penguji. Isi status Lulus, Gagal, atau Tidak diterapkan, lalu tambahkan bukti dan penjelasan.

## Identitas sesi

| Informasi | Catatan penguji |
| --- | --- |
| Nama penguji | Belum diisi. |
| Tanggal dan waktu pengujian | Belum diisi; gunakan waktu lokal Asia Jakarta. |
| Aplikasi dan versinya | Belum diisi. |
| Folder sesi manual | Salin nilai folder dari `.cache/manual-session.json`. |
| Kernel terpilih | Belum diisi; expected Python 3 BMLP dan executable `.venv` proyek. |
| Versi Python dan scikit-learn | Belum diisi; expected Python 3.12 dan sklearn 1.7.0. |
| Dataset | bank_transactions_data_edited.csv dari ZIP resmi proyek. |
| Perubahan data atau parameter | Catat Tidak ada, atau jelaskan perubahan aktual. |

## Penyiapan dan Clustering

| Kasus | Kriteria lulus ringkas | Status | Bukti atau catatan |
| --- | --- | --- | --- |
| P01 | Salinan awal berisi dua notebook output kosong dan satu CSV mentah. | Belum diuji | — |
| P02 | Kernel `.venv`, path dan versi benar, CSV terbaca. | Belum diuji | — |
| C01 | Import bawaan berhasil. | Belum diuji | — |
| C02 | Data mentah 2.537 × 16; head/info/describe ada. | Belum diuji | — |
| C03 | Korelasi lima fitur dan lima histogram numerik tampil. | Belum diuji | — |
| C04 | Boxplot, sebelas distribusi kategori, violinplot terbaca. | Belum diuji | — |
| C05 | Missing 403 sel dan duplikat 21 terdeteksi. | Belum diuji | — |
| C06 | Dropna menyisakan 2.156 baris, missing nol. | Belum diuji | — |
| C07 | Drop duplikat menyisakan 2.135 baris, duplikat nol. | Belum diuji | — |
| C08 | Tujuh kolom ID/IP/date dihapus, sembilan fitur tersisa. | Belum diuji | — |
| C09 | Empat fitur nominal di-LabelEncode, daftar kolom benar. | Belum diuji | — |
| C10 | Filter IQR berurutan menyisakan 1.945 baris. | Belum diuji | — |
| C11 | Scaling numerik berjalan; LoginAttempts menjadi nol. | Belum diuji | — |
| C12 | CustomerAgeGroup menambah fitur kesepuluh tanpa menghapus usia asal. | Belum diuji | — |
| C13 | Elbow silhouette dan K-Means dua cluster berjalan. | Belum diuji | — |
| C14 | model_clustering.h5 terbentuk. | Belum diuji | — |
| C15 | Silhouette sekitar 0,572160 dan scatter cluster tampil. | Belum diuji | — |
| C16 | Model PCA terbentuk; silhouette sekitar 0,601743. | Belum diuji | — |
| C17 | Agregasi mean/min/max dan narasi kedua cluster tersedia. | Belum diuji | — |
| C18 | Target benar dan CSV preprocessing diekspor. | Belum diuji | — |
| C19 | Inverse numerik/kategori serta analisis tersedia. | Belum diuji | — |
| C20 | CSV inverse 1.945 × 11; Target selaras 980/965. | Belum diuji | — |

## Klasifikasi dan eksekusi akhir

| Kasus | Kriteria lulus ringkas | Status | Bukti atau catatan |
| --- | --- | --- | --- |
| K01 | CSV inverse dibaca dan head tampil. | Belum diuji | — |
| K02 | One Hot Encoding berjalan, Target bukan fitur. | Belum diuji | — |
| K03 | Split 1.556 training/389 testing dengan 55 fitur. | Belum diuji | — |
| K04 | Decision Tree dilatih dan disimpan. | Belum diuji | — |
| K05 | Random Forest serta kedua evaluasi baseline tersedia. | Belum diuji | — |
| K06 | CV training lima fold, 18 kombinasi; parameter terbaik sesuai baseline. | Belum diuji | — |
| K07 | Evaluasi tuning tampil dan model disimpan. | Belum diuji | — |
| F01 | Restart dan Run All Clustering, simpan count 1–35. | Belum diuji | — |
| F02 | Restart dan Run All Klasifikasi, simpan count 1–13. | Belum diuji | — |
| F03 | manual_check terhadap folder sesi menghasilkan 13/13 PASS dan exit 0. | Belum diuji | — |
| F04 | ZIP sesi final berisi sepuluh artefak, tanpa file diagnosis/cache. | Belum diuji | — |
| F05 | Kedua notebook dalam ZIP masih mempunyai output dan penjelasan aktual. | Belum diuji | — |

## Uji negatif tambahan

| Kasus | Kegagalan yang diharapkan | Status | Bukti atau catatan |
| --- | --- | --- | --- |
| N01 | Klasifikasi sebelum Clustering gagal karena CSV inverse belum ada. | Belum diuji | — |
| N02 | Training sebelum split gagal karena variabel belum dibuat. | Belum diuji | — |
| N03 | Model hilang pada salinan tambahan terdeteksi. | Belum diuji | — |
| N04 | Target diubah pada satu CSV terdeteksi. | Belum diuji | — |
| N05 | Error tersimpan pada notebook terdeteksi. | Belum diuji | — |

Jika tidak menjalankan uji negatif GUI, isi Tidak diterapkan dengan alasan. Tes regresi otomatis sudah menilai tiga skenario perubahan artefak; status otomatisnya tersedia pada laporan tes ulang, sedangkan tabel ini tetap mencatat tindakan penguji manual.

## Catatan masalah dan penyelesaian

| Informasi | Catatan penguji |
| --- | --- |
| Kasus pertama yang gagal | Belum ada catatan manual. |
| Pesan error lengkap | Belum ada catatan manual. |
| Langkah untuk mereproduksi | Belum ada catatan manual. |
| Perbaikan yang dilakukan | Belum ada catatan manual. |
| Hasil setelah perbaikan | Belum ada catatan manual. |
| Nama atau lokasi screenshot | Belum ada catatan manual. |

## Penutupan sesi

- [ ] Seluruh kasus wajib telah dicatat.
- [ ] Kedua notebook final tidak menyimpan error dari uji negatif.
- [ ] Nama folder pada report pemeriksa sesuai sesi yang diuji.
- [ ] File ZIP berasal dari sesi final yang sama.
- [ ] Interpretasi label cluster tidak berubah menjadi klaim fraud tanpa ground truth.

Kesimpulan penguji belum diisi. Catat Lulus atau Gagal berdasarkan bukti pada sesi ini, bukan hanya berdasarkan laporan pengujian otomatis sebelumnya.
