from odoo import models, fields, api
from datetime import date

class HmsDepartment(models.Model):
    _name = 'hms.department'
    _rec_name = 'name'

    name = fields.Char(required=True)
    capacity = fields.Integer()
    is_opened = fields.Boolean()

    patients = fields.One2many('hms.patient', 'department_id', string='Patients')

    doctors = fields.Many2many('hms.doctor', 'department_doctor_rel', 'department_id', 'doctor_id', string='Doctors')
