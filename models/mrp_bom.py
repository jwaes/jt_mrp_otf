import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    bom_line_ids = fields.One2many(tracking=True)

    def update_prices(self):
        for record in self:
            product = record.product_id
            if product:

                old_list_price = product.list_price
                new_list_price = 0.0

                old_purchase_price = 0.0
                new_purchase_price = 0.0

                if product.seller_ids is not None:
                    for seller in product.seller_ids:
                            old_purchase_price = seller.price            

                for bom_line in record.bom_line_ids:
                    line_product = bom_line.product_id
                    _logger.info("BOM line [%s] %s", line_product.default_code, line_product.name)
                    qty = bom_line.product_qty

                    if product.otf_bom_list_price:
                        sale_price = line_product.list_price
                        sale_line_price = qty * sale_price
                        _logger.info(
                            "Sale - {:.2f} * {:.2f} = {:.2f}".format(qty, sale_price, sale_line_price))
                        new_list_price += sale_line_price

                    if product.otf_bom_supplier_price:
                        purchase_price = 0.0
                        if line_product.seller_ids is not None:

                            seller = line_product._select_seller(
                                uom_id=bom_line.product_uom_id)

                            if product.otf_bom_template.subcontractor.id == seller.name.id:
                                purchase_price = seller.price
                                purchase_line_price = qty * purchase_price
                                _logger.info(
                                    "Purchase - {:.2f} * {:.2f} = {:.2f}".format(qty, purchase_price, purchase_line_price))
                                new_purchase_price += purchase_line_price                                    
                            else:
                                _logger.info("Seller %s, is not the subcontractor %s, skipping", seller.name.name, product.otf_bom_template.subcontractor.name )
                        else:
                            raise Exception(
                                'Product has no seller associated', product)


                body = ''

                if product.otf_bom_list_price:
                    _logger.info('Updating sale price')                
                    product.list_price = new_list_price
                    if old_list_price != new_list_price:
                        body += '<p>Sale price has changed from {:.2f} to {:.2f}.</p>'.format(
                            old_list_price, new_list_price)
                    else :
                        _logger.info('Nothing to update')
                else :
                    _logger.info('Not updating sale price')

                if product.otf_bom_supplier_price:
                    _logger.info('Updating purchase price') 
                    for seller in product.seller_ids:
                        # product.seller_ids.price = product_purchase_price
                        seller.price = new_purchase_price
                        if old_purchase_price != new_purchase_price:
                            body += '<p>Purchase price has changed from {:.2f} to {:.2f}.</p>'.format(
                                old_purchase_price, new_purchase_price)
                        else :
                            _logger.info('Nothing to update')                                
                else :
                    _logger.info('Not updating purchase price')                        


                # add chatter
                if body != '':
                    product.message_post(
                        body=body,
                        message_type='notification'
                        )

    def write(self, vals):
        super().write(vals)
        self.update_prices()
        return True
