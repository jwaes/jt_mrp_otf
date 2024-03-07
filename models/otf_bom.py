import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class OtfBomTemplate(models.Model):
    _name = 'otf.bom.template'
    _description = 'OTF BOM Template'

    def _default_pricelist_id(self):
        return self.env['product.pricelist'].search([
            '|', ('company_id', '=', False),
            ('company_id', '=', self.env.company.id)], limit=1)

    name = fields.Char("Name", required=True)
    subcontractor = fields.Many2one(
        "res.partner", string="Subcontractor", required=True)
    subcontractor_delay = fields.Integer("Delivery Lead Time", default=1)
    buy_route_id = fields.Many2one("stock.route", required=True)
    dropship = fields.Boolean("Dropship", required=True, default=False)
    dropship_route_id = fields.Many2one("stock.route")
    sequence = fields.Many2one("ir.sequence", required=True)
    categ_id = fields.Many2one(
            'product.category', string='Product Category', required=True)
    project_ids = fields.One2many(
        'project.project', 'otf_bom_template_id', string="projects using this template")
    calculate_sale_price = fields.Boolean(default=False)
    calculate_purchase_price = fields.Boolean(default=False)
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', required=True, default=_default_pricelist_id)

    def update_related_products(self):
        _logger.info("Going to update them all")
        templates = self.env['product.template'].search([('otf_bom_template', '=', self.id),])
        for tmpl in templates:
            _logger.info("[%s] %s", tmpl.default_code, tmpl.name)
            tmpl._compute_otf_bom_list_price()

    def create_otf_bom_product_and_go(self):
        bom = self.create_otf_bom_product()
        view = self.env.ref("mrp.mrp_bom_form_view")
        return {
            "name": "BOM created",
            "view_mode": "form",
            "view_id": view.id,
            "res_model": "mrp.bom",
            "type": "ir.actions.act_window",
            "res_id": bom.id,
            "context": self.env.context,
        }

    def create_otf_bom_product(self):
        next_seq = self.sequence.next_by_code(self.sequence.code)

        product_vals = {
            "name": next_seq,
            "detailed_type": 'product',
            "default_code": next_seq,
            "categ_id": self.categ_id.id,
            "otf_bom_template": self.id,
            "otf_bom_list_price": self.calculate_sale_price,
            "otf_bom_supplier_price": self.calculate_purchase_price,
            # "partner_id": self.task_id.partner_id.id,
        }

        if self.dropship:
            _logger.info(
                 "The template has requested to set the dropship route")
            
            if self.dropship_route_id:
                _logger.info("")
                product_vals['route_ids'] = [self.buy_route_id.id, self.dropship_route_id.id]
            else:
                _logger.warning("Requested Dropship ... but dropship route not found ... is the option enabled ?")

        product = self.env["product.product"].create(product_vals)

        supplier_vals = {
            'product_id': product.id,
            'product_tmpl_id': product.product_tmpl_id.id,
            'partner_id': self.subcontractor.id,
            'delay': self.subcontractor_delay,
        }
        supplier_info = self.env['product.supplierinfo'].create(supplier_vals)

        bom_vals = {
            'product_id': product.id,
            'product_tmpl_id': product.product_tmpl_id.id,
            'type': 'subcontract',
            'subcontractor_ids': [self.subcontractor.id],
        }
        bom = self.env['mrp.bom'].create(bom_vals)

        # add chatter
        body = 'Created OTF BOM ' + bom.display_name
        product.message_post(
            body=body,
            message_type='notification'
        )
        return bom
