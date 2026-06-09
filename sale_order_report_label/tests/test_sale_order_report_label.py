from odoo.tests import common


class TestSaleOrderReportLabel(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Report Label Partner"})
        cls.product = cls.env["product.product"].create(
            {"name": "Service Product", "type": "service", "invoice_policy": "order"}
        )

    def _create_sale_order(self, **values):
        order = self.env["sale.order"].create({"partner_id": self.partner.id, **values})
        self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product.id,
                "name": self.product.name,
                "product_uom_qty": 1.0,
                "product_uom": self.product.uom_id.id,
                "price_unit": 100.0,
            }
        )
        return order

    def _render_sale_report_html(self, order):
        report = self.env.ref("sale.action_report_saleorder")
        html, _ = report._render_qweb_html([order.id])
        return html.decode() if isinstance(html, bytes) else html

    def test_01_order_uses_default_report_label(self):
        order = self._create_sale_order()

        self.assertFalse(order.report_document_label)

        report_html = self._render_sale_report_html(order)
        self.assertIn("Quotation #", report_html)
        self.assertIn(order.name, report_html)

    def test_02_order_allows_custom_report_label(self):
        order = self._create_sale_order(report_document_label="Albaran")

        report_html = self._render_sale_report_html(order)
        self.assertIn("Albaran", report_html)
        self.assertNotIn("Delivery note", report_html)

    def test_03_empty_label_falls_back_to_standard_title(self):
        order = self._create_sale_order(report_document_label=False)

        report_html = self._render_sale_report_html(order)
        self.assertIn("Quotation #", report_html)
