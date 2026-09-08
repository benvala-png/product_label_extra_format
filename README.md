# product_label_extra_format (Odoo 16)

Addon Odoo 16 qui ajoute deux formats supplémentaires à l'assistant standard
d'impression d'étiquettes produit : **3×7** (nom sur une ligne + fournisseur/
date auto-pricing en petit) et **2×4 avec ingrédients et allergènes**
(étiquette d'affichage frigo/vrac, sans code-barres).

---

## Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Format **3×7** (`3x7xprice`) | Étiquette produit classique avec code-barres, dimensionnée pour rester lisible au lecteur sans fil ; affiche en petit le dernier fournisseur/date d'auto-pricing |
| Format **2×4 ingrédients** (`2x4xingredients`) | Étiquette d'**affichage** (frigo à fromage, bacs de vrac) : pas de code-barres ni de référence, toute la place va au nom, à l'origine, aux ingrédients (allergènes en gras) et aux traces possibles |
| Taille de texte adaptative | Le bloc ingrédients/origine/traces redescend en taille de police par paliers selon la longueur du texte, plutôt que de tronquer une mention obligatoire |

---

## Installation

1. Copier le dossier `product_label_extra_format` dans un répertoire présent dans `addons_path`
2. **Dépendances non incluses dans Odoo** : `product_auto_pricing` et `product_allergen` doivent être installés avant
3. Redémarrer Odoo
4. **Apps > Mettre à jour la liste des applications**
5. Rechercher `Product Label Extra Format` et cliquer sur **Installer**

---

## Utilisation

Depuis l'assistant standard d'impression d'étiquettes (**Imprimer les
étiquettes** sur une liste de produits), le champ **Format** propose en plus
« 3 x 7 with price » et « 2 x 4 avec ingrédients et allergènes ». S'utilise
avec `product_label_direct_print` pour l'impression directe, ou par
téléchargement PDF classique.

Le format 2×4 lit `product._get_ingredients_html()` (module
`product_allergen`) pour la mise en gras des allergènes déclarés, exigée par
le règlement (UE) n°1169/2011.

---

## Champs ajoutés

### `product.label.layout` (assistant, transient)

| Champ | Type | Description |
|---|---|---|
| `print_format` | Selection (extension) | Ajoute `3x7xprice` et `2x4xingredients` aux formats standard |

### `product.product`

| Champ | Type | Description |
|---|---|---|
| `x_last_auto_date` | Datetime (related) | Reprend `product_auto_pricing`, affiché en petit sur l'étiquette 3×7 |
| `x_last_auto_supplier_id` | Many2one (related) | Idem, fournisseur retenu |

---

## Utilisé par / dépend de

- **`product_auto_pricing`** — fournit `x_last_auto_date` / `x_last_auto_supplier_id` affichés sur le format 3×7
- **`product_allergen`** — fournit `ingredients`, `allergen_trace_ids`, `allergen_origin` et `_get_ingredients_html()` pour le format 2×4
- **`product_label_direct_print`** — les deux formats s'impriment par son bouton « Imprimer »

---

## Structure du module

```
product_label_extra_format/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── product_label_layout.py       # Ajoute les deux entrées au champ print_format
│   └── product_product.py            # Champs related fournisseur/date auto-pricing
└── report/
    ├── product_label_report_extra.xml    # Gabarit 3x7 + réglages code-barres
    └── product_label_ingredients.xml     # Gabarit 2x4 ingrédients/allergènes
```

---

## Pièges connus (format 3×7 — code-barres)

**L'alignement pixel-image / point-imprimante n'est pas une question
d'échelle CSS.** Le Canon TS7450i rastérise à 600 dpi. Le gabarit de planche
reste au format papier « A4 Label Sheet » à **96 dpi**, donc wkhtmltopdf
raisonne en pixels CSS et **arrondit la largeur à l'entier** — demander une
largeur en millimètres réintroduit un rééchantillonnage non entier de
l'image du code-barres, avec des barres qui sortent tantôt sur 7, tantôt sur
8 ou 9 points (28,6 % d'écart mesuré), illisibles pour un lecteur imageur.

La solution : exprimer la largeur directement en pixels CSS ronds qui
correspondent à un compte de points entier à 600 dpi — **144 px = 900
points**, et générer l'image du code-barres en 900 px. Un pixel de l'image =
un point de l'imprimante. Les deux nombres (largeur CSS, largeur de
l'image) doivent toujours être changés ensemble. Ce réglage vise l'EAN-13
(2255 codes sur 2390 au catalogue) ; les codes courts en Code128 ont un
alignement moins précis mais une densité trois à quatre fois moindre, la
marge y reste confortable.

Voir aussi les options d'impression posées par `product_label_direct_print`
(noir et blanc, pas de mise à l'échelle CUPS) : les deux correctifs vont
ensemble.

## Pièges connus (format 2×4 — nom du produit)

`product.template` ignore le contexte `display_default_code` (contrairement
à `product.product`) : sur un template, `display_name` préfixerait le nom de
la référence interne. D'où le repli explicite sur `product.name` quand
`is_product_variant` est faux.
