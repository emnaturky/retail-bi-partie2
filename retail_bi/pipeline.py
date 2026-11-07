"""Pipeline reproductible Online Retail : nettoyage, KPI, SQLite et graphiques.

Conventions du TD : les codes produits ne contenant pas exactement cinq chiffres
sont écartés pour l'analyse principale. Ceci constitue un choix pédagogique,
qui élimine aussi certains codes produits alphanumériques légitimes.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_COLUMNS = {
    "InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate",
    "UnitPrice", "CustomerID", "Country"
}


def load_excel(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(
            f"Fichier absent : {path}\nCopie 'Online Retail.xlsx' dans data/raw/."
        )
    data = pd.read_excel(path, dtype={"InvoiceNo": str, "StockCode": str})
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes : {', '.join(sorted(missing))}")
    data["InvoiceNo"] = data["InvoiceNo"].astype("string").str.strip()
    data["StockCode"] = data["StockCode"].astype("string").str.strip()
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")
    return data


def quality_report(data: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Valeurs manquantes": data.isna().sum(),
        "Pourcentage manquant (%)": (data.isna().mean() * 100).round(2),
        "Valeurs distinctes": data.nunique(dropna=True),
    })


def clean_transactions(data: pd.DataFrame, only_five_digits: bool = True):
    clean = data.drop_duplicates().copy()
    clean["InvoiceNo"] = clean["InvoiceNo"].astype("string").str.strip()
    clean["StockCode"] = clean["StockCode"].astype("string").str.strip()
    is_cancelled = clean["InvoiceNo"].str.startswith("C", na=False)
    cancelled = clean.loc[is_cancelled].copy()
    sales = clean.loc[~is_cancelled].copy()
    sales = sales.loc[(sales["Quantity"] > 0) & (sales["UnitPrice"] > 0)].copy()
    if only_five_digits:
        sales = sales.loc[sales["StockCode"].str.fullmatch(r"\d{5}", na=False)].copy()
    sales = sales.loc[sales["InvoiceDate"].notna()].copy()
    # Le code 0 signifie client inconnu, il ne doit PAS être compté comme client réel.
    sales["CustomerID"] = sales["CustomerID"].fillna(0).astype("Int64")
    sales["Description"] = (sales["Description"].fillna("DESCRIPTION INCONNUE")
                            .astype("string").str.strip().str.upper())
    sales["montant"] = sales["Quantity"] * sales["UnitPrice"]
    return sales.reset_index(drop=True), cancelled.reset_index(drop=True)


def calculate_kpis(sales: pd.DataFrame) -> dict:
    invoice_count = int(sales["InvoiceNo"].nunique())
    clients = sales.loc[sales["CustomerID"].ne(0), "CustomerID"]
    return {
        "chiffre_affaires_gbp": round(float(sales["montant"].sum()), 2),
        "lignes_ventes": int(len(sales)),
        "nombre_factures": invoice_count,
        "nombre_produits": int(sales["StockCode"].nunique()),
        "nombre_pays": int(sales["Country"].nunique()),
        "clients_identifies": int(clients.nunique()),
        "quantite_totale": int(sales["Quantity"].sum()),
        "panier_moyen_gbp": (round(float(sales["montant"].sum()) / invoice_count, 2)
                              if invoice_count else 0.0),
    }


def build_marts(sales: pd.DataFrame) -> dict[str,pd.DataFrame]:
    src = sales.copy()
    src["mois"] = pd.to_datetime(src["InvoiceDate"]).dt.to_period("M").astype(str)
    monthly = (src.groupby("mois", as_index=False)["montant"].sum()
               .sort_values("mois"))
    country = (src.groupby("Country", as_index=False)["montant"].sum()
               .sort_values("montant", ascending=False))
    products = (src.groupby(["StockCode", "Description"], as_index=False)
                .agg(montant=("montant", "sum"), quantite=("Quantity", "sum"))
                .sort_values("montant", ascending=False).head(10))
    return {"ca_mensuel": monthly, "ca_par_pays": country, "top_produits": products}


def save_charts(marts: dict[str, pd.DataFrame], out: Path):
    out.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 5))
    monthly = marts["ca_mensuel"]
    ax.plot(monthly["mois"], monthly["montant"], marker="o")
    ax.set(title="Évolution du chiffre d'affaires mensuel", xlabel="Mois", ylabel="CA (£)")
    ax.tick_params(axis="x", labelrotation=45)
    fig.tight_layout()
    fig.savefig(out / "ca_mensuel.png", dpi=150)
    plt.close(fig)

    top = marts["ca_par_pays"].head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top["Country"], top["montant"])
    ax.set(title="Top 10 pays par chiffre d'affaires", xlabel="CA (£)")
    fig.tight_layout()
    fig.savefig(out / "ca_par_pays.png", dpi=150)
    plt.close(fig)

    products = marts["top_produits"].iloc[::-1]
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.barh(products["StockCode"], products["montant"])
    ax.set(title="Top 10 références par chiffre d'affaires", xlabel="CA (£)", ylabel="Code produit")
    fig.tight_layout()
    fig.savefig(out / "top_produits.png", dpi=150)
    plt.close(fig)


def run_pipeline(project_root: Path, only_five_digits: bool = True) -> dict:
    project_root = Path(project_root)
    data_root = project_root / "data"
    raw = data_root / "raw"
    clean = data_root / "clean"
    marts_dir = data_root / "marts"
    bi = project_root / "bi"
    for folder in [raw, clean, marts_dir, bi]:
        folder.mkdir(parents=True, exist_ok=True)
    data = load_excel(raw / "Online Retail.xlsx")
    quality_report(data).to_csv(marts_dir / "qualite_donnees.csv", encoding="utf-8-sig")
    data.to_csv(raw / "online_retail.csv", index=False)
    sales, cancelled = clean_transactions(data, only_five_digits)
    sales.to_csv(clean / "ventes.csv", index=False)
    cancelled.to_csv(clean / "annulations.csv", index=False)
    marts = build_marts(sales)
    for name, table in marts.items():
        table.to_csv(marts_dir / f"{name}.csv", index=False)
    kpis = calculate_kpis(sales)
    (marts_dir / "kpi.json").write_text(json.dumps(kpis, ensure_ascii=False, indent=2), encoding="utf-8")
    with sqlite3.connect(data_root / "retail.db") as connection:
        sales.to_sql("ventes", connection, if_exists="replace", index=False, chunksize=5000)
        cancelled.to_sql("annulations", connection, if_exists="replace", index=False, chunksize=5000)
        for name, table in marts.items():
            table.to_sql(name, connection, if_exists="replace", index=False)
    save_charts(marts, bi)
    stats = {
        "lignes_initiales": len(data),
        "doublons_initiaux": int(data.duplicated().sum()),
        "annulations_apres_dedoublonnage": len(cancelled),
        **kpis,
    }
    print("\n=== BILAN RETAIL BI ===")
    for k, v in stats.items():
        print(f"{k} : {v}")
    print("\nExports : data/clean, data/marts, data/retail.db et bi/*.png")
    return stats
