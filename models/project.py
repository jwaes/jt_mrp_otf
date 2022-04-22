import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    otf_bom_template_id = fields.Many2one('otf.bom.template', string="related OTF BOM Template")
