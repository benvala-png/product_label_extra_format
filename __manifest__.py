{
    'name': 'Product Label Extra Format',
    'version': '16.0.1.0.0',
    'category': 'Inventory',
    'summary': "Format d'étiquette 3x7 avec nom sur une ligne + fournisseur/date auto-pricing en petit",
    'author': 'Benjamin',
    'license': 'LGPL-3',
    'depends': ['product', 'product_auto_pricing'],
    'data': [
        'report/product_label_report_extra.xml',
    ],
    'installable': True,
    'application': False,
}
