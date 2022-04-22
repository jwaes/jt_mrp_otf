import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    task_id = fields.Many2one(
        comodel_name="project.task", string="Task")            

    def otf_btn_bom_list_price(self):
        self._compute_otf_bom_list_price()

    def _compute_bom_price(self, bom, boms_to_recompute=False, byproduct_bom=False):
        # remove the price again for our special subcontracting stuff
        price = super()._compute_bom_price(bom, boms_to_recompute, byproduct_bom)
        if self.otf_bom_list_price and bom and bom.type == 'subcontract':
            seller = self._select_seller(quantity=bom.product_qty, uom_id=bom.product_uom_id, params={'subcontractor_ids': bom.subcontractor_ids})
            if seller:
                price -= seller.product_uom._compute_price(seller.price, self.uom_id)
        return price