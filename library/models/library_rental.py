# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    book_id = fields.Many2one('product.product', string='Book', required=True)

    book_name = fields.Char(related='book_id.name')
    customer_name = fields.Char(related='customer_id.name')
    price = fields.Float('Price')



