# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _must_open_product_template(self):
        context = self.env.context
        if context.get("open_product_template_from_document"):
            return True

        source_model = (context.get("params") or {}).get("model")
        return source_model in {
            "sale.order",
            "sale.order.line",
            "account.move",
            "account.move.line",
        }

    def get_formview_action(self, access_uid=None):
        if len(self) == 1 and self._must_open_product_template():
            return self.product_tmpl_id.get_formview_action(access_uid=access_uid)
        return super().get_formview_action(access_uid=access_uid)
