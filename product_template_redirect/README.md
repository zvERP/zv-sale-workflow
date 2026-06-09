# Product Template Redirect

This module makes Odoo open the product template directly when a product is opened from sales or invoices.

## What it does

- Extends `product.product` to redirect the open action depending on the context.
- Adds context in sales order and invoice views to force that redirection.
- Applies when opening products from sales lines and invoice or journal lines.
