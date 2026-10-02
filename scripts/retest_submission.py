"""Replay only notebook code and raw CSV from the actual ZIP in a fresh folder."""

from pathlib import Path
import hashlib
import json
import time
import uuid
import zipfile

# Reuse the same workspace-local kernel and cache environment as the production executor.
import execute_submission
import nbformat
import pandas as pd
from nbclient import NotebookClient
from manual_check import ROOT, NOTEBOOKS, REQUIRED, check_folder


def main():
    started = time.monotonic()
    archive_path = ROOT/'dist'/'BMLP_Arief_Maulana.zip'
    zip_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    folder = ROOT/'.cache'/'retests'/uuid.uuid4().hex[:12]
    folder.mkdir(parents=True)
    seeds = list(NOTEBOOKS.values()) + ['bank_transactions_data_edited.csv']
    with zipfile.ZipFile(archive_path) as archive:
        assert set(archive.namelist()) == set(REQUIRED), 'ZIP manifest differs'
        assert archive.testzip() is None, 'ZIP CRC failed'
        for name in seeds:
            (folder/name).write_bytes(archive.read(name))
    assert sorted(p.name for p in folder.iterdir()) == sorted(seeds)
    for kind, name in NOTEBOOKS.items():
        path = folder/name
        notebook = nbformat.read(path, as_version=4)
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        def cell_started(cell, cell_index, **kwargs):
            if cell.cell_type == 'code':
                print(f'{kind}: {cell.source.splitlines()[0][:90]}', flush=True)
        client = NotebookClient(notebook, timeout=600, kernel_name='bmlp', allow_errors=False,
                                resources={'metadata': {'path': str(folder)}}, on_cell_start=cell_started)
        try:
            client.execute()
        finally:
            nbformat.write(notebook, path)
    result = check_folder(folder)
    assert result['passed'], result
    for name in ['data_clustering.csv', 'data_clustering_inverse.csv']:
        pd.testing.assert_frame_equal(pd.read_csv(folder/name),
            pd.read_csv(ROOT/'submission'/'BMLP_Arief_Maulana'/name), rtol=1e-12, atol=1e-12)
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == zip_hash, 'Original ZIP changed'
    result.update({'source': 'actual submission ZIP', 'zip_sha256': zip_hash,
                   'old_models_or_processed_csv_seeded': False, 'cleared_outputs_before_execution': True,
                   'fresh_kernel_per_notebook': True, 'csvs_match_baseline': True,
                   'original_zip_unchanged': True, 'duration_seconds': round(time.monotonic()-started, 2)})
    path = ROOT/'reports'/'retest-results.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
