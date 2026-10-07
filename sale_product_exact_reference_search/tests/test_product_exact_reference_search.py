# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests import common


class TestProductExactReferenceSearch(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.exact_product = cls.env["product.product"].create(
            {"name": "Exact product", "default_code": "ZVTEST-785"}
        )
        cls.partial_product = cls.env["product.product"].create(
            {"name": "Partial product", "default_code": "PRE-ZVTEST-785-POST"}
        )

    def test_priority_is_scoped_to_sales(self):
        products = self.env["product.product"]

        self.assertFalse(products._must_prioritize_exact_reference())
        self.assertTrue(
            products.with_context(
                params={"model": "sale.order"}
            )._must_prioritize_exact_reference()
        )
        self.assertFalse(
            products.with_context(
                params={"model": "purchase.order"}
            )._must_prioritize_exact_reference()
        )

    def test_sale_product_fields_enable_exact_reference_priority(self):
        view = self.env["sale.order"].get_view(
            view_id=self.env.ref("sale.view_order_form").id,
            view_type="form",
        )
        arch = etree.fromstring(view["arch"].encode())
        product_fields = arch.xpath(
            "//field[@name='order_line']/*[self::form or self::tree]"
            "//field[@name='product_id']"
        )

        self.assertEqual(len(product_fields), 2)
        for product_field in product_fields:
            self.assertIn(
                "'prioritize_exact_reference': True",
                product_field.get("context"),
            )

    def test_exact_reference_is_moved_before_partial_matches(self):
        initial_results = [
            (self.partial_product.id, "[PRE-ZVTEST-785-POST] Partial product"),
        ]

        results = (
            self.env["product.product"]
            .with_context(prioritize_exact_reference=True)
            ._prioritize_exact_reference_name_search_results(
                "ZVTEST-785", [], 100, initial_results
            )
        )

        self.assertEqual(results[0][0], self.exact_product.id)
        self.assertEqual(results[1][0], self.partial_product.id)

    def test_exact_reference_respects_search_domain(self):
        results = (
            self.env["product.product"]
            .with_context(prioritize_exact_reference=True)
            ._prioritize_exact_reference_name_search_results(
                "ZVTEST-785",
                [("id", "!=", self.exact_product.id)],
                100,
                [
                    (
                        self.partial_product.id,
                        "[PRE-ZVTEST-785-POST] Partial product",
                    )
                ],
            )
        )

        self.assertEqual(
            results,
            [
                (
                    self.partial_product.id,
                    "[PRE-ZVTEST-785-POST] Partial product",
                )
            ],
        )

    def test_name_search_finds_exact_reference_first(self):
        results = (
            self.env["product.product"]
            .with_context(prioritize_exact_reference=True)
            .name_search(name="ZVTEST-785", operator="ilike", limit=100)
        )

        self.assertEqual(results[0][0], self.exact_product.id)
