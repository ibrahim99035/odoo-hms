from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')

    vat = fields.Char(required=True)

    @api.constrains('related_patient_id')
    def _check_patient_email_unique(self):
        for rec in self:
            if not rec.related_patient_id:
                continue
            patient_email = rec.related_patient_id.email
            if not patient_email:
                continue
            duplicate = self.search([
                ('related_patient_id.email', '=', patient_email),
                ('id', '!=', rec.id),
            ], limit=1)
            if duplicate:
                raise ValidationError(f"The patient's email '{patient_email}' is already linked to another customer ({duplicate.name}).")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise UserError(f"cannot delete customer '{rec.name}' because they are linked to patient: {rec.related_patient_id.first_name} ")
        return super().unlink()