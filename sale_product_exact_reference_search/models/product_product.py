# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression


POSITIVE_NAME_SEARCH_OPERATORS = {"=", "ilike", "=ilike", "like", "=like"}


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """Return only exact internal-reference matches when they exist."""
        if name and operator in POSITIVE_NAME_SEARCH_OPERATORS:
            domain = expression.AND([args or [], [("default_code", "=", name)]])
            exact_products = self.search(domain, limit=limit)
            if exact_products:
                return exact_products.sudo().name_get()

        return super().name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
        )
