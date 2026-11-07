"""Tests autonomes (sans le fichier Online Retail.xlsx)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from retail_bi.pipeline import clean_transactions, calculate_kpis, quality_report, build_marts


def sample():
    return pd.DataFrame({
        "InvoiceNo": ["100", "100", "C101", "102", "103", "104", "105", "106", "107"],
        "StockCode": ["12345", "12345", "12345", "12345", "POST", "12345", "54321", "54321", "99999"],
        "Description": ["test", "test", "test", "test", "Postage", "test", None, "second", "free"],
        "Quantity": [2, 2, -2, -4, 1, 3, 1, 2, 1],
        "InvoiceDate": pd.to_datetime(["2011-01-01"] * 9),
        "UnitPrice": [5, 5, 5, 5, 4, -1, 3, 2, 0],
        "CustomerID": [111, 111, 111, 111, 111, 111, None, 112, 112],
        "Country": ["France"] * 9,
    })


def test_cleaning():
    raw = sample()
    assert int(raw.duplicated().sum()) == 1
    sales, cancelled = clean_transactions(raw)
    assert len(cancelled) == 1
    assert len(sales) == 3
    assert sales["montant"].sum() == 17
    assert sales["CustomerID"].isna().sum() == 0
    assert int(sales.duplicated().sum()) == 0
    assert sales["Description"].isna().sum() == 0


def test_kpis_and_marts():
    sales, _ = clean_transactions(sample())
    kpi = calculate_kpis(sales)
    assert kpi["chiffre_affaires_gbp"] == 17
    assert kpi["nombre_factures"] == 3
    assert kpi["clients_identifies"] == 2
    assert len(build_marts(sales)["ca_mensuel"]) == 1


def test_quality_report():
    q = quality_report(sample())
    assert q.loc["CustomerID", "Valeurs manquantes"] == 1
