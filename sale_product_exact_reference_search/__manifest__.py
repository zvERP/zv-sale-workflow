# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Product Exact Reference Search",
    "version": "16.0.1.0.4",
    "summary": "Prioritize exact product references on sales order lines",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "zvERP.com",
    "website": "https://zverp.com",
    "depends": ["sale_management"],
    "assets": {
        "web.assets_backend": [
            "sale_product_exact_reference_search/static/src/js/"
            "exact_reference_autocomplete.js",
        ],
        "web.qunit_suite_tests": [
            "sale_product_exact_reference_search/static/tests/"
            "exact_reference_autocomplete_tests.js",
        ],
    },
    "installable": True,
}
