# -*- coding: utf-8 -*-
{
    "name": "Product Form View Fix",
    "summary": "Redirect product.product to product.template when there is only one variant",
    "description": """
        Adjusts product navigation so that clicking a product from
        sale.order.line or other models opens the product.template form
        instead of product.product when the product has only one variant.
    """,
    "version": "16.0.1.0.0",
    "category": "Sales",
    "author": "zvERP",
    "website": "http://www.zverp.com",
    "license": "LGPL-3",
    "depends": ["product"],
    "installable": True,
    "auto_install": False,
}
