{
    'name': 'Product Label Extra Format',
    'version': '16.0.1.3.0',
    'category': 'Inventory',
    'summary': "Formats d'étiquette supplémentaires : 3x7 (nom sur une ligne + "
               "fournisseur/date auto-pricing), 2x4 et 2x8 (pain, 3 cm) avec "
               "ingrédients et allergènes, mini 8x10 sans code-barres",
    'author': 'Benjamin',
    'license': 'LGPL-3',
    'depends': ['product', 'product_auto_pricing', 'product_allergen',
                'product_label_direct_print'],
    'data': [
        'report/product_label_report_extra.xml',
        'report/product_label_ingredients.xml',
        'report/product_label_bread.xml',
        'report/product_label_mini.xml',
    ],
    'installable': True,
    'application': False,
}
