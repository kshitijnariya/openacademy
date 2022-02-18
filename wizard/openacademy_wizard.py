# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class OpenAcademyWizard(models.TransientModel):
    _name = 'openacademy.wizard.attendee'

    session_id = fields.Many2one('openacademy.session', string="Session", default=lambda x: x.env.context.get('active_id'))
    attendee_ids = fields.Many2many('res.partner', string="Attendee")


    def register_attendee(self):
        self.session_id.write({'attendee_ids': [(4, attendee.id) for attendee in self.attendee_ids  ] } )