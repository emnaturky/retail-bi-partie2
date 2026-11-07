# Méthodologie de préparation

## Source et périmètre

Le jeu de données source est Online Retail.xlsx. Il contient 541 909 transactions et 8 colonnes. Les données ont été chargées et analysées avec Python et Pandas.

## Étapes du notebook initial

1. Lecture Excel et inspection de la structure.
2. Détection des valeurs manquantes, doublons, prix/quantités négatifs et factures annulées (`InvoiceNo` commençant par `C`).
3. Déduplication ; séparation des factures annulées.
4. Suppression des montants/quantités non positifs.
5. Conservation des codes produits à cinq chiffres (règle de l'exercice).
6. Remplacement des `CustomerID` manquants par 0 ; normalisation des descriptions ; calcul du montant (`Quantity * UnitPrice`).
7. Calcul des KPI sur les ventes retenues ; analyses mensuelle, géographique et par produit.

## Points de vigilance

- **Annulations :** les lignes annulées sont exportées séparément et ne contribuent pas au chiffre d'affaires brut retenu.
- **Codes produits :** un identifiant tel que `85123A` n'a pas cinq chiffres ; cette règle du TD l'exclut même s'il peut s'agir d'un vrai article. Vérifier avec la professeure si les codes alphanumériques doivent être conservés dans un autre scénario.
- **Client inconnu :** `CustomerID=0` est une catégorie de données manquantes, pas un client ; exclure 0 pour le nombre de clients distincts.
- **Description :** les descriptions absentes encore présentes dans les lignes retenues sont remplacées par `DESCRIPTION INCONNUE` dans le pipeline automatique.
- **Performance :** l'import Excel de plus de 500 000 lignes peut prendre du temps ; une fois exportés, les CSV sont plus rapides à ouvrir.
