import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for product in records:
            if product._should_generate_variant_barcode():
                barcode = product._generate_barcode()
                product.barcode = barcode

                _logger.warning(
                    "[AUTO_BARCODE][VARIANT] product_id=%s | barcode=%s",
                    product.id,
                    barcode,
                )

        return records

    def _should_generate_variant_barcode(self):
        enabled = self.env["ir.config_parameter"].sudo().get_param(
            "auto_barcode.enabled"
        )

        _logger.warning(
            "[AUTO_BARCODE][CHECK VARIANT] enabled=%s | type=%s | barcode=%s | variants=%s",
            enabled,
            self.type,
            self.barcode,
            len(self.product_tmpl_id.product_variant_ids),
        )

        return (
                enabled
                and not self.barcode
                and self.type == "product"                      # stockable
                and self.product_tmpl_id
                and len(self.product_tmpl_id.product_variant_ids) > 1
        )

    def _generate_barcode(self):
        prefix = self.env["ir.config_parameter"].sudo().get_param(
            "auto_barcode.prefix", "20"
        )
        seq = self.env["ir.sequence"].next_by_code("product.barcode")
        return f"{prefix}{seq}"
