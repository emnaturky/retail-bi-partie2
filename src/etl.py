"""Lancer depuis le dossier retail-bi : uv run python src/etl.py.

Conserve l'organisation de la professeure : src/etl.py + retail_bi/.
"""
from pathlib import Path
import sys

# Quand Python exécute src/etl.py, ajouter la racine aux imports.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from retail_bi.pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline(PROJECT_ROOT, only_five_digits=True)
