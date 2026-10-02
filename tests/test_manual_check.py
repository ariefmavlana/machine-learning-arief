"""Regression coverage for the checker used after the user's manual Run All."""

from pathlib import Path
import shutil

import nbformat
import pandas as pd

from scripts.manual_check import check_folder

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / 'submission' / 'BMLP_Arief_Maulana'


def test_current_submission_passes_manual_checker():
    result = check_folder(ORIGINAL)
    assert result['passed'], result


def test_checker_detects_target_changed_in_only_one_csv(tmp_path):
    folder = tmp_path / 'changed_target'
    shutil.copytree(ORIGINAL, folder)
    data = pd.read_csv(folder / 'data_clustering_inverse.csv')
    data.loc[0, 'Target'] = 1 - data.loc[0, 'Target']
    data.to_csv(folder / 'data_clustering_inverse.csv', index=False)
    result = check_folder(folder)
    assert not result['passed']
    assert any(c['name'] == 'csv_alignment' and not c['passed'] for c in result['checks'])


def test_checker_detects_notebook_with_saved_error(tmp_path):
    folder = tmp_path / 'saved_error'
    shutil.copytree(ORIGINAL, folder)
    path = next(folder.glob('[[]Klasifikasi[]]*.ipynb'))
    notebook = nbformat.read(path, as_version=4)
    code = next(c for c in notebook.cells if c.cell_type == 'code')
    code.outputs = [nbformat.v4.new_output('error', ename='NameError',
                                         evalue='X_train is not defined', traceback=[])]
    nbformat.write(notebook, path)
    result = check_folder(folder)
    assert not result['passed']
    assert any(c['name'] == 'notebook_classification' and not c['passed'] for c in result['checks'])


def test_checker_reports_missing_model_as_failed_check(tmp_path):
    folder = tmp_path / 'missing_model'
    shutil.copytree(ORIGINAL, folder,
                    ignore=shutil.ignore_patterns('decision_tree_model.h5'))
    result = check_folder(folder)
    assert not result['passed']
    assert any(c['name'] == 'required_files' and not c['passed'] for c in result['checks'])


def test_prepare_folder_starts_without_cached_results(tmp_path):
    from scripts.manual_check import prepare_folder
    folder = tmp_path / 'fresh_manual_session'
    prepare_folder(folder)
    assert sorted(p.name for p in folder.iterdir()) == sorted([
        '[Clustering]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
        '[Klasifikasi]_Submission_Akhir_BMLP_Arief_Maulana.ipynb',
        'bank_transactions_data_edited.csv'])
    for path in folder.glob('*.ipynb'):
        notebook = nbformat.read(path, as_version=4)
        assert all(not c.outputs and c.execution_count is None
                   for c in notebook.cells if c.cell_type == 'code')
