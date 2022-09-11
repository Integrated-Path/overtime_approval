# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

APPROVAL_SELECTION = [
	("by-hours", "By Hours"),
	("by-days", "By Days"),
]

class OvertimeApproval(models.Model):
	_inherit = "approval.category"

	overtime_approval = fields.Selection(APPROVAL_SELECTION, string="Overtime Approval")

	@api.onchange("overtime_approval")
	def on_overtime_approval_change(self):
		if self.overtime_approval:
			self.has_period = "required"
			self.has_date = "no"