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
        age_context = 'lebih tinggi' if mean_age > inverse.CustomerAge.mean() else 'lebih rendah atau sama'
        age_mean = f'{mean_age:.2f}'
        amount_mean = f'{group.TransactionAmount.mean():.2f}'
        balance_mean = f'{group.AccountBalance.mean():.2f}'
        section = f'### Cluster {int(target)}\n\n**Jumlah anggota:** {count} ({count/len(inverse):.2%}).\n\n'
        scaled_sections.append(section + markdown_table(scaled_stats) +
            '\n\n**Analisis:** mean menunjukkan posisi relatif dalam fitur numerik yang distandardisasi; '
            'min–max memperlihatkan rentang anggota yang masih dipertahankan. Nilai negatif bukan transaksi '
            'negatif, melainkan posisi di bawah mean data bersih. LoginAttempts menjadi konstan setelah '
            'filter IQR sehingga seluruh nilai scaled-nya nol. Makna karakteristik kategori dilengkapi '
            'pada analisis inverse; label cluster bukan urutan tingkat risiko.')
        inverse_sections.append(section + markdown_table(native_stats) + '\n\n' + '\n'.join(category_modes) +
            f'\n\n**Analisis:** mean usia {age_mean} tahun, {age_context} dibanding mean seluruh data bersih '
            f'({inverse.CustomerAge.mean():.2f} tahun). Mean nilai transaksi {amount_mean} dan mean saldo '
            f'{balance_mean} menggunakan satuan moneter dataset. Rentang min–max pada tabel menunjukkan '
            'variasi dalam kelompok, sehingga mean tidak menggambarkan semua anggota. '
            'Mode adalah kategori paling sering, bukan identitas setiap anggota. Perbedaan kelompok '
            'terutama harus dibaca bersama pengaruh kode Location pada jarak K-Means; '
            'tidak tersedia ground truth fraud untuk memberi persona aman atau fraud.')
    notebook.cells[71].source = '\n'.join(notebook.cells[71].source.splitlines()[:2]) + '\n\n' + '\n\n'.join(scaled_sections)
    notebook.cells[79].source = '\n'.join(notebook.cells[79].source.splitlines()[:2]) + '\n\n' + '\n\n'.join(inverse_sections)
    prep = report['preprocessing']
    boundaries = report['age_bins_original_scale']
    additions = [
        (22, optional('Metode, alasan, dan hasil EDA',
            '**Metode:** head, info, describe, korelasi Pearson untuk numerik, histogram numerik, '
            'distribusi frekuensi seluruh kategori, boxplot, dan violinplot.\n\n'
            '**Alasan:** memeriksa struktur, kualitas data, dan distribusi sebelum menentukan preprocessing. '
            'Kolom berkardinalitas tinggi tetap menampilkan seluruh kategori; hanya label tick yang '
            'dijarangkan agar tidak bertumpuk. Tidak digunakan pemotongan top-N.\n\n'
            f'**Hasil:** snapshot resmi berisi {report["raw_rows"]} baris dan {report["raw_columns"]} kolom, '
            f'{report["raw_missing_cells"]} sel kosong, dan {report["raw_duplicates"]} duplikat. '
            'Keterangan 2.512 sampel dan gambar expected output pada markdown bawaan adalah referensi '
            'template; output cell pada notebook ini menunjukkan snapshot yang benar-benar dianalisis. '
            'Fitur ID dan tanggal hanya divisualisasikan pada EDA, kemudian dihapus sebelum model. '
            'Distribusi nominal disajikan sebagai frekuensi kategori, karena histogram interval numerik '
            'tidak bermakna untuk nama kategori.')),
        (51, optional('Metode, alasan, dan hasil preprocessing',
            '**Metode:** dropna, drop_duplicates, drop kolom ID/IP/date, LabelEncoder per kategori, '
            'filter IQR berurutan dengan batas 1,5 IQR, StandardScaler untuk numerik asli, '
            'dan qcut tiga kelompok pada CustomerAge.\n\n'
            '**Alasan:** memenuhi tahapan template, mempertahankan encoder/scaler untuk inverse, '
            'serta menambahkan kelompok umur tanpa mengganti CustomerAge asli. '
            'qcut mengikuti cell template dan menentukan interval dari kuantil data bersih.\n\n'
            f'**Hasil:** {report["raw_rows"]} → {prep["after_dropna"]} sesudah dropna → '
            f'{prep["after_duplicates"]} sesudah duplikat → {prep["final_rows"]} sesudah outlier. '
            f'Kolom yang dibuang: {", ".join(report["dropped_columns"])}. '
            f'Batas kelompok usia pada skala asli: {", ".join(f"{v:.2f}" for v in boundaries)} tahun. '
            'Binning dilakukan pada nilai scaled sesuai urutan template; transformasi linear scaler '
            'mempertahankan urutan umur sehingga kelompok kuantil ekuivalen dengan skala asli. '
            'Label 1_Muda, 2_Dewasa, 3_Senior adalah nama relatif terhadap distribusi ini, bukan '
            'batas demografi resmi. Fitur asli tetap ada sehingga inverse numerik tidak bergantung '
            'pada rekonstruksi kategori bin.\n\n'
            '**Batas metode:** LoginAttempts memiliki IQR nol pada tahap filternya; semua nilai di atas '
            '1 terhapus. Hal ini sesuai filter pada template, tetapi dapat membuang sinyal anomali. '
            'Proyek ini tidak mengklaim kemampuan fraud detection.')),
        (67, optional('Metode, alasan, dan hasil clustering serta PCA',
            '**Metode:** KElbowVisualizer dengan metric silhouette pada k=2–9 sebagaimana rentang '
            '(2,10) pada template, K-Means utama, silhouette, dan K-Means pembanding pada dua komponen PCA. '
            'random_state=42 dan n_init=10 menjaga pengulangan eksperimen.\n\n'
            '**Alasan:** memilih k dari keluaran visualizer tanpa mengambil keputusan dari classifier '
            'testing set; PCA memberi representasi dua dimensi untuk visualisasi dan pembanding.\n\n'
            f'**Hasil:** k={report["clustering"]["clusters"]}; silhouette utama '
            f'{report["clustering"]["silhouette"]:.6f}; silhouette ruang PCA '
            f'{report["pca"]["silhouette"]:.6f}; dua komponen menjelaskan '
            f'{report["pca"]["explained_variance"]:.2%} varians. '
            'Skor dihitung pada ruang fitur berbeda sehingga tidak membuktikan PCA lebih baik '
            'untuk semua tujuan. Label Target berasal dari model utama, bukan model PCA.\n\n'
            '**Batas interpretasi:** Location di-LabelEncode menjadi kode nominal tanpa scaling karena '
            'template hanya menskalakan fitur numerik asli. Rentang kode Location dapat mendominasi '
            f'jarak dan PCA: Location menyumbang {report["clustering"]["location_variance_share"]:.2%} '
            'dari jumlah varians fitur yang masuk model. Kedekatan kode bukan bukti kedekatan geografis. Binning umur juga memberi '
            'representasi tambahan umur dalam jarak. Silhouette tinggi perlu dibaca bersama batas '
            'representasi ini, bukan dianggap validasi fraud.')),
        (82, optional('Metode, alasan, dan hasil ekspor serta inverse',
            '**Metode:** ekspor data preprocessing dengan Target; inverse_transform dengan scaler dan '
            'encoder fitted yang sama; agregasi mean/min/max dan mode; ekspor CSV inverse.\n\n'
            '**Alasan:** mempertahankan label per baris sekaligus mengembalikan satuan yang dapat '
            'diinterpretasikan untuk analisis dan notebook klasifikasi.\n\n'
            f'**Hasil:** kedua CSV berisi {len(encoded)} baris dengan Target yang identik. '
            'CSV tidak memuat indeks tambahan. CustomerAgeGroup kembali ke kategori bin, sedangkan '
            'CustomerAge asli kembali ke nilai tahun. Notebook klasifikasi memakai '
            'data_clustering_inverse.csv dan cell One Hot Encoding bawaan. '
            'CSV mentah disertakan untuk eksekusi ulang offline; sumber URL tetap dicantumkan pada cell load.')),
    ]
    for index, cell in sorted(additions, key=lambda x: x[0], reverse=True):
        notebook.cells.insert(index+1, cell)


def annotate_classification(notebook, report):
    records = report['classification']
    table = pd.DataFrame(records).set_index('name')[['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']]
    tuning = report['tuning']
    additions = [
        (9, optional('Metode, alasan, dan hasil pembagian data',
            '**Metode:** muat CSV inverse, pd.get_dummies pada kolom string dengan drop_first=True, '
            'kemudian train_test_split dengan test_size=0.2, random_state=42, dan stratify=y.\n\n'
            '**Alasan:** mengikuti cell One Hot Encoding yang tersedia serta menjaga perbandingan '
            'model pada holdout yang identik. Target dikeluarkan dari fitur X.\n\n'
            f'**Hasil:** {report["split"]["train"]} training dan {report["split"]["test"]} testing; '
            f'{report["split"]["features"]} fitur masukan sesudah encoding. '
            'One Hot Encoding hanya membentuk indikator kategori dan tidak mempelajari statistik '
            'numerik. Kosakata kategori mengikuti dataset penuh sesuai urutan template. '
            'Untuk evaluasi produksi yang benar-benar terpisah, kosakata dan seluruh transformasi '
            'perlu dipelajari pada training saja.')),
        (16, optional('Metode, alasan, dan hasil evaluasi seluruh model',
            '**Metode:** Decision Tree baseline dan Random Forest 200 pohon; classification_report '
            'serta tabel accuracy, precision macro, recall macro, F1 macro pada testing set.\n\n'
            '**Alasan:** Decision Tree memenuhi model wajib; Random Forest memberi pembanding ensemble. '
            'Macro averaging memberi bobot yang sama untuk setiap kelas.\n\n'
            '**Hasil:**\n\n' + markdown_table(table.iloc[:2]) + '\n\n'
            'Seluruh hasil mengukur prediksi label K-Means. Data clustering telah diproses dan '
            'dilabeli sebelum split klasifikasi sesuai tugas, sehingga evaluasi bersifat meniru '
            'label pada dataset ini; bukan pengukuran generalisasi seluruh pipeline ke transaksi '
            'baru maupun deteksi fraud berlabel nyata.')),
        (20, optional('Metode, alasan, dan hasil tuning',
            '**Metode:** GridSearchCV pada Random Forest, 18 kombinasi, 5-fold CV pada training, '
            'scoring accuracy sesuai template, dan refit estimator terbaik pada seluruh training.\n\n'
            '**Alasan:** keputusan hyperparameter memakai CV training; testing set hanya untuk '
            'pelaporan setelah pemilihan.\n\n'
            f'**Hasil:** best_params={tuning["best_params"]}; accuracy CV terbaik '
            f'{tuning["best_cv_accuracy"]:.6f}.\n\n' + markdown_table(table.iloc[2:]) + '\n\n'
            'Tuning tidak diwajibkan mengalahkan baseline dan hasil tidak dipilih ulang berdasarkan '
            'testing set. Artefak tuning_classification.h5 menyimpan objek GridSearchCV fitted '
            'sesuai cell template, termasuk best_estimator_ dan cv_results_.')),
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
