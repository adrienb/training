from odoo import api, exceptions, fields, models

class AddAttendee(models.TransientModel):
    _name = 'openacademy.add_attendee'
    _description = 'Add attendee'

    session_id = fields.Many2one('openacademy.session', string="Session", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        attendee_ids = self.env.context['active_ids']
        defaults['attendee_ids'] = attendee_ids
        return defaults


    @api.multi
    def button_add(self):
        self.session_id.attendee_ids |= self.attendee_ids
        return {}
