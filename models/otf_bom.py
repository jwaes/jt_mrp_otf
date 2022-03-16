from odoo import api, fields, models, _

class OtfBomTemplate(models.Model):
    _name = 'otf.bom.template'
    _description = 'OTF BOM Template'

    name = fields.Char("Name", required=True)
    subcontractor = fields.Many2one("res.partner", string="subcontractor")
    sequence = fields.Many2one("ir.sequence")