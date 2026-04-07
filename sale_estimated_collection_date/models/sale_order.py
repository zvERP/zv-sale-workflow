from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    estimated_collection_date = fields.Date(string="Fecha estimada de cobro")

    def action_confirm(self):
        for order in self:
            if not order.estimated_collection_date:
                raise ValidationError(
                    _(
                        "Debes indicar la 'Fecha estimada de cobro' antes de confirmar el pedido de venta."
                    )
                )
        return super().action_confirm()
