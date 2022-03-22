import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    bom_line_ids = fields.One2many(tracking=True)

    def update_prices(self):
        product = self.product_id
        if product:
            if product.otf_bom_list_price:
                old_price = product.standard_price
                product.button_bom_cost()
                new_price =  product.standard_price

                old_list_price = product.list_price
                product.product_tmpl_id.otf_btn_bom_list_price()
                new_list_price = product.list_price

                # add chatter
                body = '<p>Bom has changed.</p><p>Cost changed from {:.2f} to {:.2f}. Updated the purchase prices accordingly.</p>'.format(old_price, new_price)
                body += '<p>Sales price has changed from {:.2f} to {:.2f}.</p>'.format(old_list_price, new_list_price)
                product.message_post(
                    body=body,
                    message_type='notification'
                )

                supplier_infos = self.env['product.supplierinfo'].search([
                    ('product_id', '=', product.id), ])
                for supplier_info in supplier_infos:
                    supplier_info.price = product.standard_price

    def write(self, vals):
        super().write(vals)
        self.update_prices()
        return True
