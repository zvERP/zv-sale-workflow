# Sale Product Exact Reference Search

Prioritizes an exact internal reference (`default_code`) match in product
autocomplete results. As a result, pressing Enter after typing a complete
reference selects that product instead of an earlier partial match.

The ordering is applied directly to product searches and does not depend on a
specific sales order view or client context.

The web autocomplete also enforces the same ordering before keyboard selection,
so other server-side search customizations cannot place partial matches first.
