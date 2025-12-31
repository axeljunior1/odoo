import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def create(self, vals):
        # 1️⃣ Ajout automatique au PdV (si param activé)
        self._apply_auto_pos(vals)

        # 2️⃣ Barcode uniquement pour produit SIMPLE (sans variantes)
        if self._should_generate_template_barcode(vals):
            vals["barcode"] = self._generate_barcode()

        product = super().create(vals)
        return product

    def _should_generate_template_barcode(self, vals):
        enabled = self.env["ir.config_parameter"].sudo().get_param(
            "auto_barcode.enabled"
        )

        product_type = (
                vals.get("type")
                or self.env.context.get("default_type")
                or "consu"
        )

        _logger.warning(
            "[AUTO_BARCODE][TEMPLATE] enabled=%s | type=%s | barcode=%s",
            enabled,
            product_type,
            vals.get("barcode"),
        )

        return (
                enabled
                and not vals.get("barcode")
                and product_type == "product"      # stockable
        )

    def _apply_auto_pos(self, vals):
        enabled = self.env["ir.config_parameter"].sudo().get_param(
            "auto_barcode.auto_pos"
        )

        if enabled and not vals.get("available_in_pos"):
            vals["available_in_pos"] = True

    def _generate_barcode(self):
        prefix = self.env["ir.config_parameter"].sudo().get_param(
            "auto_barcode.prefix", "20"
        )
        seq = self.env["ir.sequence"].next_by_code("product.barcode")
        return f"{prefix}{seq}"
