# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestProductExactReferenceSearch(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.exact_product = cls.env["product.product"].create(
            {"name": "VITALAIT TOP 60", "default_code": "785"}
        )
        cls.partial_product = cls.env["product.product"].create(
            {"name": "ESSENTIAL CAT MIXI 3KG", "default_code": "17857395"}
        )
        cls.other_partial_product = cls.env["product.product"].create(
            {"name": "SUELO PLASTICO", "default_code": "10785"}
        )

    def test_exact_reference_respects_search_domain(self):
        results = dict(
            self.env["product.product"]
            .name_search(
                name="785",
                args=[("id", "!=", self.exact_product.id)],
                operator="ilike",
                limit=100,
            )
        )

        self.assertNotIn(self.exact_product.id, results)
        self.assertIn(self.partial_product.id, results)
        self.assertIn(self.other_partial_product.id, results)

    def test_name_search_returns_only_exact_reference(self):
        results = (
            self.env["product.product"]
            .name_search(name="785", operator="ilike", limit=100)
        )

        self.assertEqual([result[0] for result in results], [self.exact_product.id])

    def test_sale_product_template_search_returns_only_exact_reference(self):
        results = self.env["product.template"].name_search(
            name="785",
            args=[("sale_ok", "=", True)],
            operator="ilike",
            limit=100,
        )

        self.assertEqual(
            [result[0] for result in results],
            [self.exact_product.product_tmpl_id.id],
        )

    def test_name_search_keeps_partial_search_without_exact_reference(self):
        results = dict(
            self.env["product.product"].name_search(
                name="1785", operator="ilike", limit=100
            )
        )

        self.assertIn(self.partial_product.id, results)
