-- À exécuter après : uv run python src/etl.py
-- SQLite : tables ventes, annulations, ca_mensuel, ca_par_pays, top_produits

-- 1) KPI généraux
SELECT COUNT(*) AS lignes_ventes,
       COUNT(DISTINCT InvoiceNo) AS nombre_factures,
       COUNT(DISTINCT StockCode) AS nombre_produits,
       COUNT(DISTINCT Country) AS nombre_pays,
       ROUND(SUM(montant), 2) AS chiffre_affaires_gbp
FROM ventes;

-- 2) Chiffre d'affaires mensuel
SELECT mois, ROUND(montant, 2) AS chiffre_affaires_gbp
FROM ca_mensuel ORDER BY mois;

-- 3) Top pays
SELECT Country, ROUND(montant, 2) AS chiffre_affaires_gbp
FROM ca_par_pays ORDER BY montant DESC LIMIT 10;

-- 4) Top produits
SELECT StockCode, Description, ROUND(montant, 2) AS chiffre_affaires_gbp
FROM top_produits ORDER BY montant DESC;

-- 5) Nombre de commandes identifiées par pays
SELECT Country, COUNT(DISTINCT InvoiceNo) AS factures
FROM ventes GROUP BY Country ORDER BY factures DESC LIMIT 10;
