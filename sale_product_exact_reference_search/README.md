# Sale Product Exact Reference Search

When an exact internal reference (`default_code`) exists, product autocomplete
returns only that exact match. As a result, pressing Enter after typing a
complete reference cannot select an earlier partial match.

The rule is applied directly to product searches and does not depend on a
specific sales order view, client context, JavaScript, or web asset cache.
It covers both product variants (`product.product`) and the product-template
selector (`product.template`) displayed by Odoo's sales configurator.

The web autocomplete applies the same exact-reference priority to both models
before handling keyboard selection.
