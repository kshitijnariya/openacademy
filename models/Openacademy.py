# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, models, fields
from odoo.exceptions import ValidationError


class OpenAcademyCourse(models.Model):
    _name = 'openacademy.course'
    _description = 'Training Course'

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    responsible_id = fields.Many2one('res.users', string="Responsible", ondelete="restrict")
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Session")
    login = fields.Char(string="Login", related="responsible_id.login")

    _sql_constraints = [('name_unique',  'unique(name)',  'The name must be unique!!')]
    

    @api.constrains('name', 'description')
    def _check_name_description(self):
        for record in self:
            if record.name == record.description:
                raise ValidationError('Name cannot be same with Description')


class OpenAcademySession(models.Model):
    _name = 'openacademy.session'
    _description = "Training Session"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('instructor', '=', True)])
    start_date = fields.Date(default=fields.Date.today())
    duration = fields.Float()
    seats = fields.Integer()
    course_id = fields.Many2one('openacademy.course', string="Course")
    attendee_ids = fields.Many2many('res.partner', 'session_attendee_rel', 'session_id', 'attendee_id', string="Attendees")
    attendee_count = fields.Integer(string="No. of Attendee", compute="_compute_attendee_count")
    state = fields.Selection([('draft', 'Draft'), 
                              ('confirm', 'Confirm'), 
                              ('delay', 'Delay'),
                              ('cancel', 'Cancel'), 
                              ('done', 'Done')], string="Status", default='draft')

    @api.depends('attendee_ids')
    def _compute_attendee_count(self):   
        for record in self:
            print ("COMPUATE RECORD", record.active)
            record.attendee_count = len(record.attendee_ids)

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_attendee(self):
        for record in self:
            if record.instructor_id in record.attendee_ids:
                raise ValidationError('Instructor cannot be attendee')

    @api.onchange('seats', 'attendee_ids')
    def _onchange_seats(self):
        if self.seats < len(self.attendee_ids):
            return {                                                                                    
                'warning': {
                    'title': 'Warning',
                    'message': 'cannot register more atttendee then total seats!'
                }
            }

    def action_confirm(self):
        self.write({'state': 'confirm'})


class ResPartner(models.Model):
    _inherit = 'res.partner'

    session_ids = fields.Many2many('openacademy.session', 'session_attendee_rel', 'attendee_id', 'session_id', string="Session")
    instructor = fields.Boolean()


class Teachers(models.Model):
    _name = 'academy.teachers'

    name = fields.Char()