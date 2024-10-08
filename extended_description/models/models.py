# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	extended_description = fields.Text()


class ProductProduct(models.Model):
	_inherit = 'product.product'

	extended_description = fields.Text(related='product_tmpl_id.extended_description', string="Extended Description", store=True)


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	@api.model
	def create(self, vals):
		sale_order_line = super(SaleOrderLine, self).create(vals)
		if sale_order_line.product_id:
			product_template = sale_order_line.product_id.product_tmpl_id
			if product_template.extended_description:
				self.env['sale.order.line'].create({
					'order_id': sale_order_line.order_id.id,
					'display_type': 'line_note',
					'name': product_template.extended_description,
				})
		return sale_order_line
