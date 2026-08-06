# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import common


class TestSaleQuotationTermsOnly(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["ir.config_parameter"].sudo().set_param(
            "account.use_invoice_terms", True
        )
        cls.env.company.terms_type = "plain"
        cls.env.company.invoice_terms = "Default terms for quotations"
        cls.env["account.journal"].create(
            {
                "name": "Terms Test Sales Journal",
                "code": "TST",
                "type": "sale",
                "company_id": cls.env.company.id,
            }
        )
        cls.income_account = cls.env["account.account"].create(
            {
                "code": "700000",
                "name": "Terms Test Income",
                "account_type": "income",
                "company_id": cls.env.company.id,
            }
        )
        cls.receivable_account = cls.env["account.account"].create(
            {
                "code": "430000",
                "name": "Terms Test Receivable",
                "account_type": "asset_receivable",
                "company_id": cls.env.company.id,
                "reconcile": True,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Terms Partner"})
        cls.partner.property_account_receivable_id = cls.receivable_account
        cls.product = cls.env["product.product"].create(
            {"name": "Terms Product", "type": "service", "invoice_policy": "order"}
        )
        cls.product.product_tmpl_id.property_account_income_id = cls.income_account

    def _create_sale_order(self):
        order = self.env["sale.order"].create({"partner_id": self.partner.id})
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

    def test_default_terms_remain_on_quotations(self):
        order = self._create_sale_order()

        self.assertIn("Default terms for quotations", order.note)

    def test_direct_customer_invoice_has_no_default_terms(self):
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Invoice line",
                            "quantity": 1.0,
                            "price_unit": 100.0,
                            "account_id": self.income_account.id,
                        }
                    )
                ],
            }
        )

        self.assertFalse(invoice.narration)

    def test_invoice_created_from_quotation_has_no_terms(self):
        order = self._create_sale_order()
        order.action_confirm()
        invoice = order._create_invoices()

        self.assertFalse(invoice.narration)
