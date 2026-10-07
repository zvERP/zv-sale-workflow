# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression


POSITIVE_NAME_SEARCH_OPERATORS = {"=", "ilike", "=ilike", "like", "=like"}


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _prioritize_exact_reference_name_search_results(
        self, name, args, limit, results
    ):
        """Put exact internal-reference matches before partial matches."""
        domain = expression.AND([args or [], [("default_code", "=", name)]])
        exact_products = self.search(domain, limit=limit)
        if not exact_products:
            return results

        exact_results = exact_products.sudo().name_get()
        exact_ids = set(exact_products.ids)
        ordered_results = exact_results + [
            result for result in results if result[0] not in exact_ids
        ]
        return ordered_results[:limit] if limit else ordered_results

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        results = list(
            super().name_search(
                name=name,
                args=args,
                operator=operator,
                limit=limit,
            )
        )
        if not name or operator not in POSITIVE_NAME_SEARCH_OPERATORS:
            return results
        return self._prioritize_exact_reference_name_search_results(
            name, args, limit, results
        )
