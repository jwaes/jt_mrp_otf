import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    otf_bom_template = fields.Many2one(
        'otf.bom.template')
    otf_bom_list_price = fields.Boolean(default=True)
    otf_bom_list_price_updated_date = fields.Date('BOM price last calculated')

    otf_bom_supplier_price = fields.Boolean(default=True)
    otf_bom_supplier_price_updated_date = fields.Date()

    @api.depends('list_price', 'price_extra')
    @api.depends_context('uom')
    def _compute_otf_bom_list_price(self):
        print("Button clicked ... ")

        bom_count = self.bom_count
        if(bom_count > 0):
            if(bom_count == 1):
                _logger.info("BOM found, going to calculate")
                for bom in self.bom_ids:
                    bom.update_prices()
            else:
                _logger.warning("More than one BOM found")

        else:
            _logger.warning("No BOM detected, nothing to calculate")

    def otf_btn_bom_list_price(self):
        self._compute_otf_bom_list_price()
