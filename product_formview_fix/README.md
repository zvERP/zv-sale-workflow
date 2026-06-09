# Product Form View Fix

This module adjusts product navigation so that, when a product has only one variant, Odoo opens the product template form instead of the variant form.

## What it does

- Extends `product.product`.
- Redirects form opening to `product.template` when the template has a single variant.
- Keeps the standard behavior when the product has multiple variants.
