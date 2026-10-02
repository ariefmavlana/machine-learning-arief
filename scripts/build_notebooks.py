"""Fill the official templates without adding code cells or modifying imports."""

from pathlib import Path
import re
import shutil
import nbformat

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'submission' / 'BMLP_Arief_Maulana'
NAMES = {
    'clustering': '[Clustering]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
    'classification': '[Klasifikasi]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
}


def fill(notebook, index, values):
    cell = notebook.cells[index]
    source = cell.source
    blanks = re.compile(r'_{4,}')
    if len(blanks.findall(source)) != len(values):
        raise ValueError(f'Cell {index}: expected {len(blanks.findall(source))} replacements, got {len(values)}')
    for value in values:
        source = blanks.sub(lambda match: value, source, count=1)
    cell.source = source


def build():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / 'sources' / 'bank_transactions_data_edited.csv',
                    OUTPUT / 'bank_transactions_data_edited.csv')
    cluster = nbformat.read(ROOT / 'sources' / 'clustering.ipynb', as_version=4)
    classification = nbformat.read(ROOT / 'sources' / 'classification.ipynb', as_version=4)

    values = {
        7: ['pd.read_csv("bank_transactions_data_edited.csv")'],
        8: ['head'], 10: ['df'], 12: ['df'],
        15: ['corr', 'heatmap'], 18: ['histplot', 'ax=axes[i]'],
        22: ['boxplot', '"CustomerOccupation"', '"TransactionAmount"', 'xticks'],
        24: ['isnull()'], 27: ['duplicated()'], 29: ['dropna', 'inplace', 'isnull()'],
        32: ['drop_duplicates', 'inplace', 'duplicated()'],
        34: ['df.columns', "'id'", 'lower', 'lower', 'drop', 'head'],
        37: ['select_dtypes', 'columns', 'LabelEncoder', 'fit_transform', 'head'],
        40: ['df'],
        44: ['quantile', 'quantile', 'Q3', 'Q1', 'lower_bound', 'upper_bound'],
        47: ['StandardScaler', 'fit_transform', 'head'],
        51: ['CustomerAge', 'CustomerAgeGroup', '1_Muda', '2_Dewasa', '3_Senior',
             'qcut', 'LabelEncoder', 'fit_transform', 'head'],
        53: ['copy', 'describe'],
        54: ['KElbowVisualizer', 'model', 'k', 'metric', 'fit', 'show'],
        57: ['KMeans', 'int(visualizer.elbow_value_)', 'fit'],
        59: ['joblib', 'model'],
        61: ['labels_', 'silhouette_score', 'labels'],
        62: ['PCA', '2', 'fit_transform', 'labels', 'scatterplot', 'hue'],
        66: ['PCA', '2', 'fit_transform', 'df_pca_array', 'KMeans',
             'model.n_clusters', 'fit', 'data_final'],
        67: ['joblib', 'kmeans_pca'],
        70: ['labels', 'groupby', "'Cluster'", 'agg', 'agg_summary'],
        73: ['rename', 'columns', 'inplace', 'head'], 74: ['df_used'],
        76: ['inverse_transform', 'head'],
        77: ['encoders', 'column', 'inverse_transform', 'head'],
        78: ['groupby', 'agg', 'groupby', 'agg'],
        81: ['df_inverse'], 82: ['df_inverse'],
    }
    for index, replacements in values.items():
        fill(cluster, index, replacements)

    # Supporting adjustments in existing visualization cells: reproducibility and readable labels.
    cluster.cells[15].source = cluster.cells[15].source.replace(
        "plt.figure(figsize=(10, 6))", "plt.figure(figsize=(10, 8))").replace(
        "plt.show()", "plt.xticks(rotation=30, ha='right')\nplt.yticks(rotation=0)\nplt.tight_layout()\nplt.show()")
    cluster.cells[18].source = cluster.cells[18].source.replace(
        'plt.tight_layout()',
        "for unused_axis in axes[len(numerical_cols):]:\n    unused_axis.set_visible(False)\nplt.tight_layout()")
    cluster.cells[22].source = cluster.cells[22].source.replace(
        'plt.show()', 'plt.tight_layout()\nplt.show()', 1)
    cluster.cells[22].source += '''

# Distribusi seluruh kolom kategorikal, termasuk ID dan tanggal sebelum drop.
# Semua kategori ditampilkan; hanya tick yang dijarangkan untuk kardinalitas tinggi.
eda_categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
for column in eda_categorical_cols:
    category_counts = df[column].fillna('(Missing)').value_counts()
    fig, axis = plt.subplots(figsize=(12, 4), layout='constrained')
    category_positions = np.arange(len(category_counts))
    axis.bar(category_positions, category_counts.values, color='steelblue', width=0.9)
    tick_positions = np.unique(np.linspace(0, len(category_counts) - 1,
                                          min(8, len(category_counts)), dtype=int))
    axis.set_xticks(tick_positions)
    axis.set_xticklabels([str(category_counts.index[pos]) for pos in tick_positions],
                        rotation=30, ha='right', fontsize=8)
    axis.set_title('Distribusi kategorikal: ' + column)
    axis.set_xlabel('Kategori diurutkan berdasarkan frekuensi; seluruh kategori tercakup')
    axis.set_ylabel('Jumlah observasi')
    plt.show()

# Tantangan visualisasi kepadatan distribusi yang disediakan template.
plt.figure(figsize=(12, 6))
sns.violinplot(x='CustomerOccupation', y='TransactionAmount', data=df,
               inner='quartile', cut=0)
plt.title('Distribusi nilai transaksi per pekerjaan nasabah')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()
'''
    cluster.cells[54].source = cluster.cells[54].source.replace(
        'model = KMeans()', 'model = KMeans(random_state=42, n_init=10)')
    cluster.cells[57].source = cluster.cells[57].source.replace(
        'random_state=42)', 'random_state=42, n_init=10)')
    cluster.cells[62].source = cluster.cells[62].source.replace(
        'n_colors=2', 'n_colors=model.n_clusters').replace(
        'pca.transform(model.cluster_centers_)',
        'pca.transform(pd.DataFrame(model.cluster_centers_, columns=df.columns))').replace(
        'plt.show()', 'plt.tight_layout()\nplt.show()')
    cluster.cells[66].source = cluster.cells[66].source.replace(
        'random_state=42)', 'random_state=42, n_init=10)')
    cluster.cells[66].source += '''

print('Jumlah komponen PCA:', pca.n_components_)
print('Proporsi varians dijelaskan:', pca.explained_variance_ratio_)
print('Total varians dijelaskan:', pca.explained_variance_ratio_.sum())
print('Silhouette pada ruang PCA:', silhouette_score(data_final, kmeans_pca.labels_))
print('Distribusi cluster utama:', pd.Series(labels).value_counts().sort_index().to_dict())
print('Distribusi cluster PCA:', pd.Series(kmeans_pca.labels_).value_counts().sort_index().to_dict())
'''

    for index in [74, 82]:
        name = 'data_clustering.csv' if index == 74 else 'data_clustering_inverse.csv'
        cluster.cells[index].source += f"\nprint('Data berhasil disimpan: {name}; jumlah baris:', len(df_used))\n"

    # Fill the original answer slots after actual execution in execute_submission.py.
    cluster.cells[71].source = '# **⚠️PERHATIAN: JAWAB DI BAWAH SINI**\n## Menjelaskan karakteristik tiap cluster berdasarkan rentangnya sebelum **Inverse** (masih dalam kondisi **Scaled**).\n\nAnalisis diisi berdasarkan hasil eksekusi.'
    cluster.cells[79].source = '# **⚠️PERHATIAN: JAWAB DI BAWAH SINI**\n## Menjelaskan karakteristik tiap cluster berdasarkan rentangnya setelah **Inverse**.\n\nAnalisis diisi berdasarkan hasil eksekusi.'
    cluster.cells[7].source += "\n# Snapshot CSV resmi disertakan agar Run All dapat dilakukan tanpa koneksi internet.\n"

    class_values = {
        4: ['df', 'data_clustering_inverse'], 5: ['df'],
        7: ['df', 'get_dummies', 'categorical_cols', 'head'],
        9: ['df_encoded', 'drop', '1', 'df_encoded', "'Target'", 'train_test_split', '0.2', 'y'],
        11: ['DecisionTreeClassifier', 'fit', 'X_train', 'y_train'],
        12: ['decision_tree_model'],
        15: ['RandomForestClassifier', 'n_estimators=200, random_state=42, n_jobs=1', 'fit', 'X_train', 'y_train'],
        16: ['predict', 'X_test', 'predict', 'X_test', 'y_test', 'y_pred_dt, digits=4, zero_division=0',
             'y_test', 'y_pred_new, digits=4, zero_division=0'],
        17: ['joblib'],
        19: ["'n_estimators': [100, 200]", "'max_depth': [None, 8, 16]", "'min_samples_leaf': [1, 2, 4]",
             'GridSearchCV', 'RandomForestClassifier', 'param_grid', 'fit', 'X_train', 'y_train'],
        20: ['predict', 'X_test', 'y_test', 'y_pred_tuning, digits=4, zero_division=0'],
        21: ['joblib'],
    }
    for index, replacements in class_values.items():
        fill(classification, index, replacements)
    classification.cells[17].source = classification.cells[17].source.replace(
        '<NAMA ALGORITMA-MU>', 'RandomForest')
    classification.cells[19].source += '''

print('Parameter terbaik berdasarkan CV training:', new_model_tuned.best_params_)
print('Rata-rata accuracy CV terbaik:', new_model_tuned.best_score_)
print('Jumlah kombinasi diuji:', len(new_model_tuned.cv_results_['params']))
'''
    classification.cells[16].source += '''

evaluation_rows = []
for model_name, predictions in [('Decision Tree', y_pred_dt), ('Random Forest', y_pred_new)]:
    evaluation_rows.append({
        'Model': model_name,
        'Accuracy': accuracy_score(y_test, predictions),
        'Precision macro': precision_score(y_test, predictions, average='macro', zero_division=0),
        'Recall macro': recall_score(y_test, predictions, average='macro', zero_division=0),
        'F1 macro': f1_score(y_test, predictions, average='macro', zero_division=0),
    })
pd.DataFrame(evaluation_rows).set_index('Model')
'''
    classification.cells[20].source += '''

pd.DataFrame([{
    'Model': 'Random Forest tuned',
    'Accuracy': accuracy_score(y_test, y_pred_tuning),
    'Precision macro': precision_score(y_test, y_pred_tuning, average='macro', zero_division=0),
    'Recall macro': recall_score(y_test, y_pred_tuning, average='macro', zero_division=0),
    'F1 macro': f1_score(y_test, y_pred_tuning, average='macro', zero_division=0),
}]).set_index('Model')
'''

    for kind, notebook in [('clustering', cluster), ('classification', classification)]:
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        notebook.metadata.kernelspec = {'display_name': 'Python 3 (BMLP)',
                                       'language': 'python', 'name': 'bmlp'}
        nbformat.write(notebook, OUTPUT / NAMES[kind])
        print('Prepared', NAMES[kind], flush=True)


if __name__ == '__main__':
    build()
