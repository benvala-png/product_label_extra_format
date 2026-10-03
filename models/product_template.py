# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Mots clés de dégustation des vins, imprimés sur l'étiquette 2 x 6 à la
    # place des ingrédients. Relevés chez le producteur (ou sur Vivino), JAMAIS
    # rédigés de tête : la source est gardée à côté pour pouvoir le vérifier.
    x_mots_cles_vin = fields.Char(
        string="Mots clés (vin)",
        help="5 mots clés au plus, séparés par des virgules. Imprimés sur "
             "l'étiquette « Pain / Vin — 2 x 6 », sous le nom.")
    x_mots_cles_source = fields.Char(
        string="Source des mots clés",
        help="Page du producteur (ou de Vivino) d'où viennent les mots clés.")
