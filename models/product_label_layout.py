# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError

FORMAT_PAIN = '2x6xingredients'


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(
        selection_add=[
            ('3x7xprice', '3 x 7 with price'),
            ('2x4xingredients', "2 x 4 avec ingrédients et allergènes"),
            (FORMAT_PAIN, "2 x 6 pain — ingrédients/allergènes (4 cm)"),
        ],
        ondelete={
            '3x7xprice': 'set default',
            '2x4xingredients': 'set default',
            FORMAT_PAIN: 'set default',
        },
    )

    def _prepare_report_data(self):
        """Vérifier AVANT d'imprimer, pas après : une fiche sans ingrédients
        sortirait une étiquette « Ingrédients : » vide — pire qu'une case
        blanche, ça a l'air d'une déclaration réglementaire. On écarte ces
        fiches du lot plutôt que de bloquer tout le tirage pour une seule —
        `Croissant / pain Choco` n'a par exemple aucune fiche technique en
        ligne depuis toujours (voir product_allergen_labels).
        """
        self.bread_label_skipped = False
        if self.print_format == FORMAT_PAIN:
            cible = self.product_tmpl_ids or self.product_ids.product_tmpl_id
            imprimables = cible.filtered(lambda p: p.ingredients)
            self.bread_label_skipped = ", ".join((cible - imprimables).mapped("name"))
            if not imprimables:
                raise UserError(_(
                    "Aucune des fiches sélectionnées n'a d'ingrédients "
                    "renseignés : rien à imprimer."))
            if self.product_tmpl_ids:
                self.product_tmpl_ids = [(6, 0, imprimables.ids)]
            else:
                self.product_ids = self.product_ids.filtered(
                    lambda p: p.product_tmpl_id in imprimables)
        return super()._prepare_report_data()

    # Un modèle Odoo n'accepte pas d'attribut Python arbitraire sur une
    # instance (AttributeError, testé le 2026-09-15 sur product_shelf_label) :
    # ce qui doit survivre entre `_prepare_report_data` et `process()` doit
    # être un vrai champ. Jamais affiché dans une vue, jamais recopié.
    bread_label_skipped = fields.Char(readonly=True, copy=False)

    def action_print_direct(self):
        resultat = super().action_print_direct()
        # Notifier les fiches écartées faute d'ingrédients — après le tirage,
        # pour ne pas masquer un succès partiel derrière une fausse erreur.
        if self.print_format == FORMAT_PAIN and self.bread_label_skipped:
            params = isinstance(resultat, dict) and resultat.get("params")
            if params and params.get("type") == "success":
                params["message"] += _(
                    "\n\nNon imprimé (pas d'ingrédients renseignés) : %s"
                ) % self.bread_label_skipped
                params["sticky"] = True
        return resultat
