# Rapport de synthèse — Retail BI

## Objectif

Explorer, nettoyer et analyser le jeu de données de transactions `Online Retail` pour préparer des indicateurs de pilotage du commerce.

## 1. Exploration des données

Le jeu de données Online Retail contient 541 909 lignes et 8 colonnes. Les variables sont : InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID et Country.

Le diagnostic **enregistré dans ce notebook** indique :

| Indicateur | Valeur observée dans le fichier |
|---|---:|
| Lignes initiales | 541 909 |
| Valeurs CustomerID manquantes | 135 080 |
| Descriptions manquantes | 1 454 |
| Doublons exacts | 5 268 |
| Lignes de facture d'annulation avant déduplication | 9 288 |
| Quantités négatives | 10 624 |
| Prix strictement négatifs | 2 |

## 2. Nettoyage et transformation

Les étapes de nettoyage enregistrées incluent la suppression des doublons, la séparation des annulations, l'exclusion des quantités/prix non positifs et la conservation des références à cinq chiffres.

Après l'exécution du pipeline ETL, nous avons obtenu 472 253 lignes de ventes valides et 9 251 lignes d'annulation. Les données ont été nettoyées, transformées et exportées avec succès.

## 3. KPI enregistrés dans le notebook

| KPI | Résultat sauvegardé |
|---|---:|
| Chiffre d'affaires sur ventes retenues | 9 345 497,67 £ |
| Lignes de ventes | 472 253 |
| Factures distinctes | 19 549 |
| Références produit distinctes | 2 868 |
| Pays distincts | 38 |

Le script `src/etl.py` produit également panier moyen, clients identifiés et volumes, qui seront calculés après dépôt du vrai fichier Excel.

## 4. Analyses complémentaires prévues et automatisées

- Chiffre d'affaires par mois ; graphique `bi/ca_mensuel.png`.
- Chiffre d'affaires par pays ; graphique `bi/ca_par_pays.png`.
- Dix références au plus fort chiffre d'affaires ; graphique `bi/top_produits.png`.
- Base de données SQLite pour réutilisation dans un outil BI et requêtes `sql/analyses.sql`.

## 5. Conclusion

La préparation vise à constituer une base exploitable pour des tableaux de bord de ventes. Les critères de filtrage choisis dans le cours peuvent toutefois exclure des références alphanumériques légitimes. La validation des KPI requiert le fichier Excel original et l'exécution du pipeline.

> **Statut des résultats :** observations reprises du notebook remis, à confirmer par exécution du projet. Aucun nouveau total n'a été inventé.
