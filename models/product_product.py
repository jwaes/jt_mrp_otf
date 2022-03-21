import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    task_id = fields.Many2one(
        comodel_name="project.task", string="Task")            
