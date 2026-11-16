from odoo import models, fields, api

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'

    patient_id = fields.Many2one('hms.patient', ondelete='cascade')

    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    date = fields.Date(default=fields.Date.today)
    description = fields.Text()