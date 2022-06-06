# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class OvertimeApproval(models.Model):
	_inherit = "approval.category"
	overtime_approval = fields.Boolean(string="Overtime Approval ?")
	

class HrPayslip(models.Model):
	_inherit = "hr.payslip"

	# env = payslip.env
	# employee_approvals = env["approval.request"].search([
	# 	("request_status", "=", "approved"),
	# 	("category_id.overtime_approval", "=", True),
	# 	("request_owner_id", "=", employee.user_id.id),
	# 	("date_end", ">=", payslip.date_from),
	# 	("date_end", "<=", payslip.date_to),
	# ])
	# total_hours = 0
	# for approval_id in employee_approvals:
	# 	time_range_time_delta = approval_id.date_end - approval_id.date_start
	# 	time_range_in_hours = time_range_time_delta.seconds / 3600
	# 	total_hours += time_range_in_hours

	# result = total_hours * 20

	# TODO: This function isn't working on the payslip rule
	# This needs to be used in place of writing the code directly in the rule
	@property
	def compute_overtime_hours(self) -> float:
		employee_approvals = self.env["approval.request"].search([
			("request_status", "=", "approved"),
			("category_id.overtime_approval", "=", True),
			("request_owner_id", "=", self.employee_id.user_id.id),
			("date_end", ">=", self.date_from),
			("date_end", "<=", self.date_to),
		])
		total_hours = 0
		for approval_id in employee_approvals:
			time_range_time_delta = approval_id.date_end - approval_id.date_start
			time_range_in_hours = time_range_time_delta.seconds / 3600
			total_hours += time_range_in_hours

		return total_hours