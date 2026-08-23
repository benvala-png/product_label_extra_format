{
    'name': 'Product Label Extra Format',
    'version': '16.0.1.1.0',
    'category': 'Inventory',
    'summary': "Formats d'étiquette supplémentaires : 3x7 (nom sur une ligne + "
               "fournisseur/date auto-pricing) et 2x4 avec ingrédients et allergènes",
    'author': 'Benjamin',
    'license': 'LGPL-3',
    'depends': ['product', 'product_auto_pricing', 'product_allergen'],
    'data': [
        'report/product_label_report_extra.xml',
        'report/product_label_ingredients.xml',
    ],
    'installable': True,
    'application': False,
}
