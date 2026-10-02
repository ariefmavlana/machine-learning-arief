# Hasil pengujian ulang dan kesiapan pengujian manual

[Panduan manual](../docs/submission/10-panduan-test-manual.md) · [Lembar hasil](../docs/submission/11-lembar-hasil-test-manual.md) · [Hasil replay JSON](retest-results.json)

Pengujian ulang pada sesi permintaan pengguna ini berhasil mengeksekusi kedua notebook langsung dari isi ZIP final. Salinan hanya diberi dua notebook dan CSV mentah; output sebelumnya dikosongkan dan model serta CSV hasil dibuat ulang oleh eksekusi cell.

## Hasil pengujian

| Pemeriksaan | Hasil |
| --- | --- |
| Suite proyek sebelum penambahan alat manual | 6 passed. |
| Suite lengkap setelah penambahan alat manual | 11 passed, termasuk lima tes untuk pemeriksa/persiapan manual. |
| Pemeriksa terhadap hasil replay ZIP | 13 dari 13 check lulus. |
| Kernel | Kernel baru untuk setiap notebook, memakai environment Python 3.12.14 dan sklearn 1.7.0. |
| Notebook Clustering | 35 code cell, 17 grafik, tanpa error atau warning tersimpan. |
| Notebook Klasifikasi | 13 code cell, tanpa error atau warning tersimpan. |
| CSV hasil replay | Nilai, kolom, dan urutan observasi sama dengan baseline. |
| Model dan CSV lama | Tidak disediakan sebagai input replay. |
| ZIP utama | Hash sebelum dan sesudah sama; tidak diganti oleh pengujian ulang. |
| Waktu replay dan pemeriksaan artefak | Sekitar 56 detik pada environment sesi ini; bukan estimasi untuk setiap komputer. |

Hash ZIP yang diuji: `6f86a2b72a018b0b1bbec15db23813e44a9ddf3c0214d34b17215caa8029c30d`. Lokasi salinan replay dan rincian setiap check tercatat pada `retest-results.json`.

## Hasil model yang berhasil direproduksi

- Data mentah 2.537 × 16, dengan 403 sel kosong dan 21 duplikat.
- Data hasil preprocessing 1.945 observasi, sepuluh fitur ditambah Target.
- Dua cluster: 980 dan 965 anggota; silhouette utama 0,5721599258.
- Silhouette PCA 0,6017426993; varians dua komponen 0,9731776820.
- Split klasifikasi 1.556 training dan 389 testing; 55 fitur.
- Decision Tree, Random Forest, dan Random Forest tuning: accuracy, precision macro, recall macro, F1 macro semuanya 1,0.
- Tuning: lima fold CV training, 18 kandidat, parameter terbaik n_estimators=200, max_depth=None, min_samples_leaf=1.

Skor klasifikasi tetap merupakan kemampuan memprediksi label hasil clustering. Pengujian ulang tidak menyediakan ground truth fraud ataupun evaluasi seluruh pipeline terhadap transaksi masa depan.

## Alat yang disiapkan untuk pengguna

`scripts/prepare_manual.ps1` menyediakan salinan input dari ZIP, membersihkan output notebook, mendaftarkan kernel lokal, dan menyimpan lokasi sesi. Script sudah dijalankan serta kernel BMLP berhasil terdeteksi. Pemeriksaan runtime menemukan kebutuhan `JUPYTER_DATA_DIR` lokal agar daftar kernel tidak mencoba membuat folder pada profil yang tidak dapat ditulis; pengaturan tersebut sudah ditambahkan pada script persiapan.

`scripts/manual_check.py` memeriksa sepuluh file, struktur dan output notebook, sumber dataset, label, inverse, prediksi clustering/PCA, split, metrik classifier, serta CV. Exit code 0 berarti semua 13 check lulus; exit code 1 berarti setidaknya satu check gagal.

Lima tes pemeriksa mencakup artefak baseline yang valid, Target yang berubah pada satu CSV, error notebook tersimpan, model mandatory hilang, dan persiapan folder yang tidak membawa output/model lama. Kegagalan buatan hanya dibuat pada salinan sementara.

## Batas cakupan

Kode notebook diuji melalui kernel Jupyter tanpa interaksi GUI. VS Code ditemukan pada komputer dan extension Python terdaftar, tetapi extension Jupyter tidak terdaftar pada pemeriksaan ini. Server Notebook/JupyterLab tidak terdapat di `.venv` proyek. Instalasi milik pengguna di environment lain tidak diasumsikan tidak ada.

Tampilan serta interaksi GUI VS Code atau Jupyter pada sesi pengguna belum diuji langsung. Panduan manual menyediakan kedua jalur, hasil expected tiap tahap, troubleshooting, uji negatif, dan lembar pencatatan yang belum ditandai Lulus oleh penguji manual.

ZIP, notebook utama, dan model submission tetap sama selama replay tersebut. Alat manual dan dokumentasi tidak dimasukkan ke dalam ZIP submission.

## Pembaruan narasi pada 3 Oktober 2026

Setelah replay, penjelasan tambahan pada kedua notebook dirapikan dan ZIP dikemas kembali. Narasi kini menekankan hasil per cluster, alasan metode, serta perbandingan model. Markdown bawaan template tetap dipertahankan. Kode perhitungan, output eksekusi, CSV, dan model tidak berubah.

Pemeriksaan versi terbaru menghasilkan 11 tes lulus serta 13/13 pemeriksaan artefak lulus. Isi ZIP sesuai dengan sepuluh berkas pada folder submission. Hash ZIP terbaru dan rincian perubahan tersedia di [catatan penyuntingan](narrative-review.json); hash pada bagian replay di atas merujuk pada versi sebelum penyuntingan. Hasil pemeriksaan terbaru tersedia di [manual-check-latest.json](manual-check-latest.json).
