"""Integration checks for submission contracts; run after executing both notebooks."""

from pathlib import Path
import json
import zipfile

import joblib
import nbformat
import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / 'submission' / 'BMLP_Arief_Maulana'
NAMES = {
    'clustering': '[Clustering]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
    'classification': '[Klasifikasi]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
}
MODELS = ['model_clustering.h5', 'PCA_model_clustering.h5',
          'decision_tree_model.h5', 'explore_RandomForest_classification.h5',
          'tuning_classification.h5']


@pytest.mark.parametrize('kind', NAMES)
def test_notebooks_preserve_template_and_run_all(kind):
    source = nbformat.read(ROOT / 'sources' / f'{kind}.ipynb', as_version=4)
    result = nbformat.read(SUBMISSION / NAMES[kind], as_version=4)
    nbformat.validate(result)
    source_code = [c for c in source.cells if c.cell_type == 'code']
    result_code = [c for c in result.cells if c.cell_type == 'code']
    assert len(source_code) == len(result_code), 'No extra code cells allowed'
    assert source_code[0].source == result_code[0].source, 'Preserve imports exactly'
    expected_count = 1
    for cell in result_code:
        assert '________' not in cell.source and '<NAMA ALGORITMA-MU>' not in cell.source
        assert cell.execution_count == expected_count
        expected_count += 1
        assert not any(o.output_type == 'error' for o in cell.outputs)
        assert not any('Warning' in o.get('text', '') for o in cell.outputs)
        assert not any(line.startswith(('import ', 'from ', 'def '))
                       for line in cell.source.splitlines()) or cell is result_code[0]
    # Imports, assignments, and CSV writes naturally have no notebook display value.
    for cell in result_code:
        if any(token in cell.source for token in ['.head()', '.info()', '.describe()',
                                                  'classification_report(', 'silhouette_score(']):
            assert cell.outputs, 'Required evidence cells must retain their outputs'
    original_markdown = [c.source for i, c in enumerate(source.cells)
                         if c.cell_type == 'markdown' and
                         not (kind == 'clustering' and i in [71, 79])]
    actual_markdown = [c.source for c in result.cells if c.cell_type == 'markdown']
    pos = 0
    for text in original_markdown:
        pos = actual_markdown.index(text, pos) + 1
    assert any('Penilaian (Opsional)' in m for m in actual_markdown)


def test_preprocessing_inverse_and_labels_round_trip():
    encoded = pd.read_csv(SUBMISSION / 'data_clustering.csv')
    inverse = pd.read_csv(SUBMISSION / 'data_clustering_inverse.csv')
    raw = pd.read_csv(SUBMISSION / 'bank_transactions_data_edited.csv')
    assert raw.shape == (2537, 16), 'Use the supplied modified dataset'
    assert encoded.shape == inverse.shape
    assert encoded.columns.tolist() == inverse.columns.tolist()
    assert encoded['Target'].equals(inverse['Target'])
    assert encoded['Target'].nunique() >= 2
    assert not encoded.isna().any().any() and not inverse.isna().any().any()
    assert not any('unnamed' in c.lower() for c in encoded.columns)
    assert not any(token in c.lower() for c in encoded.columns
                   for token in ['id', 'ip', 'date'])
    cluster_model = joblib.load(SUBMISSION / 'model_clustering.h5')
    assert np.array_equal(cluster_model.predict(encoded.drop(columns='Target')), encoded.Target)
    numerical_cols = raw.select_dtypes('number').columns.tolist()
    cleaned = raw.dropna().drop_duplicates()
    for col in numerical_cols:
        q1, q3 = cleaned[col].quantile([.25, .75])
        cleaned = cleaned[cleaned[col].between(q1 - 1.5*(q3-q1), q3 + 1.5*(q3-q1))]
    assert len(inverse) == len(cleaned)
    np.testing.assert_allclose(inverse[numerical_cols], cleaned[numerical_cols], atol=1e-9)
    for col in ['TransactionType', 'Location', 'Channel', 'CustomerOccupation']:
        assert inverse[col].tolist() == cleaned[col].tolist()
    assert inverse.CustomerAgeGroup.nunique() == 3
    assert 'Target' not in cluster_model.feature_names_in_


def test_models_and_evaluation_on_same_holdout():
    data = pd.read_csv(SUBMISSION / 'data_clustering_inverse.csv')
    categorical = data.select_dtypes('object').columns.tolist()
    encoded = pd.get_dummies(data, columns=categorical, drop_first=True)
    X, y = encoded.drop(columns='Target'), encoded.Target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.2, random_state=42, stratify=y)
    tuning = joblib.load(SUBMISSION / 'tuning_classification.h5')
    assert tuning.cv == 5 and tuning.scoring == 'accuracy'
    assert tuning.refit and tuning.best_estimator_ is not None
    assert 'Target' not in tuning.feature_names_in_
    best_idx = np.argmax(tuning.cv_results_['mean_test_score'])
    assert tuning.best_index_ == best_idx
    for name in ['decision_tree_model.h5', 'explore_RandomForest_classification.h5',
                 'tuning_classification.h5']:
        model = joblib.load(SUBMISSION / name)
        assert model.feature_names_in_.tolist() == X.columns.tolist()
        assert 'Target' not in model.feature_names_in_
        predictions = model.predict(X_test)
        assert set(predictions).issubset(set(y.unique()))
        assert 0 <= accuracy_score(y_test, predictions) <= 1
        assert 0 <= f1_score(y_test, predictions, average='macro') <= 1
    assert len(X_train) + len(X_test) == len(data)
    assert set(X_train.index).isdisjoint(X_test.index)
    assert joblib.load(SUBMISSION / 'PCA_model_clustering.h5').n_features_in_ == 2


def test_zip_contains_final_artifacts_with_matching_bytes():
    path = ROOT / 'dist' / 'BMLP_Arief_Maulana.zip'
    required = list(NAMES.values()) + MODELS + ['data_clustering.csv',
                'data_clustering_inverse.csv', 'bank_transactions_data_edited.csv']
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(required)
        for name in required:
            assert archive.read(name) == (SUBMISSION / name).read_bytes()


def test_metrics_report_matches_saved_models():
    report = json.loads((ROOT / 'reports' / 'metrics.json').read_text(encoding='utf-8'))
    data = pd.read_csv(SUBMISSION / 'data_clustering_inverse.csv')
    X = pd.get_dummies(data.drop(columns='Target'), drop_first=True)
    _, X_test, _, y_test = train_test_split(
        X, data.Target, test_size=.2, random_state=42, stratify=data.Target)
    for record in report['classification']:
        model = joblib.load(SUBMISSION / record['file'])
        prediction = model.predict(X_test)
        assert record['accuracy'] == pytest.approx(accuracy_score(y_test, prediction))
        assert record['f1_macro'] == pytest.approx(f1_score(y_test, prediction, average='macro'))
