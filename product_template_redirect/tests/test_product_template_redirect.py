# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProductTemplateRedirect(common.TransactionCase):
    def test_redirect_is_enabled_for_sale_and_invoice_documents(self):
        product_model = self.env["product.product"]

        for source_model in (
            "sale.order",
            "sale.order.line",
            "account.move",
            "account.move.line",
        ):
            with self.subTest(source_model=source_model):
                self.assertTrue(
                    product_model.with_context(
                        params={"model": source_model}
                    )._must_open_product_template()
                )

    def test_redirect_is_disabled_outside_supported_documents(self):
        product_model = self.env["product.product"]

        self.assertFalse(product_model._must_open_product_template())
        self.assertFalse(
            product_model.with_context(
                params={"model": "purchase.order"}
            )._must_open_product_template()
        )

    def test_explicit_context_still_enables_redirect(self):
        product_model = self.env["product.product"].with_context(
            open_product_template_from_document=True
        )

        self.assertTrue(product_model._must_open_product_template())
