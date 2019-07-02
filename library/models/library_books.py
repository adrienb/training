from odoo import api, fields, models
from odoo.exceptions import Warning


class Books(models.Model):
    _inherit = 'product.product'

    isbn = fields.Char('ISBN')
    status = fields.Selection([('available', 'Available'), ('rented', 'Rented')], default='available')
    price = fields.Float('Price')
    rent_ids = fields.One2many('library.rental', 'book_id', string ="Rented")
    total_renters = fields.Integer(compute="_compute_renters")
    is_book = fields.Boolean('is_book')
    is_rented = fields.Boolean('is_rented')

    @api.depends('rent_ids', 'rent_ids.customer_id')
    def _compute_renters(self):
        for rec in self:
                rec.total_renters = len(rec.rent_ids)
    

