import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    bom_line_ids = fields.One2many(tracking=True)

    def update_prices(self):
        product = self.product_id
        if product:
            if product.otf_bom_list_price is not None:
                old_price = product.standard_price
                product.button_bom_cost()
                new_price =  product.standard_price

                old_list_price = product.list_price
                product.product_tmpl_id.otf_btn_bom_list_price()
                new_list_price = product.list_price

                # for seller in product.seller_ids:
                #     blah = seller
                product_purchase_price = 0.0
                old_purchase_price = 0.0

                if product.seller_ids is not None:
                    if len(product.seller_ids) > 1:
                        raise Exception('Found multiple sellers for this product, do not know how to handle this', bom_product)
                    else:
                        for seller in product.seller_ids:
                            old_purchase_price = seller.price

                else:
                    raise Exception('Product has no seller associated', product)
                
                

                if product.bom_count > 2:
                    raise Exception('Found more than one BOM for this product ... i do not know how to handle this.')
                if product.bom_count == 0:
                    raise Exception('BOM not found ... cannot calculate a purchase price')
                for bom in product.bom_ids:
                    for bom_line in bom.bom_line_ids:
                        bom_product = bom_line
                        _logger.info("BOM line %s", bom_line.product_id.name)
                        qty = bom_line.product_qty
                        purchase_price = 0.0
                        if bom_line.product_id.seller_ids is not None:
                            seller_ids = bom_line.product_id.seller_ids                            
                            if len(seller_ids) > 1:
                                raise Exception('Found multiple sellers for this product, do not know how to handle this', bom_product)
                            else:
                                for seller in seller_ids:
                                    purchase_price = seller.price
                        else:
                            raise Exception('Did not find a seller for this product ', bom_product)
                        bom_lineprice = qty * purchase_price
                        product_purchase_price += bom_lineprice
                
                for seller in product.seller_ids:
                    product.seller_ids.price = product_purchase_price                  

                # add chatter
                body = '<p>Bom has changed.</p><p>Purchase price changed from {:.2f} to {:.2f}. Updated the purchase prices accordingly.</p>'.format(old_purchase_price, product_purchase_price)
                body += '<p>Sales price has changed from {:.2f} to {:.2f}.</p>'.format(old_list_price, new_list_price)
                product.message_post(
                    body=body,
                    message_type='notification'
                )

    def write(self, vals):
        super().write(vals)
        self.update_prices()
        return True
