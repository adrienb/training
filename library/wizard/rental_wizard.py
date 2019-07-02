from odoo import api, exceptions, fields, models

class RentalWizard(models.TransientModel):
    _name = 'library.rental_wizard'
    _description = 'Rental wizard'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    book_id = fields.Many2one('product.product', string='Book', required=True)

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        book_id = self.env.context['active_id']
        defaults['book_id'] = book_id
        return defaults


    # @api.multi
    # def button_add(self):
    #     self.session_id.attendee_ids |= self.attendee_ids
    #     return {}
