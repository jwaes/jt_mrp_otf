from odoo import api, fields, models, _

class OtfBomTemplate(models.Model):
    _name = 'otf.bom.template'
    _description = 'OTF BOM Template'

    name = fields.Char("Name", required=True)
    subcontractor = fields.Many2one("res.partner", string="Subcontractor", required=True)
    sequence = fields.Many2one("ir.sequence", required=True)
    categ_id = fields.Many2one(
            'product.category', string='Product Category', required=True)

    def create_otf_bom_product(self):
        next_seq = self.sequence.next_by_code(self.sequence.code)

        product_vals = {
            "name": next_seq,
            "detailed_type": 'product',
            "default_code": next_seq,
            "categ_id": self.categ_id.id,
            "otf_bom_template": self.id,
            "otf_bom_list_price": True,
        }
        product_template = self.env["product.template"].create(product_vals)

        supplier_vals = {
            'product_tmpl_id': product_template.id,
            'name': self.subcontractor.id,
        }
        supplier_info = self.env['product.supplierinfo'].create(supplier_vals)

        bom_vals = {
            'product_tmpl_id': product_template.id,
            'type': 'subcontract',
            'subcontractor_ids': [self.subcontractor.id],
        }
        bom = self.env['mrp.bom'].create(bom_vals)

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