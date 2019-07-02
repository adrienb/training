from odoo import api, fields, models
from odoo.exceptions import Warning


class Customers(models.Model):
    _inherit = 'res.partner'


    owed_money = fields.Float(compute="_compute_owed_money", store=True)
    rent_ids = fields.One2many('library.rental', 'customer_id', string="Rented")
    
    # book_ids = fields.Many2many('product.product', compute='_compute_book_list')

    @api.depends('rent_ids')
    def _compute_owed_money(self):
        for rec in self:
            for rent in rec.rent_ids:
                rec.owed_money += rent.price

    # def _compute_book_list(self):
    #     for rec in self:
    #         for rent in rec.rent_ids:
    #             rec.book_ids = (4, rent.book_id.id, _)
    #             # rec.book_ids = (6, _, [rent.book_id].ids)
    #             # rec.book_ids = (5, _, _)
    #             # rec.book_ids = (3, rent.book_id.id, _)
    

        



