from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
import re

class HmsPatient(models.Model):
    _name = 'hms.patient'
    

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    email = fields.Char(required=True)

    birth_date = fields.Date(required=True)
    
    history = fields.Html()
    cr_ratio = fields.Float()
    
    blood_type = fields.Selection([('a+', 'A+'), ('b+', 'B+'), ('o+', 'O+'), ('ab+', 'AB+')])
    
    pcr = fields.Boolean()
    
    image = fields.Binary()
    
    address = fields.Text()
    
    age = fields.Integer(compute='_compute_age', store=True)

    state = fields.Selection([
        ('undetermined', 'Undetermined'), ('good', 'Good'), ('fair', 'Fair'), ('serious', 'Serious'),
    ], default='undetermined')

    department_id = fields.Many2one('hms.department', domain="[('is_opened', '=', True)]")

    department_capacity = fields.Integer(related='department_id.capacity', readonly=True)

    doctor_ids = fields.Many2many('hms.doctor', 'patient_doctor_rel', 'patient_id', 'doctor_id', string='Doctors')

    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='History Log')

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = (date.today() - rec.birth_date).days // 365
            else:
                rec.age = 0

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Auto-Checked',
                    'message': 'PCR has been automatically checked because age is under 30.'
                }
            }

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is mandatory when PCR is checked!")

    @api.constrains('email')
    def _check_email(self):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for rec in self:
            if rec.email and not re.match(email_pattern, rec.email):
                raise ValidationError("Invalid email format!")

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'The email must be unique!'),
    ]

    @api.onchange('state')
    def _onchange_state(self):
        if self.state:
            log_entry = (0, 0, {
                'created_by': self.env.user.id,
                'date': date.today(),
                'description': f'State changed to {dict(self._fields["state"].selection).get(self.state)}'
            })
            self.log_ids = [log_entry]
