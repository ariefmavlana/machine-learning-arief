"""Execute notebooks in fresh kernels, derive evidence, annotate, and package."""

from pathlib import Path
import asyncio
import base64
import hashlib
import json
import os
import platform
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
os.environ['IPYTHONDIR'] = str(ROOT / '.ipython')
os.environ['JUPYTER_CONFIG_DIR'] = str(ROOT / '.jupyter')
os.environ['JUPYTER_RUNTIME_DIR'] = str(ROOT / '.jupyter' / 'runtime')
os.environ['JUPYTER_PATH'] = str(ROOT / '.jupyter' / 'share' / 'jupyter')
os.environ['MPLBACKEND'] = 'module://matplotlib_inline.backend_inline'
os.environ['MPLCONFIGDIR'] = str(ROOT / '.cache' / 'matplotlib')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import joblib
import nbformat
import numpy as np
import pandas as pd
import sklearn
from nbclient import NotebookClient
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, silhouette_score
from sklearn.model_selection import train_test_split

from build_notebooks import OUTPUT, NAMES

REPORTS = ROOT / 'reports'
FIGURES = REPORTS / 'figures'


def markdown_table(frame):
    """Render simple tables without requiring optional tabulate in the notebook."""
    headers = ['Fitur'] + [str(c) for c in frame.columns]
    rows = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---']*len(headers)) + ' |']
    for index, values in frame.iterrows():
        cells = [str(index)] + [f'{v:.4f}' if isinstance(v, (float, np.floating)) else str(v) for v in values]
        rows.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(rows)


def optional(title, text):
    cell = nbformat.v4.new_markdown_cell(f'### Penilaian (Opsional)\n\n**{title}**\n\n{text}')
    # Official templates use nbformat 4.0, which predates top-level cell IDs.
    cell.pop('id', None)
    return cell


def annotate_cluster(notebook, encoded, inverse, report):
    numeric = report['numerical_columns']
    labels = sorted(inverse.Target.unique())
    scaled_sections, inverse_sections = [], []
    for target in labels:
        group = inverse[inverse.Target == target]
        scaled = encoded[encoded.Target == target]
        count = len(group)
        scaled_stats = scaled[numeric].agg(['mean', 'min', 'max']).T
        native_stats = group[numeric].agg(['mean', 'min', 'max']).T
        category_modes = []
        for col in group.select_dtypes('object'):
            modes = group[col].mode().tolist()
            frequency = group[col].value_counts().iloc[0]
            category_modes.append(f'- **{col}:** mode {", ".join(map(str, modes))}; '
                                  f'frekuensi maksimum {frequency}/{count} ({frequency/count:.1%}).')
        mean_age = group.CustomerAge.mean()
        age_context = 'sedikit lebih tinggi' if mean_age > inverse.CustomerAge.mean() else 'sedikit lebih rendah'
        age_mean = f'{mean_age:.2f}'
        amount_mean = f'{group.TransactionAmount.mean():.2f}'
        balance_mean = f'{group.AccountBalance.mean():.2f}'
        section = f'### Cluster {int(target)}\n\n**Jumlah anggota:** {count} ({count/len(inverse):.2%}).\n\n'
        scaled_sections.append(section + markdown_table(scaled_stats) +
            f'\n\nRata-rata TransactionAmount pada cluster ini adalah '
            f'{scaled.TransactionAmount.mean():.4f}, sedangkan CustomerAge '
            f'{scaled.CustomerAge.mean():.4f}. Keduanya dekat dengan nol, sehingga anggota kelompok '
            'tidak jauh berbeda dari rata-rata data bersih pada dua fitur tersebut. '
            f'Rata-rata kode Location adalah {scaled.Location.mean():.2f}; '
            'perbedaan kode lokasi antarkelompok lebih besar daripada perbedaan fitur numerik. '
            'Kode lokasi akan dibaca kembali sebagai nama kota pada bagian inverse.\n\n'
            'Angka pada tabel masih dalam skala StandardScaler. Nilai negatif berarti berada '
            'di bawah rata-rata, bukan nilai transaksi negatif. LoginAttempts bernilai nol '
            'untuk semua anggota karena filter IQR menyisakan nilai asli 1.')
        inverse_sections.append(section + markdown_table(native_stats) + '\n\n' + '\n'.join(category_modes) +
            f'\n\nRata-rata usia anggota adalah {age_mean} tahun, {age_context} dari '
            f'rata-rata seluruh data bersih ({inverse.CustomerAge.mean():.2f} tahun). '
            f'Usia anggota tetap mencakup {group.CustomerAge.min():.0f}–{group.CustomerAge.max():.0f} tahun. '
            f'Rata-rata nilai transaksi {amount_mean}, dengan rentang '
            f'{group.TransactionAmount.min():.2f}–{group.TransactionAmount.max():.2f}; '
            f'rata-rata saldo {balance_mean}. Satuan moneter mengikuti dataset. '
            'Rentang transaksi yang lebar menunjukkan bahwa anggota tidak memiliki nilai transaksi yang seragam.\n\n'
            f'Transaksi yang paling sering adalah {group.TransactionType.mode().iloc[0]}, '
            f'dan kanal yang paling sering adalah {group.Channel.mode().iloc[0]}. '
            f'Pekerjaan dengan frekuensi tertinggi adalah {group.CustomerOccupation.mode().iloc[0]}; '
            f'kelompok usia yang paling sering adalah {group.CustomerAgeGroup.mode().iloc[0]}. '
            f'Anggota berasal dari {group.Location.nunique()} kota. '
            'Mode pada daftar di atas hanya menunjukkan kategori yang paling sering muncul. '
            'Sebagai contoh, kota dengan frekuensi tertinggi tidak mewakili seluruh lokasi dalam cluster.')
    notebook.cells[71].source = '\n'.join(notebook.cells[71].source.splitlines()[:2]) + '\n\n' + '\n\n'.join(scaled_sections)
    notebook.cells[79].source = '\n'.join(notebook.cells[79].source.splitlines()[:2]) + '\n\n' + '\n\n'.join(inverse_sections)
    prep = report['preprocessing']
    boundaries = report['age_bins_original_scale']
    additions = [
        (22, optional('Pemeriksaan awal data',
            '**Metode:** struktur data diperiksa dengan head, info, dan describe. Korelasi Pearson '
            'dan histogram digunakan untuk fitur numerik. Frekuensi kategori, boxplot, dan '
            'violinplot digunakan untuk melihat kategori serta sebaran nilai transaksi.\n\n'
            '**Alasan:** pemeriksaan ini membantu mengenali nilai kosong, duplikat, dan perbedaan '
            'sebaran sebelum data dibersihkan. Nama kota dan pekerjaan ditampilkan sebagai frekuensi '
            'kategori. Untuk kolom dengan banyak kategori, sebagian label sumbu disembunyikan '
            'agar terbaca; seluruh batang tetap ditampilkan.\n\n'
            f'**Hasil:** CSV yang dibaca berisi {report["raw_rows"]} baris dan {report["raw_columns"]} kolom, '
            f'dengan {report["raw_missing_cells"]} sel kosong dan {report["raw_duplicates"]} baris duplikat. '
            'Jumlah baris ini berbeda dari keterangan 2.512 sampel pada template. '
            'Analisis berikutnya menggunakan jumlah yang diperoleh dari CSV. '
            'Kolom ID dan tanggal masih ditampilkan pada pemeriksaan awal, lalu dihapus sebelum clustering.')),
        (51, optional('Pembersihan data dan kelompok usia',
            '**Metode:** baris dengan nilai kosong dan duplikat dihapus. Kolom ID, IP, dan tanggal '
            'dikeluarkan, lalu setiap fitur kategori dikodekan dengan LabelEncoder. Outlier numerik '
            'dihapus dengan batas 1,5 IQR, fitur numerik distandardisasi, dan CustomerAge dibagi '
            'menjadi tiga kelompok menggunakan qcut.\n\n'
            '**Alasan:** scaling menyamakan skala fitur numerik untuk perhitungan jarak. '
            'Encoder dan scaler disimpan dalam variabel yang sama untuk proses inverse. '
            'Kelompok usia ditambahkan sebagai fitur baru agar nilai usia asal tetap tersedia. '
            'qcut membentuk kelompok berdasarkan kuantil data bersih.\n\n'
            f'**Hasil:** {report["raw_rows"]} → {prep["after_dropna"]} sesudah dropna → '
            f'{prep["after_duplicates"]} sesudah duplikat → {prep["final_rows"]} sesudah outlier. '
            f'Kolom yang dibuang: {", ".join(report["dropped_columns"])}. '
            f'Batas kelompok usia pada skala asli: {", ".join(f"{v:.2f}" for v in boundaries)} tahun. '
            'Binning dijalankan setelah scaling. StandardScaler mempertahankan urutan nilai, '
            'sehingga kelompok kuantilnya sama dengan kelompok pada skala usia asli. '
            'Nama 1_Muda, 2_Dewasa, dan 3_Senior digunakan untuk membedakan rentang pada dataset ini.\n\n'
            'Filter IQR pada LoginAttempts memiliki batas bawah dan atas yang sama, yaitu 1. '
            'Akibatnya, semua baris dengan lebih dari satu percobaan login terhapus. '
            'Fitur ini menjadi konstan dan tidak lagi membedakan anggota cluster. '
            'Penghapusan tersebut juga perlu dipertimbangkan jika data dipakai untuk analisis anomali.')),
        (67, optional('Pemilihan jumlah cluster dan perbandingan PCA',
            '**Metode:** KElbowVisualizer membandingkan silhouette untuk k=2–9. K-Means dilatih '
            'pada sepuluh fitur hasil preprocessing. Model pembanding dilatih pada dua komponen PCA. '
            'Kedua model menggunakan random_state=42 dan n_init=10.\n\n'
            '**Alasan:** silhouette digunakan untuk membandingkan pemisahan kelompok pada setiap k. '
            'PCA merangkum fitur menjadi dua dimensi untuk visualisasi dan percobaan clustering kedua.\n\n'
            f'**Hasil:** k={report["clustering"]["clusters"]}; silhouette utama '
            f'{report["clustering"]["silhouette"]:.6f}; silhouette ruang PCA '
            f'{report["pca"]["silhouette"]:.6f}; dua komponen menjelaskan '
            f'{report["pca"]["explained_variance"]:.2%} varians. '
            'Silhouette PCA lebih tinggi, tetapi dihitung pada ruang yang berbeda. '
            'Perbandingan ini perlu dibaca bersama perubahan representasi fitur. '
            'Label Target untuk tahap klasifikasi diambil dari K-Means utama.\n\n'
            f'Location menyumbang {report["clustering"]["location_variance_share"]:.2%} dari jumlah varians '
            'fitur masukan. Kolom ini berupa kode LabelEncoder dan tidak ikut scaling fitur numerik. '
            'Pengaruhnya terhadap jarak jauh lebih besar daripada fitur lain. '
            'Selisih kode nama kota tidak menunjukkan jarak geografis, sehingga cluster perlu '
            'ditafsirkan sebagai hasil dari representasi tersebut. Penambahan kelompok usia juga '
            'membuat usia terwakili oleh dua fitur.')),
        (82, optional('Mengembalikan satuan data dan menyimpan label',
            '**Metode:** hasil preprocessing disimpan bersama Target. Nilai numerik dan kategori '
            'dikembalikan dengan inverse_transform, kemudian diringkas melalui mean, min, max, '
            'dan mode sebelum CSV inverse disimpan.\n\n'
            '**Alasan:** satuan asli memudahkan pembacaan usia, transaksi, dan saldo. '
            'Label serta urutan baris dipertahankan agar kedua CSV merujuk pada observasi yang sama.\n\n'
            f'**Hasil:** kedua CSV berisi {len(encoded)} baris dengan Target yang identik. '
            'CSV tidak memuat indeks tambahan. CustomerAgeGroup kembali ke kategori bin, sedangkan '
            'CustomerAge asli kembali ke nilai tahun. Notebook klasifikasi memakai '
            'data_clustering_inverse.csv dan cell One Hot Encoding bawaan. '
            'CSV mentah juga disertakan agar notebook dapat dijalankan kembali tanpa mengunduh data. '
            'Rata-rata usia dan transaksi kedua cluster berdekatan; perbedaan utamanya berkaitan '
            'dengan kode Location. Data tidak menyediakan label fraud yang terverifikasi, '
            'sehingga nomor cluster tidak digunakan sebagai kategori aman atau penipuan.')),
    ]
    for index, cell in sorted(additions, key=lambda x: x[0], reverse=True):
        notebook.cells.insert(index+1, cell)


def annotate_classification(notebook, report):
    records = report['classification']
    table = pd.DataFrame(records).set_index('name')[['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']]
    tuning = report['tuning']
    additions = [
        (9, optional('Data masukan dan pembagian train–test',
            '**Metode:** data diambil dari CSV inverse. Kolom string diubah dengan pd.get_dummies '
            'dan drop_first=True. Pembagian data menggunakan test_size=0.2, random_state=42, '
            'serta stratify=y. Target menjadi y dan dikeluarkan dari fitur X.\n\n'
            '**Alasan:** One Hot Encoding mewakili setiap kategori dengan indikator tersendiri. '
            'Stratifikasi menjaga proporsi kedua kelas pada train dan test. Semua model menggunakan '
            'pembagian yang sama agar hasilnya dapat dibandingkan.\n\n'
            f'**Hasil:** {report["split"]["train"]} training dan {report["split"]["test"]} testing; '
            f'{report["split"]["features"]} fitur masukan sesudah encoding. '
            'Encoding dilakukan sebelum split sesuai urutan notebook, sehingga kategori yang '
            'tersedia berasal dari seluruh dataset. Jika pipeline digunakan untuk transaksi baru, '
            'encoding perlu dilatih pada data training lalu diterapkan pada data testing.')),
        (16, optional('Perbandingan Decision Tree dan Random Forest',
            '**Metode:** Decision Tree baseline dan Random Forest 200 pohon; classification_report '
            'serta tabel accuracy, precision macro, recall macro, F1 macro pada testing set.\n\n'
            '**Alasan:** Decision Tree digunakan sebagai model awal. Random Forest menggabungkan '
            'prediksi beberapa pohon untuk pembanding. Precision, recall, dan F1 dirata-ratakan '
            'secara macro agar setiap kelas memiliki bobot yang sama.\n\n'
            '**Hasil:**\n\n' + markdown_table(table.iloc[:2]) + '\n\n'
            'Kedua model memperoleh nilai 1,0 untuk seluruh metrik: semua 389 label testing '
            'diprediksi sesuai Target. Hasil ini menunjukkan bahwa pembagian K-Means dapat '
            'dipelajari oleh kedua model pada split tersebut. Pengaruh Location yang besar pada '
            'clustering membantu menjelaskan mengapa label mudah dipisahkan.\n\n'
            'Target berasal dari clustering yang dilakukan sebelum split klasifikasi. '
            'Skor ini mengukur prediksi label cluster pada dataset yang digunakan. '
            'Kemampuan mendeteksi fraud atau kinerja seluruh pipeline pada transaksi baru '
            'belum diuji dengan evaluasi ini.')),
        (20, optional('Hasil pencarian parameter Random Forest',
            '**Metode:** GridSearchCV pada Random Forest, 18 kombinasi, 5-fold CV pada training, '
            'scoring accuracy sesuai template, dan refit estimator terbaik pada seluruh training.\n\n'
            '**Alasan:** cross-validation membandingkan parameter pada data training. '
            'Data testing digunakan setelah pencarian selesai.\n\n'
            f'**Hasil:** parameter terpilih adalah {tuning["best_params"]}; accuracy CV terbaik '
            f'{tuning["best_cv_accuracy"]:.6f}.\n\n' + markdown_table(table.iloc[2:]) + '\n\n'
            'Metrik testing tetap 1,0, sama dengan Random Forest awal. Pencarian parameter '
            'tidak memberi peningkatan pada split ini. File tuning_classification.h5 menyimpan '
            'objek GridSearchCV yang sudah dilatih, termasuk best_estimator_ dan cv_results_.')),
    ]
    for index, cell in sorted(additions, key=lambda x: x[0], reverse=True):
        notebook.cells.insert(index+1, cell)


def derive_report():
    raw = pd.read_csv(OUTPUT / 'bank_transactions_data_edited.csv')
    encoded = pd.read_csv(OUTPUT / 'data_clustering.csv')
    inverse = pd.read_csv(OUTPUT / 'data_clustering_inverse.csv')
    numeric = raw.select_dtypes('number').columns.tolist()
    cleaned = raw.dropna()
    after_dropna = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    after_duplicates = len(cleaned)
    steps = []
    for col in numeric:
        before = len(cleaned)
        q1, q3 = cleaned[col].quantile([.25, .75])
        low, high = q1 - 1.5*(q3-q1), q3 + 1.5*(q3-q1)
        cleaned = cleaned[cleaned[col].between(low, high)]
        steps.append({'feature': col, 'lower': float(low), 'upper': float(high),
                      'removed': before-len(cleaned), 'remaining': len(cleaned)})
    main = joblib.load(OUTPUT / 'model_clustering.h5')
    pca_model = joblib.load(OUTPUT / 'PCA_model_clustering.h5')
    pca = PCA(n_components=2)
    coordinates = pca.fit_transform(encoded.drop(columns='Target'))
    pca_frame = pd.DataFrame(coordinates, columns=['PCA1', 'PCA2'])
    data = pd.get_dummies(inverse, columns=inverse.select_dtypes('object').columns.tolist(), drop_first=True)
    X, y = data.drop(columns='Target'), data.Target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    classification = []
    for name, filename in [('Decision Tree', 'decision_tree_model.h5'),
                           ('Random Forest', 'explore_RandomForest_classification.h5'),
                           ('Random Forest tuned', 'tuning_classification.h5')]:
        model = joblib.load(OUTPUT / filename)
        prediction = model.predict(X_test)
        classification.append({'name': name, 'file': filename,
            'accuracy': accuracy_score(y_test, prediction),
            'precision_macro': precision_score(y_test, prediction, average='macro', zero_division=0),
            'recall_macro': recall_score(y_test, prediction, average='macro', zero_division=0),
            'f1_macro': f1_score(y_test, prediction, average='macro', zero_division=0)})
    tuned = joblib.load(OUTPUT / 'tuning_classification.h5')
    return {
        'environment': {'python': platform.python_version(), 'sklearn': sklearn.__version__,
                        'pandas': pd.__version__, 'numpy': np.__version__, 'joblib': joblib.__version__},
        'raw_rows': len(raw), 'raw_columns': len(raw.columns),
        'raw_missing_cells': int(raw.isna().sum().sum()), 'raw_duplicates': int(raw.duplicated().sum()),
        'numerical_columns': numeric,
        'dropped_columns': [c for c in raw.columns if any(t in c.lower() for t in ['id', 'ip', 'date'])],
        'preprocessing': {'after_dropna': after_dropna, 'after_duplicates': after_duplicates,
                          'outlier_steps': steps, 'final_rows': len(cleaned)},
        'age_bins_original_scale': pd.qcut(cleaned.CustomerAge, 3, retbins=True)[1].tolist(),
        'clustering': {'clusters': int(main.n_clusters),
                       'silhouette': silhouette_score(encoded.drop(columns='Target'), encoded.Target),
                       'location_variance_share': float(encoded.Location.var(ddof=0) /
                                                       encoded.drop(columns='Target').var(ddof=0).sum()),
                       'counts': {str(k): int(v) for k,v in encoded.Target.value_counts().sort_index().items()}},
        'pca': {'silhouette': silhouette_score(pca_frame, pca_model.predict(pca_frame)),
                'explained_variance': float(pca.explained_variance_ratio_.sum())},
        'split': {'train': len(X_train), 'test': len(X_test), 'features': len(X.columns)},
        'classification': classification,
        'tuning': {'best_params': tuned.best_params_, 'best_cv_accuracy': float(tuned.best_score_),
                   'candidates': len(tuned.cv_results_['params'])},
    }


def extract_figures(kind, notebook):
    count = 0
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            for output in cell.outputs:
                png = output.get('data', {}).get('image/png')
                if png:
                    count += 1
                    (FIGURES / f'{kind}-{count:02d}.png').write_bytes(base64.b64decode(png))
    return count


def main():
    REPORTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    (ROOT / '.jupyter' / 'runtime').mkdir(parents=True, exist_ok=True)
    completed = {}
    for kind, name in NAMES.items():
        path = OUTPUT / name
        notebook = nbformat.read(path, as_version=4)
        # Preparation is deliberate: actual execution always starts from clean templates.
        def started(cell, cell_index, **kwargs):
            if cell.cell_type == 'code':
                print(f'{kind}: cell {cell_index}: {cell.source.splitlines()[0][:90]}', flush=True)
        client = NotebookClient(notebook, timeout=600, kernel_name='bmlp',
                                resources={'metadata': {'path': str(OUTPUT)}},
                                allow_errors=False, on_cell_start=started)
        try:
            client.execute()
        finally:
            nbformat.write(notebook, path)
        completed[kind] = notebook
        print(f'{kind}: completed', flush=True)
    report = derive_report()
    encoded = pd.read_csv(OUTPUT / 'data_clustering.csv')
    inverse = pd.read_csv(OUTPUT / 'data_clustering_inverse.csv')
    annotate_cluster(completed['clustering'], encoded, inverse, report)
    annotate_classification(completed['classification'], report)
    report['figures'] = {}
    for kind, notebook in completed.items():
        report['figures'][kind] = extract_figures(kind, notebook)
        notebook.metadata.kernelspec = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
        nbformat.write(notebook, OUTPUT / NAMES[kind])
    (REPORTS / 'metrics.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    with zipfile.ZipFile(dist / 'BMLP_Arief_Maulana.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(OUTPUT.iterdir()):
            if path.is_file():
                archive.write(path, arcname=path.name)
    manifest = {'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(OUTPUT.iterdir()) if p.is_file()},
                'source_sha256': {name: hashlib.sha256((ROOT / 'sources' / name).read_bytes()).hexdigest()
                                  for name in ['clustering.ipynb', 'classification.ipynb',
                                               'bank_transactions_data_edited.csv']}}
    (REPORTS / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
