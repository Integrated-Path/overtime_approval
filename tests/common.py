import datetime
from odoo.addons.hr_payroll.tests.common import TestPayslipContractBase, TestPayslipBase

class TestOvertimeApprovalBase(TestPayslipBase):

	@classmethod
	def setUpClass(cls):
		super(TestOvertimeApprovalBase, cls).setUpClass()
		cls.admin_user = cls.env.ref("base.user_admin")
		def create_related_user():
			cls.richard_user = cls.env["res.users"].create({
				"name": "Richard",
				"login": "richard",
				"employee_ids": [(4, cls.richard_emp.id, False)]
			})
		create_related_user()

		def create_salary_rules():
			hour_overtime_code = """
				total_hours = env["approval.request"].calculate_employe_overtime_hours_type(
					employee.user_id.id,
					payslip.date_from,
					payslip.date_to
				)
				result = total_hours * (contract.wage / 30 / 8)
			"""
			cls.hours_overtime_rule = cls.env['hr.salary.rule'].create({
				'name': 'Hours Overtime Rule',
				'sequence': 120,
				'amount_select': 'code',
				'amount_python_compute': hour_overtime_code,
				'quantity': 'worked_days.WORK100 and worked_days.WORK100.number_of_days',
				'code': 'HOT',
				'category_id': cls.env.ref('hr_payroll.ALW').id,
				'struct_id': cls.developer_pay_structure.id,
			})

			days_overtime_code = """
				total_hours = env["approval.request"].calculate_employe_overtime_days_type(
					employee.user_id.id,
					payslip.date_from,
					payslip.date_to
				)
				result = total_hours * (contract.wage / 30 / 8)
			"""
			cls.days_overtime_rule = cls.env['hr.salary.rule'].create({
				'name': 'Days Overtime Rule',
				'sequence': 120,
				'amount_select': 'code',
				'amount_python_compute': days_overtime_code,
				'quantity': 'worked_days.WORK100 and worked_days.WORK100.number_of_days',
				'code': 'DOT',
				'category_id': cls.env.ref('hr_payroll.ALW').id,
				'struct_id': cls.developer_pay_structure.id,
			})
		create_salary_rules()

		def create_approval_categories():
			cls.hours_overtime_category = cls.env["approval.category"].create({
				"name": "Hours Overtime",
				"overtime_approval": "by-hours",
				"has_period": "required",
				"approver_ids": [
					(0, 0, {
						"user_id": cls.admin_user.id
					})
				]
			})

			cls.days_overtime_category = cls.env["approval.category"].create({
				"name": "Days Overtime",
				"overtime_approval": "by-days",
				"has_period": "required",
				"approver_ids": [
					(0, 0, {
						"user_id": cls.env.ref("base.user_admin").id
					})
				]
			})
		create_approval_categories()	