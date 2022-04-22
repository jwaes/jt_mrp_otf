import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)    


    otf_bom_template = fields.Many2one('otf.bom.template', string="OTF BOM template")
    otf_bom_list_price = fields.Boolean("BOM based sales price")
    otf_bom_list_price_updated_date = fields.Date('BOM price last calculated')

    @api.depends('list_price', 'price_extra')
    @api.depends_context('uom')
    def _compute_otf_bom_list_price(self):
        # to_uom = None
        # if 'uom' in self._context:
        #     to_uom = self.env['uom.uom'].browse(self._context['uom'])

        # for product in self:
        #     if to_uom:
        #         list_price = product.uom_id._compute_price(product.list_price, to_uom)
        #     else:
        #         list_price = product.list_price
        #     product.lst_price = list_price + product.price_extra
        print("Button clicked ... ")
        prc = 0.0
        bom_count = self.bom_count
        if(bom_count > 0):
            if(bom_count == 1):
                _logger.info("BOM found, going to calculate")
                for bom in self.bom_ids:
                    for bom_line in bom.bom_line_ids:
                        _logger.info("BOM line %s", bom_line.product_id.name)
                        qty = bom_line.product_qty
                        prod_list_price = bom_line.product_id.list_price
                        lineprice = qty * prod_list_price
                        _logger.info("- %s * %s = %s", qty, prod_list_price, lineprice)
                        prc += lineprice
                self.list_price = prc                
                self.otf_bom_list_price_updated_date = fields.Date.today()
            else :
                _logger.warning("More than one BOM found")

        else:
            _logger.warning("No BOM detected, nothing to calculate")


    def otf_btn_bom_list_price(self):
        self._compute_otf_bom_list_price()
