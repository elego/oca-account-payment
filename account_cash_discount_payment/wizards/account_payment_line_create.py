# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPaymentLineCreate(models.TransientModel):

    _inherit = "account.payment.line.create"

    date_type = fields.Selection(
        selection_add=[("discount_due_date", "Discount Due Date")],
        ondelete={"discount_due_date": "cascade"},
    )
    cash_discount_date = fields.Date(
        default=lambda self: fields.Date.today(),
        help="Search lines with a discount due date which is posterior to "
        "the selected date.",
    )

    @api.depends("cash_discount_date")
    def _compute_move_line_domain(self):
        super()._compute_move_line_domain()
        if self.date_type == "discount_due_date":
            self.move_line_domain = self.move_line_domain + [
                ("move_id.discount_due_date", ">=", self.cash_discount_date),
            ]
