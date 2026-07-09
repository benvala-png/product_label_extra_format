# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    x_last_auto_date = fields.Datetime(
        related='product_tmpl_id.x_last_auto_date', string="Date MAJ auto", readonly=True
    )
    x_last_auto_supplier_id = fields.Many2one(
        related='product_tmpl_id.x_last_auto_supplier_id', string="Fournisseur auto", readonly=True
    )
