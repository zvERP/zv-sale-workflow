from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    report_document_label = fields.Char(
        string="Report title",
        translate=True,
        help=(
            "Editable title shown before the order number in the printed report. "
            "If empty, the report will use the standard Odoo title."
        ),
    )
