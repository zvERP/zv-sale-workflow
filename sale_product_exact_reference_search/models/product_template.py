# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression

from .product_product import POSITIVE_NAME_SEARCH_OPERATORS


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _name_search(
        self,
        name="",
        args=None,
        operator="ilike",
        limit=100,
        name_get_uid=None,
    ):
        """Stop template search as soon as an exact reference is found."""
        if name and operator in POSITIVE_NAME_SEARCH_OPERATORS:
            domain = expression.AND([args or [], [("default_code", "=", name)]])
            exact_ids = self._search(
                domain,
                limit=limit,
                access_rights_uid=name_get_uid,
            )
            if exact_ids:
                return exact_ids

        return super()._name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )
