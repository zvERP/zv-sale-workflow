# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo import api, models
from odoo.osv import expression


POSITIVE_NAME_SEARCH_OPERATORS = {"=", "ilike", "=ilike", "like", "=like"}
REFERENCE_PREFIX_PATTERN = re.compile(r"^\[([^]]+)]")
SALE_PRODUCT_CONTEXT_KEYS = {
    "company_id",
    "partner_id",
    "pricelist",
    "quantity",
    "uom",
}


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _must_prioritize_exact_reference(self):
        if self.env.context.get("prioritize_exact_reference"):
            return True
        source_model = (self.env.context.get("params") or {}).get("model")
        if source_model in {"sale.order", "sale.order.line"}:
            return True
        return SALE_PRODUCT_CONTEXT_KEYS.issubset(self.env.context)

    @api.model
    def _get_displayed_reference(self, name_get_result):
        display_name = name_get_result[1].split("\n", 1)[0].strip()
        match = REFERENCE_PREFIX_PATTERN.match(display_name)
        return match.group(1) if match else False

    @api.model
    def _prioritize_exact_reference_name_search_results(
        self, name, args, limit, results
    ):
        """Put exact displayed or internal references before partial matches."""
        displayed_exact_results = [
            result
            for result in results
            if self._get_displayed_reference(result) == name
        ]
        if displayed_exact_results:
            exact_ids = {result[0] for result in displayed_exact_results}
            ordered_results = displayed_exact_results + [
                result for result in results if result[0] not in exact_ids
            ]
            return ordered_results[:limit] if limit else ordered_results

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
        if (
            not name
            or operator not in POSITIVE_NAME_SEARCH_OPERATORS
            or not self._must_prioritize_exact_reference()
        ):
            return results
        return self._prioritize_exact_reference_name_search_results(
            name, args, limit, results
        )
