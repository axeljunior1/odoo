from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auto_barcode_enabled = fields.Boolean(
        string="Enable automatic barcode generation",
        config_parameter="auto_barcode.enabled"
    )

    auto_barcode_prefix = fields.Char(
        string="Barcode prefix",
        config_parameter="auto_barcode.prefix",
        default="20"
    )

    auto_pos_enabled = fields.Boolean(
        string="Automatically add new products to POS",
        config_parameter="auto_barcode.auto_pos"
    )
