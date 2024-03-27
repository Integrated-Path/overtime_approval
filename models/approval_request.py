# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ApprovalRequest(models.Model):
	_inherit = "approval.request"

	@api.model
	def get_all_overtime_approvals(self):
		overtime_approvals = self.env["approval.request"].search([
			("request_status", "=", "approved"),
			("category_id.overtime_approval", "!=", False),
		])
		return overtime_approvals

	@api.model
	def calculate_employe_overtime_hours_type(
		self,
		employee_id,
		start_date,
		end_date
	):
		overtime_approvals = self.env["approval.request"].get_all_overtime_approvals()
		employee_approvals = overtime_approvals.filtered(
			lambda x:
				x.request_owner_id == employee_id.name and
				x.category_id.overtime_approval == "by-hours" and
				x.date_end.date() >= start_date and
				x.date_end.date() <= end_date
		)
		total_hours = 0
		for approval_id in employee_approvals:
			time_range_time_delta = approval_id.date_end - approval_id.date_start
			time_range_in_hours = time_range_time_delta.seconds / 3600
			total_hours += time_range_in_hours
		return total_hours
		
		
	@api.model
	def calculate_employe_overtime_days_type(
		self,
		employee_id,
		start_date,
		end_date
	):
		if not employee_id.resource_calendar_id:
			raise UserError(f"You need to set a working calendar for the employee {employee_id.name} before calculating its overtime hours")

		hours_per_day = employee_id.resource_calendar_id.hours_per_day
		overtime_approvals = self.env["approval.request"].get_all_overtime_approvals()
		employee_approvals = overtime_approvals.filtered(
			lambda x:
				x.request_owner_id == employee_id.name and
				x.category_id.overtime_approval == "by-days" and
				x.date_end.date() >= start_date and
				x.date_end.date() <= end_date
		)
		total_hours = 0
		for approval_id in employee_approvals:
			time_range_time_delta = approval_id.date_end - approval_id.date_start
			time_range_in_days = time_range_time_delta.days
			total_hours += time_range_in_days * hours_per_day
		return total_hours
