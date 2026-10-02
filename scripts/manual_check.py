"""Check saved results after a manual notebook run without modifying the submission."""

from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import uuid
import zipfile

import joblib
import nbformat
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, silhouette_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = {
    'clustering': '[Clustering]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
    'classification': '[Klasifikasi]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
}
MODELS = ['model_clustering.h5', 'PCA_model_clustering.h5',
          'decision_tree_model.h5', 'explore_RandomForest_classification.h5',
          'tuning_classification.h5']
REQUIRED = list(NOTEBOOKS.values()) + MODELS + ['bank_transactions_data_edited.csv',
                                              'data_clustering.csv', 'data_clustering_inverse.csv']


def prepare_folder(folder):
    """Extract input-only copies from ZIP and clear old outputs in those copies."""
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(ROOT/'dist'/'BMLP_Arief_Maulana.zip') as archive:
        assert set(archive.namelist()) == set(REQUIRED), 'Unexpected ZIP manifest'
        assert archive.testzip() is None, 'ZIP CRC failed'
        for name in list(NOTEBOOKS.values()) + ['bank_transactions_data_edited.csv']:
            (folder/name).write_bytes(archive.read(name))
    for name in NOTEBOOKS.values():
        path = folder/name
        notebook = nbformat.read(path, as_version=4)
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        nbformat.write(notebook, path)
    return folder


def check_folder(folder):
    folder = Path(folder).resolve()
    checks = []

    def check(name, action):
        try:
            details = action()
            checks.append({'name': name, 'passed': True, 'details': details})
        except Exception as exc:
            checks.append({'name': name, 'passed': False,
                           'error': f'{type(exc).__name__}: {exc}'})

    def files():
        missing = [name for name in REQUIRED if not (folder/name).is_file()]
        assert not missing, f'Missing: {missing}'
        assert all((folder/name).stat().st_size > 0 for name in REQUIRED), 'Empty file'
        return {'files': len(REQUIRED)}
    check('required_files', files)

    def notebook(kind):
        source = nbformat.read(ROOT/'sources'/f'{kind}.ipynb', as_version=4)
        result = nbformat.read(folder/NOTEBOOKS[kind], as_version=4)
        nbformat.validate(result)
        original = [c for c in source.cells if c.cell_type == 'code']
        actual = [c for c in result.cells if c.cell_type == 'code']
        assert len(actual) == len(original), 'Code cell count differs from official template'
        assert actual[0].source == original[0].source, 'Original imports changed'
        plots = 0
        for index, cell in enumerate(actual, start=1):
            assert cell.execution_count == index, 'Restart kernel then Run All; save afterward'
            assert '________' not in cell.source, 'Unfilled code placeholder'
            compile(cell.source, f'{kind}-cell-{index}', 'exec')
            for output in cell.outputs:
                assert output.output_type != 'error', f'Saved error: {output.get("ename", "")}'
                assert 'Warning' not in output.get('text', ''), 'Saved runtime warning'
                plots += int('image/png' in output.get('data', {}))
            if any(t in cell.source for t in ['.head()', '.info()', '.describe()',
                                              'classification_report(', 'silhouette_score(']):
                assert cell.outputs, 'Required output missing'
        if kind == 'clustering':
            assert plots == 17, f'Expected 17 plots, got {plots}'
        return {'code_cells': len(actual), 'plots': plots, 'saved_errors': 0}
    for kind in NOTEBOOKS:
        check('notebook_'+kind, lambda kind=kind: notebook(kind))

    def raw_source():
        expected = (ROOT/'sources'/'bank_transactions_data_edited.csv').read_bytes()
        actual = (folder/'bank_transactions_data_edited.csv').read_bytes()
        assert hashlib.sha256(actual).digest() == hashlib.sha256(expected).digest(), 'Raw dataset differs'
        raw = pd.read_csv(folder/'bank_transactions_data_edited.csv')
        assert raw.shape == (2537, 16)
        return {'rows': len(raw), 'columns': len(raw.columns),
                'missing_cells': int(raw.isna().sum().sum()),
                'duplicates': int(raw.duplicated().sum())}
    check('raw_dataset', raw_source)

    def csv_alignment():
        encoded = pd.read_csv(folder/'data_clustering.csv')
        inverse = pd.read_csv(folder/'data_clustering_inverse.csv')
        assert encoded.shape == inverse.shape == (1945, 11), 'Expected 1945 rows and 11 columns'
        assert encoded.columns.tolist() == inverse.columns.tolist(), 'Column order differs'
        assert encoded.Target.equals(inverse.Target), 'Target differs between CSVs'
        assert not encoded.isna().any().any() and not inverse.isna().any().any(), 'Missing values remain'
        assert not any(c.lower().startswith('unnamed') for c in encoded.columns), 'CSV index leaked'
        assert not any(t in c.lower() for c in encoded.columns for t in ['id', 'ip', 'date'])
        assert encoded.Target.value_counts().sort_index().to_dict() == {0: 980, 1: 965}
        return {'rows': len(encoded), 'columns': len(encoded.columns), 'target_counts': {0: 980, 1: 965}}
    check('csv_alignment', csv_alignment)

    def inverse_roundtrip():
        raw = pd.read_csv(folder/'bank_transactions_data_edited.csv')
        numerical = raw.select_dtypes('number').columns.tolist()
        cleaned = raw.dropna().drop_duplicates()
        for col in numerical:
            q1, q3 = cleaned[col].quantile([.25, .75])
            cleaned = cleaned[cleaned[col].between(q1 - 1.5*(q3-q1), q3 + 1.5*(q3-q1))]
        inverse = pd.read_csv(folder/'data_clustering_inverse.csv')
        np.testing.assert_allclose(inverse[numerical], cleaned[numerical], rtol=0, atol=1e-9)
        for col in ['TransactionType', 'Location', 'Channel', 'CustomerOccupation']:
            assert inverse[col].tolist() == cleaned[col].tolist(), f'Inverse categories mismatch: {col}'
        bins = pd.qcut(cleaned.CustomerAge, q=3, labels=['1_Muda','2_Dewasa','3_Senior'])
        assert inverse.CustomerAgeGroup.tolist() == bins.astype(str).tolist(), 'Age bin mismatch'
        return {'numerical_max_tolerance': 1e-9, 'rows_verified': len(cleaned)}
    check('inverse_roundtrip', inverse_roundtrip)

    def clustering():
        data = pd.read_csv(folder/'data_clustering.csv')
        X = data.drop(columns='Target')
        model = joblib.load(folder/'model_clustering.h5')
        assert model.feature_names_in_.tolist() == X.columns.tolist()
        assert 'Target' not in model.feature_names_in_
        assert model.n_clusters == 2
        assert np.array_equal(model.predict(X), data.Target), 'Model predictions differ from Target'
        score = silhouette_score(X, data.Target)
        assert math.isclose(score, 0.572159925838334, abs_tol=1e-10)
        return {'clusters': model.n_clusters, 'silhouette': score, 'features': X.shape[1]}
    check('clustering_model', clustering)

    def pca_model():
        X = pd.read_csv(folder/'data_clustering.csv').drop(columns='Target')
        pca = PCA(n_components=2)
        transformed = pd.DataFrame(pca.fit_transform(X), columns=['PCA1','PCA2'])
        model = joblib.load(folder/'PCA_model_clustering.h5')
        assert model.n_features_in_ == 2 and model.n_clusters == 2
        score = silhouette_score(transformed, model.predict(transformed))
        assert math.isclose(score, 0.6017426992642231, abs_tol=1e-10)
        return {'silhouette': score, 'explained_variance': float(pca.explained_variance_ratio_.sum())}
    check('pca_model', pca_model)

    def split_data():
        data = pd.read_csv(folder/'data_clustering_inverse.csv')
        encoded = pd.get_dummies(data, columns=data.select_dtypes('object').columns.tolist(), drop_first=True)
        X, y = encoded.drop(columns='Target'), encoded.Target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
        assert X.shape == (1945, 55)
        assert len(X_train) == 1556 and len(X_test) == 389
        assert set(X_train.index).isdisjoint(X_test.index)
        return X_train, X_test, y_train, y_test

    def split_check():
        train, test, _, _ = split_data()
        return {'train': len(train), 'test': len(test), 'features': len(train.columns)}
    check('classification_split', split_check)

    def classifier(filename):
        _, X_test, _, y_test = split_data()
        model = joblib.load(folder/filename)
        assert model.feature_names_in_.tolist() == X_test.columns.tolist()
        assert 'Target' not in model.feature_names_in_
        prediction = model.predict(X_test)
        scores = {'accuracy': accuracy_score(y_test, prediction),
                  'precision_macro': precision_score(y_test, prediction, average='macro', zero_division=0),
                  'recall_macro': recall_score(y_test, prediction, average='macro', zero_division=0),
                  'f1_macro': f1_score(y_test, prediction, average='macro', zero_division=0)}
        assert all(math.isclose(value, 1, abs_tol=1e-12) for value in scores.values()), 'Metrics changed'
        return scores
    for name, filename in [('decision_tree', 'decision_tree_model.h5'),
                           ('random_forest', 'explore_RandomForest_classification.h5'),
                           ('tuned_random_forest', 'tuning_classification.h5')]:
        check(name, lambda filename=filename: classifier(filename))

    def tuning():
        model = joblib.load(folder/'tuning_classification.h5')
        assert model.cv == 5 and model.scoring == 'accuracy' and model.n_splits_ == 5
        assert len(model.cv_results_['params']) == 18
        assert model.best_params_ == {'max_depth': None, 'min_samples_leaf': 1, 'n_estimators': 200}
        assert model.best_index_ == int(np.argmax(model.cv_results_['mean_test_score']))
        return {'best_params': model.best_params_, 'best_cv_accuracy': float(model.best_score_), 'candidates': 18}
    check('tuning_cv', tuning)
    return {'folder': str(folder), 'passed': all(c['passed'] for c in checks),
            'passed_checks': sum(c['passed'] for c in checks),
            'total_checks': len(checks), 'checks': checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path)
    parser.add_argument('--prepare', action='store_true', help='Create a fresh input-only manual test folder')
    parser.add_argument('--report', type=Path, default=ROOT/'reports'/'manual-check-latest.json')
    args = parser.parse_args()
    if args.prepare:
        folder = prepare_folder(args.folder or ROOT/'.cache'/'manual-tests'/uuid.uuid4().hex[:12])
        session = {'folder': str(folder), 'python': str(ROOT/'.venv'/'Scripts'/'python.exe')}
        (ROOT/'.cache').mkdir(exist_ok=True)
        (ROOT/'.cache'/'manual-session.json').write_text(json.dumps(session, indent=2), encoding='utf-8')
        print(json.dumps(session, ensure_ascii=False))
        return 0
    result = check_folder(args.folder or ROOT/'submission'/'BMLP_Arief_Maulana')
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    for item in result['checks']:
        print(('PASS' if item['passed'] else 'FAIL') + ' ' + item['name'])
        if not item['passed']:
            print('  ' + item['error'])
    print(f"{result['passed_checks']}/{result['total_checks']} checks passed. Report: {args.report}")
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
