# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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

    def test_exact_reference_is_moved_before_partial_matches(self):
        initial_results = [
            (self.partial_product.id, "[PRE-ZVTEST-785-POST] Partial product"),
        ]

        results = (
            self.env["product.product"]
            ._prioritize_exact_reference_name_search_results(
                "ZVTEST-785", [], 100, initial_results
            )
        )

        self.assertEqual(results[0][0], self.exact_product.id)
        self.assertEqual(results[1][0], self.partial_product.id)

    def test_exact_reference_respects_search_domain(self):
        results = (
            self.env["product.product"]
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
            .name_search(name="ZVTEST-785", operator="ilike", limit=100)
        )

        self.assertEqual(results[0][0], self.exact_product.id)
