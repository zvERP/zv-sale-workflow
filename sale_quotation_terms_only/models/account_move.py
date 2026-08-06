# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("move_type", "partner_id", "company_id")
    def _compute_narration(self):
        """Do not fill invoice terms automatically.

        Odoo uses the same company terms for quotations and customer invoices.
        Keep the standard computation for other move types, while leaving
        customer invoices untouched so manually entered narration is preserved.
        """
        invoice_moves = self.filtered(
            lambda move: move.is_sale_document(include_receipts=True)
        )
        super(AccountMove, self - invoice_moves)._compute_narration()
