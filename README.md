# Retail BI — Projet de TP (structure de la professeure)

Projet Python / Pandas / Matplotlib / SQLite d'exploration et de préparation des données **Online Retail**. L'arborescence suit les captures d'écran envoyées : `retail_bi/` à la racine et `src/etl.py` séparé. Le notebook de la séance constitue la base du travail. 

## 1. Arborescence

```text
retail-bi/
├── .venv/                         # généré localement par uv sync ; non inclus dans le ZIP
├── bi/                            # graphiques PNG, après exécution
├── data/
│   ├── clean/                     # ventes.csv, annulations.csv (générés automatiquement)
│   ├── cleans/                    # conservé pour correspondre à la capture ; NON utilisé
│   ├── marts/                     # KPI + agrégations mensuelles/pays/produits
│   ├── raw/                       # placer Online Retail.xlsx ici
│   └── retail.db                  # SQLite initialisée vide ; remplie par le script ETL
├── docs/
│   ├── 01_exploration_original.txt
│   ├── rapport.md
│   └── methodologie.md
├── notebooks/
│   ├── 01_exploration.ipynb
│   └── 02_kpi_visualisations.ipynb
├── retail_bi/
│   ├── __init__.py
│   └── pipeline.py                # fonctions de traitement
├── sql/
│   └── analyses.sql
├── src/
│   └── etl.py                     # lance le pipeline
├── tests/
│   └── test_pipeline.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock                       # généré automatiquement après uv sync (pas inclus)
```

## 2. Lancer dans VS Code sous Windows

1. Décompresser le ZIP. Ouvrir le dossier **retail-bi** (pas un dossier parent) via `File > Open Folder`.
2. Copier votre **vrai fichier** `Online Retail.xlsx` dans `data/raw/`. Il n'est **pas inclus** dans cette archive.
3. Ouvrir `Terminal > New Terminal`. Se placer dans `retail-bi` si nécessaire.
4. Installer les dépendances, puis exécuter le pipeline :

   ```bash
   uv sync
   uv run python src/etl.py
   ```

   Si `uv` est absent, l'installer selon les consignes du cours. Lors du premier `uv sync`, UV crée `.venv/` et `uv.lock` automatiquement. Pour lancer les notebooks, choisir le kernel de `.venv` (Python 3.12 recommandé), puis cliquer sur **Run All**.
5. Ouvrir `notebooks/01_exploration.ipynb`, exécuter les cellules **dans l'ordre**. Ensuite ouvrir `notebooks/02_kpi_visualisations.ipynb`.
6. Tester avec `uv run pytest -q`.

### Résultat attendu après exécution

- `data/clean/ventes.csv` et `data/clean/annulations.csv` ;
- `data/marts/qualite_donnees.csv`, `ca_mensuel.csv`, `ca_par_pays.csv`, `top_produits.csv`, `kpi.json` ;
- `data/retail.db` contenant les tables SQLite ;
- `bi/ca_mensuel.png`, `bi/ca_par_pays.png`, `bi/top_produits.png`.

### Notes sur la méthode

- Le notebook original détecte **541 909 lignes** et **5 268 doublons** ; il sauvegarde **472 253 ventes après filtrage**. Les autres résultats sont indiqués dans `docs/rapport.md`. Ces nombres **proviennent du notebook fourni**, pas d'une nouvelle exécution ici.
- Comme dans la séance, les codes StockCode conservés sont **exactement 5 chiffres** (c'est une convention pédagogique qui supprime aussi certaines références réelles alphanumériques).
- Les `CustomerID` vides sont remplacés par `0` (client inconnu, exclu des clients identifiés).
- Le dossier `data/cleans` apparaît dans tes captures, mais le cours utilise `data/clean` : nous le laissons vide pour préserver l'arborescence sans produire de doublons.
- `data/retail.db` est initialisée **sans données** pour apparaître comme dans les captures ; elle est remplacée par les vraies tables une fois `uv run python src/etl.py` terminé.
- La base et les fichiers de données sont ignorés par Git pour éviter d'envoyer les gros fichiers sur GitHub.
