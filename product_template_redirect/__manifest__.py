# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Template Redirect",
    "version": "16.0.1.0.0",
    "summary": "Open product templates from sales and invoices",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "zvERP.com",
    "website": "https://zverp.com",
    "depends": ["sale_management", "account", "product"],
    "data": [
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
}
